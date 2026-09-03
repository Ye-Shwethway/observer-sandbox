from __future__ import annotations

import copy

import pytest

from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_cleanup import (
    SandboxLocationCleanupError,
    delete_sandbox_location_v2,
    location_delete_dependencies,
)
from observer_sandbox.sandbox_location_operations import location_source_fingerprint, update_sandbox_location_v2
from observer_sandbox.sandbox_location_v2 import materialize_sandbox_location_v2


def _payload(*, key: str, name: str, kind: str = "room"):
    payload = manual_location_template()
    payload["identity"].update({
        "key": key,
        "name": name,
        "kind": kind,
        "description": f"Cleanup fixture for {name}",
    })
    return payload


def test_location_cleanup_deletes_unreferenced_location_without_canonical_mutation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(
            conn,
            _payload(key="place.cleanup.empty", name="Empty Room"),
        )
        before = canonical_state_fingerprint(conn)

        result = delete_sandbox_location_v2(
            conn,
            location["object_id"],
            expected_source_fingerprint=location_source_fingerprint(location["source"]),
        )

        assert result["deleted"] is True
        assert result["canonical_unchanged"] is True
        assert conn.execute(
            "SELECT count(*) FROM creation_sandbox_objects WHERE object_id=?",
            (location["object_id"],),
        ).fetchone()[0] == 0
        assert conn.execute(
            "SELECT count(*) FROM creation_sandbox_location_profiles WHERE object_id=?",
            (location["object_id"],),
        ).fetchone()[0] == 0
        assert canonical_state_fingerprint(conn) == before


def test_location_cleanup_rejects_active_child_dependency_before_writes(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        parent = materialize_sandbox_location_v2(
            conn,
            _payload(key="place.cleanup.parent", name="Parent House", kind="building"),
        )
        child_payload = _payload(key="place.cleanup.child", name="Child Room")
        child_payload["structure"]["parent_ref"] = parent["object_id"]
        child = materialize_sandbox_location_v2(conn, child_payload)
        before = canonical_state_fingerprint(conn)

        dependencies = location_delete_dependencies(conn, parent["object_id"])
        assert any(
            value["object_id"] == child["object_id"] and value["reason"] == "structural parent"
            for value in dependencies
        )

        with pytest.raises(SandboxLocationCleanupError, match="active dependency"):
            delete_sandbox_location_v2(
                conn,
                parent["object_id"],
                expected_source_fingerprint=location_source_fingerprint(parent["source"]),
            )

        assert conn.execute(
            "SELECT count(*) FROM creation_sandbox_objects WHERE object_id=?",
            (parent["object_id"],),
        ).fetchone()[0] == 1
        assert canonical_state_fingerprint(conn) == before


def test_location_cleanup_stale_review_is_rejected_and_location_remains(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(
            conn,
            _payload(key="place.cleanup.stale", name="Stale Room"),
        )
        reviewed_fingerprint = location_source_fingerprint(location["source"])
        proposal = copy.deepcopy(location["source"])
        proposal["identity"]["name"] = "Changed After Review"
        update_sandbox_location_v2(
            conn,
            location["object_id"],
            proposal,
            expected_source_fingerprint=reviewed_fingerprint,
        )

        with pytest.raises(SandboxLocationCleanupError, match="changed since delete review"):
            delete_sandbox_location_v2(
                conn,
                location["object_id"],
                expected_source_fingerprint=reviewed_fingerprint,
            )

        row = conn.execute(
            "SELECT identity_json FROM creation_sandbox_objects WHERE object_id=?",
            (location["object_id"],),
        ).fetchone()
        assert row is not None
        assert "Changed After Review" in row["identity_json"]

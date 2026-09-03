from __future__ import annotations

import copy

import pytest

from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_operations import (
    SandboxLocationOperationError,
    location_source_fingerprint,
    update_sandbox_location_v2,
)
from observer_sandbox.sandbox_location_v2 import materialize_sandbox_location_v2


def test_location_update_revalidates_and_rewrites_projection_without_canonical_mutation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        parent_payload = manual_location_template()
        parent_payload["identity"].update({
            "key": "place.parent.house",
            "name": "Parent House",
            "kind": "building",
            "description": "Parent building",
        })
        parent = materialize_sandbox_location_v2(conn, parent_payload)

        child_payload = manual_location_template()
        child_payload["identity"].update({
            "key": "place.child.room",
            "name": "Old Room",
            "kind": "room",
            "description": "Old room",
        })
        child = materialize_sandbox_location_v2(conn, child_payload)
        before_canonical = canonical_state_fingerprint(conn)

        proposal = copy.deepcopy(child["source"])
        proposal["identity"]["name"] = "Updated Room"
        proposal["identity"]["description"] = "Updated through Location edit service"
        proposal["structure"]["parent_ref"] = parent["object_id"]
        proposal["facilities"]["capabilities"] = ["rest"]

        updated = update_sandbox_location_v2(
            conn,
            child["object_id"],
            proposal,
            expected_source_fingerprint=location_source_fingerprint(child["source"]),
        )

        assert updated["source"]["identity"]["name"] == "Updated Room"
        assert updated["source"]["structure"]["parent_ref"] == parent["object_id"]
        assert updated["source"]["facilities"]["capabilities"] == ["rest"]
        relation = conn.execute(
            "SELECT source_object_id,relation_type FROM creation_sandbox_relations WHERE target_object_id=? AND relation_type='contains'",
            (child["object_id"],),
        ).fetchone()
        assert relation is not None
        assert relation["source_object_id"] == parent["object_id"]
        event = conn.execute(
            "SELECT event_type FROM creation_sandbox_events WHERE object_id=? ORDER BY id DESC LIMIT 1",
            (child["object_id"],),
        ).fetchone()
        assert event["event_type"] == "sandbox_location_v2_updated"
        assert canonical_state_fingerprint(conn) == before_canonical


def test_location_update_rejects_stale_source_and_keeps_approved_state(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        payload = manual_location_template()
        location = materialize_sandbox_location_v2(conn, payload)
        proposal = copy.deepcopy(location["source"])
        proposal["identity"]["name"] = "First Edit"
        updated = update_sandbox_location_v2(
            conn,
            location["object_id"],
            proposal,
            expected_source_fingerprint=location_source_fingerprint(location["source"]),
        )

        stale_proposal = copy.deepcopy(location["source"])
        stale_proposal["identity"]["name"] = "Stale Edit"
        with pytest.raises(SandboxLocationOperationError, match="changed since edit started"):
            update_sandbox_location_v2(
                conn,
                location["object_id"],
                stale_proposal,
                expected_source_fingerprint=location_source_fingerprint(location["source"]),
            )
        current = conn.execute(
            "SELECT source_json FROM creation_sandbox_location_profiles WHERE object_id=?",
            (location["object_id"],),
        ).fetchone()
        assert "First Edit" in current["source_json"]
        assert "Stale Edit" not in current["source_json"]
        assert updated["source"]["identity"]["name"] == "First Edit"


def test_location_update_rejects_identity_key_change_and_self_parent_cycle(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(conn, manual_location_template())
        fingerprint = location_source_fingerprint(location["source"])

        changed_key = copy.deepcopy(location["source"])
        changed_key["identity"]["key"] = "place.changed.key"
        with pytest.raises(SandboxLocationOperationError, match="identity key is immutable"):
            update_sandbox_location_v2(
                conn,
                location["object_id"],
                changed_key,
                expected_source_fingerprint=fingerprint,
            )

        self_parent = copy.deepcopy(location["source"])
        self_parent["structure"]["parent_ref"] = location["object_id"]
        with pytest.raises(SandboxLocationOperationError, match="structural cycle"):
            update_sandbox_location_v2(
                conn,
                location["object_id"],
                self_parent,
                expected_source_fingerprint=fingerprint,
            )


def test_location_update_rejects_invalid_cross_sandbox_graph_target_before_writes(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(conn, manual_location_template())
        before = copy.deepcopy(location["source"])
        proposal = copy.deepcopy(before)
        proposal["structure"]["parent_ref"] = "sbx_location_missing"

        with pytest.raises(SandboxLocationOperationError, match="same Sandbox"):
            update_sandbox_location_v2(
                conn,
                location["object_id"],
                proposal,
                expected_source_fingerprint=location_source_fingerprint(before),
            )
        current = conn.execute(
            "SELECT source_json FROM creation_sandbox_location_profiles WHERE object_id=?",
            (location["object_id"],),
        ).fetchone()
        assert current is not None
        assert "sbx_location_missing" not in current["source_json"]


def test_location_update_preserves_unrelated_incoming_topology_projection(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        target_payload = manual_location_template()
        target_payload["identity"].update({
            "key": "place.topology.target",
            "name": "Target Room",
            "kind": "room",
            "description": "Target room",
        })
        target = materialize_sandbox_location_v2(conn, target_payload)

        source_payload = manual_location_template()
        source_payload["identity"].update({
            "key": "place.topology.source",
            "name": "Source Room",
            "kind": "room",
            "description": "Source room",
        })
        source_payload["topology"]["interfaces"] = [{
            "key": "door_to_target",
            "name": "Door to target",
            "kind": "door",
            "destination_ref": target["object_id"],
            "directionality": "outbound",
            "enabled": True,
            "traversal_modes": ["walk"],
            "base_duration_minutes": 1.0,
            "distance": None,
        }]
        source = materialize_sandbox_location_v2(conn, source_payload)
        before_relation = conn.execute(
            "SELECT id FROM creation_sandbox_relations WHERE source_object_id=? AND target_object_id=? AND relation_type='connected_to'",
            (source["object_id"], target["object_id"]),
        ).fetchone()
        assert before_relation is not None

        proposal = copy.deepcopy(target["source"])
        proposal["identity"]["name"] = "Edited Target Room"
        update_sandbox_location_v2(
            conn,
            target["object_id"],
            proposal,
            expected_source_fingerprint=location_source_fingerprint(target["source"]),
        )

        after_relation = conn.execute(
            "SELECT id FROM creation_sandbox_relations WHERE source_object_id=? AND target_object_id=? AND relation_type='connected_to'",
            (source["object_id"], target["object_id"]),
        ).fetchone()
        assert after_relation is not None

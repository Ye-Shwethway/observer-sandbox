from __future__ import annotations

import copy

import pytest

from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_cleanup import (
    SandboxLocationCleanupError,
    delete_sandbox_location_v2,
)
from observer_sandbox.sandbox_location_operations import (
    SandboxLocationOperationError,
    location_source_fingerprint,
    update_sandbox_location_v2,
)
from observer_sandbox.sandbox_location_v2 import (
    get_sandbox_location_v2,
    materialize_sandbox_location_v2,
)


def _location_payload(*, key: str, name: str):
    payload = manual_location_template()
    payload["identity"].update({
        "key": key,
        "name": name,
        "kind": "building",
        "description": f"A represented Location named {name}.",
    })
    return payload


def test_location_update_canonical_guard_runs_inside_writer_transaction(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    import observer_sandbox.sandbox_location_operations as operations

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(
            conn,
            _location_payload(key="place.transaction.update", name="Original House"),
        )
        proposal = copy.deepcopy(location["source"])
        proposal["identity"]["name"] = "Edited House"

        original_fingerprint = operations.canonical_state_fingerprint
        transaction_states: list[bool] = []

        def tracked_fingerprint(connection):
            transaction_states.append(bool(connection.in_transaction))
            return original_fingerprint(connection)

        monkeypatch.setattr(operations, "canonical_state_fingerprint", tracked_fingerprint)

        updated = update_sandbox_location_v2(
            conn,
            location["object_id"],
            proposal,
            expected_source_fingerprint=location_source_fingerprint(location["source"]),
        )

        assert updated["source"]["identity"]["name"] == "Edited House"
        assert transaction_states == [True, True]


def test_location_update_rolls_back_sandbox_and_canonical_when_transaction_causes_canonical_mutation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        conn.execute("CREATE TABLE canonical_probe(id TEXT PRIMARY KEY, value TEXT NOT NULL)")
        conn.execute("INSERT INTO canonical_probe(id,value) VALUES('probe','stable')")
        conn.commit()

        location = materialize_sandbox_location_v2(
            conn,
            _location_payload(key="place.transaction.rollback", name="Stable House"),
        )
        object_id = location["object_id"]
        conn.execute(
            f"""
            CREATE TRIGGER force_canonical_mutation_after_location_update
            AFTER UPDATE ON creation_sandbox_objects
            WHEN NEW.object_id='{object_id}'
            BEGIN
                UPDATE canonical_probe SET value='mutated' WHERE id='probe';
            END
            """
        )
        conn.commit()

        proposal = copy.deepcopy(location["source"])
        proposal["identity"]["name"] = "Should Roll Back"

        with pytest.raises(SandboxLocationOperationError, match="Canonical Real World changed"):
            update_sandbox_location_v2(
                conn,
                object_id,
                proposal,
                expected_source_fingerprint=location_source_fingerprint(location["source"]),
            )

        current = get_sandbox_location_v2(conn, object_id)
        probe = conn.execute("SELECT value FROM canonical_probe WHERE id='probe'").fetchone()
        assert current["source"]["identity"]["name"] == "Stable House"
        assert probe["value"] == "stable"
        event = conn.execute(
            "SELECT 1 FROM creation_sandbox_events WHERE object_id=? AND event_type='sandbox_location_v2_updated'",
            (object_id,),
        ).fetchone()
        assert event is None


def test_location_delete_canonical_guard_runs_inside_writer_transaction(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    import observer_sandbox.sandbox_location_cleanup as cleanup

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(
            conn,
            _location_payload(key="place.transaction.delete", name="Disposable House"),
        )

        original_fingerprint = cleanup.canonical_state_fingerprint
        transaction_states: list[bool] = []

        def tracked_fingerprint(connection):
            transaction_states.append(bool(connection.in_transaction))
            return original_fingerprint(connection)

        monkeypatch.setattr(cleanup, "canonical_state_fingerprint", tracked_fingerprint)

        deleted = delete_sandbox_location_v2(
            conn,
            location["object_id"],
            expected_source_fingerprint=location_source_fingerprint(location["source"]),
        )

        assert deleted["deleted"] is True
        assert deleted["canonical_unchanged"] is True
        assert transaction_states == [True, True]


def test_location_delete_rolls_back_if_transaction_causes_canonical_mutation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        conn.execute("CREATE TABLE canonical_probe(id TEXT PRIMARY KEY, value TEXT NOT NULL)")
        conn.execute("INSERT INTO canonical_probe(id,value) VALUES('probe','stable')")
        conn.commit()

        location = materialize_sandbox_location_v2(
            conn,
            _location_payload(key="place.transaction.delete.rollback", name="Keep House"),
        )
        object_id = location["object_id"]
        conn.execute(
            f"""
            CREATE TRIGGER force_canonical_mutation_after_location_delete
            AFTER DELETE ON creation_sandbox_objects
            WHEN OLD.object_id='{object_id}'
            BEGIN
                UPDATE canonical_probe SET value='mutated' WHERE id='probe';
            END
            """
        )
        conn.commit()

        with pytest.raises(SandboxLocationCleanupError, match="Canonical Real World changed"):
            delete_sandbox_location_v2(
                conn,
                object_id,
                expected_source_fingerprint=location_source_fingerprint(location["source"]),
            )

        current = get_sandbox_location_v2(conn, object_id)
        probe = conn.execute("SELECT value FROM canonical_probe WHERE id='probe'").fetchone()
        assert current["source"]["identity"]["name"] == "Keep House"
        assert probe["value"] == "stable"

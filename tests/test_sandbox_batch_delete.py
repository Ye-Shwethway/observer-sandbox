from __future__ import annotations

import sqlite3

import pytest

from observer_sandbox.creation_sandbox import DEFAULT_SANDBOX_ID, CreationSandboxError, canonical_state_fingerprint
from observer_sandbox.db import migrate
from observer_sandbox.sandbox_batch_delete import delete_sandbox_objects


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    migrate(conn)
    conn.execute("INSERT INTO creation_sandboxes(sandbox_id,label,status,revision) VALUES(?,?, 'active', 1)", (DEFAULT_SANDBOX_ID, "Test"))
    conn.commit()
    return conn


def _object(conn, object_id: str, creation_type: str, name: str) -> None:
    conn.execute(
        """INSERT INTO creation_sandbox_objects(
            object_id,sandbox_id,creation_type,schema_version,lifecycle_status,identity_json,properties_json,relationships_json,capabilities_json,provenance_json
        ) VALUES(?,?,?,1,'active',json_object('name', ?),'{}','[]','[]','{}')""",
        (object_id, DEFAULT_SANDBOX_ID, creation_type, name),
    )
    if creation_type == "character":
        conn.execute("INSERT INTO creation_sandbox_actor_runtime(object_id,sandbox_id,activation_status) VALUES(?,?, 'created')", (object_id, DEFAULT_SANDBOX_ID))
    conn.commit()


def test_batch_delete_mixed_character_and_item_preserves_canonical_state():
    conn = _conn()
    _object(conn, "char_seed", "character", "Seed")
    _object(conn, "item_old", "item", "Old Item")
    conn.execute(
        """INSERT INTO creation_sandbox_item_definitions(
        sandbox_id,definition_key,schema_version,name,kind,description,stackable,mobility
        ) VALUES(?,?,?,?,?,?,0,'movable')""",
        (DEFAULT_SANDBOX_ID, "old.item", "item-v1", "Old Item", "equipment", "old"),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_item_instances(object_id,sandbox_id,definition_key,instance_mode) VALUES(?,?,?,'unique')",
        ("item_old", DEFAULT_SANDBOX_ID, "old.item"),
    )
    conn.commit()
    before = canonical_state_fingerprint(conn)

    result = delete_sandbox_objects(conn, ["char_seed", "item_old"])

    assert result["deleted_count"] == 2
    assert result["canonical_unchanged"] is True
    assert conn.execute("SELECT count(*) FROM creation_sandbox_objects").fetchone()[0] == 0
    assert conn.execute("SELECT count(*) FROM creation_sandbox_item_definitions WHERE definition_key='old.item'").fetchone()[0] == 0
    assert canonical_state_fingerprint(conn) == before


def test_batch_delete_keeps_shared_definition_when_instance_remains():
    conn = _conn()
    _object(conn, "item_a", "item", "A")
    _object(conn, "item_b", "item", "B")
    conn.execute(
        """INSERT INTO creation_sandbox_item_definitions(
        sandbox_id,definition_key,schema_version,name,kind,description,stackable,mobility
        ) VALUES(?,?,?,?,?,?,0,'movable')""",
        (DEFAULT_SANDBOX_ID, "shared", "item-v1", "Shared", "equipment", "shared"),
    )
    conn.executemany(
        "INSERT INTO creation_sandbox_item_instances(object_id,sandbox_id,definition_key,instance_mode) VALUES(?,?,?,'unique')",
        [("item_a", DEFAULT_SANDBOX_ID, "shared"), ("item_b", DEFAULT_SANDBOX_ID, "shared")],
    )
    conn.commit()

    delete_sandbox_objects(conn, ["item_a"])

    assert conn.execute("SELECT count(*) FROM creation_sandbox_item_definitions WHERE definition_key='shared'").fetchone()[0] == 1
    assert conn.execute("SELECT count(*) FROM creation_sandbox_objects WHERE object_id='item_b'").fetchone()[0] == 1


def test_batch_delete_rejects_locations_before_mutation():
    conn = _conn()
    _object(conn, "loc_keep", "location", "Keep")
    with pytest.raises(CreationSandboxError, match="Characters and Items only"):
        delete_sandbox_objects(conn, ["loc_keep"])
    assert conn.execute("SELECT count(*) FROM creation_sandbox_objects WHERE object_id='loc_keep'").fetchone()[0] == 1

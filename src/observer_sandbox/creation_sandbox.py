from __future__ import annotations

import hashlib
import json
import sqlite3
import uuid
from typing import Any, Mapping

from .creation_socket import validate_creation_proposal


DEFAULT_SANDBOX_ID = "creator-default"
DEFAULT_SANDBOX_LABEL = "Creator Sandbox"


class CreationSandboxError(ValueError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _loads(value: str, fallback: Any) -> Any:
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


def ensure_sandbox(
    conn: sqlite3.Connection,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    *,
    label: str = DEFAULT_SANDBOX_LABEL,
) -> dict[str, Any]:
    sandbox_id = str(sandbox_id or "").strip()
    if not sandbox_id:
        raise CreationSandboxError("Sandbox id is required")
    conn.execute(
        """
        INSERT INTO creation_sandboxes(sandbox_id,label,status,revision)
        VALUES(?,?,'active',1)
        ON CONFLICT(sandbox_id) DO NOTHING
        """,
        (sandbox_id, label),
    )
    conn.commit()
    row = conn.execute(
        "SELECT sandbox_id,label,status,revision,created_at,updated_at FROM creation_sandboxes WHERE sandbox_id=?",
        (sandbox_id,),
    ).fetchone()
    if row is None:
        raise CreationSandboxError("Unable to initialize Creation Sandbox")
    return dict(row)


def _new_object_id(conn: sqlite3.Connection, creation_type: str) -> str:
    for _ in range(8):
        candidate = f"sbx_{creation_type}_{uuid.uuid4().hex[:16]}"
        canonical = conn.execute("SELECT 1 FROM entities WHERE id=?", (candidate,)).fetchone()
        sandbox = conn.execute(
            "SELECT 1 FROM creation_sandbox_objects WHERE object_id=?", (candidate,)
        ).fetchone()
        if canonical is None and sandbox is None:
            return candidate
    raise CreationSandboxError("Unable to allocate collision-free sandbox object id")


def _row_to_object(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "object_id": str(row["object_id"]),
        "sandbox_id": str(row["sandbox_id"]),
        "creation_type": str(row["creation_type"]),
        "schema_version": int(row["schema_version"]),
        "lifecycle_status": str(row["lifecycle_status"]),
        "identity": _loads(row["identity_json"], {}),
        "properties": _loads(row["properties_json"], {}),
        "relationships": _loads(row["relationships_json"], []),
        "capabilities": _loads(row["capabilities_json"], []),
        "provenance": _loads(row["provenance_json"], {}),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def activate_creation_proposal(
    conn: sqlite3.Connection,
    proposal: Mapping[str, Any],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    normalized = validate_creation_proposal(proposal)
    sandbox = ensure_sandbox(conn, sandbox_id)
    if sandbox["status"] != "active":
        raise CreationSandboxError("Creation Sandbox is archived")
    object_id = _new_object_id(conn, normalized["creation_type"])
    conn.execute(
        """
        INSERT INTO creation_sandbox_objects(
            object_id,sandbox_id,creation_type,schema_version,lifecycle_status,
            identity_json,properties_json,relationships_json,capabilities_json,provenance_json
        ) VALUES(?,?,?,?, 'active', ?,?,?,?,?)
        """,
        (
            object_id,
            sandbox_id,
            normalized["creation_type"],
            normalized["schema_version"],
            _json(normalized["identity"]),
            _json(normalized["properties"]),
            _json(normalized["relationships"]),
            _json(normalized["capabilities"]),
            _json(normalized["provenance"]),
        ),
    )
    if normalized["creation_type"] == "character":
        conn.execute(
            """
            INSERT INTO creation_sandbox_actor_runtime(object_id,sandbox_id,activation_status)
            VALUES(?,?,'created')
            ON CONFLICT(object_id) DO NOTHING
            """,
            (object_id, sandbox_id),
        )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
        (
            sandbox_id,
            object_id,
            "sandbox_object_activated",
            _json({"creation_type": normalized["creation_type"]}),
        ),
    )
    conn.commit()
    return get_sandbox_object(conn, object_id)


def get_sandbox_object(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    row = conn.execute(
        "SELECT * FROM creation_sandbox_objects WHERE object_id=?", (object_id,)
    ).fetchone()
    if row is None:
        raise CreationSandboxError(f"Unknown sandbox object: {object_id}")
    result = _row_to_object(row)
    relations = conn.execute(
        """
        SELECT relation_type,target_object_id,metadata_json
        FROM creation_sandbox_relations
        WHERE sandbox_id=? AND source_object_id=?
        ORDER BY id
        """,
        (result["sandbox_id"], object_id),
    ).fetchall()
    result["resolved_relations"] = [
        {
            "relation_type": str(value["relation_type"]),
            "target_object_id": str(value["target_object_id"]),
            "metadata": _loads(value["metadata_json"], {}),
        }
        for value in relations
    ]
    return result


def list_sandbox_objects(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    include_archived: bool = False,
) -> list[dict[str, Any]]:
    ensure_sandbox(conn, sandbox_id)
    sql = "SELECT * FROM creation_sandbox_objects WHERE sandbox_id=?"
    params: list[Any] = [sandbox_id]
    if not include_archived:
        sql += " AND lifecycle_status='active'"
    sql += " ORDER BY created_at, object_id"
    return [_row_to_object(row) for row in conn.execute(sql, params).fetchall()]


def bind_sandbox_character_to_location(
    conn: sqlite3.Connection,
    character_object_id: str,
    location_object_id: str,
) -> dict[str, Any]:
    character = get_sandbox_object(conn, character_object_id)
    location = get_sandbox_object(conn, location_object_id)
    if character["creation_type"] != "character":
        raise CreationSandboxError("Source sandbox object must be a character")
    if location["creation_type"] != "location":
        raise CreationSandboxError("Target sandbox object must be a location")
    if character["sandbox_id"] != location["sandbox_id"]:
        raise CreationSandboxError("Sandbox relations cannot cross sandbox namespaces")
    if character["lifecycle_status"] != "active" or location["lifecycle_status"] != "active":
        raise CreationSandboxError("Archived sandbox objects cannot receive active relations")
    conn.execute(
        "DELETE FROM creation_sandbox_relations WHERE sandbox_id=? AND source_object_id=? AND relation_type='located_in'",
        (character["sandbox_id"], character_object_id),
    )
    conn.execute(
        """
        INSERT INTO creation_sandbox_relations(
            sandbox_id,source_object_id,relation_type,target_object_id,metadata_json
        ) VALUES(?,?, 'located_in', ?, '{}')
        """,
        (character["sandbox_id"], character_object_id, location_object_id),
    )
    conn.execute(
        """
        INSERT INTO creation_sandbox_actor_runtime(
            object_id,sandbox_id,activation_status,current_location_object_id,autonomy_enabled
        ) VALUES(?,?,'configured',?,0)
        ON CONFLICT(object_id) DO UPDATE SET
            activation_status=CASE
                WHEN creation_sandbox_actor_runtime.activation_status='running' THEN 'running'
                ELSE 'configured'
            END,
            current_location_object_id=excluded.current_location_object_id,
            autonomy_enabled=0,
            updated_at=CURRENT_TIMESTAMP
        """,
        (character_object_id, character["sandbox_id"], location_object_id),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
        (
            character["sandbox_id"],
            character_object_id,
            "sandbox_relation_bound",
            _json({"relation_type": "located_in", "target_object_id": location_object_id}),
        ),
    )
    conn.commit()
    return get_sandbox_object(conn, character_object_id)


def archive_sandbox_object(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    obj = get_sandbox_object(conn, object_id)
    conn.execute(
        "UPDATE creation_sandbox_objects SET lifecycle_status='archived',updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
        (object_id,),
    )
    conn.execute(
        "DELETE FROM creation_sandbox_relations WHERE source_object_id=? OR target_object_id=?",
        (object_id, object_id),
    )
    if obj["creation_type"] == "character":
        conn.execute(
            """
            UPDATE creation_sandbox_actor_runtime
            SET activation_status='stopped',current_location_object_id=NULL,autonomy_enabled=0,updated_at=CURRENT_TIMESTAMP
            WHERE object_id=?
            """,
            (object_id,),
        )
    else:
        conn.execute(
            """
            UPDATE creation_sandbox_actor_runtime
            SET activation_status='configured',current_location_object_id=NULL,autonomy_enabled=0,updated_at=CURRENT_TIMESTAMP
            WHERE sandbox_id=? AND current_location_object_id=?
            """,
            (obj["sandbox_id"], object_id),
        )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_object_archived', '{}')",
        (obj["sandbox_id"], object_id),
    )
    conn.commit()
    return get_sandbox_object(conn, object_id)


def delete_sandbox_object(conn: sqlite3.Connection, object_id: str) -> None:
    obj = get_sandbox_object(conn, object_id)
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_object_deleted', ?)",
        (obj["sandbox_id"], object_id, _json({"creation_type": obj["creation_type"], "name": obj["identity"].get("name")})),
    )
    conn.execute("DELETE FROM creation_sandbox_objects WHERE object_id=?", (object_id,))
    conn.commit()


def reset_sandbox(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    sandbox = ensure_sandbox(conn, sandbox_id)
    next_revision = int(sandbox["revision"]) + 1
    conn.execute("DELETE FROM creation_sandbox_runtime WHERE sandbox_id=?", (sandbox_id,))
    conn.execute("DELETE FROM creation_sandbox_relations WHERE sandbox_id=?", (sandbox_id,))
    conn.execute("DELETE FROM creation_sandbox_events WHERE sandbox_id=?", (sandbox_id,))
    conn.execute("DELETE FROM creation_sandbox_objects WHERE sandbox_id=?", (sandbox_id,))
    conn.execute(
        "UPDATE creation_sandboxes SET status='active',revision=?,updated_at=CURRENT_TIMESTAMP WHERE sandbox_id=?",
        (next_revision, sandbox_id),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,NULL,'sandbox_reset',?)",
        (sandbox_id, _json({"previous_revision": int(sandbox["revision"]), "revision": next_revision})),
    )
    conn.commit()
    return ensure_sandbox(conn, sandbox_id)


def canonical_state_fingerprint(conn: sqlite3.Connection) -> str:
    """Hash canonical/runtime data while intentionally excluding Creation Sandbox tables."""
    table_rows = conn.execute(
        """
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
          AND name NOT LIKE 'creation_sandbox%'
          AND name != 'schema_meta'
        ORDER BY name
        """
    ).fetchall()
    snapshot: dict[str, Any] = {}
    for table_row in table_rows:
        table = str(table_row["name"])
        columns = [str(row["name"]) for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
        if not columns:
            continue
        rows = [dict(row) for row in conn.execute(f"SELECT * FROM {table}").fetchall()]
        snapshot[table] = sorted((_json(row) for row in rows))
    return hashlib.sha256(_json(snapshot).encode("utf-8")).hexdigest()


__all__ = [
    "CreationSandboxError",
    "DEFAULT_SANDBOX_ID",
    "activate_creation_proposal",
    "archive_sandbox_object",
    "bind_sandbox_character_to_location",
    "canonical_state_fingerprint",
    "delete_sandbox_object",
    "ensure_sandbox",
    "get_sandbox_object",
    "list_sandbox_objects",
    "reset_sandbox",
]

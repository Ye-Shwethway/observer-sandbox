from __future__ import annotations

import sqlite3
from collections.abc import Iterable
from typing import Any

from .creation_sandbox import (
    DEFAULT_SANDBOX_ID,
    CreationSandboxError,
    canonical_state_fingerprint,
)

_ALLOWED_DELETE_TYPES = frozenset({"character", "item"})


def _unique_ids(object_ids: Iterable[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for raw in object_ids:
        object_id = str(raw or "").strip()
        if not object_id or object_id in seen:
            continue
        seen.add(object_id)
        result.append(object_id)
    if not result:
        raise CreationSandboxError("Select at least one Sandbox Character or Item to delete")
    return result


def delete_sandbox_objects(
    conn: sqlite3.Connection,
    object_ids: Iterable[str],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    """Atomically delete selected active Sandbox Characters/Items only.

    The operation is deliberately narrower than reset_sandbox: Locations and all
    canonical/Real World state are outside this deletion authority. Shared Item
    definitions are removed only when the deleted selection leaves them orphaned.
    """

    ids = _unique_ids(object_ids)
    placeholders = ",".join("?" for _ in ids)
    rows = conn.execute(
        f"""
        SELECT object_id,sandbox_id,creation_type,lifecycle_status,identity_json
        FROM creation_sandbox_objects
        WHERE object_id IN ({placeholders})
        """,
        ids,
    ).fetchall()
    by_id = {str(row["object_id"]): row for row in rows}
    missing = [object_id for object_id in ids if object_id not in by_id]
    if missing:
        raise CreationSandboxError(f"Unknown Sandbox object(s): {', '.join(missing)}")

    records: list[dict[str, str]] = []
    for object_id in ids:
        row = by_id[object_id]
        row_sandbox = str(row["sandbox_id"])
        creation_type = str(row["creation_type"])
        lifecycle = str(row["lifecycle_status"])
        if row_sandbox != sandbox_id:
            raise CreationSandboxError("Batch delete cannot cross Sandbox namespaces")
        if creation_type not in _ALLOWED_DELETE_TYPES:
            raise CreationSandboxError(
                f"Batch delete currently supports Characters and Items only; {object_id} is {creation_type}"
            )
        if lifecycle != "active":
            raise CreationSandboxError(f"Batch delete target must be active: {object_id}")
        name_row = conn.execute(
            "SELECT json_extract(identity_json, '$.name') AS name FROM creation_sandbox_objects WHERE object_id=?",
            (object_id,),
        ).fetchone()
        name = str(name_row["name"] or object_id) if name_row is not None else object_id
        records.append({"object_id": object_id, "creation_type": creation_type, "name": name})

    definition_rows = conn.execute(
        f"""
        SELECT DISTINCT definition_key
        FROM creation_sandbox_item_instances
        WHERE sandbox_id=? AND object_id IN ({placeholders})
        """,
        [sandbox_id, *ids],
    ).fetchall()
    touched_definition_keys = [str(row["definition_key"]) for row in definition_rows]

    fingerprint_before = canonical_state_fingerprint(conn)
    savepoint = "sandbox_batch_delete"
    conn.execute(f"SAVEPOINT {savepoint}")
    try:
        for record in records:
            conn.execute(
                """
                INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json)
                VALUES(?,?, 'sandbox_object_deleted', json_object('creation_type', ?, 'name', ?, 'batch', 1))
                """,
                (sandbox_id, record["object_id"], record["creation_type"], record["name"]),
            )
        conn.execute(
            f"DELETE FROM creation_sandbox_objects WHERE sandbox_id=? AND object_id IN ({placeholders})",
            [sandbox_id, *ids],
        )
        for definition_key in touched_definition_keys:
            conn.execute(
                """
                DELETE FROM creation_sandbox_item_definitions
                WHERE sandbox_id=? AND definition_key=?
                  AND NOT EXISTS (
                    SELECT 1 FROM creation_sandbox_item_instances
                    WHERE sandbox_id=? AND definition_key=?
                  )
                """,
                (sandbox_id, definition_key, sandbox_id, definition_key),
            )

        fingerprint_after = canonical_state_fingerprint(conn)
        if fingerprint_after != fingerprint_before:
            raise CreationSandboxError("Canonical state changed during Sandbox batch delete; operation rolled back")
        conn.execute(f"RELEASE SAVEPOINT {savepoint}")
    except Exception:
        conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
        conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        raise

    return {
        "deleted_count": len(records),
        "deleted": records,
        "sandbox_id": sandbox_id,
        "canonical_unchanged": True,
    }


__all__ = ["delete_sandbox_objects"]

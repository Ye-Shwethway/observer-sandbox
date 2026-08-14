from __future__ import annotations

import json
import sqlite3
from typing import Any

from .composition_schema import ensure_actor_runtime


LEGACY_KEYS = {
    "autonomy_enabled": "autonomy_enabled",
    "autonomy_mode": "autonomy_mode",
    "autonomy_pending_action": "pending",
    "autonomy_lease": "lease",
    "autonomy_retry": "retry",
    "cognition_wake_stats": "cognition_stats",
    "cognition_wake_reason": "wake_reason",
}


def _legacy_value(conn: sqlite3.Connection, key: str) -> Any:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (key,)).fetchone()
    return None if row is None else json.loads(row[0])


def migrate_legacy_actor_runtime(conn: sqlite3.Connection, actor_id: str) -> None:
    """Move the old singleton scheduler state onto one explicitly selected actor.

    This exists only for pre-v4 compatibility. Runtime engines themselves are actor-id
    driven and must not infer a named character here.
    """
    ensure_actor_runtime(conn, actor_id)
    marker = conn.execute("SELECT value FROM schema_meta WHERE key=?", (f"actor_runtime_migrated:{actor_id}",)).fetchone()
    if marker is not None:
        return

    enabled = _legacy_value(conn, "autonomy_enabled")
    mode = _legacy_value(conn, "autonomy_mode")
    pending = _legacy_value(conn, "autonomy_pending_action")
    lease = _legacy_value(conn, "autonomy_lease")
    retry = _legacy_value(conn, "autonomy_retry")
    cognition = _legacy_value(conn, "cognition_wake_stats")
    wake_reason = _legacy_value(conn, "cognition_wake_reason")

    pending_action_id = None
    if isinstance(pending, dict) and pending.get("action_id"):
        action_id = str(pending["action_id"])
        existing = conn.execute("SELECT 1 FROM action_instances WHERE id=?", (action_id,)).fetchone()
        if existing is not None:
            pending_action_id = action_id
        else:
            pending_action_id = None
            wake_reason = "runtime_schema_migrated"

    conn.execute(
        """UPDATE actor_runtime SET
            autonomy_enabled=?, autonomy_mode=?, pending_action_id=?,
            lease_owner=?, lease_expires_at=?, retry_failures=?, retry_after=?, retry_last_error=?,
            cognition_stats_json=?, wake_reason=?, updated_at=CURRENT_TIMESTAMP
        WHERE actor_id=?""",
        (
            1 if bool(enabled) else 0,
            str(mode or "normal"),
            pending_action_id,
            (lease or {}).get("owner") if isinstance(lease, dict) else None,
            (lease or {}).get("expires_at") if isinstance(lease, dict) else None,
            int((retry or {}).get("failures", 0)) if isinstance(retry, dict) else 0,
            (retry or {}).get("retry_after") if isinstance(retry, dict) else None,
            (retry or {}).get("last_error") if isinstance(retry, dict) else None,
            json.dumps(cognition or {}, ensure_ascii=False),
            wake_reason,
            actor_id,
        ),
    )
    for key in LEGACY_KEYS:
        conn.execute("DELETE FROM runtime_state WHERE key=?", (key,))
    conn.execute(
        "INSERT OR REPLACE INTO schema_meta(key,value) VALUES(?, '1')",
        (f"actor_runtime_migrated:{actor_id}",),
    )
    conn.commit()


def actor_runtime(conn: sqlite3.Connection, actor_id: str) -> dict[str, Any]:
    ensure_actor_runtime(conn, actor_id)
    row = conn.execute("SELECT * FROM actor_runtime WHERE actor_id=?", (actor_id,)).fetchone()
    assert row is not None
    return {
        "actor_id": actor_id,
        "autonomy_enabled": bool(row["autonomy_enabled"]),
        "autonomy_mode": row["autonomy_mode"],
        "pending_action_id": row["pending_action_id"],
        "lease": None if row["lease_owner"] is None else {"owner": row["lease_owner"], "expires_at": row["lease_expires_at"]},
        "retry": None if not row["retry_failures"] and row["retry_after"] is None else {
            "failures": row["retry_failures"], "retry_after": row["retry_after"], "last_error": row["retry_last_error"]
        },
        "cognition_stats": json.loads(row["cognition_stats_json"] or "{}"),
        "wake_reason": row["wake_reason"],
    }


def set_actor_runtime(conn: sqlite3.Connection, actor_id: str, **changes: Any) -> None:
    ensure_actor_runtime(conn, actor_id)
    mapping = {
        "autonomy_enabled": ("autonomy_enabled", lambda v: 1 if bool(v) else 0),
        "autonomy_mode": ("autonomy_mode", str),
        "pending_action_id": ("pending_action_id", lambda v: v),
        "wake_reason": ("wake_reason", lambda v: v),
        "cognition_stats": ("cognition_stats_json", lambda v: json.dumps(v or {}, ensure_ascii=False)),
    }
    assignments: list[str] = []
    values: list[Any] = []
    for key, value in changes.items():
        if key not in mapping:
            raise KeyError(key)
        column, transform = mapping[key]
        assignments.append(f"{column}=?")
        values.append(transform(value))
    if assignments:
        values.append(actor_id)
        conn.execute(f"UPDATE actor_runtime SET {', '.join(assignments)}, updated_at=CURRENT_TIMESTAMP WHERE actor_id=?", values)


def set_lease(conn: sqlite3.Connection, actor_id: str, lease: dict[str, Any] | None) -> None:
    ensure_actor_runtime(conn, actor_id)
    conn.execute(
        "UPDATE actor_runtime SET lease_owner=?, lease_expires_at=?, updated_at=CURRENT_TIMESTAMP WHERE actor_id=?",
        (None if lease is None else lease.get("owner"), None if lease is None else lease.get("expires_at"), actor_id),
    )


def set_retry(conn: sqlite3.Connection, actor_id: str, retry: dict[str, Any] | None) -> None:
    ensure_actor_runtime(conn, actor_id)
    conn.execute(
        """UPDATE actor_runtime SET retry_failures=?, retry_after=?, retry_last_error=?, updated_at=CURRENT_TIMESTAMP
        WHERE actor_id=?""",
        (
            0 if retry is None else int(retry.get("failures", 0)),
            None if retry is None else retry.get("retry_after"),
            None if retry is None else retry.get("last_error"),
            actor_id,
        ),
    )


def pending_action(conn: sqlite3.Connection, actor_id: str) -> dict[str, Any] | None:
    state = actor_runtime(conn, actor_id)
    action_id = state["pending_action_id"]
    if not action_id:
        return None
    row = conn.execute("SELECT * FROM action_instances WHERE id=?", (action_id,)).fetchone()
    if row is None:
        return None
    return {
        "action_id": row["id"],
        "action": row["action_type"],
        "duration_minutes": row["duration_minutes"],
        "target": row["target_id"],
        "reason": row["intent"],
        "planned_sim_time": row["planned_sim_time"],
        "planned_wall_time": row["planned_wall_time"],
        "due_wall_time": row["due_wall_time"],
        "speed_at_plan": row["speed_at_plan"],
        "autonomy_mode": state["autonomy_mode"],
        "place_id": row["place_id"],
        "conditions": json.loads(row["conditions_json"] or "{}"),
        "modifiers": json.loads(row["modifiers_json"] or "{}"),
        "resources": json.loads(row["resources_json"] or "[]"),
        "participants": json.loads(row["participants_json"] or "[]"),
    }

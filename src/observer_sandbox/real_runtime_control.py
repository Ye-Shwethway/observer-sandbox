from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from .actor_runtime import set_actor_runtime, set_lease, set_retry
from .autonomy import set_autonomy_paused, set_autonomy_speed
from .event_log import record_event
from .simulation import runtime_value, set_runtime_value
from .world import set_field


class RealRuntimeControlError(ValueError):
    pass


def _normalize_sim_time(value: str | datetime) -> str:
    if isinstance(value, datetime):
        parsed = value
    else:
        try:
            parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError as exc:
            raise RealRuntimeControlError("Real World sim_time must be ISO-8601") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.isoformat()


def real_runtime_status(conn: sqlite3.Connection) -> dict[str, Any]:
    return {
        "sim_time": runtime_value(conn, "sim_time", None),
        "speed": float(runtime_value(conn, "speed", 1.0)),
        "paused": bool(runtime_value(conn, "paused", False)),
    }


def set_real_runtime_paused(conn: sqlite3.Connection, paused: bool) -> dict[str, Any]:
    set_autonomy_paused(conn, bool(paused))
    return real_runtime_status(conn)


def set_real_runtime_speed(conn: sqlite3.Connection, speed: float) -> dict[str, Any]:
    try:
        set_autonomy_speed(conn, float(speed))
    except ValueError as exc:
        raise RealRuntimeControlError(str(exc)) from exc
    return real_runtime_status(conn)


def set_real_runtime_time(
    conn: sqlite3.Connection,
    sim_time: str | datetime,
    *,
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Set the canonical universe clock under explicit Creator control.

    Manual clock edits automatically pause the Real World first. Any autonomous
    action planned against the previous clock is cancelled so a later resume
    forces fresh cognition instead of completing stale work on a rewritten
    timeline. The runtime intentionally remains paused after the edit.
    """
    normalized = _normalize_sim_time(sim_time)
    before = real_runtime_status(conn)

    # The established pause path also preserves pending-action wall timing if a
    # Creator merely pauses/resumes without changing the clock.
    set_autonomy_paused(conn, True)

    rows = conn.execute(
        """
        SELECT actor_id,pending_action_id
        FROM actor_runtime
        ORDER BY actor_id
        """
    ).fetchall()
    cancelled: list[str] = []
    for row in rows:
        actor_id = str(row["actor_id"])
        action_id = row["pending_action_id"]
        if action_id:
            conn.execute(
                """
                UPDATE action_instances
                SET status='cancelled',updated_at=CURRENT_TIMESTAMP
                WHERE id=? AND status IN ('planned','in_progress')
                """,
                (action_id,),
            )
            cancelled.append(str(action_id))
        set_actor_runtime(
            conn,
            actor_id,
            pending_action_id=None,
            wake_reason="creator_world_time_changed",
        )
        set_lease(conn, actor_id, None)
        set_retry(conn, actor_id, None)
        set_field(
            conn,
            actor_id,
            "runtime.current_action",
            "idle",
            mode="simulated",
            authority="living_runtime",
            source="creator-world-time-control",
        )

    set_runtime_value(conn, "sim_time", normalized)
    record_event(
        conn,
        sim_time=normalized,
        event_type="creator_world_time_changed",
        payload={
            "authority": "creator",
            "requested_by": requested_by,
            "before_sim_time": before["sim_time"],
            "after_sim_time": normalized,
            "auto_paused": True,
            "cancelled_action_ids": cancelled,
        },
    )
    conn.commit()
    return {
        **real_runtime_status(conn),
        "before_sim_time": before["sim_time"],
        "cancelled_action_ids": cancelled,
        "auto_paused": True,
    }


__all__ = [
    "RealRuntimeControlError",
    "real_runtime_status",
    "set_real_runtime_paused",
    "set_real_runtime_speed",
    "set_real_runtime_time",
]

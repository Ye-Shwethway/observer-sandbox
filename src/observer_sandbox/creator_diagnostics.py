from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any

from .actor_runtime import actor_runtime, set_actor_runtime, set_lease, set_retry
from .event_log import record_event
from .location_runtime import set_dynamic_location
from .simulation import runtime_value, set_runtime_value, snapshot
from .world import set_field


def _parse_sim_time(value: str) -> datetime:
    parsed = datetime.fromisoformat(str(value))
    if parsed.tzinfo is None:
        raise ValueError("Simulation time must include a timezone offset")
    return parsed


def relocate_character_for_diagnostic(
    conn: sqlite3.Connection,
    actor_id: str,
    location_id: str,
    *,
    sim_time: str | None = None,
    authority: str = "creator",
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Relocate one character for an explicit Creator diagnostic.

    This is administrative world-state control, not a character action. Location
    may be changed while preserving the universe clock, or the caller may also
    move the clock forward to an explicit timezone-aware simulation timestamp.
    A time jump never fabricates elapsed actions, sleep, meals, or other history.
    Any pending action is cancelled because its original place/time assumptions
    are no longer authoritative after relocation.
    """
    actor = conn.execute(
        "SELECT id,name FROM entities WHERE id=? AND entity_type='character'",
        (actor_id,),
    ).fetchone()
    if actor is None:
        raise KeyError(f"Unknown character: {actor_id}")
    location = conn.execute(
        "SELECT id,name FROM entities WHERE id=? AND entity_type='location'",
        (location_id,),
    ).fetchone()
    if location is None:
        raise KeyError(f"Unknown location: {location_id}")

    raw_current_time = runtime_value(conn, "sim_time", None)
    if not isinstance(raw_current_time, str) or not raw_current_time:
        raise RuntimeError("Creator diagnostic relocation requires initialized simulation time")
    current_time = _parse_sim_time(raw_current_time)
    target_time = current_time if sim_time is None else _parse_sim_time(sim_time)
    if target_time < current_time:
        raise ValueError("Creator diagnostic relocation cannot move simulation time backward")

    conn.execute("BEGIN IMMEDIATE")
    try:
        before = snapshot(conn, actor_id)
        runtime = actor_runtime(conn, actor_id)
        cancelled_action_id = runtime.get("pending_action_id")
        if cancelled_action_id:
            conn.execute(
                "UPDATE action_instances SET status='cancelled',updated_at=CURRENT_TIMESTAMP "
                "WHERE id=? AND status IN ('planned','in_progress')",
                (cancelled_action_id,),
            )

        if target_time != current_time:
            set_runtime_value(conn, "sim_time", target_time.isoformat())
        set_dynamic_location(conn, actor_id, location_id)
        set_field(
            conn,
            actor_id,
            "runtime.current_action",
            "idle",
            mode="simulated",
            authority="living_runtime",
            source="creator-diagnostic-relocation",
        )
        set_actor_runtime(
            conn,
            actor_id,
            pending_action_id=None,
            wake_reason="creator_diagnostic_relocation",
        )
        set_lease(conn, actor_id, None)
        set_retry(conn, actor_id, None)

        after = snapshot(conn, actor_id)
        elapsed_minutes = (target_time - current_time).total_seconds() / 60.0
        state_changes: dict[str, Any] = {
            "location": {"before": before["location"], "after": after["location"]},
            "current_action": {"before": before["current_action"], "after": after["current_action"]},
        }
        if before["sim_time"] != after["sim_time"]:
            state_changes["sim_time"] = {"before": before["sim_time"], "after": after["sim_time"]}

        record_event(
            conn,
            sim_time=after["sim_time"],
            actor_id=actor_id,
            event_type="creator_diagnostic_relocation",
            location_id=location_id,
            state_changes=state_changes,
            payload={
                "authority": authority,
                "requested_by": requested_by,
                "diagnostic_only": True,
                "cancelled_action_id": cancelled_action_id,
                "target_location_id": location_id,
                "target_location_name": location["name"],
                "time_mode": "preserve" if sim_time is None else "raw_forward_jump",
                "elapsed_minutes_without_simulation": elapsed_minutes,
                "warning": "A raw time jump changes the universe clock but does not synthesize elapsed actions or biological history.",
                "before": before,
                "after": after,
            },
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return {
        "ok": True,
        "actor_id": actor_id,
        "character_name": str(actor["name"]),
        "location_id": location_id,
        "location_name": str(location["name"]),
        "authority": authority,
        "requested_by": requested_by,
        "cancelled_action_id": cancelled_action_id,
        "time_mode": "preserve" if sim_time is None else "raw_forward_jump",
        "elapsed_minutes_without_simulation": elapsed_minutes,
        "before": before,
        "after": after,
        "state_changes": state_changes,
    }

from __future__ import annotations

import sqlite3
from typing import Any

from .actor_runtime import actor_runtime, set_actor_runtime, set_retry
from .event_log import record_event
from .simulation import snapshot
from .world import set_field


BASIC_STAT_BASELINE: dict[str, float] = {
    "needs.energy": 75.0,
    "needs.hunger": 20.0,
    "needs.thirst": 15.0,
    "needs.sleepiness": 15.0,
    "physiology.cleanliness": 80.0,
    "physiology.fatigue": 0.0,
}


def restore_basic_stats(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    authority: str = "creator",
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Restore one actor's basic living state under explicit Creator authority.

    This is an administrative world-state control, not an AI action. Any pending
    autonomous action is cancelled because its original need/reason may no longer
    be valid after the restore. The universe clock, location, profile canon and
    autonomy enabled/mode are preserved.
    """
    row = conn.execute(
        "SELECT id,name FROM entities WHERE id=? AND entity_type='character'",
        (actor_id,),
    ).fetchone()
    if row is None:
        raise KeyError(f"Unknown character: {actor_id}")

    conn.execute("BEGIN IMMEDIATE")
    before = snapshot(conn, actor_id)
    runtime = actor_runtime(conn, actor_id)
    cancelled_action_id = runtime.get("pending_action_id")
    if cancelled_action_id:
        conn.execute(
            "UPDATE action_instances SET status=?,updated_at=CURRENT_TIMESTAMP WHERE id=? AND status IN (?,?)",
            ("cancelled", cancelled_action_id, "planned", "in_progress"),
        )

    for field_key, value in BASIC_STAT_BASELINE.items():
        set_field(
            conn,
            actor_id,
            field_key,
            value,
            mode="simulated",
            authority="creator_control",
            source="creator-basic-stats-restore",
        )
    set_field(
        conn,
        actor_id,
        "runtime.current_action",
        "idle",
        mode="simulated",
        authority="living_runtime",
        source="creator-basic-stats-restore",
    )
    set_actor_runtime(
        conn,
        actor_id,
        pending_action_id=None,
        wake_reason="creator_basic_stats_restored",
    )
    set_retry(conn, actor_id, None)

    after = snapshot(conn, actor_id)
    changes: dict[str, Any] = {}
    for key in ("energy", "hunger", "thirst", "sleepiness", "cleanliness", "fatigue", "current_action"):
        if before.get(key) != after.get(key):
            changes[key] = {"before": before.get(key), "after": after.get(key)}

    record_event(
        conn,
        sim_time=after["sim_time"],
        actor_id=actor_id,
        event_type="creator_basic_stats_restored",
        location_id=after["location"],
        state_changes=changes,
        payload={
            "authority": authority,
            "requested_by": requested_by,
            "cancelled_action_id": cancelled_action_id,
            "baseline": BASIC_STAT_BASELINE,
            "before": before,
            "after": after,
        },
    )
    conn.commit()
    return {
        "ok": True,
        "actor_id": actor_id,
        "character_name": row["name"],
        "authority": authority,
        "cancelled_action_id": cancelled_action_id,
        "before": before,
        "after": after,
        "state_changes": changes,
    }

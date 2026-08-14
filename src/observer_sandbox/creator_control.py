from __future__ import annotations

import sqlite3
from typing import Any

from .actor_runtime import actor_runtime, set_actor_runtime, set_lease, set_retry
from .event_log import record_event
from .inventory import stack_state
from .simulation import runtime_value, snapshot
from .world import set_field


BASIC_STAT_BASELINE: dict[str, float] = {
    "needs.energy": 75.0,
    "needs.hunger": 20.0,
    "needs.thirst": 15.0,
    "needs.sleepiness": 15.0,
    "physiology.cleanliness": 80.0,
    "physiology.fatigue": 0.0,
}

_FIELD_AUTHORITIES = {
    "needs.energy": "needs_engine",
    "needs.hunger": "needs_engine",
    "needs.thirst": "needs_engine",
    "needs.sleepiness": "needs_engine",
    "physiology.cleanliness": "physiology_engine",
    "physiology.fatigue": "physiology_engine",
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
    autonomy enabled/mode are preserved. Creator authority authorizes the control;
    domain field ownership remains with the normal simulation engines.
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
            authority=_FIELD_AUTHORITIES[field_key],
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
    set_lease(conn, actor_id, None)
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


def replenish_inventory_stack(
    conn: sqlite3.Connection,
    stack_id: str,
    quantity: float,
    *,
    authority: str = "creator",
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Add stock to one existing stack under explicit Creator authority.

    The operation is intentionally narrow: it cannot create arbitrary definitions,
    move ownership, edit containers, or set negative quantities. Normal inventory
    semantics remain authoritative after the intervention.
    """
    amount = float(quantity)
    if amount <= 0.0:
        raise ValueError("Replenishment quantity must be positive")
    if amount > 1_000_000_000.0:
        raise ValueError("Replenishment quantity exceeds the bounded control limit")

    before_stack = stack_state(conn, stack_id)
    conn.execute("BEGIN IMMEDIATE")
    current = conn.execute(
        "SELECT quantity FROM inventory_stacks WHERE entity_id=?",
        (stack_id,),
    ).fetchone()
    if current is None:
        conn.rollback()
        raise KeyError(f"Unknown inventory stack: {stack_id}")
    before = float(current[0])
    after = before + amount
    conn.execute(
        "UPDATE inventory_stacks SET quantity=?,updated_at=CURRENT_TIMESTAMP WHERE entity_id=?",
        (after, stack_id),
    )

    sim_time = runtime_value(conn, "sim_time")
    if not isinstance(sim_time, str) or not sim_time:
        conn.rollback()
        raise RuntimeError("Creator inventory control requires initialized simulation time")

    record_event(
        conn,
        sim_time=sim_time,
        event_type="creator_inventory_replenished",
        location_id=before_stack.owner_id if before_stack.owner_id else None,
        state_changes={
            "inventory.quantity": {
                "stack_id": stack_id,
                "before": before,
                "after": after,
                "unit": before_stack.unit,
            }
        },
        payload={
            "authority": authority,
            "requested_by": requested_by,
            "stack_id": stack_id,
            "definition_id": before_stack.definition_id,
            "item_name": before_stack.name,
            "added_quantity": amount,
            "unit": before_stack.unit,
            "before_quantity": before,
            "after_quantity": after,
            "container_id": before_stack.container_id,
            "owner_id": before_stack.owner_id,
        },
    )
    conn.commit()
    return {
        "ok": True,
        "stack_id": stack_id,
        "definition_id": before_stack.definition_id,
        "item_name": before_stack.name,
        "added_quantity": amount,
        "unit": before_stack.unit,
        "before_quantity": before,
        "after_quantity": after,
        "container_id": before_stack.container_id,
        "owner_id": before_stack.owner_id,
        "authority": authority,
        "requested_by": requested_by,
    }

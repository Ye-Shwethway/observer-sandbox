from __future__ import annotations

import sqlite3

from .location_runtime import current_location, set_dynamic_location


def recover_missing_actor_location(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    fallback_location_id: str | None = None,
) -> str | None:
    """Repair an invalid missing actor location from represented runtime evidence.

    A character with no location is not a valid runtime transit state: movement
    updates location atomically and simulation snapshots require one. Recovery
    therefore prefers the actor's most recent represented action place. Only when
    no such evidence exists may the caller supply an explicit seed/start fallback.
    Existing valid locations are never rewritten.
    """
    existing = current_location(conn, actor_id)
    if existing is not None:
        return existing

    row = conn.execute(
        """
        SELECT ai.place_id
        FROM action_instances ai
        JOIN entities e ON e.id=ai.place_id AND e.entity_type='location'
        WHERE ai.actor_id=? AND ai.place_id IS NOT NULL
        ORDER BY
            COALESCE(ai.ended_sim_time, ai.started_sim_time, ai.planned_sim_time) DESC,
            ai.updated_at DESC,
            ai.created_at DESC
        LIMIT 1
        """,
        (actor_id,),
    ).fetchone()
    recovered = str(row["place_id"]) if row is not None else None

    if recovered is None and fallback_location_id:
        valid = conn.execute(
            "SELECT 1 FROM entities WHERE id=? AND entity_type='location'",
            (fallback_location_id,),
        ).fetchone()
        if valid is not None:
            recovered = str(fallback_location_id)

    if recovered is None:
        return None

    set_dynamic_location(conn, actor_id, recovered)
    return recovered

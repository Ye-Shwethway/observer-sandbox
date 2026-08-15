from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any


SOURCE = "habit_adaptation_v1"
EXCLUDED_ACTIONS = {"move", "idle", "sleep", "self_satisfaction"}
FORMATION_RATE = 0.04
ESTABLISHED_STRENGTH = 50.0
ESTABLISHED_EFFECTIVE_REPETITIONS = 18.0
DECAY_GRACE_DAYS = 7.0
DECAY_POINTS_PER_DAY = 1.5
DORMANT_STRENGTH = 30.0
LAPSED_STRENGTH = 10.0
LAPSED_INACTIVITY_DAYS = 30.0


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _metadata(row: sqlite3.Row) -> dict[str, Any]:
    raw = json.loads(row["metadata_json"] or "{}")
    return raw if isinstance(raw, dict) else {}


def _habit_key(action_name: str, location_id: str, target_id: str | None) -> str:
    return "|".join((action_name, location_id, target_id or ""))


def _entity_name(conn: sqlite3.Connection, entity_id: str | None) -> str | None:
    if not entity_id:
        return None
    row = conn.execute("SELECT name FROM entities WHERE id=?", (entity_id,)).fetchone()
    return str(row[0]) if row is not None and row[0] else entity_id


def _habit_name(
    conn: sqlite3.Connection,
    *,
    action_name: str,
    location_id: str,
    target_id: str | None,
) -> str:
    action_label = action_name.replace("_", " ").strip().title()
    target_name = _entity_name(conn, target_id)
    location_name = _entity_name(conn, location_id) or location_id
    return f"{action_label} — {target_name or location_name}"


def _dynamic_rows(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    rows = conn.execute(
        "SELECT id,name,strength,metadata_json FROM character_habits WHERE entity_id=? ORDER BY id",
        (actor_id,),
    ).fetchall()
    return [row for row in rows if _metadata(row).get("source") == SOURCE]


def _temporal_reinforcement(last_sim_time: str | None, ended_sim_time: str) -> float:
    if not last_sim_time:
        return 1.0
    elapsed_hours = max(
        0.0,
        (_parse_time(ended_sim_time) - _parse_time(last_sim_time)).total_seconds() / 3600.0,
    )
    if elapsed_hours < 6.0:
        return 0.25
    if elapsed_hours < 18.0:
        return 0.60
    return 1.0


def _status_after_reinforcement(strength: float, effective_repetitions: float) -> str:
    if strength >= ESTABLISHED_STRENGTH and effective_repetitions >= ESTABLISHED_EFFECTIVE_REPETITIONS:
        return "established"
    return "emerging"


def _decay_dynamic_habits(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    now_sim_time: str,
) -> list[dict[str, Any]]:
    now = _parse_time(now_sim_time)
    changes: list[dict[str, Any]] = []
    for row in _dynamic_rows(conn, actor_id):
        metadata = _metadata(row)
        last_reinforced = metadata.get("last_reinforced_sim_time")
        if not isinstance(last_reinforced, str) or not last_reinforced:
            continue
        last_reinforced_dt = _parse_time(last_reinforced)
        inactivity_days = max(0.0, (now - last_reinforced_dt).total_seconds() / 86400.0)
        if inactivity_days <= DECAY_GRACE_DAYS:
            continue

        last_decay = metadata.get("last_decay_sim_time")
        decay_anchor = _parse_time(last_decay) if isinstance(last_decay, str) and last_decay else last_reinforced_dt
        grace_end = last_reinforced_dt.timestamp() + DECAY_GRACE_DAYS * 86400.0
        effective_anchor_timestamp = max(decay_anchor.timestamp(), grace_end)
        decay_days = max(0.0, (now.timestamp() - effective_anchor_timestamp) / 86400.0)
        if decay_days <= 0.0:
            continue

        before_strength = float(row["strength"] or 0.0)
        after_strength = max(0.0, round(before_strength - decay_days * DECAY_POINTS_PER_DAY, 3))
        previous_status = str(metadata.get("status") or "emerging")
        status = previous_status
        if inactivity_days >= LAPSED_INACTIVITY_DAYS and after_strength <= LAPSED_STRENGTH:
            status = "lapsed"
        elif previous_status == "established" and after_strength < DORMANT_STRENGTH:
            status = "dormant"
        elif previous_status in {"dormant", "lapsed"}:
            status = previous_status

        metadata["status"] = status
        metadata["last_decay_sim_time"] = now_sim_time
        conn.execute(
            "UPDATE character_habits SET strength=?,metadata_json=? WHERE id=?",
            (after_strength, json.dumps(metadata, ensure_ascii=False, sort_keys=True), row["id"]),
        )
        if after_strength != before_strength or status != previous_status:
            changes.append(
                {
                    "habit_id": int(row["id"]),
                    "name": row["name"],
                    "strength_before": before_strength,
                    "strength_after": after_strength,
                    "status_before": previous_status,
                    "status_after": status,
                    "inactivity_days": round(inactivity_days, 3),
                }
            )
    return changes


def settle_habit_adaptation(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    action_name: str,
    location_id: str,
    target_id: str | None,
    ended_sim_time: str,
) -> dict[str, Any] | None:
    """Update learned habit state from one completed represented action.

    The deterministic runtime is the mutation authority. The model only receives
    compact read-only disposition context later.
    """
    decay_changes = _decay_dynamic_habits(conn, actor_id, now_sim_time=ended_sim_time)
    if action_name in EXCLUDED_ACTIONS:
        return {"source": SOURCE, "decay": decay_changes} if decay_changes else None

    key = _habit_key(action_name, location_id, target_id)
    candidate: sqlite3.Row | None = None
    candidate_metadata: dict[str, Any] = {}
    for row in _dynamic_rows(conn, actor_id):
        metadata = _metadata(row)
        if metadata.get("habit_key") == key:
            candidate = row
            candidate_metadata = metadata
            break

    if candidate is None:
        weight = 1.0
        strength_before = 0.0
        effective_repetitions = 1.0
        repetition_count = 1
        strength_after = round((100.0 - strength_before) * FORMATION_RATE * weight, 3)
        status = _status_after_reinforcement(strength_after, effective_repetitions)
        name = _habit_name(
            conn,
            action_name=action_name,
            location_id=location_id,
            target_id=target_id,
        )
        metadata = {
            "source": SOURCE,
            "habit_key": key,
            "behavior": {"action": action_name, "target_id": target_id},
            "cue": {"location_id": location_id},
            "status": status,
            "first_reinforced_sim_time": ended_sim_time,
            "last_reinforced_sim_time": ended_sim_time,
            "last_decay_sim_time": ended_sim_time,
            "repetition_count": repetition_count,
            "effective_repetitions": effective_repetitions,
        }
        cursor = conn.execute(
            """
            INSERT INTO character_habits(entity_id,name,description,strength,metadata_json)
            VALUES(?,?,?,?,?)
            """,
            (
                actor_id,
                name,
                "Learned from repeated represented behavior in a stable context.",
                strength_after,
                json.dumps(metadata, ensure_ascii=False, sort_keys=True),
            ),
        )
        habit_id = int(cursor.lastrowid)
        status_before = None
    else:
        last_reinforced = candidate_metadata.get("last_reinforced_sim_time")
        weight = _temporal_reinforcement(
            str(last_reinforced) if isinstance(last_reinforced, str) else None,
            ended_sim_time,
        )
        strength_before = float(candidate["strength"] or 0.0)
        repetition_count = int(candidate_metadata.get("repetition_count", 0)) + 1
        effective_repetitions = round(
            float(candidate_metadata.get("effective_repetitions", 0.0)) + weight,
            3,
        )
        strength_after = min(
            100.0,
            round(strength_before + (100.0 - strength_before) * FORMATION_RATE * weight, 3),
        )
        status_before = str(candidate_metadata.get("status") or "emerging")
        status = _status_after_reinforcement(strength_after, effective_repetitions)
        candidate_metadata.update(
            {
                "status": status,
                "last_reinforced_sim_time": ended_sim_time,
                "last_decay_sim_time": ended_sim_time,
                "repetition_count": repetition_count,
                "effective_repetitions": effective_repetitions,
            }
        )
        conn.execute(
            "UPDATE character_habits SET strength=?,metadata_json=? WHERE id=?",
            (
                strength_after,
                json.dumps(candidate_metadata, ensure_ascii=False, sort_keys=True),
                candidate["id"],
            ),
        )
        habit_id = int(candidate["id"])
        name = str(candidate["name"])

    return {
        "source": SOURCE,
        "reinforcement": {
            "habit_id": habit_id,
            "name": name,
            "habit_key": key,
            "strength_before": strength_before,
            "strength_after": strength_after,
            "status_before": status_before,
            "status_after": status,
            "repetition_count": repetition_count,
            "effective_repetitions": effective_repetitions,
            "temporal_weight": weight,
        },
        "decay": decay_changes,
    }


def habit_dynamics_context(conn: sqlite3.Connection, actor_id: str) -> list[dict[str, Any]]:
    """Compact read-only habit state suitable for cognition input."""
    result: list[dict[str, Any]] = []
    for row in _dynamic_rows(conn, actor_id):
        metadata = _metadata(row)
        behavior = metadata.get("behavior") if isinstance(metadata.get("behavior"), dict) else {}
        cue = metadata.get("cue") if isinstance(metadata.get("cue"), dict) else {}
        result.append(
            {
                "name": str(row["name"]),
                "strength": round(float(row["strength"] or 0.0), 3),
                "status": str(metadata.get("status") or "emerging"),
                "behavior": behavior.get("action"),
                "cue_location_id": cue.get("location_id"),
            }
        )
    return result

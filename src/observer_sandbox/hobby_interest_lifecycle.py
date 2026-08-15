from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any


SOURCE = "hobby_interest_lifecycle_v1"
ELIGIBLE_ACTIONS = {"read", "use"}
FORMATION_RATE = 0.06
RECURRING_STRENGTH = 15.0
RECURRING_EFFECTIVE_ENGAGEMENTS = 4.0
RECURRING_DISTINCT_DAYS = 2
ESTABLISHED_STRENGTH = 35.0
ESTABLISHED_EFFECTIVE_ENGAGEMENTS = 10.0
ESTABLISHED_DISTINCT_DAYS = 4
DECAY_GRACE_DAYS = 14.0
DECAY_POINTS_PER_DAY = 0.75
DORMANT_STRENGTH = 25.0
LAPSED_STRENGTH = 8.0
LAPSED_INACTIVITY_DAYS = 60.0


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _metadata(row: sqlite3.Row) -> dict[str, Any]:
    raw = json.loads(row["metadata_json"] or "{}")
    return raw if isinstance(raw, dict) else {}


def _dynamic_rows(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    rows = conn.execute(
        "SELECT id,name,enjoyment,metadata_json FROM character_hobbies WHERE entity_id=? ORDER BY id",
        (actor_id,),
    ).fetchall()
    return [row for row in rows if _metadata(row).get("source") == SOURCE]


def _entity_name(conn: sqlite3.Connection, entity_id: str) -> str:
    row = conn.execute("SELECT name FROM entities WHERE id=?", (entity_id,)).fetchone()
    return str(row[0]) if row is not None and row[0] else entity_id


def _interest_key(action_name: str, target_id: str) -> str:
    return f"{action_name}|{target_id}"


def _interest_name(conn: sqlite3.Connection, action_name: str, target_id: str) -> str:
    verb = "Reading" if action_name == "read" else "Using"
    return f"{verb} — {_entity_name(conn, target_id)}"


def _temporal_weight(last_sim_time: str | None, ended_sim_time: str) -> float:
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


def _status_after_engagement(strength: float, effective: float, distinct_days: int) -> str:
    if (
        strength >= ESTABLISHED_STRENGTH
        and effective >= ESTABLISHED_EFFECTIVE_ENGAGEMENTS
        and distinct_days >= ESTABLISHED_DISTINCT_DAYS
    ):
        return "established"
    if (
        strength >= RECURRING_STRENGTH
        and effective >= RECURRING_EFFECTIVE_ENGAGEMENTS
        and distinct_days >= RECURRING_DISTINCT_DAYS
    ):
        return "recurring"
    return "emerging"


def _decay_dynamic_interests(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    now_sim_time: str,
) -> list[dict[str, Any]]:
    now = _parse_time(now_sim_time)
    changes: list[dict[str, Any]] = []
    for row in _dynamic_rows(conn, actor_id):
        metadata = _metadata(row)
        last_engaged = metadata.get("last_engaged_sim_time")
        if not isinstance(last_engaged, str) or not last_engaged:
            continue
        last_engaged_dt = _parse_time(last_engaged)
        inactivity_days = max(0.0, (now - last_engaged_dt).total_seconds() / 86400.0)
        if inactivity_days <= DECAY_GRACE_DAYS:
            continue

        last_decay = metadata.get("last_decay_sim_time")
        decay_anchor = _parse_time(last_decay) if isinstance(last_decay, str) and last_decay else last_engaged_dt
        grace_end = last_engaged_dt.timestamp() + DECAY_GRACE_DAYS * 86400.0
        effective_anchor = max(decay_anchor.timestamp(), grace_end)
        decay_days = max(0.0, (now.timestamp() - effective_anchor) / 86400.0)
        if decay_days <= 0.0:
            continue

        before = float(row["enjoyment"] or 0.0)
        after = max(0.0, round(before - decay_days * DECAY_POINTS_PER_DAY, 3))
        previous_status = str(metadata.get("status") or "emerging")
        status = previous_status
        if inactivity_days >= LAPSED_INACTIVITY_DAYS and after <= LAPSED_STRENGTH:
            status = "lapsed"
        elif previous_status == "established" and after < DORMANT_STRENGTH:
            status = "dormant"
        elif previous_status == "recurring" and after < RECURRING_STRENGTH:
            status = "emerging"

        metadata["status"] = status
        metadata["last_decay_sim_time"] = now_sim_time
        conn.execute(
            "UPDATE character_hobbies SET enjoyment=?,metadata_json=? WHERE id=?",
            (after, json.dumps(metadata, ensure_ascii=False, sort_keys=True), row["id"]),
        )
        if after != before or status != previous_status:
            changes.append(
                {
                    "hobby_id": int(row["id"]),
                    "name": str(row["name"]),
                    "interest_strength_before": before,
                    "interest_strength_after": after,
                    "status_before": previous_status,
                    "status_after": status,
                    "inactivity_days": round(inactivity_days, 3),
                }
            )
    return changes


def settle_hobby_interest_lifecycle(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    action_name: str,
    target_id: str | None,
    ended_sim_time: str,
) -> dict[str, Any] | None:
    """Settle hobby/interest state from one completed represented engagement."""
    decay = _decay_dynamic_interests(conn, actor_id, now_sim_time=ended_sim_time)
    if action_name not in ELIGIBLE_ACTIONS or not target_id:
        return {"source": SOURCE, "decay": decay} if decay else None

    key = _interest_key(action_name, target_id)
    candidate: sqlite3.Row | None = None
    metadata: dict[str, Any] = {}
    for row in _dynamic_rows(conn, actor_id):
        item = _metadata(row)
        if item.get("interest_key") == key:
            candidate = row
            metadata = item
            break

    ended_day = _parse_time(ended_sim_time).date().isoformat()
    if candidate is None:
        weight = 1.0
        before = 0.0
        engagement_count = 1
        effective = 1.0
        distinct_days = 1
        after = round((100.0 - before) * FORMATION_RATE * weight, 3)
        status = _status_after_engagement(after, effective, distinct_days)
        name = _interest_name(conn, action_name, target_id)
        metadata = {
            "source": SOURCE,
            "interest_key": key,
            "activity": action_name,
            "target_name": _entity_name(conn, target_id),
            "status": status,
            "first_engaged_sim_time": ended_sim_time,
            "last_engaged_sim_time": ended_sim_time,
            "last_engaged_day": ended_day,
            "last_decay_sim_time": ended_sim_time,
            "engagement_count": engagement_count,
            "effective_engagements": effective,
            "distinct_engagement_days": distinct_days,
        }
        cursor = conn.execute(
            """
            INSERT INTO character_hobbies(entity_id,name,proficiency,frequency,enjoyment,metadata_json)
            VALUES(?,?,?,?,?,?)
            """,
            (
                actor_id,
                name,
                None,
                "emerging",
                after,
                json.dumps(metadata, ensure_ascii=False, sort_keys=True),
            ),
        )
        hobby_id = int(cursor.lastrowid)
        status_before = None
    else:
        last_engaged = metadata.get("last_engaged_sim_time")
        weight = _temporal_weight(
            str(last_engaged) if isinstance(last_engaged, str) else None,
            ended_sim_time,
        )
        before = float(candidate["enjoyment"] or 0.0)
        engagement_count = int(metadata.get("engagement_count", 0)) + 1
        effective = round(float(metadata.get("effective_engagements", 0.0)) + weight, 3)
        distinct_days = int(metadata.get("distinct_engagement_days", 1))
        if metadata.get("last_engaged_day") != ended_day:
            distinct_days += 1
        after = min(100.0, round(before + (100.0 - before) * FORMATION_RATE * weight, 3))
        status_before = str(metadata.get("status") or "emerging")
        status = _status_after_engagement(after, effective, distinct_days)
        metadata.update(
            {
                "status": status,
                "last_engaged_sim_time": ended_sim_time,
                "last_engaged_day": ended_day,
                "last_decay_sim_time": ended_sim_time,
                "engagement_count": engagement_count,
                "effective_engagements": effective,
                "distinct_engagement_days": distinct_days,
            }
        )
        conn.execute(
            "UPDATE character_hobbies SET frequency=?,enjoyment=?,metadata_json=? WHERE id=?",
            (
                status,
                after,
                json.dumps(metadata, ensure_ascii=False, sort_keys=True),
                candidate["id"],
            ),
        )
        hobby_id = int(candidate["id"])
        name = str(candidate["name"])

    return {
        "source": SOURCE,
        "engagement": {
            "hobby_id": hobby_id,
            "name": name,
            "interest_key": key,
            "interest_strength_before": before,
            "interest_strength_after": after,
            "status_before": status_before,
            "status_after": status,
            "engagement_count": engagement_count,
            "effective_engagements": effective,
            "distinct_engagement_days": distinct_days,
            "temporal_weight": weight,
        },
        "decay": decay,
    }


def hobby_dynamics_context(conn: sqlite3.Connection, actor_id: str) -> list[dict[str, Any]]:
    """Compact read-only developmental hobby/interest context for cognition."""
    result: list[dict[str, Any]] = []
    for row in _dynamic_rows(conn, actor_id):
        metadata = _metadata(row)
        result.append(
            {
                "name": str(row["name"]),
                "interest_strength": round(float(row["enjoyment"] or 0.0), 3),
                "status": str(metadata.get("status") or "emerging"),
                "activity": metadata.get("activity"),
                "subject": metadata.get("target_name"),
            }
        )
    return result

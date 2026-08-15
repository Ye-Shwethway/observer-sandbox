from __future__ import annotations

import json
import sqlite3
from collections import deque
from datetime import datetime, timedelta
from typing import Any

from .world import get_field, set_field


ADULT_MIN_AGE_YEARS = 18
MIN_DRIVE_FOR_ACTION = 60.0
BEHAVIOR_COOLDOWN_HOURS = 2.0
MAX_RELEASE_PRESSURE = 24.0
UNOBSERVED_HISTORY_PRESSURE = 12.0
RECENT_RELEASE_PENALTY_PER_24H = 7.0
POST_RELEASE_SUBSIDING_MINUTES = 30.0

_ALLOWED_PRIVATE_ACTIVITY_POLICIES = {
    "resident_private",
    "secluded",
    "secluded_when_alone",
}


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, round(float(value), 3)))


def _profile_exists(conn: sqlite3.Connection, actor_id: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM character_profiles WHERE entity_id=? LIMIT 1",
        (actor_id,),
    ).fetchone() is not None


def _profile_value(conn: sqlite3.Connection, actor_id: str, field_key: str, default: Any = None) -> Any:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    return default if row is None else json.loads(row[0])


def _age_years(conn: sqlite3.Connection, actor_id: str, as_of: datetime) -> int | None:
    raw = _profile_value(conn, actor_id, "identity.date_of_birth")
    if not raw:
        return None
    try:
        dob = datetime.fromisoformat(str(raw)).date()
    except ValueError:
        return None
    today = as_of.date()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


def _ancestor_locations(conn: sqlite3.Connection, location_id: str) -> set[str]:
    seen = {location_id}
    queue: deque[str] = deque([location_id])
    while queue:
        child = queue.popleft()
        rows = conn.execute(
            "SELECT source_id FROM relations WHERE relation_type='contains' AND target_id=?",
            (child,),
        ).fetchall()
        for row in rows:
            parent = str(row[0])
            if parent not in seen:
                seen.add(parent)
                queue.append(parent)
    return seen


def _descendant_locations(conn: sqlite3.Connection, root_id: str) -> set[str]:
    seen = {root_id}
    queue: deque[str] = deque([root_id])
    while queue:
        parent = queue.popleft()
        rows = conn.execute(
            """
            SELECT r.target_id
            FROM relations r
            JOIN entities e ON e.id=r.target_id
            WHERE r.relation_type='contains' AND r.source_id=? AND e.entity_type='location'
            """,
            (parent,),
        ).fetchall()
        for row in rows:
            child = str(row[0])
            if child not in seen:
                seen.add(child)
                queue.append(child)
    return seen


def _resident_roots(conn: sqlite3.Connection, actor_id: str) -> list[str]:
    rows = conn.execute(
        "SELECT source_id FROM relations WHERE relation_type='resident' AND target_id=? ORDER BY source_id",
        (actor_id,),
    ).fetchall()
    return [str(row[0]) for row in rows]


def _resident_scope(conn: sqlite3.Connection, actor_id: str, location_id: str) -> bool:
    ancestors = tuple(_ancestor_locations(conn, location_id))
    placeholders = ",".join("?" for _ in ancestors)
    return conn.execute(
        f"SELECT 1 FROM relations WHERE relation_type='resident' AND target_id=? AND source_id IN ({placeholders}) LIMIT 1",
        (actor_id, *ancestors),
    ).fetchone() is not None


def _character_ids_at(conn: sqlite3.Connection, location_ids: set[str], *, exclude_actor_id: str) -> list[str]:
    if not location_ids:
        return []
    ids: set[str] = set()
    placeholders = ",".join("?" for _ in location_ids)
    rows = conn.execute(
        f"""
        SELECT e.id FROM relations r
        JOIN entities e ON e.id=r.source_id
        WHERE r.relation_type='located_at' AND r.target_id IN ({placeholders})
          AND e.entity_type='character' AND e.id<>?
        """,
        (*sorted(location_ids), exclude_actor_id),
    ).fetchall()
    ids.update(str(row[0]) for row in rows)

    encoded_locations = [json.dumps(location_id) for location_id in sorted(location_ids)]
    placeholders = ",".join("?" for _ in encoded_locations)
    rows = conn.execute(
        f"""
        SELECT e.id FROM fields f
        JOIN entities e ON e.id=f.entity_id
        WHERE f.field_key='runtime.location' AND f.value_json IN ({placeholders})
          AND e.entity_type='character' AND e.id<>?
        """,
        (*encoded_locations, exclude_actor_id),
    ).fetchall()
    ids.update(str(row[0]) for row in rows)
    return sorted(ids)


def _other_characters_at(conn: sqlite3.Connection, actor_id: str, location_id: str) -> list[str]:
    return _character_ids_at(conn, {location_id}, exclude_actor_id=actor_id)


def _resident_scope_solitude(conn: sqlite3.Connection, actor_id: str) -> tuple[bool, list[str]]:
    locations: set[str] = set()
    for root_id in _resident_roots(conn, actor_id):
        locations.update(_descendant_locations(conn, root_id))
    others = _character_ids_at(conn, locations, exclude_actor_id=actor_id)
    return not others, others


def _private_activity_policy(conn: sqlite3.Connection, location_id: str) -> str:
    metadata = get_field(conn, location_id, "world.metadata", {})
    if isinstance(metadata, dict) and metadata.get("private_activity"):
        return str(metadata["private_activity"])
    # Compatibility fallback for worlds that predate explicit private-activity
    # metadata. New authored worlds should prefer world.metadata.private_activity.
    access = str(get_field(conn, location_id, "world.access", "open"))
    return "resident_private" if access == "private" else "shared"


def private_environment_context(conn: sqlite3.Connection, actor_id: str, location_id: str) -> dict[str, Any]:
    access = str(get_field(conn, location_id, "world.access", "open"))
    policy = _private_activity_policy(conn, location_id)
    others = _other_characters_at(conn, actor_id, location_id)
    privacy_suitable = policy in _ALLOWED_PRIVATE_ACTIVITY_POLICIES
    resident_scope = _resident_scope(conn, actor_id, location_id)
    return {
        "location_id": location_id,
        "access": access,
        "privacy_policy": policy,
        "private": privacy_suitable,
        "privacy_suitable": privacy_suitable,
        "resident_scope": resident_scope,
        "alone": not others,
        "other_characters": others,
        "safe_private": bool(privacy_suitable and resident_scope and not others),
    }


def _reachable_safe_private_locations(conn: sqlite3.Connection, actor_id: str, location_id: str) -> list[dict[str, Any]]:
    queue: deque[tuple[str, int]] = deque([(location_id, 0)])
    seen = {location_id}
    result: list[dict[str, Any]] = []
    while queue:
        current, distance = queue.popleft()
        rows = conn.execute(
            """
            SELECT e.id,e.name FROM relations r
            JOIN entities e ON e.id=r.target_id
            WHERE r.source_id=? AND r.relation_type='connected_to' AND e.entity_type='location'
            ORDER BY e.id
            """,
            (current,),
        ).fetchall()
        for row in rows:
            target_id = str(row["id"])
            if target_id in seen:
                continue
            seen.add(target_id)
            next_distance = distance + 1
            queue.append((target_id, next_distance))
            if private_environment_context(conn, actor_id, target_id)["safe_private"]:
                result.append({
                    "id": target_id,
                    "name": str(row["name"]),
                    "distance_steps": next_distance,
                })
    return sorted(result, key=lambda item: (int(item["distance_steps"]), str(item["id"])))


def _release_times(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of: datetime,
    days: int | None = None,
    hours: float | None = None,
) -> list[datetime]:
    params: list[Any] = [actor_id, as_of.isoformat()]
    where = "actor_id=? AND action_type='self_satisfaction' AND status='completed' AND ended_sim_time IS NOT NULL AND ended_sim_time<=?"
    if days is not None:
        where += " AND ended_sim_time>=?"
        params.append((as_of - timedelta(days=days)).isoformat())
    elif hours is not None:
        where += " AND ended_sim_time>=?"
        params.append((as_of - timedelta(hours=hours)).isoformat())
    rows = conn.execute(
        f"SELECT ended_sim_time FROM action_instances WHERE {where} ORDER BY ended_sim_time",
        tuple(params),
    ).fetchall()
    return [datetime.fromisoformat(str(row[0])) for row in rows]


def _age_drive_bonus(age_years: int) -> float:
    # A bounded gameplay heuristic for adult life-stage vitality, not a
    # population-frequency claim or clinical rule.
    if age_years <= 24:
        return 10.0
    if age_years <= 34:
        return 7.0
    if age_years <= 44:
        return 4.0
    if age_years <= 54:
        return 2.0
    return 0.0


def _recovery_bonus(*, fatigue: float, sleepiness: float, energy: float) -> float:
    energy_bonus = min(4.0, max(0.0, (energy - 55.0) * 0.12))
    fatigue_bonus = min(3.0, max(0.0, (30.0 - fatigue) * 0.10))
    sleep_bonus = min(3.0, max(0.0, (45.0 - sleepiness) * 0.08))
    return round(energy_bonus + fatigue_bonus + sleep_bonus, 3)


def _drive_ramp_hours(libido: float) -> float:
    # Higher authored libido rebuilds discretionary desire salience faster,
    # while remaining bounded and separate from the short anti-loop cooldown.
    return round(max(16.0, min(40.0, 48.0 - _clamp(libido) * 0.35)), 3)


def _drive(
    *,
    libido: float,
    age_years: int,
    fatigue: float,
    sleepiness: float,
    energy: float,
    hours_since_release: float | None,
    recent_24h_count: int,
    resident_scope_solitary: bool,
) -> tuple[float, dict[str, float]]:
    base = _clamp(libido) * 0.58
    age_bonus = _age_drive_bonus(age_years)
    recovery_bonus = _recovery_bonus(fatigue=fatigue, sleepiness=sleepiness, energy=energy)
    solitude_bonus = 5.0 if resident_scope_solitary else 0.0
    ramp_hours = _drive_ramp_hours(libido)
    release_pressure = (
        UNOBSERVED_HISTORY_PRESSURE
        if hours_since_release is None
        else min(MAX_RELEASE_PRESSURE, max(0.0, hours_since_release) / ramp_hours * MAX_RELEASE_PRESSURE)
    )
    recent_release_penalty = max(0, recent_24h_count) * RECENT_RELEASE_PENALTY_PER_24H
    fatigue_penalty = max(0.0, fatigue - 55.0) * 0.16
    sleep_penalty = max(0.0, sleepiness - 75.0) * 0.12
    energy_penalty = max(0.0, 30.0 - energy) * 0.20
    drive = _clamp(
        base
        + age_bonus
        + recovery_bonus
        + solitude_bonus
        + release_pressure
        - recent_release_penalty
        - fatigue_penalty
        - sleep_penalty
        - energy_penalty
    )
    return drive, {
        "libido_base": round(base, 3),
        "age_bonus": round(age_bonus, 3),
        "recovery_bonus": round(recovery_bonus, 3),
        "solitude_bonus": round(solitude_bonus, 3),
        "release_pressure": round(release_pressure, 3),
        "recent_24h_penalty": round(recent_release_penalty, 3),
        "fatigue_penalty": round(fatigue_penalty, 3),
        "sleep_penalty": round(sleep_penalty, 3),
        "energy_penalty": round(energy_penalty, 3),
        "drive_ramp_hours": ramp_hours,
    }


def solo_sexual_regulation_context(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    state: dict[str, Any],
) -> dict[str, Any]:
    as_of = datetime.fromisoformat(str(state["sim_time"]))
    location_id = str(state["location"])
    represented = _profile_exists(conn, actor_id)
    age = _age_years(conn, actor_id, as_of) if represented else None
    adult = represented and age is not None and age >= ADULT_MIN_AGE_YEARS
    libido = float(_profile_value(conn, actor_id, "raps_sa.libido", 0.0) or 0.0) if represented else 0.0
    releases = _release_times(conn, actor_id, as_of=as_of) if represented else []
    last_release = releases[-1] if releases else None
    hours_since_release = None if last_release is None else max(0.0, (as_of - last_release).total_seconds() / 3600.0)
    recent_7d_count = len(_release_times(conn, actor_id, as_of=as_of, days=7)) if represented else 0
    recent_24h_count = len(_release_times(conn, actor_id, as_of=as_of, hours=24.0)) if represented else 0
    resident_scope_solitary, resident_scope_others = _resident_scope_solitude(conn, actor_id) if represented else (False, [])
    if adult and age is not None:
        drive, drive_components = _drive(
            libido=libido,
            age_years=age,
            fatigue=float(state.get("fatigue", 0.0)),
            sleepiness=float(state.get("sleepiness", 0.0)),
            energy=float(state.get("energy", 75.0)),
            hours_since_release=hours_since_release,
            recent_24h_count=recent_24h_count,
            resident_scope_solitary=resident_scope_solitary,
        )
    else:
        drive, drive_components = 0.0, {}
    cooldown_remaining = 0.0 if hours_since_release is None else max(0.0, BEHAVIOR_COOLDOWN_HOURS - hours_since_release)
    environment = private_environment_context(conn, actor_id, location_id)
    available = bool(adult and environment["safe_private"] and cooldown_remaining <= 0.0 and drive >= MIN_DRIVE_FOR_ACTION)
    return {
        "source": "solo-sexual-regulation-v2-naturalism",
        "represented": represented,
        "adult": adult,
        "age_years": age,
        "baseline_libido": round(libido, 3),
        "drive": drive,
        "drive_components": drive_components,
        "action_threshold": MIN_DRIVE_FOR_ACTION,
        "recent_7d_count": recent_7d_count,
        "recent_24h_count": recent_24h_count,
        "last_release_sim_time": last_release.isoformat() if last_release else None,
        "hours_since_last_release": round(hours_since_release, 3) if hours_since_release is not None else None,
        "cooldown_remaining_hours": round(cooldown_remaining, 3),
        "resident_scope_solitary": resident_scope_solitary,
        "resident_scope_other_characters": resident_scope_others,
        "private_environment": environment,
        "reachable_safe_private_locations": _reachable_safe_private_locations(conn, actor_id, location_id) if adult else [],
        "available_now": available,
        "guidance": (
            "This is a legitimate private discretionary self-regulation option when available; it is never a weekly quota or mandatory routine. "
            "Current drive reflects authored libido, adult life-stage, recovery condition, release recency, recent same-day activity, and represented home solitude. "
            "If drive is meaningful but the current room is unsuitable, moving through the normal location graph to an authorized private-activity location may be considered before the behavior."
            if adult
            else "Solo sexual behavior is unavailable unless an adult sexual profile is represented for this actor."
        ),
    }


def self_satisfaction_action_option(conn: sqlite3.Connection, actor_id: str, *, state: dict[str, Any]) -> dict[str, Any] | None:
    context = solo_sexual_regulation_context(conn, actor_id, state=state)
    if not context["available_now"]:
        return None
    return {
        "action": "self_satisfaction",
        "target": None,
        "target_name": None,
        "duration": (5, 45),
        "solo_regulation": {
            "drive": context["drive"],
            "recent_7d_count": context["recent_7d_count"],
            "recent_24h_count": context["recent_24h_count"],
            "private_safe": True,
        },
    }


def validate_self_satisfaction_action(conn: sqlite3.Connection, actor_id: str, *, state: dict[str, Any]) -> dict[str, Any]:
    context = solo_sexual_regulation_context(conn, actor_id, state=state)
    if not context["represented"] or not context["adult"]:
        raise ValueError("Self-satisfaction is unavailable for non-adult or unrepresented actors")
    if not context["private_environment"]["safe_private"]:
        raise ValueError("Self-satisfaction requires an authorized private environment with no other character present")
    if context["cooldown_remaining_hours"] > 0:
        raise ValueError("Self-satisfaction is temporarily unavailable during the behavioral cooldown")
    if context["drive"] < MIN_DRIVE_FOR_ACTION:
        raise ValueError("Self-satisfaction is not currently supported by sufficient sexual-regulation drive")
    return context


def begin_self_satisfaction_action(conn: sqlite3.Connection, actor_id: str, *, state: dict[str, Any]) -> dict[str, Any]:
    context = validate_self_satisfaction_action(conn, actor_id, state=state)
    baseline = float(_profile_value(conn, actor_id, "sexual_anatomy.baseline_erectile_function", 0.0) or 0.0)
    cap = float(_profile_value(conn, actor_id, "sexual_anatomy.erection_firmness_cap", 100.0) or 100.0)
    arousal = _clamp(max(60.0, float(context["drive"])))
    firmness = _clamp(min(cap, baseline * (0.65 + 0.003 * float(context["drive"]))))
    erectile_state = "erect" if firmness >= 70.0 else "developing"
    set_field(conn, actor_id, "sexual_state.solo_regulation_drive", float(context["drive"]), authority="sexual_behavior_engine", source="solo-sexual-regulation-v2-naturalism")
    set_field(conn, actor_id, "sexual_state.arousal_level", arousal, authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
    set_field(conn, actor_id, "sexual_anatomy.erection_firmness", firmness, authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
    set_field(conn, actor_id, "sexual_anatomy.erectile_state", erectile_state, authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
    return {
        "drive": float(context["drive"]),
        "arousal_level": arousal,
        "erection_firmness": firmness,
        "erectile_state": erectile_state,
        "private_safe": True,
    }


def _set_weekly_count(conn: sqlite3.Connection, actor_id: str, count: int, *, sim_time: str) -> bool:
    field_key = "raps_sa.self_satisfaction_weekly"
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    old_value = None if row is None else json.loads(row[0])
    if old_value == count:
        return False
    conn.execute(
        """
        INSERT INTO character_profile_values(entity_id,field_key,value_json,mode,authority,source,observed_at)
        VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(entity_id,field_key) DO UPDATE SET
            value_json=excluded.value_json,
            mode=excluded.mode,
            authority=excluded.authority,
            source=excluded.source,
            observed_at=excluded.observed_at,
            updated_at=CURRENT_TIMESTAMP
        """,
        (actor_id, field_key, json.dumps(count), "simulated", "sexual_behavior_engine", "solo-sexual-regulation-v2-naturalism", sim_time),
    )
    conn.execute(
        """
        INSERT INTO character_profile_history(entity_id,field_key,old_value_json,new_value_json,mode,authority,reason,sim_time)
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            actor_id,
            field_key,
            None if old_value is None else json.dumps(old_value),
            json.dumps(count),
            "simulated",
            "sexual_behavior_engine",
            "rolling seven-day count from completed self-satisfaction actions",
            sim_time,
        ),
    )
    return True


def settle_solo_sexual_regulation(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    action_name: str,
    ended_sim_time: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    if not _profile_exists(conn, actor_id):
        return {
            "source": "solo-sexual-regulation-v2-naturalism",
            "represented": False,
            "release_completed": False,
            "weekly_count_changed": False,
        }

    as_of = datetime.fromisoformat(ended_sim_time)
    weekly_count = len(_release_times(conn, actor_id, as_of=as_of, days=7))
    weekly_changed = _set_weekly_count(conn, actor_id, weekly_count, sim_time=ended_sim_time)

    if action_name == "self_satisfaction":
        libido = float(_profile_value(conn, actor_id, "raps_sa.libido", 0.0) or 0.0)
        post_drive = _clamp(libido * 0.25)
        set_field(conn, actor_id, "sexual_state.solo_regulation_drive", post_drive, authority="sexual_behavior_engine", source="solo-sexual-regulation-v2-naturalism")
        set_field(conn, actor_id, "sexual_state.arousal_level", 5.0, authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
        set_field(conn, actor_id, "sexual_anatomy.erection_firmness", 10.0, authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
        set_field(conn, actor_id, "sexual_anatomy.erectile_state", "subsiding", authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
        return {
            "source": "solo-sexual-regulation-v2-naturalism",
            "represented": True,
            "release_completed": True,
            "weekly_count": weekly_count,
            "weekly_count_changed": weekly_changed,
            "post_state": "subsiding",
            "post_arousal_level": 5.0,
            "post_erection_firmness": 10.0,
            "post_drive": post_drive,
        }

    context = solo_sexual_regulation_context(conn, actor_id, state={**state, "sim_time": ended_sim_time})
    if context["adult"]:
        set_field(conn, actor_id, "sexual_state.solo_regulation_drive", float(context["drive"]), authority="sexual_behavior_engine", source="solo-sexual-regulation-v2-naturalism")
        last_release = context.get("last_release_sim_time")
        if last_release:
            minutes_since = max(0.0, (as_of - datetime.fromisoformat(str(last_release))).total_seconds() / 60.0)
            if minutes_since >= POST_RELEASE_SUBSIDING_MINUTES:
                set_field(conn, actor_id, "sexual_state.arousal_level", 0.0, authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
                set_field(conn, actor_id, "sexual_anatomy.erection_firmness", 0.0, authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
                set_field(conn, actor_id, "sexual_anatomy.erectile_state", "flaccid", authority="sexual_physiology_engine", source="solo-sexual-regulation-v2-naturalism")
    return {
        "source": "solo-sexual-regulation-v2-naturalism",
        "represented": True,
        "release_completed": False,
        "weekly_count": weekly_count,
        "weekly_count_changed": weekly_changed,
        "drive": float(context["drive"]),
    }

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any

SESSION_BREAK_MINUTES = 120
SESSION_LIMIT = 90.0
RECENT_HOURS = 6
RECENT_LIMIT = 120.0
DAILY_HOURS = 24
DAILY_LIMIT = 180.0


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _effective_minutes(row: sqlite3.Row) -> float:
    outcome = json.loads(row["outcome_json"] or "{}")
    load = outcome.get("training_load", {}) if isinstance(outcome, dict) else {}
    if isinstance(load, dict) and load.get("effective_minutes") is not None:
        return max(0.0, float(load["effective_minutes"]))
    modifiers = json.loads(row["modifiers_json"] or "{}")
    readiness = modifiers.get("training_readiness", {}) if isinstance(modifiers, dict) else {}
    effectiveness = float(readiness.get("effectiveness", readiness.get("readiness", 1.0))) if isinstance(readiness, dict) else 1.0
    return max(0.0, float(row["duration_minutes"]) * max(0.0, min(1.0, effectiveness)))


def training_load_status(conn: sqlite3.Connection, actor_id: str, *, sim_time: str) -> dict[str, Any]:
    now = datetime.fromisoformat(sim_time)
    rows = conn.execute(
        """SELECT id,duration_minutes,planned_sim_time,started_sim_time,ended_sim_time,modifiers_json,outcome_json
        FROM action_instances
        WHERE actor_id=? AND action_type='train' AND status='completed' AND ended_sim_time IS NOT NULL
        ORDER BY ended_sim_time ASC,id ASC""",
        (actor_id,),
    ).fetchall()
    items: list[dict[str, Any]] = []
    for row in rows:
        ended = datetime.fromisoformat(row["ended_sim_time"])
        if ended > now:
            continue
        started = datetime.fromisoformat(row["started_sim_time"] or row["planned_sim_time"])
        items.append({"started": started, "ended": ended, "effective": _effective_minutes(row)})

    recent = sum(item["effective"] for item in items if item["ended"] >= now - timedelta(hours=RECENT_HOURS))
    daily = sum(item["effective"] for item in items if item["ended"] >= now - timedelta(hours=DAILY_HOURS))
    session_items: list[dict[str, Any]] = []
    if items and now - items[-1]["ended"] <= timedelta(minutes=SESSION_BREAK_MINUTES):
        session_items = [items[-1]]
        cursor = items[-1]["started"]
        for item in reversed(items[:-1]):
            if cursor - item["ended"] > timedelta(minutes=SESSION_BREAK_MINUTES):
                break
            session_items.append(item)
            cursor = item["started"]
    session = sum(item["effective"] for item in session_items)
    remaining = min(SESSION_LIMIT - session, RECENT_LIMIT - recent, DAILY_LIMIT - daily)
    allowed = remaining > 0.0
    blocked_by: list[str] = []
    if session >= SESSION_LIMIT:
        blocked_by.append("session_load")
    if recent >= RECENT_LIMIT:
        blocked_by.append("recent_6h_load")
    if daily >= DAILY_LIMIT:
        blocked_by.append("daily_24h_load")
    return {
        "source": "training-session-load-recovery-guard-v1",
        "allowed": allowed,
        "blocked_by": blocked_by,
        "session_effective_minutes": round(session, 3),
        "recent_6h_effective_minutes": round(recent, 3),
        "daily_24h_effective_minutes": round(daily, 3),
        "remaining_effective_minutes": round(max(0.0, remaining), 3),
        "limits": {"session": SESSION_LIMIT, "recent_6h": RECENT_LIMIT, "daily_24h": DAILY_LIMIT},
    }


def training_behavior_balance(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    state: dict[str, Any],
    load_status: dict[str, Any],
) -> dict[str, Any]:
    """Return a soft training-repetition signal without changing action legality.

    The hard load guard remains authoritative for safety. This signal exists only
    to make repeated discretionary training progressively less attractive when
    recent dose, bout frequency, recency, or recovery state already make other
    meaningful activity more natural.
    """
    now = datetime.fromisoformat(str(state["sim_time"]))
    rows = conn.execute(
        """SELECT ended_sim_time
        FROM action_instances
        WHERE actor_id=? AND action_type='train' AND status='completed' AND ended_sim_time IS NOT NULL
        ORDER BY ended_sim_time ASC,id ASC""",
        (actor_id,),
    ).fetchall()
    ended_times = [
        datetime.fromisoformat(str(row["ended_sim_time"]))
        for row in rows
        if datetime.fromisoformat(str(row["ended_sim_time"])) <= now
    ]
    daily_cutoff = now - timedelta(hours=DAILY_HOURS)
    bouts_24h = sum(1 for ended in ended_times if ended >= daily_cutoff)
    last_ended = ended_times[-1] if ended_times else None
    minutes_since_last = None if last_ended is None else max(0.0, (now - last_ended).total_seconds() / 60.0)

    daily_pressure = _clamp01(float(load_status["daily_24h_effective_minutes"]) / DAILY_LIMIT)
    recent_pressure = _clamp01(float(load_status["recent_6h_effective_minutes"]) / RECENT_LIMIT)
    bout_pressure = _clamp01(bouts_24h / 4.0)
    if minutes_since_last is None or minutes_since_last >= 480.0:
        recency_pressure = 0.0
    elif minutes_since_last <= 120.0:
        recency_pressure = 1.0
    else:
        recency_pressure = _clamp01((480.0 - minutes_since_last) / 360.0)

    fatigue = float(state.get("fatigue", 0.0))
    energy = float(state.get("energy", 100.0))
    fatigue_pressure = _clamp01((fatigue - 25.0) / 50.0)
    energy_pressure = _clamp01((60.0 - energy) / 40.0)

    pressure = _clamp01(
        0.28 * daily_pressure
        + 0.22 * recent_pressure
        + 0.18 * bout_pressure
        + 0.14 * recency_pressure
        + 0.10 * fatigue_pressure
        + 0.08 * energy_pressure
    )
    if pressure >= 0.55:
        level = "high"
        guidance = (
            "Training is still legal when a train option is present, but recent dose/frequency and recovery context make another workout low priority. "
            "Prefer recovery or a meaningful non-training activity unless there is a concrete reason to train again and current recovery state supports it."
        )
    elif pressure >= 0.30:
        level = "moderate"
        guidance = (
            "Training remains available, but recent training creates a soft preference for variety. "
            "Choose another meaningful activity when it fits as well; repeat training only for a concrete purpose rather than because the facility is convenient."
        )
    else:
        level = "low"
        guidance = "No meaningful repetition pressure is active; training may compete normally with other suitable activities."

    return {
        "source": "training-behavior-balance-v1",
        "hard_block": False,
        "repetition_pressure": round(pressure, 3),
        "level": level,
        "completed_training_bouts_24h": bouts_24h,
        "minutes_since_last_training": None if minutes_since_last is None else round(minutes_since_last, 1),
        "signals": {
            "daily_dose": round(daily_pressure, 3),
            "recent_6h_dose": round(recent_pressure, 3),
            "bout_frequency": round(bout_pressure, 3),
            "recency": round(recency_pressure, 3),
            "fatigue": round(fatigue_pressure, 3),
            "low_energy": round(energy_pressure, 3),
        },
        "guidance": guidance,
    }


def shape_training_options_for_load(conn: sqlite3.Connection, actor_id: str, *, state: dict[str, Any], action_options: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    status = training_load_status(conn, actor_id, sim_time=str(state["sim_time"]))
    balance = training_behavior_balance(conn, actor_id, state=state, load_status=status)
    status = {**status, "behavioral_balance": balance}
    shaped: list[dict[str, Any]] = []
    for option in action_options:
        if option.get("action") != "train":
            shaped.append(option)
            continue
        readiness = option.get("modifiers", {}).get("training_readiness", {})
        effectiveness = float(readiness.get("effectiveness", readiness.get("readiness", 1.0))) if isinstance(readiness, dict) else 1.0
        effectiveness = max(0.0, min(1.0, effectiveness))
        remaining = float(status["remaining_effective_minutes"])
        max_planned = int(remaining / effectiveness) if effectiveness > 0 else 0
        low, high = option.get("duration", (10, 240))
        capped_high = min(int(high), max_planned)
        if not status["allowed"] or capped_high < int(low):
            continue
        copy = dict(option)
        copy["duration"] = (int(low), capped_high)
        copy["training_load_guard"] = status
        copy["training_behavior_balance"] = balance
        shaped.append(copy)
    return shaped, status


def projected_training_allowed(status: dict[str, Any], *, duration_minutes: int, effectiveness: float) -> bool:
    projected = max(0.0, float(duration_minutes) * max(0.0, min(1.0, float(effectiveness))))
    return projected <= float(status["remaining_effective_minutes"]) + 1e-9

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


def shape_training_options_for_load(conn: sqlite3.Connection, actor_id: str, *, state: dict[str, Any], action_options: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    status = training_load_status(conn, actor_id, sim_time=str(state["sim_time"]))
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
        shaped.append(copy)
    return shaped, status


def projected_training_allowed(status: dict[str, Any], *, duration_minutes: int, effectiveness: float) -> bool:
    projected = max(0.0, float(duration_minutes) * max(0.0, min(1.0, float(effectiveness))))
    return projected <= float(status["remaining_effective_minutes"]) + 1e-9

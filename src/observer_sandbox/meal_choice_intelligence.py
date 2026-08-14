from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any

from .nutrition_energy import energy_balance_window, resting_energy_reference


MEAL_CHOICE_SOURCE = "meal-choice-intelligence-v1"
RECENT_TRAINING_HOURS = 12.0


def _completed_action_rows(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id",
        (actor_id,),
    ).fetchall()


def _minutes_since(now: datetime, then_raw: str | None) -> float | None:
    if not isinstance(then_raw, str):
        return None
    try:
        then = datetime.fromisoformat(then_raw)
    except ValueError:
        return None
    minutes = (now - then).total_seconds() / 60.0
    if minutes < 0.0:
        return None
    return round(minutes, 1)


def _last_meal_context(rows: list[sqlite3.Row], now: datetime) -> dict[str, Any] | None:
    for row in reversed(rows):
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") != "eat":
            continue
        nutrition = payload.get("nutrition_intake")
        ended = payload.get("action_ended_sim_time") or row["sim_time"]
        result: dict[str, Any] = {
            "ended_sim_time": ended,
            "minutes_ago": _minutes_since(now, ended if isinstance(ended, str) else None),
        }
        if isinstance(nutrition, dict):
            result["energy_kcal"] = round(float(nutrition.get("energy_kcal", 0.0)), 1)
            result["protein_g"] = round(float(nutrition.get("protein_g", 0.0)), 1)
            result["source"] = nutrition.get("source")
        return result
    return None


def _recent_training_context(rows: list[sqlite3.Row], now: datetime) -> dict[str, Any]:
    cutoff = now - timedelta(hours=RECENT_TRAINING_HOURS)
    count = 0
    minutes = 0.0
    last_ended: str | None = None
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") != "train":
            continue
        ended_raw = payload.get("action_ended_sim_time") or row["sim_time"]
        if not isinstance(ended_raw, str):
            continue
        try:
            ended = datetime.fromisoformat(ended_raw)
        except ValueError:
            continue
        if ended < cutoff or ended > now:
            continue
        count += 1
        duration = payload.get("duration_minutes")
        if isinstance(duration, (int, float)):
            minutes += max(0.0, float(duration))
        last_ended = ended_raw
    return {
        "window_hours": RECENT_TRAINING_HOURS,
        "completed_sessions": count,
        "completed_minutes": round(minutes, 1),
        "minutes_since_last_training": _minutes_since(now, last_ended),
    }


def meal_choice_context(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    state: dict[str, Any],
    autonomy_policy: dict[str, Any],
) -> dict[str, Any]:
    """Build compact deterministic meal-choice context for an existing cognition call.

    This is decision support only. It never selects food, mutates inventory, invents
    nutrition targets, or adds another model call.
    """
    now = datetime.fromisoformat(str(state["sim_time"]))
    day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if now <= day_start:
        day_start = now - timedelta(minutes=1)

    balance = energy_balance_window(
        conn,
        actor_id,
        start_sim_time=day_start.isoformat(),
        end_sim_time=now.isoformat(),
    )
    resting = resting_energy_reference(conn, actor_id, as_of_sim_time=str(state["sim_time"]))
    rows = _completed_action_rows(conn, actor_id)
    nutrition_policy = autonomy_policy.get("nutrition_policy", {})
    if not isinstance(nutrition_policy, dict):
        nutrition_policy = {}

    return {
        "source": MEAL_CHOICE_SOURCE,
        "sim_day": now.date().isoformat(),
        "today": {
            "intake_kcal": balance["intake_kcal"],
            "protein_g": balance["protein_g"],
            "carbohydrate_g": balance["carbohydrate_g"],
            "fat_g": balance["fat_g"],
            "meal_count": balance["intake_event_count"],
            "estimated_expenditure_kcal": balance["expenditure_kcal"],
            "evidence_coverage_ratio": balance["coverage_ratio"],
        },
        "last_meal": _last_meal_context(rows, now),
        "recent_training": _recent_training_context(rows, now),
        "current_recovery": {
            "hunger": round(float(state.get("hunger", 0.0)), 1),
            "energy": round(float(state.get("energy", 0.0)), 1),
            "fatigue": round(float(state.get("fatigue", 0.0)), 1),
            "sleepiness": round(float(state.get("sleepiness", 0.0)), 1),
            "thirst": round(float(state.get("thirst", 0.0)), 1),
        },
        "resting_energy_reference": None if resting is None else {
            "ree_kcal_day": resting["ree_kcal_day"],
            "note": "Reference resting estimate only; not a daily calorie target.",
        },
        "character_nutrition_policy": {
            "goal": nutrition_policy.get("goal", "support ordinary health, activity, and stable body composition"),
            "energy_intent": nutrition_policy.get("energy_intent", "contextual maintenance"),
            "protein_priority": nutrition_policy.get("protein_priority", "contextual"),
            "dietary_constraints": list(nutrition_policy.get("dietary_constraints", [])),
            "guidance": nutrition_policy.get(
                "guidance",
                "Use accumulated intake, recent training/recovery, hunger and available foods to choose a plausible meal. Do not invent nutrient values or treat the resting estimate as a calorie target.",
            ),
        },
    }

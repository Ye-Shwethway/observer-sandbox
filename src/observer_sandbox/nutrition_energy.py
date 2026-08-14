from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
NUTRITION_PATH = REPO_ROOT / "config" / "nutrition_profiles.v1.json"
ENERGY_PATH = REPO_ROOT / "config" / "energy_expenditure.v1.json"
EVIDENCE_SOURCE = "nutrition-energy-evidence-v1"
MIN_WINDOW_COVERAGE = 0.95


@lru_cache(maxsize=1)
def load_nutrition_catalog(path: str | Path = NUTRITION_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_energy_policy(path: str | Path = ENERGY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def nutrition_profile_for_target(target: str | None) -> dict[str, Any] | None:
    if not target:
        return None
    source = load_nutrition_catalog()
    raw = source.get("profiles", {}).get(target)
    if not isinstance(raw, dict):
        return None
    result = dict(raw)
    result["target"] = target
    result["source"] = str(source.get("revision", "nutrition-evidence-v1"))
    return result


def nutrition_intake_evidence(*, action_name: str, target: str | None) -> dict[str, Any] | None:
    if action_name != "eat":
        return None
    profile = nutrition_profile_for_target(target)
    if profile is None:
        return None
    energy = float(profile["energy_kcal"])
    protein = float(profile["protein_g"])
    carbs = float(profile.get("carbohydrate_g", 0.0))
    fat = float(profile.get("fat_g", 0.0))
    if energy <= 0.0 or min(protein, carbs, fat) < 0.0:
        raise ValueError(f"Invalid authored nutrition profile for {target}")
    return {
        "target": target,
        "portion_label": str(profile.get("portion_label", "authored portion")),
        "energy_kcal": round(energy, 3),
        "protein_g": round(protein, 3),
        "carbohydrate_g": round(carbs, 3),
        "fat_g": round(fat, 3),
        "source": profile["source"],
    }


def _profile_value(conn: sqlite3.Connection, actor_id: str, field_key: str) -> Any | None:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    return None if row is None else json.loads(row["value_json"])


def _age_years(dob_raw: str, as_of_sim_time: str) -> float:
    born = date.fromisoformat(dob_raw)
    as_of = datetime.fromisoformat(as_of_sim_time).date()
    if as_of < born:
        raise ValueError("simulation time precedes actor date of birth")
    return (as_of - born).days / 365.2425


def resting_energy_reference(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
) -> dict[str, Any] | None:
    """Return an actor-specific healthy-adult REE estimate when inputs are supported.

    Mifflin-St Jeor is a reference estimate, not a measured metabolic rate. The
    function deliberately returns None instead of inventing a sex coefficient or
    body size when a required canonical/profile input is unavailable.
    """
    weight_lb = _profile_value(conn, actor_id, "body.weight_lb")
    height_in = _profile_value(conn, actor_id, "body.height_in")
    sex_raw = _profile_value(conn, actor_id, "identity.sex")
    dob_raw = _profile_value(conn, actor_id, "identity.date_of_birth")
    if weight_lb is None or height_in is None or sex_raw is None or dob_raw is None:
        return None
    sex = str(sex_raw).strip().lower()
    if sex not in {"male", "female"}:
        return None
    weight_kg = float(weight_lb) / 2.2046226218
    height_cm = float(height_in) * 2.54
    age_years = _age_years(str(dob_raw), as_of_sim_time)
    if weight_kg <= 0.0 or height_cm <= 0.0:
        return None
    sex_constant = 5.0 if sex == "male" else -161.0
    ree = 10.0 * weight_kg + 6.25 * height_cm - 5.0 * age_years + sex_constant
    if ree <= 0.0:
        return None
    policy = load_energy_policy()
    return {
        "ree_kcal_day": round(ree, 3),
        "formula": str(policy.get("resting_reference", {}).get("formula", "mifflin-st-jeor-1990")),
        "weight_kg": round(weight_kg, 6),
        "height_cm": round(height_cm, 3),
        "age_years": round(age_years, 6),
        "sex": sex,
        "source": str(policy.get("revision", "energy-expenditure-evidence-v1")),
    }


def activity_multiplier(action_name: str, target: str | None) -> float | None:
    policy = load_energy_policy()
    if action_name == "train" and target:
        override = policy.get("training_target_multipliers", {}).get(target)
        if isinstance(override, (int, float)):
            return float(override)
    value = policy.get("action_multipliers", {}).get(action_name)
    if not isinstance(value, (int, float)):
        return None
    return float(value)


def energy_expenditure_evidence(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    action_name: str,
    target: str | None,
    duration_minutes: int | float,
    as_of_sim_time: str,
) -> dict[str, Any] | None:
    duration = float(duration_minutes)
    if duration <= 0.0:
        return None
    multiplier = activity_multiplier(action_name, target)
    if multiplier is None or multiplier <= 0.0:
        return None
    resting = resting_energy_reference(conn, actor_id, as_of_sim_time=as_of_sim_time)
    if resting is None:
        return None
    resting_kcal = float(resting["ree_kcal_day"]) * duration / 1440.0
    estimated = resting_kcal * multiplier
    return {
        "estimated_kcal": round(estimated, 3),
        "resting_kcal_component": round(resting_kcal, 3),
        "activity_multiplier": round(multiplier, 3),
        "duration_minutes": round(duration, 3),
        "resting_reference": resting,
        "source": str(load_energy_policy().get("revision", "energy-expenditure-evidence-v1")),
        "model_note": "Actor-scaled deterministic estimate; activity multiplier is an authored Compendium-informed intensity anchor, not direct calorimetry.",
    }


def energy_balance_window(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    start_sim_time: str,
    end_sim_time: str,
) -> dict[str, Any]:
    """Aggregate immutable intake/expenditure evidence over a bounded sim window.

    Historical actions that predate BC-1 intentionally do not get recomputed from
    current policy. Missing stored evidence lowers coverage and makes the window
    incomplete, preventing future body-composition code from treating absence of
    evidence as a physiological deficit.
    """
    start = datetime.fromisoformat(start_sim_time)
    end = datetime.fromisoformat(end_sim_time)
    if end <= start:
        raise ValueError("energy balance window requires end > start")
    window_minutes = (end - start).total_seconds() / 60.0
    expenditure = 0.0
    intake = 0.0
    protein = 0.0
    carbs = 0.0
    fat = 0.0
    covered_minutes = 0.0
    intake_events = 0
    missing_energy: list[int] = []
    missing_nutrition: list[int] = []

    rows = conn.execute(
        "SELECT id,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id",
        (actor_id,),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        started_raw = payload.get("action_started_sim_time")
        ended_raw = payload.get("action_ended_sim_time")
        if not isinstance(started_raw, str) or not isinstance(ended_raw, str):
            continue
        action_start = datetime.fromisoformat(started_raw)
        action_end = datetime.fromisoformat(ended_raw)
        overlap_start = max(start, action_start)
        overlap_end = min(end, action_end)
        if overlap_end <= overlap_start:
            continue
        overlap_minutes = (overlap_end - overlap_start).total_seconds() / 60.0
        duration = max(0.0, (action_end - action_start).total_seconds() / 60.0)
        energy = payload.get("energy_expenditure")
        if isinstance(energy, dict) and duration > 0.0 and isinstance(energy.get("estimated_kcal"), (int, float)):
            expenditure += float(energy["estimated_kcal"]) * overlap_minutes / duration
            covered_minutes += overlap_minutes
        else:
            missing_energy.append(int(row["id"]))

        # Intake is an event at completion, so count it once only when completion
        # falls inside the aggregation window rather than prorating a meal.
        if payload.get("action") == "eat" and start < action_end <= end:
            nutrition = payload.get("nutrition_intake")
            if isinstance(nutrition, dict) and isinstance(nutrition.get("energy_kcal"), (int, float)):
                intake += float(nutrition["energy_kcal"])
                protein += float(nutrition.get("protein_g", 0.0))
                carbs += float(nutrition.get("carbohydrate_g", 0.0))
                fat += float(nutrition.get("fat_g", 0.0))
                intake_events += 1
            else:
                missing_nutrition.append(int(row["id"]))

    coverage_ratio = min(1.0, covered_minutes / window_minutes)
    complete = (
        coverage_ratio >= MIN_WINDOW_COVERAGE
        and not missing_energy
        and not missing_nutrition
    )
    return {
        "actor_id": actor_id,
        "start_sim_time": start_sim_time,
        "end_sim_time": end_sim_time,
        "window_minutes": round(window_minutes, 3),
        "covered_action_minutes": round(covered_minutes, 3),
        "coverage_ratio": round(coverage_ratio, 6),
        "complete": complete,
        "intake_kcal": round(intake, 3),
        "protein_g": round(protein, 3),
        "carbohydrate_g": round(carbs, 3),
        "fat_g": round(fat, 3),
        "intake_event_count": intake_events,
        "expenditure_kcal": round(expenditure, 3),
        "net_energy_kcal": round(intake - expenditure, 3),
        "missing_energy_event_ids": missing_energy,
        "missing_nutrition_event_ids": missing_nutrition,
        "source": EVIDENCE_SOURCE,
    }

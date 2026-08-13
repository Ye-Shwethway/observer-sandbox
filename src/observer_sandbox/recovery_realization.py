from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any


RECOVERY_CURVE_ID = "strength-recovery-realization-v1"
MIN_RECOVERY_HOURS = 6.0
FULL_RECOVERY_HOURS = 48.0
FATIGUE_HARD_BLOCK = 70.0


@dataclass(frozen=True)
class StrengthRecoveryEvidence:
    curve_id: str
    elapsed_hours: float
    time_factor: float
    state_quality: float
    recovery_multiplier: float
    recovery_factor: float
    blocked: bool
    latest_stimulus_sim_time: str | None
    components: dict[str, float]


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _higher_is_better(value: float, *, good: float, bad: float) -> float:
    return _clamp01((float(value) - bad) / (good - bad))


def _lower_is_better(value: float, *, good: float, bad: float) -> float:
    return _clamp01((bad - float(value)) / (bad - good))


def latest_strength_stimulus_sim_time(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
) -> str | None:
    """Return the newest eligible Strength stimulus time by simulated time.

    Event insertion order is intentionally ignored because event ids are not a
    guarantee of simulated-time chronology.
    """
    as_of = datetime.fromisoformat(as_of_sim_time)
    latest: datetime | None = None
    latest_raw: str | None = None
    rows = conn.execute(
        """
        SELECT sim_time,payload_json
        FROM events
        WHERE actor_id=? AND event_type='action_completed'
        """,
        (actor_id,),
    ).fetchall()
    for row in rows:
        event_time = datetime.fromisoformat(row["sim_time"])
        if event_time > as_of:
            continue
        payload = json.loads(row["payload_json"] or "{}")
        evidence = payload.get("training_stimulus")
        if not isinstance(evidence, dict) or evidence.get("domain") != "strength":
            continue
        units = evidence.get("stimulus_units")
        if not isinstance(units, (int, float)) or float(units) <= 0.0:
            continue
        if latest is None or event_time > latest:
            latest = event_time
            latest_raw = row["sim_time"]
    return latest_raw


def recovery_time_factor(
    elapsed_hours: float | int,
    *,
    minimum_hours: float = MIN_RECOVERY_HOURS,
    full_hours: float = FULL_RECOVERY_HOURS,
) -> float:
    elapsed = max(0.0, float(elapsed_hours))
    minimum = float(minimum_hours)
    full = float(full_hours)
    if minimum < 0.0 or full <= minimum:
        raise ValueError("recovery timing requires 0 <= minimum_hours < full_hours")
    if elapsed <= minimum:
        return 0.0
    if elapsed >= full:
        return 1.0
    return round((elapsed - minimum) / (full - minimum), 9)


def recovery_state_quality(state: dict[str, Any]) -> tuple[float, dict[str, float]]:
    components = {
        "energy": _higher_is_better(float(state["energy"]), good=75.0, bad=20.0),
        "alertness": _lower_is_better(float(state["sleepiness"]), good=25.0, bad=80.0),
        "fatigue_recovery": _lower_is_better(float(state["fatigue"]), good=20.0, bad=70.0),
    }
    quality = sum(components.values()) / len(components)
    return round(quality, 9), {key: round(value, 9) for key, value in components.items()}


def strength_recovery_realization_evidence(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
    recovery_multiplier: float = 1.0,
) -> StrengthRecoveryEvidence:
    multiplier = float(recovery_multiplier)
    if multiplier < 0.0:
        raise ValueError("recovery_multiplier must be non-negative")

    latest_raw = latest_strength_stimulus_sim_time(conn, actor_id, as_of_sim_time=as_of_sim_time)
    if latest_raw is None:
        return StrengthRecoveryEvidence(
            curve_id=RECOVERY_CURVE_ID,
            elapsed_hours=0.0,
            time_factor=0.0,
            state_quality=0.0,
            recovery_multiplier=round(multiplier, 6),
            recovery_factor=0.0,
            blocked=False,
            latest_stimulus_sim_time=None,
            components={},
        )

    as_of = datetime.fromisoformat(as_of_sim_time)
    latest = datetime.fromisoformat(latest_raw)
    elapsed_hours = max(0.0, (as_of - latest).total_seconds() / 3600.0)
    time_factor = recovery_time_factor(elapsed_hours)
    state_quality, components = recovery_state_quality(state)
    blocked = float(state["fatigue"]) >= FATIGUE_HARD_BLOCK
    factor = 0.0 if blocked else _clamp01(time_factor * state_quality * multiplier)

    return StrengthRecoveryEvidence(
        curve_id=RECOVERY_CURVE_ID,
        elapsed_hours=round(elapsed_hours, 6),
        time_factor=round(time_factor, 9),
        state_quality=round(state_quality, 9),
        recovery_multiplier=round(multiplier, 6),
        recovery_factor=round(factor, 9),
        blocked=blocked,
        latest_stimulus_sim_time=latest_raw,
        components=components,
    )

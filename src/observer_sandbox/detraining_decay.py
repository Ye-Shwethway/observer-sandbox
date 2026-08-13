from __future__ import annotations

import math
import sqlite3
from dataclasses import dataclass
from datetime import datetime

from .recovery_realization import latest_strength_stimulus_sim_time


DETRAINING_CURVE_ID = "strength-detraining-decay-v1"
DEFAULT_GRACE_DAYS = 14.0
DEFAULT_TIME_CONSTANT_DAYS = 60.0
DEFAULT_CEILING = 100.0


@dataclass(frozen=True)
class StrengthDetrainingEvidence:
    curve_id: str
    last_strength_stimulus_sim_time: str | None
    untrained_days: float
    grace_days: float
    overdue_days: float
    time_constant_days: float
    time_factor: float
    level_exposure: float
    detraining_multiplier: float
    decay_pressure: float
    eligible: bool


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def detraining_time_factor(
    untrained_days: float | int,
    *,
    grace_days: float = DEFAULT_GRACE_DAYS,
    time_constant_days: float = DEFAULT_TIME_CONSTANT_DAYS,
) -> tuple[float, float]:
    days = max(0.0, float(untrained_days))
    grace = float(grace_days)
    tau = float(time_constant_days)
    if grace < 0.0:
        raise ValueError("grace_days must be non-negative")
    if tau <= 0.0:
        raise ValueError("time_constant_days must be positive")
    overdue = max(0.0, days - grace)
    if overdue <= 0.0:
        return 0.0, 0.0
    return round(overdue, 9), round(1.0 - math.exp(-overdue / tau), 9)


def detraining_level_exposure(
    current_value: float | int,
    *,
    effective_ceiling: float = DEFAULT_CEILING,
    exponent: float = 2.0,
) -> float:
    current = max(0.0, float(current_value))
    ceiling = float(effective_ceiling)
    power = float(exponent)
    if ceiling <= 0.0:
        raise ValueError("effective_ceiling must be positive")
    if power <= 0.0:
        raise ValueError("exponent must be positive")
    fraction = _clamp01(current / ceiling)
    return round(fraction**power, 9)


def strength_detraining_decay_evidence(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    current_strength: float | int,
    effective_ceiling: float = DEFAULT_CEILING,
    grace_days: float = DEFAULT_GRACE_DAYS,
    time_constant_days: float = DEFAULT_TIME_CONSTANT_DAYS,
    detraining_multiplier: float = 1.0,
) -> StrengthDetrainingEvidence:
    multiplier = float(detraining_multiplier)
    if multiplier < 0.0:
        raise ValueError("detraining_multiplier must be non-negative")

    as_of = datetime.fromisoformat(as_of_sim_time)
    latest_raw = latest_strength_stimulus_sim_time(conn, actor_id, as_of_sim_time=as_of_sim_time)
    if latest_raw is None:
        # No authored Strength-training history means this proof cannot establish
        # an untrained interval. Avoid inventing a decay start point.
        return StrengthDetrainingEvidence(
            curve_id=DETRAINING_CURVE_ID,
            last_strength_stimulus_sim_time=None,
            untrained_days=0.0,
            grace_days=round(float(grace_days), 6),
            overdue_days=0.0,
            time_constant_days=round(float(time_constant_days), 6),
            time_factor=0.0,
            level_exposure=detraining_level_exposure(current_strength, effective_ceiling=effective_ceiling),
            detraining_multiplier=round(multiplier, 6),
            decay_pressure=0.0,
            eligible=False,
        )

    latest = datetime.fromisoformat(latest_raw)
    untrained_days = max(0.0, (as_of - latest).total_seconds() / 86400.0)
    overdue_days, time_factor = detraining_time_factor(
        untrained_days,
        grace_days=grace_days,
        time_constant_days=time_constant_days,
    )
    level_exposure = detraining_level_exposure(current_strength, effective_ceiling=effective_ceiling)
    pressure = _clamp01(time_factor * level_exposure * multiplier)
    eligible = overdue_days > 0.0 and pressure > 0.0
    return StrengthDetrainingEvidence(
        curve_id=DETRAINING_CURVE_ID,
        last_strength_stimulus_sim_time=latest_raw,
        untrained_days=round(untrained_days, 6),
        grace_days=round(float(grace_days), 6),
        overdue_days=round(overdue_days, 6),
        time_constant_days=round(float(time_constant_days), 6),
        time_factor=round(time_factor, 9),
        level_exposure=round(level_exposure, 9),
        detraining_multiplier=round(multiplier, 6),
        decay_pressure=round(pressure, 9),
        eligible=eligible,
    )

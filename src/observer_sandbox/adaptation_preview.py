from __future__ import annotations

import sqlite3
from dataclasses import asdict, dataclass
from typing import Any

from .adaptation_curve import strength_level_factor
from .detraining_decay import strength_detraining_decay_evidence
from .recovery_realization import strength_recovery_realization_evidence
from .stimulus_saturation import strength_stimulus_saturation_evidence


PREVIEW_ID = "strength-adaptation-preview-v1"
BASE_POSITIVE_SCALE = 0.25
BASE_DETRAINING_POINTS_PER_DAY = 0.02
DEFAULT_PREVIEW_DAYS = 1.0


@dataclass(frozen=True)
class StrengthAdaptationPreview:
    preview_id: str
    current_strength: float
    positive_delta: float
    negative_delta: float
    net_delta: float
    preview_days: float
    base_positive_scale: float
    base_detraining_points_per_day: float
    adaptation_rate_multiplier: float
    decay_rate_multiplier: float
    recent_stimulus_units: float
    level_factor: float
    saturation_factor: float
    recovery_factor: float
    decay_pressure: float
    evidence: dict[str, Any]


def strength_adaptation_preview(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    current_strength: float | int,
    state: dict[str, Any],
    natural_ceiling: float = 100.0,
    ceiling_multiplier: float = 1.0,
    recovery_multiplier: float = 1.0,
    adaptation_rate_multiplier: float = 1.0,
    detraining_multiplier: float = 1.0,
    decay_rate_multiplier: float = 1.0,
    preview_days: float = DEFAULT_PREVIEW_DAYS,
    base_positive_scale: float = BASE_POSITIVE_SCALE,
    base_detraining_points_per_day: float = BASE_DETRAINING_POINTS_PER_DAY,
) -> StrengthAdaptationPreview:
    """Compose positive and negative Strength progression evidence without mutation.

    Positive preview:
      base_positive_scale * recent_stimulus * level_factor * saturation_factor
      * recovery_factor * adaptation_rate_multiplier

    Negative preview over `preview_days`:
      base_detraining_points_per_day * decay_pressure * preview_days
      * decay_rate_multiplier

    This function never writes profile values, events, or settlement state.
    """
    current = float(current_strength)
    adaptation_multiplier = float(adaptation_rate_multiplier)
    decay_multiplier = float(decay_rate_multiplier)
    days = float(preview_days)
    positive_scale = float(base_positive_scale)
    decay_scale = float(base_detraining_points_per_day)
    if adaptation_multiplier < 0.0 or decay_multiplier < 0.0:
        raise ValueError("rate multipliers must be non-negative")
    if days <= 0.0:
        raise ValueError("preview_days must be positive")
    if positive_scale < 0.0 or decay_scale < 0.0:
        raise ValueError("base progression scales must be non-negative")

    level = strength_level_factor(
        current,
        natural_ceiling=natural_ceiling,
        ceiling_multiplier=ceiling_multiplier,
    )
    saturation = strength_stimulus_saturation_evidence(
        conn,
        actor_id,
        as_of_sim_time=as_of_sim_time,
    )
    recovery = strength_recovery_realization_evidence(
        conn,
        actor_id,
        as_of_sim_time=as_of_sim_time,
        state=state,
        recovery_multiplier=recovery_multiplier,
    )
    detraining = strength_detraining_decay_evidence(
        conn,
        actor_id,
        as_of_sim_time=as_of_sim_time,
        current_strength=current,
        effective_ceiling=level.effective_ceiling,
        detraining_multiplier=detraining_multiplier,
    )

    recent_stimulus = saturation.recent_stimulus_units
    positive = (
        positive_scale
        * recent_stimulus
        * level.level_factor
        * saturation.saturation_factor
        * recovery.recovery_factor
        * adaptation_multiplier
    )
    negative = decay_scale * detraining.decay_pressure * days * decay_multiplier
    net = positive - negative

    return StrengthAdaptationPreview(
        preview_id=PREVIEW_ID,
        current_strength=round(current, 6),
        positive_delta=round(positive, 9),
        negative_delta=round(negative, 9),
        net_delta=round(net, 9),
        preview_days=round(days, 6),
        base_positive_scale=round(positive_scale, 6),
        base_detraining_points_per_day=round(decay_scale, 6),
        adaptation_rate_multiplier=round(adaptation_multiplier, 6),
        decay_rate_multiplier=round(decay_multiplier, 6),
        recent_stimulus_units=round(recent_stimulus, 6),
        level_factor=level.level_factor,
        saturation_factor=saturation.saturation_factor,
        recovery_factor=recovery.recovery_factor,
        decay_pressure=detraining.decay_pressure,
        evidence={
            "level": asdict(level),
            "saturation": asdict(saturation),
            "recovery": asdict(recovery),
            "detraining": asdict(detraining),
        },
    )

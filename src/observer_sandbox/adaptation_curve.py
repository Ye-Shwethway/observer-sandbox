from __future__ import annotations

from dataclasses import dataclass


ADAPTATION_CURVE_ID = "strength-level-curve-v1"
DEFAULT_NATURAL_CEILING = 100.0
DEFAULT_EXPONENT = 2.0


@dataclass(frozen=True)
class AdaptationLevelEvidence:
    curve_id: str
    current_value: float
    natural_ceiling: float
    ceiling_multiplier: float
    effective_ceiling: float
    exponent: float
    remaining_fraction: float
    level_factor: float


def strength_level_factor(
    current_value: float | int,
    *,
    natural_ceiling: float = DEFAULT_NATURAL_CEILING,
    ceiling_multiplier: float = 1.0,
    exponent: float = DEFAULT_EXPONENT,
) -> AdaptationLevelEvidence:
    """Return read-only current-level difficulty evidence for Strength adaptation.

    v1 proof curve:
        level_factor = ((effective_ceiling - current) / effective_ceiling) ** exponent

    The result is bounded to 0..1. A value at or above the effective ceiling has
    no ordinary adaptation headroom. This function never mutates profile state.
    """
    current = float(current_value)
    ceiling = float(natural_ceiling)
    multiplier = float(ceiling_multiplier)
    power = float(exponent)

    if current < 0.0:
        raise ValueError("current_value must be non-negative")
    if ceiling <= 0.0:
        raise ValueError("natural_ceiling must be positive")
    if multiplier <= 0.0:
        raise ValueError("ceiling_multiplier must be positive")
    if power <= 0.0:
        raise ValueError("exponent must be positive")

    effective_ceiling = ceiling * multiplier
    remaining = max(0.0, min(1.0, (effective_ceiling - current) / effective_ceiling))
    factor = remaining**power

    return AdaptationLevelEvidence(
        curve_id=ADAPTATION_CURVE_ID,
        current_value=round(current, 6),
        natural_ceiling=round(ceiling, 6),
        ceiling_multiplier=round(multiplier, 6),
        effective_ceiling=round(effective_ceiling, 6),
        exponent=round(power, 6),
        remaining_fraction=round(remaining, 6),
        level_factor=round(factor, 9),
    )

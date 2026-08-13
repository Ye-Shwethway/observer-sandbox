from __future__ import annotations

from typing import Any


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _higher_is_better(value: float, *, good: float, bad: float) -> float:
    if good <= bad:
        raise ValueError("good threshold must be greater than bad threshold")
    return _clamp01((float(value) - bad) / (good - bad))


def _lower_is_better(value: float, *, good: float, bad: float) -> float:
    if bad <= good:
        raise ValueError("bad threshold must be greater than good threshold")
    return _clamp01((bad - float(value)) / (bad - good))


def training_readiness_modifier(state: dict[str, Any]) -> dict[str, Any]:
    """Derive the first bounded training modifier from existing live state.

    This is intentionally not a universal modifier engine. It converts four
    existing authoritative physiology/needs signals into one action-scoped
    readiness value and one fatigue-cost multiplier.
    """

    components = {
        "energy": _higher_is_better(float(state["energy"]), good=75.0, bad=20.0),
        "hydration": _lower_is_better(float(state["thirst"]), good=25.0, bad=75.0),
        "alertness": _lower_is_better(float(state["sleepiness"]), good=25.0, bad=80.0),
        "recovery": _lower_is_better(float(state["fatigue"]), good=20.0, bad=70.0),
    }
    readiness = sum(components.values()) / len(components)
    fatigue_cost_multiplier = 1.0 + (1.0 - readiness) * 0.5
    return {
        "source": "p3.3-training-readiness-v1",
        "readiness": round(readiness, 3),
        "fatigue_cost_multiplier": round(fatigue_cost_multiplier, 3),
        "components": {key: round(value, 3) for key, value in components.items()},
        "inputs": {
            "energy": round(float(state["energy"]), 3),
            "thirst": round(float(state["thirst"]), 3),
            "sleepiness": round(float(state["sleepiness"]), 3),
            "fatigue": round(float(state["fatigue"]), 3),
        },
    }

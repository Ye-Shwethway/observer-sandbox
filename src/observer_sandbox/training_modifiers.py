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
    """Derive bounded training readiness, cost, and effectiveness signals.

    This remains intentionally smaller than a universal modifier engine. Four
    existing authoritative physiology/needs signals produce one readiness
    value. Readiness then drives two distinct action-scoped outputs:

    * fatigue_cost_multiplier: how physiologically costly the session is;
    * effectiveness: how much useful training stimulus the session can deliver.

    P3.4 records effectiveness as outcome evidence only. Strength, skill,
    hypertrophy, or other adaptation state is intentionally not mutated yet.
    """

    components = {
        "energy": _higher_is_better(float(state["energy"]), good=75.0, bad=20.0),
        "hydration": _lower_is_better(float(state["thirst"]), good=25.0, bad=75.0),
        "alertness": _lower_is_better(float(state["sleepiness"]), good=25.0, bad=80.0),
        "recovery": _lower_is_better(float(state["fatigue"]), good=20.0, bad=70.0),
    }
    readiness = sum(components.values()) / len(components)
    fatigue_cost_multiplier = 1.0 + (1.0 - readiness) * 0.5
    effectiveness = readiness
    return {
        "source": "p3.4-training-readiness-effectiveness-v1",
        "readiness": round(readiness, 3),
        "effectiveness": round(effectiveness, 3),
        "fatigue_cost_multiplier": round(fatigue_cost_multiplier, 3),
        "components": {key: round(value, 3) for key, value in components.items()},
        "inputs": {
            "energy": round(float(state["energy"]), 3),
            "thirst": round(float(state["thirst"]), 3),
            "sleepiness": round(float(state["sleepiness"]), 3),
            "fatigue": round(float(state["fatigue"]), 3),
        },
    }

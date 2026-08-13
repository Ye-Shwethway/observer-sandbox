from __future__ import annotations

from typing import Any


FREE_WEIGHTS_TARGET = "obj_thorne_estate_gym_free_weights"
STRENGTH_STIMULUS_DOMAIN = "strength"
STRENGTH_STIMULUS_SOURCE = "minimum-training-stimulus-v1"


def training_stimulus_evidence(*, action_name: str, target: str | None, training_load: dict[str, Any] | None) -> dict[str, Any] | None:
    """Derive session-only strength stimulus evidence for the v1 exemplar.

    This is deliberately not progression state. It consumes the already-derived
    effective training load and emits deterministic evidence only for Free Weights.
    """
    if action_name != "train" or target != FREE_WEIGHTS_TARGET or not isinstance(training_load, dict):
        return None
    effective_minutes = max(0.0, float(training_load.get("effective_minutes", 0.0)))
    stimulus_units = round(effective_minutes / 60.0, 3)
    return {
        "domain": STRENGTH_STIMULUS_DOMAIN,
        "target": FREE_WEIGHTS_TARGET,
        "effective_minutes": round(effective_minutes, 3),
        "stimulus_units": stimulus_units,
        "unit": "session_strength_stimulus",
        "source": STRENGTH_STIMULUS_SOURCE,
    }

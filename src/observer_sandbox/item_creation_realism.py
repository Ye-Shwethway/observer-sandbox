from __future__ import annotations

import re
from typing import Any, Mapping

from .physical_quantity import PhysicalQuantityError, normalize_physical_quantity


DEFAULT_ITEM_REALISM_INSTRUCTION = (
    "REALISM INVARIANT: unless the target universe explicitly declares different physical laws, "
    "all generated physical facts must obey ordinary real-world physics, geometry, scale and mutual consistency. "
    "Treat dimensions as the external bounding dimensions of the Item. Container internal capacity must fit inside "
    "that external envelope and therefore must never exceed the outer bounding volume. Keep mass, dimensions, capacity, "
    "nutrition and other numeric facts mutually plausible for the described object. Do not invent false precision: when "
    "a numeric fact cannot be conservatively supported, use null for the nullable slot instead of guessing. "
    "Numeric immersion depth requires explicit waterproof/submersible/immersion evidence; generic water-resistant wording "
    "does not justify a depth rating. When power, runtime and stored energy are all represented, reject grossly impossible "
    "energy budgets instead of treating the metrics as independent guesses. "
)


class ItemRealismError(ValueError):
    pass


def _quantity_base(raw: Any, *, kind: str, label: str) -> float | None:
    if raw is None:
        return None
    if not isinstance(raw, Mapping) or set(raw) != {"value", "unit"}:
        raise ItemRealismError(f"{label} must be a physical quantity object")
    try:
        return float(normalize_physical_quantity(kind, raw["value"], str(raw["unit"])).base_value)
    except (PhysicalQuantityError, TypeError, ValueError) as exc:
        raise ItemRealismError(f"{label} could not be normalized: {exc}") from exc


def _metric_value(metrics: Mapping[str, Any], key: str, *, expected_unit: str) -> float | None:
    raw = metrics.get(key)
    if raw is None:
        return None
    if not isinstance(raw, Mapping) or set(raw) != {"value", "unit"}:
        raise ItemRealismError(f"modules.metrics.{key} must contain exactly value and unit")
    if str(raw.get("unit")) != expected_unit:
        raise ItemRealismError(
            f"modules.metrics.{key}.unit must be canonical unit {expected_unit!r} before realism validation"
        )
    value = raw.get("value")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ItemRealismError(f"modules.metrics.{key}.value must be numeric")
    return float(value)


def _text_evidence(definition: Mapping[str, Any]) -> str:
    parts = [str(definition.get("name") or ""), str(definition.get("description") or "")]
    tags = definition.get("tags")
    if isinstance(tags, list):
        parts.extend(str(value) for value in tags)
    return " ".join(parts).lower().replace("_", " ")


def _has_explicit_immersion_evidence(definition: Mapping[str, Any]) -> bool:
    text = _text_evidence(definition)
    evidence_patterns = (
        r"\bwaterproof\b",
        r"\bsubmersible\b",
        r"\bsubmersion\b",
        r"\bimmersion\b",
        r"\bdive\b",
        r"\bdiving\b",
        r"\bipx[7-9]\b",
        r"\bip6[7-9]\b",
    )
    return any(re.search(pattern, text) for pattern in evidence_patterns)


def _validate_metric_coherence(definition: Mapping[str, Any], modules: Mapping[str, Any]) -> None:
    metrics = modules.get("metrics")
    if not isinstance(metrics, Mapping):
        return

    depth = _metric_value(metrics, "water_resistance_depth", expected_unit="m")
    if depth is not None and not _has_explicit_immersion_evidence(definition):
        raise ItemRealismError(
            "water_resistance_depth requires explicit waterproof/submersible/immersion evidence; "
            "generic water-resistant or outdoor wording does not justify a numeric immersion depth"
        )

    power_w = _metric_value(metrics, "power", expected_unit="W")
    runtime_h = _metric_value(metrics, "runtime", expected_unit="h")
    energy_wh = _metric_value(metrics, "energy_capacity", expected_unit="Wh")
    if power_w is not None and runtime_h is not None and energy_wh is not None:
        nominal_need_wh = power_w * runtime_h
        # `power` may be rated/peak rather than average draw. Only reject a
        # large contradiction: represented energy below 25% of the simple
        # rated-power x runtime budget is not a conservative ordinary-world fit.
        if energy_wh + 1e-9 < nominal_need_wh * 0.25:
            raise ItemRealismError(
                "power, runtime and energy_capacity are grossly inconsistent "
                f"({power_w:g} W × {runtime_h:g} h implies about {nominal_need_wh:g} Wh, "
                f"but represented energy capacity is only {energy_wh:g} Wh); "
                "correct the conflicting metrics or leave unsupported metrics null"
            )


def validate_item_default_realism(payload: Mapping[str, Any]) -> None:
    """Reject clear physical impossibilities for the default Creation Sandbox.

    This intentionally implements objective/conservative cross-field checks. It
    is not a general realism oracle and does not infer missing facts. Future
    universes may replace/extend this policy when their physical-law contract
    differs.
    """

    if not isinstance(payload, Mapping):
        raise ItemRealismError("Item payload must be an object")
    definition = payload.get("definition")
    if not isinstance(definition, Mapping):
        return
    modules = definition.get("modules")
    if not isinstance(modules, Mapping):
        return

    _validate_metric_coherence(definition, modules)

    physical = modules.get("physical")
    container = modules.get("container")
    if not isinstance(physical, Mapping) or not isinstance(container, Mapping):
        return

    length = _quantity_base(physical.get("length"), kind="length", label="modules.physical.length")
    width = _quantity_base(physical.get("width"), kind="length", label="modules.physical.width")
    height = _quantity_base(physical.get("height"), kind="length", label="modules.physical.height")
    capacity = _quantity_base(container.get("capacity_volume"), kind="volume", label="modules.container.capacity_volume")
    if None in (length, width, height, capacity):
        return

    outer_volume_m3 = float(length) * float(width) * float(height)
    if float(capacity) > outer_volume_m3 * (1.0 + 1e-9):
        raise ItemRealismError(
            "container capacity exceeds the Item's outer bounding volume "
            f"({float(capacity) * 1000:g} L > {outer_volume_m3 * 1000:g} L); "
            "dimensions and capacity are physically inconsistent"
        )


__all__ = [
    "DEFAULT_ITEM_REALISM_INSTRUCTION",
    "ItemRealismError",
    "validate_item_default_realism",
]

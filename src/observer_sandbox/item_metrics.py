from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Any, Mapping


_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


class ItemMetricError(ValueError):
    pass


@dataclass(frozen=True)
class ItemMetricSpec:
    metric_id: str
    label: str
    canonical_unit: str
    unit_factors: Mapping[str, float]
    minimum: float = 0.0
    positive: bool = False
    ai_inferable: bool = True


def _stable_id(value: str, *, label: str) -> str:
    normalized = str(value or "").strip().lower()
    if not _ID_RE.fullmatch(normalized):
        raise ItemMetricError(f"{label} must be a stable lowercase id")
    return normalized


class ItemMetricRegistry:
    def __init__(self) -> None:
        self._specs: dict[str, ItemMetricSpec] = {}

    def register(self, spec: ItemMetricSpec) -> None:
        metric_id = _stable_id(spec.metric_id, label="metric_id")
        if metric_id in self._specs:
            raise ItemMetricError(f"Item metric already registered: {metric_id}")
        canonical_unit = str(spec.canonical_unit or "").strip()
        if not canonical_unit:
            raise ItemMetricError("canonical_unit must be non-empty")
        factors: dict[str, float] = {}
        for raw_unit, raw_factor in dict(spec.unit_factors).items():
            unit = str(raw_unit or "").strip()
            if not unit:
                raise ItemMetricError(f"{metric_id} has an empty unit")
            factor = float(raw_factor)
            if not math.isfinite(factor) or factor <= 0:
                raise ItemMetricError(f"{metric_id} unit factor for {unit!r} must be finite and positive")
            factors[unit] = factor
        if canonical_unit not in factors:
            raise ItemMetricError(f"{metric_id} canonical unit must be present in unit_factors")
        if not math.isclose(factors[canonical_unit], 1.0, rel_tol=0.0, abs_tol=1e-12):
            raise ItemMetricError(f"{metric_id} canonical unit factor must equal 1")
        minimum = float(spec.minimum)
        if not math.isfinite(minimum):
            raise ItemMetricError(f"{metric_id} minimum must be finite")
        self._specs[metric_id] = ItemMetricSpec(
            metric_id=metric_id,
            label=str(spec.label or "").strip() or metric_id.replace("_", " ").title(),
            canonical_unit=canonical_unit,
            unit_factors=factors,
            minimum=minimum,
            positive=bool(spec.positive),
            ai_inferable=bool(spec.ai_inferable),
        )

    def spec(self, metric_id: str) -> ItemMetricSpec:
        key = _stable_id(metric_id, label="metric_id")
        try:
            return self._specs[key]
        except KeyError as exc:
            raise ItemMetricError(f"Unknown Item metric: {key}") from exc

    def metric_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._specs))

    def normalize(self, metric_id: str, raw: Any) -> dict[str, Any]:
        spec = self.spec(metric_id)
        if not isinstance(raw, Mapping):
            raise ItemMetricError(f"metrics.{spec.metric_id} must be an object")
        keys = set(raw)
        if keys != {"value", "unit"}:
            missing = {"value", "unit"} - keys
            unknown = keys - {"value", "unit"}
            if missing:
                raise ItemMetricError(
                    f"metrics.{spec.metric_id} missing required field(s): {sorted(missing)}"
                )
            raise ItemMetricError(
                f"metrics.{spec.metric_id} has unknown field(s): {sorted(unknown)}"
            )
        value = raw["value"]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ItemMetricError(f"metrics.{spec.metric_id}.value must be numeric")
        numeric = float(value)
        if not math.isfinite(numeric):
            raise ItemMetricError(f"metrics.{spec.metric_id}.value must be finite")
        if spec.positive:
            if numeric <= spec.minimum:
                raise ItemMetricError(
                    f"metrics.{spec.metric_id}.value must be greater than {spec.minimum:g}"
                )
        elif numeric < spec.minimum:
            raise ItemMetricError(
                f"metrics.{spec.metric_id}.value must be at least {spec.minimum:g}"
            )
        unit = str(raw["unit"] or "").strip()
        try:
            factor = spec.unit_factors[unit]
        except KeyError as exc:
            raise ItemMetricError(
                f"metrics.{spec.metric_id}.unit must be one of {sorted(spec.unit_factors)}"
            ) from exc
        canonical_value = numeric * factor
        if not math.isfinite(canonical_value):
            raise ItemMetricError(f"metrics.{spec.metric_id} normalized value must be finite")
        return {"value": canonical_value, "unit": spec.canonical_unit}

    def ai_schema_properties(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for metric_id in self.metric_ids():
            spec = self._specs[metric_id]
            result[metric_id] = {
                "anyOf": [
                    {
                        "type": "object",
                        "properties": {
                            "value": {"type": "number", "minimum": spec.minimum},
                            "unit": {"type": "string", "enum": sorted(spec.unit_factors)},
                        },
                        "required": ["value", "unit"],
                        "additionalProperties": False,
                    },
                    {"type": "null"},
                ]
            }
        return result


def build_default_item_metric_registry() -> ItemMetricRegistry:
    registry = ItemMetricRegistry()
    registry.register(ItemMetricSpec("luminous_flux", "Luminous Flux", "lm", {"lm": 1.0, "klm": 1000.0}, positive=True))
    registry.register(ItemMetricSpec("runtime", "Runtime", "h", {"h": 1.0, "min": 1.0 / 60.0, "s": 1.0 / 3600.0}, positive=True))
    registry.register(ItemMetricSpec("power", "Power", "W", {"W": 1.0, "kW": 1000.0, "mW": 0.001}, positive=True))
    registry.register(ItemMetricSpec("energy_capacity", "Energy Capacity", "Wh", {"Wh": 1.0, "kWh": 1000.0, "mWh": 0.001}, positive=True))
    registry.register(ItemMetricSpec("range", "Range", "m", {"m": 1.0, "km": 1000.0, "ft": 0.3048, "mi": 1609.344}, positive=True))
    registry.register(ItemMetricSpec("speed", "Speed", "m/s", {"m/s": 1.0, "km/h": 1.0 / 3.6, "mph": 0.44704}, positive=True))
    registry.register(ItemMetricSpec("data_rate", "Data Rate", "Mbps", {"kbps": 0.001, "Mbps": 1.0, "Gbps": 1000.0}, positive=True))
    registry.register(ItemMetricSpec("digital_storage", "Digital Storage", "GB", {"MB": 0.001, "GB": 1.0, "TB": 1000.0}, positive=True))
    registry.register(ItemMetricSpec("beam_distance", "Beam Distance", "m", {"m": 1.0, "km": 1000.0, "ft": 0.3048}, positive=True))
    registry.register(ItemMetricSpec("water_resistance_depth", "Water Resistance Depth", "m", {"m": 1.0, "cm": 0.01, "ft": 0.3048}, positive=True))
    registry.register(ItemMetricSpec("charge_time", "Charge Time", "h", {"h": 1.0, "min": 1.0 / 60.0}, positive=True))
    registry.register(ItemMetricSpec("payload_capacity", "Payload Capacity", "kg", {"kg": 1.0, "g": 0.001, "lb": 0.45359237, "oz": 0.028349523125}, positive=True))
    return registry


DEFAULT_ITEM_METRIC_REGISTRY = build_default_item_metric_registry()


def normalize_item_metrics(
    raw: Any,
    *,
    registry: ItemMetricRegistry = DEFAULT_ITEM_METRIC_REGISTRY,
) -> dict[str, dict[str, Any]]:
    if not isinstance(raw, Mapping):
        raise ItemMetricError("modules.metrics must be an object")
    unknown = set(raw) - set(registry.metric_ids())
    if unknown:
        raise ItemMetricError(f"modules.metrics contains unregistered metric(s): {sorted(unknown)}")
    if not raw:
        raise ItemMetricError("modules.metrics must contain at least one represented metric")
    return {metric_id: registry.normalize(metric_id, raw[metric_id]) for metric_id in sorted(raw)}


__all__ = [
    "DEFAULT_ITEM_METRIC_REGISTRY",
    "ItemMetricError",
    "ItemMetricRegistry",
    "ItemMetricSpec",
    "build_default_item_metric_registry",
    "normalize_item_metrics",
]

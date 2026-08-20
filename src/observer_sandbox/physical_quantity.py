from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final


class PhysicalQuantityError(ValueError):
    pass


QUANTITY_KINDS: Final[frozenset[str]] = frozenset({"mass", "length", "area", "volume"})
DISPLAY_SYSTEMS: Final[frozenset[str]] = frozenset({"imperial", "metric"})

_BASE_UNITS: Final[dict[str, str]] = {
    "mass": "kg",
    "length": "m",
    "area": "m2",
    "volume": "m3",
}

# Multipliers convert one source unit into the canonical SI base unit for its kind.
_UNIT_TO_BASE: Final[dict[str, tuple[str, float]]] = {
    # mass
    "kg": ("mass", 1.0),
    "g": ("mass", 0.001),
    "lb": ("mass", 0.45359237),
    "oz": ("mass", 0.028349523125),
    # length
    "m": ("length", 1.0),
    "cm": ("length", 0.01),
    "mm": ("length", 0.001),
    "in": ("length", 0.0254),
    "ft": ("length", 0.3048),
    "yd": ("length", 0.9144),
    # area
    "m2": ("area", 1.0),
    "cm2": ("area", 0.0001),
    "in2": ("area", 0.00064516),
    "ft2": ("area", 0.09290304),
    "yd2": ("area", 0.83612736),
    # volume/capacity
    "m3": ("volume", 1.0),
    "l": ("volume", 0.001),
    "ml": ("volume", 0.000001),
    "in3": ("volume", 0.000016387064),
    "ft3": ("volume", 0.028316846592),
    "floz_us": ("volume", 0.0000295735295625),
    "cup_us": ("volume", 0.0002365882365),
    "pt_us": ("volume", 0.000473176473),
    "qt_us": ("volume", 0.000946352946),
    "gal_us": ("volume", 0.003785411784),
}

_DEFAULT_DISPLAY_UNITS: Final[dict[str, dict[str, str]]] = {
    "imperial": {
        "mass": "lb",
        "length": "in",
        "area": "ft2",
        "volume": "gal_us",
    },
    "metric": {
        "mass": "kg",
        "length": "m",
        "area": "m2",
        "volume": "l",
    },
}

_UNIT_LABELS: Final[dict[str, str]] = {
    "kg": "kg",
    "g": "g",
    "lb": "lb",
    "oz": "oz",
    "m": "m",
    "cm": "cm",
    "mm": "mm",
    "in": "in",
    "ft": "ft",
    "yd": "yd",
    "m2": "m²",
    "cm2": "cm²",
    "in2": "in²",
    "ft2": "ft²",
    "yd2": "yd²",
    "m3": "m³",
    "l": "L",
    "ml": "mL",
    "in3": "in³",
    "ft3": "ft³",
    "floz_us": "US fl oz",
    "cup_us": "US cup",
    "pt_us": "US pt",
    "qt_us": "US qt",
    "gal_us": "US gal",
}


@dataclass(frozen=True)
class PhysicalQuantity:
    """Presentation-independent physical quantity normalized to an SI base unit."""

    kind: str
    base_value: float

    def __post_init__(self) -> None:
        if self.kind not in QUANTITY_KINDS:
            raise PhysicalQuantityError(f"Unsupported physical quantity kind: {self.kind!r}")
        if isinstance(self.base_value, bool) or not isinstance(self.base_value, (int, float)):
            raise PhysicalQuantityError("Physical quantity value must be numeric")
        value = float(self.base_value)
        if not math.isfinite(value):
            raise PhysicalQuantityError("Physical quantity value must be finite")
        if value < 0.0:
            raise PhysicalQuantityError("Physical quantity value cannot be negative")
        object.__setattr__(self, "base_value", value)

    @property
    def base_unit(self) -> str:
        return _BASE_UNITS[self.kind]

    def as_dict(self) -> dict[str, object]:
        return {
            "kind": self.kind,
            "value": self.base_value,
            "unit": self.base_unit,
        }


def _unit_definition(unit: str) -> tuple[str, float]:
    key = str(unit or "").strip().lower()
    try:
        return _UNIT_TO_BASE[key]
    except KeyError as exc:
        raise PhysicalQuantityError(f"Unsupported physical unit: {unit!r}") from exc


def normalize_physical_quantity(kind: str, value: float | int, unit: str) -> PhysicalQuantity:
    normalized_kind = str(kind or "").strip().lower()
    if normalized_kind not in QUANTITY_KINDS:
        raise PhysicalQuantityError(f"Unsupported physical quantity kind: {kind!r}")
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise PhysicalQuantityError("Physical quantity value must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise PhysicalQuantityError("Physical quantity value must be finite")
    if numeric < 0.0:
        raise PhysicalQuantityError("Physical quantity value cannot be negative")

    unit_kind, multiplier = _unit_definition(unit)
    if unit_kind != normalized_kind:
        raise PhysicalQuantityError(
            f"Unit {unit!r} represents {unit_kind}, not {normalized_kind}"
        )
    return PhysicalQuantity(normalized_kind, numeric * multiplier)


def convert_physical_quantity(quantity: PhysicalQuantity, unit: str) -> float:
    unit_kind, multiplier = _unit_definition(unit)
    if unit_kind != quantity.kind:
        raise PhysicalQuantityError(
            f"Unit {unit!r} represents {unit_kind}, not {quantity.kind}"
        )
    return quantity.base_value / multiplier


def default_display_unit(kind: str, system: str = "imperial") -> str:
    normalized_kind = str(kind or "").strip().lower()
    normalized_system = str(system or "").strip().lower()
    if normalized_kind not in QUANTITY_KINDS:
        raise PhysicalQuantityError(f"Unsupported physical quantity kind: {kind!r}")
    if normalized_system not in DISPLAY_SYSTEMS:
        raise PhysicalQuantityError(f"Unsupported display system: {system!r}")
    return _DEFAULT_DISPLAY_UNITS[normalized_system][normalized_kind]


def display_physical_quantity(
    quantity: PhysicalQuantity,
    *,
    system: str = "imperial",
    unit: str | None = None,
    precision: int = 2,
) -> dict[str, object]:
    if not isinstance(precision, int) or isinstance(precision, bool) or precision < 0 or precision > 12:
        raise PhysicalQuantityError("Display precision must be an integer in 0..12")
    target_unit = unit or default_display_unit(quantity.kind, system)
    value = convert_physical_quantity(quantity, target_unit)
    return {
        "kind": quantity.kind,
        "value": round(value, precision),
        "unit": target_unit,
        "label": _UNIT_LABELS[target_unit],
        "system": str(system or "").strip().lower(),
    }


def format_physical_quantity(
    quantity: PhysicalQuantity,
    *,
    system: str = "imperial",
    unit: str | None = None,
    precision: int = 2,
) -> str:
    display = display_physical_quantity(
        quantity,
        system=system,
        unit=unit,
        precision=precision,
    )
    value = float(display["value"])
    rendered = f"{value:.{precision}f}".rstrip("0").rstrip(".") if precision else f"{value:.0f}"
    return f"{rendered} {display['label']}"


__all__ = [
    "DISPLAY_SYSTEMS",
    "PhysicalQuantity",
    "PhysicalQuantityError",
    "QUANTITY_KINDS",
    "convert_physical_quantity",
    "default_display_unit",
    "display_physical_quantity",
    "format_physical_quantity",
    "normalize_physical_quantity",
]

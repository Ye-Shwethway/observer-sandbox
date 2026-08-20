from __future__ import annotations

import math

import pytest

from observer_sandbox.physical_quantity import (
    PhysicalQuantity,
    PhysicalQuantityError,
    convert_physical_quantity,
    default_display_unit,
    display_physical_quantity,
    format_physical_quantity,
    normalize_physical_quantity,
)


def test_equivalent_mass_units_normalize_to_same_physical_truth() -> None:
    pounds = normalize_physical_quantity("mass", 55, "lb")
    kilograms = normalize_physical_quantity("mass", 24.94758035, "kg")

    assert pounds.kind == "mass"
    assert pounds.base_unit == "kg"
    assert math.isclose(pounds.base_value, kilograms.base_value, rel_tol=0.0, abs_tol=1e-12)


def test_equivalent_length_area_and_volume_units_normalize_identically() -> None:
    assert math.isclose(
        normalize_physical_quantity("length", 12, "in").base_value,
        normalize_physical_quantity("length", 0.3048, "m").base_value,
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    assert math.isclose(
        normalize_physical_quantity("area", 1, "ft2").base_value,
        normalize_physical_quantity("area", 0.09290304, "m2").base_value,
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    assert math.isclose(
        normalize_physical_quantity("volume", 1, "gal_us").base_value,
        normalize_physical_quantity("volume", 3.785411784, "l").base_value,
        rel_tol=0.0,
        abs_tol=1e-12,
    )


def test_imperial_is_default_creator_facing_presentation() -> None:
    mass = normalize_physical_quantity("mass", 25, "kg")
    length = normalize_physical_quantity("length", 1, "m")
    area = normalize_physical_quantity("area", 1, "m2")
    volume = normalize_physical_quantity("volume", 1, "l")

    assert default_display_unit("mass") == "lb"
    assert default_display_unit("length") == "in"
    assert default_display_unit("area") == "ft2"
    assert default_display_unit("volume") == "gal_us"

    assert display_physical_quantity(mass)["unit"] == "lb"
    assert display_physical_quantity(length)["unit"] == "in"
    assert display_physical_quantity(area)["unit"] == "ft2"
    assert display_physical_quantity(volume)["unit"] == "gal_us"


def test_metric_and_imperial_presentation_do_not_mutate_authoritative_quantity() -> None:
    quantity = normalize_physical_quantity("mass", 55, "lb")
    before = quantity.as_dict()

    imperial = display_physical_quantity(quantity, system="imperial", precision=4)
    metric = display_physical_quantity(quantity, system="metric", precision=4)

    assert imperial == {
        "kind": "mass",
        "value": 55.0,
        "unit": "lb",
        "label": "lb",
        "system": "imperial",
    }
    assert metric == {
        "kind": "mass",
        "value": 24.9476,
        "unit": "kg",
        "label": "kg",
        "system": "metric",
    }
    assert quantity.as_dict() == before


def test_round_trip_conversion_stays_within_precision_tolerance() -> None:
    original = normalize_physical_quantity("volume", 2.75, "gal_us")
    liters = convert_physical_quantity(original, "l")
    round_trip = normalize_physical_quantity("volume", liters, "l")

    assert math.isclose(original.base_value, round_trip.base_value, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(convert_physical_quantity(round_trip, "gal_us"), 2.75, rel_tol=0.0, abs_tol=1e-12)


def test_serialized_authority_is_normalized_not_formatted_text() -> None:
    quantity = normalize_physical_quantity("mass", 55, "lb")

    assert quantity.as_dict() == {
        "kind": "mass",
        "value": pytest.approx(24.94758035),
        "unit": "kg",
    }
    assert format_physical_quantity(quantity, precision=0) == "55 lb"


def test_unit_kind_mismatch_fails_closed() -> None:
    with pytest.raises(PhysicalQuantityError, match="represents length, not mass"):
        normalize_physical_quantity("mass", 10, "ft")

    quantity = normalize_physical_quantity("length", 2, "ft")
    with pytest.raises(PhysicalQuantityError, match="represents mass, not length"):
        convert_physical_quantity(quantity, "lb")


def test_invalid_values_and_units_fail_closed() -> None:
    with pytest.raises(PhysicalQuantityError, match="cannot be negative"):
        normalize_physical_quantity("mass", -1, "lb")
    with pytest.raises(PhysicalQuantityError, match="must be finite"):
        normalize_physical_quantity("length", float("inf"), "m")
    with pytest.raises(PhysicalQuantityError, match="must be numeric"):
        normalize_physical_quantity("mass", True, "kg")
    with pytest.raises(PhysicalQuantityError, match="Unsupported physical unit"):
        normalize_physical_quantity("volume", 1, "barrel")


def test_direct_physical_quantity_constructor_enforces_same_invariants() -> None:
    assert PhysicalQuantity("mass", 0).base_value == 0.0
    with pytest.raises(PhysicalQuantityError, match="Unsupported physical quantity kind"):
        PhysicalQuantity("temperature", 20)
    with pytest.raises(PhysicalQuantityError, match="cannot be negative"):
        PhysicalQuantity("length", -0.01)

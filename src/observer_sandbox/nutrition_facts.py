from __future__ import annotations

from typing import Any

from .inventory import item_definition, load_item_catalog


MACRO_KEYS = ("energy_kcal", "protein_g", "carbohydrate_g", "fat_g")


def nutrition_facts_for_definition(
    definition_id: str,
    quantity: float | None = None,
) -> dict[str, Any] | None:
    """Return deterministic nutrition facts for a universal item definition.

    Nutrition semantics belong to the reusable item definition, not to a named
    character, location, or inventory stack. When quantity is omitted, the
    definition's authored default portion is used; if absent, the nutrition basis
    quantity is used.
    """
    definition = item_definition(definition_id)
    nutrition = definition.get("nutrition")
    if not isinstance(nutrition, dict):
        return None

    basis_quantity = float(nutrition.get("basis_quantity", 0.0))
    unit = str(nutrition.get("unit") or "").strip()
    if basis_quantity <= 0.0 or not unit:
        raise ValueError(f"Invalid nutrition basis for {definition_id}")

    properties = definition.get("properties", {})
    default_portion = float(properties.get("default_portion_quantity", basis_quantity))
    requested_quantity = default_portion if quantity is None else float(quantity)
    if requested_quantity <= 0.0:
        raise ValueError("Nutrition quantity must be positive")

    canonical_unit = str(properties.get("canonical_unit", unit))
    if canonical_unit != unit:
        raise ValueError(
            f"Nutrition unit {unit} does not match canonical unit {canonical_unit} for {definition_id}"
        )

    factor = requested_quantity / basis_quantity
    catalog = load_item_catalog()
    return {
        "definition_id": definition_id,
        "name": str(definition.get("name", definition_id)),
        "quantity": round(requested_quantity, 6),
        "unit": unit,
        "basis_quantity": round(basis_quantity, 6),
        "default_portion_quantity": round(default_portion, 6),
        "energy_kcal": round(float(nutrition.get("energy_kcal", 0.0)) * factor, 3),
        "protein_g": round(float(nutrition.get("protein_g", 0.0)) * factor, 3),
        "carbohydrate_g": round(float(nutrition.get("carbohydrate_g", 0.0)) * factor, 3),
        "fat_g": round(float(nutrition.get("fat_g", 0.0)) * factor, 3),
        "source_revision": str(catalog.get("revision", "universal-items-v1")),
    }

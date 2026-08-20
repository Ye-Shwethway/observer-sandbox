from __future__ import annotations

import math
import re
from copy import deepcopy
from typing import Any, Mapping

from .economic_value import VALID_CLASSIFICATIONS, VALID_NET_WORTH_TREATMENTS
from .grading import GradeResult, evaluate_item_resistance_load
from .physical_quantity import (
    PhysicalQuantity,
    PhysicalQuantityError,
    normalize_physical_quantity,
)
from .requirements import RequirementContext, RequirementContractError, evaluate_requirements


ITEM_SCHEMA_VERSION = "item-v1"
ITEM_KINDS = frozenset({"object", "fixture", "equipment", "consumable", "container"})
ITEM_MOBILITY = frozenset({"movable", "fixed"})
ITEM_MODULES = frozenset({"physical", "stack", "nutrition", "container", "resistance_training"})
ITEM_CAPABILITIES = frozenset({"inspect", "eat", "store", "train", "use", "equip", "wear"})
ITEM_RELATION_TYPES = frozenset({"located_at", "stored_in", "owned_by", "carried_by", "equipped_by"})

_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


class ItemSchemaError(ValueError):
    pass


def _exact(mapping: Mapping[str, Any], required: set[str], *, label: str) -> None:
    if not isinstance(mapping, Mapping):
        raise ItemSchemaError(f"{label} must be an object")
    keys = set(mapping)
    missing = required - keys
    unknown = keys - required
    if missing:
        raise ItemSchemaError(f"{label} missing required field(s): {sorted(missing)}")
    if unknown:
        raise ItemSchemaError(f"{label} has unknown field(s): {sorted(unknown)}")


def _nonempty_string(value: Any, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ItemSchemaError(f"{label} must be a non-empty string")
    return value.strip()


def _token(value: Any, *, label: str) -> str:
    token = _nonempty_string(value, label=label).lower()
    if not _KEY_RE.fullmatch(token):
        raise ItemSchemaError(f"{label} must be a stable lowercase token")
    return token


def _number(value: Any, *, label: str, minimum: float = 0.0, positive: bool = False) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ItemSchemaError(f"{label} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric):
        raise ItemSchemaError(f"{label} must be finite")
    if positive and numeric <= minimum:
        raise ItemSchemaError(f"{label} must be greater than {minimum}")
    if not positive and numeric < minimum:
        raise ItemSchemaError(f"{label} must be at least {minimum}")
    return numeric


def _string_list(value: Any, *, label: str, tokenized: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise ItemSchemaError(f"{label} must be a list")
    result: list[str] = []
    for index, raw in enumerate(value):
        item = _token(raw, label=f"{label}[{index}]") if tokenized else _nonempty_string(raw, label=f"{label}[{index}]")
        if item in result:
            raise ItemSchemaError(f"{label} contains duplicate value: {item}")
        result.append(item)
    return result


def _quantity(raw: Any, *, kind: str, label: str, positive: bool = False) -> PhysicalQuantity:
    if not isinstance(raw, Mapping):
        raise ItemSchemaError(f"{label} must be a physical quantity object")
    _exact(raw, {"value", "unit"}, label=label)
    try:
        quantity = normalize_physical_quantity(kind, raw["value"], str(raw["unit"]))
    except PhysicalQuantityError as exc:
        raise ItemSchemaError(f"{label}: {exc}") from exc
    if positive and quantity.base_value <= 0.0:
        raise ItemSchemaError(f"{label} must be greater than zero")
    return quantity


def _quantity_payload(quantity: PhysicalQuantity) -> dict[str, Any]:
    return quantity.as_dict()


def _validate_physical_module(raw: Any) -> tuple[dict[str, Any], dict[str, PhysicalQuantity]]:
    if not isinstance(raw, Mapping):
        raise ItemSchemaError("modules.physical must be an object")
    _exact(raw, {"mass", "length", "width", "height"}, label="modules.physical")
    quantities: dict[str, PhysicalQuantity] = {}
    normalized: dict[str, Any] = {}
    for field, kind in (("mass", "mass"), ("length", "length"), ("width", "length"), ("height", "length")):
        value = raw[field]
        if value is None:
            normalized[field] = None
            continue
        quantity = _quantity(value, kind=kind, label=f"modules.physical.{field}", positive=True)
        quantities[field] = quantity
        normalized[field] = _quantity_payload(quantity)
    if not quantities:
        raise ItemSchemaError("modules.physical must represent at least one known physical quantity")
    return normalized, quantities


def _validate_stack_module(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ItemSchemaError("modules.stack must be an object")
    _exact(raw, {"canonical_unit", "initial_quantity"}, label="modules.stack")
    unit = _token(raw["canonical_unit"], label="modules.stack.canonical_unit")
    quantity = _number(raw["initial_quantity"], label="modules.stack.initial_quantity", positive=True)
    return {"canonical_unit": unit, "initial_quantity": quantity}


def _validate_nutrition_module(raw: Any, *, stack_unit: str | None) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ItemSchemaError("modules.nutrition must be an object")
    required = {"basis_quantity", "unit", "energy_kcal", "protein_g", "carbohydrate_g", "fat_g"}
    _exact(raw, required, label="modules.nutrition")
    unit = _token(raw["unit"], label="modules.nutrition.unit")
    if stack_unit is not None and unit != stack_unit:
        raise ItemSchemaError("modules.nutrition.unit must match modules.stack.canonical_unit")
    return {
        "basis_quantity": _number(raw["basis_quantity"], label="modules.nutrition.basis_quantity", positive=True),
        "unit": unit,
        "energy_kcal": _number(raw["energy_kcal"], label="modules.nutrition.energy_kcal"),
        "protein_g": _number(raw["protein_g"], label="modules.nutrition.protein_g"),
        "carbohydrate_g": _number(raw["carbohydrate_g"], label="modules.nutrition.carbohydrate_g"),
        "fat_g": _number(raw["fat_g"], label="modules.nutrition.fat_g"),
    }


def _validate_container_module(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ItemSchemaError("modules.container must be an object")
    _exact(raw, {"capacity_volume"}, label="modules.container")
    capacity = _quantity(raw["capacity_volume"], kind="volume", label="modules.container.capacity_volume", positive=True)
    return {"capacity_volume": _quantity_payload(capacity)}


def _validate_resistance_module(raw: Any) -> tuple[dict[str, Any], GradeResult]:
    if not isinstance(raw, Mapping):
        raise ItemSchemaError("modules.resistance_training must be an object")
    _exact(raw, {"resistance_load"}, label="modules.resistance_training")
    load = _quantity(raw["resistance_load"], kind="mass", label="modules.resistance_training.resistance_load", positive=True)
    grade = evaluate_item_resistance_load(load)
    return {"resistance_load": _quantity_payload(load)}, grade


def _validate_requirements(raw: Any) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ItemSchemaError("requirements must be an object")
    _exact(raw, {"use"}, label="requirements")
    use = raw["use"]
    if use is None:
        return {"use": None}
    try:
        # Empty evidence intentionally fails requirement predicates while still
        # exercising the exact typed contract shape. The result is discarded;
        # this validation must never infer that an unmet requirement is invalid.
        evaluate_requirements(
            use,
            RequirementContext(grades={}, values={}, states={}),
        )
    except RequirementContractError as exc:
        raise ItemSchemaError(f"requirements.use: {exc}") from exc
    return {"use": deepcopy(use)}


def _validate_economic_policy(raw: Any, *, stackable: bool, stack_unit: str | None) -> dict[str, Any]:
    if not isinstance(raw, Mapping):
        raise ItemSchemaError("economic_policy must be an object")
    required = {
        "classification",
        "currency_code",
        "market_value_minor",
        "replacement_value_minor",
        "unit_value_minor",
        "unit_quantity",
        "unit_label",
        "net_worth_treatment",
        "included_in_parent_ref",
        "valuation_method",
    }
    _exact(raw, required, label="economic_policy")

    classification = _nonempty_string(raw["classification"], label="economic_policy.classification")
    if classification not in VALID_CLASSIFICATIONS:
        raise ItemSchemaError(f"unsupported economic value classification: {classification}")
    treatment = _nonempty_string(raw["net_worth_treatment"], label="economic_policy.net_worth_treatment")
    if treatment not in VALID_NET_WORTH_TREATMENTS:
        raise ItemSchemaError(f"unsupported net_worth_treatment: {treatment}")

    currency = raw["currency_code"]
    if currency is not None:
        currency = _nonempty_string(currency, label="economic_policy.currency_code").upper()
        if len(currency) != 3 or not currency.isalpha():
            raise ItemSchemaError("economic_policy.currency_code must be a 3-letter code")

    def minor(key: str) -> int | None:
        value = raw[key]
        if value is None:
            return None
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ItemSchemaError(f"economic_policy.{key} must be a non-negative integer minor-unit amount or null")
        return value

    market = minor("market_value_minor")
    replacement = minor("replacement_value_minor")
    unit_value = minor("unit_value_minor")
    unit_quantity_raw = raw["unit_quantity"]
    unit_quantity = None if unit_quantity_raw is None else _number(
        unit_quantity_raw,
        label="economic_policy.unit_quantity",
        positive=True,
    )
    unit_label = raw["unit_label"]
    if unit_label is not None:
        unit_label = _token(unit_label, label="economic_policy.unit_label")

    included_ref = raw["included_in_parent_ref"]
    if included_ref is not None:
        included_ref = _nonempty_string(included_ref, label="economic_policy.included_in_parent_ref")

    valuation_method = _token(raw["valuation_method"], label="economic_policy.valuation_method")
    monetary = any(value is not None for value in (market, replacement, unit_value))
    if monetary and currency is None:
        raise ItemSchemaError("economic_policy.currency_code is required when monetary values are represented")
    if treatment == "included_in_parent" and included_ref is None:
        raise ItemSchemaError("included_in_parent treatment requires economic_policy.included_in_parent_ref")
    if treatment != "included_in_parent" and included_ref is not None:
        raise ItemSchemaError("economic_policy.included_in_parent_ref is only valid with included_in_parent treatment")

    if classification == "consumable_stock":
        if not stackable:
            raise ItemSchemaError("consumable_stock classification requires a stackable Item")
        if treatment != "derived_stock":
            raise ItemSchemaError("consumable_stock classification requires derived_stock treatment")
        if unit_value is None or unit_quantity is None or unit_label is None:
            raise ItemSchemaError("consumable_stock requires unit_value_minor, unit_quantity and unit_label")
        if stack_unit is not None and unit_label != stack_unit:
            raise ItemSchemaError("economic_policy.unit_label must match modules.stack.canonical_unit")
    elif treatment == "derived_stock":
        raise ItemSchemaError("derived_stock treatment is only valid for consumable_stock classification")

    if classification in {"resource_proxy", "economically_immaterial"} and monetary:
        raise ItemSchemaError(f"{classification} must not carry monetary values in Item schema v1")
    if classification == "economically_immaterial" and treatment != "excluded":
        raise ItemSchemaError("economically_immaterial classification requires excluded treatment")
    if classification == "resource_proxy" and treatment != "excluded":
        raise ItemSchemaError("resource_proxy classification requires excluded treatment")

    return {
        "classification": classification,
        "currency_code": currency,
        "market_value_minor": market,
        "replacement_value_minor": replacement,
        "unit_value_minor": unit_value,
        "unit_quantity": unit_quantity,
        "unit_label": unit_label,
        "net_worth_treatment": treatment,
        "included_in_parent_ref": included_ref,
        "valuation_method": valuation_method,
    }


def validate_item_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and normalize one exact Item creation payload without persistence."""

    if not isinstance(payload, Mapping):
        raise ItemSchemaError("Item payload must be an object")
    _exact(
        payload,
        {"schema_version", "definition", "instance", "economic_policy", "requirements", "relationships"},
        label="Item payload",
    )
    if payload["schema_version"] != ITEM_SCHEMA_VERSION:
        raise ItemSchemaError(f"schema_version must be {ITEM_SCHEMA_VERSION!r}")

    definition = payload["definition"]
    if not isinstance(definition, Mapping):
        raise ItemSchemaError("definition must be an object")
    _exact(
        definition,
        {"key", "name", "kind", "description", "stackable", "mobility", "capabilities", "tags", "modules"},
        label="definition",
    )
    key = _token(definition["key"], label="definition.key")
    name = _nonempty_string(definition["name"], label="definition.name")
    description = _nonempty_string(definition["description"], label="definition.description")
    kind = _token(definition["kind"], label="definition.kind")
    if kind not in ITEM_KINDS:
        raise ItemSchemaError(f"unsupported definition.kind: {kind}")
    if not isinstance(definition["stackable"], bool):
        raise ItemSchemaError("definition.stackable must be boolean")
    stackable = definition["stackable"]
    mobility = _token(definition["mobility"], label="definition.mobility")
    if mobility not in ITEM_MOBILITY:
        raise ItemSchemaError(f"unsupported definition.mobility: {mobility}")
    if kind == "fixture" and mobility != "fixed":
        raise ItemSchemaError("fixture Items must use fixed mobility")

    capabilities = _string_list(definition["capabilities"], label="definition.capabilities", tokenized=True)
    unknown_capabilities = set(capabilities) - ITEM_CAPABILITIES
    if unknown_capabilities:
        raise ItemSchemaError(f"definition.capabilities contains unregistered capability(s): {sorted(unknown_capabilities)}")
    tags = _string_list(definition["tags"], label="definition.tags", tokenized=True)

    modules_raw = definition["modules"]
    if not isinstance(modules_raw, Mapping):
        raise ItemSchemaError("definition.modules must be an object")
    unknown_modules = set(modules_raw) - ITEM_MODULES
    if unknown_modules:
        raise ItemSchemaError(f"definition.modules contains unregistered module(s): {sorted(unknown_modules)}")

    normalized_modules: dict[str, Any] = {}
    physical_quantities: dict[str, PhysicalQuantity] = {}
    grade_results: dict[str, GradeResult] = {}
    if "physical" in modules_raw:
        normalized_modules["physical"], physical_quantities = _validate_physical_module(modules_raw["physical"])

    stack_unit: str | None = None
    if "stack" in modules_raw:
        normalized_modules["stack"] = _validate_stack_module(modules_raw["stack"])
        stack_unit = str(normalized_modules["stack"]["canonical_unit"])
    if stackable and "stack" not in modules_raw:
        raise ItemSchemaError("stackable Item requires modules.stack")
    if not stackable and "stack" in modules_raw:
        raise ItemSchemaError("non-stackable Item must not declare modules.stack")

    if "nutrition" in modules_raw:
        if not stackable or "eat" not in capabilities:
            raise ItemSchemaError("modules.nutrition requires a stackable Item with eat capability")
        normalized_modules["nutrition"] = _validate_nutrition_module(modules_raw["nutrition"], stack_unit=stack_unit)
    if "eat" in capabilities and "nutrition" not in modules_raw:
        raise ItemSchemaError("eat capability requires modules.nutrition")

    if "container" in modules_raw:
        if "store" not in capabilities:
            raise ItemSchemaError("modules.container requires store capability")
        normalized_modules["container"] = _validate_container_module(modules_raw["container"])
    if "store" in capabilities and "container" not in modules_raw:
        raise ItemSchemaError("store capability requires modules.container")

    if "resistance_training" in modules_raw:
        if "train" not in capabilities:
            raise ItemSchemaError("modules.resistance_training requires train capability")
        normalized_modules["resistance_training"], grade = _validate_resistance_module(modules_raw["resistance_training"])
        grade_results["resistance_load"] = grade
    if "train" in capabilities and "resistance_training" not in modules_raw:
        raise ItemSchemaError("train capability requires modules.resistance_training")

    instance = payload["instance"]
    if not isinstance(instance, Mapping):
        raise ItemSchemaError("instance must be an object")
    expected_mode = "stack" if stackable else "unique"
    if expected_mode == "stack":
        _exact(instance, {"mode", "quantity", "unit"}, label="instance")
        if instance["mode"] != "stack":
            raise ItemSchemaError("stackable Item instance.mode must be 'stack'")
        quantity = _number(instance["quantity"], label="instance.quantity", positive=True)
        unit = _token(instance["unit"], label="instance.unit")
        if unit != stack_unit:
            raise ItemSchemaError("instance.unit must match modules.stack.canonical_unit")
        if not math.isclose(quantity, float(normalized_modules["stack"]["initial_quantity"]), rel_tol=0.0, abs_tol=1e-12):
            raise ItemSchemaError("instance.quantity must match modules.stack.initial_quantity for initial creation")
        normalized_instance = {"mode": "stack", "quantity": quantity, "unit": unit}
    else:
        _exact(instance, {"mode"}, label="instance")
        if instance["mode"] != "unique":
            raise ItemSchemaError("non-stackable Item instance.mode must be 'unique'")
        normalized_instance = {"mode": "unique"}

    relationships = payload["relationships"]
    if not isinstance(relationships, Mapping):
        raise ItemSchemaError("relationships must be an object")
    _exact(relationships, set(ITEM_RELATION_TYPES), label="relationships")
    normalized_relationships: dict[str, str | None] = {}
    for relation_type in sorted(ITEM_RELATION_TYPES):
        target = relationships[relation_type]
        normalized_relationships[relation_type] = None if target is None else _nonempty_string(
            target,
            label=f"relationships.{relation_type}",
        )
    location_relation_count = sum(
        normalized_relationships[key] is not None for key in ("located_at", "stored_in", "carried_by", "equipped_by")
    )
    if location_relation_count > 1:
        raise ItemSchemaError("Item may have only one current physical placement mode among located_at/stored_in/carried_by/equipped_by")
    if mobility == "fixed" and any(normalized_relationships[key] is not None for key in ("carried_by", "equipped_by")):
        raise ItemSchemaError("fixed Item cannot be carried or equipped")

    normalized_requirements = _validate_requirements(payload["requirements"])
    normalized_economic = _validate_economic_policy(
        payload["economic_policy"],
        stackable=stackable,
        stack_unit=stack_unit,
    )

    normalized = {
        "schema_version": ITEM_SCHEMA_VERSION,
        "definition": {
            "key": key,
            "name": name,
            "kind": kind,
            "description": description,
            "stackable": stackable,
            "mobility": mobility,
            "capabilities": capabilities,
            "tags": tags,
            "modules": normalized_modules,
        },
        "instance": normalized_instance,
        "economic_policy": normalized_economic,
        "requirements": normalized_requirements,
        "relationships": normalized_relationships,
        "derived": {
            "grades": {
                dimension: {
                    "scheme_id": result.scheme_id,
                    "grade": result.grade,
                    "label": result.label,
                    "value": result.value,
                    "domain": result.domain,
                    "dimension": result.dimension,
                }
                for dimension, result in sorted(grade_results.items())
            }
        },
    }
    return normalized


__all__ = [
    "ITEM_CAPABILITIES",
    "ITEM_KINDS",
    "ITEM_MOBILITY",
    "ITEM_MODULES",
    "ITEM_RELATION_TYPES",
    "ITEM_SCHEMA_VERSION",
    "ItemSchemaError",
    "validate_item_payload",
]

from __future__ import annotations

import copy
import re
from typing import Any

from .economic_value import VALID_CLASSIFICATIONS, VALID_NET_WORTH_TREATMENTS
from .item_creation_schema import ITEM_CAPABILITIES, ITEM_KINDS, ITEM_MOBILITY
from .item_metrics import DEFAULT_ITEM_METRIC_REGISTRY


_MASS_UNITS = ["kg", "g", "lb", "oz"]
_LENGTH_UNITS = ["m", "cm", "mm", "in", "ft", "yd"]
_VOLUME_UNITS = ["m3", "l", "ml", "in3", "ft3", "floz_us", "cup_us", "pt_us", "qt_us", "gal_us"]
_GRADES = ["E", "D", "C", "B", "A", "S", "SS", "SSS", "X", "XX"]
_OPERATORS = ["lt", "lte", "gt", "gte", "eq", "ne"]
_IMMATERIAL_VALUATION_METHOD = "creator_explicit"
_AI_VALUATION_METHOD = "ai_estimate"
_REF_TOKEN_RE = re.compile(r"[^a-z0-9_-]+")


def _obj(properties: dict[str, Any], *, required: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": required if required is not None else list(properties),
        "additionalProperties": False,
    }


def _nullable(schema: dict[str, Any]) -> dict[str, Any]:
    return {"anyOf": [schema, {"type": "null"}]}


def _quantity(units: list[str]) -> dict[str, Any]:
    return _obj({"value": {"type": "number", "exclusiveMinimum": 0}, "unit": {"type": "string", "enum": units}})


def _requirement_leaf_schemas() -> list[dict[str, Any]]:
    scalar = {"type": ["string", "number", "boolean", "null"]}
    return [
        _obj({
            "type": {"type": "string", "enum": ["minimum_grade"]},
            "domain": {"type": "string"},
            "dimension": {"type": "string"},
            "minimum": {"type": "string", "enum": _GRADES},
        }),
        _obj({
            "type": {"type": "string", "enum": ["value_compare", "state_compare"]},
            "key": {"type": "string"},
            "operator": {"type": "string", "enum": _OPERATORS},
            "value": scalar,
        }),
        _obj({"type": {"type": "string", "enum": ["has_skill"]}, "skill": {"type": "string"}}),
        _obj({"type": {"type": "string", "enum": ["has_item", "equipped", "owns"]}, "ref": {"type": "string"}}),
        _obj({"type": {"type": "string", "enum": ["resident_of", "authorized_for"]}, "location_id": {"type": "string"}}),
    ]


def _requirement_schema() -> dict[str, Any]:
    leaves = _requirement_leaf_schemas()
    child = {"anyOf": copy.deepcopy(leaves)}
    composition = [
        _obj({"all": {"type": "array", "minItems": 1, "items": copy.deepcopy(child)}}),
        _obj({"any": {"type": "array", "minItems": 1, "items": copy.deepcopy(child)}}),
    ]
    return {"anyOf": [{"type": "null"}, *leaves, *composition]}


def item_ai_fill_schema() -> dict[str, Any]:
    physical = _obj({
        "mass": _nullable(_quantity(_MASS_UNITS)),
        "length": _nullable(_quantity(_LENGTH_UNITS)),
        "width": _nullable(_quantity(_LENGTH_UNITS)),
        "height": _nullable(_quantity(_LENGTH_UNITS)),
    })
    stack = _obj({
        "canonical_unit": {"type": "string"},
        "initial_quantity": {"type": "number", "exclusiveMinimum": 0},
    })
    nutrition = _obj({
        "basis_quantity": {"type": "number", "exclusiveMinimum": 0},
        "unit": {"type": "string"},
        "energy_kcal": {"type": "number", "minimum": 0},
        "protein_g": {"type": "number", "minimum": 0},
        "carbohydrate_g": {"type": "number", "minimum": 0},
        "fat_g": {"type": "number", "minimum": 0},
    })
    container = _obj({"capacity_volume": _quantity(_VOLUME_UNITS)})
    resistance = _obj({"resistance_load": _quantity(_MASS_UNITS)})
    metrics = _obj(DEFAULT_ITEM_METRIC_REGISTRY.ai_schema_properties())

    modules = _obj({
        "physical": _nullable(physical),
        "stack": _nullable(stack),
        "nutrition": _nullable(nutrition),
        "container": _nullable(container),
        "resistance_training": _nullable(resistance),
        "metrics": _nullable(metrics),
    })

    definition = _obj({
        "key": {"type": "string"},
        "name": {"type": "string"},
        "kind": {"type": "string", "enum": sorted(ITEM_KINDS)},
        "description": {"type": "string"},
        "stackable": {"type": "boolean"},
        "mobility": {"type": "string", "enum": sorted(ITEM_MOBILITY)},
        "capabilities": {"type": "array", "items": {"type": "string", "enum": sorted(ITEM_CAPABILITIES)}},
        "tags": {"type": "array", "items": {"type": "string"}},
        "modules": modules,
    })

    instance = _obj({
        "mode": {"type": "string", "enum": ["unique", "stack"]},
        "quantity": {"type": ["number", "null"], "minimum": 0},
        "unit": {"type": ["string", "null"]},
    })

    economic = _obj({
        "classification": {"type": "string", "enum": sorted(VALID_CLASSIFICATIONS)},
        "currency_code": {"type": ["string", "null"]},
        "market_value_minor": {"type": ["integer", "null"], "minimum": 0},
        "replacement_value_minor": {"type": ["integer", "null"], "minimum": 0},
        "unit_value_minor": {"type": ["integer", "null"], "minimum": 0},
        "unit_quantity": {"type": ["number", "null"], "exclusiveMinimum": 0},
        "unit_label": {"type": ["string", "null"]},
        "net_worth_treatment": {"type": "string", "enum": sorted(VALID_NET_WORTH_TREATMENTS)},
        "included_in_parent_ref": {"type": ["string", "null"]},
        "valuation_method": {"type": "string"},
    })

    relationships = _obj({
        "located_at": {"type": ["string", "null"]},
        "stored_in": {"type": ["string", "null"]},
        "owned_by": {"type": ["string", "null"]},
        "carried_by": {"type": ["string", "null"]},
        "equipped_by": {"type": ["string", "null"]},
    })

    return _obj({
        "schema_version": {"type": "string", "enum": ["item-v1"]},
        "definition": definition,
        "instance": instance,
        "economic_policy": economic,
        "requirements": _obj({"use": _requirement_schema()}),
        "relationships": relationships,
    })


def item_batch_ai_fill_schema() -> dict[str, Any]:
    return _obj({
        "items": {
            "type": "array",
            "minItems": 1,
            "items": _obj({
                "ref": {"type": "string"},
                "payload": item_ai_fill_schema(),
            }),
        }
    })


def _canonical_token(value: Any, *, prefix: str = "item") -> str:
    token = str(value or "").strip().lower()
    token = _REF_TOKEN_RE.sub("_", token)
    token = re.sub(r"_+", "_", token).strip("_-")
    if token and not token[0].isalpha():
        token = f"{prefix}_{token}"
    return token


def _canonicalize_token_list(values: Any) -> Any:
    if not isinstance(values, list):
        return values
    result: list[Any] = []
    for value in values:
        token = _canonical_token(value, prefix="tag")
        if token and token not in result:
            result.append(token)
    return result


def _canonicalize_modules_and_instance(payload: dict[str, Any], definition: dict[str, Any]) -> None:
    modules = definition.get("modules")
    if not isinstance(modules, dict):
        return

    physical = modules.get("physical")
    if isinstance(physical, dict) and not any(value is not None for value in physical.values()):
        modules["physical"] = None

    metrics = modules.get("metrics")
    if isinstance(metrics, dict):
        metrics = {key: metric for key, metric in metrics.items() if metric is not None}
        modules["metrics"] = metrics or None

    instance = payload.get("instance")
    if not isinstance(instance, dict):
        instance = {}
        payload["instance"] = instance

    stack = modules.get("stack")
    if definition.get("stackable") is False:
        modules["stack"] = None
        instance.clear()
        instance["mode"] = "unique"
    elif isinstance(stack, dict):
        unit = _canonical_token(stack.get("canonical_unit"), prefix="unit")
        if unit:
            stack["canonical_unit"] = unit
            instance.clear()
            instance.update({"mode": "stack", "quantity": stack.get("initial_quantity"), "unit": unit})
    elif instance.get("mode") == "stack" and instance.get("quantity") is not None and instance.get("unit") is not None:
        unit = _canonical_token(instance.get("unit"), prefix="unit")
        if unit:
            modules["stack"] = {"canonical_unit": unit, "initial_quantity": instance.get("quantity")}
            instance.clear()
            instance.update({"mode": "stack", "quantity": modules["stack"]["initial_quantity"], "unit": unit})

    stack = modules.get("stack")
    if isinstance(stack, dict):
        stack_unit = stack.get("canonical_unit")
        nutrition = modules.get("nutrition")
        if isinstance(nutrition, dict) and stack_unit:
            nutrition["unit"] = stack_unit

    modules = {key: item for key, item in modules.items() if item is not None}
    definition["modules"] = modules

    capabilities = definition.get("capabilities")
    if isinstance(capabilities, list):
        normalized_capabilities: list[str] = []
        for value in capabilities:
            token = str(value or "").strip().lower()
            if token and token not in normalized_capabilities:
                normalized_capabilities.append(token)
        capabilities[:] = normalized_capabilities
        for module_name, capability in (
            ("nutrition", "eat"),
            ("container", "store"),
            ("resistance_training", "train"),
        ):
            if module_name in modules:
                if capability not in capabilities:
                    capabilities.append(capability)
            elif capability in capabilities:
                capabilities.remove(capability)


def _canonicalize_ai_economic_policy(payload: dict[str, Any]) -> None:
    economic = payload.get("economic_policy")
    if not isinstance(economic, dict):
        return

    currency = economic.get("currency_code")
    if isinstance(currency, str):
        economic["currency_code"] = currency.strip().upper() or None

    classification = economic.get("classification")
    treatment = economic.get("net_worth_treatment")
    monetary_keys = ("market_value_minor", "replacement_value_minor", "unit_value_minor")
    has_monetary_value = any(economic.get(key) is not None for key in monetary_keys)

    raw_method = economic.get("valuation_method")
    method = _canonical_token(raw_method, prefix="valuation")
    if classification == "economically_immaterial" and treatment == "excluded" and not has_monetary_value and not method:
        economic["valuation_method"] = _IMMATERIAL_VALUATION_METHOD
    else:
        economic["valuation_method"] = method or _AI_VALUATION_METHOD

    stack = payload.get("definition", {}).get("modules", {}).get("stack") if isinstance(payload.get("definition"), dict) else None
    stack_unit = stack.get("canonical_unit") if isinstance(stack, dict) else None
    unit_label = economic.get("unit_label")
    if classification == "consumable_stock" and stack_unit:
        economic["unit_label"] = stack_unit
    elif isinstance(unit_label, str):
        economic["unit_label"] = _canonical_token(unit_label, prefix="unit") or None


def canonicalize_ai_item_fill(value: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(value)
    definition = payload.get("definition")
    if isinstance(definition, dict):
        key = _canonical_token(definition.get("key"), prefix="item")
        if not key:
            key = _canonical_token(definition.get("name"), prefix="item")
        if key:
            definition["key"] = key
        definition["tags"] = _canonicalize_token_list(definition.get("tags"))
        _canonicalize_modules_and_instance(payload, definition)
    _canonicalize_ai_economic_policy(payload)
    return payload


def _canonical_batch_ref(value: Any) -> str:
    return _canonical_token(value, prefix="item")


def canonicalize_ai_item_batch_fill(value: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(value)
    items = candidate.get("items")
    if isinstance(items, list):
        aliases: dict[str, str] = {}
        for entry in items:
            if not isinstance(entry, dict):
                continue
            original = str(entry.get("ref") or "").strip()
            canonical = _canonical_batch_ref(original)
            if canonical:
                aliases[original.lower()] = canonical
                aliases[canonical] = canonical
                entry["ref"] = canonical

        for entry in items:
            if not isinstance(entry, dict) or not isinstance(entry.get("payload"), dict):
                continue
            payload = canonicalize_ai_item_fill(entry["payload"])
            relationships = payload.get("relationships")
            if isinstance(relationships, dict):
                stored_in = relationships.get("stored_in")
                if isinstance(stored_in, str):
                    raw_target = stored_in.strip()
                    bare_target = raw_target[1:] if raw_target.startswith("$") else raw_target
                    canonical_target = aliases.get(bare_target.lower())
                    if canonical_target:
                        relationships["stored_in"] = f"${canonical_target}"
            economic = payload.get("economic_policy")
            if isinstance(economic, dict):
                parent_ref = economic.get("included_in_parent_ref")
                if isinstance(parent_ref, str):
                    raw_target = parent_ref.strip()
                    bare_target = raw_target[1:] if raw_target.startswith("$") else raw_target
                    canonical_target = aliases.get(bare_target.lower())
                    if canonical_target:
                        economic["included_in_parent_ref"] = f"${canonical_target}"
            entry["payload"] = payload
    return candidate


__all__ = [
    "canonicalize_ai_item_batch_fill",
    "canonicalize_ai_item_fill",
    "item_ai_fill_schema",
    "item_batch_ai_fill_schema",
]

from __future__ import annotations

import copy
from typing import Any

from .economic_value import VALID_CLASSIFICATIONS, VALID_NET_WORTH_TREATMENTS
from .item_creation_schema import ITEM_CAPABILITIES, ITEM_KINDS, ITEM_MOBILITY


_MASS_UNITS = ["kg", "g", "lb", "oz"]
_LENGTH_UNITS = ["m", "cm", "mm", "in", "ft", "yd"]
_VOLUME_UNITS = ["m3", "l", "ml", "in3", "ft3", "floz_us", "cup_us", "pt_us", "qt_us", "gal_us"]
_GRADES = ["E", "D", "C", "B", "A", "S", "SS", "SSS", "X", "XX"]
_OPERATORS = ["lt", "lte", "gt", "gte", "eq", "ne"]


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
    """Exact provider-facing fill form for one item-v1 payload.

    The form intentionally carries nullable slots for every registered conditional
    module. Provider output is normalized back to the canonical sparse source
    representation before deterministic Item validation.
    """

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

    modules = _obj({
        "physical": _nullable(physical),
        "stack": _nullable(stack),
        "nutrition": _nullable(nutrition),
        "container": _nullable(container),
        "resistance_training": _nullable(resistance),
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


def canonicalize_ai_item_fill(value: dict[str, Any]) -> dict[str, Any]:
    """Convert the complete AI fill form into canonical sparse item-v1 source shape."""

    payload = copy.deepcopy(value)
    definition = payload.get("definition")
    if isinstance(definition, dict):
        modules = definition.get("modules")
        if isinstance(modules, dict):
            definition["modules"] = {key: item for key, item in modules.items() if item is not None}
    instance = payload.get("instance")
    if isinstance(instance, dict) and instance.get("mode") == "unique":
        instance.pop("quantity", None)
        instance.pop("unit", None)
    return payload


def canonicalize_ai_item_batch_fill(value: dict[str, Any]) -> dict[str, Any]:
    candidate = copy.deepcopy(value)
    items = candidate.get("items")
    if isinstance(items, list):
        for entry in items:
            if isinstance(entry, dict) and isinstance(entry.get("payload"), dict):
                entry["payload"] = canonicalize_ai_item_fill(entry["payload"])
    return candidate


__all__ = [
    "canonicalize_ai_item_batch_fill",
    "canonicalize_ai_item_fill",
    "item_ai_fill_schema",
    "item_batch_ai_fill_schema",
]

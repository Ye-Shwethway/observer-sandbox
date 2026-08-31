from __future__ import annotations

import copy
from typing import Any

from .location_schema_registry_v2 import (
    BOUNDARY_TYPES,
    DIRECTIONALITY,
    ENCLOSURES,
    EXPOSURES,
    FACILITY_TYPES,
    FUNCTIONAL_CLASSES,
    INTERFACE_KINDS,
    LIGHTING_PROFILES,
    LOCATION_CAPABILITIES,
    LOCATION_KINDS,
    LOCATION_SCHEMA_VERSION,
    OPERATING_STATES,
    OWNERSHIP_CLASSES,
    RESOURCE_TYPES,
    SOURCE_STATUSES,
    SURFACES,
    TRAVERSAL_MODES,
    UTILITIES,
    VALUE_CLASSIFICATIONS,
    VALUE_TREATMENTS,
    WEATHER_EXPOSURES,
)


def _enum(values) -> dict[str, Any]:
    return {"type": "string", "enum": sorted(str(value) for value in values)}


def _nullable(schema: dict[str, Any]) -> dict[str, Any]:
    return {"anyOf": [schema, {"type": "null"}]}


def _object(properties: dict[str, Any], *, required: list[str] | None = None) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": properties,
        "required": list(required if required is not None else properties),
        "additionalProperties": False,
    }


def _token_array(values=None) -> dict[str, Any]:
    item = _enum(values) if values is not None else {
        "type": "string",
        "pattern": "^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$",
    }
    return {"type": "array", "items": item, "uniqueItems": True}


def _quantity(kind: str) -> dict[str, Any]:
    return _nullable(
        _object(
            {
                "kind": {"type": "string", "enum": [kind]},
                "value": {"type": "number", "minimum": 0},
                "unit": {"type": "string", "minLength": 1},
            }
        )
    )


def _requirement_leaf_schemas() -> list[dict[str, Any]]:
    scalar = {"type": ["string", "number", "boolean", "null"]}
    return [
        _object({
            "type": {"type": "string", "enum": ["minimum_grade"]},
            "domain": {"type": "string", "minLength": 1},
            "dimension": {"type": "string", "minLength": 1},
            "minimum": {"type": "string", "minLength": 1},
        }),
        _object({
            "type": {"type": "string", "enum": ["value_compare", "state_compare"]},
            "key": {"type": "string", "minLength": 1},
            "operator": {"type": "string", "minLength": 1},
            "value": scalar,
        }),
        _object({
            "type": {"type": "string", "enum": ["has_skill"]},
            "skill": {"type": "string", "minLength": 1},
        }),
        _object({
            "type": {"type": "string", "enum": ["has_item", "equipped", "owns"]},
            "ref": {"type": "string", "minLength": 1},
        }),
        _object({
            "type": {"type": "string", "enum": ["resident_of", "authorized_for"]},
            "location_id": {"type": "string", "minLength": 1},
        }),
    ]


def _requirement_schema() -> dict[str, Any]:
    # The shared Requirement validator remains authoritative. The provider schema
    # supports typed leaves plus one explicit all/any composition layer; generated
    # Location access policies do not need unrestricted recursive authoring.
    leaves = _requirement_leaf_schemas()
    child = {"anyOf": leaves}
    return {
        "anyOf": [
            *leaves,
            _object({"all": {"type": "array", "minItems": 1, "items": child}}),
            _object({"any": {"type": "array", "minItems": 1, "items": child}}),
        ]
    }


def _access_policy_schema() -> dict[str, Any]:
    simple = [
        _object({"mode": {"type": "string", "enum": [mode]}})
        for mode in ("public", "owner_or_resident", "authorized", "restricted")
    ]
    return {
        "anyOf": [
            *simple,
            _object({
                "mode": {"type": "string", "enum": ["requirements"]},
                "requirements": _requirement_schema(),
            }),
        ]
    }


def location_ai_fill_schema() -> dict[str, Any]:
    """Provider-facing structured fill schema for one complete location-v2 payload."""

    interface = _object({
        "key": {"type": "string", "pattern": "^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$"},
        "name": {"type": "string", "minLength": 1},
        "kind": _enum(INTERFACE_KINDS),
        "destination_ref": {"type": ["string", "null"]},
        "directionality": _enum(DIRECTIONALITY),
        "enabled": {"type": "boolean"},
        "traversal_modes": _token_array(TRAVERSAL_MODES),
        "base_duration_minutes": {"type": ["number", "null"], "exclusiveMinimum": 0},
        "distance": _quantity("length"),
    })

    economics = _object({
        "classification": _enum(VALUE_CLASSIFICATIONS),
        "currency_code": {"type": ["string", "null"]},
        "market_value_minor": {"type": ["integer", "null"], "minimum": 0},
        "replacement_value_minor": {"type": ["integer", "null"], "minimum": 0},
        "net_worth_treatment": _enum(VALUE_TREATMENTS),
        "included_in_parent_ref": {"type": ["string", "null"]},
        "valuation_method": {"type": ["string", "null"]},
    })

    return _object({
        "schema_version": {"type": "string", "enum": [LOCATION_SCHEMA_VERSION]},
        "identity": _object({
            "key": {"type": "string", "pattern": "^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$"},
            "name": {"type": "string", "minLength": 1},
            "kind": _enum(LOCATION_KINDS),
            "description": {"type": "string", "minLength": 1},
            "functional_classes": _token_array(FUNCTIONAL_CLASSES),
            "tags": _token_array(),
        }),
        "structure": _object({
            "parent_ref": {"type": ["string", "null"]},
            "exposure": _enum(EXPOSURES),
        }),
        "geography": _object({
            "address_text": {"type": ["string", "null"]},
            "locality": {"type": ["string", "null"]},
            "region": {"type": ["string", "null"]},
            "country_code": {"type": ["string", "null"]},
            "position": _nullable(_object({
                "latitude": {"type": "number", "minimum": -90, "maximum": 90},
                "longitude": {"type": "number", "minimum": -180, "maximum": 180},
            })),
            "bounds": _nullable(_object({
                "south": {"type": "number", "minimum": -90, "maximum": 90},
                "west": {"type": "number", "minimum": -180, "maximum": 180},
                "north": {"type": "number", "minimum": -90, "maximum": 90},
                "east": {"type": "number", "minimum": -180, "maximum": 180},
            })),
        }),
        "spatial": _object({
            "area": _quantity("area"),
            "length": _quantity("length"),
            "width": _quantity("length"),
            "height": _quantity("length"),
            "elevation": _quantity("length"),
            "terrain": {"type": ["string", "null"]},
            "surface": _enum(SURFACES),
            "orientation_notes": {"type": ["string", "null"]},
        }),
        "boundary": _object({
            "type": _enum(BOUNDARY_TYPES),
            "enclosure": _enum(ENCLOSURES),
            "notes": {"type": ["string", "null"]},
        }),
        "access": _object({"policy": _access_policy_schema()}),
        "operations": _object({"initial_state": _enum(OPERATING_STATES)}),
        "topology": _object({"interfaces": {"type": "array", "items": interface}}),
        "facilities": _object({
            "capabilities": _token_array(LOCATION_CAPABILITIES),
            "facility_types": _token_array(FACILITY_TYPES),
            "resource_types": _token_array(RESOURCE_TYPES),
            "utilities": _token_array(UTILITIES),
        }),
        "environment": _object({
            "lighting_profile": _enum(LIGHTING_PROFILES),
            "weather_exposure": _enum(WEATHER_EXPOSURES),
        }),
        "control": _object({
            "ownership_class": _enum(OWNERSHIP_CLASSES),
            "owner_ref": {"type": ["string", "null"]},
            "operator_ref": {"type": ["string", "null"]},
        }),
        "economic_policy": _nullable(economics),
        "provenance": _object({
            "source_status": _enum(SOURCE_STATUSES),
            "source_note": {"type": ["string", "null"]},
        }),
    })


_FORBIDDEN_DERIVED_KEYS = {
    "derived", "grade", "grades", "grading", "evaluator", "evaluator_id",
    "threshold", "thresholds", "reference_profile", "reference_profile_id",
}

_OPTIONAL_TEXT_PATHS = {
    ("structure", "parent_ref"),
    ("geography", "address_text"),
    ("geography", "locality"),
    ("geography", "region"),
    ("geography", "country_code"),
    ("spatial", "terrain"),
    ("spatial", "orientation_notes"),
    ("boundary", "notes"),
    ("control", "owner_ref"),
    ("control", "operator_ref"),
    ("provenance", "source_note"),
    ("economic_policy", "currency_code"),
    ("economic_policy", "included_in_parent_ref"),
    ("economic_policy", "valuation_method"),
}


def _strip_forbidden(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_forbidden(item)
            for key, item in value.items()
            if str(key).lower() not in _FORBIDDEN_DERIVED_KEYS
        }
    if isinstance(value, list):
        return [_strip_forbidden(item) for item in value]
    return value


def repair_location_ai_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    """One deterministic representation-only repair pass.

    This function may normalize representation, never invent missing world facts.
    Missing semantic sections/fields remain missing and therefore still fail closed.
    """

    repaired = _strip_forbidden(copy.deepcopy(candidate))
    if not isinstance(repaired, dict):
        return candidate
    repaired["schema_version"] = LOCATION_SCHEMA_VERSION

    geography = repaired.get("geography")
    if isinstance(geography, dict) and isinstance(geography.get("country_code"), str):
        geography["country_code"] = geography["country_code"].strip().upper() or None

    provenance = repaired.get("provenance")
    if isinstance(provenance, dict):
        provenance["source_status"] = "provisional"

    for path in _OPTIONAL_TEXT_PATHS:
        current: Any = repaired
        for key in path[:-1]:
            if not isinstance(current, dict) or key not in current:
                current = None
                break
            current = current[key]
        if isinstance(current, dict):
            key = path[-1]
            if isinstance(current.get(key), str) and not current[key].strip():
                current[key] = None

    return repaired


__all__ = ["location_ai_fill_schema", "repair_location_ai_candidate"]

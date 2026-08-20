from __future__ import annotations

import math
import re
from copy import deepcopy
from typing import Any, Mapping

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
from .physical_quantity import PhysicalQuantityError, normalize_physical_quantity
from .requirements import RequirementContext, RequirementContractError, evaluate_access_policy
from .grading import evaluate_location_completeness

_KEY_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")
_COUNTRY_RE = re.compile(r"^[A-Z]{2}$")


class LocationCreationSchemaV2Error(ValueError):
    pass


def _exact(value: Mapping[str, Any], required: set[str], label: str) -> None:
    if not isinstance(value, Mapping):
        raise LocationCreationSchemaV2Error(f"{label} must be an object")
    missing = required - set(value)
    unknown = set(value) - required
    if missing:
        raise LocationCreationSchemaV2Error(f"{label} missing field(s): {sorted(missing)}")
    if unknown:
        raise LocationCreationSchemaV2Error(f"{label} unknown field(s): {sorted(unknown)}")


def _text(value: Any, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable:
        return None
    if not isinstance(value, str) or not value.strip():
        raise LocationCreationSchemaV2Error(f"{label} must be non-empty text")
    return value.strip()


def _token(value: Any, label: str) -> str:
    token = _text(value, label)
    assert token is not None
    token = token.lower()
    if not _KEY_RE.fullmatch(token):
        raise LocationCreationSchemaV2Error(f"{label} must be a stable lowercase token")
    return token


def _enum(value: Any, allowed: frozenset[str], label: str) -> str:
    token = str(value or "").strip().lower()
    if token not in allowed:
        raise LocationCreationSchemaV2Error(f"Unsupported {label}: {token!r}")
    return token


def _token_list(value: Any, allowed: frozenset[str], label: str) -> list[str]:
    if not isinstance(value, list):
        raise LocationCreationSchemaV2Error(f"{label} must be a list")
    result: list[str] = []
    for index, raw in enumerate(value):
        token = _token(raw, f"{label}[{index}]")
        if token not in allowed:
            raise LocationCreationSchemaV2Error(f"Unsupported {label} token: {token!r}")
        if token not in result:
            result.append(token)
    return result


def _free_token_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise LocationCreationSchemaV2Error(f"{label} must be a list")
    result: list[str] = []
    for index, raw in enumerate(value):
        token = _token(raw, f"{label}[{index}]")
        if token not in result:
            result.append(token)
    return result


def _quantity(value: Any, dimension: str, label: str) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping):
        raise LocationCreationSchemaV2Error(f"{label} must be a physical quantity object")
    if set(value) == {"value", "unit"}:
        raw_value, raw_unit = value["value"], value["unit"]
    elif set(value) == {"kind", "value", "unit"}:
        if str(value["kind"]).strip().lower() != dimension:
            raise LocationCreationSchemaV2Error(f"{label}.kind must be {dimension!r}")
        raw_value, raw_unit = value["value"], value["unit"]
    else:
        raise LocationCreationSchemaV2Error(f"{label} must contain value/unit or kind/value/unit")
    try:
        quantity = normalize_physical_quantity(dimension, raw_value, str(raw_unit))
    except (PhysicalQuantityError, TypeError, ValueError) as exc:
        raise LocationCreationSchemaV2Error(f"{label}: {exc}") from exc
    return quantity.as_dict()


def _finite_number(value: Any, label: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise LocationCreationSchemaV2Error(f"{label} must be numeric")
    numeric = float(value)
    if not math.isfinite(numeric) or numeric < minimum or numeric > maximum:
        raise LocationCreationSchemaV2Error(f"{label} must be in {minimum}..{maximum}")
    return numeric


def _geography(raw: Any) -> dict[str, Any]:
    fields = {"address_text", "locality", "region", "country_code", "position", "bounds"}
    _exact(raw, fields, "geography")
    country = _text(raw["country_code"], "country_code", nullable=True)
    if country is not None:
        country = country.upper()
        if not _COUNTRY_RE.fullmatch(country):
            raise LocationCreationSchemaV2Error("country_code must be a two-letter uppercase code")
    position = raw["position"]
    normalized_position = None
    if position is not None:
        _exact(position, {"latitude", "longitude"}, "geography.position")
        normalized_position = {
            "latitude": _finite_number(position["latitude"], "latitude", -90.0, 90.0),
            "longitude": _finite_number(position["longitude"], "longitude", -180.0, 180.0),
        }
    bounds = raw["bounds"]
    normalized_bounds = None
    if bounds is not None:
        _exact(bounds, {"south", "west", "north", "east"}, "geography.bounds")
        south = _finite_number(bounds["south"], "bounds.south", -90.0, 90.0)
        north = _finite_number(bounds["north"], "bounds.north", -90.0, 90.0)
        west = _finite_number(bounds["west"], "bounds.west", -180.0, 180.0)
        east = _finite_number(bounds["east"], "bounds.east", -180.0, 180.0)
        if south > north:
            raise LocationCreationSchemaV2Error("geography.bounds south must not exceed north")
        if west > east:
            raise LocationCreationSchemaV2Error("Antimeridian-spanning geography.bounds are not supported in v2")
        normalized_bounds = {"south": south, "west": west, "north": north, "east": east}
    return {
        "address_text": _text(raw["address_text"], "address_text", nullable=True),
        "locality": _text(raw["locality"], "locality", nullable=True),
        "region": _text(raw["region"], "region", nullable=True),
        "country_code": country,
        "position": normalized_position,
        "bounds": normalized_bounds,
    }


def _economic(raw: Any) -> dict[str, Any] | None:
    if raw is None:
        return None
    fields = {
        "classification", "currency_code", "market_value_minor", "replacement_value_minor",
        "net_worth_treatment", "included_in_parent_ref", "valuation_method",
    }
    _exact(raw, fields, "economic_policy")
    classification = _enum(raw["classification"], VALUE_CLASSIFICATIONS, "economic classification")
    treatment = _enum(raw["net_worth_treatment"], VALUE_TREATMENTS, "net-worth treatment")
    currency = _text(raw["currency_code"], "currency_code", nullable=True)
    if currency is not None:
        currency = currency.upper()
    result = {
        "classification": classification,
        "currency_code": currency,
        "market_value_minor": raw["market_value_minor"],
        "replacement_value_minor": raw["replacement_value_minor"],
        "net_worth_treatment": treatment,
        "included_in_parent_ref": _text(raw["included_in_parent_ref"], "included_in_parent_ref", nullable=True),
        "valuation_method": _text(raw["valuation_method"], "valuation_method", nullable=True),
    }
    for key in ("market_value_minor", "replacement_value_minor"):
        value = result[key]
        if value is not None and (isinstance(value, bool) or not isinstance(value, int) or value < 0):
            raise LocationCreationSchemaV2Error(f"{key} must be a non-negative integer or null")
    if classification in {"standalone_asset", "component"} and not currency:
        raise LocationCreationSchemaV2Error("Valued Location requires currency_code")
    if treatment == "included_in_parent" and not result["included_in_parent_ref"]:
        raise LocationCreationSchemaV2Error("included_in_parent requires included_in_parent_ref")
    return result


def _interface(raw: Any, index: int) -> dict[str, Any]:
    fields = {
        "key", "name", "kind", "destination_ref", "directionality", "enabled",
        "traversal_modes", "base_duration_minutes", "distance",
    }
    _exact(raw, fields, f"topology.interfaces[{index}]")
    enabled = raw["enabled"]
    if not isinstance(enabled, bool):
        raise LocationCreationSchemaV2Error("Interface enabled must be boolean")
    duration = raw["base_duration_minutes"]
    if duration is not None:
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(float(duration)) or float(duration) <= 0:
            raise LocationCreationSchemaV2Error("Interface base_duration_minutes must be positive or null")
        duration = float(duration)
    modes = _token_list(raw["traversal_modes"], TRAVERSAL_MODES, "interface traversal_modes")
    if not modes:
        raise LocationCreationSchemaV2Error("interface traversal_modes must not be empty")
    distance = _quantity(raw["distance"], "length", "interface distance")
    if distance is not None and float(distance["value"]) <= 0:
        raise LocationCreationSchemaV2Error("Interface distance must be positive or null")
    return {
        "key": _token(raw["key"], "interface key"),
        "name": _text(raw["name"], "interface name"),
        "kind": _enum(raw["kind"], INTERFACE_KINDS, "interface kind"),
        "destination_ref": _text(raw["destination_ref"], "destination_ref", nullable=True),
        "directionality": _enum(raw["directionality"], DIRECTIONALITY, "interface directionality"),
        "enabled": enabled,
        "traversal_modes": modes,
        "base_duration_minutes": duration,
        "distance": distance,
    }


def _completeness(payload: Mapping[str, Any]) -> str:
    kind = payload["identity"]["kind"]
    parent_ref = payload["structure"]["parent_ref"]
    level = 0
    if parent_ref is not None or kind in {"region", "property"}:
        level = 1
    interfaces = payload["topology"]["interfaces"]
    if level >= 1 and any(interface["enabled"] and interface["destination_ref"] for interface in interfaces):
        level = 2
    facilities = payload["facilities"]
    if level >= 2 and any(facilities[key] for key in ("capabilities", "facility_types", "resource_types", "utilities")):
        level = 3
    environment = payload["environment"]
    control = payload["control"]
    living_config = (
        payload["economic_policy"] is not None
        or control["owner_ref"] is not None
        or control["operator_ref"] is not None
        or control["ownership_class"] not in {"unknown", "unowned"}
        or environment["lighting_profile"] != "unknown"
        or environment["weather_exposure"] != "unknown"
        or payload["operations"]["initial_state"] != "open"
    )
    if level >= 3 and living_config:
        level = 4
    return f"L{level}"


def validate_location_payload_v2(payload: Mapping[str, Any]) -> dict[str, Any]:
    top = {
        "schema_version", "identity", "structure", "geography", "spatial", "boundary",
        "access", "operations", "topology", "facilities", "environment", "control",
        "economic_policy", "provenance",
    }
    _exact(payload, top, "Location payload")
    if payload["schema_version"] != LOCATION_SCHEMA_VERSION:
        raise LocationCreationSchemaV2Error("Unsupported Location schema version")

    _exact(payload["identity"], {"key", "name", "kind", "description", "functional_classes", "tags"}, "identity")
    identity = {
        "key": _token(payload["identity"]["key"], "Location key"),
        "name": _text(payload["identity"]["name"], "Location name"),
        "kind": _enum(payload["identity"]["kind"], LOCATION_KINDS, "Location kind"),
        "description": _text(payload["identity"]["description"], "Location description"),
        "functional_classes": _token_list(payload["identity"]["functional_classes"], FUNCTIONAL_CLASSES, "functional_classes"),
        "tags": _free_token_list(payload["identity"]["tags"], "tags"),
    }

    _exact(payload["structure"], {"parent_ref", "exposure"}, "structure")
    structure = {
        "parent_ref": _text(payload["structure"]["parent_ref"], "parent_ref", nullable=True),
        "exposure": _enum(payload["structure"]["exposure"], EXPOSURES, "exposure"),
    }

    geography = _geography(payload["geography"])

    _exact(payload["spatial"], {"area", "length", "width", "height", "elevation", "terrain", "surface", "orientation_notes"}, "spatial")
    spatial = {
        "area": _quantity(payload["spatial"]["area"], "area", "spatial.area"),
        "length": _quantity(payload["spatial"]["length"], "length", "spatial.length"),
        "width": _quantity(payload["spatial"]["width"], "length", "spatial.width"),
        "height": _quantity(payload["spatial"]["height"], "length", "spatial.height"),
        "elevation": _quantity(payload["spatial"]["elevation"], "length", "spatial.elevation"),
        "terrain": _text(payload["spatial"]["terrain"], "terrain", nullable=True),
        "surface": _enum(payload["spatial"]["surface"], SURFACES, "surface"),
        "orientation_notes": _text(payload["spatial"]["orientation_notes"], "orientation_notes", nullable=True),
    }

    _exact(payload["boundary"], {"type", "enclosure", "notes"}, "boundary")
    boundary = {
        "type": _enum(payload["boundary"]["type"], BOUNDARY_TYPES, "boundary type"),
        "enclosure": _enum(payload["boundary"]["enclosure"], ENCLOSURES, "boundary enclosure"),
        "notes": _text(payload["boundary"]["notes"], "boundary notes", nullable=True),
    }

    _exact(payload["access"], {"policy"}, "access")
    try:
        evaluate_access_policy(
            payload["access"]["policy"],
            RequirementContext(grades={}, values={}),
            location_id="schema-probe",
        )
    except RequirementContractError as exc:
        raise LocationCreationSchemaV2Error(str(exc)) from exc
    access = {"policy": deepcopy(payload["access"]["policy"])}

    _exact(payload["operations"], {"initial_state"}, "operations")
    operations = {"initial_state": _enum(payload["operations"]["initial_state"], OPERATING_STATES, "initial operating state")}

    _exact(payload["topology"], {"interfaces"}, "topology")
    raw_interfaces = payload["topology"]["interfaces"]
    if not isinstance(raw_interfaces, list):
        raise LocationCreationSchemaV2Error("topology.interfaces must be a list")
    interfaces = [_interface(raw, index) for index, raw in enumerate(raw_interfaces)]
    if len({row["key"] for row in interfaces}) != len(interfaces):
        raise LocationCreationSchemaV2Error("Interface keys must be unique")
    topology = {"interfaces": interfaces}

    _exact(payload["facilities"], {"capabilities", "facility_types", "resource_types", "utilities"}, "facilities")
    facilities = {
        "capabilities": _token_list(payload["facilities"]["capabilities"], LOCATION_CAPABILITIES, "facilities.capabilities"),
        "facility_types": _token_list(payload["facilities"]["facility_types"], FACILITY_TYPES, "facilities.facility_types"),
        "resource_types": _token_list(payload["facilities"]["resource_types"], RESOURCE_TYPES, "facilities.resource_types"),
        "utilities": _token_list(payload["facilities"]["utilities"], UTILITIES, "facilities.utilities"),
    }

    _exact(payload["environment"], {"lighting_profile", "weather_exposure"}, "environment")
    environment = {
        "lighting_profile": _enum(payload["environment"]["lighting_profile"], LIGHTING_PROFILES, "lighting profile"),
        "weather_exposure": _enum(payload["environment"]["weather_exposure"], WEATHER_EXPOSURES, "weather exposure"),
    }

    _exact(payload["control"], {"ownership_class", "owner_ref", "operator_ref"}, "control")
    control = {
        "ownership_class": _enum(payload["control"]["ownership_class"], OWNERSHIP_CLASSES, "ownership class"),
        "owner_ref": _text(payload["control"]["owner_ref"], "owner_ref", nullable=True),
        "operator_ref": _text(payload["control"]["operator_ref"], "operator_ref", nullable=True),
    }

    economic = _economic(payload["economic_policy"])

    _exact(payload["provenance"], {"source_status", "source_note"}, "provenance")
    provenance = {
        "source_status": _enum(payload["provenance"]["source_status"], SOURCE_STATUSES, "source status"),
        "source_note": _text(payload["provenance"]["source_note"], "source_note", nullable=True),
    }

    normalized = {
        "schema_version": LOCATION_SCHEMA_VERSION,
        "identity": identity,
        "structure": structure,
        "geography": geography,
        "spatial": spatial,
        "boundary": boundary,
        "access": access,
        "operations": operations,
        "topology": topology,
        "facilities": facilities,
        "environment": environment,
        "control": control,
        "economic_policy": economic,
        "provenance": provenance,
    }
    level = _completeness(normalized)
    grade = evaluate_location_completeness(level)
    normalized["derived"] = {
        "completeness_level": level,
        "completeness_grade": {
            "scheme_id": grade.scheme_id,
            "grade": grade.grade,
            "label": grade.label,
            "value": grade.value,
            "domain": grade.domain,
            "dimension": grade.dimension,
        },
    }
    return normalized


__all__ = ["LocationCreationSchemaV2Error", "validate_location_payload_v2"]

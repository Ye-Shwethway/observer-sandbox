from __future__ import annotations

import math
import re
from copy import deepcopy
from typing import Any, Mapping

from .grading import evaluate_location_completeness
from .physical_quantity import PhysicalQuantityError, normalize_physical_quantity
from .requirements import RequirementContext, RequirementContractError, evaluate_access_policy


LOCATION_SCHEMA_VERSION = "location-v1"
LOCATION_KINDS = frozenset({"region","property","building","floor","room","outdoor_zone","boundary","road","path","venue","wilderness","service_area"})
EXPOSURES = frozenset({"indoor","covered_outdoor","outdoor","mixed","unknown"})
OPERATING_STATES = frozenset({"open","closed","locked","blocked"})
DIRECTIONALITY = frozenset({"two_way","outbound","inbound"})
TRAVERSAL_MODES = frozenset({"walk"})
SOURCE_STATUSES = frozenset({"canonical","creator_authored","provisional","imported"})
VALUE_CLASSIFICATIONS = frozenset({"standalone_asset","component","resource_proxy","economically_immaterial"})
VALUE_TREATMENTS = frozenset({"independent","included_in_parent","excluded"})
_KEY_RE = re.compile(r"^[a-z][a-z0-9_.-]*$")


class LocationCreationSchemaError(ValueError):
    pass


def _exact(value: Mapping[str, Any], required: set[str], label: str) -> None:
    if not isinstance(value, Mapping):
        raise LocationCreationSchemaError(f"{label} must be an object")
    missing = required - set(value); unknown = set(value) - required
    if missing: raise LocationCreationSchemaError(f"{label} missing field(s): {sorted(missing)}")
    if unknown: raise LocationCreationSchemaError(f"{label} unknown field(s): {sorted(unknown)}")


def _text(value: Any, label: str, *, nullable: bool = False) -> str | None:
    if value is None and nullable: return None
    if not isinstance(value, str) or not value.strip(): raise LocationCreationSchemaError(f"{label} must be non-empty text")
    return value.strip()


def _ref(value: Any, label: str) -> str | None:
    return _text(value, label, nullable=True)


def _quantity(value: Any, dimension: str, label: str):
    if value is None: return None
    _exact(value, {"value","unit"}, label)
    try: q = normalize_physical_quantity(dimension, value["value"], value["unit"])
    except (PhysicalQuantityError, TypeError, ValueError) as exc: raise LocationCreationSchemaError(str(exc)) from exc
    return {
        "dimension": q.kind,
        "base_value": q.base_value,
        "base_unit": q.base_unit,
        "source_value": float(value["value"]),
        "source_unit": str(value["unit"]).strip().lower(),
    }


def _economic(raw: Any) -> dict[str, Any] | None:
    if raw is None: return None
    fields = {"classification","currency_code","market_value_minor","replacement_value_minor","net_worth_treatment","included_in_parent_ref","valuation_method"}
    _exact(raw, fields, "economic_policy")
    classification = str(raw["classification"] or "").strip()
    treatment = str(raw["net_worth_treatment"] or "").strip()
    if classification not in VALUE_CLASSIFICATIONS: raise LocationCreationSchemaError("Unsupported Location economic classification")
    if treatment not in VALUE_TREATMENTS: raise LocationCreationSchemaError("Unsupported Location net-worth treatment")
    result = dict(raw)
    for key in ("market_value_minor","replacement_value_minor"):
        val = result[key]
        if val is not None and (isinstance(val, bool) or not isinstance(val, int) or val < 0): raise LocationCreationSchemaError(f"{key} must be non-negative integer or null")
    if classification in {"standalone_asset","component"} and not result["currency_code"]:
        raise LocationCreationSchemaError("Valued Location requires currency_code")
    if treatment == "included_in_parent" and not result["included_in_parent_ref"]:
        raise LocationCreationSchemaError("included_in_parent requires included_in_parent_ref")
    return result


def _interface(raw: Any, index: int) -> dict[str, Any]:
    fields = {"key","name","destination_ref","directionality","enabled","traversal_modes","base_duration_minutes"}
    _exact(raw, fields, f"topology.interfaces[{index}]")
    key = _text(raw["key"], "interface key")
    if not _KEY_RE.fullmatch(key): raise LocationCreationSchemaError("Interface key has invalid format")
    direction = str(raw["directionality"] or "")
    if direction not in DIRECTIONALITY: raise LocationCreationSchemaError("Unsupported interface directionality")
    if not isinstance(raw["enabled"], bool): raise LocationCreationSchemaError("Interface enabled must be boolean")
    modes = raw["traversal_modes"]
    if not isinstance(modes, list) or not modes or any(mode not in TRAVERSAL_MODES for mode in modes): raise LocationCreationSchemaError("Interface traversal_modes must use supported modes")
    duration = raw["base_duration_minutes"]
    if duration is not None and (isinstance(duration, bool) or not isinstance(duration, (int,float)) or not math.isfinite(float(duration)) or float(duration) <= 0): raise LocationCreationSchemaError("Interface base_duration_minutes must be positive or null")
    return {"key": key,"name": _text(raw["name"], "interface name"),"destination_ref": _ref(raw["destination_ref"], "destination_ref"),"directionality": direction,"enabled": raw["enabled"],"traversal_modes": list(dict.fromkeys(modes)),"base_duration_minutes": None if duration is None else float(duration)}


def _completeness(payload: Mapping[str, Any]) -> str:
    structure = payload["structure"]; topology = payload["topology"]; facilities = payload["facilities"]; environment = payload["environment"]
    level = "L0"
    if structure["parent_ref"] is not None or payload["identity"]["kind"] in {"region","property"}: level = "L1"
    if topology["interfaces"] and payload["access"]["policy"]: level = "L2"
    if level == "L2" and (facilities["capabilities"] or facilities["facilities"] or facilities["resources"]): level = "L3"
    if level == "L3" and (any(v is not None and v != [] for v in environment.values()) or payload["economic_policy"] is not None): level = "L4"
    return level


def validate_location_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    top = {"schema_version","identity","structure","spatial","access","topology","facilities","environment","economic_policy","provenance"}
    _exact(payload, top, "Location payload")
    if payload["schema_version"] != LOCATION_SCHEMA_VERSION: raise LocationCreationSchemaError("Unsupported Location schema version")

    _exact(payload["identity"], {"key","name","kind","description","functional_class"}, "identity")
    key = _text(payload["identity"]["key"], "Location key")
    if not _KEY_RE.fullmatch(key): raise LocationCreationSchemaError("Location key has invalid format")
    kind = str(payload["identity"]["kind"] or "")
    if kind not in LOCATION_KINDS: raise LocationCreationSchemaError("Unsupported Location kind")
    identity = {"key":key,"name":_text(payload["identity"]["name"],"Location name"),"kind":kind,"description":_text(payload["identity"]["description"],"Location description"),"functional_class":_text(payload["identity"]["functional_class"],"functional_class",nullable=True)}

    _exact(payload["structure"], {"parent_ref","exposure"}, "structure")
    exposure = str(payload["structure"]["exposure"] or "")
    if exposure not in EXPOSURES: raise LocationCreationSchemaError("Unsupported exposure")
    structure = {"parent_ref":_ref(payload["structure"]["parent_ref"],"parent_ref"),"exposure":exposure}

    _exact(payload["spatial"], {"area","length","width","height","elevation","terrain","orientation_notes"}, "spatial")
    spatial = {
        "area": _quantity(payload["spatial"]["area"], "area", "area"),
        "length": _quantity(payload["spatial"]["length"], "length", "length"),
        "width": _quantity(payload["spatial"]["width"], "length", "width"),
        "height": _quantity(payload["spatial"]["height"], "length", "height"),
        "elevation": _quantity(payload["spatial"]["elevation"], "length", "elevation"),
        "terrain": _text(payload["spatial"]["terrain"], "terrain", nullable=True),
        "orientation_notes": _text(payload["spatial"]["orientation_notes"], "orientation_notes", nullable=True),
    }

    _exact(payload["access"], {"policy","operating_state"}, "access")
    state = str(payload["access"]["operating_state"] or "")
    if state not in OPERATING_STATES: raise LocationCreationSchemaError("Unsupported operating_state")
    try:
        evaluate_access_policy(payload["access"]["policy"], RequirementContext(grades={}, values={}), location_id="schema-probe")
    except RequirementContractError as exc: raise LocationCreationSchemaError(str(exc)) from exc
    access = {"policy":deepcopy(payload["access"]["policy"]),"operating_state":state}

    _exact(payload["topology"], {"interfaces"}, "topology")
    if not isinstance(payload["topology"]["interfaces"], list): raise LocationCreationSchemaError("topology.interfaces must be a list")
    interfaces = [_interface(raw, i) for i, raw in enumerate(payload["topology"]["interfaces"])]
    if len({i["key"] for i in interfaces}) != len(interfaces): raise LocationCreationSchemaError("Interface keys must be unique")
    topology = {"interfaces":interfaces}

    _exact(payload["facilities"], {"capabilities","facilities","resources"}, "facilities")
    facilities = {}
    for field in ("capabilities","facilities","resources"):
        values = payload["facilities"][field]
        if not isinstance(values, list) or any(not isinstance(v,str) or not v.strip() for v in values): raise LocationCreationSchemaError(f"facilities.{field} must be a string list")
        facilities[field] = list(dict.fromkeys(v.strip() for v in values))

    _exact(payload["environment"], {"lighting","weather_exposure","utilities"}, "environment")
    utilities = payload["environment"]["utilities"]
    if not isinstance(utilities, list) or any(not isinstance(v,str) or not v.strip() for v in utilities): raise LocationCreationSchemaError("environment.utilities must be a string list")
    environment = {"lighting":_text(payload["environment"]["lighting"],"lighting",nullable=True),"weather_exposure":_text(payload["environment"]["weather_exposure"],"weather_exposure",nullable=True),"utilities":list(dict.fromkeys(v.strip() for v in utilities))}

    economic = _economic(payload["economic_policy"])
    _exact(payload["provenance"], {"source_status","source_note"}, "provenance")
    source_status = str(payload["provenance"]["source_status"] or "")
    if source_status not in SOURCE_STATUSES: raise LocationCreationSchemaError("Unsupported provenance source_status")
    provenance = {"source_status":source_status,"source_note":_text(payload["provenance"]["source_note"],"source_note",nullable=True)}

    normalized = {"schema_version":LOCATION_SCHEMA_VERSION,"identity":identity,"structure":structure,"spatial":spatial,"access":access,"topology":topology,"facilities":facilities,"environment":environment,"economic_policy":economic,"provenance":provenance}
    level = _completeness(normalized); grade = evaluate_location_completeness(level)
    normalized["derived"] = {"completeness_level":level,"completeness_grade":{"scheme_id":grade.scheme_id,"grade":grade.grade,"label":grade.label,"value":grade.value,"domain":grade.domain,"dimension":grade.dimension}}
    return normalized


__all__ = ["LOCATION_SCHEMA_VERSION","LocationCreationSchemaError","validate_location_payload"]

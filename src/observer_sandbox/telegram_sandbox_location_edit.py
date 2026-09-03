from __future__ import annotations

import json
import re
import sqlite3
from copy import deepcopy
from typing import Any

from .creation_sandbox import list_sandbox_objects
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
from .sandbox_location_operations import (
    SandboxLocationOperationError,
    location_source_fingerprint,
    preflight_sandbox_location_update_v2,
    update_sandbox_location_v2,
)
from .sandbox_location_v2 import get_sandbox_location_v2


class SandboxLocationEditError(ValueError):
    pass


_SESSIONS: dict[int, dict[str, Any]] = {}
_SECTION_LABELS = {
    "identity": "🪪 Identity",
    "structure": "🏗 Structure",
    "geography": "🗺 Geography",
    "spatial": "📐 Spatial",
    "boundary": "🧱 Boundary",
    "access": "🚪 Access",
    "operations": "⚙️ Operations",
    "topology": "🔗 Topology",
    "facilities": "🏢 Facilities",
    "environment": "🌤 Environment",
    "control": "🔐 Control",
    "economic_policy": "💰 Economics",
    "provenance": "🧾 Provenance",
}
_FIELD_SPECS: dict[str, dict[str, Any]] = {
    "in_name": {"section": "identity", "path": ("identity", "name"), "label": "Name", "kind": "text"},
    "in_kind": {"section": "identity", "path": ("identity", "kind"), "label": "Kind", "kind": "enum", "choices": LOCATION_KINDS},
    "in_desc": {"section": "identity", "path": ("identity", "description"), "label": "Description", "kind": "text"},
    "in_func": {"section": "identity", "path": ("identity", "functional_classes"), "label": "Functional Classes", "kind": "tokens", "choices": FUNCTIONAL_CLASSES},
    "in_tags": {"section": "identity", "path": ("identity", "tags"), "label": "Tags", "kind": "csv"},
    "st_parent": {"section": "structure", "path": ("structure", "parent_ref"), "label": "Parent Location", "kind": "reference", "ref_type": "location", "nullable": True},
    "st_exp": {"section": "structure", "path": ("structure", "exposure"), "label": "Exposure", "kind": "enum", "choices": EXPOSURES},
    "geo_addr": {"section": "geography", "path": ("geography", "address_text"), "label": "Address", "kind": "text", "nullable": True},
    "geo_loc": {"section": "geography", "path": ("geography", "locality"), "label": "Locality", "kind": "text", "nullable": True},
    "geo_reg": {"section": "geography", "path": ("geography", "region"), "label": "Region", "kind": "text", "nullable": True},
    "geo_ctry": {"section": "geography", "path": ("geography", "country_code"), "label": "Country Code", "kind": "country", "nullable": True},
    "geo_pos": {"section": "geography", "path": ("geography", "position"), "label": "Position", "kind": "position", "nullable": True},
    "geo_bnd": {"section": "geography", "path": ("geography", "bounds"), "label": "Bounds", "kind": "bounds", "nullable": True},
    "sp_area": {"section": "spatial", "path": ("spatial", "area"), "label": "Area", "kind": "quantity", "dimension": "area", "nullable": True},
    "sp_len": {"section": "spatial", "path": ("spatial", "length"), "label": "Length", "kind": "quantity", "dimension": "length", "nullable": True},
    "sp_wid": {"section": "spatial", "path": ("spatial", "width"), "label": "Width", "kind": "quantity", "dimension": "length", "nullable": True},
    "sp_hgt": {"section": "spatial", "path": ("spatial", "height"), "label": "Height", "kind": "quantity", "dimension": "length", "nullable": True},
    "sp_elv": {"section": "spatial", "path": ("spatial", "elevation"), "label": "Elevation", "kind": "quantity", "dimension": "length", "nullable": True},
    "sp_terr": {"section": "spatial", "path": ("spatial", "terrain"), "label": "Terrain", "kind": "text", "nullable": True},
    "sp_surf": {"section": "spatial", "path": ("spatial", "surface"), "label": "Surface", "kind": "enum", "choices": SURFACES},
    "sp_orient": {"section": "spatial", "path": ("spatial", "orientation_notes"), "label": "Orientation Notes", "kind": "text", "nullable": True},
    "bd_type": {"section": "boundary", "path": ("boundary", "type"), "label": "Boundary Type", "kind": "enum", "choices": BOUNDARY_TYPES},
    "bd_enc": {"section": "boundary", "path": ("boundary", "enclosure"), "label": "Enclosure", "kind": "enum", "choices": ENCLOSURES},
    "bd_note": {"section": "boundary", "path": ("boundary", "notes"), "label": "Boundary Notes", "kind": "text", "nullable": True},
    "ac_mode": {"section": "access", "path": ("access", "policy"), "label": "Access Policy", "kind": "access"},
    "op_state": {"section": "operations", "path": ("operations", "initial_state"), "label": "Initial State", "kind": "enum", "choices": OPERATING_STATES},
    "fac_cap": {"section": "facilities", "path": ("facilities", "capabilities"), "label": "Capabilities", "kind": "tokens", "choices": LOCATION_CAPABILITIES},
    "fac_type": {"section": "facilities", "path": ("facilities", "facility_types"), "label": "Facility Types", "kind": "tokens", "choices": FACILITY_TYPES},
    "fac_res": {"section": "facilities", "path": ("facilities", "resource_types"), "label": "Resource Types", "kind": "tokens", "choices": RESOURCE_TYPES},
    "fac_util": {"section": "facilities", "path": ("facilities", "utilities"), "label": "Utilities", "kind": "tokens", "choices": UTILITIES},
    "env_light": {"section": "environment", "path": ("environment", "lighting_profile"), "label": "Lighting Profile", "kind": "enum", "choices": LIGHTING_PROFILES},
    "env_weather": {"section": "environment", "path": ("environment", "weather_exposure"), "label": "Weather Exposure", "kind": "enum", "choices": WEATHER_EXPOSURES},
    "ctl_own": {"section": "control", "path": ("control", "ownership_class"), "label": "Ownership Class", "kind": "enum", "choices": OWNERSHIP_CLASSES},
    "ctl_owner": {"section": "control", "path": ("control", "owner_ref"), "label": "Owner", "kind": "reference", "ref_type": "any", "nullable": True},
    "ctl_oper": {"section": "control", "path": ("control", "operator_ref"), "label": "Operator / Manager", "kind": "reference", "ref_type": "any", "nullable": True},
    "eco_class": {"section": "economic_policy", "path": ("economic_policy", "classification"), "label": "Classification", "kind": "enum", "choices": VALUE_CLASSIFICATIONS},
    "eco_curr": {"section": "economic_policy", "path": ("economic_policy", "currency_code"), "label": "Currency Code", "kind": "currency", "nullable": True},
    "eco_market": {"section": "economic_policy", "path": ("economic_policy", "market_value_minor"), "label": "Market Value (minor units)", "kind": "integer", "nullable": True},
    "eco_repl": {"section": "economic_policy", "path": ("economic_policy", "replacement_value_minor"), "label": "Replacement Value (minor units)", "kind": "integer", "nullable": True},
    "eco_treat": {"section": "economic_policy", "path": ("economic_policy", "net_worth_treatment"), "label": "Net-worth Treatment", "kind": "enum", "choices": VALUE_TREATMENTS},
    "eco_parent": {"section": "economic_policy", "path": ("economic_policy", "included_in_parent_ref"), "label": "Included in Parent", "kind": "reference", "ref_type": "location", "nullable": True},
    "eco_method": {"section": "economic_policy", "path": ("economic_policy", "valuation_method"), "label": "Valuation Method", "kind": "text", "nullable": True},
    "prov_status": {"section": "provenance", "path": ("provenance", "source_status"), "label": "Source Status", "kind": "enum", "choices": SOURCE_STATUSES},
    "prov_note": {"section": "provenance", "path": ("provenance", "source_note"), "label": "Source Note", "kind": "text", "nullable": True},
}
_ACCESS_SIMPLE_MODES = ("public", "owner_or_resident", "authorized", "restricted")
_QUANTITY_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*([A-Za-z0-9_]+)\s*$")


def _save_session(user_id: int, value: dict[str, Any] | None) -> None:
    if value is None:
        _SESSIONS.pop(int(user_id), None)
    else:
        _SESSIONS[int(user_id)] = deepcopy(value)


def get_sandbox_location_edit_session(*, user_id: int) -> dict[str, Any] | None:
    value = _SESSIONS.get(int(user_id))
    return None if value is None else deepcopy(value)


def _current_source(conn: sqlite3.Connection, session: dict[str, Any]) -> dict[str, Any]:
    return deepcopy(get_sandbox_location_v2(conn, str(session["object_id"]))["source"])


def _get_path(source: dict[str, Any], path: tuple[Any, ...]) -> Any:
    value: Any = source
    for part in path:
        value = value[part]
    return value


def _set_path(source: dict[str, Any], path: tuple[Any, ...], value: Any) -> None:
    target: Any = source
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value


def _human(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "Enabled" if value else "Disabled"
    if isinstance(value, list):
        return ", ".join(str(v).replace("_", " ").title() for v in value) if value else "None"
    if isinstance(value, dict) and {"kind", "value", "unit"} <= set(value):
        if isinstance(value.get("value"), (int, float)):
            return f"{float(value['value']):g} {str(value['unit']).replace('m2', 'm²')}"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    if isinstance(value, str) and value.islower():
        return value.replace("_", " ").title()
    return str(value)


def _preflight_proposal(conn: sqlite3.Connection, *, user_id: int, section: str, proposal: dict[str, Any]):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Sandbox Location edit session expired")
    try:
        preflight_sandbox_location_update_v2(
            conn,
            str(session["object_id"]),
            proposal,
            expected_source_fingerprint=str(session["base_fingerprint"]),
        )
    except SandboxLocationOperationError as exc:
        raise SandboxLocationEditError(str(exc)) from exc
    session.update({
        "pending_section": section,
        "pending_source": proposal,
        "pending_input": None,
        "pending_field_id": None,
        "token_working": None,
    })
    _save_session(user_id, session)
    return location_edit_preview_view(conn, user_id=user_id)


def enter_sandbox_location_edit(conn: sqlite3.Connection, *, user_id: int, object_id: str):
    location = get_sandbox_location_v2(conn, object_id)
    if location["lifecycle_status"] != "active":
        raise SandboxLocationEditError("Location edit target must be active")
    source = deepcopy(location["source"])
    _save_session(user_id, {
        "object_id": object_id,
        "name": source["identity"]["name"],
        "base_fingerprint": location_source_fingerprint(source),
        "pending_section": None,
        "pending_source": None,
        "pending_input": None,
        "pending_field_id": None,
        "token_working": None,
        "ref_picker_ids": [],
        "pending_interface_index": None,
    })
    return location_edit_home_view(conn, user_id=user_id)


def exit_sandbox_location_edit(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        return "✏️ No active Sandbox Location edit session.", [[{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]]
    object_id = str(session["object_id"])
    _save_session(user_id, None)
    return (
        "✅ SANDBOX LOCATION EDIT MODE CLOSED\n━━━━━━━━━━━━━━━━━━\n"
        f"{session.get('name') or object_id} editing finished.\n"
        "No runtime pause was needed because approved Sandbox Locations are not running yet.\n"
        "Canonical Real World remained unchanged.",
        [[{"text": "← Location", "callback_data": f"sw:o:{object_id}"}], [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]],
    )


def location_edit_home_view(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Sandbox Location edit session expired")
    location = get_sandbox_location_v2(conn, str(session["object_id"]))
    name = str(location["source"]["identity"]["name"])
    session.update({"name": name, "pending_section": None, "pending_source": None, "pending_input": None, "pending_field_id": None, "token_working": None})
    _save_session(user_id, session)
    lines = [
        f"✏️ {name} · SANDBOX LOCATION EDIT",
        "━━━━━━━━━━━━━━━━━━",
        "Choose a section, then the exact field you want to change.",
        "Normal editing is field-by-field; you do not need to write JSON.",
        "🔒 Identity key is immutable after creation.",
        "Every change still passes the complete location-v2 validator and graph preflight before Apply.",
    ]
    keyboard = [[{"text": label, "callback_data": f"sw:ledit:s:{section}"}] for section, label in _SECTION_LABELS.items()]
    keyboard.extend([[{"text": "✅ Done Editing", "callback_data": "sw:ledit:done"}], [{"text": "← Location", "callback_data": f"sw:o:{session['object_id']}"}]])
    return "\n".join(lines), keyboard


def _section_specs(section: str) -> list[tuple[str, dict[str, Any]]]:
    return [(field_id, spec) for field_id, spec in _FIELD_SPECS.items() if spec["section"] == section]


def location_section_prompt_view(conn: sqlite3.Connection, *, user_id: int, section: str):
    if section not in _SECTION_LABELS:
        raise SandboxLocationEditError("Unknown Location edit section")
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Sandbox Location edit session expired")
    source = _current_source(conn, session)
    session.update({"pending_section": None, "pending_source": None, "pending_input": None, "pending_field_id": None, "token_working": None})
    _save_session(user_id, session)
    if section == "topology":
        return topology_view(conn, user_id=user_id)
    if section == "economic_policy" and source["economic_policy"] is None:
        return (
            "💰 ECONOMICS · EDIT\n━━━━━━━━━━━━━━━━━━\nNo economic policy is represented for this Location.\n\nEnable one to edit its fields, or leave it unrepresented.",
            [[{"text": "➕ Enable Economics", "callback_data": "sw:ledit:eco:on"}], [{"text": "← Edit Location", "callback_data": "sw:ledit:home"}]],
        )
    lines = [f"{_SECTION_LABELS[section]} · EDIT", "━━━━━━━━━━━━━━━━━━", "Select one field to edit."]
    keyboard: list[list[dict[str, str]]] = []
    for field_id, spec in _section_specs(section):
        current = _get_path(source, spec["path"])
        keyboard.append([{"text": f"✏️ {spec['label']}: {_human(current)}"[:60], "callback_data": f"sw:ledit:f:{field_id}"}])
    if section == "economic_policy":
        keyboard.append([{"text": "🗑 Remove Economic Policy", "callback_data": "sw:ledit:eco:off"}])
    keyboard.append([{"text": "🧰 Advanced JSON", "callback_data": f"sw:ledit:json:{section}"}])
    keyboard.append([{"text": "← Edit Location", "callback_data": "sw:ledit:home"}])
    keyboard.append([{"text": "✅ Done Editing", "callback_data": "sw:ledit:done"}])
    return "\n".join(lines), keyboard


def _choice_rows(field_id: str, values: list[str], prefix: str) -> list[list[dict[str, str]]]:
    rows: list[list[dict[str, str]]] = []
    for start in range(0, len(values), 2):
        row = []
        for value in values[start:start + 2]:
            row.append({"text": value.replace("_", " ").title(), "callback_data": f"sw:ledit:{prefix}:{field_id}:{value}"})
        rows.append(row)
    return rows


def field_editor_view(conn: sqlite3.Connection, *, user_id: int, field_id: str):
    spec = _FIELD_SPECS.get(field_id)
    session = get_sandbox_location_edit_session(user_id=user_id)
    if spec is None or session is None:
        raise SandboxLocationEditError("Unknown or expired Location field selection")
    current = _get_path(_current_source(conn, session), spec["path"])
    kind = str(spec["kind"])
    session.update({"pending_field_id": field_id, "pending_input": None, "token_working": None, "pending_section": None, "pending_source": None})
    _save_session(user_id, session)
    header = f"✏️ {spec['label'].upper()}\n━━━━━━━━━━━━━━━━━━\nCurrent: {_human(current)}\n\n"
    if kind == "enum":
        keyboard = _choice_rows(field_id, sorted(str(v) for v in spec["choices"]), "choose")
        keyboard.append([{"text": "← Back", "callback_data": f"sw:ledit:s:{spec['section']}"}])
        return header + "Choose the new value.", keyboard
    if kind == "tokens":
        session["token_working"] = list(current or [])
        _save_session(user_id, session)
        return token_picker_view(conn, user_id=user_id, field_id=field_id)
    if kind == "reference":
        return reference_picker_view(conn, user_id=user_id, field_id=field_id)
    if kind == "access":
        keyboard = _choice_rows(field_id, list(_ACCESS_SIMPLE_MODES), "access")
        keyboard.append([{"text": "🧰 Requirement-based Access", "callback_data": "sw:ledit:access:req"}])
        keyboard.append([{"text": "← Back", "callback_data": "sw:ledit:s:access"}])
        return header + "Choose a standard access mode. Requirement-based access uses the universal advanced requirement contract editor.", keyboard
    session["pending_input"] = kind
    _save_session(user_id, session)
    prompt = {
        "text": "Send the new text as your next message.",
        "csv": "Send tags separated by commas, for example: home, private, lakeside",
        "country": "Send a two-letter country code, for example: US or MM.",
        "currency": "Send a currency code, for example: USD or MMK.",
        "integer": "Send a non-negative whole number in minor currency units.",
        "quantity": "Send value and unit, for example: 120 ft, 36 m, or 1800 ft2.",
        "position": "Send latitude, longitude, for example: 38.9399, -119.9772",
        "bounds": "Send south, west, north, east as four comma-separated numbers.",
    }.get(kind, "Send the new value as your next message.")
    keyboard: list[list[dict[str, str]]] = []
    if spec.get("nullable"):
        keyboard.append([{"text": "⊘ Clear / Unset", "callback_data": f"sw:ledit:clear:{field_id}"}])
    keyboard.append([{"text": "✕ Cancel Field Edit", "callback_data": f"sw:ledit:s:{spec['section']}"}])
    return header + prompt + "\nNothing changes until Preview → Apply.", keyboard


def token_picker_view(conn: sqlite3.Connection, *, user_id: int, field_id: str):
    spec = _FIELD_SPECS.get(field_id)
    session = get_sandbox_location_edit_session(user_id=user_id)
    if spec is None or session is None or spec.get("kind") != "tokens":
        raise SandboxLocationEditError("Token picker expired")
    selected = set(str(v) for v in (session.get("token_working") or []))
    lines = [f"☑️ {spec['label'].upper()}", "━━━━━━━━━━━━━━━━━━", "Tap values to select/unselect them.", f"Selected: {len(selected)}"]
    keyboard: list[list[dict[str, str]]] = []
    for value in sorted(str(v) for v in spec["choices"]):
        mark = "☑️" if value in selected else "◻️"
        keyboard.append([{"text": f"{mark} {value.replace('_', ' ').title()}"[:60], "callback_data": f"sw:ledit:tok:{field_id}:{value}"}])
    keyboard.append([{"text": "✅ Review Selection", "callback_data": f"sw:ledit:tokdone:{field_id}"}])
    keyboard.append([{"text": "⬜ Clear All", "callback_data": f"sw:ledit:tokclear:{field_id}"}])
    keyboard.append([{"text": "← Cancel", "callback_data": f"sw:ledit:s:{spec['section']}"}])
    return "\n".join(lines), keyboard


def _active_refs(conn: sqlite3.Connection, session: dict[str, Any], ref_type: str) -> list[dict[str, Any]]:
    sandbox_id = str(get_sandbox_location_v2(conn, str(session["object_id"]))["sandbox_id"])
    result: list[dict[str, Any]] = []
    for value in list_sandbox_objects(conn, sandbox_id=sandbox_id):
        if value.get("lifecycle_status") != "active" or str(value.get("object_id")) == str(session["object_id"]):
            continue
        if ref_type == "location" and value.get("creation_type") != "location":
            continue
        result.append(value)
    return result


def reference_picker_view(conn: sqlite3.Connection, *, user_id: int, field_id: str):
    spec = _FIELD_SPECS.get(field_id)
    session = get_sandbox_location_edit_session(user_id=user_id)
    if spec is None or session is None:
        raise SandboxLocationEditError("Reference picker expired")
    refs = _active_refs(conn, session, str(spec.get("ref_type") or "any"))
    session["ref_picker_ids"] = [str(value["object_id"]) for value in refs]
    _save_session(user_id, session)
    lines = [f"🔗 {spec['label'].upper()}", "━━━━━━━━━━━━━━━━━━", "Choose a represented object. Raw object IDs are not required."]
    keyboard: list[list[dict[str, str]]] = []
    for index, value in enumerate(refs):
        name = str(value.get("identity", {}).get("name") or value["object_id"])
        icon = {"location": "📍", "character": "👤", "item": "📦"}.get(str(value.get("creation_type")), "•")
        keyboard.append([{"text": f"{icon} {name}"[:60], "callback_data": f"sw:ledit:ref:{field_id}:{index}"}])
    if spec.get("nullable"):
        keyboard.append([{"text": "⊘ Clear / Unset", "callback_data": f"sw:ledit:clear:{field_id}"}])
    keyboard.append([{"text": "← Back", "callback_data": f"sw:ledit:s:{spec['section']}"}])
    if not refs:
        lines.append("No eligible active Sandbox objects are currently available.")
    return "\n".join(lines), keyboard


def _proposal_for_field(conn: sqlite3.Connection, session: dict[str, Any], spec: dict[str, Any], value: Any) -> dict[str, Any]:
    source = _current_source(conn, session)
    _set_path(source, spec["path"], value)
    return source


def _parse_text_value(spec: dict[str, Any], text: str) -> Any:
    raw = str(text or "").strip()
    kind = str(spec["kind"])
    if kind == "text":
        if not raw:
            raise SandboxLocationEditError("Value must not be empty; use Clear / Unset for nullable fields")
        return raw
    if kind == "csv":
        values: list[str] = []
        for part in raw.split(","):
            token = part.strip().lower().replace(" ", "_")
            if token and token not in values:
                values.append(token)
        return values
    if kind == "country":
        if len(raw) != 2 or not raw.isalpha():
            raise SandboxLocationEditError("Country code must contain exactly two letters")
        return raw.upper()
    if kind == "currency":
        if not raw or not raw.isalpha() or len(raw) > 8:
            raise SandboxLocationEditError("Currency code must contain letters only")
        return raw.upper()
    if kind == "integer":
        try:
            value = int(raw)
        except ValueError as exc:
            raise SandboxLocationEditError("Send a whole number") from exc
        if value < 0:
            raise SandboxLocationEditError("Value cannot be negative")
        return value
    if kind == "quantity":
        match = _QUANTITY_RE.fullmatch(raw)
        if not match:
            raise SandboxLocationEditError("Send a value followed by a unit, for example: 12 ft or 36 m")
        try:
            return normalize_physical_quantity(str(spec["dimension"]), float(match.group(1)), match.group(2)).as_dict()
        except (PhysicalQuantityError, ValueError) as exc:
            raise SandboxLocationEditError(str(exc)) from exc
    if kind == "position":
        parts = [part.strip() for part in raw.split(",")]
        if len(parts) != 2:
            raise SandboxLocationEditError("Position needs latitude, longitude")
        try:
            return {"latitude": float(parts[0]), "longitude": float(parts[1])}
        except ValueError as exc:
            raise SandboxLocationEditError("Latitude and longitude must be numbers") from exc
    if kind == "bounds":
        parts = [part.strip() for part in raw.split(",")]
        if len(parts) != 4:
            raise SandboxLocationEditError("Bounds need south, west, north, east")
        try:
            values = [float(part) for part in parts]
        except ValueError as exc:
            raise SandboxLocationEditError("All four bounds values must be numbers") from exc
        return {"south": values[0], "west": values[1], "north": values[2], "east": values[3]}
    raise SandboxLocationEditError("This field does not accept free-text input")


def advanced_json_prompt_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    section: str,
    access_requirements_only: bool = False,
):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Sandbox Location edit session expired")
    source = _current_source(conn, session)
    session["pending_section"] = section
    session["pending_source"] = None
    session["pending_field_id"] = "ac_mode" if access_requirements_only else None
    session["pending_input"] = "access_requirements_json" if access_requirements_only else "section_json"
    _save_session(user_id, session)
    current: Any = source[section]
    title = _SECTION_LABELS[section]
    if access_requirements_only:
        policy = source["access"]["policy"]
        current = policy.get("requirements") if policy.get("mode") == "requirements" else None
        title = "🚪 Access Requirements"
    return (
        f"🧰 {title} · ADVANCED JSON\n━━━━━━━━━━━━━━━━━━\n"
        "This is the advanced contract editor, not the normal edit path.\n"
        + ("Send the replacement requirement contract JSON.\n" if access_requirements_only else "Send the complete replacement JSON value for this section.\n")
        + "The complete Location still passes exact validation and graph preflight before Apply.\n\nCurrent value:\n"
        + json.dumps(current, ensure_ascii=False, indent=2, sort_keys=True),
        [[{"text": "✕ Cancel Advanced Edit", "callback_data": f"sw:ledit:s:{section}"}], [{"text": "✅ Done Editing", "callback_data": "sw:ledit:done"}]],
    )


def handle_sandbox_location_edit_text(conn: sqlite3.Connection, *, user_id: int, text: str):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None or not session.get("pending_input"):
        return None
    pending = str(session["pending_input"])
    if pending.startswith("interface:") or pending in {"interface_modes", "interface_dest"}:
        return None
    if pending == "section_json":
        section = str(session["pending_section"])
        try:
            replacement = json.loads((text or "").strip())
        except json.JSONDecodeError as exc:
            raise SandboxLocationEditError("Send valid JSON for the complete Location section") from exc
        proposal = _current_source(conn, session)
        proposal[section] = replacement
        return _preflight_proposal(conn, user_id=user_id, section=section, proposal=proposal)
    if pending == "access_requirements_json":
        try:
            requirement = json.loads((text or "").strip())
        except json.JSONDecodeError as exc:
            raise SandboxLocationEditError("Send valid JSON for the access requirement contract") from exc
        proposal = _current_source(conn, session)
        proposal["access"]["policy"] = {"mode": "requirements", "requirements": requirement}
        return _preflight_proposal(conn, user_id=user_id, section="access", proposal=proposal)
    field_id = str(session.get("pending_field_id") or "")
    spec = _FIELD_SPECS.get(field_id)
    if spec is None:
        raise SandboxLocationEditError("Location field input expired; open the field again")
    value = _parse_text_value(spec, text)
    return _preflight_proposal(
        conn,
        user_id=user_id,
        section=str(spec["section"]),
        proposal=_proposal_for_field(conn, session, spec, value),
    )


def topology_view(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Sandbox Location edit session expired")
    interfaces = list(_current_source(conn, session)["topology"]["interfaces"])
    lines = ["🔗 TOPOLOGY · EDIT", "━━━━━━━━━━━━━━━━━━", "Manage interfaces one at a time. No JSON is required for the normal path."]
    keyboard: list[list[dict[str, str]]] = []
    for index, interface in enumerate(interfaces):
        label = str(interface.get("name") or interface.get("key") or f"Interface {index + 1}")
        keyboard.append([{"text": f"✏️ {label}"[:60], "callback_data": f"sw:ledit:if:{index}"}])
    keyboard.append([{"text": "➕ Add Interface", "callback_data": "sw:ledit:ifadd"}])
    keyboard.append([{"text": "🧰 Advanced JSON", "callback_data": "sw:ledit:json:topology"}])
    keyboard.append([{"text": "← Edit Location", "callback_data": "sw:ledit:home"}])
    if not interfaces:
        lines.append("No interfaces are represented yet.")
    return "\n".join(lines), keyboard


def interface_view(conn: sqlite3.Connection, *, user_id: int, index: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Sandbox Location edit session expired")
    interfaces = _current_source(conn, session)["topology"]["interfaces"]
    if index < 0 or index >= len(interfaces):
        raise SandboxLocationEditError("Interface selection is no longer available")
    interface = interfaces[index]
    session.update({"pending_interface_index": index, "pending_input": None, "token_working": None})
    _save_session(user_id, session)
    lines = [f"🔗 {str(interface.get('name') or interface.get('key')).upper()}", "━━━━━━━━━━━━━━━━━━", "Choose the interface field to edit."]
    keyboard = [
        [{"text": f"✏️ Name: {_human(interface['name'])}"[:60], "callback_data": "sw:ledit:iff:name"}],
        [{"text": f"✏️ Key: {_human(interface['key'])}"[:60], "callback_data": "sw:ledit:iff:key"}],
        [{"text": f"✏️ Kind: {_human(interface['kind'])}"[:60], "callback_data": "sw:ledit:iff:kind"}],
        [{"text": f"✏️ Destination: {_human(interface['destination_ref'])}"[:60], "callback_data": "sw:ledit:iff:dest"}],
        [{"text": f"✏️ Direction: {_human(interface['directionality'])}"[:60], "callback_data": "sw:ledit:iff:dir"}],
        [{"text": f"✏️ Enabled: {_human(interface['enabled'])}"[:60], "callback_data": "sw:ledit:iff:enabled"}],
        [{"text": f"✏️ Traversal: {_human(interface['traversal_modes'])}"[:60], "callback_data": "sw:ledit:iff:modes"}],
        [{"text": f"✏️ Base Duration: {_human(interface['base_duration_minutes'])}"[:60], "callback_data": "sw:ledit:iff:dur"}],
        [{"text": f"✏️ Distance: {_human(interface['distance'])}"[:60], "callback_data": "sw:ledit:iff:dist"}],
        [{"text": "🗑 Delete Interface", "callback_data": "sw:ledit:ifdel"}],
        [{"text": "← Topology", "callback_data": "sw:ledit:s:topology"}],
    ]
    return "\n".join(lines), keyboard


def _interface_proposal(conn: sqlite3.Connection, session: dict[str, Any], key: str, value: Any) -> dict[str, Any]:
    source = _current_source(conn, session)
    index = int(session["pending_interface_index"])
    field = {
        "name": "name", "key": "key", "kind": "kind", "dest": "destination_ref",
        "dir": "directionality", "enabled": "enabled", "modes": "traversal_modes",
        "dur": "base_duration_minutes", "dist": "distance",
    }[key]
    source["topology"]["interfaces"][index][field] = value
    return source


def _interface_field_view(conn: sqlite3.Connection, *, user_id: int, key: str):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None or session.get("pending_interface_index") is None:
        raise SandboxLocationEditError("Interface edit session expired")
    index = int(session["pending_interface_index"])
    interface = _current_source(conn, session)["topology"]["interfaces"][index]
    if key in {"name", "key", "dur", "dist"}:
        session["pending_input"] = f"interface:{key}"
        _save_session(user_id, session)
        prompt = {
            "name": "Send the new interface name.",
            "key": "Send a stable lowercase interface key.",
            "dur": "Send base duration in minutes, or use Clear.",
            "dist": "Send distance such as 12 ft or 4 m, or use Clear.",
        }[key]
        keyboard: list[list[dict[str, str]]] = []
        if key in {"dur", "dist"}:
            keyboard.append([{"text": "⊘ Clear / Unset", "callback_data": f"sw:ledit:ifclear:{key}"}])
        keyboard.append([{"text": "← Interface", "callback_data": f"sw:ledit:if:{index}"}])
        return f"🔗 INTERFACE · {key.upper()}\n━━━━━━━━━━━━━━━━━━\n{prompt}\nNothing changes until Preview → Apply.", keyboard
    if key == "kind":
        return "🔗 INTERFACE KIND\n━━━━━━━━━━━━━━━━━━\nChoose a kind.", _choice_rows("ifkind", sorted(INTERFACE_KINDS), "ifchoose") + [[{"text": "← Interface", "callback_data": f"sw:ledit:if:{index}"}]]
    if key == "dir":
        return "🔗 INTERFACE DIRECTION\n━━━━━━━━━━━━━━━━━━\nChoose directionality.", _choice_rows("ifdir", sorted(DIRECTIONALITY), "ifchoose") + [[{"text": "← Interface", "callback_data": f"sw:ledit:if:{index}"}]]
    if key == "enabled":
        return "🔗 INTERFACE ENABLED\n━━━━━━━━━━━━━━━━━━\nChoose state.", [[{"text": "✅ Enabled", "callback_data": "sw:ledit:ifbool:1"}, {"text": "⛔ Disabled", "callback_data": "sw:ledit:ifbool:0"}], [{"text": "← Interface", "callback_data": f"sw:ledit:if:{index}"}]]
    if key == "modes":
        if session.get("pending_input") != "interface_modes":
            session["token_working"] = list(interface["traversal_modes"])
        session["pending_input"] = "interface_modes"
        _save_session(user_id, session)
        selected = set(str(v) for v in (session.get("token_working") or []))
        keyboard = [[{"text": ("☑️ " if value in selected else "◻️ ") + value.title(), "callback_data": f"sw:ledit:ifmode:{value}"}] for value in sorted(TRAVERSAL_MODES)]
        keyboard.append([{"text": "✅ Review Selection", "callback_data": "sw:ledit:ifmodedone"}])
        keyboard.append([{"text": "← Interface", "callback_data": f"sw:ledit:if:{index}"}])
        return "🔗 INTERFACE TRAVERSAL\n━━━━━━━━━━━━━━━━━━\nTap modes to select/unselect them. At least one is required.", keyboard
    if key == "dest":
        refs = _active_refs(conn, session, "location")
        session["ref_picker_ids"] = [str(value["object_id"]) for value in refs]
        session["pending_input"] = "interface_dest"
        _save_session(user_id, session)
        keyboard = [[{"text": f"📍 {str(value.get('identity', {}).get('name') or value['object_id'])}"[:60], "callback_data": f"sw:ledit:ifref:{idx}"}] for idx, value in enumerate(refs)]
        keyboard.append([{"text": "⊘ Clear / Unset", "callback_data": "sw:ledit:ifclear:dest"}])
        keyboard.append([{"text": "← Interface", "callback_data": f"sw:ledit:if:{index}"}])
        return "🔗 INTERFACE DESTINATION\n━━━━━━━━━━━━━━━━━━\nChoose a Location. Raw IDs are not required.", keyboard
    raise SandboxLocationEditError("Unknown interface field")


def _handle_interface_text(conn: sqlite3.Connection, *, user_id: int, key: str, text: str):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Interface edit session expired")
    raw = str(text or "").strip()
    if key == "name":
        if not raw:
            raise SandboxLocationEditError("Interface name must not be empty")
        value: Any = raw
    elif key == "key":
        value = raw.lower().replace(" ", "_")
    elif key == "dur":
        try:
            value = float(raw)
        except ValueError as exc:
            raise SandboxLocationEditError("Duration must be numeric minutes") from exc
        if value <= 0:
            raise SandboxLocationEditError("Duration must be positive")
    elif key == "dist":
        match = _QUANTITY_RE.fullmatch(raw)
        if not match:
            raise SandboxLocationEditError("Send distance such as 12 ft or 4 m")
        try:
            value = normalize_physical_quantity("length", float(match.group(1)), match.group(2)).as_dict()
        except (PhysicalQuantityError, ValueError) as exc:
            raise SandboxLocationEditError(str(exc)) from exc
    else:
        raise SandboxLocationEditError("Unknown interface text field")
    return _preflight_proposal(conn, user_id=user_id, section="topology", proposal=_interface_proposal(conn, session, key, value))


def _short(value: Any) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return rendered if len(rendered) <= 500 else rendered[:497] + "..."


def location_edit_preview_view(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None or not isinstance(session.get("pending_source"), dict):
        raise SandboxLocationEditError("No Location edit proposal is ready for Preview")
    section = str(session["pending_section"])
    location = get_sandbox_location_v2(conn, str(session["object_id"]))
    current = location["source"].get(section)
    proposed = session["pending_source"].get(section)
    return (
        "📋 LOCATION EDIT PREVIEW\n━━━━━━━━━━━━━━━━━━\n"
        f"Location: {location['source']['identity']['name']}\n"
        f"Section: {_SECTION_LABELS.get(section, section)}\n\n"
        f"BEFORE\n{_short(current)}\n\n"
        f"AFTER\n{_short(proposed)}\n\n"
        "✅ Exact location-v2 + same-Sandbox graph preflight passed.\n"
        "Apply is stale-guarded against the approved source you started editing.",
        [[{"text": "✅ Apply Edit", "callback_data": "sw:ledit:apply"}], [{"text": "← Edit Section", "callback_data": f"sw:ledit:s:{section}"}], [{"text": "✕ Discard Proposal", "callback_data": "sw:ledit:discard"}]],
    )


def apply_sandbox_location_edit(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None or not isinstance(session.get("pending_source"), dict):
        raise SandboxLocationEditError("No Location edit proposal is ready to Apply")
    try:
        updated = update_sandbox_location_v2(
            conn,
            str(session["object_id"]),
            session["pending_source"],
            expected_source_fingerprint=str(session["base_fingerprint"]),
        )
    except SandboxLocationOperationError as exc:
        raise SandboxLocationEditError(str(exc)) from exc
    session["base_fingerprint"] = location_source_fingerprint(updated["source"])
    session["name"] = updated["source"]["identity"]["name"]
    session.update({"pending_section": None, "pending_source": None, "pending_input": None, "pending_field_id": None, "token_working": None})
    _save_session(user_id, session)
    return (
        "✅ LOCATION EDIT APPLIED\n━━━━━━━━━━━━━━━━━━\n"
        f"Location: {session['name']}\n"
        "The approved Sandbox Location was atomically updated and audited.\n"
        "Runtime was not started and canonical Real World remained unchanged.",
        [[{"text": "✏️ Continue Editing", "callback_data": "sw:ledit:home"}], [{"text": "✅ Done Editing", "callback_data": "sw:ledit:done"}], [{"text": "← Location", "callback_data": f"sw:o:{session['object_id']}"}]],
    )


def _choose_field_value(conn: sqlite3.Connection, *, user_id: int, field_id: str, value: Any):
    spec = _FIELD_SPECS.get(field_id)
    session = get_sandbox_location_edit_session(user_id=user_id)
    if spec is None or session is None:
        raise SandboxLocationEditError("Location field selection expired")
    return _preflight_proposal(conn, user_id=user_id, section=str(spec["section"]), proposal=_proposal_for_field(conn, session, spec, value))


def location_edit_callback_view(conn: sqlite3.Connection, *, user_id: int, callback_data: str):
    if callback_data.startswith("sw:ledit:start:"):
        return enter_sandbox_location_edit(conn, user_id=user_id, object_id=callback_data.split(":", 3)[3])
    if callback_data == "sw:ledit:home":
        return location_edit_home_view(conn, user_id=user_id)
    if callback_data.startswith("sw:ledit:s:"):
        return location_section_prompt_view(conn, user_id=user_id, section=callback_data.split(":", 3)[3])
    if callback_data.startswith("sw:ledit:f:"):
        return field_editor_view(conn, user_id=user_id, field_id=callback_data.split(":", 3)[3])
    if callback_data.startswith("sw:ledit:json:"):
        return advanced_json_prompt_view(conn, user_id=user_id, section=callback_data.split(":", 3)[3])
    if callback_data == "sw:ledit:access:req":
        return advanced_json_prompt_view(conn, user_id=user_id, section="access", access_requirements_only=True)
    if callback_data.startswith("sw:ledit:choose:"):
        _, _, _, field_id, value = callback_data.split(":", 4)
        return _choose_field_value(conn, user_id=user_id, field_id=field_id, value=value)
    if callback_data.startswith("sw:ledit:access:"):
        _, _, _, field_id, mode = callback_data.split(":", 4)
        return _choose_field_value(conn, user_id=user_id, field_id=field_id, value={"mode": mode})
    if callback_data.startswith("sw:ledit:clear:"):
        return _choose_field_value(conn, user_id=user_id, field_id=callback_data.split(":", 3)[3], value=None)
    if callback_data.startswith("sw:ledit:tok:"):
        _, _, _, field_id, token = callback_data.split(":", 4)
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None or session.get("pending_field_id") != field_id:
            raise SandboxLocationEditError("Token selection expired")
        selected = set(str(value) for value in (session.get("token_working") or []))
        if token in selected:
            selected.remove(token)
        else:
            selected.add(token)
        session["token_working"] = sorted(selected)
        _save_session(user_id, session)
        return token_picker_view(conn, user_id=user_id, field_id=field_id)
    if callback_data.startswith("sw:ledit:tokclear:"):
        field_id = callback_data.split(":", 3)[3]
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Token selection expired")
        session["token_working"] = []
        _save_session(user_id, session)
        return token_picker_view(conn, user_id=user_id, field_id=field_id)
    if callback_data.startswith("sw:ledit:tokdone:"):
        field_id = callback_data.split(":", 3)[3]
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Token selection expired")
        return _choose_field_value(conn, user_id=user_id, field_id=field_id, value=list(session.get("token_working") or []))
    if callback_data.startswith("sw:ledit:ref:"):
        _, _, _, field_id, raw_index = callback_data.split(":", 4)
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Reference selection expired")
        refs = list(session.get("ref_picker_ids") or [])
        index = int(raw_index)
        if index < 0 or index >= len(refs):
            raise SandboxLocationEditError("Reference selection is no longer available")
        return _choose_field_value(conn, user_id=user_id, field_id=field_id, value=refs[index])
    if callback_data == "sw:ledit:eco:on":
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Sandbox Location edit session expired")
        proposal = _current_source(conn, session)
        proposal["economic_policy"] = {
            "classification": "economically_immaterial",
            "currency_code": None,
            "market_value_minor": None,
            "replacement_value_minor": None,
            "net_worth_treatment": "excluded",
            "included_in_parent_ref": None,
            "valuation_method": None,
        }
        return _preflight_proposal(conn, user_id=user_id, section="economic_policy", proposal=proposal)
    if callback_data == "sw:ledit:eco:off":
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Sandbox Location edit session expired")
        proposal = _current_source(conn, session)
        proposal["economic_policy"] = None
        return _preflight_proposal(conn, user_id=user_id, section="economic_policy", proposal=proposal)
    if callback_data == "sw:ledit:ifadd":
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Sandbox Location edit session expired")
        proposal = _current_source(conn, session)
        used = {str(value.get("key")) for value in proposal["topology"]["interfaces"]}
        number = 1
        while f"interface_{number}" in used:
            number += 1
        proposal["topology"]["interfaces"].append({
            "key": f"interface_{number}", "name": f"New Interface {number}", "kind": "door",
            "destination_ref": None, "directionality": "two_way", "enabled": True,
            "traversal_modes": ["walk"], "base_duration_minutes": None, "distance": None,
        })
        return _preflight_proposal(conn, user_id=user_id, section="topology", proposal=proposal)
    if callback_data.startswith("sw:ledit:if:"):
        return interface_view(conn, user_id=user_id, index=int(callback_data.split(":", 3)[3]))
    if callback_data.startswith("sw:ledit:iff:"):
        return _interface_field_view(conn, user_id=user_id, key=callback_data.split(":", 3)[3])
    if callback_data.startswith("sw:ledit:ifchoose:"):
        _, _, _, field_id, value = callback_data.split(":", 4)
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Interface edit expired")
        key = "kind" if field_id == "ifkind" else "dir"
        return _preflight_proposal(conn, user_id=user_id, section="topology", proposal=_interface_proposal(conn, session, key, value))
    if callback_data.startswith("sw:ledit:ifbool:"):
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Interface edit expired")
        return _preflight_proposal(conn, user_id=user_id, section="topology", proposal=_interface_proposal(conn, session, "enabled", callback_data.endswith(":1")))
    if callback_data.startswith("sw:ledit:ifref:"):
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Interface reference picker expired")
        refs = list(session.get("ref_picker_ids") or [])
        index = int(callback_data.split(":", 3)[3])
        if index < 0 or index >= len(refs):
            raise SandboxLocationEditError("Interface destination is no longer available")
        return _preflight_proposal(conn, user_id=user_id, section="topology", proposal=_interface_proposal(conn, session, "dest", refs[index]))
    if callback_data.startswith("sw:ledit:ifclear:"):
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Interface edit expired")
        key = callback_data.split(":", 3)[3]
        return _preflight_proposal(conn, user_id=user_id, section="topology", proposal=_interface_proposal(conn, session, key, None))
    if callback_data.startswith("sw:ledit:ifmode:"):
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Interface traversal picker expired")
        token = callback_data.split(":", 3)[3]
        selected = set(str(value) for value in (session.get("token_working") or []))
        if token in selected:
            selected.remove(token)
        else:
            selected.add(token)
        session["token_working"] = sorted(selected)
        session["pending_input"] = "interface_modes"
        _save_session(user_id, session)
        return _interface_field_view(conn, user_id=user_id, key="modes")
    if callback_data == "sw:ledit:ifmodedone":
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Interface traversal picker expired")
        values = list(session.get("token_working") or [])
        if not values:
            raise SandboxLocationEditError("At least one traversal mode is required")
        return _preflight_proposal(conn, user_id=user_id, section="topology", proposal=_interface_proposal(conn, session, "modes", values))
    if callback_data == "sw:ledit:ifdel":
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None or session.get("pending_interface_index") is None:
            raise SandboxLocationEditError("Interface edit expired")
        proposal = _current_source(conn, session)
        index = int(session["pending_interface_index"])
        if index < 0 or index >= len(proposal["topology"]["interfaces"]):
            raise SandboxLocationEditError("Interface is no longer available")
        del proposal["topology"]["interfaces"][index]
        return _preflight_proposal(conn, user_id=user_id, section="topology", proposal=proposal)
    if callback_data == "sw:ledit:apply":
        return apply_sandbox_location_edit(conn, user_id=user_id)
    if callback_data == "sw:ledit:discard":
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Sandbox Location edit session expired")
        session.update({"pending_section": None, "pending_source": None, "pending_input": None, "pending_field_id": None, "token_working": None})
        _save_session(user_id, session)
        return location_edit_home_view(conn, user_id=user_id)
    if callback_data == "sw:ledit:done":
        return exit_sandbox_location_edit(conn, user_id=user_id)
    raise KeyError(callback_data)


def handle_sandbox_location_interface_edit_text(conn: sqlite3.Connection, *, user_id: int, text: str):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        return None
    pending = str(session.get("pending_input") or "")
    if not pending.startswith("interface:"):
        return None
    return _handle_interface_text(conn, user_id=user_id, key=pending.split(":", 1)[1], text=text)


__all__ = [
    "SandboxLocationEditError",
    "apply_sandbox_location_edit",
    "enter_sandbox_location_edit",
    "exit_sandbox_location_edit",
    "field_editor_view",
    "get_sandbox_location_edit_session",
    "handle_sandbox_location_edit_text",
    "handle_sandbox_location_interface_edit_text",
    "location_edit_callback_view",
    "location_edit_home_view",
    "location_edit_preview_view",
    "location_section_prompt_view",
    "reference_picker_view",
    "token_picker_view",
    "topology_view",
]

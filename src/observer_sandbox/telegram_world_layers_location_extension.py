from __future__ import annotations

import sqlite3
from typing import Any

from .creation_sandbox import get_sandbox_object


def _text(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value or value.lower() in {"unknown", "none"}:
            return None
        return value.replace("_", " ").title()
    if isinstance(value, (int, float)):
        return f"{value:g}" if isinstance(value, float) else str(value)
    return None


def _target_name(conn: sqlite3.Connection, ref: Any) -> str | None:
    raw = str(ref or "").strip()
    if not raw:
        return None
    if raw.startswith("sbx_"):
        try:
            target = get_sandbox_object(conn, raw)
            return str(target.get("identity", {}).get("name") or raw)
        except Exception:
            return raw
    return raw


def _append(lines: list[str], label: str, value: Any, *, icon: str = "•") -> None:
    rendered = _text(value)
    if rendered:
        lines.append(f"{icon} {label}: {rendered}")


def human_location_detail_text(conn: sqlite3.Connection, value: dict[str, Any]) -> str:
    identity = value.get("identity") or {}
    props = value.get("properties") or {}
    structure = props.get("structure") or {}
    geography = props.get("geography") or {}
    spatial = props.get("spatial") or {}
    boundary = props.get("boundary") or {}
    access = props.get("access") or {}
    operations = props.get("operations") or {}
    environment = props.get("environment") or {}
    control = props.get("control") or {}
    facilities = props.get("facilities") or {}

    name = str(identity.get("name") or value.get("object_id") or "Location")
    kind = _text(identity.get("kind")) or "Location"
    lifecycle = _text(value.get("lifecycle_status")) or "Active"
    lines = [
        f"📍 {name}",
        "━━━━━━━━━━━━━━━━━━",
        f"🧪 Creation Sandbox · {lifecycle}",
        f"🏷 Type: {kind}",
    ]

    description = str(identity.get("description") or "").strip()
    if description:
        lines.extend(["", description])

    parent = _target_name(conn, structure.get("parent_ref"))
    locality = geography.get("locality")
    region = geography.get("region")
    country = geography.get("country_code")
    address = geography.get("address_text")
    if any((parent, locality, region, country, address)):
        lines.extend(["", "🧭 LOCATION"])
        if parent:
            lines.append(f"↳ Parent: {parent}")
        _append(lines, "Address", address, icon="📌")
        _append(lines, "Locality", locality, icon="🏙")
        _append(lines, "Region", region, icon="🗺")
        _append(lines, "Country", country, icon="🌐")

    physical_rows: list[str] = []
    for label, key in (("Area", "area"), ("Length", "length"), ("Width", "width"), ("Height", "height"), ("Elevation", "elevation")):
        rendered = _text(spatial.get(key))
        if rendered:
            physical_rows.append(f"• {label}: {rendered}")
    surface = _text(spatial.get("surface"))
    enclosure = _text(boundary.get("enclosure"))
    boundary_type = _text(boundary.get("type"))
    if physical_rows or surface or enclosure or boundary_type:
        lines.extend(["", "📐 PHYSICAL"])
        lines.extend(physical_rows)
        if surface:
            lines.append(f"• Surface: {surface}")
        if enclosure:
            lines.append(f"• Enclosure: {enclosure}")
        if boundary_type:
            lines.append(f"• Boundary: {boundary_type}")

    mode = _text((access.get("policy") or {}).get("mode"))
    initial_state = _text(operations.get("initial_state"))
    owner = _target_name(conn, control.get("owner_ref"))
    ownership = _text(control.get("ownership_class"))
    if mode or initial_state or owner or ownership:
        lines.extend(["", "🔐 ACCESS & CONTROL"])
        if mode:
            lines.append(f"• Access: {mode}")
        if initial_state:
            lines.append(f"• Initial state: {initial_state}")
        if owner:
            lines.append(f"• Owner: {owner}")
        if ownership:
            lines.append(f"• Ownership: {ownership}")

    lighting = _text(environment.get("lighting_profile"))
    weather = _text(environment.get("weather_exposure"))
    if lighting or weather:
        lines.extend(["", "🌤 ENVIRONMENT"])
        if lighting:
            lines.append(f"• Lighting: {lighting}")
        if weather:
            lines.append(f"• Weather exposure: {weather}")

    facility_types = [str(v).replace("_", " ").title() for v in facilities.get("facility_types") or [] if str(v).strip()]
    capabilities = [str(v).replace("_", " ").title() for v in facilities.get("capabilities") or [] if str(v).strip()]
    utilities = [str(v).replace("_", " ").title() for v in facilities.get("utilities") or [] if str(v).strip()]
    if facility_types or capabilities or utilities:
        lines.extend(["", "🏗 FACILITIES"])
        if facility_types:
            lines.append("• Types: " + ", ".join(facility_types))
        if capabilities:
            lines.append("• Capabilities: " + ", ".join(capabilities))
        if utilities:
            lines.append("• Utilities: " + ", ".join(utilities))

    relations = value.get("resolved_relations") or []
    if relations:
        lines.extend(["", "🔗 RELATIONSHIPS"])
        for relation in relations:
            target = _target_name(conn, relation.get("target_object_id")) or str(relation.get("target_object_id") or "—")
            rel = str(relation.get("relation_type") or "related_to").replace("_", " ").title()
            lines.append(f"• {rel} → {target}")

    lines.extend(["", "🧪 Sandbox-only location · canonical universe unchanged."])
    return "\n".join(lines)


def install_location_world_layers_extension(base) -> None:
    original_object_view = base.sandbox_object_view

    def sandbox_object_view(conn: sqlite3.Connection, object_id: str):
        value = get_sandbox_object(conn, object_id)
        if value["creation_type"] != "location":
            return original_object_view(conn, object_id)
        return human_location_detail_text(conn, value), [
            [{"text": "← Locations", "callback_data": "sw:list:location"}],
            [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
            [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
        ]

    base.sandbox_object_view = sandbox_object_view


__all__ = ["human_location_detail_text", "install_location_world_layers_extension"]

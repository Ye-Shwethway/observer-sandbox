from __future__ import annotations

import sqlite3
from typing import Any

from .creation_sandbox import get_sandbox_object
from .physical_quantity import PhysicalQuantity, format_physical_quantity
from .sandbox_location_v2 import get_sandbox_location_v2


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


def _quantity(value: Any) -> str | None:
    if not isinstance(value, dict):
        return None
    kind = str(value.get("kind") or "").strip().lower()
    unit = str(value.get("unit") or "").strip().lower()
    raw = value.get("value")
    if kind not in {"mass", "length", "area", "volume"} or isinstance(raw, bool) or not isinstance(raw, (int, float)):
        return None
    try:
        return format_physical_quantity(
            PhysicalQuantity(kind, float(raw)),
            unit=unit or None,
            precision=2,
        )
    except (TypeError, ValueError):
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


def human_location_detail_text(
    conn: sqlite3.Connection,
    value: dict[str, Any],
    *,
    location_profile: dict[str, Any] | None = None,
) -> str:
    identity = value.get("identity") or {}
    props = value.get("properties") or {}
    derived: dict[str, Any] = {}
    if location_profile is not None:
        source = location_profile.get("source") or {}
        identity = source.get("identity") or identity
        props = {
            key: source.get(key)
            for key in (
                "structure", "geography", "spatial", "boundary", "access", "operations",
                "topology", "facilities", "environment", "control", "economic_policy",
            )
        }
        derived = location_profile.get("derived") or {}

    structure = props.get("structure") or {}
    geography = props.get("geography") or {}
    spatial = props.get("spatial") or {}
    boundary = props.get("boundary") or {}
    access = props.get("access") or {}
    operations = props.get("operations") or {}
    topology = props.get("topology") or {}
    environment = props.get("environment") or {}
    control = props.get("control") or {}
    facilities = props.get("facilities") or {}
    economic = props.get("economic_policy")

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
    position = geography.get("position") if isinstance(geography.get("position"), dict) else None
    if any((parent, locality, region, country, address, position)):
        lines.extend(["", "🧭 LOCATION"])
        if parent:
            lines.append(f"↳ Parent: {parent}")
        _append(lines, "Address", address, icon="📌")
        _append(lines, "Locality", locality, icon="🏙")
        _append(lines, "Region", region, icon="🗺")
        _append(lines, "Country", country, icon="🌐")
        if position:
            lat = position.get("latitude")
            lon = position.get("longitude")
            if isinstance(lat, (int, float)) and not isinstance(lat, bool) and isinstance(lon, (int, float)) and not isinstance(lon, bool):
                lines.append(f"📌 Position: {float(lat):.6f}, {float(lon):.6f}")

    physical_rows: list[str] = []
    for label, key in (("Area", "area"), ("Length", "length"), ("Width", "width"), ("Height", "height"), ("Elevation", "elevation")):
        rendered = _quantity(spatial.get(key))
        if rendered:
            physical_rows.append(f"• {label}: {rendered}")
    surface = _text(spatial.get("surface"))
    enclosure = _text(boundary.get("enclosure"))
    boundary_type = _text(boundary.get("type"))
    terrain = _text(spatial.get("terrain"))
    if physical_rows or surface or enclosure or boundary_type or terrain:
        lines.extend(["", "📐 PHYSICAL"])
        lines.extend(physical_rows)
        if surface:
            lines.append(f"• Surface: {surface}")
        if terrain:
            lines.append(f"• Terrain: {terrain}")
        if enclosure:
            lines.append(f"• Enclosure: {enclosure}")
        if boundary_type:
            lines.append(f"• Boundary: {boundary_type}")

    mode = _text((access.get("policy") or {}).get("mode"))
    initial_state = _text(operations.get("initial_state"))
    owner = _target_name(conn, control.get("owner_ref"))
    operator = _target_name(conn, control.get("operator_ref"))
    ownership = _text(control.get("ownership_class"))
    if mode or initial_state or owner or operator or ownership:
        lines.extend(["", "🔐 ACCESS & CONTROL"])
        if mode:
            lines.append(f"• Access: {mode}")
        if initial_state:
            lines.append(f"• Initial state: {initial_state}")
        if owner:
            lines.append(f"• Owner: {owner}")
        if operator:
            lines.append(f"• Operator: {operator}")
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
    resources = [str(v).replace("_", " ").title() for v in facilities.get("resource_types") or [] if str(v).strip()]
    utilities = [str(v).replace("_", " ").title() for v in facilities.get("utilities") or [] if str(v).strip()]
    if facility_types or capabilities or resources or utilities:
        lines.extend(["", "🏗 FACILITIES"])
        if facility_types:
            lines.append("• Types: " + ", ".join(facility_types))
        if capabilities:
            lines.append("• Capabilities: " + ", ".join(capabilities))
        if resources:
            lines.append("• Resources: " + ", ".join(resources))
        if utilities:
            lines.append("• Utilities: " + ", ".join(utilities))

    interfaces = topology.get("interfaces") if isinstance(topology.get("interfaces"), list) else []
    if interfaces:
        lines.extend(["", "🔗 TOPOLOGY"])
        for interface in interfaces:
            if not isinstance(interface, dict):
                continue
            label = str(interface.get("name") or interface.get("key") or "Interface")
            kind_label = _text(interface.get("kind")) or "Interface"
            destination = _target_name(conn, interface.get("destination_ref")) or "Unassigned"
            direction = _text(interface.get("directionality")) or "—"
            enabled = "Enabled" if interface.get("enabled") else "Disabled"
            lines.append(f"• {label} · {kind_label} · {enabled}")
            lines.append(f"  → {destination} · {direction}")
            modes = [str(v).replace("_", " ").title() for v in interface.get("traversal_modes") or []]
            extras: list[str] = []
            if modes:
                extras.append("Modes: " + ", ".join(modes))
            duration = interface.get("base_duration_minutes")
            if isinstance(duration, (int, float)) and not isinstance(duration, bool):
                extras.append(f"Base: {float(duration):g} min")
            distance = _quantity(interface.get("distance"))
            if distance:
                extras.append(f"Distance: {distance}")
            if extras:
                lines.append("  " + " · ".join(extras))

    if isinstance(economic, dict):
        classification = _text(economic.get("classification"))
        treatment = _text(economic.get("net_worth_treatment"))
        currency = str(economic.get("currency_code") or "").strip().upper() or None
        market = economic.get("market_value_minor")
        replacement = economic.get("replacement_value_minor")
        parent_value = _target_name(conn, economic.get("included_in_parent_ref"))
        if any((classification, treatment, currency, market is not None, replacement is not None, parent_value)):
            lines.extend(["", "💰 ECONOMICS"])
            if classification:
                lines.append(f"• Classification: {classification}")
            if treatment:
                lines.append(f"• Net-worth treatment: {treatment}")
            if currency:
                lines.append(f"• Currency: {currency}")
            if isinstance(market, int) and not isinstance(market, bool):
                lines.append(f"• Market value: {market:,} minor units")
            if isinstance(replacement, int) and not isinstance(replacement, bool):
                lines.append(f"• Replacement value: {replacement:,} minor units")
            if parent_value:
                lines.append(f"• Included in parent: {parent_value}")

    completeness = derived.get("completeness_grade") if isinstance(derived.get("completeness_grade"), dict) else None
    level = str(derived.get("completeness_level") or "").strip()
    if completeness:
        grade = str(completeness.get("grade") or "—")
        grade_label = str(completeness.get("label") or "").strip()
        lines.extend(["", "📊 LOCATION GRADE PROFILE"])
        lines.append(f"• Completeness: {grade}{' · ' + grade_label if grade_label else ''}{' · ' + level if level else ''}")
        lines.append("• Overall: Not defined")

    relations = location_profile.get("resolved_relations") if location_profile is not None else value.get("resolved_relations")
    relations = relations or []
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
        profile = get_sandbox_location_v2(conn, object_id)
        return human_location_detail_text(conn, value, location_profile=profile), [
            [{"text": "← Locations", "callback_data": "sw:list:location"}],
            [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
            [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
        ]

    base.sandbox_object_view = sandbox_object_view


__all__ = ["human_location_detail_text", "install_location_world_layers_extension"]

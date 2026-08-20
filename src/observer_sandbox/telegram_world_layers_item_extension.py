from __future__ import annotations

import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID, ensure_sandbox, get_sandbox_object, list_sandbox_objects
from .item_grading import item_grading_lines
from .item_metric_ui import item_metric_lines
from .sandbox_item_creation import get_sandbox_item
from .sandbox_runtime import sandbox_runtime_status
from .telegram_economy import format_money_minor


def _fmt_number(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def _qty(value: Any) -> str:
    if not isinstance(value, dict):
        return "—"
    raw = value.get("value")
    unit = value.get("unit")
    if raw is None or unit is None:
        return "—"
    return f"{_fmt_number(raw)} {unit}"


def _target_name(conn: sqlite3.Connection, target_id: str) -> str:
    try:
        target = get_sandbox_object(conn, target_id)
    except Exception:
        return str(target_id)
    return str(target.get("identity", {}).get("name") or target_id)


def _relations_by_type(conn: sqlite3.Connection, value: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for relation in value.get("resolved_relations") or []:
        relation_type = str(relation.get("relation_type") or "")
        target_id = str(relation.get("target_object_id") or "")
        if relation_type and target_id:
            result[relation_type] = _target_name(conn, target_id)
    return result


def _stock_value_minor(unit_value_minor: int, unit_quantity: float, quantity: float) -> int:
    return int(round(float(quantity) / float(unit_quantity) * int(unit_value_minor)))


def _economic_lines(item: dict[str, Any]) -> list[str]:
    economic = item.get("economic_policy") or {}
    classification = str(economic.get("classification") or "")
    treatment = str(economic.get("net_worth_treatment") or "")
    currency = economic.get("currency_code")
    instance = item.get("instance") or {}
    lines = ["", "💰 ECONOMIC VALUE"]

    if classification == "standalone_asset":
        market = economic.get("market_value_minor")
        replacement = economic.get("replacement_value_minor")
        if market is not None and currency:
            lines.append(f"💵 Market value      {format_money_minor(int(market), str(currency))}")
        if replacement is not None and currency:
            lines.append(f"♻️ Replacement value {format_money_minor(int(replacement), str(currency))}")
        if len(lines) == 2:
            lines.append("⚠️ Value not assigned to this approved Sandbox Item.")
        return lines

    if classification == "consumable_stock":
        unit_value = economic.get("unit_value_minor")
        unit_quantity = economic.get("unit_quantity")
        unit_label = economic.get("unit_label")
        quantity = instance.get("quantity")
        if unit_value is not None and unit_quantity is not None and quantity is not None and currency:
            stock = _stock_value_minor(int(unit_value), float(unit_quantity), float(quantity))
            lines.append(f"💵 Current stock  {format_money_minor(stock, str(currency))}")
            lines.append(
                f"🏷 Unit value     {format_money_minor(int(unit_value), str(currency))} / "
                f"{_fmt_number(unit_quantity)} {unit_label or instance.get('unit') or 'unit'}"
            )
        else:
            lines.append("⚠️ Value not assigned to this approved Sandbox Item.")
        return lines

    if classification == "component" and treatment == "included_in_parent":
        lines.append("🧩 Value treatment  Included in parent value")
        return lines
    if classification == "resource_proxy":
        lines.append("ℹ️ Value treatment  Resource proxy; no independent monetary value")
        return lines

    lines.append("⚠️ Value not assigned to this approved Sandbox Item.")
    return lines


def _nutrition_lines(modules: dict[str, Any]) -> list[str]:
    nutrition = modules.get("nutrition")
    if not isinstance(nutrition, dict):
        return []
    basis = nutrition.get("basis_quantity")
    unit = nutrition.get("unit") or "unit"
    return [
        "",
        "🥗 NUTRIENT FACTS · DEFAULT PORTION",
        f"🍽 Serving     {_fmt_number(basis)} {unit}" if basis is not None else "🍽 Serving     —",
        f"🔥 Energy      {_fmt_number(nutrition.get('energy_kcal'))} kcal" if nutrition.get("energy_kcal") is not None else "🔥 Energy      —",
        f"🥩 Protein     {_fmt_number(nutrition.get('protein_g'))} g" if nutrition.get("protein_g") is not None else "🥩 Protein     —",
        f"🌾 Carbs       {_fmt_number(nutrition.get('carbohydrate_g'))} g" if nutrition.get("carbohydrate_g") is not None else "🌾 Carbs       —",
        f"🥑 Fat         {_fmt_number(nutrition.get('fat_g'))} g" if nutrition.get("fat_g") is not None else "🥑 Fat         —",
        f"📐 Basis       {_fmt_number(basis)} {unit}" if basis is not None else "📐 Basis       —",
    ]


def _physical_lines(modules: dict[str, Any]) -> list[str]:
    physical = modules.get("physical")
    if not isinstance(physical, dict):
        return []
    lines = ["", "📐 PHYSICAL"]
    mass = physical.get("mass")
    if isinstance(mass, dict):
        lines.append(f"⚖️ Mass        {_qty(mass)}")
    dimensions = [physical.get("length"), physical.get("width"), physical.get("height")]
    if all(isinstance(value, dict) for value in dimensions):
        typed_dimensions = [value for value in dimensions if isinstance(value, dict)]
        units = [str(value.get("unit")) for value in typed_dimensions]
        if len(set(units)) == 1:
            values = " × ".join(_fmt_number(value.get("value")) for value in typed_dimensions)
            lines.append(f"📏 Size        {values} {units[0]}")
        else:
            lines.append("📏 Size        " + " × ".join(_qty(value) for value in typed_dimensions))
    else:
        for label, value in zip(("Length", "Width", "Height"), dimensions):
            if isinstance(value, dict):
                lines.append(f"📏 {label:<10} {_qty(value)}")
    return lines if len(lines) > 2 else []


def _special_module_lines(modules: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    container = modules.get("container")
    if isinstance(container, dict) and isinstance(container.get("capacity_volume"), dict):
        lines.extend(["", "📦 STORAGE", f"🫙 Capacity     {_qty(container['capacity_volume'])}"])
    resistance = modules.get("resistance_training")
    if isinstance(resistance, dict) and isinstance(resistance.get("resistance_load"), dict):
        lines.extend(["", "🏋️ TRAINING", f"⚖️ Resistance   {_qty(resistance['resistance_load'])}"])
    return lines


def approved_item_detail_text(conn: sqlite3.Connection, value: dict[str, Any]) -> str:
    item = value["item"]
    definition = item["definition"]
    instance = item["instance"]
    modules = definition.get("modules") or {}
    relations = _relations_by_type(conn, value)
    quantity = (
        f"{_fmt_number(instance.get('quantity'))} {instance.get('unit')}"
        if instance.get("mode") == "stack" and instance.get("quantity") is not None
        else "1 item"
    )
    kind = str(definition.get("kind") or "item").replace("_", " ").title()
    lifecycle = str(value.get("lifecycle_status") or "active").title()

    lines = [
        f"📦 {definition.get('name', value.get('object_id', 'Item'))}",
        "━━━━━━━━━━━━━━━━━━",
        f"🧪 Creation Sandbox · {lifecycle}",
        "",
        f"📏 Quantity    {quantity}",
        f"🧬 Definition  {definition.get('key', '—')}",
    ]
    if relations.get("stored_in"):
        lines.append(f"📦 Container   {relations['stored_in']}")
    if relations.get("owned_by"):
        lines.append(f"🏷 Owner       {relations['owned_by']}")
    lines.extend([
        f"🧭 Mobility    {str(definition.get('mobility', '—')).replace('_', ' ').title()}",
        f"🗂 Kind        {kind}",
    ])
    if relations.get("located_at"):
        lines.append(f"📍 Location    {relations['located_at']}")
    if relations.get("carried_by"):
        lines.append(f"🎒 Carried by  {relations['carried_by']}")
    if relations.get("equipped_by"):
        lines.append(f"🧷 Equipped by {relations['equipped_by']}")

    description = str(definition.get("description") or "").strip()
    if description:
        lines.extend(["", description])

    lines.extend(_economic_lines(item))
    lines.extend(_nutrition_lines(modules))
    lines.extend(_physical_lines(modules))
    lines.extend(_special_module_lines(modules))
    metrics = item_metric_lines(modules, heading="⚙️ PERFORMANCE METRICS")
    if metrics:
        lines.extend(["", *metrics])
    lines.extend(["", *item_grading_lines(item, heading="🏅 GRADING")])
    lines.extend(["", "🧪 Sandbox-only item · canonical universe unchanged."])
    return "\n".join(lines)


def install_item_world_layers_extension(base) -> None:
    original_list_view = base.sandbox_list_view
    original_object_view = base.sandbox_object_view
    original_callback = base.world_layer_callback_view

    def sandbox_world_view(conn: sqlite3.Connection):
        sandbox = ensure_sandbox(conn, DEFAULT_SANDBOX_ID)
        objects = list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
        characters = sum(value["creation_type"] == "character" for value in objects)
        locations = sum(value["creation_type"] == "location" for value in objects)
        items = sum(value["creation_type"] == "item" for value in objects)
        runtime = sandbox_runtime_status(conn, DEFAULT_SANDBOX_ID)
        runtime_label = "Not configured" if not runtime["configured"] else (
            f"{'Paused' if runtime['paused'] else 'Active'} · {runtime['speed']:g}x"
        )
        text = (
            "🧪 SANDBOX WORLD\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "Creation Sandbox · isolated from the canonical universe.\n\n"
            f"Revision: {sandbox['revision']}\n"
            f"Objects: {len(objects)} · Characters: {characters} · Locations: {locations} · Items: {items}\n"
            f"Runtime: {runtime_label}\n"
            "Canonical universe: unchanged by sandbox-only operations."
        )
        keyboard = [
            [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
            [
                {"text": "🌐 Universe", "callback_data": "sw:universe"},
                {"text": "👥 Characters", "callback_data": "sw:list:character"},
            ],
            [
                {"text": "📍 Locations", "callback_data": "sw:list:location"},
                {"text": "📦 Items", "callback_data": "sw:list:item"},
            ],
            [
                {"text": "🕒 Runtime", "callback_data": "sw:runtime"},
                {"text": "📜 History", "callback_data": "sw:history"},
            ],
            [{"text": "📡 Observer", "callback_data": "sw:notif"}],
            [{"text": "← Observer Home", "callback_data": "nav:home"}],
        ]
        return text, keyboard

    def sandbox_universe_view(conn: sqlite3.Connection):
        objects = list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
        icons = {"character": "👤", "location": "📍", "item": "📦"}
        lines = ["🌐 SANDBOX UNIVERSE", "━━━━━━━━━━━━━━━━━━", "Isolated staging namespace. Nothing here is canonical."]
        if not objects:
            lines.extend(["", "No sandbox creations yet."])
        else:
            lines.extend(["", "Active creations"])
            for value in objects:
                icon = icons.get(str(value["creation_type"]), "•")
                lines.append(f"• {icon} {value['identity'].get('name', value['object_id'])}")
        return "\n".join(lines), [[{"text": "← Sandbox World", "callback_data": "nav:sandbox"}]]

    def sandbox_list_view(conn: sqlite3.Connection, creation_type: str):
        if creation_type != "item":
            return original_list_view(conn, creation_type)
        values = [
            value for value in list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
            if value["creation_type"] == "item"
        ]
        lines = ["📦 SANDBOX ITEMS", "━━━━━━━━━━━━━━━━━━"]
        keyboard: list[list[dict[str, str]]] = []
        if not values:
            lines.append("No active Sandbox Items.")
        for value in values:
            name = str(value["identity"].get("name") or value["object_id"])
            lines.append(f"• {name}")
            keyboard.append([{"text": f"📦 {name}"[:60], "callback_data": f"sw:o:{value['object_id']}"}])
        keyboard.extend([
            [{"text": "➕ Create Item", "callback_data": "sw:cs:type:item"}],
            [{"text": "← Sandbox World", "callback_data": "nav:sandbox"}],
        ])
        return "\n".join(lines), keyboard

    def sandbox_object_view(conn: sqlite3.Connection, object_id: str):
        basic = get_sandbox_object(conn, object_id)
        if basic["creation_type"] != "item":
            return original_object_view(conn, object_id)
        value = get_sandbox_item(conn, object_id)
        return approved_item_detail_text(conn, value), [
            [{"text": "← Items", "callback_data": "sw:list:item"}],
            [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
            [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
        ]

    def world_layer_callback_view(conn: sqlite3.Connection, callback_data: str):
        if callback_data == "nav:sandbox":
            return sandbox_world_view(conn)
        if callback_data == "sw:universe":
            return sandbox_universe_view(conn)
        if callback_data == "sw:list:item":
            return sandbox_list_view(conn, "item")
        return original_callback(conn, callback_data)

    base.sandbox_world_view = sandbox_world_view
    base.sandbox_universe_view = sandbox_universe_view
    base.sandbox_list_view = sandbox_list_view
    base.sandbox_object_view = sandbox_object_view
    base.world_layer_callback_view = world_layer_callback_view


__all__ = ["approved_item_detail_text", "install_item_world_layers_extension"]

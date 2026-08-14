from __future__ import annotations

import sqlite3
from typing import Any

from .creator_control import replenish_inventory_stack
from .inventory import all_inventory_stacks, inventory_for_entity, list_inventory_scopes, stack_state
from .nutrition_facts import nutrition_facts_for_definition
from .world import get_field

PAGE_SIZE = 8


def _fmt_number(value: float) -> str:
    number = float(value)
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.2f}".rstrip("0").rstrip(".")


def _entity_name(conn: sqlite3.Connection, entity_id: str | None) -> str:
    if not entity_id:
        return "None"
    row = conn.execute("SELECT name FROM entities WHERE id=?", (entity_id,)).fetchone()
    return str(row[0]) if row is not None else str(entity_id)


def _inventory_home() -> tuple[str, list[list[dict[str, str]]]]:
    return (
        "🎒 INVENTORY\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Browse inventory anywhere in the universe.\n\n"
        "Choose a scope:",
        [
            [
                {"text": "📍 Locations", "callback_data": "inv:list:locations:0"},
                {"text": "👥 Characters", "callback_data": "inv:list:characters:0"},
            ],
            [
                {"text": "📦 Containers", "callback_data": "inv:list:containers:0"},
                {"text": "🧺 All Stocks", "callback_data": "inv:all:0"},
            ],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ],
    )


def _paged_scope_list(
    conn: sqlite3.Connection,
    scope_type: str,
    page: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    rows = list_inventory_scopes(conn, scope_type)
    page = max(0, int(page))
    start = page * PAGE_SIZE
    shown = rows[start : start + PAGE_SIZE]
    labels = {"locations": "LOCATIONS", "characters": "CHARACTERS", "containers": "CONTAINERS"}
    icons = {"locations": "📍", "characters": "👤", "containers": "📦"}
    lines = [f"🎒 INVENTORY · {labels[scope_type]}", "━━━━━━━━━━━━━━━━━━"]
    if not shown:
        lines.append("No matching inventory scopes.")
    keyboard: list[list[dict[str, str]]] = []
    for row in shown:
        count = int(row["stack_count"])
        lines.append(f"• {row['name']} · {count} stock{'s' if count != 1 else ''}")
        keyboard.append([
            {
                "text": f"{icons[scope_type]} {row['name']} · {count}",
                "callback_data": f"inv:scope:{row['id']}",
            }
        ])
    nav: list[dict[str, str]] = []
    if page > 0:
        nav.append({"text": "← Previous", "callback_data": f"inv:list:{scope_type}:{page-1}"})
    if start + PAGE_SIZE < len(rows):
        nav.append({"text": "Next →", "callback_data": f"inv:list:{scope_type}:{page+1}"})
    if nav:
        keyboard.append(nav)
    keyboard.extend([
        [{"text": "← Inventory", "callback_data": "inv:home"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _scope_view(conn: sqlite3.Connection, entity_id: str) -> tuple[str, list[list[dict[str, str]]]]:
    data = inventory_for_entity(conn, entity_id)
    scope = data["scope"]
    stacks = data["stacks"]
    containers = data["containers"]
    type_label = str(scope["type"]).replace("_", " ").title()
    lines = [f"🎒 {scope['name']}", "━━━━━━━━━━━━━━━━━━", f"🧭 Scope   {type_label}"]
    if containers:
        lines.extend(["", "📦 Related containers"])
        for container in containers[:8]:
            mobility = str(container.get("mobility") or "unknown").replace("_", " ").title()
            lines.append(f"• {container['name']} · {mobility}")
        if len(containers) > 8:
            lines.append(f"• +{len(containers)-8} more")
    lines.extend(["", "🧺 Stocks"])
    if not stacks:
        lines.append("• No inventory currently related to this scope.")
    else:
        for stack in stacks[:12]:
            lines.append(f"• {stack.name}: {_fmt_number(stack.quantity)} {stack.unit}")
        if len(stacks) > 12:
            lines.append(f"• +{len(stacks)-12} more")

    keyboard: list[list[dict[str, str]]] = []
    for stack in stacks[:12]:
        keyboard.append([
            {
                "text": f"🧺 {stack.name} · {_fmt_number(stack.quantity)} {stack.unit}",
                "callback_data": f"inv:stack:{stack.entity_id}",
            }
        ])
    keyboard.extend([
        [{"text": "← Inventory", "callback_data": "inv:home"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _all_stocks(conn: sqlite3.Connection, page: int) -> tuple[str, list[list[dict[str, str]]]]:
    rows = all_inventory_stacks(conn)
    page = max(0, int(page))
    start = page * PAGE_SIZE
    shown = rows[start : start + PAGE_SIZE]
    lines = ["🧺 ALL UNIVERSE STOCKS", "━━━━━━━━━━━━━━━━━━"]
    keyboard: list[list[dict[str, str]]] = []
    if not shown:
        lines.append("No active stock stacks.")
    for stack in shown:
        owner = _entity_name(conn, stack.owner_id)
        container = _entity_name(conn, stack.container_id)
        lines.append(f"• {stack.name}: {_fmt_number(stack.quantity)} {stack.unit}")
        lines.append(f"  ↳ {owner} · {container}")
        keyboard.append([
            {
                "text": f"🧺 {stack.name} · {_fmt_number(stack.quantity)} {stack.unit}",
                "callback_data": f"inv:stack:{stack.entity_id}",
            }
        ])
    nav: list[dict[str, str]] = []
    if page > 0:
        nav.append({"text": "← Previous", "callback_data": f"inv:all:{page-1}"})
    if start + PAGE_SIZE < len(rows):
        nav.append({"text": "Next →", "callback_data": f"inv:all:{page+1}"})
    if nav:
        keyboard.append(nav)
    keyboard.extend([
        [{"text": "← Inventory", "callback_data": "inv:home"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _stack_view(
    conn: sqlite3.Connection,
    stack_id: str,
    *,
    is_owner: bool,
) -> tuple[str, list[list[dict[str, str]]]]:
    stack = stack_state(conn, stack_id)
    container_name = _entity_name(conn, stack.container_id)
    owner_name = _entity_name(conn, stack.owner_id)
    mobility = None
    kind = None
    if stack.container_id:
        mobility = get_field(conn, stack.container_id, "inventory.container_mobility", None)
        kind = get_field(conn, stack.container_id, "inventory.container_kind", None)
    lines = [
        f"🧺 {stack.name}",
        "━━━━━━━━━━━━━━━━━━",
        f"📏 Quantity    {_fmt_number(stack.quantity)} {stack.unit}",
        f"🧬 Definition  {stack.definition_id}",
        f"📦 Container   {container_name}",
        f"🏷 Owner       {owner_name}",
    ]
    if mobility:
        lines.append(f"🧭 Mobility    {str(mobility).replace('_', ' ').title()}")
    if kind:
        lines.append(f"🗃 Storage     {str(kind).replace('_', ' ').title()}")

    nutrition = nutrition_facts_for_definition(stack.definition_id)
    if nutrition is not None:
        lines.extend([
            "",
            "🥗 NUTRIENT FACTS · DEFAULT PORTION",
            f"🍽 Serving     {_fmt_number(nutrition['quantity'])} {nutrition['unit']}",
            f"🔥 Energy      {_fmt_number(nutrition['energy_kcal'])} kcal",
            f"🥩 Protein     {_fmt_number(nutrition['protein_g'])} g",
            f"🌾 Carbs       {_fmt_number(nutrition['carbohydrate_g'])} g",
            f"🥑 Fat         {_fmt_number(nutrition['fat_g'])} g",
            f"📐 Basis       {_fmt_number(nutrition['basis_quantity'])} {nutrition['unit']}",
        ])

    keyboard: list[list[dict[str, str]]] = []
    if is_owner:
        keyboard.append([{"text": "➕ Replenish Stock", "callback_data": f"inv:replenish:{stack_id}"}])
    keyboard.extend([
        [{"text": "← Inventory", "callback_data": "inv:home"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _replenish_presets(unit: str) -> list[float]:
    if unit == "piece":
        return [12.0, 24.0, 60.0]
    if unit in {"g", "ml"}:
        return [500.0, 2000.0, 10000.0]
    return [1.0, 5.0, 10.0]


def _replenish_view(conn: sqlite3.Connection, stack_id: str) -> tuple[str, list[list[dict[str, str]]]]:
    stack = stack_state(conn, stack_id)
    lines = [
        f"➕ REPLENISH {stack.name.upper()}",
        "━━━━━━━━━━━━━━━━━━",
        f"Current: {_fmt_number(stack.quantity)} {stack.unit}",
        "Creator authority required.",
        "Choose an amount to add:",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for amount in _replenish_presets(stack.unit):
        keyboard.append([
            {
                "text": f"+{_fmt_number(amount)} {stack.unit}",
                "callback_data": f"inv:addprompt:{stack_id}:{_fmt_number(amount)}",
            }
        ])
    keyboard.extend([
        [{"text": "← Item", "callback_data": f"inv:stack:{stack_id}"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _replenish_prompt(
    conn: sqlite3.Connection,
    stack_id: str,
    amount: float,
) -> tuple[str, list[list[dict[str, str]]]]:
    stack = stack_state(conn, stack_id)
    after = stack.quantity + amount
    return (
        "⚠️ CONFIRM INVENTORY CHANGE\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"Item: {stack.name}\n"
        f"Current: {_fmt_number(stack.quantity)} {stack.unit}\n"
        f"Add: +{_fmt_number(amount)} {stack.unit}\n"
        f"After: {_fmt_number(after)} {stack.unit}\n\n"
        "This is a Creator administrative intervention and will be audited.",
        [
            [{"text": "✅ Confirm Replenish", "callback_data": f"inv:addapply:{stack_id}:{_fmt_number(amount)}"}],
            [{"text": "← Cancel", "callback_data": f"inv:stack:{stack_id}"}],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ],
    )


def _replenish_result(result: dict[str, Any]) -> tuple[str, list[list[dict[str, str]]]]:
    return (
        "✅ INVENTORY REPLENISHED\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🧺 {result['item_name']}\n"
        f"➕ Added      {_fmt_number(result['added_quantity'])} {result['unit']}\n"
        f"📏 Before     {_fmt_number(result['before_quantity'])} {result['unit']}\n"
        f"📏 After      {_fmt_number(result['after_quantity'])} {result['unit']}\n\n"
        "Audit event recorded.",
        [
            [{"text": "← Item", "callback_data": f"inv:stack:{result['stack_id']}"}],
            [{"text": "← Inventory", "callback_data": "inv:home"}],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ],
    )


def inventory_callback_view(
    conn: sqlite3.Connection,
    callback_data: str,
    *,
    role: str,
    requested_by: str,
) -> tuple[str, list[list[dict[str, str]]] | None] | None:
    if callback_data == "inv:home":
        return _inventory_home()
    if callback_data.startswith("inv:list:"):
        _, _, scope_type, page_raw = callback_data.split(":", 3)
        if scope_type not in {"locations", "characters", "containers"}:
            return None
        return _paged_scope_list(conn, scope_type, int(page_raw))
    if callback_data.startswith("inv:scope:"):
        return _scope_view(conn, callback_data.split(":", 2)[2])
    if callback_data.startswith("inv:all:"):
        return _all_stocks(conn, int(callback_data.split(":", 2)[2]))
    if callback_data.startswith("inv:stack:"):
        return _stack_view(conn, callback_data.split(":", 2)[2], is_owner=role == "owner")
    if callback_data.startswith("inv:replenish:"):
        stack_id = callback_data.split(":", 2)[2]
        if role != "owner":
            return "🔒 Creator authority required for inventory replenishment.", [[{"text": "← Inventory", "callback_data": "inv:home"}]]
        return _replenish_view(conn, stack_id)
    if callback_data.startswith("inv:addprompt:"):
        if role != "owner":
            return "🔒 Creator authority required for inventory replenishment.", [[{"text": "← Inventory", "callback_data": "inv:home"}]]
        _, _, stack_id, amount_raw = callback_data.split(":", 3)
        amount = float(amount_raw)
        if amount <= 0.0:
            raise ValueError("Replenishment quantity must be positive")
        return _replenish_prompt(conn, stack_id, amount)
    if callback_data.startswith("inv:addapply:"):
        if role != "owner":
            return "🔒 Creator authority required for inventory replenishment.", [[{"text": "← Inventory", "callback_data": "inv:home"}]]
        _, _, stack_id, amount_raw = callback_data.split(":", 3)
        result = replenish_inventory_stack(
            conn,
            stack_id,
            float(amount_raw),
            authority="creator",
            requested_by=requested_by,
        )
        return _replenish_result(result)
    return None


def inventory_command_view(conn: sqlite3.Connection) -> str:
    stacks = all_inventory_stacks(conn)
    return (
        "🎒 INVENTORY\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"Active stock stacks: {len(stacks)}\n"
        "Use /start → Inventory to browse Locations, Characters, Containers, or all universe stocks."
    )

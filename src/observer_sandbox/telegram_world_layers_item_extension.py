from __future__ import annotations

import sqlite3

from .creation_sandbox import DEFAULT_SANDBOX_ID, ensure_sandbox, get_sandbox_object, list_sandbox_objects
from .sandbox_item_creation import get_sandbox_item
from .sandbox_runtime import sandbox_runtime_status


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
        item = value["item"]
        definition = item["definition"]
        instance = item["instance"]
        economic = item.get("economic_policy") or {}
        modules = definition.get("modules") or {}
        capabilities = definition.get("capabilities") or []
        lines = [
            f"📦 {definition.get('name', object_id)}",
            "━━━━━━━━━━━━━━━━━━",
            "🧪 Creation Sandbox",
            f"Lifecycle: {str(value.get('lifecycle_status', 'active')).title()}",
            f"ID: {object_id}",
            "",
            f"Kind: {str(definition.get('kind', '—')).replace('_', ' ').title()}",
            f"Mobility: {str(definition.get('mobility', '—')).title()}",
            f"Definition: {definition.get('key', '—')}",
            str(definition.get("description") or "No description."),
            "",
            f"Instance: {instance.get('mode', '—')}" + (
                f" · {instance.get('quantity'):g} {instance.get('unit')}" if instance.get("mode") == "stack" and isinstance(instance.get("quantity"), (int, float)) else ""
            ),
            f"Capabilities: {', '.join(str(v) for v in capabilities) if capabilities else '—'}",
            f"Modules: {', '.join(sorted(str(v) for v in modules)) if modules else '—'}",
            f"Economics: {str(economic.get('classification', '—')).replace('_', ' ')} / {str(economic.get('net_worth_treatment', '—')).replace('_', ' ')}",
        ]
        relations = value.get("resolved_relations") or []
        if relations:
            lines.extend(["", "Sandbox relations"])
            for relation in relations:
                lines.append(f"• {str(relation['relation_type']).replace('_', ' ').title()} → {relation['target_object_id']}")
        lines.extend(["", "Canonical universe: unchanged."])
        return "\n".join(lines), [
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

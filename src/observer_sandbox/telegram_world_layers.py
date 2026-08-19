from __future__ import annotations

import json
import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID, ensure_sandbox, get_sandbox_object, list_sandbox_objects


def real_world_view() -> tuple[str, list[list[dict[str, str]]]]:
    return (
        "🌍 REAL WORLD\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Canonical universe observation and live runtime surfaces.",
        [
            [
                {"text": "🌍 Universe", "callback_data": "nav:universe"},
                {"text": "👥 Characters", "callback_data": "nav:characters"},
            ],
            [
                {"text": "🕒 Runtime", "callback_data": "nav:runtime"},
                {"text": "📜 History", "callback_data": "nav:history"},
            ],
            [{"text": "🎒 Inventory", "callback_data": "inv:home"}],
            [{"text": "← Observer Home", "callback_data": "nav:home"}],
        ],
    )


def _sandbox_counts(conn: sqlite3.Connection) -> tuple[int, int, int]:
    objects = list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
    characters = sum(value["creation_type"] == "character" for value in objects)
    locations = sum(value["creation_type"] == "location" for value in objects)
    return len(objects), characters, locations


def sandbox_world_view(conn: sqlite3.Connection) -> tuple[str, list[list[dict[str, str]]]]:
    sandbox = ensure_sandbox(conn, DEFAULT_SANDBOX_ID)
    total, characters, locations = _sandbox_counts(conn)
    text = (
        "🧪 SANDBOX WORLD\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Creation Sandbox · isolated from the canonical universe.\n\n"
        f"Revision: {sandbox['revision']}\n"
        f"Objects: {total} · Characters: {characters} · Locations: {locations}\n"
        "Canonical universe: unchanged by sandbox-only operations."
    )
    keyboard = [
        [
            {"text": "🌐 Universe", "callback_data": "sw:universe"},
            {"text": "👥 Characters", "callback_data": "sw:list:character"},
        ],
        [
            {"text": "📍 Locations", "callback_data": "sw:list:location"},
            {"text": "📜 History", "callback_data": "sw:history"},
        ],
        [{"text": "← Observer Home", "callback_data": "nav:home"}],
    ]
    return text, keyboard


def sandbox_universe_view(conn: sqlite3.Connection) -> tuple[str, list[list[dict[str, str]]]]:
    objects = list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
    lines = [
        "🌐 SANDBOX UNIVERSE",
        "━━━━━━━━━━━━━━━━━━",
        "Isolated staging namespace. Nothing here is canonical.",
    ]
    if not objects:
        lines.extend(["", "No sandbox creations yet."])
    else:
        lines.extend(["", "Active creations"])
        for value in objects:
            icon = "👤" if value["creation_type"] == "character" else "📍"
            lines.append(f"• {icon} {value['identity'].get('name', value['object_id'])}")
    return "\n".join(lines), [[{"text": "← Sandbox World", "callback_data": "nav:sandbox"}]]


def sandbox_list_view(
    conn: sqlite3.Connection,
    creation_type: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    if creation_type not in {"character", "location"}:
        return sandbox_world_view(conn)
    values = [
        value
        for value in list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
        if value["creation_type"] == creation_type
    ]
    label = "CHARACTERS" if creation_type == "character" else "LOCATIONS"
    icon = "👥" if creation_type == "character" else "📍"
    lines = [f"{icon} SANDBOX {label}", "━━━━━━━━━━━━━━━━━━"]
    keyboard: list[list[dict[str, str]]] = []
    if not values:
        lines.append("No active sandbox creations.")
    for value in values:
        name = str(value["identity"].get("name") or value["object_id"])
        lines.append(f"• {name}")
        keyboard.append([{"text": f"{'👤' if creation_type == 'character' else '📍'} {name}", "callback_data": f"sw:o:{value['object_id']}"}])
    keyboard.append([{"text": "← Sandbox World", "callback_data": "nav:sandbox"}])
    return "\n".join(lines), keyboard


def sandbox_object_view(
    conn: sqlite3.Connection,
    object_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    value = get_sandbox_object(conn, object_id)
    icon = "👤" if value["creation_type"] == "character" else "📍"
    lines = [
        f"{icon} {value['identity'].get('name', value['object_id'])}",
        "━━━━━━━━━━━━━━━━━━",
        "🧪 Creation Sandbox",
        f"Type: {value['creation_type'].title()}",
        f"Lifecycle: {value['lifecycle_status'].title()}",
        f"ID: {value['object_id']}",
    ]
    if value["properties"]:
        lines.extend(["", "Properties"])
        for key, item in sorted(value["properties"].items()):
            lines.append(f"• {key.replace('_', ' ').title()}: {item}")
    if value["resolved_relations"]:
        lines.extend(["", "Sandbox relations"])
        for relation in value["resolved_relations"]:
            lines.append(f"• {relation['relation_type'].replace('_', ' ').title()} → {relation['target_object_id']}")
    lines.extend(["", "Canonical universe: unchanged."])
    back = "sw:list:character" if value["creation_type"] == "character" else "sw:list:location"
    return "\n".join(lines), [[{"text": "← Back", "callback_data": back}], [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]]


def sandbox_history_view(conn: sqlite3.Connection) -> tuple[str, list[list[dict[str, str]]]]:
    ensure_sandbox(conn, DEFAULT_SANDBOX_ID)
    rows = conn.execute(
        """
        SELECT event_type,payload_json,created_at
        FROM creation_sandbox_events
        WHERE sandbox_id=?
        ORDER BY id DESC LIMIT 12
        """,
        (DEFAULT_SANDBOX_ID,),
    ).fetchall()
    lines = ["📜 SANDBOX HISTORY", "━━━━━━━━━━━━━━━━━━"]
    if not rows:
        lines.append("No sandbox activity yet.")
    for row in rows:
        event = str(row["event_type"]).replace("_", " ").title()
        payload: Any
        try:
            payload = json.loads(row["payload_json"] or "{}")
        except json.JSONDecodeError:
            payload = {}
        detail = ""
        if isinstance(payload, dict):
            detail = str(payload.get("name") or payload.get("creation_type") or "")
        lines.append(f"• {event}{' · ' + detail if detail else ''}")
        lines.append(f"  {row['created_at']}")
    lines.extend(["", "Canonical history is separate and unchanged."])
    return "\n".join(lines), [[{"text": "← Sandbox World", "callback_data": "nav:sandbox"}]]


def world_layer_callback_view(
    conn: sqlite3.Connection,
    callback_data: str,
) -> tuple[str, list[list[dict[str, str]]]] | None:
    if callback_data == "nav:real":
        return real_world_view()
    if callback_data == "nav:sandbox":
        return sandbox_world_view(conn)
    if callback_data == "sw:universe":
        return sandbox_universe_view(conn)
    if callback_data == "sw:list:character":
        return sandbox_list_view(conn, "character")
    if callback_data == "sw:list:location":
        return sandbox_list_view(conn, "location")
    if callback_data == "sw:history":
        return sandbox_history_view(conn)
    if callback_data.startswith("sw:o:"):
        return sandbox_object_view(conn, callback_data[5:])
    raise KeyError(callback_data)


__all__ = [
    "real_world_view",
    "sandbox_history_view",
    "sandbox_list_view",
    "sandbox_object_view",
    "sandbox_universe_view",
    "sandbox_world_view",
    "world_layer_callback_view",
]

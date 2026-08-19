from __future__ import annotations

import sqlite3
from typing import Any

from .creation_sandbox import (
    DEFAULT_SANDBOX_ID,
    bind_sandbox_character_to_location,
    get_sandbox_object,
    list_sandbox_objects,
)
from .sandbox_affordances import refresh_sandbox_runtime_options
from .sandbox_runtime import (
    bind_sandbox_character_ai,
    configure_sandbox_clock,
    sandbox_character_readiness,
)
from .simulation import runtime_value


class SandboxCharacterConfigError(ValueError):
    pass


def _require_character(conn: sqlite3.Connection, character_object_id: str) -> dict[str, Any]:
    character = get_sandbox_object(conn, character_object_id)
    if character["creation_type"] != "character" or character["lifecycle_status"] != "active":
        raise SandboxCharacterConfigError("Configuration target must be an active sandbox Character")
    return character


def _locations(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    return [
        value
        for value in list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
        if value["creation_type"] == "location" and value["lifecycle_status"] == "active"
    ]


def _providers(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT p.id,p.display_name,COUNT(m.model_id) AS model_count
        FROM ai_providers p
        JOIN ai_models m ON m.provider_id=p.id AND m.active=1
        WHERE p.enabled=1
        GROUP BY p.id,p.display_name
        ORDER BY lower(p.display_name),p.id
        """
    ).fetchall()
    return [dict(row) for row in rows]


def _models(conn: sqlite3.Connection, provider_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT model_id,display_name
        FROM ai_models
        WHERE provider_id=? AND active=1
        ORDER BY lower(display_name),model_id
        """,
        (provider_id,),
    ).fetchall()
    return [dict(row) for row in rows]


def _gate_line(passed: bool, label: str) -> str:
    return f"{'✅' if passed else '⚠️'} {label}"


def character_config_view(
    conn: sqlite3.Connection,
    character_object_id: str,
    *,
    notice: str | None = None,
) -> tuple[str, list[list[dict[str, str]]]]:
    character = _require_character(conn, character_object_id)
    readiness = sandbox_character_readiness(conn, character_object_id)
    binding = readiness["ai_binding"]
    runtime = readiness["runtime"]
    location_name = "Not assigned"
    if readiness["location_object_id"]:
        location = get_sandbox_object(conn, str(readiness["location_object_id"]))
        location_name = str(location["identity"].get("name") or location["object_id"])
    ai_name = "Not assigned"
    if binding:
        ai_name = f"{binding['provider_name']} · {binding['model_name']}"
    options = readiness["runtime_options"]
    lines = [
        "⚙️ SANDBOX CHARACTER CONFIG",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {character['identity'].get('name', character_object_id)}",
        f"State: {readiness['activation_status'].replace('_', ' ').title()}",
        "",
        _gate_line(readiness["gates"]["location_assigned"], f"Location · {location_name}"),
        _gate_line(readiness["gates"]["cognition_ai_bound"], f"Character AI · {ai_name}"),
        _gate_line(
            readiness["gates"]["runtime_options_available"],
            f"Runtime options · {len(options)} represented",
        ),
        _gate_line(
            readiness["gates"]["clock_configured"],
            f"Sandbox clock · {runtime['sim_time'] or 'Not configured'}",
        ),
        "",
        f"{'✅ RUNTIME READY' if readiness['ready'] else '⚠️ NOT RUNTIME READY'}",
        "Readiness never starts autonomy automatically.",
    ]
    if notice:
        lines.extend(["", notice])
    keyboard: list[list[dict[str, str]]] = [
        [{"text": "📍 Location", "callback_data": f"sw:cfg:l:{character_object_id}"}],
        [{"text": "🤖 Character AI", "callback_data": f"sw:cfg:a:{character_object_id}"}],
        [{"text": "🎛 Refresh Options", "callback_data": f"sw:cfg:o:{character_object_id}"}],
    ]
    if runtime["configured"]:
        keyboard.append([{"text": "🕒 Sandbox Runtime", "callback_data": "sw:runtime"}])
    else:
        keyboard.append([{"text": "🕒 Initialize Sandbox Clock", "callback_data": f"sw:cfg:t:{character_object_id}"}])
    keyboard.extend(
        [
            [{"text": "🧠 Readiness Details", "callback_data": f"sw:cr:{character_object_id}"}],
            [{"text": "← Character", "callback_data": f"sw:o:{character_object_id}"}],
            [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
        ]
    )
    return "\n".join(lines), keyboard


def location_picker_view(
    conn: sqlite3.Connection,
    character_object_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    character = _require_character(conn, character_object_id)
    values = _locations(conn)
    lines = [
        "📍 ASSIGN SANDBOX LOCATION",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {character['identity'].get('name', character_object_id)}",
        "Choose an active Location in this Creation Sandbox.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    if not values:
        lines.extend(["", "No active sandbox Locations exist yet. Create one in Creator Studio first."])
        keyboard.append([{"text": "➕ Creator Studio", "callback_data": "sw:studio"}])
    else:
        for index, value in enumerate(values):
            name = str(value["identity"].get("name") or value["object_id"])
            keyboard.append([{"text": f"📍 {name}", "callback_data": f"sw:cfg:ls:{character_object_id}:{index}"}])
    keyboard.append([{"text": "← Configuration", "callback_data": f"sw:cfg:{character_object_id}"}])
    return "\n".join(lines), keyboard


def ai_provider_view(
    conn: sqlite3.Connection,
    character_object_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    character = _require_character(conn, character_object_id)
    providers = _providers(conn)
    lines = [
        "🤖 ASSIGN CHARACTER AI",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {character['identity'].get('name', character_object_id)}",
        "Choose an enabled provider. This assignment belongs only to this sandbox Character.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    if not providers:
        lines.extend(["", "No enabled providers with active models are available."])
        keyboard.append([{"text": "⚙️ AI Settings", "callback_data": "ai:settings"}])
    else:
        for index, provider in enumerate(providers):
            keyboard.append([
                {
                    "text": f"{provider['display_name']} · {provider['model_count']} models",
                    "callback_data": f"sw:cfg:ap:{character_object_id}:{index}",
                }
            ])
    keyboard.append([{"text": "← Configuration", "callback_data": f"sw:cfg:{character_object_id}"}])
    return "\n".join(lines), keyboard


def ai_model_view(
    conn: sqlite3.Connection,
    character_object_id: str,
    provider_index: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    character = _require_character(conn, character_object_id)
    providers = _providers(conn)
    if provider_index < 0 or provider_index >= len(providers):
        raise SandboxCharacterConfigError("AI provider selection is stale; reopen Character AI")
    provider = providers[provider_index]
    models = _models(conn, str(provider["id"]))
    lines = [
        "🤖 CHOOSE CHARACTER MODEL",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {character['identity'].get('name', character_object_id)}",
        f"Provider: {provider['display_name']}",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for model_index, model in enumerate(models):
        keyboard.append([
            {
                "text": str(model["display_name"]),
                "callback_data": f"sw:cfg:am:{character_object_id}:{provider_index}:{model_index}",
            }
        ])
    keyboard.append([{"text": "← Providers", "callback_data": f"sw:cfg:a:{character_object_id}"}])
    return "\n".join(lines), keyboard


def character_config_callback_view(
    conn: sqlite3.Connection,
    callback_data: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    if callback_data.startswith("sw:cfg:ls:"):
        _, _, _, character_id, raw_index = callback_data.split(":", 4)
        values = _locations(conn)
        index = int(raw_index)
        if index < 0 or index >= len(values):
            raise SandboxCharacterConfigError("Location selection is stale; reopen Location")
        bind_sandbox_character_to_location(conn, character_id, values[index]["object_id"])
        options = refresh_sandbox_runtime_options(conn, character_id)
        name = str(values[index]["identity"].get("name") or values[index]["object_id"])
        return character_config_view(
            conn,
            character_id,
            notice=f"📍 Location assigned: {name}. Runtime options refreshed ({len(options)}).",
        )
    if callback_data.startswith("sw:cfg:am:"):
        parts = callback_data.split(":")
        if len(parts) != 6:
            raise SandboxCharacterConfigError("Invalid model selection")
        character_id = parts[3]
        provider_index = int(parts[4])
        model_index = int(parts[5])
        providers = _providers(conn)
        if provider_index < 0 or provider_index >= len(providers):
            raise SandboxCharacterConfigError("AI provider selection is stale; reopen Character AI")
        provider = providers[provider_index]
        models = _models(conn, str(provider["id"]))
        if model_index < 0 or model_index >= len(models):
            raise SandboxCharacterConfigError("AI model selection is stale; reopen Character AI")
        model = models[model_index]
        bind_sandbox_character_ai(conn, character_id, str(provider["id"]), str(model["model_id"]))
        return character_config_view(
            conn,
            character_id,
            notice=f"🤖 Character AI assigned: {provider['display_name']} · {model['display_name']}.",
        )
    if callback_data.startswith("sw:cfg:ap:"):
        _, _, _, character_id, raw_index = callback_data.split(":", 4)
        return ai_model_view(conn, character_id, int(raw_index))
    if callback_data.startswith("sw:cfg:l:"):
        return location_picker_view(conn, callback_data.split(":", 3)[3])
    if callback_data.startswith("sw:cfg:a:"):
        return ai_provider_view(conn, callback_data.split(":", 3)[3])
    if callback_data.startswith("sw:cfg:o:"):
        character_id = callback_data.split(":", 3)[3]
        options = refresh_sandbox_runtime_options(conn, character_id)
        return character_config_view(conn, character_id, notice=f"🎛 Runtime options refreshed: {len(options)} represented.")
    if callback_data.startswith("sw:cfg:t:"):
        character_id = callback_data.split(":", 3)[3]
        canonical_time = runtime_value(conn, "sim_time", None)
        if not canonical_time:
            raise SandboxCharacterConfigError("Real World clock is unavailable for sandbox initialization")
        configure_sandbox_clock(conn, str(canonical_time))
        return character_config_view(conn, character_id, notice="🕒 Sandbox clock initialized from the current Real World time snapshot.")
    if callback_data.startswith("sw:cfg:"):
        return character_config_view(conn, callback_data.split(":", 2)[2])
    raise KeyError(callback_data)


__all__ = [
    "SandboxCharacterConfigError",
    "ai_model_view",
    "ai_provider_view",
    "character_config_callback_view",
    "character_config_view",
    "location_picker_view",
]

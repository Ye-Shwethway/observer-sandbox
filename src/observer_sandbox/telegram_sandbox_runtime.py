from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID, get_sandbox_object
from .sandbox_runtime import (
    SandboxRuntimeError,
    configure_sandbox_clock,
    sandbox_character_readiness,
    sandbox_runtime_status,
    set_sandbox_paused,
    set_sandbox_speed,
)
from .simulation import runtime_value


def _fmt_time(value: str | None) -> str:
    if not value:
        return "Not configured"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d-%m-%Y (%A) %I:%M %p")
    except (TypeError, ValueError):
        return str(value)


def sandbox_runtime_view(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> tuple[str, list[list[dict[str, str]]]]:
    status = sandbox_runtime_status(conn, sandbox_id)
    lines = [
        "🕒 SANDBOX RUNTIME",
        "━━━━━━━━━━━━━━━━━━",
        "🧪 Isolated Creation Sandbox clock",
        "",
        f"🕒 Sim Time   {_fmt_time(status['sim_time'])}",
        f"⏩ Speed      {status['speed']:g}x",
        f"⏸ Paused     {'Yes' if status['paused'] else 'No'}",
        f"⚙️ Status     {str(status['runtime_status']).replace('_', ' ').title()}",
        "",
        "Real World runtime: untouched.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    if status["configured"]:
        keyboard.append(
            [{
                "text": "▶ Resume" if status["paused"] else "⏸ Pause",
                "callback_data": "sw:rt:resume" if status["paused"] else "sw:rt:pause",
            }]
        )
        keyboard.append(
            [
                {"text": "1x", "callback_data": "sw:rt:speed:1"},
                {"text": "60x", "callback_data": "sw:rt:speed:60"},
                {"text": "3600x", "callback_data": "sw:rt:speed:3600"},
            ]
        )
    else:
        lines.extend(["", "Clock must be configured before runtime readiness can pass."])
        keyboard.append([{"text": "🕒 Initialize from Real World Time", "callback_data": "sw:rt:init"}])
    keyboard.append([{"text": "← Sandbox World", "callback_data": "nav:sandbox"}])
    return "\n".join(lines), keyboard


def sandbox_character_runtime_view(
    conn: sqlite3.Connection,
    character_object_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    character = get_sandbox_object(conn, character_object_id)
    readiness = sandbox_character_readiness(conn, character_object_id)
    binding = readiness["ai_binding"]
    lines = [
        "🧠 SANDBOX CHARACTER RUNTIME",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {character['identity'].get('name', character_object_id)}",
        f"⚙️ State      {readiness['activation_status'].replace('_', ' ').title()}",
        f"✅ Ready      {'Yes' if readiness['ready'] else 'No'}",
        "",
        "Readiness gates",
    ]
    labels = {
        "character_active": "Character active",
        "location_assigned": "Location assigned",
        "runtime_options_available": "Runtime options available",
        "cognition_ai_bound": "Cognition AI bound",
        "clock_configured": "Sandbox clock configured",
    }
    for key, passed in readiness["gates"].items():
        lines.append(f"{'✓' if passed else '✕'} {labels.get(key, key)}")
    lines.extend(["", "🤖 Cognition AI"])
    if binding:
        lines.append(f"• {binding['provider_name']} · {binding['model_name']}")
    else:
        lines.append("• Not assigned")
    if readiness["runtime_options"]:
        lines.extend(["", "🎛 Runtime options"])
        for option in readiness["runtime_options"]:
            lines.append(f"• {option['action_key'].replace('_', ' ').title()}")
    if readiness["missing"]:
        lines.extend(["", "Missing before activation"])
        for key in readiness["missing"]:
            lines.append(f"• {labels.get(key, key)}")
    lines.extend(["", "Canonical universe: unchanged."])
    return "\n".join(lines), [
        [{"text": "🕒 Sandbox Runtime", "callback_data": "sw:runtime"}],
        [{"text": "← Character", "callback_data": f"sw:o:{character_object_id}"}],
        [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
    ]


def sandbox_runtime_callback_view(
    conn: sqlite3.Connection,
    callback_data: str,
) -> tuple[str, list[list[dict[str, str]]]] | None:
    if callback_data == "sw:runtime":
        return sandbox_runtime_view(conn)
    if callback_data == "sw:rt:init":
        canonical_time = runtime_value(conn, "sim_time", None)
        if not canonical_time:
            raise SandboxRuntimeError("Real World clock is unavailable for initialization")
        configure_sandbox_clock(conn, str(canonical_time))
        return sandbox_runtime_view(conn)
    if callback_data == "sw:rt:pause":
        set_sandbox_paused(conn, True)
        return sandbox_runtime_view(conn)
    if callback_data == "sw:rt:resume":
        status = sandbox_runtime_status(conn)
        if not status["configured"]:
            raise SandboxRuntimeError("Configure sandbox clock before resume")
        set_sandbox_paused(conn, False)
        return sandbox_runtime_view(conn)
    if callback_data.startswith("sw:rt:speed:"):
        raw = callback_data.rsplit(":", 1)[1]
        set_sandbox_speed(conn, float(raw))
        return sandbox_runtime_view(conn)
    if callback_data.startswith("sw:cr:"):
        return sandbox_character_runtime_view(conn, callback_data[6:])
    raise KeyError(callback_data)


def handle_sandbox_command(conn: sqlite3.Connection, parts: list[str]) -> str:
    if len(parts) == 1 or parts[1].lower() == "status":
        return sandbox_runtime_view(conn)[0]
    action = parts[1].lower()
    if action == "pause":
        return sandbox_runtime_view_after(conn, set_sandbox_paused(conn, True))
    if action == "resume":
        status = sandbox_runtime_status(conn)
        if not status["configured"]:
            return "Sandbox runtime rejected: configure the sandbox clock first."
        return sandbox_runtime_view_after(conn, set_sandbox_paused(conn, False))
    if action == "speed":
        if len(parts) != 3:
            return "Usage: /sandbox speed <1-3600>"
        try:
            status = set_sandbox_speed(conn, float(parts[2]))
        except (ValueError, SandboxRuntimeError) as exc:
            return f"Sandbox runtime rejected: {exc}"
        return sandbox_runtime_view_after(conn, status)
    if action == "time":
        if len(parts) < 3:
            return "Usage: /sandbox time <ISO-8601>"
        raw = " ".join(parts[2:]).strip()
        try:
            status = configure_sandbox_clock(conn, raw)
        except SandboxRuntimeError as exc:
            return f"Sandbox runtime rejected: {exc}"
        return sandbox_runtime_view_after(conn, status)
    return "Usage: /sandbox [status|pause|resume|speed <value>|time <ISO-8601>]"


def sandbox_runtime_view_after(conn: sqlite3.Connection, status: dict[str, Any]) -> str:
    return sandbox_runtime_view(conn, sandbox_id=str(status["sandbox_id"]))[0]


__all__ = [
    "handle_sandbox_command",
    "sandbox_character_runtime_view",
    "sandbox_runtime_callback_view",
    "sandbox_runtime_view",
]

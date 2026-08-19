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


def handle_sandbox_runtime_command(
    conn: sqlite3.Connection,
    command: str,
    args: list[str],
) -> str:
    if command == "/sandboxstatus":
        return sandbox_runtime_view(conn)[0]
    if command == "/sandboxpause":
        set_sandbox_paused(conn, True)
        return sandbox_runtime_view(conn)[0]
    if command == "/sandboxresume":
        status = sandbox_runtime_status(conn)
        if not status["configured"]:
            return "Sandbox runtime rejected: configure the sandbox clock first."
        set_sandbox_paused(conn, False)
        return sandbox_runtime_view(conn)[0]
    if command == "/sandboxspeed":
        if len(args) != 1:
            return "Usage: /sandboxspeed <0-3600>"
        try:
            set_sandbox_speed(conn, float(args[0]))
        except (ValueError, SandboxRuntimeError) as exc:
            return f"Sandbox runtime rejected: {exc}"
        return sandbox_runtime_view(conn)[0]
    if command == "/sandboxtime":
        if not args:
            return sandbox_runtime_view(conn)[0] + "\n\nSet manually with /sandboxtime <ISO-8601>."
        raw = " ".join(args).strip()
        try:
            set_sandbox_paused(conn, True)
            configure_sandbox_clock(conn, raw)
        except SandboxRuntimeError as exc:
            return f"Sandbox runtime rejected: {exc}"
        return (
            sandbox_runtime_view(conn)[0]
            + "\n\n✅ Manual time applied. Sandbox World was auto-paused and remains paused."
        )
    raise KeyError(command)


def handle_sandbox_command(conn: sqlite3.Connection, parts: list[str]) -> str:
    """Legacy internal grouped adapter retained for compatibility tests/callers.

    Public Telegram UX uses the explicit /sandbox* command family so every
    runtime mutation names its world directly.
    """
    if len(parts) == 1 or parts[1].lower() == "status":
        return handle_sandbox_runtime_command(conn, "/sandboxstatus", [])
    action = parts[1].lower()
    if action == "pause":
        return handle_sandbox_runtime_command(conn, "/sandboxpause", [])
    if action == "resume":
        return handle_sandbox_runtime_command(conn, "/sandboxresume", [])
    if action == "speed":
        return handle_sandbox_runtime_command(conn, "/sandboxspeed", parts[2:])
    if action == "time":
        return handle_sandbox_runtime_command(conn, "/sandboxtime", parts[2:])
    return "Use /sandboxstatus, /sandboxpause, /sandboxresume, /sandboxspeed, or /sandboxtime."


def sandbox_runtime_view_after(conn: sqlite3.Connection, status: dict[str, Any]) -> str:
    return sandbox_runtime_view(conn, sandbox_id=str(status["sandbox_id"]))[0]


__all__ = [
    "handle_sandbox_command",
    "handle_sandbox_runtime_command",
    "sandbox_character_runtime_view",
    "sandbox_runtime_callback_view",
    "sandbox_runtime_view",
]

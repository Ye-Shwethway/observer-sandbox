from __future__ import annotations

import sqlite3
from datetime import datetime

from .real_runtime_control import (
    RealRuntimeControlError,
    real_runtime_status,
    set_real_runtime_paused,
    set_real_runtime_speed,
    set_real_runtime_time,
)


def _fmt_time(value: str | None) -> str:
    if not value:
        return "Not configured"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d-%m-%Y (%A) %I:%M %p")
    except (TypeError, ValueError):
        return str(value)


def real_runtime_view(conn: sqlite3.Connection) -> tuple[str, list[list[dict[str, str]]]]:
    status = real_runtime_status(conn)
    lines = [
        "🕒 REAL WORLD RUNTIME",
        "━━━━━━━━━━━━━━━━━━",
        "🌍 Canonical universe clock",
        "",
        f"🕒 Sim Time   {_fmt_time(status['sim_time'])}",
        f"⏩ Speed      {status['speed']:g}x",
        f"⏸ Paused     {'Yes' if status['paused'] else 'No'}",
        "",
        "Sandbox World runtime: untouched.",
    ]
    keyboard = [
        [{
            "text": "▶ Resume" if status["paused"] else "⏸ Pause",
            "callback_data": "rw:rt:resume" if status["paused"] else "rw:rt:pause",
        }],
        [
            {"text": "1x", "callback_data": "rw:rt:speed:1"},
            {"text": "60x", "callback_data": "rw:rt:speed:60"},
            {"text": "3600x", "callback_data": "rw:rt:speed:3600"},
        ],
        [{"text": "← Real World", "callback_data": "nav:real"}],
    ]
    return "\n".join(lines), keyboard


def real_runtime_callback_view(
    conn: sqlite3.Connection,
    callback_data: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    if callback_data in {"nav:runtime", "rw:runtime"}:
        return real_runtime_view(conn)
    if callback_data == "rw:rt:pause":
        set_real_runtime_paused(conn, True)
        return real_runtime_view(conn)
    if callback_data == "rw:rt:resume":
        set_real_runtime_paused(conn, False)
        return real_runtime_view(conn)
    if callback_data.startswith("rw:rt:speed:"):
        raw = callback_data.rsplit(":", 1)[1]
        set_real_runtime_speed(conn, float(raw))
        return real_runtime_view(conn)
    raise KeyError(callback_data)


def handle_real_runtime_command(
    conn: sqlite3.Connection,
    command: str,
    args: list[str],
    *,
    requested_by: str | None = None,
) -> str:
    if command == "/realstatus":
        return real_runtime_view(conn)[0]
    if command == "/realpause":
        set_real_runtime_paused(conn, True)
        return real_runtime_view(conn)[0]
    if command == "/realresume":
        set_real_runtime_paused(conn, False)
        return real_runtime_view(conn)[0]
    if command == "/realspeed":
        if len(args) != 1:
            return "Usage: /realspeed <0-3600>"
        try:
            set_real_runtime_speed(conn, float(args[0]))
        except (ValueError, RealRuntimeControlError) as exc:
            return f"Real World runtime rejected: {exc}"
        return real_runtime_view(conn)[0]
    if command == "/realtime":
        if not args:
            return real_runtime_view(conn)[0] + "\n\nSet manually with /realtime <ISO-8601>."
        raw = " ".join(args).strip()
        try:
            result = set_real_runtime_time(conn, raw, requested_by=requested_by)
        except RealRuntimeControlError as exc:
            return f"Real World runtime rejected: {exc}"
        cancelled = len(result["cancelled_action_ids"])
        return (
            real_runtime_view(conn)[0]
            + "\n\n✅ Manual time applied. Real World was auto-paused and remains paused."
            + f"\nStale pending autonomous actions cancelled: {cancelled}."
        )
    raise KeyError(command)


__all__ = [
    "handle_real_runtime_command",
    "real_runtime_callback_view",
    "real_runtime_view",
]

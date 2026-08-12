from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from .autonomy import set_autonomy_paused, set_autonomy_speed
from .db import connect, migrate
from .observer_query import character_summary, location_summary, observer_status, recent_history
from .secrets import load_runtime_secrets

DEFAULT_DB = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))


def _allowed_user_ids() -> set[int]:
    raw = os.environ.get("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "")
    result: set[int] = set()
    for part in raw.replace(";", ",").split(","):
        part = part.strip()
        if part:
            try:
                result.add(int(part))
            except ValueError:
                continue
    return result


def _api(token: str, method: str, payload: dict[str, Any] | None = None, *, timeout: int = 30) -> Any:
    data = urllib.parse.urlencode(payload or {}).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    if not body.get("ok"):
        raise RuntimeError(body.get("description", "Telegram API request failed"))
    return body.get("result")


def _send(token: str, chat_id: int, text: str) -> None:
    _api(token, "sendMessage", {"chat_id": chat_id, "text": text[:4096]}, timeout=15)


def _fmt_character(data: dict[str, Any]) -> str:
    c = data["character"]
    s = data["state"]
    return (
        f"{c['name']}\n"
        f"Location: {s['location_name']}\n"
        f"Action: {s['current_action']}\n"
        f"Sim time: {s['sim_time']}\n"
        f"Energy: {s['energy']:.1f}\n"
        f"Hunger: {s['hunger']:.1f}\n"
        f"Thirst: {s['thirst']:.1f}\n"
        f"Sleepiness: {s['sleepiness']:.1f}\n"
        f"Cleanliness: {s['cleanliness']:.1f}"
    )


def _fmt_location(data: dict[str, Any]) -> str:
    loc = data["location"]
    lines = [f"{loc['name']} ({loc['type']})"]
    if data["children"]:
        lines.append("Contents:")
        for child in data["children"]:
            caps = ", ".join(child["capabilities"])
            suffix = f" [{caps}]" if caps else ""
            lines.append(f"- {child['name']} ({child['id']}){suffix}")
    if data["residents"]:
        lines.append("Residents: " + ", ".join(row["name"] for row in data["residents"]))
    if data["occupants"]:
        lines.append("Occupants: " + ", ".join(row["name"] for row in data["occupants"]))
    return "\n".join(lines)


def _fmt_history(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No history yet."
    lines = ["Recent history:"]
    for row in rows:
        detail = row.get("action") or row["event_type"]
        if row.get("target"):
            detail += f" → {row['target']}"
        reason = f" — {row['reason']}" if row.get("reason") else ""
        lines.append(f"- {row['sim_time']} | {detail}{reason}")
    return "\n".join(lines)


def _fmt_status(data: dict[str, Any]) -> str:
    c = data["character"]
    pending = data.get("pending_action")
    return (
        f"Observer Sandbox\n"
        f"Autonomy: {'ON' if data['autonomy_enabled'] else 'OFF'} ({data['mode']})\n"
        f"Paused: {data['paused']} | Speed: {data['speed']}x\n"
        f"Pending: {pending['action'] if pending else 'none'}\n\n"
        f"{c['location_name']} | {c['current_action']}\n"
        f"Sim time: {c['sim_time']}"
    )


def _help() -> str:
    return (
        "Observer Sandbox — P2.1\n"
        "/status — runtime overview\n"
        "/watch — Darian now + recent history\n"
        "/history [n] — recent events\n"
        "/darian — character summary\n"
        "/home — Home summary\n"
        "/pause — pause autonomy\n"
        "/resume — resume autonomy\n"
        "/speed <value> — set runtime speed\n"
        "/whoami — show your Telegram user id"
    )


def handle_command(db_path: str | Path, *, user_id: int, text: str) -> str:
    allowed = _allowed_user_ids()
    command_line = (text or "").strip()
    first, *rest = command_line.split()
    command = first.split("@", 1)[0].lower() if first else ""

    if command in {"/whoami", "/start"} and user_id not in allowed:
        return f"Observer Sandbox bot is connected. Your Telegram user id is {user_id}. Authorization is not enabled for this id yet."
    if user_id not in allowed:
        return "Not authorized. Use /whoami to obtain your Telegram user id."

    with connect(db_path) as conn:
        migrate(conn)
        if command in {"/start", "/help"}:
            return _help()
        if command == "/status":
            return _fmt_status(observer_status(conn))
        if command == "/darian":
            return _fmt_character(character_summary(conn, "char_darian"))
        if command == "/home":
            return _fmt_location(location_summary(conn, "home"))
        if command == "/watch":
            return _fmt_character(character_summary(conn, "char_darian")) + "\n\n" + _fmt_history(recent_history(conn, limit=5))
        if command == "/history":
            limit = 8
            if rest:
                try:
                    limit = max(1, min(int(rest[0]), 20))
                except ValueError:
                    return "Usage: /history [1-20]"
            return _fmt_history(recent_history(conn, limit=limit))
        if command == "/pause":
            return _fmt_status(set_autonomy_paused(conn, True))
        if command == "/resume":
            return _fmt_status(set_autonomy_paused(conn, False))
        if command == "/speed":
            if not rest:
                return "Usage: /speed <0-3600>"
            try:
                value = float(rest[0])
                return _fmt_status(set_autonomy_speed(conn, value))
            except ValueError as exc:
                return f"Speed rejected: {exc}"
        return _help()


def run_polling(db_path: str | Path = DEFAULT_DB) -> None:
    load_runtime_secrets()
    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return

    offset: int | None = None
    backoff = 1.0
    while True:
        try:
            payload: dict[str, Any] = {
                "timeout": 20,
                "allowed_updates": json.dumps(["message"]),
            }
            if offset is not None:
                payload["offset"] = offset
            updates = _api(token, "getUpdates", payload, timeout=30) or []
            backoff = 1.0
            for update in updates:
                update_id = int(update["update_id"])
                offset = update_id + 1
                message = update.get("message") or {}
                chat = message.get("chat") or {}
                sender = message.get("from") or {}
                text = message.get("text")
                if not text or chat.get("type") != "private":
                    continue
                chat_id = int(chat["id"])
                user_id = int(sender.get("id", chat_id))
                try:
                    reply = handle_command(db_path, user_id=user_id, text=text)
                except Exception as exc:
                    reply = f"Observer command failed safely: {type(exc).__name__}"
                _send(token, chat_id, reply)
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
            time.sleep(backoff)
            backoff = min(backoff * 2.0, 30.0)

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from . import telegram_bot as base
from .db import connect, migrate
from .telegram_ai_control import callback_view as ai_callback_view
from .telegram_ai_control import home_view as ai_home_view

_ORIGINAL_API = base._api
_ORIGINAL_SEND = base._send
_ORIGINAL_EDIT = base._edit
_ORIGINAL_CALLBACK_VIEW = base._callback_view
_ORIGINAL_HOME_MESSAGE = base._home_message
_ORIGINAL_HOME_KEYBOARD = base._home_keyboard
_ORIGINAL_HANDLE_COMMAND = base.handle_command
_ORIGINAL_COMMAND_KEYBOARD = base._command_keyboard
_ORIGINAL_HELP = base._help
_DELETE_SENTINEL = "__DELETE_OBSERVER_HOME__"
_HOME_DELETE_DEADLINES: dict[tuple[int, int], float] = {}


def _home_ttl_seconds() -> int:
    raw = os.environ.get("OBSERVER_TELEGRAM_HOME_TTL_SECONDS", "300").strip()
    try:
        value = int(raw)
    except ValueError:
        value = 300
    return max(30, min(value, 3600))


def _home_message(conn, user_id: int) -> str:
    ttl_minutes = _home_ttl_seconds() / 60.0
    ttl_text = f"{int(ttl_minutes)} min" if ttl_minutes.is_integer() else f"{ttl_minutes:g} min"
    return _ORIGINAL_HOME_MESSAGE(conn, user_id) + f"\n\n🧹 Auto-close: {ttl_text}"


def _home_keyboard() -> list[list[dict[str, str]]]:
    keyboard = [list(row) for row in _ORIGINAL_HOME_KEYBOARD()]
    keyboard.append([{"text": "⚙️ Creator Settings", "callback_data": "ai:home"}])
    keyboard.append([{"text": "✕ Close", "callback_data": "nav:close"}])
    return keyboard


def _forget_home_delete(chat_id: int, message_id: int) -> None:
    _HOME_DELETE_DEADLINES.pop((int(chat_id), int(message_id)), None)


def _arm_home_delete(chat_id: int, message_id: int) -> None:
    _HOME_DELETE_DEADLINES[(int(chat_id), int(message_id))] = time.time() + _home_ttl_seconds()


def _expire_home_messages(token: str, *, now: float | None = None) -> None:
    current = time.time() if now is None else float(now)
    due = [key for key, deadline in _HOME_DELETE_DEADLINES.items() if deadline <= current]
    for chat_id, message_id in due:
        try:
            _ORIGINAL_API(
                token,
                "deleteMessage",
                {"chat_id": chat_id, "message_id": message_id},
                timeout=10,
            )
        except Exception:
            pass
        finally:
            _forget_home_delete(chat_id, message_id)


def _api(token: str, method: str, payload: dict[str, Any] | None = None, *, timeout: int = 30) -> Any:
    result = _ORIGINAL_API(token, method, payload, timeout=timeout)
    if method == "getUpdates":
        _expire_home_messages(token)
    return result


def _send(token: str, chat_id: int, text: str, keyboard: list[list[dict[str, str]]] | None = None) -> Any:
    payload: dict[str, Any] = {"chat_id": chat_id, "text": text[:4096]}
    markup = base._reply_markup(keyboard)
    if markup:
        payload["reply_markup"] = markup
    result = _ORIGINAL_API(token, "sendMessage", payload, timeout=15)
    if text.startswith("🌌 OBSERVER HOME") and isinstance(result, dict) and result.get("message_id") is not None:
        _arm_home_delete(chat_id, int(result["message_id"]))
    return result


def _edit(token: str, chat_id: int, message_id: int, text: str, keyboard: list[list[dict[str, str]]] | None = None) -> None:
    if text == _DELETE_SENTINEL:
        try:
            _ORIGINAL_API(
                token,
                "deleteMessage",
                {"chat_id": int(chat_id), "message_id": int(message_id)},
                timeout=10,
            )
        finally:
            _forget_home_delete(chat_id, message_id)
        return
    _ORIGINAL_EDIT(token, chat_id, message_id, text, keyboard)
    if text.startswith("🌌 OBSERVER HOME"):
        _arm_home_delete(chat_id, message_id)
    else:
        _forget_home_delete(chat_id, message_id)


def _callback_view(conn, user_id: int, callback_data: str):
    if callback_data == "nav:close":
        return _DELETE_SENTINEL, None
    if callback_data.startswith(("ai:", "af:")):
        if base._user_role(user_id) != "owner":
            return (
                "🔒 Creator authority required for AI settings.",
                [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]],
            )
        return ai_callback_view(conn, user_id, callback_data)
    return _ORIGINAL_CALLBACK_VIEW(conn, user_id, callback_data)


def _help(role: str) -> str:
    text = _ORIGINAL_HELP(role)
    if role == "owner":
        text += "\n/settings — Creator settings and AI cognition"
    return text


def handle_command(db_path: str | Path, *, user_id: int, text: str) -> str:
    command_line = (text or "").strip()
    first = command_line.split()[0] if command_line else ""
    command = first.split("@", 1)[0].lower()
    if command in {"/settings", "/ai"}:
        role = base._user_role(user_id)
        if role == "unauthorized":
            return "Not authorized. Use /whoami to obtain your Telegram user id."
        if role != "owner":
            return "🔒 Creator authority required for AI settings."
        with connect(db_path) as conn:
            migrate(conn)
            text_value, _ = ai_home_view(conn)
            return text_value
    return _ORIGINAL_HANDLE_COMMAND(db_path, user_id=user_id, text=text)


def _command_keyboard(command: str):
    if command in {"/settings", "/ai"}:
        return [
            [{"text": "🧠 Primary Cognition", "callback_data": "ai:providers"}],
            [{"text": "🛟 Fallback Model", "callback_data": "af:providers"}],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ]
    return _ORIGINAL_COMMAND_KEYBOARD(command)


# Install bounded Creator extensions into the existing polling loop. Telegram
# remains an adapter; provider/fallback semantics live in reusable AI services,
# while message deletion is presentation lifecycle only.
base._api = _api
base._send = _send
base._edit = _edit
base._home_message = _home_message
base._home_keyboard = _home_keyboard
base._callback_view = _callback_view
base._help = _help
base.handle_command = handle_command
base._command_keyboard = _command_keyboard

run_polling = base.run_polling

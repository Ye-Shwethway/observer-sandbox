from __future__ import annotations

from pathlib import Path

from . import telegram_bot as base
from .db import connect, migrate
from .telegram_ai_control import callback_view as ai_callback_view
from .telegram_ai_control import home_view as ai_home_view

_ORIGINAL_CALLBACK_VIEW = base._callback_view
_ORIGINAL_HOME_KEYBOARD = base._home_keyboard
_ORIGINAL_HANDLE_COMMAND = base.handle_command
_ORIGINAL_COMMAND_KEYBOARD = base._command_keyboard
_ORIGINAL_HELP = base._help


def _home_keyboard() -> list[list[dict[str, str]]]:
    keyboard = [list(row) for row in _ORIGINAL_HOME_KEYBOARD()]
    keyboard.append([{"text": "⚙️ Creator Settings", "callback_data": "ai:home"}])
    return keyboard


def _callback_view(conn, user_id: int, callback_data: str):
    if callback_data.startswith("ai:"):
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
            [{"text": "🧠 AI Cognition", "callback_data": "ai:providers"}],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ]
    return _ORIGINAL_COMMAND_KEYBOARD(command)


# Install the extension into the existing polling loop. Telegram remains a UI
# adapter; all provider/catalog/probe/binding behavior lives in reusable AI
# control services.
base._home_keyboard = _home_keyboard
base._callback_view = _callback_view
base._help = _help
base.handle_command = handle_command
base._command_keyboard = _command_keyboard

run_polling = base.run_polling

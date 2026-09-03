from __future__ import annotations

from pathlib import Path
from typing import Any

from .db import connect, migrate
from .telegram_sandbox_location_edit import (
    SandboxLocationEditError,
    get_sandbox_location_edit_session,
    handle_sandbox_location_edit_text,
)


_PENDING_KEYBOARD: list[list[dict[str, str]]] | None = None


def install_sandbox_location_edit_text_adapter(base_module: Any) -> None:
    if getattr(base_module, "_sandbox_location_edit_text_adapter_installed", False):
        return
    original_handle_command = base_module.handle_command
    original_command_keyboard = base_module._command_keyboard

    def handle_command(db_path: str | Path, *, user_id: int, text: str) -> str:
        global _PENDING_KEYBOARD
        command_line = (text or "").strip()
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None or not session.get("pending_section") or command_line.startswith("/"):
            return original_handle_command(db_path, user_id=user_id, text=text)
        with connect(db_path) as conn:
            migrate(conn)
            try:
                result = handle_sandbox_location_edit_text(conn, user_id=user_id, text=command_line)
            except SandboxLocationEditError as exc:
                _PENDING_KEYBOARD = [
                    [{"text": "✕ Cancel Section Edit", "callback_data": "sw:ledit:cancelinput"}],
                    [{"text": "✅ Done Editing", "callback_data": "sw:ledit:done"}],
                ]
                return (
                    "❌ LOCATION SECTION REJECTED\n━━━━━━━━━━━━━━━━━━\n"
                    f"{exc}\n\n"
                    "Send a corrected complete section JSON, or cancel this section edit."
                )
        if result is None:
            return original_handle_command(db_path, user_id=user_id, text=text)
        reply, keyboard = result
        _PENDING_KEYBOARD = keyboard
        return reply

    def command_keyboard(command: str):
        global _PENDING_KEYBOARD
        if _PENDING_KEYBOARD is not None:
            keyboard = _PENDING_KEYBOARD
            _PENDING_KEYBOARD = None
            return keyboard
        return original_command_keyboard(command)

    base_module.handle_command = handle_command
    base_module._command_keyboard = command_keyboard
    base_module._sandbox_location_edit_text_adapter_installed = True


__all__ = ["install_sandbox_location_edit_text_adapter"]

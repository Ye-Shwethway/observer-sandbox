"""Item-edit launcher and callback routing for Telegram world-layer views."""

from __future__ import annotations

from typing import Any

from .creation_sandbox import get_sandbox_object
from .telegram_sandbox_item_edit import SandboxItemEditError, sandbox_item_edit_callback_view


def _safe_item_edit_failure(exc: Exception, callback_data: str) -> tuple[str, list[list[dict[str, str]]]]:
    reason = " ".join(str(exc).replace("\x00", "").split())[:700] or "No additional reason was provided."
    error_type = type(exc).__name__
    object_id = callback_data.split(":", 3)[3] if callback_data.startswith("sw:iedit:enter:") else None
    text = (
        "⚠️ SANDBOX ITEM EDIT FAILED\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"Error: {error_type}\n"
        f"Reason: {reason}\n\n"
        "No Item mutation was applied. Real World and canonical state were not changed."
    )
    keyboard: list[list[dict[str, str]]] = []
    if object_id:
        keyboard.append([{"text": "← Item", "callback_data": f"sw:o:{object_id}"}])
    keyboard.append([{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}])
    return text, keyboard


def install_item_edit_world_layers_extension(base_module: Any) -> None:
    """Install Item edit launch UI and route ``sw:iedit:*`` callbacks."""
    if getattr(base_module, "_item_edit_extension_installed", False):
        return

    original_object_view = base_module.sandbox_object_view
    original_world_layer_callback_view = base_module.world_layer_callback_view

    def sandbox_object_view(conn, object_id: str):
        text, keyboard = original_object_view(conn, object_id)
        try:
            obj = get_sandbox_object(conn, object_id)
        except (KeyError, ValueError):
            return text, keyboard
        if obj.get("creation_type") != "item" or obj.get("lifecycle_status") != "active":
            return text, keyboard

        rows = [list(row) for row in (keyboard or [])]
        callback_data = f"sw:iedit:enter:{object_id}"
        if not any(
            button.get("callback_data") == callback_data
            for row in rows
            for button in row
        ):
            rows.insert(0, [{"text": "✏️ Edit Item", "callback_data": callback_data}])
        return text, rows

    def world_layer_callback_view(conn, callback_data: str):
        if callback_data.startswith("sw:iedit:"):
            try:
                return sandbox_item_edit_callback_view(
                    conn,
                    user_id=base_module._notification_user_id(),
                    callback_data=callback_data,
                )
            except Exception as exc:
                # Sandbox Item editing is owner-only. Surface a bounded diagnostic
                # instead of letting the outer polling loop collapse it to a generic
                # "failed safely" toast, while preserving zero-mutation semantics.
                return _safe_item_edit_failure(exc, callback_data)
        return original_world_layer_callback_view(conn, callback_data)

    base_module.sandbox_object_view = sandbox_object_view
    base_module.world_layer_callback_view = world_layer_callback_view
    base_module._item_edit_extension_installed = True


# Compatibility alias for the short-lived WIP name used by focused tests and
# any already-imported callers. The established world-layer extension naming
# remains the canonical public installer.
install_world_layer_item_edit_extension = install_item_edit_world_layers_extension

__all__ = [
    "install_item_edit_world_layers_extension",
    "install_world_layer_item_edit_extension",
]

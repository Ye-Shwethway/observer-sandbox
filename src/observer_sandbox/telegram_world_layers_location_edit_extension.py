from __future__ import annotations

import sqlite3

from .creation_sandbox import get_sandbox_object
from .telegram_sandbox_location_edit import SandboxLocationEditError, location_edit_callback_view


def install_location_edit_world_layers_extension(base) -> None:
    original_object_view = base.sandbox_object_view
    original_callback = base.world_layer_callback_view

    def sandbox_object_view(conn: sqlite3.Connection, object_id: str):
        text, keyboard = original_object_view(conn, object_id)
        try:
            value = get_sandbox_object(conn, object_id)
        except Exception:
            return text, keyboard
        if value.get("creation_type") != "location" or value.get("lifecycle_status") != "active":
            return text, keyboard
        edit_row = [{"text": "✏️ Edit Location", "callback_data": f"sw:ledit:start:{object_id}"}]
        return text, [edit_row, *keyboard]

    def world_layer_callback_view(conn: sqlite3.Connection, callback_data: str):
        if callback_data.startswith("sw:ledit:"):
            try:
                return location_edit_callback_view(
                    conn,
                    user_id=base._notification_user_id(),
                    callback_data=callback_data,
                )
            except SandboxLocationEditError as exc:
                return (
                    "❌ SANDBOX LOCATION EDIT\n━━━━━━━━━━━━━━━━━━\n"
                    f"{exc}",
                    [[{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]],
                )
        return original_callback(conn, callback_data)

    base.sandbox_object_view = sandbox_object_view
    base.world_layer_callback_view = world_layer_callback_view


__all__ = ["install_location_edit_world_layers_extension"]

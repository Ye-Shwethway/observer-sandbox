from __future__ import annotations

import sqlite3

from .creation_sandbox import get_sandbox_object
from .sandbox_location_cleanup import SandboxLocationCleanupError
from .telegram_sandbox_location_cleanup import location_cleanup_callback_view


def install_location_cleanup_world_layers_extension(base) -> None:
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
        delete_row = [{"text": "🗑 Delete Location", "callback_data": f"sw:ldel:start:{object_id}"}]
        rows = [list(row) for row in (keyboard or [])]
        insert_at = 1 if rows else 0
        rows.insert(insert_at, delete_row)
        return text, rows

    def world_layer_callback_view(conn: sqlite3.Connection, callback_data: str):
        if callback_data.startswith("sw:ldel:"):
            try:
                view = location_cleanup_callback_view(
                    conn,
                    user_id=base._notification_user_id(),
                    callback_data=callback_data,
                )
                if isinstance(view, dict) and view.get("return_to"):
                    return original_callback(conn, str(view["return_to"]))
                return view
            except SandboxLocationCleanupError as exc:
                return (
                    "❌ SANDBOX LOCATION CLEANUP\n━━━━━━━━━━━━━━━━━━\n"
                    f"{exc}\n\nNo Location data was deleted.",
                    [
                        [{"text": "← Locations", "callback_data": "sw:list:location"}],
                        [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
                    ],
                )
        return original_callback(conn, callback_data)

    base.sandbox_object_view = sandbox_object_view
    base.world_layer_callback_view = world_layer_callback_view


__all__ = ["install_location_cleanup_world_layers_extension"]

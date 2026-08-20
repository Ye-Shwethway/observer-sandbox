"""Item-edit launcher and callback routing for Telegram world-layer views."""

from __future__ import annotations

from typing import Any

from .telegram_sandbox_item_edit import sandbox_item_edit_callback_view


def install_world_layer_item_edit_extension(base_module: Any) -> None:
    """Install Item edit launch UI and route ``sw:iedit:*`` callbacks."""
    if getattr(base_module, "_item_edit_extension_installed", False):
        return

    original_item_detail_view = base_module.sandbox_item_detail_view
    original_world_layer_callback_view = base_module.world_layer_callback_view

    def sandbox_item_detail_view(conn, item_id: int):
        text, keyboard = original_item_detail_view(conn, item_id)
        rows = [list(row) for row in keyboard]
        insert_at = max(0, len(rows) - 1)
        rows.insert(
            insert_at,
            [{"text": "✏️ Edit Item", "callback_data": f"sw:iedit:open:{int(item_id)}"}],
        )
        return text, rows

    def world_layer_callback_view(conn, callback_data: str):
        if callback_data.startswith("sw:iedit:"):
            return sandbox_item_edit_callback_view(
                conn,
                callback_data,
                user_id=base_module._notification_user_id(),
            )
        return original_world_layer_callback_view(conn, callback_data)

    base_module.sandbox_item_detail_view = sandbox_item_detail_view
    base_module.world_layer_callback_view = world_layer_callback_view
    base_module._item_edit_extension_installed = True

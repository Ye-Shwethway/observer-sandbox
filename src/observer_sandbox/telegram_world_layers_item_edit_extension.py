from __future__ import annotations

import sqlite3

from .creation_sandbox import get_sandbox_object


def install_item_edit_world_layers_extension(base) -> None:
    """Add the Creator Item editor entry without changing generic world-layer routing."""

    original_object_view = base.sandbox_object_view

    def sandbox_object_view(conn: sqlite3.Connection, object_id: str):
        text, keyboard = original_object_view(conn, object_id)
        value = get_sandbox_object(conn, object_id)
        if value["creation_type"] != "item" or value["lifecycle_status"] != "active":
            return text, keyboard
        rows = list(keyboard or [])
        rows.insert(0, [{"text": "✏️ Edit Item", "callback_data": f"sw:iedit:enter:{object_id}"}])
        return text, rows

    base.sandbox_object_view = sandbox_object_view


__all__ = ["install_item_edit_world_layers_extension"]

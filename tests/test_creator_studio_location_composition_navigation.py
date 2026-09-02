from __future__ import annotations

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_studio import studio_callback_view
from observer_sandbox.telegram_world_layers import world_layer_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if button.get("callback_data")
    }


def test_approved_composition_sandbox_world_button_routes_to_supported_world_view(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        studio_callback_view(conn, 91, "sw:cs:location:composition:starter")
        approved, keyboard = studio_callback_view(conn, 91, "sw:cs:approve:confirm:1")

        assert "SANDBOX COMPOSITION APPROVED" in approved
        assert "nav:sandbox" in _callbacks(keyboard)
        assert "sw:world" not in _callbacks(keyboard)

        text, world_keyboard = world_layer_callback_view(conn, "nav:sandbox")
        assert "SANDBOX WORLD" in text
        assert world_keyboard

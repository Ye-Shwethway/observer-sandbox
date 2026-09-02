from __future__ import annotations

from observer_sandbox.creator_studio_location_composition import (
    approve_location_composition_draft,
    start_location_composition_draft,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_world_layers import world_layer_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if button.get("callback_data")
    }


def test_location_detail_is_human_friendly_and_omits_raw_nested_dict_dump(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        draft = start_location_composition_draft(conn, 501)
        created = approve_location_composition_draft(conn, 501, int(draft["revision"]))
        property_id = created["refs"]["property"]
        room_id = created["refs"]["room"]

        property_text, property_keyboard = world_layer_callback_view(conn, f"sw:o:{property_id}")
        room_text, room_keyboard = world_layer_callback_view(conn, f"sw:o:{room_id}")

        for text in (property_text, room_text):
            assert "Creation Sandbox · Active" in text
            assert "🔐 ACCESS & CONTROL" in text
            assert "Access: Public" in text
            assert "📐 PHYSICAL" in text
            assert "{'" not in text
            assert "None" not in text
            assert "Properties" not in text
            assert "canonical universe unchanged" in text.lower()

        assert "📍 Composition Test Property" in property_text
        assert "📍 Composition Test Room" in room_text
        assert "Parent: Composition Test Property" in room_text
        assert "nav:sandbox" in _callbacks(property_keyboard)
        assert "sw:list:location" in _callbacks(room_keyboard)

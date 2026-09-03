from __future__ import annotations

from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_v2 import get_sandbox_location_v2, materialize_sandbox_location_v2
from observer_sandbox.telegram_sandbox_location_edit import handle_sandbox_location_edit_text
from observer_sandbox.telegram_world_layers import world_layer_callback_view


def _payload():
    payload = manual_location_template()
    payload["identity"].update(
        {
            "key": "residential.family.house",
            "name": "Family House",
            "kind": "building",
            "description": "A small detached private residential building.",
            "functional_classes": ["residential"],
            "tags": ["residential-building", "family-house"],
        }
    )
    payload["facilities"]["capabilities"] = ["cook", "eat"]
    return payload


def test_single_field_preview_shows_only_human_change(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "901")

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(conn, _payload())
        object_id = location["object_id"]
        world_layer_callback_view(conn, f"sw:ledit:start:{object_id}")
        world_layer_callback_view(conn, "sw:ledit:s:identity")
        world_layer_callback_view(conn, "sw:ledit:f:in_name")

        preview = handle_sandbox_location_edit_text(conn, user_id=901, text="Test House")
        assert preview is not None
        text, keyboard = preview

        assert "📋 LOCATION EDIT PREVIEW" in text
        assert "Section: 🪪 Identity" in text
        assert "CHANGES" in text
        assert "• Name: Family House → Test House" in text
        assert "description" not in text.lower()
        assert "functional_classes" not in text
        assert "residential-building" not in text
        assert "{\"" not in text
        assert "BEFORE" not in text
        assert "AFTER" not in text
        assert "Nothing has changed yet" in text
        assert any(
            button.get("callback_data") == "sw:ledit:apply"
            for row in keyboard
            for button in row
        )
        assert get_sandbox_location_v2(conn, object_id)["source"]["identity"]["name"] == "Family House"


def test_facilities_preview_renders_token_lists_without_json(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "902")

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(conn, _payload())
        object_id = location["object_id"]
        world_layer_callback_view(conn, f"sw:ledit:start:{object_id}")
        world_layer_callback_view(conn, "sw:ledit:s:facilities")
        world_layer_callback_view(conn, "sw:ledit:f:fac_cap")
        world_layer_callback_view(conn, "sw:ledit:tok:fac_cap:sleep")
        text, _ = world_layer_callback_view(conn, "sw:ledit:tokdone:fac_cap")

        assert "• Capabilities: Cook, Eat → Cook, Eat, Sleep" in text
        assert "{\"" not in text
        assert "facility_types" not in text
        assert get_sandbox_location_v2(conn, object_id)["source"]["facilities"]["capabilities"] == ["cook", "eat"]

from __future__ import annotations

import json

from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_v2 import get_sandbox_location_v2, materialize_sandbox_location_v2
from observer_sandbox.sandbox_runtime import sandbox_runtime_status
from observer_sandbox.telegram_sandbox_location_edit import (
    get_sandbox_location_edit_session,
    handle_sandbox_location_edit_text,
)
from observer_sandbox.telegram_world_layers import sandbox_object_view, world_layer_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard or []
        for button in row
        if isinstance(button, dict) and button.get("callback_data")
    }


def test_location_detail_exposes_edit_and_section_preview_apply_done_without_runtime_pause(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "77")

    with connect(db) as conn:
        payload = manual_location_template()
        payload["identity"].update({
            "key": "place.edit.house",
            "name": "Family House",
            "kind": "building",
            "description": "A modest family house.",
        })
        location = materialize_sandbox_location_v2(conn, payload)
        object_id = location["object_id"]
        runtime_before = sandbox_runtime_status(conn, location["sandbox_id"])

        detail_text, detail_keyboard = sandbox_object_view(conn, object_id)
        assert "Family House" in detail_text
        assert f"sw:ledit:start:{object_id}" in _callbacks(detail_keyboard)

        home_text, home_keyboard = world_layer_callback_view(conn, f"sw:ledit:start:{object_id}")
        assert "SANDBOX LOCATION EDIT" in home_text
        assert "sw:ledit:s:identity" in _callbacks(home_keyboard)
        assert sandbox_runtime_status(conn, location["sandbox_id"]) == runtime_before

        prompt_text, _ = world_layer_callback_view(conn, "sw:ledit:s:identity")
        assert "Identity" in prompt_text
        replacement = dict(payload["identity"])
        replacement["name"] = "Edited Family House"
        replacement["description"] = "A modest family house after Creator edit."
        preview = handle_sandbox_location_edit_text(conn, user_id=77, text=json.dumps(replacement))
        assert preview is not None
        preview_text, preview_keyboard = preview
        assert "LOCATION EDIT PREVIEW" in preview_text
        assert "Edited Family House" in preview_text
        assert "sw:ledit:apply" in _callbacks(preview_keyboard)
        assert get_sandbox_location_v2(conn, object_id)["source"]["identity"]["name"] == "Family House"

        applied_text, applied_keyboard = world_layer_callback_view(conn, "sw:ledit:apply")
        assert "LOCATION EDIT APPLIED" in applied_text
        assert "Edited Family House" in applied_text
        assert "sw:ledit:done" in _callbacks(applied_keyboard)
        assert get_sandbox_location_v2(conn, object_id)["source"]["identity"]["name"] == "Edited Family House"
        assert sandbox_runtime_status(conn, location["sandbox_id"]) == runtime_before

        done_text, done_keyboard = world_layer_callback_view(conn, "sw:ledit:done")
        assert "EDIT MODE CLOSED" in done_text
        assert "No runtime pause was needed" in done_text
        assert f"sw:o:{object_id}" in _callbacks(done_keyboard)
        assert get_sandbox_location_edit_session(user_id=77) is None


def test_location_edit_rejects_invalid_section_before_preview_and_preserves_source(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "88")

    with connect(db) as conn:
        location = materialize_sandbox_location_v2(conn, manual_location_template())
        object_id = location["object_id"]
        world_layer_callback_view(conn, f"sw:ledit:start:{object_id}")
        world_layer_callback_view(conn, "sw:ledit:s:operations")
        before = get_sandbox_location_v2(conn, object_id)["source"]

        try:
            handle_sandbox_location_edit_text(conn, user_id=88, text=json.dumps({"initial_state": "teleporting"}))
        except Exception as exc:
            assert "Unsupported" in str(exc) or "operation" in str(exc).lower()
        else:
            raise AssertionError("invalid Location operation state should be rejected")
        after = get_sandbox_location_v2(conn, object_id)["source"]
        assert after == before

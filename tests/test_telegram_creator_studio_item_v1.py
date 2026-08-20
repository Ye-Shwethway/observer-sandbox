from __future__ import annotations

import json

import pytest

import observer_sandbox.creator_studio_item as item_studio
from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_studio import CreatorStudioError, active_draft
from observer_sandbox.creator_studio_item import ai_item_draft, manual_item_draft, manual_item_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import get_sandbox_item
from observer_sandbox.telegram_creator_studio import draft_preview_view, studio_callback_view
from observer_sandbox.telegram_world_layers import sandbox_list_view, sandbox_object_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if button.get("callback_data")
    }


def test_create_menu_exposes_item_and_item_methods(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        text, keyboard = studio_callback_view(conn, 1, "sw:cs:create")
        assert "CREATE IN SANDBOX" in text
        assert "sw:cs:type:item" in _callbacks(keyboard)

        text, keyboard = studio_callback_view(conn, 1, "sw:cs:type:item")
        assert "CREATE ITEM" in text
        callbacks = _callbacks(keyboard)
        assert "sw:cs:input:item:ai" in callbacks
        assert "sw:cs:input:item:manual" in callbacks


def test_manual_item_template_is_valid_and_unknown_fields_fail_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        draft = manual_item_draft(conn, 7, json.dumps(manual_item_template()))
        assert draft["creation_type"] == "item"
        assert draft["proposal"]["properties"]["item_payload"]["definition"]["name"] == "Steel Water Bottle"

        bad = manual_item_template()
        bad["definition"]["invented_field"] = True
        with pytest.raises(CreatorStudioError, match="unknown"):
            manual_item_draft(conn, 8, json.dumps(bad))


def test_item_preview_confirm_approval_materializes_through_item_service_only(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        draft = manual_item_draft(conn, 11, json.dumps(manual_item_template()))

        text, keyboard = draft_preview_view(conn, 11)
        assert "ITEM SANDBOX DRAFT" in text
        assert "Exact item-v1 validation passed" in text
        assert "sw:cs:approve" in _callbacks(keyboard)

        confirm_text, confirm_keyboard = studio_callback_view(conn, 11, "sw:cs:approve")
        confirm = f"sw:cs:approve:confirm:{draft['revision']}"
        assert confirm in _callbacks(confirm_keyboard)
        assert "approval" in confirm_text.lower()

        approved_text, approved_keyboard = studio_callback_view(conn, 11, confirm)
        assert "SANDBOX ITEM APPROVED" in approved_text
        assert active_draft(conn, 11) is None
        assert canonical_state_fingerprint(conn) == before

        view_callbacks = _callbacks(approved_keyboard)
        item_callback = next(value for value in view_callbacks if value and value.startswith("sw:o:"))
        object_id = item_callback.removeprefix("sw:o:")
        item = get_sandbox_item(conn, object_id)
        assert item["creation_type"] == "item"
        assert item["item"]["definition"]["name"] == "Steel Water Bottle"

        list_text, list_keyboard = sandbox_list_view(conn, "item")
        assert "SANDBOX ITEMS" in list_text
        assert "Steel Water Bottle" in list_text
        assert item_callback in _callbacks(list_keyboard)

        detail_text, detail_keyboard = sandbox_object_view(conn, object_id)
        assert "Steel Water Bottle" in detail_text
        assert "Creation Sandbox" in detail_text
        assert "sw:list:item" in _callbacks(detail_keyboard)


def test_ai_item_path_uses_creation_binding_then_exact_validation(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    candidate = manual_item_template()
    candidate["definition"]["key"] = "ai_water_bottle"
    candidate["definition"]["name"] = "AI Water Bottle"

    monkeypatch.setattr(
        item_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "fake", "model_id": "fake-model", "parameters": {}},
    )
    monkeypatch.setattr(item_studio, "generate_structured", lambda *args, **kwargs: candidate)

    with connect(db) as conn:
        draft = ai_item_draft(conn, 13, "Create a reusable water bottle")
        assert draft["creation_type"] == "item"
        assert draft["draft_mode"] == "ai_generated"
        assert draft["proposal"]["properties"]["item_payload"]["definition"]["name"] == "AI Water Bottle"

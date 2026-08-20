from __future__ import annotations

from copy import deepcopy

import observer_sandbox.creator_studio_item_batch as batch_studio
from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.creator_studio_item_batch import ai_item_batch_draft
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_studio import draft_preview_view, studio_callback_view
from observer_sandbox.telegram_item_draft_review import render_item_draft_text


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if button.get("callback_data")
    }


def _candidate():
    backpack = manual_item_template()
    backpack["definition"].update({
        "key": "camping_backpack",
        "name": "Camping Backpack",
        "kind": "container",
        "capabilities": ["inspect", "store"],
        "modules": {"container": {"capacity_volume": {"value": 30, "unit": "l"}}},
    })
    flashlight = manual_item_template()
    flashlight["definition"].update({"key": "camping_flashlight", "name": "Camping Flashlight", "kind": "equipment"})
    flashlight["relationships"]["stored_in"] = "$camping_backpack"
    return {"items": [{"ref": "camping_backpack", "payload": backpack}, {"ref": "camping_flashlight", "payload": flashlight}]}


def test_item_batch_preview_exposes_detail_and_txt_review_actions(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setattr(batch_studio, "creator_creation_binding", lambda conn: {"provider_id": "fake", "model_id": "fake", "parameters": {}})
    monkeypatch.setattr(batch_studio, "generate_structured", lambda *args, **kwargs: deepcopy(_candidate()))
    with connect(db) as conn:
        draft = ai_item_batch_draft(conn, 91, "Create a camping backpack and flashlight inside it")
        text, keyboard = draft_preview_view(conn, 91)
        callbacks = _callbacks(keyboard)
        assert "ITEM BATCH SANDBOX DRAFT" in text
        assert "sw:cs:item-detail:0" in callbacks
        assert "sw:cs:item-export" in callbacks

        detail, detail_keyboard = studio_callback_view(conn, 91, "sw:cs:item-detail:0")
        assert "ITEM DRAFT PROFILE" in detail
        assert "Camping Backpack" in detail
        assert "Definition key" not in detail
        assert "Type: Container" in detail
        assert "Capacity: 30 l" in detail
        assert "Value tracking: Not included" in detail
        assert "Next Item →" in {button["text"] for row in detail_keyboard for button in row}

        detail2, _ = studio_callback_view(conn, 91, "sw:cs:item-detail:1")
        assert "Camping Flashlight" in detail2
        assert "Stored in: Camping Backpack" in detail2
        assert "$camping_backpack" not in detail2

        back_text, back_keyboard = studio_callback_view(conn, 91, "sw:cs:preview")
        back_callbacks = _callbacks(back_keyboard)
        assert "ITEM BATCH SANDBOX DRAFT" in back_text
        assert "sw:cs:item-detail:0" in back_callbacks
        assert "sw:cs:item-export" in back_callbacks
        assert "sw:cs:reroll" in back_callbacks
        assert "sw:cs:approve" in back_callbacks

        filename, exported = render_item_draft_text(draft)
        assert filename == f"creator-studio-item-batch-camping-backpack-plus-1-r{draft['revision']}.txt"
        assert "Camping Backpack" in exported
        assert "Camping Flashlight" in exported
        assert '"stored_in": "$camping_backpack"' in exported
        assert "Internal batch ref: camping_backpack" in exported
        assert "Creation Sandbox draft only" in exported

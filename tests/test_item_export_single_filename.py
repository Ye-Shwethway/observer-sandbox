from __future__ import annotations

from observer_sandbox.telegram_item_draft_review import render_item_draft_text


def test_single_item_export_filename_includes_item_name():
    payload = {
        "definition": {"key": "camping-lantern", "name": "Camping Lantern"},
    }
    draft = {
        "revision": 3,
        "draft_mode": "ai_generated",
        "proposal": {"properties": {"item_payload": payload}},
    }
    filename, _ = render_item_draft_text(draft)
    assert filename == "creator-studio-item-camping-lantern-r3.txt"

from __future__ import annotations

import observer_sandbox.creator_draft_export as export_mod


def test_character_export_filename_includes_type_and_character_name(monkeypatch):
    monkeypatch.setattr(
        export_mod,
        "active_draft",
        lambda conn, user_id: {
            "revision": 4,
            "draft_mode": "ai_generated",
            "proposal": {
                "creation_type": "character",
                "identity": {"name": "Adrian Vale"},
                "target_scope": "Creation Sandbox",
                "properties": {},
                "capabilities": [],
                "relationships": [],
                "provenance": {},
            },
        },
    )
    filename, text = export_mod.render_full_draft_text(object(), 7)
    assert filename == "creator-studio-character-adrian-vale-r4.txt"
    assert "Type: Character" in text
    assert "Name: Adrian Vale" in text

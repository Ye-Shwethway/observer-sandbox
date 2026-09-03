from __future__ import annotations

import json

from observer_sandbox.creator_studio_location import manual_location_draft, manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_studio import studio_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if isinstance(button, dict) and button.get("callback_data")
    }


def test_single_location_approval_uses_canonical_sandbox_world_route(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        draft = manual_location_draft(conn, 23, json.dumps(manual_location_template()))
        confirm = f"sw:cs:approve:confirm:{draft['revision']}"
        text, keyboard = studio_callback_view(conn, 23, confirm)

        assert "SANDBOX LOCATION APPROVED" in text
        callbacks = _callbacks(keyboard)
        assert "nav:sandbox" in callbacks
        assert "sw:world" not in callbacks


def test_public_navigation_boundary_normalizes_legacy_sandbox_world_callback(monkeypatch) -> None:
    import observer_sandbox.telegram_creator_studio as studio

    monkeypatch.setattr(
        studio._base,
        "studio_callback_view",
        lambda conn, user_id, callback_data: (
            "ok",
            [[{"text": "🌌 Sandbox World", "callback_data": "sw:world"}]],
        ),
    )

    text, keyboard = studio.studio_callback_view(None, 1, "anything")
    assert text == "ok"
    assert _callbacks(keyboard) == {"nav:sandbox"}

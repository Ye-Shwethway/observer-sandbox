from __future__ import annotations

from types import SimpleNamespace

import observer_sandbox.telegram_sandbox_batch_delete as delete_ui


def _objects():
    return [
        {"object_id": "char_seed", "creation_type": "character", "lifecycle_status": "active", "identity": {"name": "Seed Character"}},
        {"object_id": "item_old", "creation_type": "item", "lifecycle_status": "active", "identity": {"name": "Old Item"}},
        {"object_id": "loc_keep", "creation_type": "location", "lifecycle_status": "active", "identity": {"name": "Keep Location"}},
    ]


def test_world_view_adds_batch_delete_and_selection_excludes_locations(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    base = SimpleNamespace(
        sandbox_world_view=lambda conn: ("world", [[{"text": "studio", "callback_data": "sw:studio"}]]),
        world_layer_callback_view=lambda conn, callback_data: ("legacy", None),
        _notification_user_id=lambda: 4242,
    )
    delete_ui.install_sandbox_batch_delete_world_layers_extension(base)

    _, keyboard = base.sandbox_world_view(object())
    assert any(button.get("callback_data") == "sw:del:enter" for row in keyboard for button in row)

    text, keyboard = base.world_layer_callback_view(object(), "sw:del:enter")
    assert "Seed Character" in " ".join(button["text"] for row in keyboard for button in row)
    assert "Old Item" in " ".join(button["text"] for row in keyboard for button in row)
    assert "Keep Location" not in " ".join(button["text"] for row in keyboard for button in row)
    assert "Locations are intentionally excluded" in text


def test_select_all_review_then_apply_deletes_mixed_batch(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    calls = []
    monkeypatch.setattr(
        delete_ui,
        "delete_sandbox_objects",
        lambda conn, ids, sandbox_id: calls.append(list(ids)) or {
            "deleted_count": 2,
            "deleted": [
                {"object_id": "char_seed", "creation_type": "character", "name": "Seed Character"},
                {"object_id": "item_old", "creation_type": "item", "name": "Old Item"},
            ],
            "canonical_unchanged": True,
        },
    )

    delete_ui.sandbox_batch_delete_callback_view(object(), user_id=4242, callback_data="sw:del:enter")
    delete_ui.sandbox_batch_delete_callback_view(object(), user_id=4242, callback_data="sw:del:all")
    review, review_keyboard = delete_ui.sandbox_batch_delete_callback_view(object(), user_id=4242, callback_data="sw:del:review")
    assert "CONFIRM SANDBOX DELETE" in review
    assert "Seed Character" in review and "Old Item" in review
    assert review_keyboard[0][0]["callback_data"] == "sw:del:apply"

    result, _ = delete_ui.sandbox_batch_delete_callback_view(object(), user_id=4242, callback_data="sw:del:apply")
    assert calls == [["char_seed", "item_old"]]
    assert "BATCH DELETE COMPLETE" in result
    assert "Canonical state fingerprint unchanged" in result


def test_cancel_returns_to_world_without_delete(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    base = SimpleNamespace(
        sandbox_world_view=lambda conn: ("world", [[{"text": "studio", "callback_data": "sw:studio"}]]),
        world_layer_callback_view=lambda conn, callback_data: ("legacy", None),
        _notification_user_id=lambda: 4242,
    )
    delete_ui.install_sandbox_batch_delete_world_layers_extension(base)
    base.world_layer_callback_view(object(), "sw:del:enter")
    assert base.world_layer_callback_view(object(), "sw:del:cancel")[0] == "world"

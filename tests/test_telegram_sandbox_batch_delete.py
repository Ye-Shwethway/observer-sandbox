from __future__ import annotations

from types import SimpleNamespace

import observer_sandbox.telegram_sandbox_batch_delete as delete_ui


def _objects():
    return [
        {"object_id": "char_seed", "creation_type": "character", "lifecycle_status": "active", "identity": {"name": "Seed Character"}},
        {"object_id": "item_old", "creation_type": "item", "lifecycle_status": "active", "identity": {"name": "Old Item"}},
        {"object_id": "loc_keep", "creation_type": "location", "lifecycle_status": "active", "identity": {"name": "Keep Location"}},
    ]


def _base():
    def list_view(conn, creation_type):
        if creation_type == "item":
            return "items", [
                [{"text": "Old Item", "callback_data": "sw:o:item_old"}],
                [{"text": "+ Create Item", "callback_data": "sw:cs:type:item"}],
                [{"text": "back", "callback_data": "nav:sandbox"}],
            ]
        if creation_type == "character":
            return "characters", [
                [{"text": "Seed Character", "callback_data": "sw:o:char_seed"}],
                [{"text": "back", "callback_data": "nav:sandbox"}],
            ]
        return "locations", [[{"text": "back", "callback_data": "nav:sandbox"}]]

    def callback(conn, callback_data):
        if callback_data == "sw:list:item":
            return list_view(conn, "item")
        if callback_data == "sw:list:character":
            return list_view(conn, "character")
        if callback_data == "nav:sandbox":
            return "world", [[{"text": "studio", "callback_data": "sw:studio"}]]
        return "legacy", None

    return SimpleNamespace(
        sandbox_world_view=lambda conn: ("world", [[{"text": "studio", "callback_data": "sw:studio"}]]),
        sandbox_list_view=list_view,
        world_layer_callback_view=callback,
        _notification_user_id=lambda: 4242,
    )


def test_world_view_adds_batch_delete_and_selection_excludes_locations(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    base = _base()
    delete_ui.install_sandbox_batch_delete_world_layers_extension(base)

    _, keyboard = base.sandbox_world_view(object())
    assert any(button.get("callback_data") == "sw:del:enter" for row in keyboard for button in row)

    text, keyboard = base.world_layer_callback_view(object(), "sw:del:enter")
    assert "Seed Character" in " ".join(button["text"] for row in keyboard for button in row)
    assert "Old Item" in " ".join(button["text"] for row in keyboard for button in row)
    assert "Keep Location" not in " ".join(button["text"] for row in keyboard for button in row)
    assert "Locations are intentionally excluded" in text


def test_item_list_exposes_item_scoped_batch_delete(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    base = _base()
    delete_ui.install_sandbox_batch_delete_world_layers_extension(base)

    _, keyboard = base.sandbox_list_view(object(), "item")
    callbacks = [button.get("callback_data") for row in keyboard for button in row]
    assert "sw:del:enter:item" in callbacks
    assert callbacks.index("sw:del:enter:item") < callbacks.index("sw:cs:type:item")

    text, scoped_keyboard = base.world_layer_callback_view(object(), "sw:del:enter:item")
    labels = " ".join(button["text"] for row in scoped_keyboard for button in row)
    assert "SANDBOX ITEM DELETE" in text
    assert "Old Item" in labels
    assert "Seed Character" not in labels


def test_character_list_exposes_character_scoped_batch_delete(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    base = _base()
    delete_ui.install_sandbox_batch_delete_world_layers_extension(base)

    _, keyboard = base.sandbox_list_view(object(), "character")
    callbacks = [button.get("callback_data") for row in keyboard for button in row]
    assert "sw:del:enter:character" in callbacks

    text, scoped_keyboard = base.world_layer_callback_view(object(), "sw:del:enter:character")
    labels = " ".join(button["text"] for row in scoped_keyboard for button in row)
    assert "SANDBOX CHARACTER DELETE" in text
    assert "Seed Character" in labels
    assert "Old Item" not in labels


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


def test_item_scope_select_all_only_deletes_items(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    calls = []
    monkeypatch.setattr(
        delete_ui,
        "delete_sandbox_objects",
        lambda conn, ids, sandbox_id: calls.append(list(ids)) or {
            "deleted_count": 1,
            "deleted": [{"object_id": "item_old", "creation_type": "item", "name": "Old Item"}],
            "canonical_unchanged": True,
        },
    )

    delete_ui.sandbox_batch_delete_callback_view(object(), user_id=4242, callback_data="sw:del:enter:item")
    delete_ui.sandbox_batch_delete_callback_view(object(), user_id=4242, callback_data="sw:del:all")
    delete_ui.sandbox_batch_delete_callback_view(object(), user_id=4242, callback_data="sw:del:apply")
    assert calls == [["item_old"]]


def test_scoped_cancel_returns_to_originating_list(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    base = _base()
    delete_ui.install_sandbox_batch_delete_world_layers_extension(base)

    base.world_layer_callback_view(object(), "sw:del:enter:item")
    assert base.world_layer_callback_view(object(), "sw:del:cancel")[0] == "items"

    base.world_layer_callback_view(object(), "sw:del:enter:character")
    assert base.world_layer_callback_view(object(), "sw:del:cancel")[0] == "characters"


def test_root_cancel_returns_to_world_without_delete(monkeypatch):
    delete_ui._SESSIONS.clear()
    monkeypatch.setattr(delete_ui, "list_sandbox_objects", lambda conn, sandbox_id: _objects())
    base = _base()
    delete_ui.install_sandbox_batch_delete_world_layers_extension(base)
    base.world_layer_callback_view(object(), "sw:del:enter")
    assert base.world_layer_callback_view(object(), "sw:del:cancel")[0] == "world"

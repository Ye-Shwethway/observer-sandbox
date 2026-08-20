from __future__ import annotations

from contextlib import contextmanager
from types import SimpleNamespace

import observer_sandbox.telegram_sandbox_item_edit_adapter as text_adapter
import observer_sandbox.telegram_world_layers_item_edit_extension as world_extension


def test_world_layer_routes_item_edit_callbacks_with_owner_identity(monkeypatch):
    calls = []

    def object_view(conn, object_id):
        return "item", [[{"text": "back", "callback_data": "nav:sandbox"}]]

    def original_callback(conn, callback_data):
        return "legacy", None

    base = SimpleNamespace(
        sandbox_object_view=object_view,
        world_layer_callback_view=original_callback,
        _notification_user_id=lambda: 4242,
    )

    monkeypatch.setattr(
        world_extension,
        "get_sandbox_object",
        lambda conn, object_id: {
            "object_id": object_id,
            "creation_type": "item",
            "lifecycle_status": "active",
        },
    )
    monkeypatch.setattr(
        world_extension,
        "sandbox_item_edit_callback_view",
        lambda conn, *, user_id, callback_data: calls.append((callback_data, user_id)) or ("editor", []),
    )

    world_extension.install_item_edit_world_layers_extension(base)

    assert base.world_layer_callback_view(object(), "sw:iedit:enter:item_12") == ("editor", [])
    assert calls == [("sw:iedit:enter:item_12", 4242)]
    assert base.world_layer_callback_view(object(), "nav:sandbox") == ("legacy", None)

    _, keyboard = base.sandbox_object_view(object(), "item_12")
    assert any(
        button.get("callback_data") == "sw:iedit:enter:item_12"
        for row in keyboard
        for button in row
    )


def test_world_layer_does_not_add_edit_action_to_non_item(monkeypatch):
    base = SimpleNamespace(
        sandbox_object_view=lambda conn, object_id: (
            "location",
            [[{"text": "back", "callback_data": "nav:sandbox"}]],
        ),
        world_layer_callback_view=lambda conn, callback_data: ("legacy", None),
        _notification_user_id=lambda: 4242,
    )
    monkeypatch.setattr(
        world_extension,
        "get_sandbox_object",
        lambda conn, object_id: {
            "object_id": object_id,
            "creation_type": "location",
            "lifecycle_status": "active",
        },
    )

    world_extension.install_item_edit_world_layers_extension(base)
    _, keyboard = base.sandbox_object_view(object(), "loc_12")
    assert all(
        not str(button.get("callback_data") or "").startswith("sw:iedit:")
        for row in keyboard
        for button in row
    )


def test_item_edit_adapter_routes_pending_free_text_and_preserves_keyboard(monkeypatch):
    text_adapter._PENDING_KEYBOARD = None
    delegated = []

    base = SimpleNamespace(
        handle_command=lambda db_path, *, user_id, text: delegated.append(text) or "legacy",
        _command_keyboard=lambda command: [[{"text": "legacy", "callback_data": "legacy"}]],
    )

    monkeypatch.setattr(
        text_adapter,
        "get_sandbox_item_edit_session",
        lambda *, user_id: {"pending_path": "definition.name", "object_id": "item_12"},
    )

    @contextmanager
    def fake_connect(db_path):
        yield object()

    monkeypatch.setattr(text_adapter, "connect", fake_connect)
    monkeypatch.setattr(text_adapter, "migrate", lambda conn: None)
    expected_keyboard = [[{"text": "✅ Apply Change", "callback_data": "sw:iedit:apply"}]]
    monkeypatch.setattr(
        text_adapter,
        "handle_sandbox_item_edit_text",
        lambda conn, *, user_id, text: ("preview", expected_keyboard),
    )

    text_adapter.install_sandbox_item_edit_text_adapter(base)

    assert base.handle_command("db.sqlite", user_id=4242, text="Updated Name") == "preview"
    assert delegated == []
    assert base._command_keyboard("Updated Name") == expected_keyboard
    assert base._command_keyboard("Updated Name") == [[{"text": "legacy", "callback_data": "legacy"}]]


def test_item_edit_adapter_keeps_slash_commands_on_normal_command_path(monkeypatch):
    text_adapter._PENDING_KEYBOARD = None
    base = SimpleNamespace(
        handle_command=lambda db_path, *, user_id, text: "normal-command",
        _command_keyboard=lambda command: None,
    )
    monkeypatch.setattr(
        text_adapter,
        "get_sandbox_item_edit_session",
        lambda *, user_id: {"pending_path": "definition.name", "object_id": "item_12"},
    )

    text_adapter.install_sandbox_item_edit_text_adapter(base)

    assert base.handle_command("db.sqlite", user_id=4242, text="/status") == "normal-command"

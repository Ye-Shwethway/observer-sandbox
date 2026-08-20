from __future__ import annotations

import pytest

import observer_sandbox.telegram_sandbox_item_edit as item_edit


def test_item_edit_preflight_failure_does_not_pause_or_open_session(monkeypatch):
    item_edit._SESSIONS.clear()
    runtime_calls = []

    monkeypatch.setattr(item_edit, "_identity", lambda conn, object_id: ("sandbox_alpha", "Legacy Item"))
    monkeypatch.setattr(
        item_edit,
        "_item_payload",
        lambda conn, object_id: (_ for _ in ()).throw(ValueError("item-v1 schema mismatch")),
    )
    monkeypatch.setattr(
        item_edit,
        "sandbox_runtime_status",
        lambda conn, sandbox_id: runtime_calls.append(("status", sandbox_id)) or {"paused": False},
    )
    monkeypatch.setattr(
        item_edit,
        "set_sandbox_paused",
        lambda conn, paused, *, sandbox_id: runtime_calls.append(("pause", sandbox_id, paused)),
    )

    with pytest.raises(item_edit.SandboxItemEditError, match="Current approved Item cannot enter edit mode"):
        item_edit.enter_sandbox_item_edit(object(), user_id=4242, object_id="item_legacy")

    assert runtime_calls == []
    assert item_edit.get_sandbox_item_edit_session(user_id=4242) is None


def test_item_edit_home_failure_restores_running_runtime(monkeypatch):
    item_edit._SESSIONS.clear()
    pause_calls = []
    states = iter([{"paused": False}, {"paused": True}])

    monkeypatch.setattr(item_edit, "_identity", lambda conn, object_id: ("sandbox_alpha", "Item"))
    monkeypatch.setattr(item_edit, "_item_payload", lambda conn, object_id: {"definition": {"name": "Item"}})
    monkeypatch.setattr(item_edit, "sandbox_runtime_status", lambda conn, sandbox_id: next(states))
    monkeypatch.setattr(
        item_edit,
        "set_sandbox_paused",
        lambda conn, paused, *, sandbox_id: pause_calls.append((sandbox_id, paused)),
    )
    monkeypatch.setattr(
        item_edit,
        "item_edit_home_view",
        lambda conn, *, user_id: (_ for _ in ()).throw(RuntimeError("render failed")),
    )

    with pytest.raises(RuntimeError, match="render failed"):
        item_edit.enter_sandbox_item_edit(object(), user_id=4242, object_id="item_12")

    assert pause_calls == [("sandbox_alpha", True), ("sandbox_alpha", False)]
    assert item_edit.get_sandbox_item_edit_session(user_id=4242) is None

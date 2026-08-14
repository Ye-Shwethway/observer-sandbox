from observer_sandbox import telegram_creator_bot as creator_bot


def test_observer_home_keyboard_has_manual_close():
    keyboard = creator_bot._home_keyboard()
    assert any(
        button.get("callback_data") == "nav:close"
        for row in keyboard
        for button in row
    )


def test_home_send_schedules_and_auto_deletes(monkeypatch):
    creator_bot._HOME_DELETE_DEADLINES.clear()
    calls = []

    def fake_api(token, method, payload=None, *, timeout=30):
        calls.append((method, dict(payload or {})))
        if method == "sendMessage":
            return {"message_id": 77}
        return True

    monkeypatch.setattr(creator_bot, "_ORIGINAL_API", fake_api)
    monkeypatch.setattr(creator_bot, "_home_ttl_seconds", lambda: 60)
    monkeypatch.setattr(creator_bot.time, "time", lambda: 100.0)

    creator_bot._send("token", 111, "🌌 OBSERVER HOME\nmenu", creator_bot._home_keyboard())
    assert creator_bot._HOME_DELETE_DEADLINES[(111, 77)] == 160.0

    creator_bot._expire_home_messages("token", now=161.0)
    assert (111, 77) not in creator_bot._HOME_DELETE_DEADLINES
    assert ("deleteMessage", {"chat_id": 111, "message_id": 77}) in calls


def test_manual_close_deletes_message_and_clears_timer(monkeypatch):
    creator_bot._HOME_DELETE_DEADLINES.clear()
    creator_bot._HOME_DELETE_DEADLINES[(111, 88)] = 999.0
    calls = []

    def fake_api(token, method, payload=None, *, timeout=30):
        calls.append((method, dict(payload or {})))
        return True

    monkeypatch.setattr(creator_bot, "_ORIGINAL_API", fake_api)
    creator_bot._edit("token", 111, 88, creator_bot._DELETE_SENTINEL, None)

    assert (111, 88) not in creator_bot._HOME_DELETE_DEADLINES
    assert calls == [("deleteMessage", {"chat_id": 111, "message_id": 88})]

import threading
from types import SimpleNamespace

import observer_sandbox.telegram_creator_ux_polish as ux


def test_creator_input_prompt_lifecycle_auto_closes_after_consumed_input():
    ux._PROMPT_MESSAGES.clear()
    ux._DELETE_AFTER_INPUT.clear()

    ux._record_prompt_edit(111, 777, "👤 CHARACTER · AI DRAFT\n━━━━━━━━━━━━━━━━━━\nDescribe the character")
    assert ux._PROMPT_MESSAGES[111] == 777
    assert ux._take_prompt_delete(111) is None

    ux._mark_studio_input_consumed(111)
    assert ux._take_prompt_delete(111) == 777
    assert ux._take_prompt_delete(111) is None


def test_item_and_batch_prompt_cards_are_tracked_for_cleanup():
    ux._PROMPT_MESSAGES.clear()
    ux._DELETE_AFTER_INPUT.clear()

    for index, title in enumerate(("📦 ITEM · AI DRAFT", "📦 ITEM BATCH · AI DRAFT"), start=1):
        ux._record_prompt_edit(111, 700 + index, f"{title}\n━━━━━━━━━━━━━━━━━━\nDescribe it")
        assert ux._PROMPT_MESSAGES[111] == 700 + index

    ux._mark_studio_input_consumed(111)
    assert ux._take_prompt_delete(111) == 702


def test_navigating_away_clears_tracked_prompt_message():
    ux._PROMPT_MESSAGES.clear()
    ux._DELETE_AFTER_INPUT.clear()

    ux._record_prompt_edit(111, 777, "📍 LOCATION · MANUAL\n━━━━━━━━━━━━━━━━━━\nSend the location name")
    ux._record_prompt_edit(111, 777, "🛠 CREATOR STUDIO\n━━━━━━━━━━━━━━━━━━")
    ux._mark_studio_input_consumed(111)
    assert ux._take_prompt_delete(111) is None


def test_merge_commit_summary_prefers_meaningful_pr_title():
    message = "Merge pull request #299 from Ye-Shwethway/test\n\nRefine Character creation ownership and add draft export"
    assert ux._meaningful_commit_summary(message) == "Refine Character creation ownership and add draft export"
    assert ux._meaningful_commit_summary("Direct runtime fix") == "Direct runtime fix"


def test_typing_pump_sends_native_chat_action_and_stops():
    called = threading.Event()
    payloads = []

    def fake_api(token, method, payload, timeout=30):
        payloads.append((token, method, payload, timeout))
        called.set()
        return True

    pump = ux._start_typing_pump(fake_api, "test-token", 111)
    assert pump is not None
    assert called.wait(1.0)
    stop, thread = pump
    stop.set()
    thread.join(timeout=1.0)

    assert payloads
    token, method, payload, timeout = payloads[0]
    assert token == "test-token"
    assert method == "sendChatAction"
    assert payload == {"chat_id": 111, "action": "typing"}
    assert timeout == 10


def test_dynamic_creator_studio_router_gets_typing_and_consume_hooks(monkeypatch):
    ux._PROMPT_MESSAGES.clear()
    ux._DELETE_AFTER_INPUT.clear()
    calls = []
    typing_started = []

    def routed(db_path, *, user_id, text):
        calls.append((str(db_path), user_id, text))
        return "draft ready"

    routed._creator_studio_input_router = True
    base = SimpleNamespace(handle_command=routed)

    monkeypatch.setattr(ux, "_active_studio_input_mode", lambda db_path, user_id: "ai_generated")
    monkeypatch.setattr(ux.os.environ, "get", lambda key, default="": "test-token" if key == "OBSERVER_TELEGRAM_BOT_TOKEN" else default)

    def fake_start(api, token, chat_id):
        typing_started.append((token, chat_id))
        return None

    monkeypatch.setattr(ux, "_start_typing_pump", fake_start)

    assert ux._wrap_active_studio_router(base, lambda *args, **kwargs: True) is True
    assert getattr(base.handle_command, "_creator_ux_wrapped", False) is True
    assert base.handle_command("/tmp/test.sqlite3", user_id=111, text="Create Adrian") == "draft ready"

    assert calls == [("/tmp/test.sqlite3", 111, "Create Adrian")]
    assert typing_started == [("test-token", 111)]
    assert 111 in ux._DELETE_AFTER_INPUT

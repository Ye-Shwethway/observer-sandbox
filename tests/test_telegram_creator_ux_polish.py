import threading

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

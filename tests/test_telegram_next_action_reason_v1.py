from observer_sandbox.telegram_notifications import format_action_completion


def _state(sim_time: str) -> dict:
    return {
        "actor_id": "char_darian",
        "actor_name": "Darian Thorne",
        "sim_time": sim_time,
        "location_name": "Training Hall",
        "energy": 72.9,
        "fatigue": 33.5,
        "hunger": 37.9,
        "thirst": 6.3,
        "sleepiness": 16.6,
        "cleanliness": 69.2,
    }


def test_completion_shows_next_action_reason_with_duration_and_eta():
    before = _state("2025-05-04T17:18:00+00:00")
    after = _state("2025-05-04T17:28:00+00:00")
    action = {
        "action": "rest",
        "duration_minutes": 10,
        "speed_at_plan": 1.0,
        "reason": "Brief rest to restore energy and reduce fatigue before winding down.",
    }
    next_action = {
        "action": "idle",
        "duration_minutes": 10,
        "speed_at_plan": 1.0,
        "planned_sim_time": "2025-05-04T17:28:00+00:00",
        "reason": "Take a quiet pause before choosing the next evening activity.",
    }

    message = format_action_completion(
        action,
        before,
        after,
        actor_name="Darian Thorne",
        next_action=next_action,
    )

    assert "⏭ Next: Idle" in message
    assert "💭 Take a quiet pause before choosing the next evening activity." in message
    assert message.index("⏭ Next: Idle") < message.index("💭 Take a quiet pause") < message.index("⏱ Duration 10 sim min")
    assert "⏳ Expected update:" in message


def test_completion_omits_next_reason_line_when_reason_is_absent():
    before = _state("2025-05-04T17:18:00+00:00")
    after = _state("2025-05-04T17:28:00+00:00")
    action = {"action": "rest", "duration_minutes": 10, "speed_at_plan": 1.0}
    next_action = {
        "action": "idle",
        "duration_minutes": 10,
        "speed_at_plan": 1.0,
        "planned_sim_time": "2025-05-04T17:28:00+00:00",
    }

    message = format_action_completion(action, before, after, next_action=next_action)

    next_block = message.split("⏭ Next: Idle", 1)[1]
    assert "💭" not in next_block
    assert "⏱ Duration 10 sim min" in next_block

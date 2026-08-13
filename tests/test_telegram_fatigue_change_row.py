from observer_sandbox.telegram_notifications import format_action_completion


def test_character_update_changes_include_fatigue_with_recovery_semantics():
    before = {
        "sim_time": "2025-05-02T15:19:00+00:00",
        "location_name": "Top-Class Home Gym",
        "energy": 53.6,
        "fatigue": 70.8,
        "hunger": 31.3,
        "thirst": 22.4,
        "sleepiness": 29.3,
        "cleanliness": 92.0,
    }
    after = {
        "sim_time": "2025-05-02T15:49:00+00:00",
        "location_name": "Top-Class Home Gym",
        "energy": 58.6,
        "fatigue": 67.3,
        "hunger": 32.3,
        "thirst": 23.9,
        "sleepiness": 27.3,
        "cleanliness": 91.9,
    }
    action = {
        "action": "rest",
        "duration_minutes": 30,
        "speed_at_plan": 2.0,
        "reason": "Recovering from systemic fatigue.",
    }

    text = format_action_completion(action, before, after)

    assert "💢 Fatigue" in text
    assert "70.8 → 67.3" in text
    assert "▼3.5 ✓" in text

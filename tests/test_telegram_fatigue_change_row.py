from observer_sandbox.telegram_notifications import format_action_completion


def _state(**overrides):
    value = {
        "sim_time": "2025-05-02T15:19:00+00:00",
        "location_name": "Top-Class Home Gym",
        "energy": 53.6,
        "fatigue": 70.8,
        "hunger": 31.3,
        "thirst": 22.4,
        "sleepiness": 29.3,
        "cleanliness": 92.0,
    }
    value.update(overrides)
    return value


def test_character_update_changes_include_fatigue_with_recovery_semantics():
    before = _state()
    after = _state(
        sim_time="2025-05-02T15:49:00+00:00",
        energy=58.6,
        fatigue=67.3,
        hunger=32.3,
        thirst=23.9,
        sleepiness=27.3,
        cleanliness=91.9,
    )
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


def test_character_update_keeps_all_core_physiology_rows_when_delta_is_tiny_or_zero():
    before = _state(fatigue=0.0, cleanliness=82.75)
    after = _state(
        sim_time="2025-05-02T15:22:00+00:00",
        energy=53.5,
        fatigue=0.0,
        hunger=31.4,
        thirst=0.0,
        sleepiness=29.4,
        cleanliness=82.71,
    )
    action = {
        "action": "drink",
        "duration_minutes": 3,
        "speed_at_plan": 10.0,
        "reason": "Hydrate.",
    }

    text = format_action_completion(action, before, after)

    for row in ("⚡ Energy", "💢 Fatigue", "🍽 Hunger", "💧 Thirst", "🌙 Sleepiness", "🫧 Cleanliness"):
        assert row in text
    assert "💢 Fatigue     0.0 → 0.0  =0.0 •" in text
    assert "🫧 Cleanliness 82.8 → 82.7  =0.0 •" in text

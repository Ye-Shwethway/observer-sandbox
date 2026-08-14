from observer_sandbox.telegram_notifications import format_action_completion


def test_structured_meal_completion_shows_items_and_combined_macros():
    action = {
        "action": "eat",
        "duration_minutes": 20,
        "target": "meal_target",
        "reason": "eat a balanced meal",
        "nutrition_intake": {
            "source": "eating-behavior-v1",
            "items": [
                {"item_name": "Apple", "quantity": 1.0, "unit": "piece"},
                {"item_name": "Cooked Chicken Breast", "quantity": 200.0, "unit": "g"},
            ],
            "energy_kcal": 425.0,
            "protein_g": 62.5,
            "carbohydrate_g": 25.0,
            "fat_g": 7.5,
        },
    }
    before = {
        "actor_id": "char_test",
        "sim_time": "2025-05-05T06:00:00+00:00",
        "location_name": "Kitchen",
        "energy": 80.0,
        "fatigue": 0.0,
        "hunger": 70.0,
        "thirst": 40.0,
        "sleepiness": 10.0,
        "cleanliness": 90.0,
    }
    after = {**before, "sim_time": "2025-05-05T06:20:00+00:00", "hunger": 40.0}

    text = format_action_completion(action, before, after, actor_name="Test Character")

    assert "🍽 Meal" in text
    assert "Apple · 1 piece" in text
    assert "Cooked Chicken Breast · 200 g" in text
    assert "425 kcal · P 62.5 g · C 25 g · F 7.5 g" in text


def test_legacy_target_based_nutrition_does_not_claim_structured_meal_items():
    action = {
        "action": "eat",
        "duration_minutes": 20,
        "target": "meal_target",
        "nutrition_intake": {"source": "nutrition-profiles-v1", "energy_kcal": 800.0},
    }
    state = {
        "actor_id": "char_test",
        "sim_time": "2025-05-05T06:00:00+00:00",
        "location_name": "Kitchen",
        "energy": 80.0,
        "fatigue": 0.0,
        "hunger": 70.0,
        "thirst": 40.0,
        "sleepiness": 10.0,
        "cleanliness": 90.0,
    }

    text = format_action_completion(action, state, state, actor_name="Test Character")

    assert "🍽 Meal" not in text

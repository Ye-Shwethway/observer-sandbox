from observer_sandbox.behavior_eval import SCENARIOS
from observer_sandbox.model_decision import load_autonomy_policy


def test_universal_autonomy_policy_is_character_agnostic_and_bounded():
    policy = load_autonomy_policy()
    assert policy["policy_revision"] == "universal-autonomy-v1-no-character-hardcoding"
    assert "entity_id" not in policy
    assert policy["decision_principles"]
    assert any("character-name-specific behavioral rule" in principle for principle in policy["decision_principles"])
    assert any("resource_awareness" in principle for principle in policy["decision_principles"])
    assert any("recent_usage" in principle for principle in policy["decision_principles"])
    assert any("Outdoor activity is never a quota" in principle for principle in policy["decision_principles"])
    assert policy["nutrition_policy"]["dietary_constraints"] == []
    assert "resting-energy reference" in policy["nutrition_policy"]["guidance"]
    assert policy["need_priorities"]["critical"]["sleepiness_gte"] > policy["need_priorities"]["strong"]["sleepiness_gte"]
    assert policy["need_priorities"]["strong"]["energy_lte"] == 40
    assert policy["need_priorities"]["strong"]["fatigue_gte"] == 55
    assert policy["need_priorities"]["critical"]["fatigue_gte"] == 70
    assert policy["need_priorities"]["strong"]["cleanliness_lte"] == 50
    assert {window["name"] for window in policy["routine_windows"]} == {
        "daytime_open",
        "evening_wind_down",
        "night_sleep",
    }
    assert all("Darian" not in window["guidance"] for window in policy["routine_windows"])
    assert policy["duration_guidance"]["quick_discretionary"]["inspect_minutes"] == [2, 6]
    assert policy["duration_guidance"]["critical_night_sleep"]["min_minutes"] >= 360
    assert policy["repetition_policy"]["recent_event_window"] >= 4
    assert "authored effect" in policy["repetition_policy"]["guidance"]
    assert "authored effects" in policy["reason_style"]


def test_behavior_matrix_covers_need_resolution_without_character_specific_routine_expectation():
    names = {scenario.name for scenario in SCENARIOS}
    assert names == {
        "strong_thirst",
        "strong_hunger",
        "high_sleep_pressure",
        "poor_cleanliness",
    }
    assert all(scenario.reason_keywords for scenario in SCENARIOS)

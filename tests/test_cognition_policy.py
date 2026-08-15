from observer_sandbox.behavior_eval import SCENARIOS
from observer_sandbox.model_decision import load_autonomy_policy


def test_darian_autonomy_policy_is_authored_and_bounded():
    policy = load_autonomy_policy()
    assert policy["entity_id"] == "char_darian"
    assert policy["policy_revision"] == "darian-autonomy-p1-v1.11-circadian-sleep-rhythm-v1"
    assert policy["decision_principles"]
    assert any("resource_awareness" in principle for principle in policy["decision_principles"])
    assert any("recent_usage" in principle for principle in policy["decision_principles"])
    assert any("familiar" in principle for principle in policy["decision_principles"])
    assert any("22:00" in principle for principle in policy["decision_principles"])
    assert policy["nutrition_policy"]["goal"]
    assert policy["nutrition_policy"]["energy_intent"]
    assert policy["nutrition_policy"]["protein_priority"]
    assert policy["nutrition_policy"]["dietary_constraints"] == []
    assert "resting-energy reference" in policy["nutrition_policy"]["guidance"]
    assert policy["need_priorities"]["critical"]["sleepiness_gte"] > policy["need_priorities"]["strong"]["sleepiness_gte"]
    assert policy["need_priorities"]["strong"]["energy_lte"] == 40
    assert policy["need_priorities"]["strong"]["fatigue_gte"] == 55
    assert policy["need_priorities"]["critical"]["fatigue_gte"] == 70
    assert policy["need_priorities"]["strong"]["cleanliness_lte"] == 50
    assert len(policy["routine_windows"]) == 4
    assert policy["duration_guidance"]["quick_discretionary"]["inspect_minutes"] == [2, 6]
    assert policy["duration_guidance"]["critical_night_sleep"]["min_minutes"] >= 360
    assert policy["repetition_policy"]["recent_event_window"] >= 4
    assert "authored effect" in policy["repetition_policy"]["guidance"]
    assert "leaves unchanged or worsens" in policy["reason_style"]


def test_behavior_matrix_covers_core_p1_intents_and_reason_grounding():
    names = {scenario.name for scenario in SCENARIOS}
    assert names == {
        "morning_ready",
        "strong_thirst",
        "strong_hunger",
        "high_sleep_pressure",
        "poor_cleanliness",
    }
    assert all(scenario.reason_keywords for scenario in SCENARIOS)

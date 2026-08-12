from observer_sandbox.behavior_eval import SCENARIOS
from observer_sandbox.model_decision import load_autonomy_policy


def test_darian_autonomy_policy_is_authored_and_bounded():
    policy = load_autonomy_policy()
    assert policy["entity_id"] == "char_darian"
    assert policy["policy_revision"] == "darian-autonomy-p1-v1"
    assert policy["decision_principles"]
    assert policy["need_priorities"]["critical"]["sleepiness_gte"] > policy["need_priorities"]["strong"]["sleepiness_gte"]
    assert len(policy["routine_windows"]) == 4
    assert policy["repetition_policy"]["recent_event_window"] >= 4


def test_behavior_matrix_covers_core_p1_intents():
    names = {scenario.name for scenario in SCENARIOS}
    assert names == {
        "morning_ready",
        "strong_thirst",
        "strong_hunger",
        "high_sleep_pressure",
        "poor_cleanliness",
    }

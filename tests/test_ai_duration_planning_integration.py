import json

from observer_sandbox import ai_runtime


def test_prompt_exposes_preferred_duration_separately_from_legal_range():
    state = {
        "action_options": [
            {
                "action": "inspect",
                "target": "obj_thorne_estate_kitchen_refrigerator",
                "target_name": "Refrigerator",
                "duration": (1, 60),
            }
        ]
    }
    prompt = ai_runtime._decision_prompt(state, ["inspect"])
    assert 'preferred_duration' in prompt
    assert 'quick refrigerator check' in prompt
    assert '1, 60' in prompt
    assert '2, 5' in prompt

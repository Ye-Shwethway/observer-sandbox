from observer_sandbox.duration_planning import normalize_duration


def test_model_requested_duration_is_normalized_before_runtime():
    assert normalize_duration("inspect", "obj_thorne_estate_kitchen_refrigerator", 15) == 5
    assert normalize_duration("train", "obj_thorne_estate_gym_heavy_bag", 60) == 45
    assert normalize_duration("train", "obj_thorne_estate_gym_free_weights", 30) == 45

from observer_sandbox.training_methods import training_profile_for_target


def test_outdoor_obstacle_course_uses_obstacle_conditioning_method():
    profile = training_profile_for_target("obj_thorne_estate_outdoor_obstacle_course")
    assert profile is not None
    assert profile["method_id"] == "obstacle_conditioning"
    assert profile["family"] == "conditioning"
    assert profile["planning"]["preferred_duration"] == [20, 45]

from observer_sandbox.duration_planning import duration_profile, enrich_action_options, normalize_duration


def test_generic_profiles_clamp_new_planning_without_changing_legality_bounds():
    assert normalize_duration("inspect", "obj_any", 15) == 6
    assert normalize_duration("inspect", "obj_any", 1) == 2
    assert normalize_duration("read", "obj_any", 120) == 60
    assert normalize_duration("drink", "obj_any", 10) == 5
    assert normalize_duration("sleep", "obj_any", 480) == 480


def test_target_profiles_override_generic_ranges():
    heavy_bag = "obj_thorne_estate_gym_heavy_bag"
    free_weights = "obj_thorne_estate_gym_free_weights"
    stove = "obj_thorne_estate_kitchen_stove"
    assert duration_profile("train", heavy_bag).min_minutes == 20
    assert duration_profile("train", heavy_bag).max_minutes == 45
    assert normalize_duration("train", heavy_bag, 60) == 45
    assert normalize_duration("train", free_weights, 30) == 45
    assert normalize_duration("use", stove, 60) == 30


def test_action_options_expose_broad_legal_and_narrow_preferred_ranges_separately():
    options = enrich_action_options([
        {
            "action": "inspect",
            "target": "obj_thorne_estate_kitchen_refrigerator",
            "target_name": "Refrigerator",
            "duration": (1, 60),
        },
        {
            "action": "sleep",
            "target": "obj_thorne_estate_master_bed",
            "target_name": "Bed",
            "duration": (30, 720),
        },
    ])
    inspect = options[0]
    assert inspect["duration"] == (1, 60)
    assert inspect["preferred_duration"] == (2, 5)
    assert inspect["duration_purpose"] == "quick refrigerator check"
    sleep = options[1]
    assert sleep["duration"] == (30, 720)
    assert "preferred_duration" not in sleep

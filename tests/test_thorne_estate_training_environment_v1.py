from observer_sandbox.world import load_world_seed


NEW_TRAINING_OBJECTS = {
    "obj_thorne_estate_training_ai_combat_sim": "loc_thorne_estate_training_hall",
    "obj_thorne_estate_training_obstacle_course": "loc_thorne_estate_training_hall",
    "obj_thorne_estate_training_combat_pit": "loc_thorne_estate_training_hall",
    "obj_thorne_estate_training_vr_tactical_sim": "loc_thorne_estate_training_hall",
    "obj_thorne_estate_gym_olympic_platform": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_power_rack": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_adjustable_bench": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_strength_machines": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_high_speed_treadmill": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_rowing_ergometer": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_speed_agility_station": "loc_thorne_estate_home_gym",
    "obj_thorne_estate_gym_altitude_chamber": "loc_thorne_estate_home_gym",
}


def test_training_environment_config_matches_bounded_canonical_expansion() -> None:
    world = load_world_seed()
    assert world["revision"] == "thorne-estate-v3.2-training-environment"
    by_id = {item["id"]: item for item in world["objects"]}

    for object_id, room_id in NEW_TRAINING_OBJECTS.items():
        assert by_id[object_id]["room"] == room_id
        assert by_id[object_id]["capabilities"] == ["train", "inspect"]
        assert by_id[object_id].get("effects", {}) == {}

    assert by_id["obj_thorne_estate_kitchen_drinking_water"]["effects"]["drink"]["needs.thirst"] == -55.0
    assert "loc_thorne_estate_exterior_boundary" in world["traversal_boundaries"]
    assert all("loc_thorne_estate_exterior_boundary" not in edge for edge in world["connections"])

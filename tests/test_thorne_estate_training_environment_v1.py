from __future__ import annotations

import json

from observer_sandbox.db import connect, migrate
from observer_sandbox.world import get_field, load_world_seed, seed_home_and_darian


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


def test_training_environment_seed_matches_bounded_canonical_expansion(tmp_path) -> None:
    world = load_world_seed()
    assert world["revision"] == "thorne-estate-v3.2-training-environment"

    by_id = {item["id"]: item for item in world["objects"]}
    assert by_id["obj_thorne_estate_gym_power_rack"]["capabilities"] == ["train", "inspect"]
    for object_id, room_id in NEW_TRAINING_OBJECTS.items():
        assert by_id[object_id]["room"] == room_id
        assert by_id[object_id]["capabilities"] == ["train", "inspect"]

    # Preserve the already-proven living physiology contract while enriching the gym.
    assert by_id["obj_thorne_estate_kitchen_drinking_water"]["effects"]["drink"]["needs.thirst"] == -55.0
    assert "loc_thorne_estate_exterior_boundary" in world["traversal_boundaries"]

    conn = connect(tmp_path / "observer.sqlite3")
    migrate(conn)
    seed_home_and_darian(conn)

    assert json.loads(conn.execute(
        "SELECT value_json FROM runtime_state WHERE key='world_identity_revision'"
    ).fetchone()[0]) == "thorne-estate-v3.2-training-environment"

    for object_id, room_id in NEW_TRAINING_OBJECTS.items():
        entity = conn.execute(
            "SELECT entity_type, capabilities_json FROM entities WHERE id=?", (object_id,)
        ).fetchone()
        assert entity is not None
        assert entity["entity_type"] == "object"
        assert json.loads(entity["capabilities_json"]) == ["train", "inspect"]
        assert conn.execute(
            "SELECT 1 FROM relations WHERE source_id=? AND relation_type='contains' AND target_id=?",
            (room_id, object_id),
        ).fetchone() is not None
        assert get_field(conn, object_id, "game.effects", None) == {}

    # The exterior remains authored but non-traversable.
    assert conn.execute(
        "SELECT 1 FROM relations WHERE relation_type='connected_to' "
        "AND (source_id='loc_thorne_estate_exterior_boundary' OR target_id='loc_thorne_estate_exterior_boundary')"
    ).fetchone() is None

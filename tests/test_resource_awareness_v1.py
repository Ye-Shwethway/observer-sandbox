from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
LIVING_ROOM = "loc_thorne_estate_living_room"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"

EXPECTED_GYM_TRAIN_TARGETS = {
    "obj_thorne_estate_gym_free_weights",
    "obj_thorne_estate_gym_heavy_bag",
    "obj_thorne_estate_gym_olympic_platform",
    "obj_thorne_estate_gym_power_rack",
    "obj_thorne_estate_gym_adjustable_bench",
    "obj_thorne_estate_gym_strength_machines",
    "obj_thorne_estate_gym_high_speed_treadmill",
    "obj_thorne_estate_gym_rowing_ergometer",
    "obj_thorne_estate_gym_speed_agility_station",
    "obj_thorne_estate_gym_altitude_chamber",
}


def _provider_state(conn):
    state = snapshot(conn, "char_darian")
    return ModelDecisionProvider(conn, character_id="char_darian")._enrich_state(state)


def test_home_gym_exposes_all_training_resources_to_cognition(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        conn.commit()
        enriched = _provider_state(conn)
        train_options = [option for option in enriched["action_options"] if option["action"] == "train"]
        targets = {option["target"] for option in train_options}
        assert EXPECTED_GYM_TRAIN_TARGETS <= targets
        assert all("training_method" in option for option in train_options)
        assert all("recent_usage" in option for option in train_options)


def test_reachable_room_preview_exposes_resources_but_does_not_make_them_directly_actionable(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", LIVING_ROOM)
        conn.commit()
        enriched = _provider_state(conn)
        previews = {item["location"]: item for item in enriched["resource_awareness"]["reachable_locations"]}
        gym = previews[HOME_GYM]
        resource_ids = {item["id"] for item in gym["resources"]}
        assert "obj_thorne_estate_gym_rowing_ergometer" in resource_ids
        assert "obj_thorne_estate_gym_speed_agility_station" in resource_ids
        assert "train" in gym["available_actions_after_move"]
        assert any(option["action"] == "move" and option["target"] == HOME_GYM for option in enriched["action_options"])
        assert not any(
            option["action"] == "train" and option["target"] in resource_ids
            for option in enriched["action_options"]
        )


def test_recent_training_usage_is_context_not_a_hard_block(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        conn.commit()
        apply_action(conn, Action("train", 30, FREE_WEIGHTS, "first strength session"), "char_darian")
        apply_action(conn, Action("train", 30, FREE_WEIGHTS, "second strength session"), "char_darian")
        enriched = _provider_state(conn)
        option = next(
            option for option in enriched["action_options"]
            if option["action"] == "train" and option["target"] == FREE_WEIGHTS
        )
        assert option["recent_usage"]["recent_uses"] >= 2
        assert option["recent_usage"]["recently_repeated"] is True

from __future__ import annotations

import json

from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.training_methods import load_training_method_catalog
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
TREADMILL = "obj_thorne_estate_gym_high_speed_treadmill"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"

EXPECTED_TARGETS = {
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
    "obj_thorne_estate_training_combat_mat",
    "obj_thorne_estate_training_practice_dummy",
    "obj_thorne_estate_training_ai_combat_sim",
    "obj_thorne_estate_training_obstacle_course",
    "obj_thorne_estate_training_combat_pit",
    "obj_thorne_estate_training_vr_tactical_sim",
}


def _prepare_gym(conn) -> None:
    set_field(conn, "char_darian", "runtime.location", HOME_GYM)
    set_field(conn, "char_darian", "runtime.current_action", "idle")
    set_field(conn, "char_darian", "needs.energy", 90.0)
    set_field(conn, "char_darian", "physiology.fatigue", 0.0, authority="physiology_engine", source="training-method-test")
    conn.commit()


def test_catalog_is_complete_and_descriptive_not_progression_authority() -> None:
    catalog = load_training_method_catalog()
    profiles = catalog["profiles"]
    assert catalog["revision"] == "training-method-semantics-v1"
    assert set(profiles) == EXPECTED_TARGETS
    for profile in profiles.values():
        assert profile["method_id"]
        assert profile["method_name"]
        assert profile["family"]
        assert profile["workload_channels"]
        assert isinstance(profile["tags"], list)
        assert "primary_domains" not in profile
        assert "progression" not in profile
        assert "stimulus" not in profile


def test_cognition_options_expose_authored_training_method(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_gym(conn)
        enriched = ModelDecisionProvider(conn)._enrich_state(snapshot(conn))
        treadmill = next(
            option
            for option in enriched["action_options"]
            if option.get("action") == "train" and option.get("target") == TREADMILL
        )
        method = treadmill["training_method"]
        assert method["method_id"] == "steady_state_cardio"
        assert method["family"] == "conditioning"
        assert method["workload_channels"] == ["conditioning"]
        assert method["source"] == "training-method-semantics-v1"


def test_completed_training_events_persist_method_evidence_without_changing_strength_mapping(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_gym(conn)
        apply_action(conn, Action("train", 30, TREADMILL, "steady aerobic work"))
        treadmill_event = conn.execute(
            "SELECT payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        treadmill_payload = json.loads(treadmill_event["payload_json"])
        assert treadmill_payload["training_method"]["method_id"] == "steady_state_cardio"
        assert treadmill_payload["training_method"]["effective_load"]["planned_minutes"] == 30
        assert treadmill_payload["training_method"]["workload_channels"] == ["conditioning"]
        assert "training_stimulus" not in treadmill_payload

        set_field(conn, "char_darian", "physiology.fatigue", 0.0, authority="physiology_engine", source="training-method-test")
        set_field(conn, "char_darian", "needs.energy", 90.0)
        conn.commit()
        apply_action(conn, Action("train", 60, FREE_WEIGHTS, "strength work"))
        strength_event = conn.execute(
            "SELECT payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        strength_payload = json.loads(strength_event["payload_json"])
        assert strength_payload["training_method"]["method_id"] == "free_weight_strength"
        assert strength_payload["training_stimulus"]["domain"] == "strength"
        assert strength_payload["training_stimulus"]["target"] == FREE_WEIGHTS

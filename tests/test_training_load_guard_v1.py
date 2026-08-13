from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.training_load_guard import projected_training_allowed, training_load_status
from observer_sandbox.training_modifiers import training_readiness_modifier
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"
POWER_RACK = "obj_thorne_estate_gym_power_rack"


def _setup(conn):
    set_field(conn, "char_darian", "runtime.location", HOME_GYM)
    conn.commit()


def test_two_45_minute_strength_blocks_exhaust_current_session_budget(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _setup(conn)
        apply_action(conn, Action("train", 45, FREE_WEIGHTS, "first block"), "char_darian")
        apply_action(conn, Action("train", 45, POWER_RACK, "second block"), "char_darian")

        state = snapshot(conn, "char_darian")
        status = training_load_status(conn, "char_darian", sim_time=state["sim_time"])
        enriched = ModelDecisionProvider(conn, character_id="char_darian")._enrich_state(state)
        train_options = [item for item in enriched["action_options"] if item["action"] == "train"]

        assert 85.0 <= status["session_effective_minutes"] <= 90.0
        assert status["remaining_effective_minutes"] < 10.0
        assert train_options == []
        assert enriched["training_load_guard"]["source"] == "training-session-load-recovery-guard-v1"


def test_short_recovery_does_not_erase_recent_training_dose(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _setup(conn)
        apply_action(conn, Action("train", 45, FREE_WEIGHTS, "first block"), "char_darian")
        apply_action(conn, Action("train", 45, POWER_RACK, "second block"), "char_darian")
        apply_action(conn, Action("rest", 121, None, "recover after training"), "char_darian")

        state = snapshot(conn, "char_darian")
        status = training_load_status(conn, "char_darian", sim_time=state["sim_time"])

        assert status["session_effective_minutes"] == 0.0
        assert status["recent_6h_effective_minutes"] > 80.0
        assert status["daily_24h_effective_minutes"] == status["recent_6h_effective_minutes"]
        assert status["remaining_effective_minutes"] < 40.0


def test_projected_training_is_checked_against_effective_load_not_raw_minutes(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _setup(conn)
        apply_action(conn, Action("train", 45, FREE_WEIGHTS, "first block"), "char_darian")
        state = snapshot(conn, "char_darian")
        status = training_load_status(conn, "char_darian", sim_time=state["sim_time"])
        readiness = training_readiness_modifier(state)

        assert projected_training_allowed(
            status,
            duration_minutes=30,
            effectiveness=readiness["effectiveness"],
        )
        assert not projected_training_allowed(
            status,
            duration_minutes=120,
            effectiveness=readiness["effectiveness"],
        )

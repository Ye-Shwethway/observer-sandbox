import json

import pytest

from observer_sandbox.actor_runtime import set_actor_runtime, set_retry
from observer_sandbox.autonomy_livelock_watchdog import authoritative_recovery_action
from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot, validate_action
from observer_sandbox.world import set_field


ACTOR = "char_darian"
TRAINING_HALL = "loc_thorne_estate_training_hall"
BAD_DESTINATION = "loc_thorne_estate_food_storage"
PAIR_ERROR = "Model selected an action/target pair outside authoritative action_options after one corrective retry"


def _seed_pair_errors(conn, sim_time: str, count: int = 2) -> None:
    for _ in range(count):
        conn.execute(
            "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
            (
                sim_time,
                ACTOR,
                "autonomy_error",
                json.dumps({
                    "stage": "decide",
                    "error_type": "ValueError",
                    "message": PAIR_ERROR,
                    "retry_seconds": 8.0,
                }),
            ),
        )
    set_retry(conn, ACTOR, {"failures": count, "retry_after": 9999999999.0, "last_error": "ValueError"})
    conn.commit()


def _bad_decision(*args, **kwargs):
    return {
        "action": "move",
        "target": BAD_DESTINATION,
        "duration_minutes": 10,
        "reason": "try the distant food-storage destination directly",
        "resources": [],
        "training_movements": [],
    }


def _live_freeze_state(conn):
    set_field(conn, ACTOR, "runtime.location", TRAINING_HALL)
    set_field(conn, ACTOR, "needs.thirst", 100.0)
    conn.commit()
    return snapshot(conn, ACTOR)


def test_third_repeated_pair_failure_recovers_from_authoritative_need_shaped_options(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = _live_freeze_state(conn)
        _seed_pair_errors(conn, state["sim_time"], 2)
        monkeypatch.setattr("observer_sandbox.model_decision.generate_character_decision", _bad_decision)

        action = ModelDecisionProvider(conn, character_id=ACTOR).choose(state, [])

        assert action.target != BAD_DESTINATION
        assert action.conditions["autonomy_recovery"]["source"] == "autonomy-livelock-watchdog-v1"
        assert action.conditions["autonomy_recovery"]["threshold"] == 3
        validate_action(conn, ACTOR, action)


def test_watchdog_does_not_replace_an_early_pair_validation_failure(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = _live_freeze_state(conn)
        _seed_pair_errors(conn, state["sim_time"], 1)
        monkeypatch.setattr("observer_sandbox.model_decision.generate_character_decision", _bad_decision)

        with pytest.raises(ValueError, match="outside authoritative action_options"):
            ModelDecisionProvider(conn, character_id=ACTOR).choose(state, [])


def test_watchdog_stays_fail_closed_in_canary_mode(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = _live_freeze_state(conn)
        _seed_pair_errors(conn, state["sim_time"], 2)
        set_actor_runtime(conn, ACTOR, autonomy_mode="canary_once")
        conn.commit()
        monkeypatch.setattr("observer_sandbox.model_decision.generate_character_decision", _bad_decision)

        with pytest.raises(ValueError, match="outside authoritative action_options"):
            ModelDecisionProvider(conn, character_id=ACTOR).choose(state, [])


def test_discretionary_recovery_prefers_idle():
    action = authoritative_recovery_action({
        "action_options": [
            {"action": "move", "target": "somewhere", "duration": (5, 15)},
            {"action": "idle", "target": None, "duration": (5, 60)},
        ],
        "decision_signals": {"highest_priority": None},
    })
    assert action is not None
    assert action.name == "idle"
    assert action.target is None

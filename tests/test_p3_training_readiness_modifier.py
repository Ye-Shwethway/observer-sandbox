from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, validate_action
from observer_sandbox.training_modifiers import training_readiness_modifier
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"


def _set_training_state(conn, *, energy: float, thirst: float, sleepiness: float, fatigue: float) -> None:
    set_field(conn, "char_darian", "runtime.location", HOME_GYM)
    set_field(conn, "char_darian", "needs.energy", energy)
    set_field(conn, "char_darian", "needs.thirst", thirst)
    set_field(conn, "char_darian", "needs.sleepiness", sleepiness)
    set_field(conn, "char_darian", "physiology.fatigue", fatigue, authority="physiology_engine", source="test")
    conn.commit()


def test_healthy_training_readiness_preserves_p3_1_fatigue_baseline(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_training_state(conn, energy=80.0, thirst=15.0, sleepiness=15.0, fatigue=0.0)

        options = action_options(conn)
        target = next(row for row in options if row["action"] == "train" and row["target"] == FREE_WEIGHTS)
        readiness = target["modifiers"]["training_readiness"]
        assert readiness["readiness"] == 1.0
        assert readiness["fatigue_cost_multiplier"] == 1.0

        after = apply_action(conn, Action("train", 60, FREE_WEIGHTS, "healthy readiness training"))
        assert after["fatigue"] == pytest.approx(18.5)


def test_degraded_but_legal_readiness_increases_training_fatigue_cost(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_training_state(conn, energy=50.0, thirst=45.0, sleepiness=45.0, fatigue=40.0)

        modifier = training_readiness_modifier({
            "energy": 50.0,
            "thirst": 45.0,
            "sleepiness": 45.0,
            "fatigue": 40.0,
        })
        assert 0.0 < modifier["readiness"] < 1.0
        assert 1.0 < modifier["fatigue_cost_multiplier"] <= 1.5

        after = apply_action(conn, Action("train", 60, FREE_WEIGHTS, "degraded readiness training"))
        assert after["fatigue"] > 58.5  # old fixed-cost result from a 40-fatigue start
        assert after["fatigue"] < 70.0


def test_training_readiness_is_persisted_with_action_and_completion_evidence(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_training_state(conn, energy=55.0, thirst=40.0, sleepiness=35.0, fatigue=30.0)
        apply_action(conn, Action("train", 30, FREE_WEIGHTS, "persist modifier evidence"))

        row = conn.execute(
            "SELECT id,modifiers_json,outcome_json FROM action_instances WHERE actor_id='char_darian' ORDER BY created_at DESC,id DESC LIMIT 1"
        ).fetchone()
        modifiers = json.loads(row["modifiers_json"])
        outcome = json.loads(row["outcome_json"])
        assert "training_readiness" in modifiers
        assert outcome["modifiers"]["training_readiness"] == modifiers["training_readiness"]

        event = conn.execute(
            "SELECT payload_json FROM events WHERE action_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
            (row["id"],),
        ).fetchone()
        payload = json.loads(event["payload_json"])
        assert payload["modifiers"]["training_readiness"] == modifiers["training_readiness"]


def test_hard_fatigue_condition_still_overrides_modifier_layer(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_training_state(conn, energy=90.0, thirst=5.0, sleepiness=5.0, fatigue=70.0)
        assert not any(row["action"] == "train" for row in action_options(conn))
        with pytest.raises(ValueError, match="fatigue"):
            validate_action(conn, "char_darian", Action("train", 60, FREE_WEIGHTS))

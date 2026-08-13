from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action
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


def test_training_effectiveness_is_distinct_from_fatigue_cost() -> None:
    healthy = training_readiness_modifier({
        "energy": 80.0,
        "thirst": 15.0,
        "sleepiness": 15.0,
        "fatigue": 0.0,
    })
    degraded = training_readiness_modifier({
        "energy": 50.0,
        "thirst": 45.0,
        "sleepiness": 45.0,
        "fatigue": 40.0,
    })

    assert healthy["effectiveness"] == 1.0
    assert healthy["fatigue_cost_multiplier"] == 1.0
    assert 0.0 < degraded["effectiveness"] < 1.0
    assert degraded["effectiveness"] == degraded["readiness"]
    assert degraded["fatigue_cost_multiplier"] > 1.0
    assert degraded["effectiveness"] < healthy["effectiveness"]


def test_training_effectiveness_persists_as_first_class_outcome_evidence(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_training_state(conn, energy=50.0, thirst=45.0, sleepiness=45.0, fatigue=40.0)
        reason = "P3.4 effectiveness evidence"
        after = apply_action(conn, Action("train", 60, FREE_WEIGHTS, reason))

        row = conn.execute(
            "SELECT id,modifiers_json,outcome_json FROM action_instances WHERE actor_id=? AND intent=? ORDER BY rowid DESC LIMIT 1",
            ("char_darian", reason),
        ).fetchone()
        assert row is not None
        modifiers = json.loads(row["modifiers_json"])
        outcome = json.loads(row["outcome_json"])
        training = modifiers["training_readiness"]

        assert training["effectiveness"] == pytest.approx(0.595)
        assert training["fatigue_cost_multiplier"] == pytest.approx(1.202)
        assert outcome["modifiers"]["training_readiness"] == training
        assert after["fatigue"] == pytest.approx(62.54)

        event = conn.execute(
            "SELECT payload_json FROM events WHERE action_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
            (row["id"],),
        ).fetchone()
        assert event is not None
        payload = json.loads(event["payload_json"])
        assert payload["modifiers"]["training_readiness"]["effectiveness"] == training["effectiveness"]


def test_p3_4_does_not_mutate_progression_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_training_state(conn, energy=80.0, thirst=15.0, sleepiness=15.0, fatigue=0.0)
        before = {
            row["skill_key"]: (row["score"], row["tier"], row["experience"])
            for row in conn.execute(
                "SELECT skill_key,score,tier,experience FROM character_skills WHERE entity_id=?",
                ("char_darian",),
            ).fetchall()
        }
        apply_action(conn, Action("train", 60, FREE_WEIGHTS, "no progression mutation"))
        after = {
            row["skill_key"]: (row["score"], row["tier"], row["experience"])
            for row in conn.execute(
                "SELECT skill_key,score,tier,experience FROM character_skills WHERE entity_id=?",
                ("char_darian",),
            ).fetchall()
        }
        assert after == before

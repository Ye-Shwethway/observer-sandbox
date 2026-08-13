from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"


def _set_state(
    conn,
    *,
    energy: float,
    hunger: float = 20.0,
    thirst: float,
    sleepiness: float,
    cleanliness: float = 80.0,
    fatigue: float,
) -> None:
    set_field(conn, "char_darian", "runtime.location", HOME_GYM)
    set_field(conn, "char_darian", "needs.energy", energy)
    set_field(conn, "char_darian", "needs.hunger", hunger)
    set_field(conn, "char_darian", "needs.thirst", thirst)
    set_field(conn, "char_darian", "needs.sleepiness", sleepiness)
    set_field(conn, "char_darian", "physiology.cleanliness", cleanliness)
    set_field(conn, "char_darian", "physiology.fatigue", fatigue, authority="physiology_engine", source="p3.5-test")
    conn.commit()


def _latest_action(conn, reason: str):
    return conn.execute(
        "SELECT id,modifiers_json,outcome_json FROM action_instances WHERE actor_id=? AND intent=? ORDER BY rowid DESC LIMIT 1",
        ("char_darian", reason),
    ).fetchone()


def test_healthy_effectiveness_preserves_full_training_load(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_state(conn, energy=80.0, thirst=15.0, sleepiness=15.0, fatigue=0.0)
        reason = "P3.5 healthy effective load"
        after = apply_action(conn, Action("train", 60, FREE_WEIGHTS, reason))

        assert after["energy"] == pytest.approx(68.0)
        assert after["hunger"] == pytest.approx(26.5)
        assert after["thirst"] == pytest.approx(24.0)
        assert after["sleepiness"] == pytest.approx(18.0)
        assert after["cleanliness"] == pytest.approx(73.2)
        assert after["fatigue"] == pytest.approx(18.5)

        row = _latest_action(conn, reason)
        outcome = json.loads(row["outcome_json"])
        assert outcome["training_load"] == {
            "planned_minutes": 60,
            "effectiveness": 1.0,
            "effective_minutes": 60.0,
            "source": "p3.5-effective-training-load-v1",
        }


def test_degraded_effectiveness_scales_immediate_workload_but_not_fatigue_inefficiency(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_state(conn, energy=50.0, thirst=45.0, sleepiness=45.0, fatigue=40.0)
        reason = "P3.5 degraded effective load"
        after = apply_action(conn, Action("train", 60, FREE_WEIGHTS, reason))

        # Effectiveness 0.595 scales training-specific energy/hunger/thirst/cleanliness load.
        # Passive drift remains full-duration, while fatigue keeps P3.3's 1.202x inefficiency cost.
        assert after["energy"] == pytest.approx(42.05)
        assert after["hunger"] == pytest.approx(24.88)
        assert after["thirst"] == pytest.approx(51.57)
        assert after["sleepiness"] == pytest.approx(48.0)
        assert after["cleanliness"] == pytest.approx(75.63)
        assert after["fatigue"] == pytest.approx(62.54)

        row = _latest_action(conn, reason)
        modifiers = json.loads(row["modifiers_json"])["training_readiness"]
        outcome = json.loads(row["outcome_json"])
        assert modifiers["effectiveness"] == 0.595
        assert modifiers["fatigue_cost_multiplier"] == 1.202
        assert outcome["training_load"]["planned_minutes"] == 60
        assert outcome["training_load"]["effectiveness"] == 0.595
        assert outcome["training_load"]["effective_minutes"] == pytest.approx(35.7)

        event = conn.execute(
            "SELECT payload_json FROM events WHERE action_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
            (row["id"],),
        ).fetchone()
        payload = json.loads(event["payload_json"])
        assert payload["training_load"] == outcome["training_load"]


def test_p3_5_does_not_create_long_term_progression(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_state(conn, energy=80.0, thirst=15.0, sleepiness=15.0, fatigue=0.0)
        before_skills = [tuple(row) for row in conn.execute(
            "SELECT skill_key,score,tier,experience FROM character_skills WHERE entity_id=? ORDER BY skill_key",
            ("char_darian",),
        ).fetchall()]

        apply_action(conn, Action("train", 60, FREE_WEIGHTS, "P3.5 no progression mutation"))

        after_skills = [tuple(row) for row in conn.execute(
            "SELECT skill_key,score,tier,experience FROM character_skills WHERE entity_id=? ORDER BY skill_key",
            ("char_darian",),
        ).fetchall()]
        assert after_skills == before_skills

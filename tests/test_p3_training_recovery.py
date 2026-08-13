from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.profile_observer import profile_menu, profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot, validate_action
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"


def test_training_adds_systemic_fatigue_and_recovery_reduces_it(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        set_field(conn, "char_darian", "needs.energy", 80.0)
        set_field(conn, "char_darian", "physiology.fatigue", 0.0)
        conn.commit()

        trained = apply_action(conn, Action("train", 60, FREE_WEIGHTS, "focused strength session"))
        assert trained["fatigue"] == pytest.approx(18.5)

        rested = apply_action(conn, Action("rest", 60, None, "recover after training"))
        assert rested["fatigue"] == pytest.approx(10.0)
        assert rested["fatigue"] < trained["fatigue"]


def test_high_fatigue_blocks_further_training_but_keeps_recovery_available(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        set_field(conn, "char_darian", "physiology.fatigue", 75.0)
        conn.commit()

        options = action_options(conn)
        assert not any(option["action"] == "train" for option in options)
        assert any(option["action"] == "rest" for option in options)
        with pytest.raises(ValueError, match="fatigue"):
            validate_action(conn, "char_darian", Action("train", 60, FREE_WEIGHTS))


def test_training_fatigue_is_recorded_as_action_state_change(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        set_field(conn, "char_darian", "physiology.fatigue", 0.0)
        conn.commit()

        apply_action(conn, Action("train", 30, FREE_WEIGHTS, "short training block"))
        row = conn.execute(
            "SELECT state_changes_json FROM events WHERE actor_id='char_darian' AND event_type='action_completed' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        changes = json.loads(row[0])
        assert "fatigue" in changes
        assert changes["fatigue"]["after"] > changes["fatigue"]["before"]


def test_recovery_section_surfaces_live_fatigue_without_copying_it_into_canonical_profile(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(
            conn,
            "char_darian",
            "physiology.fatigue",
            42.0,
            authority="physiology_engine",
            source="test",
        )
        conn.commit()

        menu = profile_menu(conn, "char_darian")
        assert any(section["id"] == "recovery" for section in menu["sections"])
        recovery = profile_section(conn, "char_darian", "recovery")
        assert recovery["content"][0]["field_key"] == "physiology.fatigue"
        assert recovery["content"][0]["label"] == "Systemic fatigue"
        assert recovery["content"][0]["value"] == 42.0
        assert conn.execute(
            "SELECT 1 FROM character_profile_values WHERE entity_id='char_darian' AND field_key='physiology.fatigue'"
        ).fetchone() is None


def test_recovery_section_is_visible_at_zero_before_first_persisted_change(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert conn.execute(
            "SELECT 1 FROM fields WHERE entity_id='char_darian' AND field_key='physiology.fatigue'"
        ).fetchone() is None
        menu = profile_menu(conn, "char_darian")
        assert any(section["id"] == "recovery" for section in menu["sections"])
        recovery = profile_section(conn, "char_darian", "recovery")
        assert recovery["content"][0]["value"] == 0.0
        assert recovery["content"][0]["mode"] == "simulated"


def test_snapshot_exposes_fatigue_as_current_simulated_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn)
        assert state["fatigue"] == 0.0

from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.represented_skill_runtime_batch import spec_for_action
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import settle_skill_progression


ACTOR = "char_darian"
BLADED = "bladed_weapons"
FIREARMS = "firearms"
PARENT = "weapon_mastery"
LEGACY = "weapons"
TRAINING_HALL = "loc_thorne_estate_training_hall"
PRACTICE_TARGET = "obj_thorne_estate_training_firearms_practice_simulator"
PRACTICE_METHOD = "firearms_handling_practice"
PROGRESSION_REVISION = "skill-progression-structured-evidence-v1.3-firearms"


def _skill(conn, key: str):
    row = conn.execute(
        "SELECT score,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return row


def _last_action_payload(conn, action_name: str) -> dict:
    for row in conn.execute(
        "SELECT payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC",
        (ACTOR,),
    ).fetchall():
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") == action_name:
            return payload
    raise AssertionError(f"No {action_name} action event found")


def test_initialize_seeds_dedicated_firearms_practice_and_activates_component_progression(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        target = conn.execute(
            "SELECT capabilities_json,definition_id FROM entities WHERE id=?",
            (PRACTICE_TARGET,),
        ).fetchone()
        assert target is not None
        assert set(json.loads(target["capabilities_json"])) == {"inspect", "practice"}
        assert target["definition_id"] == f"skill_practice:{PRACTICE_METHOD}"

        firearms = _skill(conn, FIREARMS)
        assert float(firearms["score"]) == pytest.approx(87.0)
        assert firearms["experience"] is None
        metadata = json.loads(firearms["metadata_json"] or "{}")
        assert metadata["progression_active"] is True
        assert metadata["progression_revision"] == PROGRESSION_REVISION

        parent = _skill(conn, PARENT)
        assert float(parent["score"]) == pytest.approx(87.0)
        assert parent["experience"] is None


def test_firearms_learning_target_is_distinct_from_application_simulator(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    firearm_spec = spec_for_action("firearm_drill")
    assert firearm_spec is not None
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        practice_targets = {
            option.get("target")
            for option in action_options(conn, ACTOR)
            if option.get("action") == "practice"
        }
        assert PRACTICE_TARGET in practice_targets
        assert firearm_spec.simulator_id not in practice_targets


def test_explicit_firearms_practice_progresses_only_firearms_and_rederives_parent(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        before_firearms = float(_skill(conn, FIREARMS)["score"])
        before_bladed = float(_skill(conn, BLADED)["score"])

        apply_action(
            conn,
            Action("practice", 30, PRACTICE_TARGET, "deliberate simulation-safe practice"),
            ACTOR,
        )
        evidence = _last_action_payload(conn, "practice")["skill_practice"]
        assert evidence["method_id"] == PRACTICE_METHOD
        assert evidence["skill_relevance"] == {FIREARMS: 1.0}
        assert "simulation_safe" in evidence["tags"]

        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, FIREARMS, as_of_sim_time=as_of)
        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert result["evidence"][0]["evidence_kind"] == "skill_practice"
        assert result["evidence"][0]["method_id"] == PRACTICE_METHOD

        firearms = _skill(conn, FIREARMS)
        bladed = _skill(conn, BLADED)
        parent = _skill(conn, PARENT)
        legacy = _skill(conn, LEGACY)
        new_firearms = float(firearms["score"])
        expected_parent = round((before_bladed + new_firearms) / 2.0, 6)

        assert new_firearms > before_firearms
        assert float(firearms["experience"]) > 0.0
        assert float(bladed["score"]) == pytest.approx(before_bladed)
        assert bladed["experience"] is None
        assert float(parent["score"]) == pytest.approx(expected_parent)
        assert parent["experience"] is None
        assert float(legacy["score"]) == pytest.approx(expected_parent)
        assert legacy["experience"] is None

        assert settle_skill_progression(conn, ACTOR, FIREARMS, as_of_sim_time=as_of) == {
            "settled": False,
            "reason": "no_new_learning_evidence",
            "skill_key": FIREARMS,
        }


def test_firearm_drill_remains_application_only_without_learning(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    firearm_spec = spec_for_action("firearm_drill")
    assert firearm_spec is not None
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, firearm_spec.room_id)
        conn.commit()
        before = {
            key: (float(_skill(conn, key)["score"]), _skill(conn, key)["experience"])
            for key in (BLADED, FIREARMS, PARENT, LEGACY)
        }
        apply_action(
            conn,
            Action("firearm_drill", 20, firearm_spec.simulator_id, "safe represented application"),
            ACTOR,
        )
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        assert settle_skill_progression(conn, ACTOR, FIREARMS, as_of_sim_time=as_of) == {
            "settled": False,
            "reason": "no_new_learning_evidence",
            "skill_key": FIREARMS,
        }
        assert settle_skill_progression(conn, ACTOR, PARENT, as_of_sim_time=as_of) == {
            "settled": False,
            "reason": "skill_not_represented",
            "skill_key": PARENT,
        }
        after = {
            key: (float(_skill(conn, key)["score"]), _skill(conn, key)["experience"])
            for key in (BLADED, FIREARMS, PARENT, LEGACY)
        }
        assert after == before

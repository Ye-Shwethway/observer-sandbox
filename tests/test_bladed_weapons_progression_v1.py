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
PRACTICE_TARGET = "obj_thorne_estate_training_bladed_weapons_practice_simulator"
PRACTICE_METHOD = "bladed_weapons_handling_practice"
PROGRESSION_REVISION = "skill-progression-structured-evidence-v1.2-bladed-weapons"


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


def test_initialize_seeds_dedicated_bladed_practice_and_activates_component_progression(tmp_path):
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

        bladed = _skill(conn, BLADED)
        assert float(bladed["score"]) == pytest.approx(87.0)
        assert bladed["experience"] is None
        metadata = json.loads(bladed["metadata_json"] or "{}")
        assert metadata["progression_active"] is True
        assert metadata["progression_revision"] == PROGRESSION_REVISION

        parent = _skill(conn, PARENT)
        assert parent["experience"] is None
        assert float(parent["score"]) == pytest.approx(87.0)


def test_practice_options_keep_learning_target_separate_from_blade_application(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    blade_spec = spec_for_action("blade_drill")
    assert blade_spec is not None
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        practice_targets = {
            option.get("target")
            for option in action_options(conn, ACTOR)
            if option.get("action") == "practice"
        }
        assert PRACTICE_TARGET in practice_targets
        assert blade_spec.simulator_id not in practice_targets


def test_explicit_bladed_practice_progresses_component_and_rederives_parent_once(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        before_bladed = float(_skill(conn, BLADED)["score"])
        before_firearms = float(_skill(conn, FIREARMS)["score"])

        apply_action(
            conn,
            Action("practice", 30, PRACTICE_TARGET, "deliberate simulation-safe practice"),
            ACTOR,
        )
        payload = _last_action_payload(conn, "practice")
        evidence = payload["skill_practice"]
        assert evidence["source"] == "skill-evidence-semantics-v1"
        assert evidence["method_id"] == PRACTICE_METHOD
        assert evidence["skill_relevance"] == {BLADED: 1.0}
        assert "simulation_safe" in evidence["tags"]

        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, BLADED, as_of_sim_time=as_of)
        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert result["evidence"][0]["evidence_kind"] == "skill_practice"
        assert result["evidence"][0]["method_id"] == PRACTICE_METHOD

        bladed = _skill(conn, BLADED)
        firearms = _skill(conn, FIREARMS)
        parent = _skill(conn, PARENT)
        legacy = _skill(conn, LEGACY)
        new_bladed = float(bladed["score"])
        expected_parent = round((new_bladed + before_firearms) / 2.0, 6)

        assert new_bladed > before_bladed
        assert float(bladed["experience"]) > 0.0
        assert float(firearms["score"]) == pytest.approx(before_firearms)
        assert firearms["experience"] is None
        assert float(parent["score"]) == pytest.approx(expected_parent)
        assert parent["experience"] is None
        assert float(legacy["score"]) == pytest.approx(expected_parent)
        assert legacy["experience"] is None

        duplicate = settle_skill_progression(conn, ACTOR, BLADED, as_of_sim_time=as_of)
        assert duplicate == {
            "settled": False,
            "reason": "no_new_learning_evidence",
            "skill_key": BLADED,
        }


def test_blade_drill_application_remains_non_learning_and_parent_has_no_direct_progression(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    blade_spec = spec_for_action("blade_drill")
    assert blade_spec is not None
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, blade_spec.room_id)
        conn.commit()
        before = {
            key: (float(_skill(conn, key)["score"]), _skill(conn, key)["experience"])
            for key in (BLADED, FIREARMS, PARENT, LEGACY)
        }

        apply_action(
            conn,
            Action("blade_drill", 20, blade_spec.simulator_id, "safe represented application"),
            ACTOR,
        )
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        bladed_result = settle_skill_progression(conn, ACTOR, BLADED, as_of_sim_time=as_of)
        assert bladed_result == {
            "settled": False,
            "reason": "no_new_learning_evidence",
            "skill_key": BLADED,
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


def test_bladed_progression_survives_reinitialize_without_overwriting_component_learning(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        apply_action(conn, Action("practice", 30, PRACTICE_TARGET, "practice"), ACTOR)
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, BLADED, as_of_sim_time=as_of)
        expected_bladed = result["new_score"]
        expected_experience = result["new_experience"]
        expected_firearms = float(_skill(conn, FIREARMS)["score"])
        expected_parent = round((expected_bladed + expected_firearms) / 2.0, 6)

    initialize(db)
    with connect(db) as conn:
        bladed = _skill(conn, BLADED)
        firearms = _skill(conn, FIREARMS)
        parent = _skill(conn, PARENT)
        legacy = _skill(conn, LEGACY)
        assert float(bladed["score"]) == pytest.approx(expected_bladed)
        assert float(bladed["experience"]) == pytest.approx(expected_experience)
        assert float(firearms["score"]) == pytest.approx(expected_firearms)
        assert firearms["experience"] is None
        assert float(parent["score"]) == pytest.approx(expected_parent)
        assert parent["experience"] is None
        assert float(legacy["score"]) == pytest.approx(expected_parent)
        assert legacy["experience"] is None

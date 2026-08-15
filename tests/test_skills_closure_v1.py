from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import settle_skill_progression


ACTOR = "char_darian"
TRAINING_HALL = "loc_thorne_estate_training_hall"
FIELD_MEDICINE = "field_medicine"
PRACTICE_METHOD = "field_medicine_scenario_practice"
PRACTICE_TARGET = "obj_thorne_estate_training_field_medicine_practice_simulator"
PROGRESSION_REVISION = "skill-progression-structured-evidence-v1.4-field-medicine"
DETERIORATION_FIELD = "medical.deterioration_risk"
LEARNED_SKILLS = {
    "hand_to_hand_combat",
    "bladed_weapons",
    "firearms",
    "survival",
    "tactical_planning",
    "technology",
    "field_medicine",
}
NON_SKILL_COMPATIBILITY_FIELDS = {
    "combat_skill",
    "weapons_proficiency",
    "survival_skill",
    "powerlifting_capacity",
    "focus_precision",
    "practical_skills",
    "technological_aptitude",
    "medical_knowledge",
}


def _skill(conn, key: str):
    row = conn.execute(
        "SELECT score,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return row


def _last_practice_evidence(conn) -> dict:
    rows = conn.execute(
        "SELECT payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC",
        (ACTOR,),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") == "practice":
            return payload["skill_practice"]
    raise AssertionError("No practice evidence found")


def test_field_medicine_practice_is_seeded_and_progression_activates_without_casualty(tmp_path):
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

        skill = _skill(conn, FIELD_MEDICINE)
        assert float(skill["score"]) == pytest.approx(75.0)
        assert skill["experience"] is None
        metadata = json.loads(skill["metadata_json"] or "{}")
        assert metadata["progression_active"] is True
        assert metadata["progression_revision"] == PROGRESSION_REVISION

        assert conn.execute(
            "SELECT COUNT(*) FROM fields WHERE field_key=?",
            (DETERIORATION_FIELD,),
        ).fetchone()[0] == 0


def test_field_medicine_scenario_practice_learns_without_creating_patient_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        practice_targets = {
            option.get("target")
            for option in action_options(conn, ACTOR)
            if option.get("action") == "practice"
        }
        assert PRACTICE_TARGET in practice_targets

        before = float(_skill(conn, FIELD_MEDICINE)["score"])
        apply_action(
            conn,
            Action("practice", 30, PRACTICE_TARGET, "abstract simulation-safe medical scenario"),
            ACTOR,
        )
        evidence = _last_practice_evidence(conn)
        assert evidence["method_id"] == PRACTICE_METHOD
        assert evidence["skill_relevance"] == {FIELD_MEDICINE: 1.0}
        assert "simulation_safe" in evidence["tags"]

        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, FIELD_MEDICINE, as_of_sim_time=as_of)
        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert result["evidence"][0]["evidence_kind"] == "skill_practice"
        assert result["evidence"][0]["method_id"] == PRACTICE_METHOD

        after = _skill(conn, FIELD_MEDICINE)
        assert float(after["score"]) > before
        assert float(after["experience"]) > 0.0
        assert conn.execute(
            "SELECT COUNT(*) FROM fields WHERE field_key=?",
            (DETERIORATION_FIELD,),
        ).fetchone()[0] == 0

        assert settle_skill_progression(conn, ACTOR, FIELD_MEDICINE, as_of_sim_time=as_of) == {
            "settled": False,
            "reason": "no_new_learning_evidence",
            "skill_key": FIELD_MEDICINE,
        }


def test_skills_v1_surface_is_shallow_and_compatibility_fields_are_not_new_skills(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        represented = {
            str(row[0])
            for row in conn.execute(
                "SELECT skill_key FROM character_skills WHERE entity_id=?",
                (ACTOR,),
            ).fetchall()
        }
        assert LEARNED_SKILLS <= represented
        assert "weapon_mastery" in represented
        assert "weapons" in represented
        assert NON_SKILL_COMPATIBILITY_FIELDS.isdisjoint(represented)

        for skill_key in LEARNED_SKILLS:
            row = _skill(conn, skill_key)
            assert row["score"] is not None

        assert _skill(conn, "weapon_mastery")["experience"] is None

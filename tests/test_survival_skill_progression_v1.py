from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import settle_skill_progression


ACTOR = "char_darian"
SKILL = "survival"
TRAINING_HALL = "loc_thorne_estate_training_hall"
NAVIGATION_TARGET = "obj_thorne_estate_training_field_navigation_practice_simulator"
SUSTAINMENT_TARGET = "obj_thorne_estate_training_field_sustainment_practice_station"
ORDINARY_OBSTACLE_COURSE = "obj_thorne_estate_training_obstacle_course"
CURRENT_PROGRESSION_REVISION = "skill-progression-structured-evidence-v1.3-firearms"


def _skill(conn, skill_key: str = SKILL):
    row = conn.execute(
        "SELECT score,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, skill_key),
    ).fetchone()
    assert row is not None
    return row


def _last_action_payload(conn, action_name: str) -> dict:
    rows = conn.execute(
        "SELECT payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC",
        (ACTOR,),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") == action_name:
            return payload
    raise AssertionError(f"No {action_name} action event found")


def test_initialize_seeds_survival_practice_targets_and_zero_gain_activation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        for target_id, method_id in (
            (NAVIGATION_TARGET, "field_navigation_practice"),
            (SUSTAINMENT_TARGET, "field_sustainment_practice"),
        ):
            target = conn.execute(
                "SELECT capabilities_json,definition_id FROM entities WHERE id=?", (target_id,)
            ).fetchone()
            assert target is not None
            assert "practice" in json.loads(target["capabilities_json"])
            assert target["definition_id"] == f"skill_practice:{method_id}"

        row = _skill(conn)
        assert float(row["score"]) == pytest.approx(85.0)
        assert row["experience"] is None
        metadata = json.loads(row["metadata_json"] or "{}")
        assert metadata["progression_active"] is True
        assert metadata["progression_revision"] == CURRENT_PROGRESSION_REVISION


def test_action_options_expose_only_explicit_survival_practice_targets(tmp_path):
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
        assert NAVIGATION_TARGET in practice_targets
        assert SUSTAINMENT_TARGET in practice_targets
        assert ORDINARY_OBSTACLE_COURSE not in practice_targets


@pytest.mark.parametrize(
    ("target_id", "method_id"),
    [
        (NAVIGATION_TARGET, "field_navigation_practice"),
        (SUSTAINMENT_TARGET, "field_sustainment_practice"),
    ],
)
def test_registered_survival_practice_emits_evidence_and_progresses_once(
    tmp_path, target_id: str, method_id: str
):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        before = float(_skill(conn)["score"])

        apply_action(conn, Action("practice", 30, target_id, "deliberate survival practice"), ACTOR)
        payload = _last_action_payload(conn, "practice")
        evidence = payload["skill_practice"]
        assert evidence["source"] == "skill-evidence-semantics-v1"
        assert evidence["method_id"] == method_id
        assert evidence["skill_relevance"] == {"survival": 1.0}
        assert float(evidence["effective_load"]["effective_minutes"]) == pytest.approx(30.0)

        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert result["evidence"][0]["evidence_kind"] == "skill_practice"
        assert result["evidence"][0]["method_id"] == method_id
        assert float(_skill(conn)["score"]) > before

        duplicate = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert duplicate == {"settled": False, "reason": "no_new_learning_evidence", "skill_key": SKILL}


def test_survival_practice_does_not_progress_technology(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        technology_before = _skill(conn, "technology")
        technology_score = float(technology_before["score"])
        technology_experience = technology_before["experience"]

        apply_action(conn, Action("practice", 30, NAVIGATION_TARGET, "navigation practice"), ACTOR)
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, "technology", as_of_sim_time=as_of)
        technology_after = _skill(conn, "technology")

        assert result == {
            "settled": False,
            "reason": "no_new_learning_evidence",
            "skill_key": "technology",
        }
        assert float(technology_after["score"]) == pytest.approx(technology_score)
        assert technology_after["experience"] == technology_experience


def test_survival_progression_survives_reinitialize(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        conn.commit()
        apply_action(conn, Action("practice", 30, NAVIGATION_TARGET, "navigation practice"), ACTOR)
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        expected_score = result["new_score"]
        expected_experience = result["new_experience"]

    initialize(db)
    with connect(db) as conn:
        row = _skill(conn)
        assert float(row["score"]) == pytest.approx(expected_score)
        assert float(row["experience"]) == pytest.approx(expected_experience)

from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.skill_progression import SETTLEMENT_EVENT_TYPE, settle_skill_progression


ACTOR = "char_darian"
TRAINING_HALL = "loc_thorne_estate_training_hall"
VR_TACTICAL = "obj_thorne_estate_training_vr_tactical_sim"
AI_COMBAT = "obj_thorne_estate_training_ai_combat_sim"
COMBAT_MAT = "obj_thorne_estate_training_combat_mat"
SKILL = "tactical_planning"


def _skill(conn):
    row = conn.execute(
        "SELECT score,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, SKILL),
    ).fetchone()
    assert row is not None
    return row


def _settlements(conn):
    rows = conn.execute(
        "SELECT id,payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
        (ACTOR, SETTLEMENT_EVENT_TYPE),
    ).fetchall()
    return [
        json.loads(row["payload_json"] or "{}")
        for row in rows
        if json.loads(row["payload_json"] or "{}").get("skill_key") == SKILL
    ]


def _train(conn, target: str, minutes: int = 30) -> str:
    set_dynamic_location(conn, ACTOR, TRAINING_HALL)
    conn.commit()
    apply_action(conn, Action("train", minutes, target, "tactical progression acceptance fixture"), ACTOR)
    return str(snapshot(conn, ACTOR)["sim_time"])


def test_initialize_bootstraps_tactical_planning_without_retroactive_gain(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        row = _skill(conn)
        settlements = _settlements(conn)
        assert float(row["score"]) == pytest.approx(92.0)
        assert row["experience"] is None
        assert len(settlements) == 1
        assert settlements[0]["bootstrap"] is True
        assert settlements[0]["score_delta"] == 0.0
        assert settlements[0]["experience_gain"] == 0.0
        metadata = json.loads(row["metadata_json"] or "{}")
        assert metadata["progression_active"] is True


def test_vr_tactical_drill_progresses_tactical_planning_once(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        as_of = _train(conn, VR_TACTICAL, 30)
        before = float(_skill(conn)["score"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        after = _skill(conn)

        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["evidence"][0]["method_id"] == "vr_tactical_drills"
        assert result["evidence"][0]["method_weight"] == pytest.approx(1.0)
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert float(after["score"]) > before

        again = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert again == {"settled": False, "reason": "no_new_learning_evidence", "skill_key": SKILL}


def test_ai_combat_simulation_can_cross_train_tactical_planning_at_reduced_weight(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        as_of = _train(conn, AI_COMBAT, 30)
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)

        assert result["settled"] is True
        assert result["evidence"][0]["method_id"] == "ai_combat_simulation"
        assert result["evidence"][0]["method_weight"] == pytest.approx(0.8)
        assert result["score_delta"] > 0.0


def test_non_tactical_combat_method_does_not_progress_tactical_planning(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = _skill(conn)
        as_of = _train(conn, COMBAT_MAT, 30)
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        after = _skill(conn)

        assert result == {"settled": False, "reason": "no_new_learning_evidence", "skill_key": SKILL}
        assert float(after["score"]) == pytest.approx(float(before["score"]))
        assert after["experience"] == before["experience"]


def test_reinitialize_preserves_tactical_progression_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        as_of = _train(conn, VR_TACTICAL, 30)
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        expected_score = result["new_score"]
        expected_experience = result["new_experience"]

    initialize(db)
    with connect(db) as conn:
        row = _skill(conn)
        assert float(row["score"]) == pytest.approx(expected_score)
        assert float(row["experience"]) == pytest.approx(expected_experience)

from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.skill_progression import (
    proficiency_factor,
    saturation_factor,
    settle_skill_progression,
)


ACTOR = "char_darian"
HOME_GYM = "loc_thorne_estate_home_gym"
HEAVY_BAG = "obj_thorne_estate_gym_heavy_bag"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"
SKILL = "hand_to_hand_combat"


def _skill(conn):
    row = conn.execute(
        "SELECT score,tier,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, SKILL),
    ).fetchone()
    assert row is not None
    return row


def _train(conn, target: str, minutes: int = 30) -> str:
    set_dynamic_location(conn, ACTOR, HOME_GYM)
    conn.commit()
    apply_action(conn, Action("train", minutes, target, "bounded progression test"), ACTOR)
    return str(snapshot(conn, ACTOR)["sim_time"])


def test_reinitialize_preserves_progression_active_and_extra_learned_skills(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        row = _skill(conn)
        metadata = json.loads(row["metadata_json"] or "{}")
        metadata.update({"progression_active": True, "progression_revision": "test"})
        conn.execute(
            "UPDATE character_skills SET score=91.25,experience=2.5,metadata_json=? WHERE entity_id=? AND skill_key=?",
            (json.dumps(metadata), ACTOR, SKILL),
        )
        conn.execute(
            "INSERT INTO character_skills(entity_id,skill_key,category,score,experience,metadata_json) VALUES(?,?,?,?,?,?)",
            (ACTOR, "learned_future_skill", "test", 12.0, 1.0, json.dumps({"progression_active": True})),
        )
        conn.commit()

    initialize(db)
    with connect(db) as conn:
        row = _skill(conn)
        assert float(row["score"]) == pytest.approx(91.25)
        assert float(row["experience"]) == pytest.approx(2.5)
        assert conn.execute(
            "SELECT score FROM character_skills WHERE entity_id=? AND skill_key='learned_future_skill'",
            (ACTOR,),
        ).fetchone() is not None


def test_first_settlement_bootstraps_without_retroactive_progression(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        as_of = _train(conn, HEAVY_BAG, 30)
        before = _skill(conn)
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        after = _skill(conn)

        assert result["settled"] is True
        assert result["bootstrap"] is True
        assert result["consumed_action_event_ids"]
        assert float(after["score"]) == pytest.approx(float(before["score"]))
        assert after["experience"] is None
        metadata = json.loads(after["metadata_json"] or "{}")
        assert metadata["progression_active"] is True


def test_future_combat_training_progresses_score_and_experience_once(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        # Establish a clean activation cursor; historical/pre-activation work is not XP.
        initial_time = str(snapshot(conn, ACTOR)["sim_time"])
        boot = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=initial_time)
        assert boot["bootstrap"] is True

        as_of = _train(conn, HEAVY_BAG, 30)
        before = float(_skill(conn)["score"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        after = _skill(conn)

        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["evidence"][0]["method_id"] == "heavy_bag_rounds"
        assert result["experience_gain"] > 0.0
        assert result["score_delta"] > 0.0
        assert float(after["score"]) > before
        assert float(after["experience"]) == pytest.approx(result["new_experience"])

        again = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        unchanged = _skill(conn)
        assert again == {"settled": False, "reason": "no_new_learning_evidence", "skill_key": SKILL}
        assert float(unchanged["score"]) == pytest.approx(float(after["score"]))
        assert float(unchanged["experience"]) == pytest.approx(float(after["experience"]))


def test_noncombat_strength_training_does_not_progress_hand_to_hand(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        initial_time = str(snapshot(conn, ACTOR)["sim_time"])
        settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=initial_time)
        before = _skill(conn)
        as_of = _train(conn, FREE_WEIGHTS, 30)
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        after = _skill(conn)

        assert result == {"settled": False, "reason": "no_new_learning_evidence", "skill_key": SKILL}
        assert float(after["score"]) == pytest.approx(float(before["score"]))
        assert after["experience"] == before["experience"]


def test_diminishing_returns_and_recent_practice_saturation_are_bounded():
    assert proficiency_factor(60.0) == pytest.approx(1.0)
    assert proficiency_factor(90.0) == pytest.approx(0.25)
    assert proficiency_factor(99.0) == pytest.approx(0.05)
    assert proficiency_factor(100.0) == pytest.approx(0.05)

    assert saturation_factor(0.0, half_units=2.0) == pytest.approx(1.0)
    assert saturation_factor(2.0, half_units=2.0) == pytest.approx(0.5)
    assert 0.1 <= saturation_factor(100.0, half_units=2.0) <= 1.0

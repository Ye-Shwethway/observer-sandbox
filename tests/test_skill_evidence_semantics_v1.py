from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import settle_skill_progression

ACTOR = "char_darian"
SKILL = "technology"
COMMS = "loc_thorne_estate_comms"
PRACTICE_CONSOLE = "obj_thorne_estate_comms_diagnostic_practice_console"
ORDINARY_TERMINAL = "obj_thorne_estate_comms_secure_terminal"


def _skill(conn):
    row = conn.execute(
        "SELECT score,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, SKILL),
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


def test_initialize_seeds_only_explicit_practice_target_and_zero_gain_activation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        action = conn.execute(
            "SELECT min_duration_minutes,required_capability,target_mode FROM action_definitions WHERE action_type='practice'"
        ).fetchone()
        assert action is not None
        assert int(action["min_duration_minutes"]) == 10
        assert action["required_capability"] == "practice"
        assert action["target_mode"] == "object"

        target = conn.execute(
            "SELECT capabilities_json,definition_id FROM entities WHERE id=?", (PRACTICE_CONSOLE,)
        ).fetchone()
        assert target is not None
        assert "practice" in json.loads(target["capabilities_json"])
        assert target["definition_id"] == "skill_practice:systems_diagnostic_practice"

        row = _skill(conn)
        assert float(row["score"]) == pytest.approx(82.0)
        assert row["experience"] is None
        metadata = json.loads(row["metadata_json"] or "{}")
        assert metadata["progression_active"] is True


def test_action_options_do_not_reinterpret_ordinary_terminal_as_practice(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, COMMS)
        conn.commit()
        options = action_options(conn, ACTOR)
        practice_targets = {
            option.get("target") for option in options if option.get("action") == "practice"
        }
        assert PRACTICE_CONSOLE in practice_targets
        assert ORDINARY_TERMINAL not in practice_targets


def test_practice_emits_structured_evidence_and_progresses_technology_once(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, COMMS)
        conn.commit()
        before = float(_skill(conn)["score"])

        apply_action(conn, Action("practice", 30, PRACTICE_CONSOLE, "systems diagnostic practice"), ACTOR)
        payload = _last_action_payload(conn, "practice")
        evidence = payload["skill_practice"]
        assert evidence["source"] == "skill-evidence-semantics-v1"
        assert evidence["method_id"] == "systems_diagnostic_practice"
        assert evidence["skill_relevance"] == {"technology": 1.0}
        assert float(evidence["effective_load"]["effective_minutes"]) == pytest.approx(30.0)

        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert result["evidence"][0]["evidence_kind"] == "skill_practice"
        assert result["evidence"][0]["method_id"] == "systems_diagnostic_practice"
        assert float(_skill(conn)["score"]) > before

        duplicate = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert duplicate == {"settled": False, "reason": "no_new_learning_evidence", "skill_key": SKILL}


def test_generic_use_does_not_emit_skill_practice_or_progress_technology(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, COMMS)
        conn.commit()
        before = _skill(conn)
        apply_action(conn, Action("use", 20, ORDINARY_TERMINAL, "ordinary communications use"), ACTOR)
        payload = _last_action_payload(conn, "use")
        assert "skill_practice" not in payload
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        after = _skill(conn)
        assert result == {"settled": False, "reason": "no_new_learning_evidence", "skill_key": SKILL}
        assert float(after["score"]) == pytest.approx(float(before["score"]))
        assert after["experience"] == before["experience"]


def test_practice_duration_and_reseed_safety(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, COMMS)
        conn.commit()
        with pytest.raises(ValueError, match="duration must be between 10 and 180"):
            apply_action(conn, Action("practice", 5, PRACTICE_CONSOLE, "too short"), ACTOR)

        apply_action(conn, Action("practice", 30, PRACTICE_CONSOLE, "valid practice"), ACTOR)
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        expected_score = result["new_score"]
        expected_experience = result["new_experience"]

    initialize(db)
    with connect(db) as conn:
        row = _skill(conn)
        assert float(row["score"]) == pytest.approx(expected_score)
        assert float(row["experience"]) == pytest.approx(expected_experience)

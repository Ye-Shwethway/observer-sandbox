from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import maybe_settle_skill_progression
from observer_sandbox.tactical_assessment_runtime import (
    ASSESS_ACTION,
    SIMULATOR_DEFINITION_ID,
    SIMULATOR_ID,
    SIMULATOR_ROOM_ID,
    assess_tactical_assessment_action,
    tactical_assessment_outcome,
)
from observer_sandbox.world import set_field


def _move_darian_to_simulator(conn) -> None:
    set_field(conn, "char_darian", "runtime.location", SIMULATOR_ROOM_ID)
    set_field(conn, "char_darian", "runtime.current_action", "idle")
    conn.commit()


def test_runtime_seed_registers_distinct_tactical_simulator_and_assess_action(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        action = conn.execute(
            "SELECT action_type,target_mode,required_capability,requires_colocation FROM action_definitions WHERE action_type=?",
            (ASSESS_ACTION,),
        ).fetchone()
        assert action is not None
        assert action["target_mode"] == "object"
        assert action["required_capability"] == ASSESS_ACTION
        assert action["requires_colocation"] == 1

        simulator = conn.execute(
            "SELECT entity_type,definition_id,capabilities_json FROM entities WHERE id=?",
            (SIMULATOR_ID,),
        ).fetchone()
        assert simulator is not None
        assert simulator["entity_type"] == "object"
        assert simulator["definition_id"] == SIMULATOR_DEFINITION_ID
        assert not simulator["definition_id"].startswith("skill_practice:")
        capabilities = set(json.loads(simulator["capabilities_json"]))
        assert {"inspect", "assess", "situational_intelligence"}.issubset(capabilities)
        assert conn.execute(
            "SELECT 1 FROM relations WHERE source_id=? AND relation_type='contains' AND target_id=?",
            (SIMULATOR_ROOM_ID, SIMULATOR_ID),
        ).fetchone() is not None
        assert SIMULATOR_ID not in {
            "obj_thorne_estate_training_vr_tactical",
            "obj_thorne_estate_training_ai_combat_sim",
        }


def test_action_options_expose_tactical_assessment_to_cognition_only_when_colocated(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert not any(
            item["action"] == ASSESS_ACTION and item.get("target") == SIMULATOR_ID
            for item in action_options(conn, "char_darian")
        )
        _move_darian_to_simulator(conn)
        options = action_options(conn, "char_darian")
        assess = next(
            item
            for item in options
            if item["action"] == ASSESS_ACTION and item["target"] == SIMULATOR_ID
        )
        assert assess["target_name"] == "Tactical Situation Assessment Simulator"

        enriched = ModelDecisionProvider(conn, character_id="char_darian")._enrich_state(
            snapshot(conn, "char_darian")
        )
        assert any(
            item["action"] == ASSESS_ACTION and item["target"] == SIMULATOR_ID
            for item in enriched["action_options"]
        )
        tactical = next(
            item
            for item in enriched["capability_awareness"]["skills"]
            if item["skill_id"] == "tactical_planning"
        )
        assert any(
            app["application_id"] == "assess_tactical_situation"
            for app in tactical["applications"]
        )
        assert (
            enriched["capability_awareness"]["reasoning_profile"]["factors"]
            ["general_reasoning_capacity"]["value"]
            == 140
        )


def test_darian_tactical_assessment_is_supported_and_deterministic(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assessment = assess_tactical_assessment_action(conn, "char_darian", SIMULATOR_ID)
        assert assessment.status == "supported"
        assert assessment.capability.skill_score == pytest.approx(92.0)
        assert assessment.capability.proficiency_grade == "S"
        assert assessment.recognized_resource_capabilities == ("situational_intelligence",)

        first = tactical_assessment_outcome(conn, "char_darian", SIMULATOR_ID)
        second = tactical_assessment_outcome(conn, "char_darian", SIMULATOR_ID)
        assert first == second
        assert first["outcome_class"] == "strong"
        assert first["indices"]["quality_precision"] == pytest.approx(0.996912, abs=1e-6)
        assert first["indices"]["information_gained"] == pytest.approx(1.0, abs=1e-6)
        assert first["indices"]["partial_failure_recovery"] == pytest.approx(1.0, abs=1e-6)
        assert first["learning_evidence"] is False

        factor_keys = {
            contribution["field_key"]
            for dimension in first["cognitive_performance"]["dimensions"]
            for contribution in dimension["factor_contributions"]
        }
        assert "raps_ia.iq" in factor_keys
        assert "raps_ia.problem_solving" in factor_keys
        assert "raps_ma.focus" in factor_keys
        assert "raps_ma.adaptability" in factor_keys
        assert "raps_ia.tactical_thinking" not in factor_keys


def test_missing_supporting_intelligence_is_constrained_not_hard_blocked(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        target = "obj_tactical_assessment_without_support"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            (
                target,
                "object",
                "Tactical Assessment Without Intelligence Support",
                json.dumps(["inspect", "assess"]),
                SIMULATOR_DEFINITION_ID,
            ),
        )
        result = assess_tactical_assessment_action(conn, "char_darian", target)
        assert result.status == "constrained"
        outcome = tactical_assessment_outcome(conn, "char_darian", target)
        assert outcome["support_multiplier"] == pytest.approx(0.92)
        assert outcome["indices"]["quality_precision"] < 0.996912


def test_completed_assess_action_writes_application_evidence_but_no_tactical_learning(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_darian_to_simulator(conn)
        skill_before = conn.execute(
            "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key='tactical_planning'"
        ).fetchone()
        action = Action(
            ASSESS_ACTION,
            30,
            SIMULATOR_ID,
            "assess the represented tactical situation before choosing a course of action",
        )
        apply_action(conn, action, "char_darian", action_id="tactical-runtime-test-action")

        instance = conn.execute(
            "SELECT status,outcome_json FROM action_instances WHERE id='tactical-runtime-test-action'"
        ).fetchone()
        assert instance["status"] == "completed"
        outcome = json.loads(instance["outcome_json"])
        assert outcome["represented_skill_task"]["outcome_class"] == "strong"
        assert outcome["skill_application"]["learning_evidence"] is False

        rows = conn.execute(
            "SELECT event_type,payload_json,caused_by_event_id FROM events WHERE action_id=? ORDER BY id",
            ("tactical-runtime-test-action",),
        ).fetchall()
        assert [row["event_type"] for row in rows] == [
            "action_completed",
            "skill_application_evidence",
        ]
        evidence = json.loads(rows[1]["payload_json"])
        assert evidence["skill_id"] == "tactical_planning"
        assert evidence["application_id"] == "assess_tactical_situation"
        assert evidence["learning_evidence"] is False
        assert rows[1]["caused_by_event_id"] is not None

        # Application evidence must not be reinterpreted by the existing Tactical
        # training progression consumer as learning/XP evidence.
        maybe_settle_skill_progression(
            conn,
            "char_darian",
            as_of_sim_time=snapshot(conn, "char_darian")["sim_time"],
        )
        skill_after = conn.execute(
            "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key='tactical_planning'"
        ).fetchone()
        assert tuple(skill_after) == tuple(skill_before)


def test_reapplying_completed_action_id_is_idempotent_for_application_evidence(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_darian_to_simulator(conn)
        action = Action(ASSESS_ACTION, 20, SIMULATOR_ID, "repeatable tactical assessment fixture")
        apply_action(conn, action, "char_darian", action_id="tactical-assessment-idempotency")
        first_count = conn.execute(
            "SELECT COUNT(*) FROM events WHERE action_id='tactical-assessment-idempotency'"
        ).fetchone()[0]
        apply_action(conn, action, "char_darian", action_id="tactical-assessment-idempotency")
        second_count = conn.execute(
            "SELECT COUNT(*) FROM events WHERE action_id='tactical-assessment-idempotency'"
        ).fetchone()[0]
        assert first_count == second_count == 2


def test_high_iq_actor_without_tactical_skill_fails_closed_and_rolls_back(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        actor = "char_no_tactical_fixture"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
            (actor, "character", "No Tactical Fixture", "{}", "[]"),
        )
        conn.execute(
            "INSERT INTO character_profiles(entity_id,profile_schema_version,canonical_revision,status) VALUES(?,?,?,?)",
            (actor, 1, "no-tactical-runtime-test", "active"),
        )
        for field_key, value in {
            "raps_ia.iq": 180.0,
            "raps_ia.problem_solving": 100.0,
            "raps_ma.focus": 100.0,
            "raps_ma.adaptability": 100.0,
            "raps_ia.tactical_thinking": 100.0,
        }.items():
            conn.execute(
                """
                INSERT INTO character_profile_values(
                    entity_id,field_key,value_json,mode,authority,source
                ) VALUES(?,?,?,?,?,?)
                """,
                (actor, field_key, json.dumps(value), "static", "test", "test"),
            )
        set_field(conn, actor, "runtime.location", SIMULATOR_ROOM_ID)
        set_field(conn, actor, "runtime.current_action", "idle")
        set_field(conn, actor, "needs.energy", 75.0)
        set_field(conn, actor, "needs.hunger", 20.0)
        set_field(conn, actor, "needs.thirst", 15.0)
        set_field(conn, actor, "needs.sleepiness", 15.0)
        set_field(conn, actor, "physiology.cleanliness", 80.0)
        set_field(conn, actor, "physiology.fatigue", 0.0)
        conn.commit()

        before_state = snapshot(conn, actor)
        before_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        with pytest.raises(Exception, match="no authoritative Skill state"):
            apply_action(
                conn,
                Action(
                    ASSESS_ACTION,
                    30,
                    SIMULATOR_ID,
                    "IQ and legacy tactical-thinking aliases cannot substitute for learned Tactical Planning",
                ),
                actor,
                action_id="unsupported-tactical-assessment",
            )

        assert snapshot(conn, actor) == before_state
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='unsupported-tactical-assessment'"
        ).fetchone() is None
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == before_events


def test_wrong_assess_target_definition_fails_before_commit(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_darian_to_simulator(conn)
        wrong = "obj_wrong_tactical_assessment_target"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            (
                wrong,
                "object",
                "Wrong Tactical Assessment Target",
                json.dumps(["assess", "inspect", "situational_intelligence"]),
                "represented_task:not_the_authorized_tactical_assessment_simulator",
            ),
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
            (SIMULATOR_ROOM_ID, "contains", wrong),
        )
        conn.commit()
        before = snapshot(conn, "char_darian")

        with pytest.raises(Exception, match="expected"):
            apply_action(
                conn,
                Action(ASSESS_ACTION, 20, wrong, "wrong target must fail exact binding"),
                "char_darian",
                action_id="wrong-tactical-assessment-target-action",
            )
        assert snapshot(conn, "char_darian") == before
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='wrong-tactical-assessment-target-action'"
        ).fetchone() is None

from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.technology_diagnostic_runtime import (
    DIAGNOSE_ACTION,
    SIMULATOR_DEFINITION_ID,
    SIMULATOR_ID,
    SIMULATOR_ROOM_ID,
    assess_technology_diagnostic_action,
    technology_diagnostic_outcome,
)
from observer_sandbox.world import set_field


def _move_darian_to_simulator(conn) -> None:
    set_field(conn, "char_darian", "runtime.location", SIMULATOR_ROOM_ID)
    set_field(conn, "char_darian", "runtime.current_action", "idle")
    conn.commit()


def test_runtime_seed_registers_exact_simulator_and_diagnose_action(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        action = conn.execute(
            "SELECT action_type,target_mode,required_capability,requires_colocation FROM action_definitions WHERE action_type=?",
            (DIAGNOSE_ACTION,),
        ).fetchone()
        assert action is not None
        assert action["target_mode"] == "object"
        assert action["required_capability"] == DIAGNOSE_ACTION
        assert action["requires_colocation"] == 1

        simulator = conn.execute(
            "SELECT entity_type,definition_id,capabilities_json FROM entities WHERE id=?",
            (SIMULATOR_ID,),
        ).fetchone()
        assert simulator is not None
        assert simulator["entity_type"] == "object"
        assert simulator["definition_id"] == SIMULATOR_DEFINITION_ID
        capabilities = set(json.loads(simulator["capabilities_json"]))
        assert {"inspect", "diagnose", "diagnostic_interface", "technical_documentation"}.issubset(
            capabilities
        )
        assert conn.execute(
            "SELECT 1 FROM relations WHERE source_id=? AND relation_type='contains' AND target_id=?",
            (SIMULATOR_ROOM_ID, SIMULATOR_ID),
        ).fetchone() is not None


def test_action_options_expose_real_diagnostic_gameplay_to_cognition(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_darian_to_simulator(conn)
        options = action_options(conn, "char_darian")
        diagnose = next(
            item
            for item in options
            if item["action"] == DIAGNOSE_ACTION and item["target"] == SIMULATOR_ID
        )
        assert diagnose["target_name"] == "Known-System Diagnostic Simulator"

        enriched = ModelDecisionProvider(conn, character_id="char_darian")._enrich_state(
            snapshot(conn, "char_darian")
        )
        assert any(
            item["action"] == DIAGNOSE_ACTION and item["target"] == SIMULATOR_ID
            for item in enriched["action_options"]
        )
        technology = next(
            item
            for item in enriched["capability_awareness"]["skills"]
            if item["skill_id"] == "technology"
        )
        assert any(
            app["application_id"] == "diagnose_known_system_fault"
            for app in technology["applications"]
        )
        assert (
            enriched["capability_awareness"]["reasoning_profile"]["factors"]
            ["general_reasoning_capacity"]["value"]
            == 140
        )


def test_darian_task_instance_is_supported_and_outcome_is_deterministic(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assessment = assess_technology_diagnostic_action(conn, "char_darian", SIMULATOR_ID)
        assert assessment.status == "supported"
        assert assessment.capability.skill_score == pytest.approx(82.0)
        assert assessment.capability.proficiency_grade == "A"
        assert set(assessment.recognized_resource_capabilities) == {
            "diagnostic_interface",
            "technical_documentation",
        }

        first = technology_diagnostic_outcome(conn, "char_darian", SIMULATOR_ID)
        second = technology_diagnostic_outcome(conn, "char_darian", SIMULATOR_ID)
        assert first == second
        assert first["outcome_class"] == "strong"
        assert first["indices"]["quality_precision"] == pytest.approx(0.888552, abs=1e-6)
        assert first["indices"]["information_gained"] == pytest.approx(0.905805, abs=1e-6)
        assert first["indices"]["partial_failure_recovery"] == pytest.approx(0.894, abs=0.002)
        assert first["learning_evidence"] is False


def test_completed_diagnose_action_writes_application_evidence_but_no_skill_learning(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_darian_to_simulator(conn)
        skill_before = conn.execute(
            "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key='technology'"
        ).fetchone()
        event_count_before = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        action = Action(
            DIAGNOSE_ACTION,
            30,
            SIMULATOR_ID,
            "run a careful diagnostic pass on the represented simulator",
        )
        apply_action(conn, action, "char_darian", action_id="diagnostic-runtime-test-action")

        instance = conn.execute(
            "SELECT status,outcome_json FROM action_instances WHERE id='diagnostic-runtime-test-action'"
        ).fetchone()
        assert instance["status"] == "completed"
        outcome = json.loads(instance["outcome_json"])
        assert outcome["represented_skill_task"]["outcome_class"] == "strong"
        assert outcome["skill_application"]["learning_evidence"] is False

        rows = conn.execute(
            "SELECT event_type,payload_json,caused_by_event_id FROM events WHERE action_id=? ORDER BY id",
            ("diagnostic-runtime-test-action",),
        ).fetchall()
        assert [row["event_type"] for row in rows] == [
            "action_completed",
            "skill_application_evidence",
        ]
        completion = json.loads(rows[0]["payload_json"])
        evidence = json.loads(rows[1]["payload_json"])
        assert completion["skill_application"]["evidence_type"] == "skill_application"
        assert evidence["skill_id"] == "technology"
        assert evidence["application_id"] == "diagnose_known_system_fault"
        assert evidence["learning_evidence"] is False
        assert rows[1]["caused_by_event_id"] is not None

        skill_after = conn.execute(
            "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key='technology'"
        ).fetchone()
        assert tuple(skill_after) == tuple(skill_before)
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == event_count_before + 2


def test_reapplying_completed_action_id_is_idempotent_for_application_evidence(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_darian_to_simulator(conn)
        action = Action(DIAGNOSE_ACTION, 20, SIMULATOR_ID, "repeatable idempotency fixture")
        apply_action(conn, action, "char_darian", action_id="diagnostic-idempotency")
        first_count = conn.execute(
            "SELECT COUNT(*) FROM events WHERE action_id='diagnostic-idempotency'"
        ).fetchone()[0]
        apply_action(conn, action, "char_darian", action_id="diagnostic-idempotency")
        second_count = conn.execute(
            "SELECT COUNT(*) FROM events WHERE action_id='diagnostic-idempotency'"
        ).fetchone()[0]
        assert first_count == second_count == 2


def test_actor_without_technology_fails_closed_and_rolls_back_action_mutations(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        actor = "char_no_technology_fixture"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
            (actor, "character", "No Technology Fixture", "{}", "[]"),
        )
        conn.execute(
            "INSERT INTO character_profiles(entity_id,profile_schema_version,canonical_revision,status) VALUES(?,?,?,?)",
            (actor, 1, "no-tech-runtime-test", "active"),
        )
        for field_key, value in {
            "raps_ia.iq": 180.0,
            "raps_ia.problem_solving": 100.0,
            "raps_ma.focus": 100.0,
            "raps_ma.adaptability": 100.0,
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
                Action(DIAGNOSE_ACTION, 30, SIMULATOR_ID, "IQ cannot substitute for learned Technology"),
                actor,
                action_id="unsupported-diagnostic-action",
            )

        after_state = snapshot(conn, actor)
        assert after_state == before_state
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='unsupported-diagnostic-action'"
        ).fetchone() is None
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == before_events


def test_wrong_diagnose_target_definition_fails_before_commit(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_darian_to_simulator(conn)
        wrong = "obj_wrong_diagnostic_target"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            (
                wrong,
                "object",
                "Wrong Diagnostic Target",
                json.dumps(["diagnose", "inspect", "diagnostic_interface", "technical_documentation"]),
                "represented_task:not_the_authorized_diagnostic_simulator",
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
                Action(DIAGNOSE_ACTION, 20, wrong, "wrong target must fail exact binding"),
                "char_darian",
                action_id="wrong-diagnostic-target-action",
            )
        assert snapshot(conn, "char_darian") == before
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='wrong-diagnostic-target-action'"
        ).fetchone() is None

from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.field_medicine_stabilization import (
    APPLICATION_ID,
    CONSEQUENCE_ID,
    DETERIORATION_FIELD,
    SKILL_ID,
    STABILIZE_ACTION,
    SUPPLIES_CAPABILITY,
    TASK_ID,
    FieldMedicineStabilizationError,
    field_medicine_stabilization_outcome,
    settle_completed_stabilization_consequence,
)
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.represented_skill_tasks import load_represented_skill_tasks
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import maybe_settle_skill_progression
from observer_sandbox.world import get_field, set_field


ROOM = "loc_thorne_estate_medical_bay"
SESSION = "obj_test_field_medicine_stabilization_session"
CASUALTY = "char_test_field_medicine_casualty"
SUPPLIES = "obj_test_field_medicine_supplies"
SESSION_DEFINITION = "represented_task:field_medicine_stabilization_session_v1"


def _prepare(conn, *, state_mode: str = "simulated", include_supplies: bool = True) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
        (
            SESSION,
            "object",
            "Represented Field Stabilization Session",
            json.dumps(["stabilize", "field_medical_context", "evacuation_or_handoff_needed"]),
            SESSION_DEFINITION,
        ),
    )
    conn.execute(
        "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
        (ROOM, "contains", SESSION),
    )
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json,definition_id) VALUES(?,?,?,?,?,?)",
        (
            CASUALTY,
            "character",
            "Represented Field Casualty",
            "{}",
            "[]",
            "test:field_medicine_casualty_v1",
        ),
    )
    set_dynamic_location(conn, CASUALTY, ROOM)
    set_dynamic_location(conn, "char_darian", ROOM)
    set_field(
        conn,
        CASUALTY,
        DETERIORATION_FIELD,
        60.0,
        mode=state_mode,
        authority="field_medical_state_test",
        source="field-medicine-stabilization-consequence-v1-test",
    )
    if include_supplies:
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            (
                SUPPLIES,
                "object",
                "Represented Field Medical Supplies",
                json.dumps([SUPPLIES_CAPABILITY]),
                "test:field_medical_supplies_v1",
            ),
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
            (ROOM, "contains", SUPPLIES),
        )
    conn.commit()


def test_registry_adds_one_bounded_represented_stabilization_task() -> None:
    config = load_represented_skill_tasks()
    assert config["revision"] == "represented-skill-tasks-v1.5"
    task = config["tasks"][TASK_ID]
    assert task["skill_id"] == SKILL_ID
    assert task["application_id"] == APPLICATION_ID
    assert task["task_mode"] == "represented_consequential"
    assert task["target_contract"]["definition_id"] == SESSION_DEFINITION
    assert task["resource_contract"]["required_capabilities_any"] == [SUPPLIES_CAPABILITY]
    interaction = task["interaction_contract"]
    assert interaction["participant_count"] == 1
    assert interaction["required_casualty_state_field"] == DETERIORATION_FIELD
    assert interaction["allowed_consequence_fields"] == [DETERIORATION_FIELD]
    assert interaction["injury_diagnosis_mutation"] is False
    assert interaction["definitive_treatment_mutation"] is False


def test_fresh_runtime_registers_action_vocabulary_without_production_fixture(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        definition = conn.execute(
            "SELECT action_type,required_capability FROM action_definitions WHERE action_type=?",
            (STABILIZE_ACTION,),
        ).fetchone()
        assert tuple(definition) == (STABILIZE_ACTION, STABILIZE_ACTION)
        assert conn.execute(
            "SELECT 1 FROM entities WHERE definition_id=?",
            (SESSION_DEFINITION,),
        ).fetchone() is None
        assert not any(item["action"] == STABILIZE_ACTION for item in action_options(conn, "char_darian"))


def test_field_medicine_skill_authority_resolves_bounded_stabilization_outcome(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        outcome = field_medicine_stabilization_outcome(
            conn,
            "char_darian",
            SESSION,
            (CASUALTY,),
            (SUPPLIES,),
        )
        assert outcome["task"]["task_id"] == TASK_ID
        assert outcome["capability"]["skill_id"] == SKILL_ID
        assert outcome["capability"]["application_id"] == APPLICATION_ID
        assert outcome["capability"]["skill_score"] == pytest.approx(75.0)
        assert outcome["capability"]["proficiency_grade"] == "A"
        assert outcome["outcome_class"] == "solid"
        assert outcome["indices"]["deterioration_risk_reduction"] == pytest.approx(20.0)
        assert outcome["consequence"]["before"] == pytest.approx(60.0)
        assert outcome["consequence"]["planned_after"] == pytest.approx(40.0)
        assert outcome["consequence"]["injury_diagnosis_created"] is False
        assert outcome["consequence"]["definitive_treatment_completed"] is False
        assert outcome["learning_evidence"] is False


def test_completed_stabilization_applies_one_causal_consequence_without_xp(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        before_skill = tuple(
            conn.execute(
                "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key=?",
                (SKILL_ID,),
            ).fetchone()
        )
        action_id = "field-medicine-stabilization-v1-action"
        apply_action(
            conn,
            Action(
                STABILIZE_ACTION,
                10,
                SESSION,
                "bounded represented casualty stabilization for evacuation",
                participants=(CASUALTY,),
                resources=(SUPPLIES,),
            ),
            "char_darian",
            action_id=action_id,
        )

        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(40.0)
        field_row = conn.execute(
            "SELECT mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
            (CASUALTY, DETERIORATION_FIELD),
        ).fetchone()
        assert tuple(field_row) == (
            "simulated",
            "field_medical_state_test",
            "field-medicine-stabilization-consequence-v1-test",
        )

        instance = conn.execute(
            "SELECT status,outcome_json,participants_json,resources_json FROM action_instances WHERE id=?",
            (action_id,),
        ).fetchone()
        assert instance["status"] == "completed"
        assert json.loads(instance["participants_json"]) == [CASUALTY]
        assert json.loads(instance["resources_json"]) == [SUPPLIES]
        action_outcome = json.loads(instance["outcome_json"])
        represented = action_outcome["represented_skill_task"]
        evidence = action_outcome["skill_application"]
        assert represented["task"]["task_id"] == TASK_ID
        assert evidence["application_id"] == APPLICATION_ID
        assert evidence["participant_id"] == CASUALTY
        assert evidence["learning_evidence"] is False

        events = conn.execute(
            "SELECT id,event_type,payload_json,state_changes_json,caused_by_event_id FROM events WHERE action_id=? ORDER BY id",
            (action_id,),
        ).fetchall()
        assert [row["event_type"] for row in events] == [
            "action_completed",
            "skill_application_evidence",
            "represented_consequence_applied",
        ]
        completion = events[0]
        consequence = events[2]
        consequence_payload = json.loads(consequence["payload_json"])
        consequence_changes = json.loads(consequence["state_changes_json"])
        assert consequence["caused_by_event_id"] == completion["id"]
        assert consequence_payload["consequence_id"] == CONSEQUENCE_ID
        assert consequence_payload["represented_task_id"] == TASK_ID
        assert consequence_payload["subject_id"] == CASUALTY
        assert consequence_payload["learning_evidence"] is False
        change = consequence_changes["fields"][DETERIORATION_FIELD]
        assert change["before"] == pytest.approx(60.0)
        assert change["after"] == pytest.approx(40.0)
        assert change["operation"] == "set"

        maybe_settle_skill_progression(
            conn,
            "char_darian",
            as_of_sim_time=snapshot(conn, "char_darian")["sim_time"],
        )
        after_skill = tuple(
            conn.execute(
                "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key=?",
                (SKILL_ID,),
            ).fetchone()
        )
        assert after_skill == before_skill


def test_consequence_retry_is_idempotent_and_does_not_reduce_twice(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        action_id = "field-medicine-stabilization-v1-retry"
        apply_action(
            conn,
            Action(
                STABILIZE_ACTION,
                10,
                SESSION,
                "bounded represented casualty stabilization",
                participants=(CASUALTY,),
                resources=(SUPPLIES,),
            ),
            "char_darian",
            action_id=action_id,
        )
        outcome = json.loads(
            conn.execute(
                "SELECT outcome_json FROM action_instances WHERE id=?",
                (action_id,),
            ).fetchone()[0]
        )["represented_skill_task"]
        result = settle_completed_stabilization_consequence(
            conn,
            action_id=action_id,
            outcome=outcome,
        )
        assert result["already_applied"] is True
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(40.0)
        assert conn.execute(
            "SELECT COUNT(*) FROM events WHERE action_id=? AND event_type='represented_consequence_applied'",
            (action_id,),
        ).fetchone()[0] == 1


def test_missing_medical_supplies_fails_closed_and_rolls_back_action(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn, include_supplies=False)
        before = snapshot(conn, "char_darian")
        with pytest.raises(FieldMedicineStabilizationError, match="medical-supply resource"):
            apply_action(
                conn,
                Action(
                    STABILIZE_ACTION,
                    10,
                    SESSION,
                    "invalid stabilization without supplies",
                    participants=(CASUALTY,),
                ),
                "char_darian",
                action_id="field-medicine-missing-supplies",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(60.0)
        assert snapshot(conn, "char_darian") == before
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='field-medicine-missing-supplies'"
        ).fetchone() is None


def test_non_simulated_casualty_state_cannot_be_mutated(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn, state_mode="static")
        before = snapshot(conn, "char_darian")
        with pytest.raises(FieldMedicineStabilizationError, match="pre-existing simulated"):
            apply_action(
                conn,
                Action(
                    STABILIZE_ACTION,
                    10,
                    SESSION,
                    "invalid stabilization against static state",
                    participants=(CASUALTY,),
                    resources=(SUPPLIES,),
                ),
                "char_darian",
                action_id="field-medicine-static-state",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(60.0)
        assert snapshot(conn, "char_darian") == before
        assert conn.execute(
            "SELECT 1 FROM events WHERE action_id='field-medicine-static-state'"
        ).fetchone() is None

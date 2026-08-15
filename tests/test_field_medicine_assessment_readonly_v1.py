from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.field_medicine_assessment import (
    APPLICATION_ID,
    ASSESS_ACTION,
    SESSION_DEFINITION_ID,
    SKILL_ID,
    TASK_ID,
    FieldMedicineAssessmentError,
    deterioration_pressure_band,
    field_medicine_assessment_outcome,
)
from observer_sandbox.field_medicine_stabilization import DETERIORATION_FIELD
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.represented_skill_tasks import load_represented_skill_tasks
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.skill_progression import maybe_settle_skill_progression
from observer_sandbox.world import get_field, set_field


ROOM = "loc_thorne_estate_medical_bay"
SESSION = "obj_test_field_medicine_assessment_session"
CASUALTY = "char_test_field_medicine_assessment_casualty"


def _prepare(conn, *, risk: float = 50.0, state_mode: str = "simulated") -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
        (
            SESSION,
            "object",
            "Represented Field Casualty Assessment Session",
            json.dumps(["assess", "field_medical_context", "casualty_assessment_session"]),
            SESSION_DEFINITION_ID,
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
            "test:field_medicine_assessment_casualty_v1",
        ),
    )
    set_dynamic_location(conn, "char_darian", ROOM)
    set_dynamic_location(conn, CASUALTY, ROOM)
    set_field(
        conn,
        CASUALTY,
        DETERIORATION_FIELD,
        risk,
        mode=state_mode,
        authority="casualty_state_runtime",
        source="casualty-state-origin-lifecycle-v1",
    )
    conn.commit()


def test_registry_adds_read_only_field_medicine_assessment_task() -> None:
    config = load_represented_skill_tasks()
    assert config["revision"] == "represented-skill-tasks-v1.6"
    task = config["tasks"][TASK_ID]
    assert task["skill_id"] == SKILL_ID
    assert task["application_id"] == APPLICATION_ID
    assert task["task_mode"] == "represented_consequential"
    assert task["risk_class"] == "high"
    assert task["target_contract"]["definition_id"] == SESSION_DEFINITION_ID
    assert task["resource_contract"] == {
        "required_resource_mode": "none",
        "required_capabilities_any": [],
        "supporting_capabilities": ["basic_medical_assessment_tools"],
    }
    interaction = task["interaction_contract"]
    assert interaction["participant_count"] == 1
    assert interaction["required_casualty_state_field"] == DETERIORATION_FIELD
    assert interaction["observation_mode"] == "read_only"
    assert interaction["casualty_state_creation"] is False
    assert interaction["casualty_state_mutation"] is False
    assert interaction["injury_diagnosis_mutation"] is False
    assert interaction["definitive_treatment_mutation"] is False
    assert task["evidence_policy"]["learning_evidence"] is False


def test_pressure_band_is_abstract_and_deterministic() -> None:
    assert deterioration_pressure_band(0.0) == "none"
    assert deterioration_pressure_band(1.0) == "low"
    assert deterioration_pressure_band(33.0) == "low"
    assert deterioration_pressure_band(33.1) == "moderate"
    assert deterioration_pressure_band(66.0) == "moderate"
    assert deterioration_pressure_band(66.1) == "high"
    assert deterioration_pressure_band(100.0) == "high"


def test_field_medicine_assessment_reads_existing_state_without_mutation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn, risk=50.0)
        before = tuple(
            conn.execute(
                "SELECT value_json,mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
                (CASUALTY, DETERIORATION_FIELD),
            ).fetchone()
        )
        outcome = field_medicine_assessment_outcome(
            conn,
            "char_darian",
            SESSION,
            (CASUALTY,),
        )
        after = tuple(
            conn.execute(
                "SELECT value_json,mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
                (CASUALTY, DETERIORATION_FIELD),
            ).fetchone()
        )
        assert after == before
        assert outcome["task"]["task_id"] == TASK_ID
        assert outcome["capability"]["skill_id"] == SKILL_ID
        assert outcome["capability"]["application_id"] == APPLICATION_ID
        assert outcome["capability"]["skill_score"] == pytest.approx(75.0)
        assert outcome["capability"]["proficiency_grade"] == "A"
        assert outcome["outcome_class"] == "solid"
        assert outcome["observation"]["deterioration_risk"] == pytest.approx(50.0)
        assert outcome["observation"]["deterioration_pressure_band"] == "moderate"
        assert outcome["observation"]["diagnosis_created"] is False
        assert outcome["observation"]["treatment_performed"] is False
        assert outcome["world_mutation_policy"] == "read_only"
        assert outcome["learning_evidence"] is False


def test_completed_assessment_persists_application_evidence_but_no_state_change_or_xp(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn, risk=50.0)
        before_skill = tuple(
            conn.execute(
                "SELECT score,experience FROM character_skills WHERE entity_id='char_darian' AND skill_key=?",
                (SKILL_ID,),
            ).fetchone()
        )
        before_field = tuple(
            conn.execute(
                "SELECT value_json,mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
                (CASUALTY, DETERIORATION_FIELD),
            ).fetchone()
        )
        action_id = "field-medicine-assessment-readonly-v1-action"
        apply_action(
            conn,
            Action(
                ASSESS_ACTION,
                10,
                SESSION,
                "bounded represented casualty assessment",
                participants=(CASUALTY,),
            ),
            "char_darian",
            action_id=action_id,
        )

        instance = conn.execute(
            "SELECT status,outcome_json FROM action_instances WHERE id=?",
            (action_id,),
        ).fetchone()
        assert instance["status"] == "completed"
        action_outcome = json.loads(instance["outcome_json"])
        represented = action_outcome["represented_skill_task"]
        evidence = action_outcome["skill_application"]
        assert represented["task"]["task_id"] == TASK_ID
        assert represented["world_mutation_policy"] == "read_only"
        assert evidence["application_id"] == APPLICATION_ID
        assert evidence["participant_id"] == CASUALTY
        assert evidence["deterioration_pressure_band"] == "moderate"
        assert evidence["learning_evidence"] is False

        after_field = tuple(
            conn.execute(
                "SELECT value_json,mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
                (CASUALTY, DETERIORATION_FIELD),
            ).fetchone()
        )
        assert after_field == before_field
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(50.0)

        events = conn.execute(
            "SELECT event_type,state_changes_json FROM events WHERE action_id=? ORDER BY id",
            (action_id,),
        ).fetchall()
        assert [row["event_type"] for row in events] == [
            "action_completed",
            "skill_application_evidence",
        ]
        assert all(json.loads(row["state_changes_json"] or "{}") == {} for row in events)

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


def test_shared_assess_verb_still_dispatches_tactical_target_to_tactical_planning(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, "char_darian", "loc_thorne_estate_intelligence_hub")
        conn.commit()
        action_id = "shared-assess-tactical-regression"
        apply_action(
            conn,
            Action(
                "assess",
                10,
                "obj_thorne_estate_intel_tactical_situation_assessment_simulator",
                "bounded tactical assessment",
            ),
            "char_darian",
            action_id=action_id,
        )
        outcome = json.loads(
            conn.execute(
                "SELECT outcome_json FROM action_instances WHERE id=?",
                (action_id,),
            ).fetchone()[0]
        )
        assert outcome["skill_application"]["skill_id"] == "tactical_planning"
        assert outcome["skill_application"]["application_id"] == "assess_tactical_situation"


def test_missing_or_non_simulated_casualty_state_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn, state_mode="static")
        before = snapshot(conn, "char_darian")
        with pytest.raises(FieldMedicineAssessmentError, match="pre-existing simulated"):
            apply_action(
                conn,
                Action(
                    ASSESS_ACTION,
                    10,
                    SESSION,
                    "invalid assessment against static state",
                    participants=(CASUALTY,),
                ),
                "char_darian",
                action_id="field-medicine-assessment-static-state",
            )
        assert snapshot(conn, "char_darian") == before
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='field-medicine-assessment-static-state'"
        ).fetchone() is None


def test_assessment_requires_one_distinct_colocated_casualty(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        set_dynamic_location(conn, CASUALTY, "loc_thorne_estate_living_room")
        conn.commit()
        with pytest.raises(FieldMedicineAssessmentError, match="colocated"):
            field_medicine_assessment_outcome(
                conn,
                "char_darian",
                SESSION,
                (CASUALTY,),
            )

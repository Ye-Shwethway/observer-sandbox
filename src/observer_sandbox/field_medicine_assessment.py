from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable

from .field_medicine_stabilization import DETERIORATION_FIELD
from .location_runtime import current_location
from .represented_skill_task_instance import (
    RepresentedSkillTaskInstanceAssessment,
    assess_represented_skill_task_instance,
)
from .represented_skill_tasks import represented_skill_task


SOURCE = "field-medicine-assessment-readonly-v1"
ASSESS_ACTION = "assess"
TASK_ID = "field_medicine_assess_field_casualty_v1"
SKILL_ID = "field_medicine"
APPLICATION_ID = "assess_field_casualty"
SESSION_DEFINITION_ID = "represented_task:field_medicine_casualty_assessment_session_v1"


class FieldMedicineAssessmentError(ValueError):
    pass


def _target_definition(conn: sqlite3.Connection, target_id: str) -> str | None:
    row = conn.execute(
        "SELECT definition_id FROM entities WHERE id=? AND entity_type='object'",
        (target_id,),
    ).fetchone()
    return str(row["definition_id"]) if row is not None and row["definition_id"] else None


def is_field_medicine_assessment_target(conn: sqlite3.Connection, target_id: str) -> bool:
    return _target_definition(conn, target_id) == SESSION_DEFINITION_ID


def action_participants(conn: sqlite3.Connection, action_id: str) -> tuple[str, ...]:
    row = conn.execute(
        "SELECT participants_json FROM action_instances WHERE id=?",
        (action_id,),
    ).fetchone()
    if row is None:
        raise FieldMedicineAssessmentError(f"Action instance {action_id!r} does not exist")
    try:
        values = json.loads(row["participants_json"] or "[]")
    except (TypeError, json.JSONDecodeError) as exc:
        raise FieldMedicineAssessmentError(
            "Field Medicine assessment participants JSON is invalid"
        ) from exc
    if not isinstance(values, list) or not all(isinstance(value, str) and value for value in values):
        raise FieldMedicineAssessmentError(
            "Field Medicine assessment participants must contain entity ids"
        )
    return tuple(values)


def _casualty_state(
    conn: sqlite3.Connection,
    actor_id: str,
    casualty_id: str,
) -> dict[str, Any]:
    if casualty_id == actor_id:
        raise FieldMedicineAssessmentError(
            "Field Medicine assessment casualty must differ from actor"
        )
    entity = conn.execute(
        "SELECT entity_type,name FROM entities WHERE id=?",
        (casualty_id,),
    ).fetchone()
    if entity is None or entity["entity_type"] != "character":
        raise FieldMedicineAssessmentError(
            "Field Medicine assessment casualty must be a represented character"
        )

    actor_location = current_location(conn, actor_id)
    casualty_location = current_location(conn, casualty_id)
    if actor_location is None or casualty_location != actor_location:
        raise FieldMedicineAssessmentError(
            "Field Medicine assessment casualty must be colocated with actor"
        )

    field = conn.execute(
        """SELECT value_json,mode FROM fields
        WHERE entity_id=? AND field_key=?""",
        (casualty_id, DETERIORATION_FIELD),
    ).fetchone()
    if field is None or field["mode"] != "simulated":
        raise FieldMedicineAssessmentError(
            "Assessment requires pre-existing simulated casualty deterioration state"
        )
    try:
        risk = json.loads(field["value_json"])
    except (TypeError, json.JSONDecodeError) as exc:
        raise FieldMedicineAssessmentError(
            "Casualty deterioration state contains invalid JSON"
        ) from exc
    if isinstance(risk, bool) or not isinstance(risk, (int, float)):
        raise FieldMedicineAssessmentError("Casualty deterioration risk must be numeric")
    risk = float(risk)
    if not 0.0 <= risk <= 100.0:
        raise FieldMedicineAssessmentError(
            "Casualty deterioration risk must be within 0..100"
        )
    return {
        "casualty_id": casualty_id,
        "casualty_name": str(entity["name"] or casualty_id),
        "location_id": actor_location,
        "deterioration_risk": risk,
    }


def deterioration_pressure_band(risk: float) -> str:
    """Convert abstract simulation pressure into a non-diagnostic readout band."""
    if risk <= 0.0:
        return "none"
    if risk <= 33.0:
        return "low"
    if risk <= 66.0:
        return "moderate"
    return "high"


def assess_field_medicine_assessment_action(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
    participant_ids: Iterable[str],
) -> tuple[RepresentedSkillTaskInstanceAssessment, dict[str, Any]]:
    task = represented_skill_task(TASK_ID)
    interaction = task.get("interaction_contract")
    if not isinstance(interaction, dict):
        raise FieldMedicineAssessmentError(
            "Field Medicine assessment task lacks interaction contract"
        )
    participants = tuple(participant_ids)
    expected_count = int(interaction.get("participant_count") or 0)
    if len(participants) != expected_count:
        raise FieldMedicineAssessmentError(
            f"Field Medicine assessment requires exactly {expected_count} casualty participant"
        )
    casualty = _casualty_state(conn, actor_id, participants[0])
    assessment = assess_represented_skill_task_instance(
        conn,
        actor_id,
        TASK_ID,
        target_id,
        resource_capabilities=(),
    )
    if assessment.status == "unsupported":
        raise FieldMedicineAssessmentError(
            "Actor does not meet Field Medicine assessment application contract: "
            + ", ".join(assessment.reasons)
        )
    return assessment, casualty


def field_medicine_assessment_outcome(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
    participant_ids: Iterable[str],
) -> dict[str, Any]:
    """Read represented casualty pressure without creating diagnosis or mutation."""
    task, casualty = assess_field_medicine_assessment_action(
        conn,
        actor_id,
        target_id,
        participant_ids,
    )
    capability = task.capability
    effectiveness = max(0.0, min(1.0, float(capability.skill_score) / 100.0))
    if effectiveness >= 0.80:
        outcome_class = "strong"
    elif effectiveness >= 0.65:
        outcome_class = "solid"
    elif effectiveness >= 0.45:
        outcome_class = "limited"
    else:
        outcome_class = "poor"

    risk = float(casualty["deterioration_risk"])
    return {
        "source": SOURCE,
        "task": {
            "task_id": task.task_id,
            "task_revision": task.task_revision,
            "status": task.status,
            "target_entity_id": task.target_entity_id,
            "target_definition_id": task.target_definition_id,
            "recognized_resource_capabilities": list(task.recognized_resource_capabilities),
        },
        "capability": {
            "skill_id": capability.skill_id,
            "application_id": capability.application_id,
            "skill_score": capability.skill_score,
            "proficiency_grade": capability.proficiency_grade,
            "proficiency_label": capability.proficiency_label,
            "challenge_class": capability.challenge_class,
            "status": capability.status,
            "reasons": list(capability.reasons),
        },
        "observation": {
            "casualty_id": casualty["casualty_id"],
            "casualty_name": casualty["casualty_name"],
            "state_field": DETERIORATION_FIELD,
            "deterioration_risk": risk,
            "deterioration_pressure_band": deterioration_pressure_band(risk),
            "diagnosis_created": False,
            "treatment_performed": False,
        },
        "indices": {
            "assessment_effectiveness": round(effectiveness, 6),
            "information_gained": round(effectiveness, 6),
            "quality_precision": round(effectiveness, 6),
        },
        "outcome_class": outcome_class,
        "world_mutation_policy": "read_only",
        "learning_evidence": False,
    }


def field_medicine_assessment_application_evidence(
    outcome: dict[str, Any],
    *,
    action_id: str,
    actor_id: str,
    duration_minutes: int,
) -> dict[str, Any]:
    capability = outcome["capability"]
    observation = outcome["observation"]
    return {
        "source": SOURCE,
        "evidence_type": "skill_application",
        "action_id": action_id,
        "actor_id": actor_id,
        "participant_id": observation["casualty_id"],
        "skill_id": capability["skill_id"],
        "application_id": capability["application_id"],
        "task_id": outcome["task"]["task_id"],
        "task_revision": outcome["task"]["task_revision"],
        "target_entity_id": outcome["task"]["target_entity_id"],
        "target_definition_id": outcome["task"]["target_definition_id"],
        "challenge_class": capability["challenge_class"],
        "capability_status": capability["status"],
        "outcome_class": outcome["outcome_class"],
        "deterioration_pressure_band": observation["deterioration_pressure_band"],
        "duration_minutes": int(duration_minutes),
        "world_mutation_policy": "read_only",
        "learning_evidence": False,
    }

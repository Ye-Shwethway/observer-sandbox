from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable

from .location_runtime import current_location
from .represented_skill_task_instance import (
    RepresentedSkillTaskInstanceAssessment,
    assess_represented_skill_task_instance,
)
from .represented_skill_tasks import represented_skill_task


SOURCE = "field-medicine-stabilization-consequence-v1"
STABILIZE_ACTION = "stabilize"
TASK_ID = "field_medicine_stabilize_for_evacuation_v1"
SKILL_ID = "field_medicine"
APPLICATION_ID = "stabilize_for_evacuation"
DETERIORATION_FIELD = "medical.deterioration_risk"
SUPPLIES_CAPABILITY = "field_medical_supplies"
CONSEQUENCE_ID = "field_medicine_reduce_deterioration_risk_v1"


class FieldMedicineStabilizationError(ValueError):
    pass


def seed_field_medicine_stabilization_runtime(conn: sqlite3.Connection) -> None:
    """Register stabilization action vocabulary without creating a live casualty.

    A represented stabilization session, casualty participant, casualty state, and
    medical-supply resource must already exist before this action can complete.
    Production initialization intentionally seeds none of those fixtures.
    """

    conn.execute(
        """
        INSERT INTO action_definitions(
            action_type,label,min_duration_minutes,max_duration_minutes,target_mode,
            required_capability,requires_colocation,base_effects_json,conditions_json,
            modifiers_json,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(action_type) DO UPDATE SET
            label=excluded.label,
            min_duration_minutes=excluded.min_duration_minutes,
            max_duration_minutes=excluded.max_duration_minutes,
            target_mode=excluded.target_mode,
            required_capability=excluded.required_capability,
            requires_colocation=excluded.requires_colocation,
            metadata_json=excluded.metadata_json,
            updated_at=CURRENT_TIMESTAMP
        """,
        (
            STABILIZE_ACTION,
            "Stabilize",
            5,
            60,
            "object",
            STABILIZE_ACTION,
            1,
            json.dumps({}),
            json.dumps({}),
            json.dumps({}),
            json.dumps({"source": SOURCE, "task_id": TASK_ID}, sort_keys=True),
        ),
    )
    conn.commit()


def _capabilities(conn: sqlite3.Connection, entity_id: str) -> tuple[str, ...]:
    row = conn.execute(
        "SELECT capabilities_json FROM entities WHERE id=?",
        (entity_id,),
    ).fetchone()
    if row is None:
        raise FieldMedicineStabilizationError(f"Entity {entity_id!r} does not exist")
    try:
        values = json.loads(row["capabilities_json"] or "[]")
    except (TypeError, json.JSONDecodeError) as exc:
        raise FieldMedicineStabilizationError(
            f"Entity {entity_id!r} has invalid capabilities JSON"
        ) from exc
    if not isinstance(values, list) or not all(
        isinstance(value, str) and value for value in values
    ):
        raise FieldMedicineStabilizationError(
            f"Entity {entity_id!r} has malformed capabilities"
        )
    return tuple(sorted(set(values)))


def _action_lists(
    conn: sqlite3.Connection,
    action_id: str,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    row = conn.execute(
        "SELECT participants_json,resources_json FROM action_instances WHERE id=?",
        (action_id,),
    ).fetchone()
    if row is None:
        raise FieldMedicineStabilizationError(f"Action instance {action_id!r} does not exist")
    try:
        participants = json.loads(row["participants_json"] or "[]")
        resources = json.loads(row["resources_json"] or "[]")
    except (TypeError, json.JSONDecodeError) as exc:
        raise FieldMedicineStabilizationError(
            "Stabilization action participants/resources JSON is invalid"
        ) from exc
    for label, values in (("participants", participants), ("resources", resources)):
        if not isinstance(values, list) or not all(
            isinstance(value, str) and value for value in values
        ):
            raise FieldMedicineStabilizationError(
                f"Stabilization action {label} must contain entity ids"
            )
    return tuple(participants), tuple(resources)


def _local_resource_capabilities(
    conn: sqlite3.Connection,
    actor_id: str,
    resource_ids: Iterable[str],
) -> tuple[str, ...]:
    actor_location = current_location(conn, actor_id)
    if actor_location is None:
        raise FieldMedicineStabilizationError("Stabilization actor has no current location")

    recognized: set[str] = set()
    resources = tuple(resource_ids)
    if not resources:
        raise FieldMedicineStabilizationError(
            "Stabilization requires an explicitly represented medical-supply resource"
        )
    for resource_id in resources:
        row = conn.execute(
            "SELECT entity_type FROM entities WHERE id=?",
            (resource_id,),
        ).fetchone()
        if row is None or row["entity_type"] != "object":
            raise FieldMedicineStabilizationError(
                f"Stabilization resource {resource_id!r} must be a represented object"
            )
        local = conn.execute(
            """SELECT 1 FROM relations
            WHERE source_id=? AND relation_type='contains' AND target_id=?""",
            (actor_location, resource_id),
        ).fetchone()
        carried = conn.execute(
            """SELECT 1 FROM relations
            WHERE source_id=? AND relation_type='carried_by' AND target_id=?""",
            (resource_id, actor_id),
        ).fetchone()
        if local is None and carried is None:
            raise FieldMedicineStabilizationError(
                f"Stabilization resource {resource_id!r} is not locally available to actor"
            )
        recognized.update(_capabilities(conn, resource_id))

    if SUPPLIES_CAPABILITY not in recognized:
        raise FieldMedicineStabilizationError(
            "Stabilization requires represented field medical supplies"
        )
    return tuple(sorted(recognized))


def _casualty_state(
    conn: sqlite3.Connection,
    actor_id: str,
    casualty_id: str,
) -> dict[str, Any]:
    if casualty_id == actor_id:
        raise FieldMedicineStabilizationError(
            "Field Medicine stabilization casualty must differ from actor"
        )
    row = conn.execute(
        "SELECT entity_type,name FROM entities WHERE id=?",
        (casualty_id,),
    ).fetchone()
    if row is None or row["entity_type"] != "character":
        raise FieldMedicineStabilizationError(
            "Field Medicine stabilization casualty must be a represented character"
        )

    actor_location = current_location(conn, actor_id)
    casualty_location = current_location(conn, casualty_id)
    if actor_location is None or casualty_location != actor_location:
        raise FieldMedicineStabilizationError(
            "Field Medicine stabilization casualty must be colocated with actor"
        )

    field = conn.execute(
        """SELECT value_json,mode FROM fields
        WHERE entity_id=? AND field_key=?""",
        (casualty_id, DETERIORATION_FIELD),
    ).fetchone()
    if field is None or field["mode"] != "simulated":
        raise FieldMedicineStabilizationError(
            "Casualty requires pre-existing simulated medical deterioration state"
        )
    try:
        risk = json.loads(field["value_json"])
    except (TypeError, json.JSONDecodeError) as exc:
        raise FieldMedicineStabilizationError(
            "Casualty deterioration state contains invalid JSON"
        ) from exc
    if isinstance(risk, bool) or not isinstance(risk, (int, float)):
        raise FieldMedicineStabilizationError(
            "Casualty deterioration risk must be numeric"
        )
    risk = float(risk)
    if not 0.0 <= risk <= 100.0:
        raise FieldMedicineStabilizationError(
            "Casualty deterioration risk must be within 0..100"
        )
    return {
        "casualty_id": casualty_id,
        "casualty_name": str(row["name"] or casualty_id),
        "actor_location": actor_location,
        "casualty_location": casualty_location,
        "deterioration_risk_before": risk,
    }


def assess_field_medicine_stabilization_action(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
    participant_ids: Iterable[str],
    resource_ids: Iterable[str],
) -> tuple[RepresentedSkillTaskInstanceAssessment, dict[str, Any], tuple[str, ...]]:
    task = represented_skill_task(TASK_ID)
    interaction = task.get("interaction_contract")
    if not isinstance(interaction, dict):
        raise FieldMedicineStabilizationError(
            "Field Medicine stabilization task lacks interaction contract"
        )

    participants = tuple(participant_ids)
    expected_count = int(interaction.get("participant_count") or 0)
    if len(participants) != expected_count:
        raise FieldMedicineStabilizationError(
            f"Field Medicine stabilization requires exactly {expected_count} casualty participant"
        )
    casualty = _casualty_state(conn, actor_id, participants[0])
    resource_capabilities = _local_resource_capabilities(conn, actor_id, resource_ids)
    assessment = assess_represented_skill_task_instance(
        conn,
        actor_id,
        TASK_ID,
        target_id,
        resource_capabilities=resource_capabilities,
    )
    if assessment.status == "unsupported":
        raise FieldMedicineStabilizationError(
            "Actor does not meet Field Medicine stabilization application contract: "
            + ", ".join(assessment.reasons)
        )
    return assessment, casualty, resource_capabilities


def field_medicine_stabilization_outcome(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
    participant_ids: Iterable[str],
    resource_ids: Iterable[str],
) -> dict[str, Any]:
    """Resolve bounded gameplay stabilization without diagnosis or injury modeling."""

    task, casualty, resource_capabilities = assess_field_medicine_stabilization_action(
        conn,
        actor_id,
        target_id,
        participant_ids,
        resource_ids,
    )
    capability = task.capability
    effectiveness = max(0.0, min(1.0, float(capability.skill_score) / 100.0))
    if effectiveness >= 0.80:
        outcome_class = "strong"
        reduction = 25.0
    elif effectiveness >= 0.65:
        outcome_class = "solid"
        reduction = 20.0
    elif effectiveness >= 0.45:
        outcome_class = "limited"
        reduction = 10.0
    else:
        outcome_class = "poor"
        reduction = 0.0

    before = float(casualty["deterioration_risk_before"])
    after = max(0.0, round(before - reduction, 3))
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
        "authorization": {
            "casualty_id": casualty["casualty_id"],
            "casualty_name": casualty["casualty_name"],
            "subject_role": "participant",
            "resource_capabilities": list(resource_capabilities),
            "consequence_id": CONSEQUENCE_ID,
            "allowed_state_field": DETERIORATION_FIELD,
        },
        "indices": {
            "stabilization_effectiveness": round(effectiveness, 6),
            "deterioration_risk_reduction": reduction,
        },
        "outcome_class": outcome_class,
        "consequence": {
            "mode": "reduce_deterioration_risk_only",
            "field_key": DETERIORATION_FIELD,
            "before": before,
            "planned_after": after,
            "reduction": reduction,
            "injury_diagnosis_created": False,
            "definitive_treatment_completed": False,
        },
        "learning_evidence": False,
        "world_mutation_policy": "authorized_casualty_deterioration_risk_only",
    }


def field_medicine_stabilization_application_evidence(
    outcome: dict[str, Any],
    *,
    action_id: str,
    actor_id: str,
    duration_minutes: int,
) -> dict[str, Any]:
    capability = outcome["capability"]
    authorization = outcome["authorization"]
    return {
        "source": SOURCE,
        "evidence_type": "skill_application",
        "action_id": action_id,
        "actor_id": actor_id,
        "participant_id": authorization["casualty_id"],
        "skill_id": capability["skill_id"],
        "application_id": capability["application_id"],
        "task_id": outcome["task"]["task_id"],
        "task_revision": outcome["task"]["task_revision"],
        "target_entity_id": outcome["task"]["target_entity_id"],
        "target_definition_id": outcome["task"]["target_definition_id"],
        "challenge_class": capability["challenge_class"],
        "capability_status": capability["status"],
        "outcome_class": outcome["outcome_class"],
        "outcome_indices": dict(outcome["indices"]),
        "consequence_mode": outcome["consequence"]["mode"],
        "duration_minutes": int(duration_minutes),
        "learning_evidence": False,
    }


def enrich_completed_stabilization_action(
    conn: sqlite3.Connection,
    *,
    action_id: str,
    actor_id: str,
    target_id: str,
    duration_minutes: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    participants, resources = _action_lists(conn, action_id)
    outcome = field_medicine_stabilization_outcome(
        conn,
        actor_id,
        target_id,
        participants,
        resources,
    )
    evidence = field_medicine_stabilization_application_evidence(
        outcome,
        action_id=action_id,
        actor_id=actor_id,
        duration_minutes=duration_minutes,
    )
    return outcome, evidence


def settle_completed_stabilization_consequence(
    conn: sqlite3.Connection,
    *,
    action_id: str,
    outcome: dict[str, Any],
) -> dict[str, Any]:
    """Use the generic consequence foundation after action-completion evidence exists."""

    from .represented_consequence_state import (
        ConsequenceAuthorization,
        StateMutation,
        apply_represented_consequence,
    )

    authorization = outcome.get("authorization")
    consequence = outcome.get("consequence")
    task = outcome.get("task")
    if not isinstance(authorization, dict) or not isinstance(consequence, dict) or not isinstance(task, dict):
        raise FieldMedicineStabilizationError("Stabilization outcome lacks consequence authorization")
    casualty_id = authorization.get("casualty_id")
    task_id = task.get("task_id")
    planned_after = consequence.get("planned_after")
    if not isinstance(casualty_id, str) or not isinstance(task_id, str):
        raise FieldMedicineStabilizationError("Stabilization outcome lacks casualty/task identity")
    if isinstance(planned_after, bool) or not isinstance(planned_after, (int, float)):
        raise FieldMedicineStabilizationError("Stabilization outcome lacks numeric planned consequence")

    return apply_represented_consequence(
        conn,
        action_id=action_id,
        authorization=ConsequenceAuthorization(
            consequence_id=CONSEQUENCE_ID,
            represented_task_id=task_id,
            subject_id=casualty_id,
            subject_role="participant",
            mutations=(
                StateMutation(
                    field_key=DETERIORATION_FIELD,
                    operation="set",
                    value=float(planned_after),
                ),
            ),
        ),
    )

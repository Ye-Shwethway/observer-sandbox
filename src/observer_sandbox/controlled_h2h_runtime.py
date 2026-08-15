from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from typing import Any, Iterable

from .cognitive_performance import assess_actor_cognitive_performance
from .location_runtime import current_location
from .represented_skill_task_instance import (
    RepresentedSkillTaskInstanceAssessment,
    assess_represented_skill_task_instance,
)
from .represented_skill_tasks import load_represented_skill_tasks, represented_skill_task


SOURCE = "controlled-h2h-interaction-generalization-v1"
SPAR_ACTION = "spar"
TASK_ID = "h2h_controlled_striking_spar_v1"
GRAPPLE_TASK_ID = "h2h_controlled_grapple_spar_v1"
SKILL_ID = "hand_to_hand_combat"
APPLICATION_ID = "engage_unarmed_striking"
GRAPPLE_APPLICATION_ID = "control_unarmed_grapple"
CONSENT_CAPABILITY = "controlled_sparring_consent"
CONTROLLED_H2H_TASK_IDS = (TASK_ID, GRAPPLE_TASK_ID)


class ControlledH2HRuntimeError(ValueError):
    pass


def seed_controlled_h2h_runtime(conn: sqlite3.Connection) -> None:
    """Register controlled H2H action vocabulary without fabricating live fixtures.

    One generic ``spar`` action is intentionally reused across exact represented
    striking and grappling session targets. The target definition selects the
    application contract; a consenting colocated character participant must
    already exist before cognition can see or execute the action.
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
            SPAR_ACTION,
            "Spar",
            5,
            60,
            "object",
            SPAR_ACTION,
            1,
            json.dumps({}),
            json.dumps({}),
            json.dumps({}),
            json.dumps(
                {
                    "source": SOURCE,
                    "task_ids": list(CONTROLLED_H2H_TASK_IDS),
                },
                sort_keys=True,
            ),
        ),
    )
    conn.commit()


def _capabilities(conn: sqlite3.Connection, entity_id: str) -> tuple[str, ...]:
    row = conn.execute(
        "SELECT capabilities_json FROM entities WHERE id=?",
        (entity_id,),
    ).fetchone()
    if row is None:
        raise ControlledH2HRuntimeError(f"Entity {entity_id!r} does not exist")
    try:
        values = json.loads(row["capabilities_json"] or "[]")
    except (TypeError, json.JSONDecodeError) as exc:
        raise ControlledH2HRuntimeError(
            f"Entity {entity_id!r} has invalid capabilities JSON"
        ) from exc
    if not isinstance(values, list) or not all(
        isinstance(value, str) and value for value in values
    ):
        raise ControlledH2HRuntimeError(
            f"Entity {entity_id!r} has malformed capabilities"
        )
    return tuple(sorted(set(values)))


def action_participants(
    conn: sqlite3.Connection,
    action_id: str,
) -> tuple[str, ...]:
    row = conn.execute(
        "SELECT participants_json FROM action_instances WHERE id=?",
        (action_id,),
    ).fetchone()
    if row is None:
        raise ControlledH2HRuntimeError(f"Action instance {action_id!r} does not exist")
    try:
        values = json.loads(row["participants_json"] or "[]")
    except (TypeError, json.JSONDecodeError) as exc:
        raise ControlledH2HRuntimeError("Action participants JSON is invalid") from exc
    if not isinstance(values, list) or not all(
        isinstance(value, str) and value for value in values
    ):
        raise ControlledH2HRuntimeError("Action participants must be character ids")
    return tuple(values)


def _controlled_h2h_task_for_target(
    conn: sqlite3.Connection,
    target_id: str,
) -> dict[str, Any]:
    row = conn.execute(
        "SELECT entity_type,definition_id FROM entities WHERE id=?",
        (target_id,),
    ).fetchone()
    if row is None:
        raise ControlledH2HRuntimeError(f"Controlled H2H target {target_id!r} does not exist")

    definition_id = str(row["definition_id"] or "")
    source = load_represented_skill_tasks()
    matches: list[dict[str, Any]] = []
    for task_id in CONTROLLED_H2H_TASK_IDS:
        task = represented_skill_task(task_id, config=source)
        target = task.get("target_contract") or {}
        if (
            target.get("entity_type") == row["entity_type"]
            and target.get("definition_id") == definition_id
        ):
            matches.append(task)
    if len(matches) != 1:
        raise ControlledH2HRuntimeError(
            "Controlled H2H target must match exactly one authorized represented session definition"
        )
    return matches[0]


def _interaction_contract(task: dict[str, Any]) -> dict[str, Any]:
    contract = task.get("interaction_contract")
    if not isinstance(contract, dict):
        raise ControlledH2HRuntimeError("Controlled H2H task lacks interaction contract")
    return contract


def validate_sparring_participant(
    conn: sqlite3.Connection,
    actor_id: str,
    participant_id: str,
    *,
    task: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resolved_task = task or represented_skill_task(TASK_ID)
    contract = _interaction_contract(resolved_task)
    if bool(contract.get("requires_distinct_actor")) and participant_id == actor_id:
        raise ControlledH2HRuntimeError("Controlled sparring participant must differ from actor")

    row = conn.execute(
        "SELECT entity_type,name FROM entities WHERE id=?",
        (participant_id,),
    ).fetchone()
    expected_type = str(contract.get("participant_entity_type") or "")
    if row is None or row["entity_type"] != expected_type:
        raise ControlledH2HRuntimeError(
            f"Controlled sparring participant must be a represented {expected_type}"
        )

    required = tuple(contract.get("required_participant_capabilities_all") or ())
    capabilities = _capabilities(conn, participant_id)
    missing = tuple(value for value in required if value not in capabilities)
    if missing:
        raise ControlledH2HRuntimeError(
            "Controlled sparring participant lacks explicit authorization: "
            + ", ".join(missing)
        )

    actor_location = current_location(conn, actor_id)
    participant_location = current_location(conn, participant_id)
    if bool(contract.get("requires_colocation")) and (
        actor_location is None or participant_location != actor_location
    ):
        raise ControlledH2HRuntimeError(
            "Controlled sparring participant must be colocated with actor"
        )

    return {
        "participant_id": participant_id,
        "participant_name": str(row["name"] or participant_id),
        "authorization_mode": str(contract.get("authorization_mode") or ""),
        "authorization_capabilities": list(required),
        "actor_location": actor_location,
        "participant_location": participant_location,
    }


def assess_controlled_h2h_action(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
    participant_ids: Iterable[str],
) -> tuple[RepresentedSkillTaskInstanceAssessment, dict[str, Any], dict[str, Any]]:
    task = _controlled_h2h_task_for_target(conn, target_id)
    participants = tuple(participant_ids)
    contract = _interaction_contract(task)
    expected_count = int(contract.get("participant_count") or 0)
    if len(participants) != expected_count:
        raise ControlledH2HRuntimeError(
            f"Controlled sparring requires exactly {expected_count} participant"
        )

    authorization = validate_sparring_participant(
        conn,
        actor_id,
        participants[0],
        task=task,
    )
    assessment = assess_represented_skill_task_instance(
        conn,
        actor_id,
        str(task["task_id"]),
        target_id,
        resource_capabilities=_capabilities(conn, target_id),
    )
    if assessment.status == "unsupported":
        raise ControlledH2HRuntimeError(
            "Actor does not meet controlled H2H application contract: "
            + ", ".join(assessment.reasons)
        )
    return assessment, authorization, task


def controlled_h2h_outcome(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
    participant_ids: Iterable[str],
) -> dict[str, Any]:
    """Resolve exact represented controlled-H2H performance without injury mutation."""

    task_assessment, authorization, task = assess_controlled_h2h_action(
        conn,
        actor_id,
        target_id,
        participant_ids,
    )
    capability = task_assessment.capability
    application_id = str(task["application_id"])
    performance = assess_actor_cognitive_performance(
        conn,
        actor_id,
        SKILL_ID,
        application_id,
    )

    score_factor = max(0.0, min(1.0, float(capability.skill_score) / 100.0))
    precision = max(
        0.0,
        min(1.0, score_factor * performance.multiplier("precision")),
    )
    recovery = max(
        0.0,
        min(1.0, score_factor * performance.multiplier("adaptation")),
    )
    control = max(
        0.0,
        min(1.0, score_factor * performance.multiplier("reasoning_quality")),
    )
    error_severity = max(0.0, min(1.0, 1.0 - control))

    indices = {
        "quality_precision": round(precision, 6),
        "error_probability_severity": round(error_severity, 6),
        "partial_failure_recovery": round(recovery, 6),
    }
    if precision >= 0.80 and recovery >= 0.80 and error_severity <= 0.20:
        outcome_class = "strong"
    elif precision >= 0.65 and recovery >= 0.65 and error_severity <= 0.35:
        outcome_class = "solid"
    elif precision >= 0.45 and recovery >= 0.45 and error_severity <= 0.55:
        outcome_class = "limited"
    else:
        outcome_class = "poor"

    contract = _interaction_contract(task)
    return {
        "source": SOURCE,
        "task": {
            "task_id": task_assessment.task_id,
            "task_revision": task_assessment.task_revision,
            "status": task_assessment.status,
            "target_entity_id": task_assessment.target_entity_id,
            "target_definition_id": task_assessment.target_definition_id,
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
        "performance": {
            "contract_id": performance.contract_id,
            "dimensions": [asdict(item) for item in performance.dimensions],
            "principles": list(performance.principles),
        },
        "authorization": authorization,
        "indices": indices,
        "outcome_class": outcome_class,
        "consequence": {
            "mode": str(contract.get("consequence_mode") or ""),
            "injury_state_mutated": False,
            "target_state_mutated": False,
        },
        "learning_evidence": False,
        "world_mutation_policy": "time_and_needs_only_no_combat_injury_mutation",
    }


def controlled_h2h_application_evidence(
    outcome: dict[str, Any],
    *,
    action_id: str,
    actor_id: str,
    duration_minutes: int,
) -> dict[str, Any]:
    capability = outcome["capability"]
    return {
        "source": SOURCE,
        "evidence_type": "skill_application",
        "action_id": action_id,
        "actor_id": actor_id,
        "participant_id": outcome["authorization"]["participant_id"],
        "skill_id": capability["skill_id"],
        "application_id": capability["application_id"],
        "task_id": outcome["task"]["task_id"],
        "task_revision": outcome["task"]["task_revision"],
        "target_entity_id": outcome["task"]["target_entity_id"],
        "target_definition_id": outcome["task"]["target_definition_id"],
        "challenge_class": capability["challenge_class"],
        "capability_status": capability["status"],
        "authorization_mode": outcome["authorization"]["authorization_mode"],
        "outcome_class": outcome["outcome_class"],
        "outcome_indices": dict(outcome["indices"]),
        "consequence_mode": outcome["consequence"]["mode"],
        "duration_minutes": int(duration_minutes),
        "learning_evidence": False,
    }

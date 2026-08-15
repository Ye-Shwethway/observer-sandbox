from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict
from typing import Any

from .cognitive_performance import assess_actor_cognitive_performance
from .represented_skill_task_instance import (
    RepresentedSkillTaskInstanceAssessment,
    assess_represented_skill_task_instance,
)


DIAGNOSE_ACTION = "diagnose"
TASK_ID = "technology_known_system_fault_diagnostic_sim_v1"
SIMULATOR_ID = "obj_thorne_estate_intel_known_fault_diagnostic_simulator"
SIMULATOR_DEFINITION_ID = "represented_task:technology_known_fault_diagnostic_simulator_v1"
SIMULATOR_ROOM_ID = "loc_thorne_estate_intelligence_hub"
SIMULATOR_CAPABILITIES = (
    "inspect",
    DIAGNOSE_ACTION,
    "diagnostic_interface",
    "technical_documentation",
)
SOURCE = "technology-diagnostic-task-runtime-v1"


class TechnologyDiagnosticRuntimeError(ValueError):
    pass


def seed_technology_diagnostic_runtime(conn: sqlite3.Connection) -> None:
    """Seed the first low-risk represented Skill gameplay target and action."""

    if conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='location'",
        (SIMULATOR_ROOM_ID,),
    ).fetchone() is None:
        raise TechnologyDiagnosticRuntimeError(
            f"Technology diagnostic simulator room {SIMULATOR_ROOM_ID!r} does not exist"
        )

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
            DIAGNOSE_ACTION,
            "Diagnose",
            10,
            120,
            "object",
            DIAGNOSE_ACTION,
            1,
            json.dumps({}),
            json.dumps({}),
            json.dumps({}),
            json.dumps({"source": SOURCE, "task_id": TASK_ID}, sort_keys=True),
        ),
    )
    conn.execute(
        """
        INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id)
        VALUES(?,?,?,?,?)
        ON CONFLICT(id) DO UPDATE SET
            entity_type=excluded.entity_type,
            name=excluded.name,
            capabilities_json=excluded.capabilities_json,
            definition_id=excluded.definition_id,
            updated_at=CURRENT_TIMESTAMP
        """,
        (
            SIMULATOR_ID,
            "object",
            "Known-System Diagnostic Simulator",
            json.dumps(list(SIMULATOR_CAPABILITIES)),
            SIMULATOR_DEFINITION_ID,
        ),
    )
    conn.execute(
        "DELETE FROM relations WHERE relation_type='contains' AND target_id=?",
        (SIMULATOR_ID,),
    )
    conn.execute(
        "INSERT OR IGNORE INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
        (SIMULATOR_ROOM_ID, "contains", SIMULATOR_ID),
    )
    conn.commit()


def _target_capabilities(conn: sqlite3.Connection, target_id: str) -> tuple[str, ...]:
    row = conn.execute(
        "SELECT capabilities_json FROM entities WHERE id=? AND entity_type='object'",
        (target_id,),
    ).fetchone()
    if row is None:
        raise TechnologyDiagnosticRuntimeError(f"Diagnostic target {target_id!r} does not exist")
    try:
        values = json.loads(row["capabilities_json"] or "[]")
    except (TypeError, json.JSONDecodeError) as exc:
        raise TechnologyDiagnosticRuntimeError(
            f"Diagnostic target {target_id!r} has invalid capabilities JSON"
        ) from exc
    if not isinstance(values, list) or not all(isinstance(item, str) and item for item in values):
        raise TechnologyDiagnosticRuntimeError(
            f"Diagnostic target {target_id!r} has malformed capabilities"
        )
    return tuple(sorted(set(values)))


def assess_technology_diagnostic_action(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
) -> RepresentedSkillTaskInstanceAssessment:
    capabilities = _target_capabilities(conn, target_id)
    return assess_represented_skill_task_instance(
        conn,
        actor_id,
        TASK_ID,
        target_id,
        resource_capabilities=capabilities,
    )


def validate_technology_diagnostic_action(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str | None,
) -> RepresentedSkillTaskInstanceAssessment:
    if not target_id:
        raise TechnologyDiagnosticRuntimeError("Diagnose action requires a target")
    assessment = assess_technology_diagnostic_action(conn, actor_id, target_id)
    if assessment.status == "unsupported":
        raise TechnologyDiagnosticRuntimeError(
            "Actor does not meet the represented diagnostic task capability contract: "
            + ", ".join(assessment.reasons)
        )
    return assessment


def technology_diagnostic_outcome(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
) -> dict[str, Any]:
    """Resolve one deterministic low-risk diagnostic outcome.

    Feasibility remains owned by the represented task instance resolver. The
    cognitive/performance layer only shapes bounded quality dimensions after the
    task is supported or constrained.
    """

    task = validate_technology_diagnostic_action(conn, actor_id, target_id)
    capability = task.capability
    performance = assess_actor_cognitive_performance(
        conn,
        actor_id,
        "technology",
        "diagnose_known_system_fault",
    )
    score_factor = max(0.0, min(1.0, float(capability.skill_score) / 100.0))
    precision = max(0.0, min(1.0, score_factor * performance.multiplier("precision")))
    information = max(
        0.0,
        min(1.0, score_factor * performance.multiplier("reasoning_quality")),
    )
    recovery_multiplier = (
        performance.multiplier("reasoning_quality") + performance.multiplier("adaptation")
    ) / 2.0
    recovery = max(0.0, min(1.0, score_factor * recovery_multiplier))

    if task.status == "constrained":
        # Supporting resources are non-gating but their absence must remain visible
        # in outcome quality. The bounded penalty is part of this represented task
        # runtime, not a hidden change to Skill proficiency.
        support_multiplier = 0.92
        precision *= support_multiplier
        information *= support_multiplier
        recovery *= support_multiplier
    else:
        support_multiplier = 1.0

    indices = {
        "quality_precision": round(precision, 6),
        "information_gained": round(information, 6),
        "partial_failure_recovery": round(recovery, 6),
    }
    minimum = min(indices.values())
    if minimum >= 0.80:
        outcome_class = "strong"
    elif minimum >= 0.65:
        outcome_class = "solid"
    elif minimum >= 0.45:
        outcome_class = "limited"
    else:
        outcome_class = "poor"

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
        "cognitive_performance": {
            "contract_id": performance.contract_id,
            "dimensions": [asdict(item) for item in performance.dimensions],
            "principles": list(performance.principles),
        },
        "support_multiplier": support_multiplier,
        "indices": indices,
        "outcome_class": outcome_class,
        "learning_evidence": False,
    }


def technology_diagnostic_application_evidence(
    outcome: dict[str, Any],
    *,
    action_id: str,
    actor_id: str,
    duration_minutes: int,
) -> dict[str, Any]:
    return {
        "source": SOURCE,
        "evidence_type": "skill_application",
        "action_id": action_id,
        "actor_id": actor_id,
        "skill_id": "technology",
        "application_id": "diagnose_known_system_fault",
        "task_id": outcome["task"]["task_id"],
        "task_revision": outcome["task"]["task_revision"],
        "target_entity_id": outcome["task"]["target_entity_id"],
        "target_definition_id": outcome["task"]["target_definition_id"],
        "challenge_class": outcome["capability"]["challenge_class"],
        "capability_status": outcome["capability"]["status"],
        "outcome_class": outcome["outcome_class"],
        "outcome_indices": dict(outcome["indices"]),
        "duration_minutes": int(duration_minutes),
        "learning_evidence": False,
    }

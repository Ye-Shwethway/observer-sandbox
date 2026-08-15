from __future__ import annotations

import json
import sqlite3
from dataclasses import asdict, dataclass
from typing import Any

from .cognitive_performance import assess_actor_cognitive_performance
from .represented_skill_task_instance import (
    RepresentedSkillTaskInstanceAssessment,
    assess_represented_skill_task_instance,
)


SOURCE = "represented-skill-runtime-batch-v1"
SUPPORT_MULTIPLIER = 0.92


@dataclass(frozen=True)
class BatchTaskSpec:
    action: str
    label: str
    task_id: str
    skill_id: str
    application_id: str
    simulator_id: str
    simulator_name: str
    simulator_definition_id: str
    room_id: str
    capabilities: tuple[str, ...]


TASK_SPECS = (
    BatchTaskSpec(
        action="plan",
        label="Plan",
        task_id="tactical_maneuver_planning_sim_v1",
        skill_id="tactical_planning",
        application_id="plan_tactical_maneuver",
        simulator_id="obj_thorne_estate_intel_tactical_maneuver_planning_simulator",
        simulator_name="Tactical Maneuver Planning Simulator",
        simulator_definition_id="represented_task:tactical_maneuver_planning_simulator_v1",
        room_id="loc_thorne_estate_intelligence_hub",
        capabilities=("inspect", "plan", "situational_intelligence", "terrain_or_layout_information"),
    ),
    BatchTaskSpec(
        action="navigate",
        label="Navigate",
        task_id="survival_field_navigation_sim_v1",
        skill_id="survival",
        application_id="navigate_field_environment",
        simulator_id="obj_thorne_estate_training_field_navigation_simulator",
        simulator_name="Field Navigation Simulator",
        simulator_definition_id="represented_task:survival_field_navigation_simulator_v1",
        room_id="loc_thorne_estate_training_hall",
        capabilities=("inspect", "navigate", "navigation_aid"),
    ),
    BatchTaskSpec(
        action="sustain",
        label="Sustain",
        task_id="survival_field_sustainment_sim_v1",
        skill_id="survival",
        application_id="establish_field_sustainment",
        simulator_id="obj_thorne_estate_training_field_sustainment_simulator",
        simulator_name="Field Sustainment Simulator",
        simulator_definition_id="represented_task:survival_field_sustainment_simulator_v1",
        room_id="loc_thorne_estate_training_hall",
        capabilities=("inspect", "sustain", "field_sustainment_materials", "field_toolkit"),
    ),
)

SPEC_BY_ACTION = {spec.action: spec for spec in TASK_SPECS}
SPEC_BY_TASK = {spec.task_id: spec for spec in TASK_SPECS}
BATCH_ACTIONS = frozenset(SPEC_BY_ACTION)


class RepresentedSkillRuntimeBatchError(ValueError):
    pass


def seed_represented_skill_runtime_batch(conn: sqlite3.Connection) -> None:
    """Seed low-risk simulation-only represented Skill applications as one pattern batch."""

    for spec in TASK_SPECS:
        if conn.execute(
            "SELECT 1 FROM entities WHERE id=? AND entity_type='location'",
            (spec.room_id,),
        ).fetchone() is None:
            raise RepresentedSkillRuntimeBatchError(
                f"Represented Skill simulator room {spec.room_id!r} does not exist"
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
                spec.action,
                spec.label,
                10,
                120,
                "object",
                spec.action,
                1,
                json.dumps({}),
                json.dumps({}),
                json.dumps({}),
                json.dumps({"source": SOURCE, "task_id": spec.task_id}, sort_keys=True),
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
                spec.simulator_id,
                "object",
                spec.simulator_name,
                json.dumps(list(spec.capabilities)),
                spec.simulator_definition_id,
            ),
        )
        conn.execute(
            "DELETE FROM relations WHERE relation_type='contains' AND target_id=?",
            (spec.simulator_id,),
        )
        conn.execute(
            "INSERT OR IGNORE INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
            (spec.room_id, "contains", spec.simulator_id),
        )
    conn.commit()


def _target_capabilities(
    conn: sqlite3.Connection,
    target_id: str,
) -> tuple[str, ...]:
    row = conn.execute(
        "SELECT capabilities_json FROM entities WHERE id=? AND entity_type='object'",
        (target_id,),
    ).fetchone()
    if row is None:
        raise RepresentedSkillRuntimeBatchError(
            f"Represented Skill target {target_id!r} does not exist"
        )
    try:
        values = json.loads(row["capabilities_json"] or "[]")
    except (TypeError, json.JSONDecodeError) as exc:
        raise RepresentedSkillRuntimeBatchError(
            f"Represented Skill target {target_id!r} has invalid capabilities JSON"
        ) from exc
    if not isinstance(values, list) or not all(
        isinstance(item, str) and item for item in values
    ):
        raise RepresentedSkillRuntimeBatchError(
            f"Represented Skill target {target_id!r} has malformed capabilities"
        )
    return tuple(sorted(set(values)))


def spec_for_action(action_name: str) -> BatchTaskSpec | None:
    return SPEC_BY_ACTION.get(action_name)


def assess_batch_action(
    conn: sqlite3.Connection,
    actor_id: str,
    action_name: str,
    target_id: str,
) -> RepresentedSkillTaskInstanceAssessment:
    spec = spec_for_action(action_name)
    if spec is None:
        raise RepresentedSkillRuntimeBatchError(
            f"Action {action_name!r} is not owned by {SOURCE}"
        )
    return assess_represented_skill_task_instance(
        conn,
        actor_id,
        spec.task_id,
        target_id,
        resource_capabilities=_target_capabilities(conn, target_id),
    )


def validate_batch_action(
    conn: sqlite3.Connection,
    actor_id: str,
    action_name: str,
    target_id: str | None,
) -> RepresentedSkillTaskInstanceAssessment:
    if not target_id:
        raise RepresentedSkillRuntimeBatchError(
            f"{action_name.title()} action requires a target"
        )
    assessment = assess_batch_action(conn, actor_id, action_name, target_id)
    if assessment.status == "unsupported":
        raise RepresentedSkillRuntimeBatchError(
            "Actor does not meet the represented Skill application contract: "
            + ", ".join(assessment.reasons)
        )
    return assessment


def represented_skill_batch_outcome(
    conn: sqlite3.Connection,
    actor_id: str,
    action_name: str,
    target_id: str,
) -> dict[str, Any]:
    """Resolve one deterministic simulation-only represented Skill outcome."""

    spec = spec_for_action(action_name)
    if spec is None:
        raise RepresentedSkillRuntimeBatchError(
            f"Action {action_name!r} is not owned by {SOURCE}"
        )
    task = validate_batch_action(conn, actor_id, action_name, target_id)
    capability = task.capability
    performance = assess_actor_cognitive_performance(
        conn,
        actor_id,
        spec.skill_id,
        spec.application_id,
    )
    score_factor = max(0.0, min(1.0, float(capability.skill_score) / 100.0))
    precision = max(
        0.0,
        min(1.0, score_factor * performance.multiplier("precision")),
    )
    information = max(
        0.0,
        min(1.0, score_factor * performance.multiplier("reasoning_quality")),
    )
    recovery_multiplier = (
        performance.multiplier("reasoning_quality")
        + performance.multiplier("adaptation")
    ) / 2.0
    recovery = max(0.0, min(1.0, score_factor * recovery_multiplier))

    support_multiplier = SUPPORT_MULTIPLIER if task.status == "constrained" else 1.0
    precision *= support_multiplier
    information *= support_multiplier
    recovery *= support_multiplier

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
            "recognized_resource_capabilities": list(
                task.recognized_resource_capabilities
            ),
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
        "world_mutation_policy": "simulation_evidence_only",
    }


def represented_skill_batch_application_evidence(
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
        "duration_minutes": int(duration_minutes),
        "learning_evidence": False,
    }

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Iterable

from .actor_skill_capability import assess_actor_skill_application
from .skill_capability import SkillCapabilityAssessment
from .represented_skill_tasks import represented_skill_task


class RepresentedSkillTaskInstanceError(ValueError):
    pass


@dataclass(frozen=True)
class RepresentedSkillTaskInstanceAssessment:
    task_id: str
    task_revision: str
    actor_id: str
    target_entity_id: str
    target_entity_type: str
    target_definition_id: str
    target_capabilities: tuple[str, ...]
    supplied_resource_capabilities: tuple[str, ...]
    recognized_resource_capabilities: tuple[str, ...]
    capability: SkillCapabilityAssessment

    @property
    def status(self) -> str:
        return self.capability.status

    @property
    def reasons(self) -> tuple[str, ...]:
        return self.capability.reasons


def _stable_tokens(values: Iterable[str] | None) -> tuple[str, ...]:
    if values is None:
        return ()
    result: list[str] = []
    for value in values:
        if not isinstance(value, str) or not value:
            raise RepresentedSkillTaskInstanceError(
                "resource capabilities must be non-empty strings"
            )
        if value not in result:
            result.append(value)
    return tuple(sorted(result))


def _target_entity(conn: sqlite3.Connection, target_entity_id: str) -> dict[str, Any]:
    row = conn.execute(
        "SELECT id,entity_type,definition_id,capabilities_json FROM entities WHERE id=?",
        (target_entity_id,),
    ).fetchone()
    if row is None:
        raise RepresentedSkillTaskInstanceError(
            f"Represented task target {target_entity_id!r} does not exist"
        )
    try:
        capabilities = json.loads(row["capabilities_json"] or "[]")
    except (TypeError, json.JSONDecodeError) as exc:
        raise RepresentedSkillTaskInstanceError(
            f"Represented task target {target_entity_id!r} has invalid capabilities JSON"
        ) from exc
    if not isinstance(capabilities, list) or not all(
        isinstance(value, str) and value for value in capabilities
    ):
        raise RepresentedSkillTaskInstanceError(
            f"Represented task target {target_entity_id!r} has malformed capabilities"
        )
    return {
        "id": str(row["id"]),
        "entity_type": str(row["entity_type"]),
        "definition_id": row["definition_id"],
        "capabilities": tuple(sorted(set(capabilities))),
    }


def _validate_target_binding(target: dict[str, Any], task: dict[str, Any]) -> None:
    contract = task["target_contract"]
    expected_type = str(contract["entity_type"])
    expected_definition = str(contract["definition_id"])
    if target["entity_type"] != expected_type:
        raise RepresentedSkillTaskInstanceError(
            f"Target {target['id']!r} has entity type {target['entity_type']!r}; expected {expected_type!r}"
        )
    if target["definition_id"] != expected_definition:
        raise RepresentedSkillTaskInstanceError(
            f"Target {target['id']!r} has definition {target['definition_id']!r}; expected {expected_definition!r}"
        )
    missing = [
        capability
        for capability in contract["required_capabilities_all"]
        if capability not in target["capabilities"]
    ]
    if missing:
        raise RepresentedSkillTaskInstanceError(
            f"Target {target['id']!r} is missing required task capabilities {missing!r}"
        )


def assess_represented_skill_task_instance(
    conn: sqlite3.Connection,
    actor_id: str,
    task_id: str,
    target_entity_id: str,
    *,
    resource_capabilities: Iterable[str] | None = None,
    task_config: dict[str, Any] | None = None,
    skill_config: dict[str, Any] | None = None,
) -> RepresentedSkillTaskInstanceAssessment:
    """Resolve one represented task instance without mutating world or actor state.

    The represented task owns application/challenge/context and narrows the resource
    envelope. The caller supplies currently available resource capability tokens.
    Target authority is exact entity type + definition_id + required capabilities;
    names, model prose, inventory guesses, and ambient state are never authority.
    """

    task = represented_skill_task(task_id, config=task_config)
    target = _target_entity(conn, target_entity_id)
    _validate_target_binding(target, task)

    supplied_resources = _stable_tokens(resource_capabilities)
    resource_contract = task["resource_contract"]
    task_resource_envelope = set(resource_contract["required_capabilities_any"]) | set(
        resource_contract["supporting_capabilities"]
    )
    recognized_resources = tuple(
        value for value in supplied_resources if value in task_resource_envelope
    )

    capability = assess_actor_skill_application(
        conn,
        actor_id,
        str(task["skill_id"]),
        str(task["application_id"]),
        challenge_class=str(task["challenge_class"]),
        context_tags=tuple(task["context_tags"]),
        resource_capabilities=recognized_resources,
        config=skill_config,
    )

    return RepresentedSkillTaskInstanceAssessment(
        task_id=str(task["task_id"]),
        task_revision=str(task["revision"]),
        actor_id=actor_id,
        target_entity_id=target_entity_id,
        target_entity_type=target["entity_type"],
        target_definition_id=str(target["definition_id"]),
        target_capabilities=target["capabilities"],
        supplied_resource_capabilities=supplied_resources,
        recognized_resource_capabilities=recognized_resources,
        capability=capability,
    )

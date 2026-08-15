from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from .skill_application_requirements import get_executable_skill_application
from .skill_definitions import ALLOWED_RISK_CLASSES, CHALLENGE_CLASSES


REPO_ROOT = Path(__file__).resolve().parents[2]
REPRESENTED_SKILL_TASKS_CONFIG_PATH = REPO_ROOT / "config" / "represented_skill_tasks.v1.json"
TASK_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
ALLOWED_STATUSES = {"active", "experimental", "deprecated"}
ALLOWED_TASK_MODES = {"simulation_safe", "represented_low_risk", "represented_consequential"}
ALLOWED_TARGET_ENTITY_TYPES = {"object", "location", "character"}
FORBIDDEN_ACTOR_STATE_KEYS = {"score", "experience", "tier", "grade", "actor_id", "entity_id"}


class RepresentedSkillTaskValidationError(ValueError):
    pass


def _load_json(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RepresentedSkillTaskValidationError(f"{path}: expected object root")
    return value


@lru_cache(maxsize=1)
def load_represented_skill_tasks(
    path: str | Path = REPRESENTED_SKILL_TASKS_CONFIG_PATH,
) -> dict[str, Any]:
    return _load_json(path)


def _required_string(value: dict[str, Any], key: str, path: str) -> str:
    result = value.get(key)
    if not isinstance(result, str) or not result.strip():
        raise RepresentedSkillTaskValidationError(f"{path}.{key}: required non-empty string")
    return result.strip()


def _string_list(value: object, path: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise RepresentedSkillTaskValidationError(f"{path}: expected list")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise RepresentedSkillTaskValidationError(f"{path}[{index}]: expected non-empty string")
        result.append(item.strip())
    if nonempty and not result:
        raise RepresentedSkillTaskValidationError(f"{path}: must not be empty")
    if len(result) != len(set(result)):
        raise RepresentedSkillTaskValidationError(f"{path}: duplicate values are not allowed")
    return result


def _walk_forbidden_actor_state(value: object, path: str) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in FORBIDDEN_ACTOR_STATE_KEYS:
                raise RepresentedSkillTaskValidationError(
                    f"{path}.{key}: represented task definitions must not contain actor state"
                )
            _walk_forbidden_actor_state(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_forbidden_actor_state(child, f"{path}[{index}]")


def _validate_target_contract(task: dict[str, Any], path: str) -> None:
    target = task.get("target_contract")
    if not isinstance(target, dict):
        raise RepresentedSkillTaskValidationError(f"{path}.target_contract: expected object")
    entity_type = _required_string(target, "entity_type", f"{path}.target_contract")
    if entity_type not in ALLOWED_TARGET_ENTITY_TYPES:
        raise RepresentedSkillTaskValidationError(
            f"{path}.target_contract.entity_type: unsupported {entity_type!r}"
        )
    definition_id = _required_string(target, "definition_id", f"{path}.target_contract")
    if definition_id.startswith("skill_practice:"):
        raise RepresentedSkillTaskValidationError(
            f"{path}.target_contract.definition_id: practice targets cannot become application authority"
        )
    _string_list(
        target.get("required_capabilities_all"),
        f"{path}.target_contract.required_capabilities_all",
        nonempty=True,
    )


def _validate_against_application(task: dict[str, Any], path: str) -> None:
    skill_id = _required_string(task, "skill_id", path)
    application_id = _required_string(task, "application_id", path)
    try:
        _definition, application = get_executable_skill_application(skill_id, application_id)
    except (KeyError, ValueError) as exc:
        raise RepresentedSkillTaskValidationError(
            f"{path}: unknown or non-executable Skill application {skill_id}.{application_id}"
        ) from exc

    challenge = _required_string(task, "challenge_class", path)
    if challenge not in CHALLENGE_CLASSES:
        raise RepresentedSkillTaskValidationError(f"{path}.challenge_class: unknown {challenge!r}")
    if challenge not in (application.get("challenge_classes") or []):
        raise RepresentedSkillTaskValidationError(
            f"{path}.challenge_class: application does not declare {challenge!r}"
        )

    requirements = application.get("requirements") or {}
    context = _string_list(task.get("context_tags"), f"{path}.context_tags", nonempty=True)
    missing_context = [
        value for value in (requirements.get("context_tags_all") or []) if value not in context
    ]
    if missing_context:
        raise RepresentedSkillTaskValidationError(
            f"{path}.context_tags: weakens application requirements; missing {missing_context!r}"
        )

    resource = task.get("resource_contract")
    if not isinstance(resource, dict):
        raise RepresentedSkillTaskValidationError(f"{path}.resource_contract: expected object")
    required_any = _string_list(
        resource.get("required_capabilities_any"),
        f"{path}.resource_contract.required_capabilities_any",
        nonempty=True,
    )
    application_required_any = set(requirements.get("resource_capabilities_any") or [])
    if not set(required_any).issubset(application_required_any):
        raise RepresentedSkillTaskValidationError(
            f"{path}.resource_contract.required_capabilities_any: must narrow the application's declared required-any capabilities"
        )
    supporting = _string_list(
        resource.get("supporting_capabilities"),
        f"{path}.resource_contract.supporting_capabilities",
    )
    missing_supporting = [
        value
        for value in (requirements.get("supporting_resource_capabilities") or [])
        if value not in supporting
    ]
    if missing_supporting:
        raise RepresentedSkillTaskValidationError(
            f"{path}.resource_contract.supporting_capabilities: weakens application support contract; missing {missing_supporting!r}"
        )

    outcomes = _string_list(
        task.get("outcome_dimensions"),
        f"{path}.outcome_dimensions",
        nonempty=True,
    )
    allowed_outcomes = set(application.get("gameplay_effects") or [])
    if not set(outcomes).issubset(allowed_outcomes):
        raise RepresentedSkillTaskValidationError(
            f"{path}.outcome_dimensions: contains dimensions outside the Skill application contract"
        )


def _validate_evidence(task: dict[str, Any], path: str) -> None:
    evidence = task.get("evidence_policy")
    if not isinstance(evidence, dict):
        raise RepresentedSkillTaskValidationError(f"{path}.evidence_policy: expected object")
    if _required_string(evidence, "application_evidence", f"{path}.evidence_policy") != "deferred_until_action_integration":
        raise RepresentedSkillTaskValidationError(
            f"{path}.evidence_policy.application_evidence: v1 task contract must defer evidence until action integration"
        )
    if evidence.get("learning_evidence") is not False:
        raise RepresentedSkillTaskValidationError(
            f"{path}.evidence_policy.learning_evidence: represented task definition must not imply learning evidence"
        )


def validate_represented_skill_tasks(config: dict[str, Any] | None = None) -> dict[str, Any]:
    source = config if config is not None else load_represented_skill_tasks()
    revision = source.get("revision")
    if not isinstance(revision, str) or not revision.strip():
        raise RepresentedSkillTaskValidationError("revision: required non-empty string")
    tasks = source.get("tasks")
    if not isinstance(tasks, dict) or not tasks:
        raise RepresentedSkillTaskValidationError("tasks: expected non-empty object")

    _walk_forbidden_actor_state(tasks, "tasks")
    for task_id, task in tasks.items():
        path = f"tasks.{task_id}"
        if not isinstance(task_id, str) or not TASK_ID_RE.fullmatch(task_id):
            raise RepresentedSkillTaskValidationError(f"{path}: invalid task id")
        if not isinstance(task, dict):
            raise RepresentedSkillTaskValidationError(f"{path}: expected object")
        if task.get("task_id") != task_id:
            raise RepresentedSkillTaskValidationError(
                f"{path}.task_id: must equal registry key {task_id!r}"
            )
        _required_string(task, "name", path)
        status = _required_string(task, "status", path)
        if status not in ALLOWED_STATUSES:
            raise RepresentedSkillTaskValidationError(f"{path}.status: unsupported {status!r}")
        mode = _required_string(task, "task_mode", path)
        if mode not in ALLOWED_TASK_MODES:
            raise RepresentedSkillTaskValidationError(f"{path}.task_mode: unsupported {mode!r}")
        risk = _required_string(task, "risk_class", path)
        if risk not in ALLOWED_RISK_CLASSES:
            raise RepresentedSkillTaskValidationError(f"{path}.risk_class: unsupported {risk!r}")
        if mode == "simulation_safe" and risk != "low":
            raise RepresentedSkillTaskValidationError(
                f"{path}.risk_class: simulation_safe tasks must be low risk"
            )
        _validate_target_contract(task, path)
        _validate_against_application(task, path)
        _validate_evidence(task, path)
        provenance = task.get("provenance")
        if not isinstance(provenance, dict):
            raise RepresentedSkillTaskValidationError(f"{path}.provenance: expected object")
        _required_string(provenance, "source", f"{path}.provenance")
    return source


def represented_skill_task(
    task_id: str,
    *,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source = validate_represented_skill_tasks(config)
    task = (source.get("tasks") or {}).get(task_id)
    if not isinstance(task, dict):
        raise KeyError(f"Unknown represented Skill task: {task_id}")
    result = dict(task)
    result["revision"] = str(source["revision"])
    return result

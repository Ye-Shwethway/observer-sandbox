from __future__ import annotations

import re
from typing import Any

from .skill_definitions import get_skill_definition


SEMANTIC_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)*$")
KNOWLEDGE_MODES = {"declarative_support_only"}
REQUIRED_RESOURCE_MODES = {"any", "none"}


class SkillApplicationRequirementError(ValueError):
    pass


def _semantic_list(value: object, path: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list):
        raise SkillApplicationRequirementError(f"{path}: expected list")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not SEMANTIC_ID_RE.fullmatch(item):
            raise SkillApplicationRequirementError(
                f"{path}[{index}]: expected stable lower_snake semantic id"
            )
        result.append(item)
    if nonempty and not result:
        raise SkillApplicationRequirementError(f"{path}: must not be empty")
    if len(result) != len(set(result)):
        raise SkillApplicationRequirementError(f"{path}: duplicate semantic ids are not allowed")
    return result


def validate_application_requirements(
    definition: dict[str, Any],
    *,
    require_all_applications: bool = True,
) -> dict[str, Any]:
    skill_id = definition.get("skill_id")
    if not isinstance(skill_id, str) or not skill_id:
        raise SkillApplicationRequirementError("skill definition has no skill_id")

    knowledge_defs = definition.get("knowledge_requirements")
    if not isinstance(knowledge_defs, list):
        raise SkillApplicationRequirementError(f"{skill_id}.knowledge_requirements: expected list")
    known_knowledge = {
        item.get("knowledge_key")
        for item in knowledge_defs
        if isinstance(item, dict) and isinstance(item.get("knowledge_key"), str)
    }

    applications = definition.get("applications")
    if not isinstance(applications, list) or not applications:
        raise SkillApplicationRequirementError(f"{skill_id}.applications: expected non-empty list")

    for index, application in enumerate(applications):
        path = f"{skill_id}.applications[{index}]"
        if not isinstance(application, dict):
            raise SkillApplicationRequirementError(f"{path}: expected object")
        application_id = application.get("application_id")
        if not isinstance(application_id, str) or not SEMANTIC_ID_RE.fullmatch(application_id):
            raise SkillApplicationRequirementError(f"{path}.application_id: invalid semantic id")

        requirements = application.get("requirements")
        if requirements is None and not require_all_applications:
            continue
        if not isinstance(requirements, dict):
            raise SkillApplicationRequirementError(
                f"{path}.requirements: machine-readable requirements are required"
            )

        context_tags = _semantic_list(
            requirements.get("context_tags_all"),
            f"{path}.requirements.context_tags_all",
            nonempty=True,
        )
        resource_mode = requirements.get("required_resource_mode")
        if resource_mode not in REQUIRED_RESOURCE_MODES:
            raise SkillApplicationRequirementError(
                f"{path}.requirements.required_resource_mode: expected one of {sorted(REQUIRED_RESOURCE_MODES)!r}"
            )
        resource_any = _semantic_list(
            requirements.get("resource_capabilities_any", []),
            f"{path}.requirements.resource_capabilities_any",
            nonempty=resource_mode == "any",
        )
        if resource_mode == "none" and resource_any:
            raise SkillApplicationRequirementError(
                f"{path}.requirements.resource_capabilities_any: must be empty when required_resource_mode is 'none'"
            )
        supporting_resources = _semantic_list(
            requirements.get("supporting_resource_capabilities", []),
            f"{path}.requirements.supporting_resource_capabilities",
        )
        if set(resource_any) & set(supporting_resources):
            raise SkillApplicationRequirementError(
                f"{path}.requirements: required-any and supporting resource capabilities must be distinct"
            )
        if set(context_tags) & set(resource_any + supporting_resources):
            raise SkillApplicationRequirementError(
                f"{path}.requirements: context tags and resource capabilities must use distinct semantic namespaces"
            )

        knowledge = requirements.get("knowledge")
        if not isinstance(knowledge, dict):
            raise SkillApplicationRequirementError(f"{path}.requirements.knowledge: expected object")
        mode = knowledge.get("mode")
        if mode not in KNOWLEDGE_MODES:
            raise SkillApplicationRequirementError(
                f"{path}.requirements.knowledge.mode: unsupported mode {mode!r}"
            )
        supporting_keys = _semantic_list(
            knowledge.get("supporting_keys", []),
            f"{path}.requirements.knowledge.supporting_keys",
        )
        unknown = sorted(set(supporting_keys) - known_knowledge)
        if unknown:
            raise SkillApplicationRequirementError(
                f"{path}.requirements.knowledge.supporting_keys: unknown knowledge keys {unknown!r}"
            )

    return definition


def get_executable_skill_application(
    skill_id: str,
    application_id: str,
    *,
    config: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    definition = get_skill_definition(skill_id, config=config)
    validate_application_requirements(definition)
    for application in definition["applications"]:
        if application.get("application_id") == application_id:
            return definition, application
    raise KeyError(f"Unknown Skill application: {skill_id}.{application_id}")

from __future__ import annotations

import copy
import re
from typing import Any

from .skill_definitions import get_skill_definition
from .skill_hierarchy import load_skill_hierarchy_config


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


def _hierarchy_application_binding(
    skill_id: str,
    application_id: str,
) -> tuple[str, str, dict[str, Any]] | None:
    """Resolve one explicit component application binding from hierarchy config.

    Returns ``(component_skill_id, source_skill_id, authority)`` both when the
    caller names the component and when it names the legacy source. This lets the
    resolver make transfer of executable authority explicit instead of allowing
    the hidden compatibility projection to remain a second capability authority.
    """

    source = load_skill_hierarchy_config()
    for hierarchy in (source.get("hierarchies") or {}).values():
        if not isinstance(hierarchy, dict):
            continue
        components = hierarchy.get("components") or {}
        if not isinstance(components, dict):
            continue
        for component_id, component in components.items():
            if not isinstance(component_id, str) or not isinstance(component, dict):
                continue
            authority_map = component.get("application_authority") or {}
            if not isinstance(authority_map, dict):
                continue
            authority = authority_map.get(application_id)
            if not isinstance(authority, dict) or authority.get("status") != "active":
                continue
            source_skill_id = authority.get("source_skill_id")
            if not isinstance(source_skill_id, str) or not source_skill_id:
                continue
            if skill_id in {component_id, source_skill_id}:
                return component_id, source_skill_id, authority
    return None


def _component_application_definition(
    component_skill_id: str,
    source_skill_id: str,
    application_id: str,
    authority: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    source_definition = get_skill_definition(source_skill_id)
    source_application = next(
        (
            value
            for value in (source_definition.get("applications") or [])
            if isinstance(value, dict) and value.get("application_id") == application_id
        ),
        None,
    )
    if source_application is None:
        raise KeyError(
            f"Hierarchy application source is missing: {source_skill_id}.{application_id}"
        )

    definition = copy.deepcopy(source_definition)
    application = copy.deepcopy(source_application)
    requirements_override = authority.get("requirements_override")
    if requirements_override is not None:
        if not isinstance(requirements_override, dict):
            raise SkillApplicationRequirementError(
                f"Hierarchy authority {component_skill_id}.{application_id} requirements_override must be an object"
            )
        application["requirements"] = copy.deepcopy(requirements_override)

    hierarchy = load_skill_hierarchy_config()
    component_name = None
    component_description = None
    for raw in (hierarchy.get("hierarchies") or {}).values():
        if not isinstance(raw, dict):
            continue
        component = (raw.get("components") or {}).get(component_skill_id)
        if isinstance(component, dict):
            component_name = component.get("name")
            component_description = component.get("description")
            break

    definition["skill_id"] = component_skill_id
    if isinstance(component_name, str) and component_name:
        definition["name"] = component_name
    if isinstance(component_description, str) and component_description:
        definition["definition"] = component_description
    definition["applications"] = [application]
    validate_application_requirements(definition)
    return definition, application


def get_executable_skill_application(
    skill_id: str,
    application_id: str,
    *,
    config: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if config is None:
        binding = _hierarchy_application_binding(skill_id, application_id)
        if binding is not None:
            component_skill_id, source_skill_id, authority = binding
            if skill_id == source_skill_id:
                raise KeyError(
                    f"Skill application authority moved to component Skill: "
                    f"{component_skill_id}.{application_id}"
                )
            return _component_application_definition(
                component_skill_id,
                source_skill_id,
                application_id,
                authority,
            )

    definition = get_skill_definition(skill_id, config=config)
    validate_application_requirements(definition)
    for application in definition["applications"]:
        if application.get("application_id") == application_id:
            return definition, application
    raise KeyError(f"Unknown Skill application: {skill_id}.{application_id}")

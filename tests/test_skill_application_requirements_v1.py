from __future__ import annotations

from copy import deepcopy

import pytest

from observer_sandbox.skill_application_requirements import (
    SkillApplicationRequirementError,
    get_executable_skill_application,
    validate_application_requirements,
)
from observer_sandbox.skill_definitions import load_validated_skill_definitions


def canonical() -> dict:
    return deepcopy(load_validated_skill_definitions())


def test_technology_application_has_executable_requirement_contract() -> None:
    config = canonical()
    definition, application = get_executable_skill_application(
        "technology",
        "diagnose_known_system_fault",
        config=config,
    )

    requirements = application["requirements"]
    assert definition["revision"] == "technology-definition-v1.1"
    assert requirements["context_tags_all"] == [
        "technical_system_represented",
        "diagnostic_evidence_available",
    ]
    assert set(requirements["resource_capabilities_any"]) == {
        "diagnostic_interface",
        "diagnostic_instrumentation",
    }
    assert requirements["knowledge"]["mode"] == "declarative_support_only"


def test_application_requirements_are_mandatory_for_executable_definitions() -> None:
    config = canonical()
    definition = config["skills"]["technology"]
    definition["applications"][0].pop("requirements")

    with pytest.raises(SkillApplicationRequirementError, match="machine-readable requirements are required"):
        validate_application_requirements(definition)


def test_context_and_resource_tokens_must_be_stable_semantic_ids() -> None:
    config = canonical()
    definition = config["skills"]["technology"]
    definition["applications"][0]["requirements"]["context_tags_all"] = [
        "a represented technical system"
    ]

    with pytest.raises(SkillApplicationRequirementError, match="lower_snake semantic id"):
        validate_application_requirements(definition)


def test_required_resource_capability_choice_cannot_be_empty() -> None:
    config = canonical()
    definition = config["skills"]["technology"]
    definition["applications"][0]["requirements"]["resource_capabilities_any"] = []

    with pytest.raises(SkillApplicationRequirementError, match="must not be empty"):
        validate_application_requirements(definition)


def test_application_knowledge_keys_must_reference_declared_skill_knowledge() -> None:
    config = canonical()
    definition = config["skills"]["technology"]
    definition["applications"][0]["requirements"]["knowledge"]["supporting_keys"].append(
        "invented_hidden_knowledge"
    )

    with pytest.raises(SkillApplicationRequirementError, match="unknown knowledge keys"):
        validate_application_requirements(definition)


def test_v1_does_not_invent_hidden_knowledge_gate() -> None:
    config = canonical()
    definition = config["skills"]["technology"]
    definition["applications"][0]["requirements"]["knowledge"]["mode"] = "required_numeric_score"

    with pytest.raises(SkillApplicationRequirementError, match="unsupported mode"):
        validate_application_requirements(definition)


def test_required_and_supporting_resource_semantics_must_not_overlap() -> None:
    config = canonical()
    definition = config["skills"]["technology"]
    requirements = definition["applications"][0]["requirements"]
    requirements["supporting_resource_capabilities"].append("diagnostic_interface")

    with pytest.raises(SkillApplicationRequirementError, match="must be distinct"):
        validate_application_requirements(definition)


def test_unknown_application_is_rejected_after_definition_validation() -> None:
    config = canonical()
    with pytest.raises(KeyError, match="Unknown Skill application"):
        get_executable_skill_application("technology", "invented_application", config=config)

from __future__ import annotations

import copy

import pytest

from observer_sandbox.represented_skill_tasks import (
    RepresentedSkillTaskValidationError,
    load_represented_skill_tasks,
    represented_skill_task,
    validate_represented_skill_tasks,
)


TASK_ID = "technology_known_system_fault_diagnostic_sim_v1"


def config_copy():
    return copy.deepcopy(load_represented_skill_tasks())


def task(config):
    return config["tasks"][TASK_ID]


def test_canonical_represented_task_registry_validates() -> None:
    source = validate_represented_skill_tasks()
    assert source["revision"] == "represented-skill-tasks-v1"
    assert list(source["tasks"]) == [TASK_ID]


def test_technology_task_is_exact_definition_bound_and_simulation_safe() -> None:
    value = represented_skill_task(TASK_ID)

    assert value["skill_id"] == "technology"
    assert value["application_id"] == "diagnose_known_system_fault"
    assert value["challenge_class"] == "standard"
    assert value["task_mode"] == "simulation_safe"
    assert value["risk_class"] == "low"
    assert value["target_contract"] == {
        "entity_type": "object",
        "definition_id": "represented_task:technology_known_fault_diagnostic_simulator_v1",
        "required_capabilities_all": ["inspect"],
    }
    assert value["evidence_policy"]["learning_evidence"] is False


def test_task_cannot_reference_unknown_skill_application() -> None:
    source = config_copy()
    task(source)["application_id"] = "imaginary_diagnostic_application"

    with pytest.raises(RepresentedSkillTaskValidationError, match="unknown or non-executable"):
        validate_represented_skill_tasks(source)


def test_task_challenge_cannot_escape_application_envelope() -> None:
    source = config_copy()
    task(source)["challenge_class"] = "extreme"

    with pytest.raises(RepresentedSkillTaskValidationError, match="does not declare"):
        validate_represented_skill_tasks(source)


def test_task_cannot_weaken_required_context() -> None:
    source = config_copy()
    task(source)["context_tags"] = ["technical_system_represented"]

    with pytest.raises(RepresentedSkillTaskValidationError, match="weakens application requirements"):
        validate_represented_skill_tasks(source)


def test_task_required_resource_must_narrow_application_declared_capabilities() -> None:
    source = config_copy()
    task(source)["resource_contract"]["required_capabilities_any"] = ["generic_computer"]

    with pytest.raises(RepresentedSkillTaskValidationError, match="must narrow"):
        validate_represented_skill_tasks(source)


def test_task_cannot_silently_drop_application_support_contract() -> None:
    source = config_copy()
    task(source)["resource_contract"]["supporting_capabilities"] = []

    with pytest.raises(RepresentedSkillTaskValidationError, match="weakens application support contract"):
        validate_represented_skill_tasks(source)


def test_task_outcomes_must_be_declared_by_skill_application() -> None:
    source = config_copy()
    task(source)["outcome_dimensions"].append("instant_mastery")

    with pytest.raises(RepresentedSkillTaskValidationError, match="outside the Skill application contract"):
        validate_represented_skill_tasks(source)


def test_practice_definition_cannot_be_promoted_to_application_target_authority() -> None:
    source = config_copy()
    task(source)["target_contract"]["definition_id"] = "skill_practice:systems_diagnostic_practice"

    with pytest.raises(RepresentedSkillTaskValidationError, match="practice targets cannot become application authority"):
        validate_represented_skill_tasks(source)


def test_task_contract_cannot_embed_actor_skill_state() -> None:
    source = config_copy()
    task(source)["score"] = 82.0

    with pytest.raises(RepresentedSkillTaskValidationError, match="must not contain actor state"):
        validate_represented_skill_tasks(source)


def test_task_definition_cannot_imply_learning_evidence() -> None:
    source = config_copy()
    task(source)["evidence_policy"]["learning_evidence"] = True

    with pytest.raises(RepresentedSkillTaskValidationError, match="must not imply learning evidence"):
        validate_represented_skill_tasks(source)


def test_simulation_safe_task_must_remain_low_risk() -> None:
    source = config_copy()
    task(source)["risk_class"] = "moderate"

    with pytest.raises(RepresentedSkillTaskValidationError, match="must be low risk"):
        validate_represented_skill_tasks(source)

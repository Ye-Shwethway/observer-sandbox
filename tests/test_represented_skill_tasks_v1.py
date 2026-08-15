from __future__ import annotations

import copy

import pytest

from observer_sandbox.represented_skill_tasks import (
    RepresentedSkillTaskValidationError,
    load_represented_skill_tasks,
    represented_skill_task,
    validate_represented_skill_tasks,
)


TECH_TASK_ID = "technology_known_system_fault_diagnostic_sim_v1"
TACTICAL_TASK_ID = "tactical_situation_assessment_sim_v1"
BATCH_TASK_IDS = [
    "tactical_maneuver_planning_sim_v1",
    "survival_field_navigation_sim_v1",
    "survival_field_sustainment_sim_v1",
]
H2H_TASK_ID = "h2h_controlled_striking_spar_v1"
H2H_GRAPPLE_TASK_ID = "h2h_controlled_grapple_spar_v1"


def config_copy():
    return copy.deepcopy(load_represented_skill_tasks())


def task(config, task_id=TECH_TASK_ID):
    return config["tasks"][task_id]


def test_canonical_represented_task_registry_validates() -> None:
    source = validate_represented_skill_tasks()
    assert source["revision"] == "represented-skill-tasks-v1.4"
    assert list(source["tasks"]) == [
        TECH_TASK_ID,
        TACTICAL_TASK_ID,
        *BATCH_TASK_IDS,
        H2H_TASK_ID,
        H2H_GRAPPLE_TASK_ID,
    ]


def test_technology_task_is_exact_definition_bound_and_simulation_safe() -> None:
    value = represented_skill_task(TECH_TASK_ID)
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
    assert value["resource_contract"]["required_resource_mode"] == "any"
    assert value["resource_contract"]["required_capabilities_any"] == ["diagnostic_interface"]
    assert value["evidence_policy"]["learning_evidence"] is False


def test_tactical_task_preserves_no_hard_resource_application_semantics() -> None:
    value = represented_skill_task(TACTICAL_TASK_ID)
    assert value["skill_id"] == "tactical_planning"
    assert value["application_id"] == "assess_tactical_situation"
    assert value["challenge_class"] == "standard"
    assert value["task_mode"] == "simulation_safe"
    assert value["risk_class"] == "low"
    assert value["target_contract"]["definition_id"] == "represented_task:tactical_situation_assessment_simulator_v1"
    assert value["resource_contract"] == {
        "required_resource_mode": "none",
        "required_capabilities_any": [],
        "supporting_capabilities": ["situational_intelligence"],
    }
    assert value["evidence_policy"]["learning_evidence"] is False


def test_batch_tasks_are_simulation_safe_and_preserve_application_resource_modes() -> None:
    maneuver = represented_skill_task(BATCH_TASK_IDS[0])
    navigation = represented_skill_task(BATCH_TASK_IDS[1])
    sustainment = represented_skill_task(BATCH_TASK_IDS[2])
    assert maneuver["skill_id"] == "tactical_planning"
    assert maneuver["application_id"] == "plan_tactical_maneuver"
    assert maneuver["resource_contract"]["required_resource_mode"] == "none"
    assert navigation["skill_id"] == "survival"
    assert navigation["application_id"] == "navigate_field_environment"
    assert navigation["resource_contract"]["required_resource_mode"] == "none"
    assert sustainment["skill_id"] == "survival"
    assert sustainment["application_id"] == "establish_field_sustainment"
    assert sustainment["resource_contract"]["required_resource_mode"] == "any"
    assert sustainment["resource_contract"]["required_capabilities_any"] == ["field_sustainment_materials"]
    for value in (maneuver, navigation, sustainment):
        assert value["task_mode"] == "simulation_safe"
        assert value["risk_class"] == "low"
        assert value["evidence_policy"]["learning_evidence"] is False


def test_controlled_h2h_tasks_are_consequential_and_require_explicit_participant_authorization() -> None:
    striking = represented_skill_task(H2H_TASK_ID)
    grapple = represented_skill_task(H2H_GRAPPLE_TASK_ID)
    assert striking["skill_id"] == grapple["skill_id"] == "hand_to_hand_combat"
    assert striking["application_id"] == "engage_unarmed_striking"
    assert grapple["application_id"] == "control_unarmed_grapple"
    assert striking["task_mode"] == grapple["task_mode"] == "represented_consequential"
    assert striking["risk_class"] == grapple["risk_class"] == "moderate"
    assert striking["resource_contract"]["required_resource_mode"] == "none"
    assert grapple["resource_contract"]["required_resource_mode"] == "none"
    common = {
        "participant_entity_type": "character",
        "participant_count": 1,
        "requires_distinct_actor": True,
        "requires_colocation": True,
        "required_participant_capabilities_all": ["controlled_sparring_consent"],
        "authorization_mode": "explicit_participant_capability",
        "injury_state_mutation": False,
        "target_state_mutation": False,
    }
    for key, expected in common.items():
        assert striking["interaction_contract"][key] == expected
        assert grapple["interaction_contract"][key] == expected
    assert striking["interaction_contract"]["consequence_mode"] == "scored_contact_only"
    assert grapple["interaction_contract"]["consequence_mode"] == "scored_positional_control_only"
    assert striking["evidence_policy"]["learning_evidence"] is False
    assert grapple["evidence_policy"]["learning_evidence"] is False


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


def test_task_resource_mode_must_preserve_application_mode() -> None:
    source = config_copy()
    task(source, TACTICAL_TASK_ID)["resource_contract"]["required_resource_mode"] = "any"
    task(source, TACTICAL_TASK_ID)["resource_contract"]["required_capabilities_any"] = ["situational_intelligence"]
    with pytest.raises(RepresentedSkillTaskValidationError, match="must preserve application mode"):
        validate_represented_skill_tasks(source)


def test_none_resource_mode_cannot_publish_a_hidden_hard_resource() -> None:
    source = config_copy()
    task(source, TACTICAL_TASK_ID)["resource_contract"]["required_capabilities_any"] = ["situational_intelligence"]
    with pytest.raises(RepresentedSkillTaskValidationError, match="must be empty"):
        validate_represented_skill_tasks(source)


def test_any_resource_mode_must_keep_a_nonempty_required_resource_list() -> None:
    source = config_copy()
    task(source)["resource_contract"]["required_capabilities_any"] = []
    with pytest.raises(RepresentedSkillTaskValidationError, match="must not be empty"):
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

from __future__ import annotations

from copy import deepcopy

import pytest

from observer_sandbox.skill_definitions import (
    EXPECTED_ANCHORS,
    SkillDefinitionValidationError,
    get_skill_definition,
    load_validated_skill_definitions,
    validate_skill_definition_config,
)
from observer_sandbox.skill_practice import load_skill_practice_config
from observer_sandbox.skill_progression import load_skill_progression_config


def canonical() -> dict:
    return deepcopy(load_validated_skill_definitions())


def test_canonical_registry_has_only_technology_exemplar_and_valid_semantics() -> None:
    config = canonical()
    assert config["revision"] == "skill-definitions-v1"
    assert set(config["skills"]) == {"technology"}

    technology = get_skill_definition("technology", config=config)
    assert technology["skill_id"] == "technology"
    assert technology["grading_scheme"] == "skill-proficiency-100-v1"
    assert tuple(technology["proficiency_anchors"]) == EXPECTED_ANCHORS
    assert technology["learning_evidence"]["practice_method_ids"] == ["systems_diagnostic_practice"]
    assert technology["provenance"]["compatibility"]["character_skill_key"] == "technology"


def test_technology_learning_evidence_matches_practice_and_progression_catalogs() -> None:
    config = canonical()
    practice = load_skill_practice_config()
    progression = load_skill_progression_config()
    method = practice["methods"]["systems_diagnostic_practice"]

    assert method["skill_relevance"]["technology"] > 0
    assert progression["skills"]["technology"]["eligible_methods"]["systems_diagnostic_practice"] > 0
    validate_skill_definition_config(config, practice_config=practice, progression_config=progression)


def test_definition_cannot_embed_actor_state() -> None:
    config = canonical()
    config["skills"]["technology"]["score"] = 82
    with pytest.raises(SkillDefinitionValidationError, match="actor state"):
        validate_skill_definition_config(config)


def test_definition_requires_explicit_scope_boundaries() -> None:
    config = canonical()
    config["skills"]["technology"]["scope_excludes"] = []
    with pytest.raises(SkillDefinitionValidationError, match="scope_excludes"):
        validate_skill_definition_config(config)


def test_current_scale_rejects_ss_plus_capability_anchors() -> None:
    config = canonical()
    config["skills"]["technology"]["proficiency_anchors"]["SS"] = {
        "summary": "unsupported",
        "independence": "unsupported",
        "supported_challenges": ["extreme"],
        "limits": "unsupported",
    }
    with pytest.raises(SkillDefinitionValidationError, match="SS\+"):
        validate_skill_definition_config(config)


def test_higher_proficiency_cannot_reduce_supported_challenge_range() -> None:
    config = canonical()
    config["skills"]["technology"]["proficiency_anchors"]["A"]["supported_challenges"] = ["routine"]
    with pytest.raises(SkillDefinitionValidationError, match="cannot reduce"):
        validate_skill_definition_config(config)


def test_unknown_practice_method_is_rejected() -> None:
    config = canonical()
    config["skills"]["technology"]["learning_evidence"]["practice_method_ids"] = ["imaginary_method"]
    with pytest.raises(SkillDefinitionValidationError, match="unknown practice method"):
        validate_skill_definition_config(config)


def test_practice_method_must_have_positive_skill_relevance() -> None:
    config = canonical()
    practice = deepcopy(load_skill_practice_config())
    practice["methods"]["systems_diagnostic_practice"]["skill_relevance"]["technology"] = 0.0
    with pytest.raises(SkillDefinitionValidationError, match="no positive 'technology' relevance"):
        validate_skill_definition_config(config, practice_config=practice)


def test_practice_method_must_also_be_whitelisted_by_progression() -> None:
    config = canonical()
    progression = deepcopy(load_skill_progression_config())
    progression["skills"]["technology"]["eligible_methods"].pop("systems_diagnostic_practice")
    with pytest.raises(SkillDefinitionValidationError, match="not whitelisted"):
        validate_skill_definition_config(config, progression_config=progression)


def test_high_risk_application_requires_meaningful_consequence_boundary() -> None:
    config = canonical()
    app = config["skills"]["technology"]["applications"][0]
    app["risk"]["default_class"] = "high"
    app["risk"]["consequence_bounds"] = "too short"
    with pytest.raises(SkillDefinitionValidationError, match="high-risk boundary"):
        validate_skill_definition_config(config)


def test_transfer_rule_cannot_fabricate_skill_state() -> None:
    config = canonical()
    config["skills"]["technology"]["transfer"] = [
        {"skill_id": "future_skill", "auto_create_state": True}
    ]
    with pytest.raises(SkillDefinitionValidationError, match="may not fabricate"):
        validate_skill_definition_config(config)


def test_hierarchy_cycle_is_rejected() -> None:
    config = canonical()
    technology = config["skills"]["technology"]
    child = deepcopy(technology)
    child["skill_id"] = "systems_diagnostics"
    child["name"] = "Systems Diagnostics"
    child["revision"] = "systems-diagnostics-definition-v1"
    child["relations"] = {
        "parent_skill": "technology",
        "component_skills": ["technology"],
        "related_skills": [],
    }
    child["provenance"]["compatibility"]["character_skill_key"] = "systems_diagnostics"
    child["learning_evidence"]["families"] = ["supervised_application"]
    child["learning_evidence"]["practice_method_ids"] = []
    config["skills"]["systems_diagnostics"] = child
    technology["relations"]["component_skills"] = ["systems_diagnostics"]

    with pytest.raises(SkillDefinitionValidationError, match="cycle"):
        validate_skill_definition_config(config)


def test_generic_implicit_learning_policy_must_remain_explicitly_disabled() -> None:
    config = canonical()
    config["skills"]["technology"]["learning_evidence"]["implicit_action_evidence"] = True
    with pytest.raises(SkillDefinitionValidationError, match="must be false"):
        validate_skill_definition_config(config)

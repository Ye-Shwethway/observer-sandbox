from __future__ import annotations

import pytest

from observer_sandbox.skill_capability import (
    SkillCapabilityAssessmentError,
    assess_skill_application,
)


BASE_CONTEXT = {
    "technical_system_represented",
    "diagnostic_evidence_available",
}


def assess(
    *,
    score: float = 82.0,
    challenge: str = "advanced",
    resources: set[str] | None = None,
    attributes: dict[str, float] | None = None,
):
    return assess_skill_application(
        "technology",
        "diagnose_known_system_fault",
        skill_score=score,
        challenge_class=challenge,
        context_tags=BASE_CONTEXT,
        resource_capabilities=resources
        if resources is not None
        else {"diagnostic_interface", "technical_documentation"},
        attribute_values=attributes
        if attributes is not None
        else {
            "raps_ia.problem_solving": 88.0,
            "raps_ma.focus": 92.0,
        },
    )


def test_advanced_technology_actor_is_supported_for_declared_advanced_diagnosis() -> None:
    result = assess()

    assert result.status == "supported"
    assert result.proficiency_grade == "A"
    assert result.proficiency_label == "Advanced"
    assert result.challenge_class == "advanced"
    assert result.missing_context_tags == ()
    assert result.matched_required_resource_capabilities == ("diagnostic_interface",)
    assert result.missing_supporting_resource_capabilities == ()
    assert result.knowledge_mode == "declarative_support_only"
    assert result.knowledge_assessed is False
    assert result.assessment_not_authorization is True
    assert result.reasons == ("declared_capability_requirements_satisfied",)


def test_missing_supporting_documentation_is_constrained_not_unsupported() -> None:
    result = assess(resources={"diagnostic_interface"})

    assert result.status == "constrained"
    assert result.missing_supporting_resource_capabilities == ("technical_documentation",)
    assert result.reasons == ("supporting_resource_capability_missing",)


def test_missing_required_diagnostic_capability_is_unsupported() -> None:
    result = assess(resources={"technical_documentation"})

    assert result.status == "unsupported"
    assert result.matched_required_resource_capabilities == ()
    assert "required_resource_capability_missing" in result.reasons


def test_missing_required_context_is_unsupported() -> None:
    result = assess_skill_application(
        "technology",
        "diagnose_known_system_fault",
        skill_score=82.0,
        challenge_class="standard",
        context_tags={"technical_system_represented"},
        resource_capabilities={"diagnostic_interface", "technical_documentation"},
    )

    assert result.status == "unsupported"
    assert result.missing_context_tags == ("diagnostic_evidence_available",)
    assert "required_context_missing" in result.reasons


def test_proficiency_anchor_limits_challenge_without_scattered_numeric_thresholds() -> None:
    result = assess(score=65.0, challenge="advanced")

    assert result.proficiency_grade == "B"
    assert result.status == "unsupported"
    assert "proficiency_anchor_does_not_support_requested_challenge" in result.reasons


def test_application_scope_limits_extreme_even_for_expert_score() -> None:
    result = assess(score=95.0, challenge="extreme")

    assert result.proficiency_grade == "S"
    assert result.status == "unsupported"
    assert "application_does_not_declare_requested_challenge" in result.reasons
    assert "proficiency_anchor_does_not_support_requested_challenge" in result.reasons


def test_declared_attributes_are_reported_but_do_not_change_v1_status() -> None:
    high = assess(
        attributes={"raps_ia.problem_solving": 99.0, "raps_ma.focus": 99.0}
    )
    low = assess(
        attributes={"raps_ia.problem_solving": 1.0, "raps_ma.focus": 1.0}
    )
    missing = assess(attributes={})

    assert high.status == low.status == missing.status == "supported"
    assert dict(high.attribute_inputs) == {
        "raps_ia.problem_solving": 99.0,
        "raps_ma.focus": 99.0,
    }
    assert dict(low.attribute_inputs) == {
        "raps_ia.problem_solving": 1.0,
        "raps_ma.focus": 1.0,
    }
    assert dict(missing.attribute_inputs) == {
        "raps_ia.problem_solving": None,
        "raps_ma.focus": None,
    }


def test_knowledge_is_exposed_as_declarative_support_without_hidden_gate() -> None:
    result = assess()

    assert result.knowledge_assessed is False
    assert result.supporting_knowledge_keys == (
        "technical_systems_fundamentals",
        "diagnostic_procedures",
        "technical_documentation_interpretation",
    )
    assert result.status == "supported"


def test_unknown_challenge_is_rejected() -> None:
    with pytest.raises(SkillCapabilityAssessmentError, match="unknown challenge"):
        assess(challenge="impossible")


def test_skill_score_still_uses_canonical_zero_to_one_hundred_grading_contract() -> None:
    with pytest.raises(ValueError, match="inclusive range 0..100"):
        assess(score=101.0)

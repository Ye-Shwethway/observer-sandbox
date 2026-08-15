from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping

from .grading import evaluate_skill_score
from .skill_application_requirements import get_executable_skill_application
from .skill_definitions import CHALLENGE_CLASSES


CAPABILITY_STATUSES = {"supported", "constrained", "unsupported"}


class SkillCapabilityAssessmentError(ValueError):
    pass


@dataclass(frozen=True)
class SkillCapabilityAssessment:
    skill_id: str
    application_id: str
    status: str
    skill_score: float
    proficiency_grade: str
    proficiency_label: str
    challenge_class: str
    anchor_summary: str
    anchor_independence: str
    anchor_limits: str
    missing_context_tags: tuple[str, ...]
    matched_required_resource_capabilities: tuple[str, ...]
    missing_supporting_resource_capabilities: tuple[str, ...]
    knowledge_mode: str
    supporting_knowledge_keys: tuple[str, ...]
    knowledge_assessed: bool
    attribute_inputs: tuple[tuple[str, float | None], ...]
    gameplay_effects: tuple[str, ...]
    risk_class: str
    assessment_not_authorization: bool
    reasons: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _semantic_set(values: Iterable[str] | None, *, field: str) -> set[str]:
    if values is None:
        return set()
    result: set[str] = set()
    for value in values:
        if not isinstance(value, str) or not value:
            raise SkillCapabilityAssessmentError(f"{field}: expected non-empty string values")
        result.add(value)
    return result


def _attribute_inputs(
    definition: Mapping[str, Any],
    values: Mapping[str, float | int] | None,
) -> tuple[tuple[str, float | None], ...]:
    supplied = values or {}
    result: list[tuple[str, float | None]] = []
    for dependency in definition.get("ability_dependencies") or []:
        if not isinstance(dependency, Mapping):
            continue
        field_key = dependency.get("field_key")
        if not isinstance(field_key, str):
            continue
        raw = supplied.get(field_key)
        if raw is None:
            result.append((field_key, None))
            continue
        if isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise SkillCapabilityAssessmentError(
                f"attribute_values[{field_key!r}]: expected numeric value"
            )
        result.append((field_key, float(raw)))
    return tuple(result)


def assess_skill_application(
    skill_id: str,
    application_id: str,
    *,
    skill_score: float | int,
    challenge_class: str,
    context_tags: Iterable[str] | None = None,
    resource_capabilities: Iterable[str] | None = None,
    attribute_values: Mapping[str, float | int] | None = None,
    config: dict[str, Any] | None = None,
) -> SkillCapabilityAssessment:
    """Pure deterministic Skill-application capability assessment.

    v1 deliberately does not invent probability, hidden Attribute weighting,
    Knowledge scores, competency scores, XP, or action authorization. It answers
    only whether the declared application is supported by the current Skill
    proficiency anchor and machine-readable task requirements.
    """

    if challenge_class not in CHALLENGE_CLASSES:
        raise SkillCapabilityAssessmentError(
            f"challenge_class: unknown challenge {challenge_class!r}"
        )

    grade = evaluate_skill_score(skill_score)
    definition, application = get_executable_skill_application(
        skill_id,
        application_id,
        config=config,
    )

    anchors = definition.get("proficiency_anchors") or {}
    anchor = anchors.get(grade.grade)
    if not isinstance(anchor, dict):
        raise SkillCapabilityAssessmentError(
            f"{skill_id}: missing proficiency anchor for grade {grade.grade!r}"
        )

    requirements = application["requirements"]
    available_context = _semantic_set(context_tags, field="context_tags")
    available_resources = _semantic_set(
        resource_capabilities,
        field="resource_capabilities",
    )

    required_context = tuple(requirements.get("context_tags_all") or ())
    required_resource_any = tuple(requirements.get("resource_capabilities_any") or ())
    supporting_resources = tuple(
        requirements.get("supporting_resource_capabilities") or ()
    )

    missing_context = tuple(
        value for value in required_context if value not in available_context
    )
    matched_required_resources = tuple(
        value for value in required_resource_any if value in available_resources
    )
    missing_supporting_resources = tuple(
        value for value in supporting_resources if value not in available_resources
    )

    application_challenges = set(application.get("challenge_classes") or ())
    anchor_challenges = set(anchor.get("supported_challenges") or ())

    reasons: list[str] = []
    unsupported = False

    if challenge_class not in application_challenges:
        unsupported = True
        reasons.append("application_does_not_declare_requested_challenge")
    if challenge_class not in anchor_challenges:
        unsupported = True
        reasons.append("proficiency_anchor_does_not_support_requested_challenge")
    if missing_context:
        unsupported = True
        reasons.append("required_context_missing")
    if required_resource_any and not matched_required_resources:
        unsupported = True
        reasons.append("required_resource_capability_missing")

    if unsupported:
        status = "unsupported"
    elif missing_supporting_resources:
        status = "constrained"
        reasons.append("supporting_resource_capability_missing")
    else:
        status = "supported"
        reasons.append("declared_capability_requirements_satisfied")

    knowledge = requirements.get("knowledge") or {}
    knowledge_mode = str(knowledge.get("mode") or "")
    supporting_knowledge_keys = tuple(knowledge.get("supporting_keys") or ())

    risk = application.get("risk") or {}
    risk_class = str(risk.get("default_class") or "")

    return SkillCapabilityAssessment(
        skill_id=skill_id,
        application_id=application_id,
        status=status,
        skill_score=float(skill_score),
        proficiency_grade=grade.grade,
        proficiency_label=grade.label,
        challenge_class=challenge_class,
        anchor_summary=str(anchor.get("summary") or ""),
        anchor_independence=str(anchor.get("independence") or ""),
        anchor_limits=str(anchor.get("limits") or ""),
        missing_context_tags=missing_context,
        matched_required_resource_capabilities=matched_required_resources,
        missing_supporting_resource_capabilities=missing_supporting_resources,
        knowledge_mode=knowledge_mode,
        supporting_knowledge_keys=supporting_knowledge_keys,
        knowledge_assessed=False,
        attribute_inputs=_attribute_inputs(definition, attribute_values),
        gameplay_effects=tuple(application.get("gameplay_effects") or ()),
        risk_class=risk_class,
        assessment_not_authorization=True,
        reasons=tuple(reasons),
    )

from __future__ import annotations

from typing import Any, Mapping

from .grading import GradeProfile, GradeResult, evaluate_location_completeness
from .grading_socket import (
    DimensionSpec,
    EvaluatorSpec,
    GradingSocketRegistry,
    ReferenceProfile,
    UniverseGradingPolicy,
)

LOCATION_GRADING_POLICY_ID = "location-realistic-v2"
LOCATION_COMPLETENESS_EVALUATOR_ID = "location-completeness-v1"
LOCATION_COMPLETENESS_DIMENSION_ID = "completeness"


def _completeness_evaluator(
    evidence: Mapping[str, Any],
    _reference: ReferenceProfile | None,
) -> GradeResult:
    return evaluate_location_completeness(evidence["derived.completeness_level"])


def build_location_grading_registry_v2() -> GradingSocketRegistry:
    registry = GradingSocketRegistry()
    registry.register_evaluator(
        EvaluatorSpec(
            evaluator_id=LOCATION_COMPLETENESS_EVALUATOR_ID,
            family="ordinal",
            domain="location",
            supported_grades=("E", "D", "C", "B", "A"),
        ),
        _completeness_evaluator,
    )
    registry.register_dimension(
        DimensionSpec(
            dimension_id=LOCATION_COMPLETENESS_DIMENSION_ID,
            domain="location",
            label="Completeness",
            evaluator_id=LOCATION_COMPLETENESS_EVALUATOR_ID,
            source_paths=("derived.completeness_level",),
        )
    )
    registry.register_universe_policy(
        UniverseGradingPolicy(
            policy_id=LOCATION_GRADING_POLICY_ID,
            allowed_domains=frozenset({"location"}),
            allowed_dimensions=frozenset({LOCATION_COMPLETENESS_DIMENSION_ID}),
            allowed_evaluators=frozenset({LOCATION_COMPLETENESS_EVALUATOR_ID}),
            allowed_reference_profiles=frozenset(),
            grade_ceiling="S",
        )
    )
    return registry


LOCATION_GRADING_REGISTRY_V2 = build_location_grading_registry_v2()


def location_grade_profile_v2(validated_location: Mapping[str, Any]) -> GradeProfile | None:
    derived = validated_location.get("derived")
    if not isinstance(derived, Mapping) or not derived.get("completeness_level"):
        raise ValueError("Location v2 grading requires validated derived.completeness_level evidence")
    _plan, profile = LOCATION_GRADING_REGISTRY_V2.resolve(
        "location",
        validated_location,
        universe_policy_id=LOCATION_GRADING_POLICY_ID,
    )
    return profile


__all__ = [
    "LOCATION_GRADING_POLICY_ID",
    "LOCATION_GRADING_REGISTRY_V2",
    "build_location_grading_registry_v2",
    "location_grade_profile_v2",
]

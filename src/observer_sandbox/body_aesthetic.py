from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .body_physique_coherence import abdominal_definition, composition_item
from .grading import (
    BODY_AESTHETIC_PROPORTION_SCHEME_ID,
    BODY_CENTRAL_ADIPOSITY_SCHEME_ID,
    BODY_PHYSIQUE_COMPOSITE_SCHEME_ID,
    GRADE_LABELS,
    GradeResult,
    TargetRange,
    evaluate_raps_100,
    evaluate_target_range,
)


@dataclass(frozen=True)
class BodyMetricDefinition:
    metric_key: str
    label: str
    numerator_field: str
    denominator_field: str
    low: float
    high: float
    weight: float
    role: str
    calibration_kind: str
    evidence_note: str
    inverse_enabled: bool = True


@dataclass(frozen=True)
class BodyReferenceProfile:
    profile_id: str
    sex: str
    metrics: tuple[BodyMetricDefinition, ...]


_MALE_METRICS = (
    BodyMetricDefinition(
        "body.waist_to_chest_ratio",
        "Waist / Chest",
        "body.waist_in",
        "body.chest_in",
        0.68,
        0.74,
        0.45,
        "primary_aesthetic",
        "empirical_plus_project",
        "Male waist-to-chest ratio is a strong attractiveness cue; ~0.70 is an empirical anchor while this bounded S-band is project calibration.",
    ),
    BodyMetricDefinition(
        "body.waist_to_shoulders_ratio",
        "Waist / Shoulders",
        "body.waist_in",
        "body.shoulders_in",
        0.55,
        0.65,
        0.35,
        "primary_aesthetic",
        "project_calibration",
        "Existing Observer Sandbox V-taper calibration retained with corrected evidence labeling.",
    ),
    BodyMetricDefinition(
        "body.waist_to_hips_ratio",
        "Waist / Hips",
        "body.waist_in",
        "body.hips_in",
        0.78,
        0.84,
        0.20,
        "primary_aesthetic",
        "empirical_plus_project",
        "Male WHR around 0.80 is an empirical anchor; this bounded S-band is project calibration.",
    ),
)

_FEMALE_METRICS = (
    BodyMetricDefinition(
        "body.waist_to_hips_ratio",
        "Waist / Hips",
        "body.waist_in",
        "body.hips_in",
        0.67,
        0.73,
        1.0,
        "primary_aesthetic",
        "empirical_plus_project",
        "Female WHR around 0.70 is an empirical anchor; this bounded S-band is project calibration and not a universal beauty law.",
    ),
)

REFERENCE_PROFILES: Mapping[str, BodyReferenceProfile] = {
    "male": BodyReferenceProfile("body-aesthetic-male-v2", "male", _MALE_METRICS),
    "female": BodyReferenceProfile("body-aesthetic-female-v2", "female", _FEMALE_METRICS),
}

HEALTH_WAIST_HEIGHT = BodyMetricDefinition(
    "body.waist_to_height_ratio",
    "Waist / Height",
    "body.waist_in",
    "body.height_in",
    0.40,
    0.49,
    0.0,
    "health_context",
    "empirical_anchor",
    "NICE adult central-adiposity guidance classifies 0.40-0.49 as healthy; this is health context, not aesthetic authority.",
    inverse_enabled=False,
)

_GRADE_SCORES = {"E": 10.0, "D": 30.0, "C": 50.0, "B": 67.5, "A": 82.5, "S": 95.0}


def normalize_body_sex(value: object) -> str:
    text = str(value or "").strip().lower()
    if text in {"male", "m", "man", "masculine"}:
        return "male"
    if text in {"female", "f", "woman", "feminine"}:
        return "female"
    raise ValueError(f"Unsupported body aesthetic reference sex: {value!r}")


def reference_profile(sex: object) -> BodyReferenceProfile:
    return REFERENCE_PROFILES[normalize_body_sex(sex)]


def _number(values: Mapping[str, object], key: str) -> float | None:
    value = values.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return None
    numeric = float(value)
    return numeric if numeric > 0.0 else None


def _target(metric: BodyMetricDefinition) -> TargetRange:
    return TargetRange(metric.metric_key, metric.label, metric.low, metric.high, metric.evidence_note)


def evaluate_metric(metric: BodyMetricDefinition, values: Mapping[str, object]) -> dict[str, Any] | None:
    numerator = _number(values, metric.numerator_field)
    denominator = _number(values, metric.denominator_field)
    if numerator is None or denominator is None:
        return None
    ratio = numerator / denominator
    scheme = BODY_CENTRAL_ADIPOSITY_SCHEME_ID if metric.role == "health_context" else BODY_AESTHETIC_PROPORTION_SCHEME_ID
    result = evaluate_target_range(ratio, _target(metric), scheme_id=scheme)
    return {
        "kind": "derived_grade",
        "field_key": metric.metric_key,
        "domain": "body",
        "label": metric.label,
        "value": round(ratio, 3),
        "raw_value": ratio,
        "data_type": "number",
        "unit": "ratio",
        "mode": "derived",
        "role": metric.role,
        "weight": metric.weight,
        "calibration_kind": metric.calibration_kind,
        "reference_range": [metric.low, metric.high],
        "reference_note": metric.evidence_note,
        "grade_result": result,
    }


def _display_context_items(values: Mapping[str, object], sex: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    if sex == "male":
        chest = _number(values, "body.chest_in")
        waist = _number(values, "body.waist_in")
        if chest is not None and waist is not None:
            items.append(
                {
                    "kind": "derived_context",
                    "field_key": "body.chest_to_waist_ratio",
                    "domain": "body",
                    "label": "Chest / Waist",
                    "value": round(chest / waist, 3),
                    "data_type": "number",
                    "unit": "ratio",
                    "mode": "derived",
                    "role": "display_context",
                    "context": "Readable inverse of the grade-driving male Waist / Chest metric.",
                }
            )
    definition = abdominal_definition(values)
    if definition is not None:
        items.append(
            {
                "kind": "derived_context",
                "field_key": "body.abdominal_definition",
                "domain": "body",
                "label": "Visible abdominal definition",
                "value": definition,
                "data_type": "text",
                "unit": None,
                "mode": "derived",
                "role": "display_context",
                "context": "Derived from current body fat relative to the authored sustainable floor; abdominal anatomy is unchanged.",
            }
        )
    return items


def evaluate_body(values: Mapping[str, object], sex: object) -> dict[str, Any]:
    profile = reference_profile(sex)
    gradeable_items: list[dict[str, Any]] = []
    for metric in profile.metrics:
        item = evaluate_metric(metric, values)
        if item is not None:
            gradeable_items.append(item)

    composition = composition_item(values)
    if composition is not None:
        gradeable_items.append(composition)

    health_items: list[dict[str, Any]] = []
    health = evaluate_metric(HEALTH_WAIST_HEIGHT, values)
    if health is not None:
        health_items.append(health)

    available_weight = sum(float(item["weight"]) for item in gradeable_items)
    weighted_score = None
    overall: GradeResult | None = None
    if available_weight > 0.0:
        weighted_score = sum(
            _GRADE_SCORES[str(item["grade_result"].grade)] * float(item["weight"])
            for item in gradeable_items
        ) / available_weight
        base = evaluate_raps_100(weighted_score)
        overall = GradeResult(
            scheme_id=BODY_PHYSIQUE_COMPOSITE_SCHEME_ID,
            grade=base.grade,
            label=GRADE_LABELS[base.grade],
            value=weighted_score,
        )

    display_items = list(gradeable_items) + _display_context_items(values, profile.sex)
    eligible_metrics = len(profile.metrics) + (1 if composition is not None else 0)

    return {
        "reference_profile": profile.profile_id,
        "sex": profile.sex,
        "aesthetic_items": display_items,
        "health_items": health_items,
        "overall_grade": overall,
        "coverage": {
            "active_metrics": len(gradeable_items),
            "eligible_metrics": eligible_metrics,
            "active_weight": round(available_weight, 6),
            "weighted_score": None if weighted_score is None else round(weighted_score, 3),
        },
    }


def inverse_metrics(sex: object) -> tuple[BodyMetricDefinition, ...]:
    return tuple(metric for metric in reference_profile(sex).metrics if metric.inverse_enabled)


__all__ = [
    "BodyMetricDefinition",
    "BodyReferenceProfile",
    "HEALTH_WAIST_HEIGHT",
    "REFERENCE_PROFILES",
    "evaluate_body",
    "evaluate_metric",
    "inverse_metrics",
    "normalize_body_sex",
    "reference_profile",
]

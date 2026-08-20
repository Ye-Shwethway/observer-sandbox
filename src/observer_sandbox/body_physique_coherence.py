from __future__ import annotations

from typing import Any, Mapping

from .grading import BODY_PHYSIQUE_COMPOSITE_SCHEME_ID, GRADE_LABELS, GradeResult
from .physical_presentation import abdominal_definition_from_composition

# Project calibration relative to each character's authored sustainable body-fat floor.
# The grade describes current physique conditioning, not health, worth, or immutable anatomy.
_COMPOSITION_DELTA_BANDS: tuple[tuple[str, float, float | None], ...] = (
    ("S", 0.0, 1.5),
    ("A", 1.5, 4.0),
    ("B", 4.0, 7.0),
    ("C", 7.0, 10.0),
    ("D", 10.0, 14.0),
    ("E", 14.0, None),
)
_GRADE_SCORES = {"E": 10.0, "D": 30.0, "C": 50.0, "B": 67.5, "A": 82.5, "S": 95.0}
_NORMALIZE_DELTA = {"S": 0.75, "A": 2.75, "B": 5.5, "C": 8.5, "D": 12.0, "E": 17.0}


def composition_grade(body_fat_pct: float, sustainable_floor_pct: float) -> GradeResult:
    delta = max(0.0, float(body_fat_pct) - float(sustainable_floor_pct))
    grade = "E"
    for candidate, low, high in _COMPOSITION_DELTA_BANDS:
        if delta >= low and (high is None or delta < high):
            grade = candidate
            break
    return GradeResult(
        scheme_id=BODY_PHYSIQUE_COMPOSITE_SCHEME_ID,
        grade=grade,
        label=GRADE_LABELS[grade],
        value=_GRADE_SCORES[grade],
    )


def composition_item(values: Mapping[str, object], *, weight: float = 0.35) -> dict[str, Any] | None:
    body_fat = values.get("body.body_fat_pct")
    floor = values.get("genetics.body_fat_floor_pct")
    if not isinstance(body_fat, (int, float)) or isinstance(body_fat, bool):
        return None
    if not isinstance(floor, (int, float)) or isinstance(floor, bool):
        return None
    body_fat = float(body_fat)
    floor = float(floor)
    if body_fat <= 0.0 or floor < 0.0 or body_fat >= 100.0:
        return None
    result = composition_grade(body_fat, floor)
    return {
        "kind": "derived_grade",
        "field_key": "body.composition_conditioning",
        "domain": "body",
        "label": "Body composition / conditioning",
        "value": round(body_fat, 2),
        "raw_value": body_fat,
        "data_type": "number",
        "unit": "percent body fat",
        "mode": "derived",
        "role": "body_composition",
        "weight": float(weight),
        "calibration_kind": "project_calibration_relative_to_authored_floor",
        "reference_range": None,
        "reference_note": "Conditioning grade is calibrated relative to the character's authored sustainable body-fat floor.",
        "grade_result": result,
    }


def target_body_fat_pct(
    current_body_fat_pct: float,
    sustainable_floor_pct: float,
    target_grade: str,
    *,
    mode: str,
) -> float:
    grade = str(target_grade).strip().upper()
    if grade not in _NORMALIZE_DELTA:
        raise ValueError(f"Unsupported composition grade: {grade}")
    if mode not in {"preserve_shape", "normalize"}:
        raise ValueError("mode must be preserve_shape or normalize")
    floor = max(0.0, float(sustainable_floor_pct))
    current_delta = max(0.0, float(current_body_fat_pct) - floor)
    if mode == "normalize":
        delta = _NORMALIZE_DELTA[grade]
    else:
        _, low, high = next(item for item in _COMPOSITION_DELTA_BANDS if item[0] == grade)
        epsilon = 0.25
        if high is None:
            delta = max(low + epsilon, min(current_delta, _NORMALIZE_DELTA[grade]))
        elif low <= current_delta < high:
            delta = current_delta
        elif current_delta < low:
            delta = low + epsilon
        else:
            delta = max(low + epsilon, high - epsilon)
    return round(min(55.0, floor + delta), 2)


def preserve_lean_mass_weight_lb(weight_lb: float, old_body_fat_pct: float, new_body_fat_pct: float) -> float:
    old_bf = float(old_body_fat_pct) / 100.0
    new_bf = float(new_body_fat_pct) / 100.0
    if weight_lb <= 0.0 or not (0.0 <= old_bf < 1.0) or not (0.0 <= new_bf < 1.0):
        raise ValueError("Invalid body composition for lean-mass-preserving projection")
    lean_mass = float(weight_lb) * (1.0 - old_bf)
    return round(lean_mass / (1.0 - new_bf), 2)


def abdominal_definition(values: Mapping[str, object]) -> str | None:
    body_fat = values.get("body.body_fat_pct")
    floor = values.get("genetics.body_fat_floor_pct")
    if not isinstance(body_fat, (int, float)) or isinstance(body_fat, bool):
        return None
    if not isinstance(floor, (int, float)) or isinstance(floor, bool):
        return None
    return abdominal_definition_from_composition(float(body_fat), float(floor))


__all__ = [
    "abdominal_definition",
    "composition_grade",
    "composition_item",
    "preserve_lean_mass_weight_lb",
    "target_body_fat_pct",
]

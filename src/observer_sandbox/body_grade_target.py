from __future__ import annotations

import itertools
import json
import math
import sqlite3
from typing import Any

from .body_aesthetic import evaluate_body, inverse_metrics, normalize_body_sex, reference_profile
from .grading import GRADE_LABELS


class BodyGradeTargetError(RuntimeError):
    pass


_GRADE_DISTANCE = {
    "S": 0.0,
    "A": 0.025,
    "B": 0.075,
    "C": 0.15,
    "D": 0.275,
    "E": 0.45,
}


def _profile_value(conn: sqlite3.Connection, character_id: str, field_key: str) -> Any:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (character_id, field_key),
    ).fetchone()
    if row is None:
        return None
    return json.loads(row["value_json"])


def _body_values(conn: sqlite3.Connection, character_id: str) -> dict[str, Any]:
    rows = conn.execute(
        """
        SELECT v.field_key,v.value_json
        FROM character_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.entity_id=? AND d.domain='body'
        """,
        (character_id,),
    ).fetchall()
    return {str(row["field_key"]): json.loads(row["value_json"]) for row in rows}


def _sex(conn: sqlite3.Connection, character_id: str) -> str:
    value = _profile_value(conn, character_id, "identity.sex")
    if value is None:
        raise BodyGradeTargetError("Body grade targeting requires represented identity.sex")
    try:
        return normalize_body_sex(value)
    except ValueError as exc:
        raise BodyGradeTargetError(str(exc)) from exc


def _ratio_candidates(low: float, high: float, grade: str, current: float, *, normalize: bool) -> tuple[float, ...]:
    center = (low + high) / 2.0
    distance = _GRADE_DISTANCE[grade]
    if grade == "S":
        return (center,)
    lower = max(0.01, low - distance * center)
    upper = high + distance * center
    if normalize:
        # Deterministic representative side: use the one closest to the current
        # ratio so Normalize changes scale more than direction.
        return (lower if abs(current - lower) <= abs(current - upper) else upper,)
    return tuple(sorted((lower, upper), key=lambda value: (abs(current - value), value)))


def _grade_payload(result) -> dict[str, Any] | None:
    if result is None:
        return None
    return {
        "scheme_id": result.scheme_id,
        "grade": result.grade,
        "label": result.label,
        "value": round(float(result.value), 3),
    }


def _measurement_objective(old: dict[str, float], new: dict[str, float], soft_fields: set[str]) -> float:
    total = 0.0
    for key, before in old.items():
        after = new.get(key, before)
        if before <= 0:
            continue
        delta = (after - before) / before
        weight = 1.6 if key in soft_fields else 1.0
        total += weight * delta * delta
    return total


def _solve_ratio_vector(
    values: dict[str, Any],
    sex: str,
    target_grade: str,
    mode: str,
) -> tuple[dict[str, float], dict[str, Any]]:
    metrics = inverse_metrics(sex)
    active = []
    for metric in metrics:
        numerator = values.get(metric.numerator_field)
        denominator = values.get(metric.denominator_field)
        if not isinstance(numerator, (int, float)) or isinstance(numerator, bool) or float(numerator) <= 0:
            continue
        if not isinstance(denominator, (int, float)) or isinstance(denominator, bool) or float(denominator) <= 0:
            continue
        current = float(numerator) / float(denominator)
        active.append((metric, current))
    if not active:
        raise BodyGradeTargetError("Body grade targeting has insufficient represented ratio inputs")

    required = 3 if sex == "male" else 1
    if len(active) < required:
        raise BodyGradeTargetError(
            f"Body grade targeting needs at least {required} active aesthetic ratio(s) for {sex}; found {len(active)}"
        )

    option_sets = [
        _ratio_candidates(metric.low, metric.high, target_grade, current, normalize=mode == "normalize")
        for metric, current in active
    ]

    old_measurements: dict[str, float] = {}
    for metric, _ in active:
        for field in (metric.numerator_field, metric.denominator_field):
            raw = values.get(field)
            if isinstance(raw, (int, float)) and not isinstance(raw, bool):
                old_measurements[field] = float(raw)

    # All current minimum metrics share waist as the numerator. Search a small
    # deterministic scale range for the nearest valid raw vector. This lets the
    # solver distribute change across waist and denominators instead of
    # distorting a single circumference.
    waist_key = active[0][0].numerator_field
    if any(metric.numerator_field != waist_key for metric, _ in active):
        raise BodyGradeTargetError("Current Body inverse solver requires a shared numerator metric family")
    current_waist = float(values[waist_key])

    soft_fields = {"body.shoulders_in", "body.hips_in"}
    best: tuple[float, dict[str, float], dict[str, Any]] | None = None
    scale_steps = range(80, 121) if mode == "preserve_shape" else range(90, 111)

    for ratios in itertools.product(*option_sets):
        for step in scale_steps:
            waist = current_waist * (step / 100.0)
            proposed: dict[str, float] = {waist_key: waist}
            valid = True
            for (metric, _), ratio in zip(active, ratios):
                if ratio <= 0:
                    valid = False
                    break
                proposed[metric.denominator_field] = waist / ratio
            if not valid:
                continue

            rounded = {key: round(value, 2) for key, value in proposed.items()}
            candidate_values = dict(values)
            candidate_values.update(rounded)
            evaluation = evaluate_body(candidate_values, sex)
            overall = evaluation.get("overall_grade")
            if overall is None or overall.grade != target_grade:
                continue

            objective = _measurement_objective(old_measurements, rounded, soft_fields)
            # Preserve mode lightly penalizes movement away from each current
            # raw ratio direction. Normalize intentionally does not.
            if mode == "preserve_shape":
                for metric, current_ratio in active:
                    next_ratio = float(rounded[metric.numerator_field]) / float(rounded[metric.denominator_field])
                    objective += 0.25 * ((next_ratio - current_ratio) / max(current_ratio, 1e-9)) ** 2

            tie = tuple((key, rounded[key]) for key in sorted(rounded))
            score = objective
            if best is None or (score, tie) < (best[0], tuple((key, best[1][key]) for key in sorted(best[1]))):
                best = (score, rounded, evaluation)

    if best is None:
        raise BodyGradeTargetError(f"Unable to solve Body Grade {target_grade} with represented measurements")
    return best[1], best[2]


def preview_body_grade_target(
    conn: sqlite3.Connection,
    character_id: str,
    target_grade: str,
    *,
    mode: str = "preserve_shape",
) -> dict[str, Any]:
    grade = str(target_grade or "").strip().upper()
    if grade not in _GRADE_DISTANCE:
        raise BodyGradeTargetError(f"Unsupported Body target grade: {grade}")
    if mode not in {"preserve_shape", "normalize"}:
        raise BodyGradeTargetError("Body target mode must be preserve_shape or normalize")

    sex = _sex(conn, character_id)
    values = _body_values(conn, character_id)
    current_eval = evaluate_body(values, sex)
    current_overall = current_eval.get("overall_grade")
    if current_overall is None:
        raise BodyGradeTargetError("Body grade targeting requires at least one active aesthetic metric")
    if current_overall.grade == grade and mode == "preserve_shape":
        raise BodyGradeTargetError(f"Body already evaluates to Grade {grade}; no Preserve adjustment is needed")

    proposed, projected_eval = _solve_ratio_vector(values, sex, grade, mode)
    projected_overall = projected_eval.get("overall_grade")
    if projected_overall is None or projected_overall.grade != grade:
        raise BodyGradeTargetError("Body inverse proposal failed forward grade verification")

    changes = []
    for field_key, new_value in sorted(proposed.items()):
        old_value = values.get(field_key)
        if not isinstance(old_value, (int, float)) or isinstance(old_value, bool):
            continue
        if math.isclose(float(old_value), float(new_value), abs_tol=1e-9):
            continue
        row = conn.execute(
            "SELECT d.label,d.data_type,d.unit,v.mode,v.authority FROM character_profile_values v "
            "JOIN profile_field_definitions d ON d.field_key=v.field_key "
            "WHERE v.entity_id=? AND v.field_key=?",
            (character_id, field_key),
        ).fetchone()
        if row is None:
            raise BodyGradeTargetError(f"Body solver proposed non-writable field: {field_key}")
        changes.append(
            {
                "store": "profile",
                "field_key": field_key,
                "label": str(row["label"]),
                "data_type": str(row["data_type"]),
                "unit": row["unit"],
                "mode": str(row["mode"]),
                "authority": str(row["authority"]),
                "old_value": float(old_value),
                "new_value": float(new_value),
            }
        )
    if not changes:
        raise BodyGradeTargetError("Body target proposal produced no raw measurement changes")

    def item_payload(item: dict[str, Any]) -> dict[str, Any]:
        result = item.get("grade_result")
        return {
            "field_key": item.get("field_key"),
            "label": item.get("label"),
            "value": item.get("value"),
            "role": item.get("role"),
            "weight": item.get("weight"),
            "reference_range": item.get("reference_range"),
            "calibration_kind": item.get("calibration_kind"),
            "grade": _grade_payload(result),
        }

    profile = reference_profile(sex)
    return {
        "proposal_version": 1,
        "kind": "body_grade_target",
        "character_id": character_id,
        "mutation_class": "canonical_correction",
        "group": "body",
        "target_grade": grade,
        "target_label": GRADE_LABELS[grade],
        "mode": mode,
        "reference_profile": profile.profile_id,
        "sex": sex,
        "old_aggregate": _grade_payload(current_overall),
        "new_aggregate": _grade_payload(projected_overall),
        "old_coverage": current_eval.get("coverage"),
        "new_coverage": projected_eval.get("coverage"),
        "old_metrics": [item_payload(item) for item in current_eval.get("aesthetic_items") or []],
        "new_metrics": [item_payload(item) for item in projected_eval.get("aesthetic_items") or []],
        "health_context": [item_payload(item) for item in projected_eval.get("health_items") or []],
        "hard_anchors": ["body.height_in"],
        "changes": changes,
    }


__all__ = ["BodyGradeTargetError", "preview_body_grade_target"]

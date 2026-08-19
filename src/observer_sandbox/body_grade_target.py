from __future__ import annotations

import itertools
import json
import math
import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Any

from .body_aesthetic import evaluate_body, inverse_metrics, normalize_body_sex, reference_profile
from .grading import GRADE_LABELS


class BodyGradeTargetError(RuntimeError):
    pass


REPO_ROOT = Path(__file__).resolve().parents[2]
PRESERVATION_POLICY_PATH = REPO_ROOT / "config" / "body_shape_preservation.v2.json"

_GRADE_DISTANCE = {
    "S": 0.0,
    "A": 0.025,
    "B": 0.075,
    "C": 0.15,
    "D": 0.275,
    "E": 0.45,
}


@lru_cache(maxsize=1)
def load_body_shape_preservation_policy(path: str | Path = PRESERVATION_POLICY_PATH) -> dict[str, Any]:
    policy = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(policy, dict):
        raise BodyGradeTargetError("Body shape preservation policy must be an object")
    return policy


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


def _positive_number(values: dict[str, Any], key: str) -> float | None:
    raw = values.get(key)
    if not isinstance(raw, (int, float)) or isinstance(raw, bool):
        return None
    value = float(raw)
    return value if value > 0.0 else None


def _weighted_geometric_scale(scales: list[tuple[float, float]]) -> float | None:
    usable = [(scale, weight) for scale, weight in scales if scale > 0.0 and weight > 0.0]
    if not usable:
        return None
    total_weight = sum(weight for _, weight in usable)
    if total_weight <= 0.0:
        return None
    return math.exp(sum(weight * math.log(scale) for scale, weight in usable) / total_weight)


def _project_dependent_measurements(
    values: dict[str, Any],
    primary: dict[str, float],
    policy: dict[str, Any],
) -> tuple[dict[str, float], list[str]]:
    proposed = dict(primary)
    projected_fields: list[str] = []

    for rule in policy.get("dependent_fields") or []:
        if not isinstance(rule, dict):
            continue
        field_key = str(rule.get("field_key") or "")
        old_value = _positive_number(values, field_key)
        if old_value is None or not field_key:
            continue

        scales: list[tuple[float, float]] = []
        for anchor in rule.get("anchors") or []:
            if not isinstance(anchor, dict):
                continue
            anchor_key = str(anchor.get("field_key") or "")
            weight = float(anchor.get("weight") or 0.0)
            old_anchor = _positive_number(values, anchor_key)
            if old_anchor is None:
                continue
            new_anchor = proposed.get(anchor_key, old_anchor)
            if new_anchor <= 0.0:
                continue
            scales.append((float(new_anchor) / old_anchor, weight))

        scale = _weighted_geometric_scale(scales)
        if scale is None:
            continue
        proposed[field_key] = round(old_value * scale, 2)
        projected_fields.append(field_key)

    return proposed, projected_fields


def _measurement_objective(values: dict[str, Any], proposed: dict[str, float], policy: dict[str, Any]) -> float:
    penalties = policy.get("field_change_penalties") or {}
    total = 0.0
    for key, after in proposed.items():
        before = _positive_number(values, key)
        if before is None:
            continue
        delta = (float(after) - before) / before
        weight = float(penalties.get(key, 1.0)) if isinstance(penalties, dict) else 1.0
        total += weight * delta * delta
    return total


def _secondary_ratio_drift(
    values: dict[str, Any],
    proposed: dict[str, float],
    policy: dict[str, Any],
    *,
    mode: str,
) -> float:
    candidate = dict(values)
    candidate.update(proposed)
    total = 0.0
    for rule in policy.get("secondary_ratio_constraints") or []:
        if not isinstance(rule, dict):
            continue
        numerator_key = str(rule.get("numerator_field") or "")
        denominator_key = str(rule.get("denominator_field") or "")
        before_n = _positive_number(values, numerator_key)
        before_d = _positive_number(values, denominator_key)
        after_n = _positive_number(candidate, numerator_key)
        after_d = _positive_number(candidate, denominator_key)
        if None in {before_n, before_d, after_n, after_d}:
            continue
        before_ratio = float(before_n) / float(before_d)
        after_ratio = float(after_n) / float(after_d)
        drift = (after_ratio - before_ratio) / max(before_ratio, 1e-9)
        total += float(rule.get("weight") or 1.0) * drift * drift

    scale_key = "preserve_ratio_penalty_scale" if mode == "preserve_shape" else "normalize_ratio_penalty_scale"
    return total * float(policy.get(scale_key, 1.0))


def _solve_ratio_vector(
    values: dict[str, Any],
    sex: str,
    target_grade: str,
    mode: str,
) -> tuple[dict[str, float], dict[str, Any], list[str]]:
    metrics = inverse_metrics(sex)
    active = []
    for metric in metrics:
        numerator = _positive_number(values, metric.numerator_field)
        denominator = _positive_number(values, metric.denominator_field)
        if numerator is None or denominator is None:
            continue
        active.append((metric, numerator / denominator))
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

    waist_key = active[0][0].numerator_field
    if any(metric.numerator_field != waist_key for metric, _ in active):
        raise BodyGradeTargetError("Current Body inverse solver requires a shared numerator metric family")
    current_waist = float(values[waist_key])

    policy = load_body_shape_preservation_policy()
    best: tuple[float, dict[str, float], dict[str, Any], list[str]] | None = None
    scale_steps = range(80, 121) if mode == "preserve_shape" else range(90, 111)

    for ratios in itertools.product(*option_sets):
        for step in scale_steps:
            waist = current_waist * (step / 100.0)
            primary: dict[str, float] = {waist_key: waist}
            valid = True
            for (metric, _), ratio in zip(active, ratios):
                if ratio <= 0:
                    valid = False
                    break
                primary[metric.denominator_field] = waist / ratio
            if not valid:
                continue

            rounded_primary = {key: round(value, 2) for key, value in primary.items()}
            proposed, projected_fields = _project_dependent_measurements(values, rounded_primary, policy)
            proposed = {key: round(value, 2) for key, value in proposed.items()}

            candidate_values = dict(values)
            candidate_values.update(proposed)
            evaluation = evaluate_body(candidate_values, sex)
            overall = evaluation.get("overall_grade")
            if overall is None or overall.grade != target_grade:
                continue

            objective = _measurement_objective(values, proposed, policy)
            objective += _secondary_ratio_drift(values, proposed, policy, mode=mode)

            if mode == "preserve_shape":
                for metric, current_ratio in active:
                    next_ratio = float(proposed[metric.numerator_field]) / float(proposed[metric.denominator_field])
                    objective += 0.25 * ((next_ratio - current_ratio) / max(current_ratio, 1e-9)) ** 2

            tie = tuple((key, proposed[key]) for key in sorted(proposed))
            if best is None or (objective, tie) < (
                best[0],
                tuple((key, best[1][key]) for key in sorted(best[1])),
            ):
                best = (objective, proposed, evaluation, projected_fields)

    if best is None:
        raise BodyGradeTargetError(f"Unable to solve Body Grade {target_grade} with represented measurements")
    return best[1], best[2], best[3]


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

    proposed, projected_eval, projected_fields = _solve_ratio_vector(values, sex, grade, mode)
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
    policy = load_body_shape_preservation_policy()
    return {
        "proposal_version": 2,
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
        "hard_anchors": list(policy.get("hard_anchors") or ["body.height_in"]),
        "shape_preservation": {
            "revision": policy.get("revision"),
            "projected_fields": sorted(set(projected_fields)),
            "mode": mode,
        },
        "changes": changes,
    }


__all__ = [
    "BodyGradeTargetError",
    "load_body_shape_preservation_policy",
    "preview_body_grade_target",
]

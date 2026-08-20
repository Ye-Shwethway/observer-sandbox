from __future__ import annotations

import json
import math
import sqlite3
from typing import Any

from .body_aesthetic import evaluate_body, reference_profile
from .body_grade_target import (
    BodyGradeTargetError,
    _grade_payload,
    _solve_ratio_vector,
    load_body_shape_preservation_policy,
)
from .body_physique_coherence import (
    abdominal_definition,
    preserve_lean_mass_weight_lb,
    target_body_fat_pct,
)
from .grading import GRADE_LABELS


def _profile_value(conn: sqlite3.Connection, character_id: str, field_key: str) -> Any:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (character_id, field_key),
    ).fetchone()
    return None if row is None else json.loads(row["value_json"])


def _values(conn: sqlite3.Connection, character_id: str) -> dict[str, Any]:
    rows = conn.execute(
        """
        SELECT v.field_key,v.value_json
        FROM character_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.entity_id=? AND d.domain='body'
        """,
        (character_id,),
    ).fetchall()
    result = {str(row["field_key"]): json.loads(row["value_json"]) for row in rows}
    floor = _profile_value(conn, character_id, "genetics.body_fat_floor_pct")
    if floor is not None:
        result["genetics.body_fat_floor_pct"] = floor
    return result


def _sex(conn: sqlite3.Connection, character_id: str) -> Any:
    value = _profile_value(conn, character_id, "identity.sex")
    if value is None:
        raise BodyGradeTargetError("Body grade targeting requires represented identity.sex")
    return value


def solve_body_grade_target(
    values: dict[str, Any],
    sex: Any,
    target_grade: str,
    *,
    mode: str,
) -> tuple[dict[str, float], dict[str, Any], dict[str, Any], list[str], dict[str, Any]]:
    grade = str(target_grade or "").strip().upper()
    if grade not in {"E", "D", "C", "B", "A", "S"}:
        raise BodyGradeTargetError(f"Unsupported Body target grade: {grade}")
    if mode not in {"preserve_shape", "normalize"}:
        raise BodyGradeTargetError("Body target mode must be preserve_shape or normalize")
    body_fat = values.get("body.body_fat_pct")
    floor = values.get("genetics.body_fat_floor_pct")
    weight = values.get("body.weight_lb")
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (body_fat, floor, weight)):
        raise BodyGradeTargetError("Body Grade Target v2 requires body fat, weight, and sustainable body-fat floor")

    old_eval = evaluate_body(values, sex)
    old_overall = old_eval.get("overall_grade")
    if old_overall is None:
        raise BodyGradeTargetError("Body grade targeting requires active physique metrics")
    if old_overall.grade == grade and mode == "preserve_shape":
        raise BodyGradeTargetError(f"Body already evaluates to Grade {grade}; no Preserve adjustment is needed")

    new_bf = target_body_fat_pct(float(body_fat), float(floor), grade, mode=mode)
    new_weight = preserve_lean_mass_weight_lb(float(weight), float(body_fat), new_bf)
    seeded = dict(values)
    seeded["body.body_fat_pct"] = new_bf
    seeded["body.weight_lb"] = new_weight

    proposed, _, projected_fields = _solve_ratio_vector(seeded, str(sex), grade, mode)
    proposed["body.body_fat_pct"] = new_bf
    proposed["body.weight_lb"] = new_weight
    candidate = dict(values)
    candidate.update(proposed)
    projected = evaluate_body(candidate, sex)
    new_overall = projected.get("overall_grade")
    if new_overall is None or new_overall.grade != grade:
        raise BodyGradeTargetError(
            f"Body inverse proposal failed coherent forward verification: requested {grade}, got {getattr(new_overall, 'grade', None)}"
        )
    context = {
        "old_abdominal_definition": abdominal_definition(values),
        "new_abdominal_definition": abdominal_definition(candidate),
        "old_body_fat_pct": round(float(body_fat), 2),
        "new_body_fat_pct": new_bf,
        "lean_mass_preserved_lb": round(float(weight) * (1.0 - float(body_fat) / 100.0), 2),
        "genetic_abdominal_anatomy": "preserved",
    }
    return proposed, old_eval, projected, sorted(set(projected_fields)), context


def preview_body_grade_target(
    conn: sqlite3.Connection,
    character_id: str,
    target_grade: str,
    *,
    mode: str = "preserve_shape",
) -> dict[str, Any]:
    values = _values(conn, character_id)
    sex = _sex(conn, character_id)
    proposed, current_eval, projected_eval, projected_fields, context = solve_body_grade_target(
        values, sex, target_grade, mode=mode
    )
    grade = str(target_grade).strip().upper()
    changes: list[dict[str, Any]] = []
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
        changes.append({
            "store": "profile",
            "field_key": field_key,
            "label": str(row["label"]),
            "data_type": str(row["data_type"]),
            "unit": row["unit"],
            "mode": str(row["mode"]),
            "authority": str(row["authority"]),
            "old_value": float(old_value),
            "new_value": float(new_value),
        })

    definition_row = conn.execute(
        "SELECT d.label,d.data_type,d.unit,v.mode,v.authority,v.value_json FROM character_profile_values v "
        "JOIN profile_field_definitions d ON d.field_key=v.field_key "
        "WHERE v.entity_id=? AND v.field_key='body.abdominal_definition'",
        (character_id,),
    ).fetchone()
    new_definition = context.get("new_abdominal_definition")
    if definition_row is not None and new_definition is not None:
        old_definition = json.loads(definition_row["value_json"])
        if old_definition != new_definition:
            changes.append({
                "store": "profile",
                "field_key": "body.abdominal_definition",
                "label": str(definition_row["label"]),
                "data_type": str(definition_row["data_type"]),
                "unit": definition_row["unit"],
                "mode": str(definition_row["mode"]),
                "authority": str(definition_row["authority"]),
                "old_value": old_definition,
                "new_value": new_definition,
            })
    if not changes:
        raise BodyGradeTargetError("Body target proposal produced no raw physique changes")

    def payload(item: dict[str, Any]) -> dict[str, Any]:
        return {
            "field_key": item.get("field_key"),
            "label": item.get("label"),
            "value": item.get("value"),
            "role": item.get("role"),
            "weight": item.get("weight"),
            "reference_range": item.get("reference_range"),
            "calibration_kind": item.get("calibration_kind"),
            "grade": _grade_payload(item.get("grade_result")),
        }

    old_overall = current_eval["overall_grade"]
    new_overall = projected_eval["overall_grade"]
    policy = load_body_shape_preservation_policy()
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
        "sex": projected_eval.get("sex"),
        "old_aggregate": _grade_payload(old_overall),
        "new_aggregate": _grade_payload(new_overall),
        "old_coverage": current_eval.get("coverage"),
        "new_coverage": projected_eval.get("coverage"),
        "old_metrics": [payload(item) for item in current_eval.get("aesthetic_items") or []],
        "new_metrics": [payload(item) for item in projected_eval.get("aesthetic_items") or []],
        "health_context": [payload(item) for item in projected_eval.get("health_items") or []],
        "hard_anchors": list(policy.get("hard_anchors") or ["body.height_in"]),
        "shape_preservation": {
            "revision": policy.get("revision"),
            "projected_fields": projected_fields,
            "mode": mode,
        },
        "physique_coherence": context,
        "changes": changes,
    }


__all__ = ["preview_body_grade_target", "solve_body_grade_target"]

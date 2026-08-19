from __future__ import annotations

import json
import math
import sqlite3
from typing import Any

from .body_aesthetic import evaluate_body, normalize_body_sex, reference_profile
from .body_grade_target import _solve_ratio_vector, load_body_shape_preservation_policy
from .creator_profile_edit import (
    ATTRIBUTE_RAPS_100_FIELDS,
    GRADE_INTERVALS,
    GRADE_LABELS,
    GROUP_ALIASES,
    RAPS_DOMAINS,
    CreatorProfileEditError,
    _aggregate,
    _target,
)
from .grading import evaluate_raps_100, evaluate_skill_score


def _profile_value(conn: sqlite3.Connection, object_id: str, field_key: str) -> Any:
    row = conn.execute(
        "SELECT value_json FROM creation_sandbox_profile_values WHERE object_id=? AND field_key=?",
        (object_id, field_key),
    ).fetchone()
    return None if row is None else json.loads(row["value_json"])


def _section_items(conn: sqlite3.Connection, object_id: str, group: str) -> list[dict[str, Any]]:
    domain = GROUP_ALIASES.get(group.strip().lower(), group.strip().lower())
    if domain == "skills":
        rows = conn.execute(
            "SELECT skill_key,score FROM creation_sandbox_character_skills WHERE object_id=? AND score IS NOT NULL ORDER BY skill_key",
            (object_id,),
        ).fetchall()
        return [
            {"store": "skill", "field_key": f"skill:{row['skill_key']}", "label": str(row["skill_key"]), "value": float(row["score"])}
            for row in rows
        ]
    domains = RAPS_DOMAINS if domain == "attributes" else {domain}
    if not domains.issubset(RAPS_DOMAINS):
        raise CreatorProfileEditError(f"Unsupported inverse-grade group: {group}")
    rows = conn.execute(
        """
        SELECT v.field_key,v.value_json,d.label,d.domain
        FROM creation_sandbox_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.object_id=? ORDER BY d.rowid
        """,
        (object_id,),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        key = str(row["field_key"])
        value = json.loads(row["value_json"])
        if str(row["domain"]) in domains and key in ATTRIBUTE_RAPS_100_FIELDS and isinstance(value, (int, float)) and not isinstance(value, bool):
            result.append({"store": "profile", "field_key": key, "label": str(row["label"]), "value": float(value)})
    return result


def preview_sandbox_section_grade_target(
    conn: sqlite3.Connection,
    object_id: str,
    group: str,
    target_grade: str,
    *,
    mode: str = "preserve_shape",
) -> dict[str, Any]:
    grade = target_grade.strip().upper()
    if grade not in GRADE_INTERVALS:
        raise CreatorProfileEditError(f"Grade {grade} has no implemented inverse numeric interval in v1")
    if mode not in {"preserve_shape", "normalize"}:
        raise ValueError("mode must be preserve_shape or normalize")
    items = _section_items(conn, object_id, group)
    if not items:
        raise CreatorProfileEditError(f"No inverse-grade-compatible values in group: {group}")
    stores = {item["store"] for item in items}
    if len(stores) != 1:
        raise CreatorProfileEditError("Inverse-grade group must use one compatible grading family")
    store = stores.pop()
    old_values = [float(item["value"]) for item in items]
    target = _target(grade)
    if mode == "normalize":
        proposed = [target] * len(old_values)
    else:
        delta = target - sum(old_values) / len(old_values)
        proposed = [max(0.0, min(100.0, value + delta)) for value in old_values]
        for _ in range(4):
            residual = target - sum(proposed) / len(proposed)
            if abs(residual) <= 1e-9:
                break
            adjustable = [i for i, value in enumerate(proposed) if (residual > 0 and value < 100) or (residual < 0 and value > 0)]
            if not adjustable:
                break
            step = residual * len(proposed) / len(adjustable)
            for i in adjustable:
                proposed[i] = max(0.0, min(100.0, proposed[i] + step))
    aggregate = _aggregate(store, proposed)
    if aggregate["grade"] != grade:
        raise CreatorProfileEditError(f"Unable to produce requested grade {grade}; got {aggregate['grade']}")
    changes: list[dict[str, Any]] = []
    for item, new_value in zip(items, proposed):
        old_eval = evaluate_skill_score(item["value"]) if store == "skill" else evaluate_raps_100(item["value"])
        new_eval = evaluate_skill_score(new_value) if store == "skill" else evaluate_raps_100(new_value)
        changes.append({
            **item,
            "old_value": round(item["value"], 6),
            "new_value": round(new_value, 6),
            "old_grade": {"grade": old_eval.grade, "label": old_eval.label},
            "new_grade": {"grade": new_eval.grade, "label": new_eval.label},
        })
    low, high = GRADE_INTERVALS[grade]
    return {
        "kind": "section_grade_target",
        "character_id": object_id,
        "group": group,
        "target_grade": grade,
        "target_label": GRADE_LABELS[grade],
        "target_interval": [low, 100.0 if grade == "S" else high],
        "mode": mode,
        "old_aggregate": _aggregate(store, old_values),
        "new_aggregate": aggregate,
        "changes": changes,
    }


def preview_sandbox_body_grade_target(
    conn: sqlite3.Connection,
    object_id: str,
    target_grade: str,
    *,
    mode: str = "preserve_shape",
) -> dict[str, Any]:
    grade = str(target_grade or "").strip().upper()
    if grade not in GRADE_LABELS:
        raise CreatorProfileEditError(f"Unsupported Body target grade: {grade}")
    sex_value = _profile_value(conn, object_id, "identity.sex")
    if sex_value is None:
        raise CreatorProfileEditError("Body grade targeting requires represented identity.sex")
    sex = normalize_body_sex(sex_value)
    rows = conn.execute(
        """
        SELECT v.field_key,v.value_json FROM creation_sandbox_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.object_id=? AND d.domain='body'
        """,
        (object_id,),
    ).fetchall()
    values = {str(row["field_key"]): json.loads(row["value_json"]) for row in rows}
    current_eval = evaluate_body(values, sex)
    current_overall = current_eval.get("overall_grade")
    if current_overall is None:
        raise CreatorProfileEditError("Body grade targeting requires at least one active aesthetic metric")
    if current_overall.grade == grade and mode == "preserve_shape":
        raise CreatorProfileEditError(f"Body already evaluates to Grade {grade}; no Preserve adjustment is needed")
    proposed, projected_eval, projected_fields = _solve_ratio_vector(values, sex, grade, mode)
    projected_overall = projected_eval.get("overall_grade")
    if projected_overall is None or projected_overall.grade != grade:
        raise CreatorProfileEditError("Body inverse proposal failed forward grade verification")
    changes: list[dict[str, Any]] = []
    for field_key, new_value in sorted(proposed.items()):
        old_value = values.get(field_key)
        if not isinstance(old_value, (int, float)) or isinstance(old_value, bool) or math.isclose(float(old_value), float(new_value), abs_tol=1e-9):
            continue
        row = conn.execute(
            "SELECT d.label,d.data_type,d.unit,v.mode,v.authority FROM creation_sandbox_profile_values v JOIN profile_field_definitions d ON d.field_key=v.field_key WHERE v.object_id=? AND v.field_key=?",
            (object_id, field_key),
        ).fetchone()
        if row is None:
            raise CreatorProfileEditError(f"Body solver proposed non-writable field: {field_key}")
        changes.append({
            "store": "profile", "field_key": field_key, "label": str(row["label"]), "data_type": str(row["data_type"]),
            "unit": row["unit"], "mode": str(row["mode"]), "authority": str(row["authority"]),
            "old_value": float(old_value), "new_value": float(new_value),
        })
    if not changes:
        raise CreatorProfileEditError("Body target proposal produced no raw measurement changes")
    profile = reference_profile(sex)
    policy = load_body_shape_preservation_policy()
    def metric_payload(item: dict[str, Any]) -> dict[str, Any]:
        result = item.get("grade_result")
        grade_payload = None if result is None else {"grade": result.grade, "label": result.label, "value": round(float(result.value), 3)}
        return {"field_key": item.get("field_key"), "label": item.get("label"), "value": item.get("value"), "grade": grade_payload}
    return {
        "kind": "body_grade_target", "character_id": object_id, "group": "body", "target_grade": grade,
        "target_label": GRADE_LABELS[grade], "mode": mode, "reference_profile": profile.profile_id, "sex": sex,
        "old_aggregate": {"grade": current_overall.grade, "value": round(float(current_overall.value), 3)},
        "new_aggregate": {"grade": projected_overall.grade, "value": round(float(projected_overall.value), 3)},
        "new_coverage": projected_eval.get("coverage"),
        "new_metrics": [metric_payload(item) for item in projected_eval.get("aesthetic_items") or []],
        "health_context": [metric_payload(item) for item in projected_eval.get("health_items") or []],
        "projected_fields": projected_fields,
        "preservation_policy": policy.get("revision"),
        "changes": changes,
    }


__all__ = ["preview_sandbox_section_grade_target", "preview_sandbox_body_grade_target"]

from __future__ import annotations

import json
import math
import sqlite3
from typing import Any

from .body_grade_target import BodyGradeTargetError, load_body_shape_preservation_policy
from .body_grade_target_v2 import solve_body_grade_target
from .creator_profile_edit import CreatorProfileEditError
from .grading import GRADE_LABELS


def _profile_value(conn: sqlite3.Connection, object_id: str, field_key: str) -> Any:
    row = conn.execute(
        "SELECT value_json FROM creation_sandbox_profile_values WHERE object_id=? AND field_key=?",
        (object_id, field_key),
    ).fetchone()
    return None if row is None else json.loads(row["value_json"])


def preview_sandbox_body_grade_target(
    conn: sqlite3.Connection,
    object_id: str,
    target_grade: str,
    *,
    mode: str = "preserve_shape",
) -> dict[str, Any]:
    sex = _profile_value(conn, object_id, "identity.sex")
    if sex is None:
        raise CreatorProfileEditError("Body grade targeting requires represented identity.sex")
    rows = conn.execute(
        """
        SELECT v.field_key,v.value_json
        FROM creation_sandbox_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.object_id=? AND d.domain='body'
        """,
        (object_id,),
    ).fetchall()
    values = {str(row["field_key"]): json.loads(row["value_json"]) for row in rows}
    floor = _profile_value(conn, object_id, "genetics.body_fat_floor_pct")
    if floor is not None:
        values["genetics.body_fat_floor_pct"] = floor
    try:
        proposed, old_eval, new_eval, projected_fields, context = solve_body_grade_target(
            values, sex, target_grade, mode=mode
        )
    except (BodyGradeTargetError, ValueError) as exc:
        raise CreatorProfileEditError(str(exc)) from exc

    changes: list[dict[str, Any]] = []
    for field_key, new_value in sorted(proposed.items()):
        old_value = values.get(field_key)
        if not isinstance(old_value, (int, float)) or isinstance(old_value, bool):
            continue
        if math.isclose(float(old_value), float(new_value), abs_tol=1e-9):
            continue
        row = conn.execute(
            "SELECT d.label,d.data_type,d.unit,v.mode,v.authority FROM creation_sandbox_profile_values v "
            "JOIN profile_field_definitions d ON d.field_key=v.field_key "
            "WHERE v.object_id=? AND v.field_key=?",
            (object_id, field_key),
        ).fetchone()
        if row is None:
            raise CreatorProfileEditError(f"Body solver proposed non-writable field: {field_key}")
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
        "SELECT d.label,d.data_type,d.unit,v.mode,v.authority,v.value_json FROM creation_sandbox_profile_values v "
        "JOIN profile_field_definitions d ON d.field_key=v.field_key "
        "WHERE v.object_id=? AND v.field_key='body.abdominal_definition'",
        (object_id,),
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
                "mode": "derived",
                "authority": "appearance_engine",
                "old_value": old_definition,
                "new_value": new_definition,
            })
    if not changes:
        raise CreatorProfileEditError("Body target proposal produced no raw physique changes")

    def metric_payload(item: dict[str, Any]) -> dict[str, Any]:
        result = item.get("grade_result")
        grade = None if result is None else {
            "grade": result.grade,
            "label": result.label,
            "value": round(float(result.value), 3),
        }
        return {
            "field_key": item.get("field_key"),
            "label": item.get("label"),
            "value": item.get("value"),
            "role": item.get("role"),
            "grade": grade,
        }

    old_overall = old_eval.get("overall_grade")
    new_overall = new_eval.get("overall_grade")
    policy = load_body_shape_preservation_policy()
    grade = str(target_grade).strip().upper()
    return {
        "kind": "body_grade_target",
        "character_id": object_id,
        "group": "body",
        "target_grade": grade,
        "target_label": GRADE_LABELS[grade],
        "mode": mode,
        "reference_profile": new_eval.get("reference_profile"),
        "sex": new_eval.get("sex"),
        "old_aggregate": {"grade": old_overall.grade, "value": round(float(old_overall.value), 3)},
        "new_aggregate": {"grade": new_overall.grade, "value": round(float(new_overall.value), 3)},
        "new_coverage": new_eval.get("coverage"),
        "new_metrics": [metric_payload(item) for item in new_eval.get("aesthetic_items") or []],
        "health_context": [metric_payload(item) for item in new_eval.get("health_items") or []],
        "projected_fields": projected_fields,
        "preservation_policy": policy.get("revision"),
        "physique_coherence": context,
        "changes": changes,
    }


__all__ = ["preview_sandbox_body_grade_target"]

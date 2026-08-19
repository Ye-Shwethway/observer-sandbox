from __future__ import annotations

import json
import sqlite3
from typing import Any

from .body_aesthetic import evaluate_body
from .creation_sandbox import get_sandbox_object
from .grading import GradeResult, evaluate_profile_field, evaluate_skill_score
from .profile_observer import (
    _allowed_sensitivities,
    _attribute_grade_summaries,
    _grade_payload,
    _section_by_id,
    _sections,
    _skill_grade_summary,
    _visible_to_role,
)
from .skill_hierarchy import hierarchy_profile_metadata


def _character(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    value = get_sandbox_object(conn, object_id)
    if value["creation_type"] != "character" or value["lifecycle_status"] != "active":
        raise KeyError(f"Unknown active sandbox Character: {object_id}")
    return {
        "id": value["object_id"],
        "name": str(value["identity"].get("name") or value["object_id"]),
        "profile_schema_version": "shared-profile-registry",
        "canonical_revision": None,
        "profile_status": "sandbox",
    }


def sandbox_profile_menu(
    conn: sqlite3.Connection,
    object_id: str,
    *,
    role: str = "allowed",
) -> dict[str, Any]:
    character = _character(conn, object_id)
    available: list[dict[str, Any]] = []
    for section in _sections():
        if not _visible_to_role(section, role):
            continue
        if _section_has_data(conn, object_id, section, role=role):
            available.append(
                {
                    "id": section["id"],
                    "label": section["label"],
                    "icon": section["icon"],
                    "renderer": section["renderer"],
                }
            )
    return {"character": character, "sections": available}


def _section_has_data(
    conn: sqlite3.Connection,
    object_id: str,
    section: dict[str, Any],
    *,
    role: str,
) -> bool:
    sensitivities = _allowed_sensitivities(section, role)
    if not sensitivities:
        return False

    collection = section.get("collection")
    if collection == "skills":
        return conn.execute(
            "SELECT 1 FROM creation_sandbox_character_skills WHERE object_id=? LIMIT 1",
            (object_id,),
        ).fetchone() is not None
    if collection == "preferences":
        return any(
            conn.execute(
                f"SELECT 1 FROM {table} WHERE object_id=? LIMIT 1", (object_id,)
            ).fetchone()
            is not None
            for table in (
                "creation_sandbox_character_preferences",
                "creation_sandbox_character_hobbies",
                "creation_sandbox_character_habits",
            )
        )

    domains = tuple(section.get("domains") or ())
    if not domains:
        # Sandbox profile browsing never fabricates Real World runtime/default data.
        return False
    domain_placeholders = ",".join("?" for _ in domains)
    sensitivity_placeholders = ",".join("?" for _ in sensitivities)
    return (
        conn.execute(
            f"""
            SELECT 1
            FROM creation_sandbox_profile_values v
            JOIN profile_field_definitions d ON d.field_key=v.field_key
            WHERE v.object_id=? AND d.domain IN ({domain_placeholders})
              AND d.sensitivity IN ({sensitivity_placeholders})
            LIMIT 1
            """,
            (object_id, *domains, *sensitivities),
        ).fetchone()
        is not None
    )


def sandbox_profile_section(
    conn: sqlite3.Connection,
    object_id: str,
    section_id: str,
    *,
    role: str = "allowed",
) -> dict[str, Any]:
    character = _character(conn, object_id)
    section = _section_by_id(section_id)
    if section is None:
        raise KeyError(f"Unknown profile section: {section_id}")
    if not _visible_to_role(section, role):
        raise PermissionError(
            f"Profile section requires {section['visibility']} visibility: {section_id}"
        )

    sensitivities = _allowed_sensitivities(section, role)
    collection = section.get("collection")
    body_evaluation: dict[str, Any] | None = None
    if collection == "skills":
        content = _skills(conn, object_id)
    elif collection == "preferences":
        content = _preferences(conn, object_id)
    else:
        content = _profile_values(
            conn,
            object_id,
            tuple(section.get("domains") or ()),
            sensitivities=sensitivities,
        )
        if "body" in tuple(section.get("domains") or ()):
            body_values = {
                str(item["field_key"]): item.get("value")
                for item in content
                if item.get("kind") == "field" and item.get("domain") == "body"
            }
            sex_row = conn.execute(
                "SELECT value_json FROM creation_sandbox_profile_values WHERE object_id=? AND field_key='identity.sex'",
                (object_id,),
            ).fetchone()
            if sex_row is not None:
                body_evaluation = evaluate_body(
                    body_values, json.loads(sex_row["value_json"])
                )
                body_items = list(body_evaluation.get("aesthetic_items") or []) + list(
                    body_evaluation.get("health_items") or []
                )
                for item in body_items:
                    result = item.pop("grade_result", None)
                    item.pop("raw_value", None)
                    if isinstance(result, GradeResult):
                        item["grade"] = _grade_payload(result)
                content.extend(body_items)

    section_result: dict[str, Any] = {
        "id": section["id"],
        "label": section["label"],
        "icon": section["icon"],
        "renderer": section["renderer"],
    }
    if section.get("renderer") == "grouped_attributes":
        overall, groups = _attribute_grade_summaries(content)
        section_result["overall_grade"] = overall
        section_result["group_grades"] = groups
    elif collection == "skills":
        section_result["overall_grade"] = _skill_grade_summary(content)
    elif body_evaluation is not None:
        section_result["overall_grade"] = _grade_payload(
            body_evaluation.get("overall_grade")
        )
        section_result["body_reference_profile"] = body_evaluation.get(
            "reference_profile"
        )
        section_result["body_grade_coverage"] = body_evaluation.get("coverage")

    return {"character": character, "section": section_result, "content": content}


def _profile_values(
    conn: sqlite3.Connection,
    object_id: str,
    domains: tuple[str, ...],
    *,
    sensitivities: tuple[str, ...],
) -> list[dict[str, Any]]:
    if not domains or not sensitivities:
        return []
    domain_placeholders = ",".join("?" for _ in domains)
    sensitivity_placeholders = ",".join("?" for _ in sensitivities)
    rows = conn.execute(
        f"""
        SELECT v.field_key,v.value_json,v.mode,d.domain,d.label,d.data_type,d.unit
        FROM creation_sandbox_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.object_id=? AND d.domain IN ({domain_placeholders})
          AND d.sensitivity IN ({sensitivity_placeholders})
        ORDER BY CASE d.domain
            {''.join(f' WHEN ? THEN {index}' for index, _ in enumerate(domains))}
            ELSE 999 END,
            d.rowid
        """,
        (object_id, *domains, *sensitivities, *domains),
    ).fetchall()
    content: list[dict[str, Any]] = []
    for row in rows:
        value = json.loads(row["value_json"])
        item: dict[str, Any] = {
            "kind": "field",
            "field_key": row["field_key"],
            "domain": row["domain"],
            "label": row["label"],
            "value": value,
            "data_type": row["data_type"],
            "unit": row["unit"],
            "mode": row["mode"],
        }
        result = evaluate_profile_field(str(row["field_key"]), value)
        if result is not None:
            item["grade"] = _grade_payload(result)
        content.append(item)
    return content


def _skills(conn: sqlite3.Connection, object_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT skill_key,category,score,tier,experience,metadata_json
        FROM creation_sandbox_character_skills
        WHERE object_id=?
        ORDER BY COALESCE(category, ''),skill_key
        """,
        (object_id,),
    ).fetchall()
    content: list[dict[str, Any]] = []
    for row in rows:
        try:
            raw_metadata = json.loads(row["metadata_json"] or "{}")
        except (TypeError, json.JSONDecodeError):
            raw_metadata = {}
        metadata = hierarchy_profile_metadata(
            raw_metadata if isinstance(raw_metadata, dict) else {}
        )
        if metadata["profile_hidden"]:
            continue
        item: dict[str, Any] = {
            "kind": "skill",
            "key": row["skill_key"],
            "label": metadata["display_name"]
            or str(row["skill_key"]).replace("_", " ").title(),
            "category": row["category"],
            "score": row["score"],
            "tier": row["tier"],
            "experience": row["experience"],
            "hierarchy_role": metadata["hierarchy_role"],
            "parent_skill": metadata["parent_skill"],
            "component_skills": metadata["component_skills"],
            "derived": metadata["derived"],
            "mode": "derived" if metadata["derived"] else "learned",
            "aggregate_exclude": metadata["aggregate_exclude"],
            "profile_order": metadata["profile_order"],
        }
        if isinstance(row["score"], (int, float)):
            item["grade"] = _grade_payload(evaluate_skill_score(row["score"]))
        content.append(item)
    return sorted(
        content,
        key=lambda item: (
            str(item.get("category") or ""),
            int(item.get("profile_order") or 999),
            str(item.get("key") or ""),
        ),
    )


def _preferences(conn: sqlite3.Connection, object_id: str) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = []
    rows = conn.execute(
        "SELECT preference_type,subject,intensity FROM creation_sandbox_character_preferences WHERE object_id=? ORDER BY preference_type,subject",
        (object_id,),
    ).fetchall()
    for row in rows:
        content.append(
            {
                "kind": "preference",
                "preference_type": row["preference_type"],
                "subject": row["subject"],
                "intensity": row["intensity"],
            }
        )
    rows = conn.execute(
        "SELECT name,proficiency,frequency,enjoyment FROM creation_sandbox_character_hobbies WHERE object_id=? ORDER BY name",
        (object_id,),
    ).fetchall()
    for row in rows:
        content.append(
            {
                "kind": "hobby",
                "name": row["name"],
                "proficiency": row["proficiency"],
                "frequency": row["frequency"],
                "enjoyment": row["enjoyment"],
            }
        )
    rows = conn.execute(
        "SELECT name,description,frequency,strength FROM creation_sandbox_character_habits WHERE object_id=? ORDER BY name",
        (object_id,),
    ).fetchall()
    for row in rows:
        content.append(
            {
                "kind": "habit",
                "name": row["name"],
                "description": row["description"],
                "frequency": row["frequency"],
                "strength": row["strength"],
            }
        )
    return content


__all__ = ["sandbox_profile_menu", "sandbox_profile_section"]

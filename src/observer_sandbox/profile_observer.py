from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

from .grading import GradeResult, aggregate_raps_100, evaluate_attribute_field
from .simulation import snapshot
from .strength_progression_observer import strength_progression_profile_items
from .training_modifiers import training_readiness_modifier


_DEFAULT_SECTION_CONFIG = Path(__file__).resolve().parents[2] / "config" / "profile_sections.v1.json"
_RUNTIME_DEFAULTS: dict[str, Any] = {"physiology.fatigue": 0.0}


def _section_config_path() -> Path:
    configured = os.environ.get("OBSERVER_PROFILE_SECTIONS_PATH", "").strip()
    return Path(configured) if configured else _DEFAULT_SECTION_CONFIG


def _sections() -> tuple[dict[str, Any], ...]:
    payload = json.loads(_section_config_path().read_text(encoding="utf-8"))
    sections = payload.get("sections") or []
    if not isinstance(sections, list):
        raise ValueError("profile section config requires a sections list")
    normalized: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in sections:
        if not isinstance(raw, dict):
            raise ValueError("profile section entries must be objects")
        section_id = str(raw.get("id") or "").strip()
        if not section_id or section_id in seen:
            raise ValueError("profile section ids must be unique and non-empty")
        seen.add(section_id)
        section = dict(raw)
        section["id"] = section_id
        section["label"] = str(raw.get("label") or section_id.replace("_", " ").title())
        section["icon"] = str(raw.get("icon") or "•")
        section["order"] = int(raw.get("order", 999))
        section["visibility"] = str(raw.get("visibility") or "authorized")
        section["renderer"] = str(raw.get("renderer") or "fields")
        section["domains"] = tuple(str(value) for value in (raw.get("domains") or ()))
        section["runtime_fields"] = tuple(str(value) for value in (raw.get("runtime_fields") or ()))
        section["sensitivities"] = tuple(str(value) for value in (raw.get("sensitivities") or ("normal",)))
        normalized.append(section)
    return tuple(sorted(normalized, key=lambda item: (item["order"], item["id"])))


def _section_by_id(section_id: str) -> dict[str, Any] | None:
    return next((section for section in _sections() if section["id"] == section_id), None)


def _visible_to_role(section: dict[str, Any], role: str) -> bool:
    visibility = str(section.get("visibility") or "authorized")
    if visibility == "owner":
        return role == "owner"
    return role in {"owner", "allowed", "authorized"}


def _allowed_sensitivities(section: dict[str, Any], role: str) -> tuple[str, ...]:
    configured = tuple(section.get("sensitivities") or ("normal",))
    if role != "owner":
        return tuple(value for value in configured if value == "normal")
    return configured


def _character(conn: sqlite3.Connection, character_id: str) -> dict[str, Any]:
    row = conn.execute(
        "SELECT id, name FROM entities WHERE id=? AND entity_type='character'",
        (character_id,),
    ).fetchone()
    if row is None:
        raise KeyError(f"Unknown character: {character_id}")
    profile = conn.execute(
        "SELECT profile_schema_version, canonical_revision, status FROM character_profiles WHERE entity_id=?",
        (character_id,),
    ).fetchone()
    if profile is None:
        raise KeyError(f"Character has no profile: {character_id}")
    return {
        "id": row["id"],
        "name": row["name"],
        "profile_schema_version": profile["profile_schema_version"],
        "canonical_revision": profile["canonical_revision"],
        "profile_status": profile["status"],
    }


def profile_menu(conn: sqlite3.Connection, character_id: str, *, role: str = "allowed") -> dict[str, Any]:
    character = _character(conn, character_id)
    available: list[dict[str, Any]] = []
    for section in _sections():
        if not _visible_to_role(section, role):
            continue
        if _section_has_data(conn, character_id, section, role=role):
            available.append(
                {
                    "id": section["id"],
                    "label": section["label"],
                    "icon": section["icon"],
                    "renderer": section["renderer"],
                }
            )
    return {"character": character, "sections": available}


def _section_has_data(conn: sqlite3.Connection, character_id: str, section: dict[str, Any], *, role: str) -> bool:
    sensitivities = _allowed_sensitivities(section, role)
    if not sensitivities:
        return False

    collection = section.get("collection")
    if collection == "skills":
        return conn.execute("SELECT 1 FROM character_skills WHERE entity_id=? LIMIT 1", (character_id,)).fetchone() is not None
    if collection == "preferences":
        return any(
            conn.execute(f"SELECT 1 FROM {table} WHERE entity_id=? LIMIT 1", (character_id,)).fetchone() is not None
            for table in ("character_preferences", "character_hobbies", "character_habits")
        )

    placeholders = ",".join("?" for _ in sensitivities)
    domains = tuple(section.get("domains") or ())
    if domains:
        domain_placeholders = ",".join("?" for _ in domains)
        row = conn.execute(
            f"""
            SELECT 1
            FROM character_profile_values v
            JOIN profile_field_definitions d ON d.field_key=v.field_key
            WHERE v.entity_id=? AND d.domain IN ({domain_placeholders})
              AND d.sensitivity IN ({placeholders})
            LIMIT 1
            """,
            (character_id, *domains, *sensitivities),
        ).fetchone()
        if row is not None:
            return True

    runtime_fields = tuple(section.get("runtime_fields") or ())
    if runtime_fields:
        field_placeholders = ",".join("?" for _ in runtime_fields)
        row = conn.execute(
            f"""
            SELECT 1 FROM profile_field_definitions
            WHERE field_key IN ({field_placeholders}) AND sensitivity IN ({placeholders})
            LIMIT 1
            """,
            (*runtime_fields, *sensitivities),
        ).fetchone()
        if row is not None:
            return True
    return False


def profile_section(conn: sqlite3.Connection, character_id: str, section_id: str, *, role: str = "allowed") -> dict[str, Any]:
    character = _character(conn, character_id)
    section = _section_by_id(section_id)
    if section is None:
        raise KeyError(f"Unknown profile section: {section_id}")
    if not _visible_to_role(section, role):
        raise PermissionError(f"Profile section requires {section['visibility']} visibility: {section_id}")

    sensitivities = _allowed_sensitivities(section, role)
    collection = section.get("collection")
    if collection == "skills":
        content = _skills(conn, character_id)
    elif collection == "preferences":
        content = _preferences(conn, character_id)
    else:
        content = _profile_values(
            conn,
            character_id,
            tuple(section.get("domains") or ()),
            sensitivities=sensitivities,
        )
        content.extend(
            _runtime_values(
                conn,
                character_id,
                tuple(section.get("runtime_fields") or ()),
                sensitivities=sensitivities,
                include_recovery=section.get("renderer") == "recovery",
            )
        )
        seen: set[str] = set()
        content = [item for item in content if not (str(item.get("field_key") or "") in seen or seen.add(str(item.get("field_key") or "")))]

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

    return {"character": character, "section": section_result, "content": content}


def _runtime_values(
    conn: sqlite3.Connection,
    character_id: str,
    field_keys: tuple[str, ...],
    *,
    sensitivities: tuple[str, ...],
    include_recovery: bool = False,
) -> list[dict[str, Any]]:
    if not field_keys or not sensitivities:
        return []
    content: list[dict[str, Any]] = []
    placeholders = ",".join("?" for _ in sensitivities)
    for field_key in field_keys:
        definition = conn.execute(
            f"SELECT domain,label,data_type,unit,sensitivity FROM profile_field_definitions WHERE field_key=? AND sensitivity IN ({placeholders})",
            (field_key, *sensitivities),
        ).fetchone()
        if definition is None:
            continue
        row = conn.execute(
            "SELECT value_json,mode FROM fields WHERE entity_id=? AND field_key=?",
            (character_id, field_key),
        ).fetchone()
        value = json.loads(row["value_json"]) if row is not None else _RUNTIME_DEFAULTS.get(field_key)
        if value is None:
            continue
        content.append(
            {
                "kind": "field",
                "field_key": field_key,
                "domain": definition["domain"],
                "label": definition["label"],
                "value": value,
                "data_type": definition["data_type"],
                "unit": definition["unit"],
                "mode": row["mode"] if row is not None else "simulated",
            }
        )

    if include_recovery and "physiology.fatigue" in field_keys:
        state = snapshot(conn, character_id)
        modifier = training_readiness_modifier(state)
        content.append(
            {
                "kind": "derived",
                "field_key": "training.readiness",
                "domain": "physiology",
                "label": "Training readiness",
                "value": round(float(modifier["readiness"]) * 100.0, 1),
                "data_type": "number",
                "unit": "percent",
                "mode": "derived",
            }
        )
        content.extend(strength_progression_profile_items(conn, character_id, state=state))
    return content


def _profile_values(
    conn: sqlite3.Connection,
    character_id: str,
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
        SELECT v.field_key, v.value_json, v.mode, d.domain, d.label, d.data_type, d.unit
        FROM character_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.entity_id=? AND d.domain IN ({domain_placeholders})
          AND d.sensitivity IN ({sensitivity_placeholders})
        ORDER BY CASE d.domain
            {''.join(f' WHEN ? THEN {index}' for index, _ in enumerate(domains))}
            ELSE 999 END,
            d.rowid
        """,
        (character_id, *domains, *sensitivities, *domains),
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
        result = evaluate_attribute_field(str(row["field_key"]), value)
        if result is not None:
            item["grade"] = _grade_payload(result)
        content.append(item)
    return content


def _grade_payload(result: GradeResult | None) -> dict[str, Any] | None:
    if result is None:
        return None
    return {
        "scheme_id": result.scheme_id,
        "grade": result.grade,
        "label": result.label,
        "value": round(float(result.value), 3),
    }


def _attribute_grade_summaries(content: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, dict[str, dict[str, Any]]]:
    by_domain: dict[str, list[GradeResult]] = {}
    all_results: list[GradeResult] = []
    for item in content:
        grade = item.get("grade") or {}
        if not grade.get("grade") or grade.get("scheme_id") is None:
            continue
        result = GradeResult(
            scheme_id=str(grade["scheme_id"]),
            grade=str(grade["grade"]),
            label=str(grade["label"]),
            value=float(grade["value"]),
        )
        by_domain.setdefault(str(item.get("domain") or ""), []).append(result)
        all_results.append(result)
    groups: dict[str, dict[str, Any]] = {}
    for domain, results in by_domain.items():
        payload = _grade_payload(aggregate_raps_100(results))
        if payload is not None:
            groups[domain] = payload
    return _grade_payload(aggregate_raps_100(all_results)), groups


def _skills(conn: sqlite3.Connection, character_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT skill_key, category, score, tier, experience
        FROM character_skills
        WHERE entity_id=?
        ORDER BY COALESCE(category, ''), skill_key
        """,
        (character_id,),
    ).fetchall()
    return [
        {
            "kind": "skill",
            "key": row["skill_key"],
            "label": str(row["skill_key"]).replace("_", " ").title(),
            "category": row["category"],
            "score": row["score"],
            "tier": row["tier"],
            "experience": row["experience"],
        }
        for row in rows
    ]


def _preferences(conn: sqlite3.Connection, character_id: str) -> list[dict[str, Any]]:
    content: list[dict[str, Any]] = []
    rows = conn.execute(
        "SELECT preference_type, subject, intensity FROM character_preferences WHERE entity_id=? ORDER BY preference_type, subject",
        (character_id,),
    ).fetchall()
    for row in rows:
        content.append(
            {"kind": "preference", "preference_type": row["preference_type"], "subject": row["subject"], "intensity": row["intensity"]}
        )
    rows = conn.execute(
        "SELECT name, proficiency, frequency, enjoyment FROM character_hobbies WHERE entity_id=? ORDER BY name",
        (character_id,),
    ).fetchall()
    for row in rows:
        content.append(
            {"kind": "hobby", "name": row["name"], "proficiency": row["proficiency"], "frequency": row["frequency"], "enjoyment": row["enjoyment"]}
        )
    rows = conn.execute(
        "SELECT name, description, frequency, strength FROM character_habits WHERE entity_id=? ORDER BY name",
        (character_id,),
    ).fetchall()
    for row in rows:
        content.append(
            {"kind": "habit", "name": row["name"], "description": row["description"], "frequency": row["frequency"], "strength": row["strength"]}
        )
    return content

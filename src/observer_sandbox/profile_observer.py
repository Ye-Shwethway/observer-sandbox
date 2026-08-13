from __future__ import annotations

import json
import sqlite3
from typing import Any


PROFILE_SECTIONS: tuple[dict[str, Any], ...] = (
    {"id": "identity", "label": "Identity", "icon": "👤", "domains": ("identity",)},
    {"id": "appearance", "label": "Appearance", "icon": "🧬", "domains": ("appearance",)},
    {"id": "body", "label": "Body", "icon": "💪", "domains": ("body",)},
    {
        "id": "attributes",
        "label": "Attributes",
        "icon": "⚡",
        "domains": ("raps_pa", "raps_ma", "raps_ia", "social", "raps_vc"),
    },
    {"id": "personality", "label": "Personality", "icon": "🧠", "domains": ("personality",)},
    {"id": "skills", "label": "Skills", "icon": "🎯", "collection": "skills"},
    {"id": "preferences", "label": "Preferences & Habits", "icon": "❤️", "collection": "preferences"},
    {"id": "background", "label": "Background", "icon": "📜", "domains": ("background",)},
)

_SECTION_BY_ID = {section["id"]: section for section in PROFILE_SECTIONS}


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


def profile_menu(conn: sqlite3.Connection, character_id: str) -> dict[str, Any]:
    character = _character(conn, character_id)
    available: list[dict[str, Any]] = []
    for section in PROFILE_SECTIONS:
        section_id = str(section["id"])
        if _section_has_data(conn, character_id, section):
            available.append({"id": section_id, "label": section["label"], "icon": section["icon"]})
    return {"character": character, "sections": available}


def _section_has_data(conn: sqlite3.Connection, character_id: str, section: dict[str, Any]) -> bool:
    collection = section.get("collection")
    if collection == "skills":
        row = conn.execute("SELECT 1 FROM character_skills WHERE entity_id=? LIMIT 1", (character_id,)).fetchone()
        return row is not None
    if collection == "preferences":
        for table in ("character_preferences", "character_hobbies", "character_habits"):
            row = conn.execute(f"SELECT 1 FROM {table} WHERE entity_id=? LIMIT 1", (character_id,)).fetchone()
            if row is not None:
                return True
        return False

    domains = tuple(section.get("domains") or ())
    if not domains:
        return False
    placeholders = ",".join("?" for _ in domains)
    row = conn.execute(
        f"""
        SELECT 1
        FROM character_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.entity_id=? AND d.domain IN ({placeholders}) AND d.sensitivity='normal'
        LIMIT 1
        """,
        (character_id, *domains),
    ).fetchone()
    return row is not None


def profile_section(conn: sqlite3.Connection, character_id: str, section_id: str) -> dict[str, Any]:
    character = _character(conn, character_id)
    section = _SECTION_BY_ID.get(section_id)
    if section is None:
        raise KeyError(f"Unknown profile section: {section_id}")

    collection = section.get("collection")
    if collection == "skills":
        content = _skills(conn, character_id)
    elif collection == "preferences":
        content = _preferences(conn, character_id)
    else:
        content = _profile_values(conn, character_id, tuple(section.get("domains") or ()))

    return {
        "character": character,
        "section": {"id": section["id"], "label": section["label"], "icon": section["icon"]},
        "content": content,
    }


def _profile_values(conn: sqlite3.Connection, character_id: str, domains: tuple[str, ...]) -> list[dict[str, Any]]:
    if not domains:
        return []
    placeholders = ",".join("?" for _ in domains)
    rows = conn.execute(
        f"""
        SELECT v.field_key, v.value_json, v.mode, d.domain, d.label, d.data_type, d.unit
        FROM character_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.entity_id=? AND d.domain IN ({placeholders}) AND d.sensitivity='normal'
        ORDER BY CASE d.domain
            {''.join(f' WHEN ? THEN {index}' for index, _ in enumerate(domains))}
            ELSE 999 END,
            d.rowid
        """,
        (character_id, *domains, *domains),
    ).fetchall()
    return [
        {
            "kind": "field",
            "field_key": row["field_key"],
            "domain": row["domain"],
            "label": row["label"],
            "value": json.loads(row["value_json"]),
            "data_type": row["data_type"],
            "unit": row["unit"],
            "mode": row["mode"],
        }
        for row in rows
    ]


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
            {
                "kind": "preference",
                "preference_type": row["preference_type"],
                "subject": row["subject"],
                "intensity": row["intensity"],
            }
        )
    rows = conn.execute(
        "SELECT name, proficiency, frequency, enjoyment FROM character_hobbies WHERE entity_id=? ORDER BY name",
        (character_id,),
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
        "SELECT name, description, frequency, strength FROM character_habits WHERE entity_id=? ORDER BY name",
        (character_id,),
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

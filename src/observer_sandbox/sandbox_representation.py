from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable, Mapping

from .creation_sandbox import CreationSandboxError, get_sandbox_object
from .simulation import ACTION_NAMES


class SandboxRepresentationError(ValueError):
    pass


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS creation_sandbox_profile_values (
    object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    field_key TEXT NOT NULL REFERENCES profile_field_definitions(field_key),
    value_json TEXT NOT NULL,
    mode TEXT NOT NULL CHECK(mode IN ('canonical','static','derived','simulated')),
    authority TEXT NOT NULL,
    source TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(object_id, field_key)
);

CREATE TABLE IF NOT EXISTS creation_sandbox_character_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    skill_key TEXT NOT NULL,
    category TEXT,
    score REAL,
    tier TEXT,
    experience REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(object_id, skill_key)
);
"""


def migrate_sandbox_representation_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _loads(value: str | None, fallback: Any) -> Any:
    try:
        return json.loads(value or "")
    except (TypeError, json.JSONDecodeError):
        return fallback


def _require_type(conn: sqlite3.Connection, object_id: str, expected: str) -> dict[str, Any]:
    try:
        value = get_sandbox_object(conn, object_id)
    except CreationSandboxError as exc:
        raise SandboxRepresentationError(str(exc)) from exc
    if value["creation_type"] != expected:
        raise SandboxRepresentationError(f"Sandbox object must be a {expected}")
    if value["lifecycle_status"] != "active":
        raise SandboxRepresentationError(f"Archived sandbox {expected.title()} cannot be edited")
    return value


def set_sandbox_profile_values(
    conn: sqlite3.Connection,
    character_object_id: str,
    values: Mapping[str, Any],
    *,
    authority: str = "creator",
    source: str = "creator-creation-i3",
) -> list[dict[str, Any]]:
    character = _require_type(conn, character_object_id, "character")
    for field_key, raw in values.items():
        definition = conn.execute(
            "SELECT default_mode,default_authority FROM profile_field_definitions WHERE field_key=?",
            (str(field_key),),
        ).fetchone()
        if definition is None:
            raise SandboxRepresentationError(f"Unknown profile field: {field_key}")
        mode = str(definition["default_mode"])
        conn.execute(
            """
            INSERT INTO creation_sandbox_profile_values(object_id,field_key,value_json,mode,authority,source)
            VALUES(?,?,?,?,?,?)
            ON CONFLICT(object_id,field_key) DO UPDATE SET
                value_json=excluded.value_json,
                mode=excluded.mode,
                authority=excluded.authority,
                source=excluded.source,
                updated_at=CURRENT_TIMESTAMP
            """,
            (character_object_id, str(field_key), _json(raw), mode, authority, source),
        )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_profile_values_changed', ?)",
        (character["sandbox_id"], character_object_id, _json({"fields": sorted(str(k) for k in values)})),
    )
    conn.commit()
    return sandbox_profile_values(conn, character_object_id)


def sandbox_profile_values(conn: sqlite3.Connection, character_object_id: str) -> list[dict[str, Any]]:
    _require_type(conn, character_object_id, "character")
    rows = conn.execute(
        """
        SELECT v.field_key,v.value_json,v.mode,v.authority,v.source,
               d.domain,d.label,d.unit,d.sensitivity
        FROM creation_sandbox_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.object_id=?
        ORDER BY d.domain,d.field_key
        """,
        (character_object_id,),
    ).fetchall()
    return [
        {
            "field_key": str(row["field_key"]),
            "value": _loads(row["value_json"], None),
            "mode": str(row["mode"]),
            "authority": str(row["authority"]),
            "source": row["source"],
            "domain": str(row["domain"]),
            "label": str(row["label"]),
            "unit": row["unit"],
            "sensitivity": str(row["sensitivity"]),
        }
        for row in rows
    ]


def replace_sandbox_skills(
    conn: sqlite3.Connection,
    character_object_id: str,
    skills: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    character = _require_type(conn, character_object_id, "character")
    normalized: list[dict[str, Any]] = []
    for raw in skills:
        key = str(raw.get("skill_key") or "").strip()
        if not key:
            raise SandboxRepresentationError("Sandbox skill requires skill_key")
        score = raw.get("score")
        if score is not None and not 0 <= float(score) <= 100:
            raise SandboxRepresentationError(f"Sandbox skill score out of range: {key}")
        normalized.append({
            "skill_key": key,
            "category": raw.get("category"),
            "score": None if score is None else float(score),
            "tier": raw.get("tier"),
            "experience": raw.get("experience"),
            "metadata": dict(raw.get("metadata") or {}),
        })
    conn.execute("DELETE FROM creation_sandbox_character_skills WHERE object_id=?", (character_object_id,))
    for item in normalized:
        conn.execute(
            """
            INSERT INTO creation_sandbox_character_skills(
                object_id,skill_key,category,score,tier,experience,metadata_json
            ) VALUES(?,?,?,?,?,?,?)
            """,
            (
                character_object_id,item["skill_key"],item["category"],item["score"],
                item["tier"],item["experience"],_json(item["metadata"]),
            ),
        )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_skills_changed', ?)",
        (character["sandbox_id"], character_object_id, _json({"skills": [v["skill_key"] for v in normalized]})),
    )
    conn.commit()
    return sandbox_skills(conn, character_object_id)


def sandbox_skills(conn: sqlite3.Connection, character_object_id: str) -> list[dict[str, Any]]:
    _require_type(conn, character_object_id, "character")
    rows = conn.execute(
        """
        SELECT skill_key,category,score,tier,experience,metadata_json
        FROM creation_sandbox_character_skills WHERE object_id=? ORDER BY skill_key
        """,
        (character_object_id,),
    ).fetchall()
    return [
        {
            "skill_key": str(row["skill_key"]),
            "category": row["category"],
            "score": row["score"],
            "tier": row["tier"],
            "experience": row["experience"],
            "metadata": _loads(row["metadata_json"], {}),
        }
        for row in rows
    ]


def bind_sandbox_location_parent(
    conn: sqlite3.Connection,
    child_location_id: str,
    parent_location_id: str,
) -> dict[str, Any]:
    child = _require_type(conn, child_location_id, "location")
    parent = _require_type(conn, parent_location_id, "location")
    if child["sandbox_id"] != parent["sandbox_id"]:
        raise SandboxRepresentationError("Sandbox containment cannot cross namespaces")
    if child_location_id == parent_location_id:
        raise SandboxRepresentationError("Sandbox Location cannot contain itself")

    cursor = parent_location_id
    seen = {child_location_id}
    while cursor:
        if cursor in seen:
            raise SandboxRepresentationError("Sandbox Location containment cycle rejected")
        seen.add(cursor)
        row = conn.execute(
            """
            SELECT source_object_id FROM creation_sandbox_relations
            WHERE sandbox_id=? AND relation_type='contains' AND target_object_id=?
            ORDER BY id DESC LIMIT 1
            """,
            (child["sandbox_id"], cursor),
        ).fetchone()
        cursor = str(row["source_object_id"]) if row else ""

    conn.execute(
        "DELETE FROM creation_sandbox_relations WHERE sandbox_id=? AND relation_type='contains' AND target_object_id=?",
        (child["sandbox_id"], child_location_id),
    )
    conn.execute(
        """
        INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json)
        VALUES(?,?,'contains',?,'{}')
        """,
        (child["sandbox_id"], parent_location_id, child_location_id),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_location_parent_bound', ?)",
        (child["sandbox_id"], child_location_id, _json({"parent_location_id": parent_location_id})),
    )
    conn.commit()
    return get_sandbox_object(conn, child_location_id)


def sandbox_location_parent(conn: sqlite3.Connection, location_object_id: str) -> str | None:
    location = _require_type(conn, location_object_id, "location")
    row = conn.execute(
        """
        SELECT source_object_id FROM creation_sandbox_relations
        WHERE sandbox_id=? AND relation_type='contains' AND target_object_id=?
        ORDER BY id DESC LIMIT 1
        """,
        (location["sandbox_id"], location_object_id),
    ).fetchone()
    return None if row is None else str(row["source_object_id"])


def derive_sandbox_action_options(
    conn: sqlite3.Connection,
    character_object_id: str,
) -> list[dict[str, Any]]:
    character = _require_type(conn, character_object_id, "character")
    relation = conn.execute(
        """
        SELECT target_object_id FROM creation_sandbox_relations
        WHERE sandbox_id=? AND source_object_id=? AND relation_type='located_in'
        ORDER BY id DESC LIMIT 1
        """,
        (character["sandbox_id"], character_object_id),
    ).fetchone()
    if relation is None:
        return []
    location = _require_type(conn, str(relation["target_object_id"]), "location")
    allowed = set(ACTION_NAMES)
    options: dict[tuple[str, str], dict[str, Any]] = {}
    for source in (character, location):
        for capability in source.get("capabilities", []):
            action_key = str(capability).strip()
            if action_key not in allowed:
                continue
            options[(action_key, source["object_id"])] = {
                "action_key": action_key,
                "source_object_id": source["object_id"],
                "metadata": {"derived_from": "capability", "source_type": source["creation_type"]},
            }
    return [options[key] for key in sorted(options)]


__all__ = [
    "SandboxRepresentationError",
    "bind_sandbox_location_parent",
    "derive_sandbox_action_options",
    "migrate_sandbox_representation_schema",
    "replace_sandbox_skills",
    "sandbox_location_parent",
    "sandbox_profile_values",
    "sandbox_skills",
    "set_sandbox_profile_values",
]

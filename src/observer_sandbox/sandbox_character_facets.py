from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable, Mapping

from .creation_sandbox import CreationSandboxError, get_sandbox_object


class SandboxCharacterFacetError(ValueError):
    pass


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS creation_sandbox_character_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    preference_type TEXT NOT NULL CHECK(preference_type IN ('like','dislike','interest','aversion')),
    subject TEXT NOT NULL,
    intensity REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(object_id, preference_type, subject)
);

CREATE TABLE IF NOT EXISTS creation_sandbox_character_hobbies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    proficiency REAL,
    frequency TEXT,
    enjoyment REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(object_id, name)
);

CREATE TABLE IF NOT EXISTS creation_sandbox_character_habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    frequency TEXT,
    strength REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(object_id, name)
);
"""


def migrate_sandbox_character_facets_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _loads(value: str | None) -> dict[str, Any]:
    try:
        loaded = json.loads(value or "{}")
    except json.JSONDecodeError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _require_character(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    try:
        value = get_sandbox_object(conn, object_id)
    except CreationSandboxError as exc:
        raise SandboxCharacterFacetError(str(exc)) from exc
    if value["creation_type"] != "character":
        raise SandboxCharacterFacetError("Sandbox object must be a character")
    if value["lifecycle_status"] != "active":
        raise SandboxCharacterFacetError("Archived sandbox Character cannot be edited")
    return value


def replace_sandbox_preferences(
    conn: sqlite3.Connection,
    object_id: str,
    values: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    character = _require_character(conn, object_id)
    normalized: list[dict[str, Any]] = []
    for raw in values:
        preference_type = str(raw.get("preference_type") or "").strip().lower()
        subject = str(raw.get("subject") or "").strip()
        if preference_type not in {"like", "dislike", "interest", "aversion"}:
            raise SandboxCharacterFacetError(f"Unsupported preference type: {preference_type or '<empty>'}")
        if not subject:
            raise SandboxCharacterFacetError("Sandbox preference requires subject")
        intensity = raw.get("intensity")
        if intensity is not None and not 0 <= float(intensity) <= 100:
            raise SandboxCharacterFacetError("Sandbox preference intensity must be 0..100")
        normalized.append({
            "preference_type": preference_type,
            "subject": subject,
            "intensity": None if intensity is None else float(intensity),
            "metadata": dict(raw.get("metadata") or {}),
        })
    conn.execute("DELETE FROM creation_sandbox_character_preferences WHERE object_id=?", (object_id,))
    for item in normalized:
        conn.execute(
            "INSERT INTO creation_sandbox_character_preferences(object_id,preference_type,subject,intensity,metadata_json) VALUES(?,?,?,?,?)",
            (object_id, item["preference_type"], item["subject"], item["intensity"], _json(item["metadata"])),
        )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_preferences_changed', ?)",
        (character["sandbox_id"], object_id, _json({"count": len(normalized)})),
    )
    conn.commit()
    return sandbox_preferences(conn, object_id)


def sandbox_preferences(conn: sqlite3.Connection, object_id: str) -> list[dict[str, Any]]:
    _require_character(conn, object_id)
    rows = conn.execute(
        "SELECT preference_type,subject,intensity,metadata_json FROM creation_sandbox_character_preferences WHERE object_id=? ORDER BY preference_type,subject",
        (object_id,),
    ).fetchall()
    return [{
        "preference_type": str(row["preference_type"]),
        "subject": str(row["subject"]),
        "intensity": row["intensity"],
        "metadata": _loads(row["metadata_json"]),
    } for row in rows]


def replace_sandbox_hobbies(
    conn: sqlite3.Connection,
    object_id: str,
    values: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    character = _require_character(conn, object_id)
    normalized: list[dict[str, Any]] = []
    for raw in values:
        name = str(raw.get("name") or "").strip()
        if not name:
            raise SandboxCharacterFacetError("Sandbox hobby requires name")
        normalized.append({
            "name": name,
            "proficiency": raw.get("proficiency"),
            "frequency": raw.get("frequency"),
            "enjoyment": raw.get("enjoyment"),
            "metadata": dict(raw.get("metadata") or {}),
        })
    conn.execute("DELETE FROM creation_sandbox_character_hobbies WHERE object_id=?", (object_id,))
    for item in normalized:
        conn.execute(
            "INSERT INTO creation_sandbox_character_hobbies(object_id,name,proficiency,frequency,enjoyment,metadata_json) VALUES(?,?,?,?,?,?)",
            (object_id, item["name"], item["proficiency"], item["frequency"], item["enjoyment"], _json(item["metadata"])),
        )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_hobbies_changed', ?)",
        (character["sandbox_id"], object_id, _json({"count": len(normalized)})),
    )
    conn.commit()
    return sandbox_hobbies(conn, object_id)


def sandbox_hobbies(conn: sqlite3.Connection, object_id: str) -> list[dict[str, Any]]:
    _require_character(conn, object_id)
    rows = conn.execute(
        "SELECT name,proficiency,frequency,enjoyment,metadata_json FROM creation_sandbox_character_hobbies WHERE object_id=? ORDER BY name",
        (object_id,),
    ).fetchall()
    return [{
        "name": str(row["name"]),
        "proficiency": row["proficiency"],
        "frequency": row["frequency"],
        "enjoyment": row["enjoyment"],
        "metadata": _loads(row["metadata_json"]),
    } for row in rows]


def replace_sandbox_habits(
    conn: sqlite3.Connection,
    object_id: str,
    values: Iterable[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    character = _require_character(conn, object_id)
    normalized: list[dict[str, Any]] = []
    for raw in values:
        name = str(raw.get("name") or "").strip()
        if not name:
            raise SandboxCharacterFacetError("Sandbox habit requires name")
        normalized.append({
            "name": name,
            "description": raw.get("description"),
            "frequency": raw.get("frequency"),
            "strength": raw.get("strength"),
            "metadata": dict(raw.get("metadata") or {}),
        })
    conn.execute("DELETE FROM creation_sandbox_character_habits WHERE object_id=?", (object_id,))
    for item in normalized:
        conn.execute(
            "INSERT INTO creation_sandbox_character_habits(object_id,name,description,frequency,strength,metadata_json) VALUES(?,?,?,?,?,?)",
            (object_id, item["name"], item["description"], item["frequency"], item["strength"], _json(item["metadata"])),
        )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_habits_changed', ?)",
        (character["sandbox_id"], object_id, _json({"count": len(normalized)})),
    )
    conn.commit()
    return sandbox_habits(conn, object_id)


def sandbox_habits(conn: sqlite3.Connection, object_id: str) -> list[dict[str, Any]]:
    _require_character(conn, object_id)
    rows = conn.execute(
        "SELECT name,description,frequency,strength,metadata_json FROM creation_sandbox_character_habits WHERE object_id=? ORDER BY name",
        (object_id,),
    ).fetchall()
    return [{
        "name": str(row["name"]),
        "description": row["description"],
        "frequency": row["frequency"],
        "strength": row["strength"],
        "metadata": _loads(row["metadata_json"]),
    } for row in rows]


__all__ = [
    "SandboxCharacterFacetError",
    "migrate_sandbox_character_facets_schema",
    "replace_sandbox_habits",
    "replace_sandbox_hobbies",
    "replace_sandbox_preferences",
    "sandbox_habits",
    "sandbox_hobbies",
    "sandbox_preferences",
]

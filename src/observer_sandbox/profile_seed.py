from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class ProfileSeedError(RuntimeError):
    pass


def load_seed(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate_seed(conn: sqlite3.Connection, seed: dict[str, Any]) -> None:
    defined = {
        row[0]
        for row in conn.execute("SELECT field_key FROM profile_field_definitions")
    }
    unknown = sorted(set(seed.get("values", {})) - defined)
    if unknown:
        raise ProfileSeedError(f"Unknown profile fields: {', '.join(unknown)}")


def import_seed(conn: sqlite3.Connection, seed: dict[str, Any]) -> None:
    validate_seed(conn, seed)
    entity_id = seed["entity_id"]
    name = seed["name"]
    revision = seed.get("canonical_revision")
    schema_version = int(seed.get("profile_schema_version", 1))

    conn.execute(
        """
        INSERT INTO entities(id, entity_type, name)
        VALUES (?, 'character', ?)
        ON CONFLICT(id) DO UPDATE SET name=excluded.name, updated_at=CURRENT_TIMESTAMP
        """,
        (entity_id, name),
    )
    conn.execute(
        """
        INSERT INTO character_profiles(entity_id, profile_schema_version, canonical_revision, status)
        VALUES (?, ?, ?, 'active')
        ON CONFLICT(entity_id) DO UPDATE SET
            profile_schema_version=excluded.profile_schema_version,
            canonical_revision=excluded.canonical_revision,
            updated_at=CURRENT_TIMESTAMP
        """,
        (entity_id, schema_version, revision),
    )

    for field_key, record in seed.get("values", {}).items():
        value_json = json.dumps(record["value"], ensure_ascii=False)
        old = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
            (entity_id, field_key),
        ).fetchone()
        if old is not None and old[0] != value_json:
            conn.execute(
                """
                INSERT INTO character_profile_history(
                    entity_id, field_key, old_value_json, new_value_json, mode, authority, reason
                ) VALUES (?, ?, ?, ?, ?, ?, 'canonical seed update')
                """,
                (entity_id, field_key, old[0], value_json, record["mode"], record["authority"]),
            )
        conn.execute(
            """
            INSERT INTO character_profile_values(
                entity_id, field_key, value_json, mode, authority, source, confidence
            ) VALUES (?, ?, ?, ?, ?, ?, 1.0)
            ON CONFLICT(entity_id, field_key) DO UPDATE SET
                value_json=excluded.value_json,
                mode=excluded.mode,
                authority=excluded.authority,
                source=excluded.source,
                confidence=excluded.confidence,
                updated_at=CURRENT_TIMESTAMP
            """,
            (entity_id, field_key, value_json, record["mode"], record["authority"], revision),
        )

    conn.execute("DELETE FROM character_preferences WHERE entity_id=?", (entity_id,))
    for kind, items in seed.get("preferences", {}).items():
        preference_type = "like" if kind == "likes" else "dislike" if kind == "dislikes" else kind
        for subject in items:
            conn.execute(
                "INSERT INTO character_preferences(entity_id, preference_type, subject) VALUES (?, ?, ?)",
                (entity_id, preference_type, subject),
            )

    conn.execute("DELETE FROM character_hobbies WHERE entity_id=?", (entity_id,))
    for hobby in seed.get("hobbies", []):
        conn.execute(
            "INSERT INTO character_hobbies(entity_id, name) VALUES (?, ?)",
            (entity_id, hobby),
        )

    conn.execute("DELETE FROM character_habits WHERE entity_id=?", (entity_id,))
    for habit in seed.get("habits", []):
        conn.execute(
            "INSERT INTO character_habits(entity_id, name) VALUES (?, ?)",
            (entity_id, habit),
        )

    conn.execute("DELETE FROM character_skills WHERE entity_id=?", (entity_id,))
    for skill in seed.get("skills", []):
        conn.execute(
            """
            INSERT INTO character_skills(entity_id, skill_key, category, score, metadata_json)
            VALUES (?, ?, ?, ?, '{}')
            """,
            (entity_id, skill["key"], skill.get("category"), skill.get("score")),
        )
    conn.commit()

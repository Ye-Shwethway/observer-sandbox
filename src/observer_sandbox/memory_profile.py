from __future__ import annotations

import json
import sqlite3
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TRAITS_PATH = REPO_ROOT / "config" / "memory" / "character_traits.v1.json"

FIELDS = (
    ("memory.working_memory", "Working memory", "Capacity to hold and manipulate currently active information."),
    ("memory.encoding", "Memory encoding", "Quality with which experience becomes a durable memory trace."),
    ("memory.retention", "Memory retention", "Resistance of stored traces to loss of accessibility over time."),
    ("memory.recall", "Memory recall", "Ability to retrieve existing traces from partial or contextual cues."),
)


def seed_memory_profile_definitions(conn: sqlite3.Connection) -> None:
    for key, label, description in FIELDS:
        conn.execute(
            """INSERT INTO profile_field_definitions(
                field_key,domain,label,data_type,unit,description,default_mode,default_authority,sensitivity,metadata_json
            ) VALUES(?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(field_key) DO UPDATE SET
                domain=excluded.domain,label=excluded.label,data_type=excluded.data_type,
                description=excluded.description,default_mode=excluded.default_mode,
                default_authority=excluded.default_authority,updated_at=CURRENT_TIMESTAMP""",
            (key, "memory", label, "number", None, description, "static", "memory_core", "normal", "{}"),
        )


def seed_memory_profile_values(
    conn: sqlite3.Connection,
    path: str | Path = DEFAULT_TRAITS_PATH,
) -> None:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    revision = str(payload.get("revision") or "memory-character-traits-v1")
    for block in payload.get("characters", []):
        if not isinstance(block, dict):
            continue
        character_id = str(block.get("character_id") or "").strip()
        if not character_id:
            continue
        if conn.execute("SELECT 1 FROM character_profiles WHERE entity_id=?", (character_id,)).fetchone() is None:
            continue
        values = block.get("values") if isinstance(block.get("values"), dict) else {}
        for key, raw in values.items():
            if key not in {field[0] for field in FIELDS}:
                continue
            value = max(0.0, min(float(raw), 100.0))
            conn.execute(
                """INSERT INTO character_profile_values(
                    entity_id,field_key,value_json,mode,authority,source,confidence
                ) VALUES(?,?,?,?,?,?,?)
                ON CONFLICT(entity_id,field_key) DO NOTHING""",
                (character_id, key, json.dumps(value), "static", "memory_core", revision, 1.0),
            )

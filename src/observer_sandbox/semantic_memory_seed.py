from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SEMANTIC_MEMORY_PATH = REPO_ROOT / "config" / "memory" / "initial.semantic.v1.json"
SPATIAL_FAMILIARITY_LEVELS = ("unknown", "aware", "familiar", "intimate")
LEGACY_SPATIAL_FIELD = "world.spatial_familiarity"
INITIAL_KNOWN_SIM_TIME = "2025-05-01T07:00:00+00:00"


def load_initial_semantic_memory_seed(path: str | Path = DEFAULT_SEMANTIC_MEMORY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _memory_id(character_id: str, knowledge_kind: str, entity_id: str) -> str:
    return f"mem_seed_{knowledge_kind}_{character_id}_{entity_id}"


def _validate_character(conn: sqlite3.Connection, character_id: str) -> None:
    row = conn.execute("SELECT 1 FROM entities WHERE id=? AND entity_type='character'", (character_id,)).fetchone()
    if row is None:
        raise ValueError(f"Unknown semantic-memory character: {character_id}")


def _validate_spatial_memory(conn: sqlite3.Connection, raw: dict[str, Any]) -> dict[str, Any]:
    location_id = str(raw.get("location_id") or "").strip()
    familiarity = str(raw.get("familiarity") or "unknown").strip()
    if not location_id or familiarity not in SPATIAL_FAMILIARITY_LEVELS:
        raise ValueError(f"Invalid spatial semantic-memory row: {raw!r}")
    exists = conn.execute("SELECT name FROM entities WHERE id=? AND entity_type='location'", (location_id,)).fetchone()
    if exists is None:
        raise ValueError(f"Unknown spatial semantic-memory location: {location_id}")
    return {
        "knowledge_kind": "spatial_familiarity",
        "location_id": location_id,
        "location_name": str(exists["name"]),
        "familiarity": familiarity,
        "secret": bool(raw.get("secret", False)),
        "basis": str(raw.get("basis") or "authored_character_knowledge"),
    }


def seed_initial_semantic_memories(
    conn: sqlite3.Connection,
    *,
    sim_time: str,
    path: str | Path = DEFAULT_SEMANTIC_MEMORY_PATH,
) -> None:
    """Seed established actor-owned knowledge through one character-generic contract."""
    seed = load_initial_semantic_memory_seed(path)
    revision = str(seed.get("revision") or "").strip()
    if not revision:
        raise ValueError("Initial semantic-memory seed requires revision")

    for character_block in seed.get("characters", []):
        if not isinstance(character_block, dict):
            continue
        character_id = str(character_block.get("character_id") or "").strip()
        if not character_id:
            raise ValueError("Semantic-memory character block requires character_id")
        _validate_character(conn, character_id)
        for raw in character_block.get("memories", []):
            if not isinstance(raw, dict):
                continue
            knowledge_kind = str(raw.get("knowledge_kind") or "").strip()
            if knowledge_kind != "spatial_familiarity":
                raise ValueError(f"Unsupported initial semantic knowledge kind: {knowledge_kind}")
            content = _validate_spatial_memory(conn, raw)
            location_id = content["location_id"]
            memory_id = _memory_id(character_id, knowledge_kind, location_id)
            summary = f"Knows {content['location_name']} with {content['familiarity']} familiarity"
            conn.execute(
                """INSERT OR IGNORE INTO character_memories(
                    memory_id,character_id,memory_type,summary,content_json,source_type,
                    source_event_id,event_sim_time,encoded_sim_time,salience,confidence,status,
                    lifecycle_stage,memory_strength,detail_strength,emotional_arousal,personal_relevance,
                    consolidated_sim_time,last_dynamics_sim_time,metadata_json
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    memory_id, character_id, "semantic", summary,
                    json.dumps(content, ensure_ascii=False, sort_keys=True), "seed", None,
                    INITIAL_KNOWN_SIM_TIME, sim_time, 0.7, 1.0, "active", "consolidated",
                    1.0, 1.0, 0.05, 0.8, sim_time, sim_time,
                    json.dumps({"seed_revision": revision, "semantic_key": f"spatial_familiarity:{location_id}"}, ensure_ascii=False, sort_keys=True),
                ),
            )
            conn.execute(
                "INSERT OR IGNORE INTO character_memory_entities(memory_id,entity_id,relation_role) VALUES(?,?,?)",
                (memory_id, location_id, "known_location"),
            )

    conn.execute("DELETE FROM fields WHERE field_key=?", (LEGACY_SPATIAL_FIELD,))
    conn.execute("DELETE FROM runtime_state WHERE key='spatial_familiarity_revision'")
    conn.execute(
        """INSERT INTO runtime_state(key,value_json) VALUES('initial_semantic_memory_revision',?)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=CURRENT_TIMESTAMP""",
        (json.dumps(revision),),
    )
    conn.commit()

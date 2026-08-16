from __future__ import annotations

import sqlite3


MEMORY_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS character_memories (
    memory_id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    memory_type TEXT NOT NULL CHECK(memory_type IN ('episodic','semantic')),
    summary TEXT NOT NULL,
    content_json TEXT NOT NULL DEFAULT '{}',
    source_type TEXT NOT NULL,
    source_event_id INTEGER REFERENCES events(id) ON DELETE SET NULL,
    event_sim_time TEXT NOT NULL,
    encoded_sim_time TEXT NOT NULL,
    salience REAL NOT NULL DEFAULT 0.5 CHECK(salience >= 0 AND salience <= 1),
    confidence REAL NOT NULL DEFAULT 1.0 CHECK(confidence >= 0 AND confidence <= 1),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','retired')),
    last_recalled_sim_time TEXT,
    recall_count INTEGER NOT NULL DEFAULT 0 CHECK(recall_count >= 0),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS character_memory_entities (
    memory_id TEXT NOT NULL REFERENCES character_memories(memory_id) ON DELETE CASCADE,
    entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    relation_role TEXT NOT NULL DEFAULT 'related',
    PRIMARY KEY(memory_id, entity_id, relation_role)
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_character_memories_source_event
    ON character_memories(character_id, source_event_id)
    WHERE source_event_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_character_memories_character_time
    ON character_memories(character_id, status, event_sim_time DESC);
CREATE INDEX IF NOT EXISTS idx_character_memories_type
    ON character_memories(character_id, memory_type, status, event_sim_time DESC);
CREATE INDEX IF NOT EXISTS idx_character_memory_entities_entity
    ON character_memory_entities(entity_id, memory_id);
"""


def migrate_memory_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(MEMORY_SCHEMA_SQL)
    conn.commit()

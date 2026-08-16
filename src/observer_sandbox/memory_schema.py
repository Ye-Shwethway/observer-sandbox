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

CREATE TRIGGER IF NOT EXISTS trg_character_memory_action_completed
AFTER INSERT ON events
WHEN NEW.event_type='action_completed'
 AND NEW.actor_id IS NOT NULL
 AND json_extract(NEW.payload_json, '$.action') IS NOT NULL
BEGIN
    INSERT OR IGNORE INTO character_memories(
        memory_id,character_id,memory_type,summary,content_json,source_type,source_event_id,
        event_sim_time,encoded_sim_time,salience,confidence,status,metadata_json
    ) VALUES(
        'mem_event_' || NEW.id,
        NEW.actor_id,
        'episodic',
        replace(json_extract(NEW.payload_json, '$.action'), '_', ' '),
        json_object(
            'action', json_extract(NEW.payload_json, '$.action'),
            'target_id', json_extract(NEW.payload_json, '$.target'),
            'location_id', NEW.location_id,
            'duration_minutes', json_extract(NEW.payload_json, '$.duration_minutes'),
            'reason', json_extract(NEW.payload_json, '$.reason'),
            'state_changes', json(NEW.state_changes_json)
        ),
        'event',
        NEW.id,
        NEW.sim_time,
        NEW.sim_time,
        min(
            1.0,
            0.40
            + CASE WHEN json_extract(NEW.payload_json, '$.target') IS NOT NULL THEN 0.05 ELSE 0 END
            + CASE WHEN NEW.state_changes_json IS NOT NULL AND NEW.state_changes_json != '{}' THEN 0.10 ELSE 0 END
            + CASE WHEN json_type(NEW.payload_json, '$.skill_application')='object' THEN 0.08 ELSE 0 END
            + CASE WHEN json_type(NEW.payload_json, '$.training_method')='object' THEN 0.08 ELSE 0 END
            + CASE WHEN json_type(NEW.payload_json, '$.represented_skill_task')='object' THEN 0.08 ELSE 0 END
            + CASE WHEN json_type(NEW.payload_json, '$.nutrition_intake')='object' THEN 0.08 ELSE 0 END
        ),
        1.0,
        'active',
        '{}'
    );

    INSERT OR IGNORE INTO character_memory_entities(memory_id,entity_id,relation_role)
    SELECT 'mem_event_' || NEW.id, NEW.location_id, 'location'
    WHERE NEW.location_id IS NOT NULL
      AND EXISTS(SELECT 1 FROM entities WHERE id=NEW.location_id);

    INSERT OR IGNORE INTO character_memory_entities(memory_id,entity_id,relation_role)
    SELECT 'mem_event_' || NEW.id, json_extract(NEW.payload_json, '$.target'), 'target'
    WHERE json_extract(NEW.payload_json, '$.target') IS NOT NULL
      AND json_extract(NEW.payload_json, '$.target') != NEW.location_id
      AND EXISTS(
          SELECT 1 FROM entities
          WHERE id=json_extract(NEW.payload_json, '$.target')
      );
END;
"""


def migrate_memory_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(MEMORY_SCHEMA_SQL)
    conn.commit()

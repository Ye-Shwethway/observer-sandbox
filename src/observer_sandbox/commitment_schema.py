from __future__ import annotations

import sqlite3


COMMITMENT_SCHEMA_VERSION = 1

COMMITMENT_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS commitments (
    commitment_id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    commitment_type TEXT NOT NULL CHECK(commitment_type IN (
        'appointment','promise','deadline','scheduled_responsibility'
    )),
    title TEXT NOT NULL,
    details TEXT,
    start_sim_time TEXT,
    due_sim_time TEXT,
    target_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    target_location_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN (
        'pending','active','completed','cancelled','missed'
    )),
    flexibility TEXT NOT NULL DEFAULT 'fixed' CHECK(flexibility IN (
        'fixed','flexible','reschedulable'
    )),
    source_type TEXT,
    source_id TEXT,
    source_event_id INTEGER REFERENCES events(id) ON DELETE SET NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK(start_sim_time IS NOT NULL OR due_sim_time IS NOT NULL)
);

CREATE INDEX IF NOT EXISTS idx_commitments_character_status_time
    ON commitments(character_id, status, due_sim_time, start_sim_time);
CREATE INDEX IF NOT EXISTS idx_commitments_due_time
    ON commitments(status, due_sim_time);
"""


def migrate_commitment_schema(conn: sqlite3.Connection) -> None:
    """Install W2 commitment truth without creating reminders, exposure or cognition."""
    conn.executescript(COMMITMENT_SCHEMA_SQL)
    conn.execute(
        "INSERT INTO schema_meta(key,value) VALUES('commitment_schema_version',?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(COMMITMENT_SCHEMA_VERSION),),
    )
    conn.commit()

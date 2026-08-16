from __future__ import annotations

import sqlite3


WORLD_INPUT_SCHEMA_VERSION = 1

WORLD_INPUT_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS world_stimuli (
    stimulus_id TEXT PRIMARY KEY,
    stimulus_type TEXT NOT NULL CHECK(stimulus_type IN (
        'environment','information','communication','financial',
        'obligation','social','system','other'
    )),
    channel TEXT NOT NULL CHECK(channel IN (
        'visual','auditory','tactile','environmental','device',
        'media','direct','mixed','other'
    )),
    subject TEXT NOT NULL,
    payload_json TEXT NOT NULL DEFAULT '{}',
    source_type TEXT,
    source_id TEXT,
    source_event_id INTEGER REFERENCES events(id) ON DELETE SET NULL,
    source_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    salience REAL NOT NULL DEFAULT 0.5 CHECK(salience >= 0 AND salience <= 1),
    start_sim_time TEXT NOT NULL,
    end_sim_time TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','expired','retired')),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS world_stimulus_scopes (
    stimulus_id TEXT NOT NULL REFERENCES world_stimuli(stimulus_id) ON DELETE CASCADE,
    scope_type TEXT NOT NULL CHECK(scope_type IN ('world','location','entity','character','audience')),
    scope_id TEXT NOT NULL,
    relation_role TEXT NOT NULL DEFAULT 'available_to',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(stimulus_id, scope_type, scope_id, relation_role)
);

CREATE TABLE IF NOT EXISTS character_exposures (
    exposure_id TEXT PRIMARY KEY,
    stimulus_id TEXT NOT NULL REFERENCES world_stimuli(stimulus_id) ON DELETE CASCADE,
    character_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    sim_time TEXT NOT NULL,
    channel TEXT NOT NULL CHECK(channel IN (
        'visual','auditory','tactile','environmental','device',
        'media','direct','mixed','other'
    )),
    source_location_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    source_entity_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    attention_hint REAL CHECK(attention_hint IS NULL OR (attention_hint >= 0 AND attention_hint <= 1)),
    status TEXT NOT NULL DEFAULT 'exposed' CHECK(status IN ('exposed','invalidated')),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_world_stimuli_active_time
    ON world_stimuli(status, start_sim_time, end_sim_time);
CREATE INDEX IF NOT EXISTS idx_world_stimulus_scopes_lookup
    ON world_stimulus_scopes(scope_type, scope_id, stimulus_id);
CREATE INDEX IF NOT EXISTS idx_character_exposures_character_time
    ON character_exposures(character_id, sim_time DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_character_exposures_stimulus
    ON character_exposures(stimulus_id, character_id, sim_time DESC);
"""


def migrate_world_input_schema(conn: sqlite3.Connection) -> None:
    """Install the generic world stimulus/exposure schema without activating producers."""
    conn.executescript(WORLD_INPUT_SCHEMA_SQL)
    conn.execute(
        "INSERT INTO schema_meta(key,value) VALUES('world_input_schema_version',?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(WORLD_INPUT_SCHEMA_VERSION),),
    )
    conn.commit()

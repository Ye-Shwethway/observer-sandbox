from __future__ import annotations

import sqlite3


MIND_SCHEMA_VERSION = 1

MIND_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS mental_cycles (
    cycle_id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    sim_time TEXT NOT NULL,
    trigger_type TEXT NOT NULL CHECK(trigger_type IN (
        'decision_wake','action_start','action_completed','communication_received',
        'perception_event','scheduled','internal','other'
    )),
    trigger_source_type TEXT,
    trigger_source_id TEXT,
    status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open','completed','failed','aborted')),
    schema_version INTEGER NOT NULL DEFAULT 1 CHECK(schema_version >= 1),
    provider_id TEXT,
    model_id TEXT,
    input_summary_json TEXT NOT NULL DEFAULT '{}',
    output_summary_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mental_episodes (
    episode_id TEXT PRIMARY KEY,
    cycle_id TEXT NOT NULL REFERENCES mental_cycles(cycle_id) ON DELETE CASCADE,
    character_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    mode TEXT NOT NULL CHECK(mode IN (
        'task_focused','spontaneous','reflective','prospective','social','evaluative'
    )),
    summary TEXT NOT NULL,
    content_json TEXT NOT NULL DEFAULT '{}',
    importance REAL NOT NULL DEFAULT 0.5 CHECK(importance >= 0 AND importance <= 1),
    valence REAL NOT NULL DEFAULT 0.0 CHECK(valence >= -1 AND valence <= 1),
    activation REAL NOT NULL DEFAULT 0.5 CHECK(activation >= 0 AND activation <= 1),
    persistence REAL NOT NULL DEFAULT 0.0 CHECK(persistence >= 0 AND persistence <= 1),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','completed','retired')),
    start_sim_time TEXT NOT NULL,
    end_sim_time TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mental_artifacts (
    artifact_id TEXT PRIMARY KEY,
    character_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    artifact_type TEXT NOT NULL CHECK(artifact_type IN (
        'concern','goal','intention','plan','social_inference','appraisal','working_item'
    )),
    title TEXT NOT NULL,
    content_json TEXT NOT NULL DEFAULT '{}',
    priority REAL NOT NULL DEFAULT 0.5 CHECK(priority >= 0 AND priority <= 1),
    activation REAL NOT NULL DEFAULT 0.5 CHECK(activation >= 0 AND activation <= 1),
    confidence REAL NOT NULL DEFAULT 1.0 CHECK(confidence >= 0 AND confidence <= 1),
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','dormant','resolved','retired')),
    source_cycle_id TEXT REFERENCES mental_cycles(cycle_id) ON DELETE SET NULL,
    created_sim_time TEXT NOT NULL,
    updated_sim_time TEXT NOT NULL,
    resolved_sim_time TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mental_links (
    link_id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    source_kind TEXT NOT NULL CHECK(source_kind IN ('cycle','episode','artifact')),
    source_id TEXT NOT NULL,
    target_kind TEXT NOT NULL CHECK(target_kind IN (
        'memory','event','entity','action_instance','cycle','episode','artifact'
    )),
    target_id TEXT NOT NULL,
    relation_type TEXT NOT NULL DEFAULT 'related',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(character_id, source_kind, source_id, target_kind, target_id, relation_type)
);

CREATE INDEX IF NOT EXISTS idx_mental_cycles_character_time
    ON mental_cycles(character_id, sim_time DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_mental_episodes_character_time
    ON mental_episodes(character_id, start_sim_time DESC, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_mental_episodes_cycle
    ON mental_episodes(cycle_id, created_at);
CREATE INDEX IF NOT EXISTS idx_mental_artifacts_character_active
    ON mental_artifacts(character_id, status, priority DESC, activation DESC);
CREATE INDEX IF NOT EXISTS idx_mental_links_source
    ON mental_links(character_id, source_kind, source_id);
CREATE INDEX IF NOT EXISTS idx_mental_links_target
    ON mental_links(character_id, target_kind, target_id);
"""


def migrate_mind_schema(conn: sqlite3.Connection) -> None:
    """Install the generic Mind Engine foundation schema without activating behavior."""
    conn.executescript(MIND_SCHEMA_SQL)
    conn.execute(
        "INSERT INTO schema_meta(key,value) VALUES('mind_schema_version',?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(MIND_SCHEMA_VERSION),),
    )
    conn.commit()

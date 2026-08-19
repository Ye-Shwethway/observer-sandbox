from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from .commitment_schema import migrate_commitment_schema
from .composition_schema import migrate_composition_schema
from .creation_sandbox_schema import migrate_creation_sandbox_schema
from .economy_schema import migrate_economy_schema
from .environment_schema import migrate_environment_schema
from .information_schema import migrate_information_schema
from .memory_schema import migrate_memory_schema
from .mind_schema import migrate_mind_schema
from .world_input_schema import migrate_world_input_schema

SCHEMA_VERSION = 18

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS entities (
    id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    name TEXT NOT NULL,
    state_json TEXT NOT NULL DEFAULT '{}',
    capabilities_json TEXT NOT NULL DEFAULT '[]',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    target_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(source_id, relation_type, target_id)
);

CREATE TABLE IF NOT EXISTS fields (
    entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    field_key TEXT NOT NULL,
    value_json TEXT NOT NULL,
    mode TEXT NOT NULL CHECK(mode IN ('canonical','static','derived','simulated')),
    authority TEXT NOT NULL,
    source TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(entity_id, field_key)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sim_time TEXT NOT NULL,
    actor_id TEXT REFERENCES entities(id) ON DELETE SET NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS runtime_state (
    key TEXT PRIMARY KEY,
    value_json TEXT NOT NULL,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS profile_field_definitions (
    field_key TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    label TEXT NOT NULL,
    data_type TEXT NOT NULL CHECK(data_type IN ('integer','number','text','boolean','date','datetime','json')),
    unit TEXT,
    description TEXT,
    default_mode TEXT NOT NULL DEFAULT 'static' CHECK(default_mode IN ('canonical','static','derived','simulated')),
    default_authority TEXT NOT NULL DEFAULT 'profile_core',
    sensitivity TEXT NOT NULL DEFAULT 'normal' CHECK(sensitivity IN ('normal','private','intimate')),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS character_profiles (
    entity_id TEXT PRIMARY KEY REFERENCES entities(id) ON DELETE CASCADE,
    profile_schema_version INTEGER NOT NULL DEFAULT 1,
    canonical_revision TEXT,
    status TEXT NOT NULL DEFAULT 'active',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS character_profile_values (
    entity_id TEXT NOT NULL REFERENCES character_profiles(entity_id) ON DELETE CASCADE,
    field_key TEXT NOT NULL REFERENCES profile_field_definitions(field_key),
    value_json TEXT NOT NULL,
    mode TEXT NOT NULL CHECK(mode IN ('canonical','static','derived','simulated')),
    authority TEXT NOT NULL,
    source TEXT,
    confidence REAL CHECK(confidence IS NULL OR (confidence >= 0 AND confidence <= 1)),
    observed_at TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(entity_id, field_key)
);

CREATE TABLE IF NOT EXISTS character_profile_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL REFERENCES character_profiles(entity_id) ON DELETE CASCADE,
    field_key TEXT NOT NULL REFERENCES profile_field_definitions(field_key),
    old_value_json TEXT,
    new_value_json TEXT NOT NULL,
    mode TEXT NOT NULL CHECK(mode IN ('canonical','static','derived','simulated')),
    authority TEXT NOT NULL,
    reason TEXT,
    sim_time TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS character_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL REFERENCES character_profiles(entity_id) ON DELETE CASCADE,
    preference_type TEXT NOT NULL CHECK(preference_type IN ('like','dislike','interest','aversion')),
    subject TEXT NOT NULL,
    intensity REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(entity_id, preference_type, subject)
);

CREATE TABLE IF NOT EXISTS character_hobbies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL REFERENCES character_profiles(entity_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    proficiency REAL,
    frequency TEXT,
    enjoyment REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(entity_id, name)
);

CREATE TABLE IF NOT EXISTS character_habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL REFERENCES character_profiles(entity_id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    frequency TEXT,
    strength REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(entity_id, name)
);

CREATE TABLE IF NOT EXISTS character_routines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL REFERENCES character_profiles(entity_id) ON DELETE CASCADE,
    routine_key TEXT NOT NULL,
    daypart TEXT,
    sequence_index INTEGER NOT NULL DEFAULT 0,
    activity TEXT NOT NULL,
    conditions_json TEXT NOT NULL DEFAULT '{}',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(entity_id, routine_key, sequence_index)
);

CREATE TABLE IF NOT EXISTS character_skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id TEXT NOT NULL REFERENCES character_profiles(entity_id) ON DELETE CASCADE,
    skill_key TEXT NOT NULL,
    category TEXT,
    score REAL,
    tier TEXT,
    experience REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    UNIQUE(entity_id, skill_key)
);

CREATE TABLE IF NOT EXISTS character_relationship_state (
    source_entity_id TEXT NOT NULL REFERENCES character_profiles(entity_id) ON DELETE CASCADE,
    target_entity_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    relationship_type TEXT,
    trust REAL,
    warmth REAL,
    attachment REAL,
    tension REAL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(source_entity_id, target_entity_id)
);

CREATE TABLE IF NOT EXISTS ai_providers (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    adapter_type TEXT NOT NULL,
    base_url TEXT,
    credential_ref TEXT,
    enabled INTEGER NOT NULL DEFAULT 0 CHECK(enabled IN (0, 1)),
    config_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_models (
    provider_id TEXT NOT NULL REFERENCES ai_providers(id) ON DELETE CASCADE,
    model_id TEXT NOT NULL,
    display_name TEXT NOT NULL,
    capabilities_json TEXT NOT NULL DEFAULT '{}',
    context_window INTEGER,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0, 1)),
    last_seen_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(provider_id, model_id)
);

CREATE TABLE IF NOT EXISTS ai_bindings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope_type TEXT NOT NULL CHECK(scope_type IN ('global','character','engine','task')),
    scope_id TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'default',
    provider_id TEXT NOT NULL REFERENCES ai_providers(id),
    model_id TEXT NOT NULL,
    parameters_json TEXT NOT NULL DEFAULT '{}',
    enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scope_type, scope_id, role),
    FOREIGN KEY(provider_id, model_id) REFERENCES ai_models(provider_id, model_id)
);

CREATE TABLE IF NOT EXISTS ai_catalog_sync (
    provider_id TEXT PRIMARY KEY REFERENCES ai_providers(id) ON DELETE CASCADE,
    last_refresh_at TEXT,
    status TEXT NOT NULL DEFAULT 'never',
    error_text TEXT,
    model_count INTEGER NOT NULL DEFAULT 0
);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    db_path = Path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    migrate_composition_schema(conn)
    migrate_memory_schema(conn)
    migrate_mind_schema(conn)
    migrate_world_input_schema(conn)
    migrate_commitment_schema(conn)
    migrate_economy_schema(conn)
    migrate_environment_schema(conn)
    migrate_information_schema(conn)
    migrate_creation_sandbox_schema(conn)
    conn.execute(
        "INSERT INTO schema_meta(key, value) VALUES('schema_version', ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


def get_runtime_state(conn: sqlite3.Connection) -> dict[str, object]:
    rows = conn.execute("SELECT key, value_json FROM runtime_state ORDER BY key").fetchall()
    return {row["key"]: json.loads(row["value_json"]) for row in rows}

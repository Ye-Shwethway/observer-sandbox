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

SCHEMA_VERSION = 20

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
    sensitivity TEXT NOT NULL DEFAULT 'public' CHECK(sensitivity IN ('public','owner_only','secret')),
    mutable_by TEXT NOT NULL DEFAULT 'creator' CHECK(mutable_by IN ('creator','simulation','derived','none')),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS character_profiles (
    entity_id TEXT PRIMARY KEY REFERENCES entities(id) ON DELETE CASCADE,
    status TEXT NOT NULL DEFAULT 'active',
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
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(entity_id, field_key)
);

CREATE TABLE IF NOT EXISTS ai_providers (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    enabled INTEGER NOT NULL DEFAULT 0 CHECK(enabled IN (0,1)),
    base_url TEXT,
    api_key_env TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_models (
    provider_id TEXT NOT NULL REFERENCES ai_providers(id) ON DELETE CASCADE,
    model_id TEXT NOT NULL,
    display_name TEXT NOT NULL,
    active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(provider_id, model_id)
);

CREATE TABLE IF NOT EXISTS ai_bindings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    scope_type TEXT NOT NULL,
    scope_id TEXT NOT NULL,
    role TEXT NOT NULL,
    provider_id TEXT NOT NULL REFERENCES ai_providers(id),
    model_id TEXT NOT NULL,
    parameters_json TEXT NOT NULL DEFAULT '{}',
    enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN (0,1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(scope_type, scope_id, role),
    FOREIGN KEY(provider_id, model_id) REFERENCES ai_models(provider_id, model_id)
);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    migrate_memory_schema(conn)
    migrate_mind_schema(conn)
    migrate_world_input_schema(conn)
    migrate_environment_schema(conn)
    migrate_commitment_schema(conn)
    migrate_economy_schema(conn)
    migrate_information_schema(conn)
    migrate_composition_schema(conn)
    migrate_creation_sandbox_schema(conn)
    conn.execute(
        "INSERT INTO schema_meta(key,value) VALUES('schema_version',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


def json_value(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


__all__ = ["SCHEMA_VERSION", "connect", "json_value", "migrate"]
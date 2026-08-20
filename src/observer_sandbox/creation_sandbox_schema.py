from __future__ import annotations

import sqlite3

from .creator_studio_schema import migrate_creator_studio_schema
from .sandbox_character_facets import migrate_sandbox_character_facets_schema
from .sandbox_representation import migrate_sandbox_representation_schema


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS creation_sandboxes (
    sandbox_id TEXT PRIMARY KEY,
    label TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','archived')),
    revision INTEGER NOT NULL DEFAULT 1 CHECK(revision >= 1),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS creation_sandbox_objects (
    object_id TEXT PRIMARY KEY,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    creation_type TEXT NOT NULL,
    schema_version INTEGER NOT NULL,
    lifecycle_status TEXT NOT NULL DEFAULT 'active' CHECK(lifecycle_status IN ('active','archived')),
    identity_json TEXT NOT NULL DEFAULT '{}',
    properties_json TEXT NOT NULL DEFAULT '{}',
    relationships_json TEXT NOT NULL DEFAULT '[]',
    capabilities_json TEXT NOT NULL DEFAULT '[]',
    provenance_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_creation_sandbox_objects_scope
ON creation_sandbox_objects(sandbox_id, creation_type, lifecycle_status);

CREATE TABLE IF NOT EXISTS creation_sandbox_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    source_object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL,
    target_object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sandbox_id, source_object_id, relation_type, target_object_id)
);

CREATE TABLE IF NOT EXISTS creation_sandbox_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    object_id TEXT REFERENCES creation_sandbox_objects(object_id) ON DELETE SET NULL,
    event_type TEXT NOT NULL,
    payload_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS creation_sandbox_notification_state (
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN (0,1)),
    last_event_id INTEGER NOT NULL DEFAULT 0 CHECK(last_event_id >= 0),
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(sandbox_id,user_id)
);

CREATE TABLE IF NOT EXISTS creation_sandbox_runtime (
    sandbox_id TEXT PRIMARY KEY REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    sim_time TEXT,
    speed REAL NOT NULL DEFAULT 1.0 CHECK(speed > 0 AND speed <= 3600),
    paused INTEGER NOT NULL DEFAULT 1 CHECK(paused IN (0,1)),
    pause_started_wall_time REAL,
    runtime_status TEXT NOT NULL DEFAULT 'stopped' CHECK(runtime_status IN ('stopped','ready','running')),
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS creation_sandbox_actor_runtime (
    object_id TEXT PRIMARY KEY REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    activation_status TEXT NOT NULL DEFAULT 'created' CHECK(activation_status IN ('created','configured','runtime_ready','running','stopped')),
    current_location_object_id TEXT REFERENCES creation_sandbox_objects(object_id) ON DELETE SET NULL,
    autonomy_enabled INTEGER NOT NULL DEFAULT 0 CHECK(autonomy_enabled IN (0,1)),
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_creation_sandbox_actor_runtime_scope
ON creation_sandbox_actor_runtime(sandbox_id, activation_status);

CREATE TABLE IF NOT EXISTS creation_sandbox_ai_bindings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'cognition',
    provider_id TEXT NOT NULL REFERENCES ai_providers(id),
    model_id TEXT NOT NULL,
    parameters_json TEXT NOT NULL DEFAULT '{}',
    enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN (0,1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sandbox_id, object_id, role),
    FOREIGN KEY(provider_id, model_id) REFERENCES ai_models(provider_id, model_id)
);

CREATE TABLE IF NOT EXISTS creation_sandbox_runtime_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    character_object_id TEXT NOT NULL REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    action_key TEXT NOT NULL,
    source_object_id TEXT REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    enabled INTEGER NOT NULL DEFAULT 1 CHECK(enabled IN (0,1)),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sandbox_id, character_object_id, action_key, source_object_id)
);

CREATE TABLE IF NOT EXISTS creation_sandbox_item_definitions (
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    definition_key TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    name TEXT NOT NULL,
    kind TEXT NOT NULL,
    description TEXT NOT NULL,
    stackable INTEGER NOT NULL CHECK(stackable IN (0,1)),
    mobility TEXT NOT NULL CHECK(mobility IN ('movable','fixed')),
    capabilities_json TEXT NOT NULL DEFAULT '[]',
    tags_json TEXT NOT NULL DEFAULT '[]',
    modules_json TEXT NOT NULL DEFAULT '{}',
    requirements_json TEXT NOT NULL DEFAULT '{}',
    derived_json TEXT NOT NULL DEFAULT '{}',
    provenance_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(sandbox_id, definition_key)
);

CREATE TABLE IF NOT EXISTS creation_sandbox_item_instances (
    object_id TEXT PRIMARY KEY REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    definition_key TEXT NOT NULL,
    instance_mode TEXT NOT NULL CHECK(instance_mode IN ('unique','stack')),
    quantity REAL,
    unit TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(sandbox_id, definition_key)
        REFERENCES creation_sandbox_item_definitions(sandbox_id, definition_key)
        ON DELETE RESTRICT
);

CREATE INDEX IF NOT EXISTS idx_creation_sandbox_item_instances_definition
ON creation_sandbox_item_instances(sandbox_id, definition_key);

CREATE TABLE IF NOT EXISTS creation_sandbox_item_economic_profiles (
    object_id TEXT PRIMARY KEY REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    classification TEXT NOT NULL,
    policy_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS creation_sandbox_location_profiles (
    object_id TEXT PRIMARY KEY REFERENCES creation_sandbox_objects(object_id) ON DELETE CASCADE,
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    location_key TEXT NOT NULL,
    schema_version TEXT NOT NULL,
    kind TEXT NOT NULL,
    source_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(sandbox_id, location_key)
);

CREATE INDEX IF NOT EXISTS idx_creation_sandbox_location_profiles_scope
ON creation_sandbox_location_profiles(sandbox_id, kind);
"""


def migrate_creation_sandbox_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    migrate_sandbox_representation_schema(conn)
    migrate_sandbox_character_facets_schema(conn)
    migrate_creator_studio_schema(conn)


__all__ = ["migrate_creation_sandbox_schema"]
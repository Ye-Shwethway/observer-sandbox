from __future__ import annotations

import sqlite3


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
"""


def migrate_creation_sandbox_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)


__all__ = ["migrate_creation_sandbox_schema"]

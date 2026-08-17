from __future__ import annotations

import sqlite3


INFORMATION_SCHEMA_VERSION = 1

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS information_schema_meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS information_sources (
    source_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    credibility TEXT NOT NULL DEFAULT 'unknown',
    provenance_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS information_items (
    item_id TEXT PRIMARY KEY,
    item_type TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL DEFAULT '',
    source_id TEXT REFERENCES information_sources(source_id) ON DELETE SET NULL,
    published_at TEXT,
    provider_id TEXT,
    provider_ref TEXT,
    source_url TEXT,
    language TEXT,
    verification_status TEXT NOT NULL DEFAULT 'reported',
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_information_items_published
    ON information_items(published_at DESC, item_id);
CREATE INDEX IF NOT EXISTS idx_information_items_provider
    ON information_items(provider_id, provider_ref);

CREATE TABLE IF NOT EXISTS media_publications (
    publication_id TEXT PRIMARY KEY,
    medium TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL DEFAULT '',
    publisher_source_id TEXT REFERENCES information_sources(source_id) ON DELETE SET NULL,
    available_from TEXT NOT NULL,
    available_until TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('draft','active','expired','retired')),
    editorial_provider_id TEXT,
    editorial_model_id TEXT,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS media_publication_items (
    publication_id TEXT NOT NULL REFERENCES media_publications(publication_id) ON DELETE CASCADE,
    item_id TEXT NOT NULL REFERENCES information_items(item_id) ON DELETE CASCADE,
    ordinal INTEGER NOT NULL,
    PRIMARY KEY(publication_id, item_id),
    UNIQUE(publication_id, ordinal)
);

CREATE TABLE IF NOT EXISTS media_devices (
    entity_id TEXT PRIMARY KEY REFERENCES entities(id) ON DELETE CASCADE,
    device_type TEXT NOT NULL,
    channels_json TEXT NOT NULL DEFAULT '[]',
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active','inactive','retired')),
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""


def migrate_information_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    conn.execute(
        "INSERT INTO information_schema_meta(key, value) VALUES('schema_version', ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(INFORMATION_SCHEMA_VERSION),),
    )
    conn.commit()

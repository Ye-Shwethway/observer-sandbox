from __future__ import annotations

import json
import sqlite3
from pathlib import Path

SCHEMA_VERSION = 1

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
    conn.execute(
        "INSERT INTO schema_meta(key, value) VALUES('schema_version', ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(SCHEMA_VERSION),),
    )
    conn.commit()


def get_runtime_state(conn: sqlite3.Connection) -> dict[str, object]:
    rows = conn.execute("SELECT key, value_json FROM runtime_state ORDER BY key").fetchall()
    return {row["key"]: json.loads(row["value_json"]) for row in rows}

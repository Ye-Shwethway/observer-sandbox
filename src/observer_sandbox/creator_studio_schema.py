from __future__ import annotations

import sqlite3


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS creation_sandbox_drafts (
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location')),
    draft_mode TEXT NOT NULL CHECK(draft_mode IN ('manual','ai_generated')),
    prompt_text TEXT,
    proposal_json TEXT NOT NULL,
    revision INTEGER NOT NULL DEFAULT 1 CHECK(revision >= 1),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(sandbox_id, user_id)
);
"""


def migrate_creator_studio_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)


__all__ = ["migrate_creator_studio_schema"]

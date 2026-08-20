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

-- Pending Telegram input is presentation/session state, not a staged universe object.
-- expected_input remains the coarse transport kind ('name' or free-form 'description').
-- input_target optionally identifies the exact manual draft field/collection receiving
-- that free-form input without overloading the constrained transport column.
CREATE TABLE IF NOT EXISTS creation_sandbox_studio_sessions (
    sandbox_id TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location')),
    input_mode TEXT NOT NULL CHECK(input_mode IN ('manual','ai_generated')),
    expected_input TEXT NOT NULL CHECK(expected_input IN ('name','description')),
    input_target TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(sandbox_id, user_id)
);
"""


def _ensure_session_input_target(conn: sqlite3.Connection) -> None:
    columns = {
        str(row["name"] if isinstance(row, sqlite3.Row) else row[1])
        for row in conn.execute("PRAGMA table_info(creation_sandbox_studio_sessions)").fetchall()
    }
    if "input_target" not in columns:
        conn.execute("ALTER TABLE creation_sandbox_studio_sessions ADD COLUMN input_target TEXT")


def migrate_creator_studio_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    _ensure_session_input_target(conn)


__all__ = ["migrate_creator_studio_schema"]

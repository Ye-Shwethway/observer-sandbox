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
-- expected_input is an extensible presentation target. Initial creation uses
-- 'name'/'description'; guided editors may use namespaced targets such as
-- 'manual-field:<field_key>' or 'manual-collection:<collection>'.
CREATE TABLE IF NOT EXISTS creation_sandbox_studio_sessions (
    sandbox_id TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location')),
    input_mode TEXT NOT NULL CHECK(input_mode IN ('manual','ai_generated')),
    expected_input TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(sandbox_id, user_id)
);
"""


def _relax_legacy_expected_input_check(conn: sqlite3.Connection) -> None:
    row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='creation_sandbox_studio_sessions'"
    ).fetchone()
    sql = str(row["sql"] if isinstance(row, sqlite3.Row) else row[0]) if row else ""
    if "expected_input IN ('name','description')" not in sql:
        return

    conn.execute("ALTER TABLE creation_sandbox_studio_sessions RENAME TO creation_sandbox_studio_sessions_legacy")
    conn.executescript(
        """
        CREATE TABLE creation_sandbox_studio_sessions (
            sandbox_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location')),
            input_mode TEXT NOT NULL CHECK(input_mode IN ('manual','ai_generated')),
            expected_input TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(sandbox_id, user_id)
        );
        INSERT INTO creation_sandbox_studio_sessions(
            sandbox_id,user_id,creation_type,input_mode,expected_input,created_at,updated_at
        )
        SELECT sandbox_id,user_id,creation_type,input_mode,expected_input,created_at,updated_at
        FROM creation_sandbox_studio_sessions_legacy;
        DROP TABLE creation_sandbox_studio_sessions_legacy;
        """
    )


def migrate_creator_studio_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    _relax_legacy_expected_input_check(conn)


__all__ = ["migrate_creator_studio_schema"]

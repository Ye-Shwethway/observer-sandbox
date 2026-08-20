from __future__ import annotations

import sqlite3


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS creation_sandbox_drafts (
    sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL,
    creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location','item')),
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
-- 'name'/'description'; guided editors use namespaced targets. prompt_chat_id and
-- prompt_message_id identify the temporary Telegram input card so it can be
-- removed after the pending input is consumed instead of becoming stale UI.
CREATE TABLE IF NOT EXISTS creation_sandbox_studio_sessions (
    sandbox_id TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location','item')),
    input_mode TEXT NOT NULL CHECK(input_mode IN ('manual','ai_generated')),
    expected_input TEXT NOT NULL,
    prompt_chat_id INTEGER,
    prompt_message_id INTEGER,
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
            creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location','item')),
            input_mode TEXT NOT NULL CHECK(input_mode IN ('manual','ai_generated')),
            expected_input TEXT NOT NULL,
            prompt_chat_id INTEGER,
            prompt_message_id INTEGER,
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


def _expand_creation_types(conn: sqlite3.Connection) -> None:
    draft_row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='creation_sandbox_drafts'"
    ).fetchone()
    draft_sql = str(draft_row["sql"] if isinstance(draft_row, sqlite3.Row) else draft_row[0]) if draft_row else ""
    if "creation_type IN ('character','location')" in draft_sql:
        conn.execute("ALTER TABLE creation_sandbox_drafts RENAME TO creation_sandbox_drafts_legacy")
        conn.executescript(
            """
            CREATE TABLE creation_sandbox_drafts (
                sandbox_id TEXT NOT NULL REFERENCES creation_sandboxes(sandbox_id) ON DELETE CASCADE,
                user_id INTEGER NOT NULL,
                creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location','item')),
                draft_mode TEXT NOT NULL CHECK(draft_mode IN ('manual','ai_generated')),
                prompt_text TEXT,
                proposal_json TEXT NOT NULL,
                revision INTEGER NOT NULL DEFAULT 1 CHECK(revision >= 1),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(sandbox_id, user_id)
            );
            INSERT INTO creation_sandbox_drafts(
                sandbox_id,user_id,creation_type,draft_mode,prompt_text,proposal_json,revision,created_at,updated_at
            )
            SELECT sandbox_id,user_id,creation_type,draft_mode,prompt_text,proposal_json,revision,created_at,updated_at
            FROM creation_sandbox_drafts_legacy;
            DROP TABLE creation_sandbox_drafts_legacy;
            """
        )

    session_row = conn.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name='creation_sandbox_studio_sessions'"
    ).fetchone()
    session_sql = str(session_row["sql"] if isinstance(session_row, sqlite3.Row) else session_row[0]) if session_row else ""
    if "creation_type IN ('character','location')" in session_sql:
        conn.execute("ALTER TABLE creation_sandbox_studio_sessions RENAME TO creation_sandbox_studio_sessions_legacy_type")
        conn.executescript(
            """
            CREATE TABLE creation_sandbox_studio_sessions (
                sandbox_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location','item')),
                input_mode TEXT NOT NULL CHECK(input_mode IN ('manual','ai_generated')),
                expected_input TEXT NOT NULL,
                prompt_chat_id INTEGER,
                prompt_message_id INTEGER,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(sandbox_id, user_id)
            );
            INSERT INTO creation_sandbox_studio_sessions(
                sandbox_id,user_id,creation_type,input_mode,expected_input,prompt_chat_id,prompt_message_id,created_at,updated_at
            )
            SELECT sandbox_id,user_id,creation_type,input_mode,expected_input,prompt_chat_id,prompt_message_id,created_at,updated_at
            FROM creation_sandbox_studio_sessions_legacy_type;
            DROP TABLE creation_sandbox_studio_sessions_legacy_type;
            """
        )


def _ensure_prompt_message_columns(conn: sqlite3.Connection) -> None:
    columns = {
        str(row["name"] if isinstance(row, sqlite3.Row) else row[1])
        for row in conn.execute("PRAGMA table_info(creation_sandbox_studio_sessions)").fetchall()
    }
    if "prompt_chat_id" not in columns:
        conn.execute("ALTER TABLE creation_sandbox_studio_sessions ADD COLUMN prompt_chat_id INTEGER")
    if "prompt_message_id" not in columns:
        conn.execute("ALTER TABLE creation_sandbox_studio_sessions ADD COLUMN prompt_message_id INTEGER")


def migrate_creator_studio_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA_SQL)
    _relax_legacy_expected_input_check(conn)
    _ensure_prompt_message_columns(conn)
    _expand_creation_types(conn)


__all__ = ["migrate_creator_studio_schema"]

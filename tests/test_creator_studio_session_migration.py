import sqlite3

from observer_sandbox.creator_studio_schema import migrate_creator_studio_schema


def test_legacy_session_check_is_relaxed_without_losing_pending_input(tmp_path):
    db = tmp_path / "legacy-studio.sqlite3"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    try:
        conn.executescript(
            """
            CREATE TABLE creation_sandbox_studio_sessions (
                sandbox_id TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                creation_type TEXT NOT NULL CHECK(creation_type IN ('character','location')),
                input_mode TEXT NOT NULL CHECK(input_mode IN ('manual','ai_generated')),
                expected_input TEXT NOT NULL CHECK(expected_input IN ('name','description')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(sandbox_id, user_id)
            );
            INSERT INTO creation_sandbox_studio_sessions(
                sandbox_id,user_id,creation_type,input_mode,expected_input
            ) VALUES('creator-default',42,'character','manual','name');
            """
        )
        before = dict(
            conn.execute(
                "SELECT sandbox_id,user_id,creation_type,input_mode,expected_input "
                "FROM creation_sandbox_studio_sessions WHERE user_id=42"
            ).fetchone()
        )

        migrate_creator_studio_schema(conn)

        after = dict(
            conn.execute(
                "SELECT sandbox_id,user_id,creation_type,input_mode,expected_input "
                "FROM creation_sandbox_studio_sessions WHERE user_id=42"
            ).fetchone()
        )
        assert after == before

        conn.execute(
            "UPDATE creation_sandbox_studio_sessions SET expected_input=? WHERE user_id=42",
            ('manual-field:identity.full_name',),
        )
        conn.commit()
        assert conn.execute(
            "SELECT expected_input FROM creation_sandbox_studio_sessions WHERE user_id=42"
        ).fetchone()[0] == 'manual-field:identity.full_name'

        # Idempotence matters because migrate() runs on ordinary service startup.
        migrate_creator_studio_schema(conn)
        assert conn.execute(
            "SELECT expected_input FROM creation_sandbox_studio_sessions WHERE user_id=42"
        ).fetchone()[0] == 'manual-field:identity.full_name'
    finally:
        conn.close()

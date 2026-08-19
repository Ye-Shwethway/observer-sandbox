from observer_sandbox.creator_studio import manual_draft
from observer_sandbox.db import connect, migrate
from observer_sandbox.telegram_creator_studio import studio_callback_view


def _count_sandbox_objects(conn):
    return conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]


def test_approve_first_click_only_confirms_and_second_click_applies(tmp_path):
    db_path = tmp_path / "approval-confirmation.sqlite3"
    with connect(db_path) as conn:
        migrate(conn)
        draft = manual_draft(conn, 42, "location", "Test Ridge")
        assert draft["revision"] == 1
        before = _count_sandbox_objects(conn)

        text, keyboard = studio_callback_view(conn, 42, "sw:cs:approve")
        assert "CONFIRM SANDBOX APPROVAL" in text
        assert "Test Ridge" in text
        assert _count_sandbox_objects(conn) == before
        confirm = keyboard[0][0]["callback_data"]
        assert confirm == "sw:cs:approve:confirm:1"

        text, _keyboard = studio_callback_view(conn, 42, confirm)
        assert "SANDBOX CREATION APPROVED" in text
        assert _count_sandbox_objects(conn) == before + 1


def test_stale_confirmation_cannot_approve_changed_revision(tmp_path):
    db_path = tmp_path / "approval-stale.sqlite3"
    with connect(db_path) as conn:
        migrate(conn)
        manual_draft(conn, 42, "location", "First Ridge")
        text, keyboard = studio_callback_view(conn, 42, "sw:cs:approve")
        assert "CONFIRM SANDBOX APPROVAL" in text
        stale_confirm = keyboard[0][0]["callback_data"]

        # Replacing the active draft advances its revision and invalidates the old confirmation.
        changed = manual_draft(conn, 42, "location", "Second Ridge")
        assert changed["revision"] == 2
        before = _count_sandbox_objects(conn)

        text, _keyboard = studio_callback_view(conn, 42, stale_confirm)
        assert "Draft changed after confirmation" in text
        assert _count_sandbox_objects(conn) == before

from observer_sandbox.creation_sandbox import activate_creation_proposal
from observer_sandbox.creation_socket import build_creation_proposal
from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_sandbox_notifications import (
    dispatch_pending_sandbox_notifications,
    pending_sandbox_events,
    sandbox_notification_callback_view,
    sandbox_notifications_enabled,
)
from observer_sandbox.telegram_world_layers import world_layer_callback_view


def test_schema_v20_registers_isolated_notification_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert SCHEMA_VERSION == 20
        assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "20"
        assert conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='creation_sandbox_notification_state'"
        ).fetchone() is not None


def test_observer_feed_toggle_and_world_entry(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        _, keyboard = world_layer_callback_view(conn, "nav:sandbox")
        callbacks = {b["callback_data"] for row in keyboard for b in row}
        assert "sw:notif" in callbacks
        text, _ = world_layer_callback_view(conn, "sw:notif")
        assert "SANDBOX OBSERVER" in text
        assert sandbox_notifications_enabled(conn, 111) is True
        world_layer_callback_view(conn, "sw:notif:toggle")
        assert sandbox_notifications_enabled(conn, 111) is False


def test_pending_dispatch_is_cursor_based_and_does_not_touch_canonical_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before_entities = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        proposal = build_creation_proposal(
            "location",
            identity={"name": "Observer Test Cabin"},
            provenance_mode="manual",
            requested_by="test",
        )
        activate_creation_proposal(conn, proposal)
        assert pending_sandbox_events(conn, 111)
        sent = []
        count = dispatch_pending_sandbox_notifications(
            conn,
            111,
            send=lambda user_id, text: sent.append((user_id, text)),
        )
        assert count == 1
        assert sent and sent[0][0] == 111
        assert "SANDBOX UPDATE" in sent[0][1]
        assert "Creation approved" in sent[0][1]
        assert dispatch_pending_sandbox_notifications(
            conn,
            111,
            send=lambda user_id, text: sent.append((user_id, text)),
        ) == 0
        assert conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0] == before_entities


def test_mark_current_seen_suppresses_backlog(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        proposal = build_creation_proposal(
            "character",
            identity={"name": "Observer Test Character"},
            provenance_mode="manual",
            requested_by="test",
        )
        activate_creation_proposal(conn, proposal)
        assert pending_sandbox_events(conn, 111)
        sandbox_notification_callback_view(conn, 111, "sw:notif:seen")
        assert pending_sandbox_events(conn, 111) == []

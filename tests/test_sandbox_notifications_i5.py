from observer_sandbox.creation_sandbox import activate_creation_proposal
from observer_sandbox.creation_socket import build_creation_proposal
from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_sandbox_notifications import (
    dispatch_owner_sandbox_notifications,
    dispatch_pending_sandbox_notifications,
    pending_sandbox_events,
    sandbox_notification_callback_view,
    sandbox_notifications_enabled,
    set_sandbox_notifications,
)
from observer_sandbox.telegram_world_layers import world_layer_callback_view


def _create_location(conn, name):
    return activate_creation_proposal(
        conn,
        build_creation_proposal(
            "location",
            identity={"name": name},
            provenance_mode="manual",
            requested_by="test",
        ),
    )


def test_schema_v20_registers_isolated_notification_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert SCHEMA_VERSION == 20
        assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "20"
        assert conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='creation_sandbox_notification_state'"
        ).fetchone() is not None


def test_observer_feed_defaults_off_and_toggle_baselines_current_history(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        _create_location(conn, "Historical Cabin")
        _, keyboard = world_layer_callback_view(conn, "nav:sandbox")
        callbacks = {b["callback_data"] for row in keyboard for b in row}
        assert "sw:notif" in callbacks
        text, _ = world_layer_callback_view(conn, "sw:notif")
        assert "SANDBOX OBSERVER" in text
        assert "Historical Cabin" in text
        assert sandbox_notifications_enabled(conn, 111) is False
        assert pending_sandbox_events(conn, 111) == []
        world_layer_callback_view(conn, "sw:notif:toggle")
        assert sandbox_notifications_enabled(conn, 111) is True
        assert pending_sandbox_events(conn, 111) == []


def test_pending_dispatch_is_cursor_based_after_enable_and_does_not_touch_canonical_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before_entities = conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
        _create_location(conn, "Before Enable")
        assert set_sandbox_notifications(conn, 111, True) is True
        assert pending_sandbox_events(conn, 111) == []

        _create_location(conn, "Observer Test Cabin")
        assert len(pending_sandbox_events(conn, 111)) == 1
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
        assert "Observer Test Cabin" in sent[0][1]
        assert dispatch_pending_sandbox_notifications(
            conn,
            111,
            send=lambda user_id, text: sent.append((user_id, text)),
        ) == 0
        assert conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0] == before_entities


def test_transport_failure_keeps_event_pending(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_sandbox_notifications(conn, 111, True)
        _create_location(conn, "Retry Cabin")
        try:
            dispatch_pending_sandbox_notifications(
                conn,
                111,
                send=lambda user_id, text: (_ for _ in ()).throw(RuntimeError("network")),
            )
        except RuntimeError:
            pass
        assert len(pending_sandbox_events(conn, 111)) == 1


def test_owner_transport_respects_global_and_sandbox_preferences(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_BOT_TOKEN", "test-token")
    sent = []
    monkeypatch.setattr(
        "observer_sandbox.telegram_bot._send",
        lambda token, user_id, text, keyboard=None: sent.append((token, user_id, text)),
    )
    with connect(db) as conn:
        set_sandbox_notifications(conn, 111, True)
        _create_location(conn, "Transport Cabin")
        assert dispatch_owner_sandbox_notifications(conn) == 1
        assert sent == [("test-token", 111, sent[0][2])]
        assert "Transport Cabin" in sent[0][2]
        assert pending_sandbox_events(conn, 111) == []

        set_sandbox_notifications(conn, 111, False)
        _create_location(conn, "Muted Cabin")
        assert dispatch_owner_sandbox_notifications(conn) == 0
        assert len(sent) == 1


def test_mark_current_seen_suppresses_new_pending_events(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_sandbox_notifications(conn, 111, True)
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

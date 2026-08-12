from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_bot import _callback_view, _home_keyboard, _notifications_enabled, handle_command


def test_unauthorized_user_gets_only_identity_bootstrap(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.delenv("OBSERVER_TELEGRAM_OWNER_ID", raising=False)
    monkeypatch.delenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", raising=False)
    text = handle_command(db, user_id=12345, text="/start")
    assert "12345" in text
    assert "unauthorized" in text
    assert handle_command(db, user_id=12345, text="/status").startswith("Not authorized")


def test_owner_is_authorized_without_duplicate_allowlist_entry(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.delenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", raising=False)
    assert "Role: Owner" in handle_command(db, user_id=111, text="/whoami")
    assert "OBSERVER SANDBOX" in handle_command(db, user_id=111, text="/status")
    start = handle_command(db, user_id=111, text="/start")
    assert "OBSERVER HOME" in start
    assert "Access Owner" in start


def test_allowed_user_is_separate_non_owner_role(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222,333")
    assert "Role: Allowed" in handle_command(db, user_id=222, text="/whoami")
    assert "OBSERVER SANDBOX" in handle_command(db, user_id=222, text="/status")
    assert handle_command(db, user_id=444, text="/status").startswith("Not authorized")


def test_authorized_mvp_commands_and_controls(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "12345")
    status = handle_command(db, user_id=12345, text="/status")
    assert "OBSERVER SANDBOX" in status
    assert "01-05-2025 (Thursday) 07:00 AM" in status
    assert "Darian" in handle_command(db, user_id=12345, text="/darian")
    assert "Darian Home" in handle_command(db, user_id=12345, text="/home")
    assert "Recent Activity" in handle_command(db, user_id=12345, text="/history")
    assert "Paused     Yes" in handle_command(db, user_id=12345, text="/pause")
    assert "Paused     No" in handle_command(db, user_id=12345, text="/resume")
    assert "Speed      60.0x" in handle_command(db, user_id=12345, text="/speed 60")


def test_notifications_default_on_and_persist_per_user(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")
    with connect(db) as conn:
        assert _notifications_enabled(conn, 111) is True
        assert _notifications_enabled(conn, 222) is True
    assert "Notifications OFF" in handle_command(db, user_id=111, text="/notify off")
    with connect(db) as conn:
        assert _notifications_enabled(conn, 111) is False
        assert _notifications_enabled(conn, 222) is True
    assert "Notifications ON" in handle_command(db, user_id=111, text="/notion/on")
    assert "Notifications OFF" in handle_command(db, user_id=111, text="/notion/off")


def test_observer_home_uses_stable_inline_navigation(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    keyboard = _home_keyboard()
    assert keyboard[0][0]["callback_data"] == "nav:universe"
    assert keyboard[0][1]["callback_data"] == "nav:characters"
    with connect(db) as conn:
        text, universe_keyboard = _callback_view(conn, 111, "nav:universe")
        assert "UNIVERSE" in text
        assert any(button[0]["callback_data"].startswith("loc:room_") for button in universe_keyboard[:-1])
        chars_text, chars_keyboard = _callback_view(conn, 111, "nav:characters")
        assert "Darian Thorne" in chars_text
        assert chars_keyboard[0][0]["callback_data"] == "char:char_darian"

import os

from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_bot import handle_command


def test_unauthorized_user_gets_only_identity_bootstrap(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.delenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", raising=False)
    text = handle_command(db, user_id=12345, text="/start")
    assert "12345" in text
    assert "Authorization is not enabled" in text
    assert handle_command(db, user_id=12345, text="/status").startswith("Not authorized")


def test_authorized_mvp_commands_and_controls(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "12345")

    assert "Observer Sandbox" in handle_command(db, user_id=12345, text="/status")
    assert "Darian" in handle_command(db, user_id=12345, text="/darian")
    home = handle_command(db, user_id=12345, text="/home")
    assert "Darian Home" in home
    assert "Bedroom" in home
    assert "Recent history" not in handle_command(db, user_id=12345, text="/history")

    paused = handle_command(db, user_id=12345, text="/pause")
    assert "Paused: True" in paused
    resumed = handle_command(db, user_id=12345, text="/resume")
    assert "Paused: False" in resumed
    speed = handle_command(db, user_id=12345, text="/speed 60")
    assert "Speed: 60.0x" in speed

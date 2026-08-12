from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_bot import handle_command


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

    who = handle_command(db, user_id=111, text="/whoami")
    assert "Role: owner" in who
    assert "Observer Sandbox" in handle_command(db, user_id=111, text="/status")
    assert "Role: Owner" in handle_command(db, user_id=111, text="/start")


def test_allowed_user_is_separate_non_owner_role(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222,333")

    assert "Role: allowed" in handle_command(db, user_id=222, text="/whoami")
    assert "Observer Sandbox" in handle_command(db, user_id=222, text="/status")
    assert handle_command(db, user_id=444, text="/status").startswith("Not authorized")


def test_authorized_mvp_commands_and_controls(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
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

from __future__ import annotations

from pathlib import Path

from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_runtime_bot import _FILE_SENTINEL, handle_command


def test_runtime_logs_are_creator_only(tmp_path: Path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "456")

    denied = handle_command(db, user_id=456, text="/logs")
    assert "Creator authority required" in denied

    preview = handle_command(db, user_id=123, text="/logs 5")
    assert "RUNTIME DIAGNOSTICS" in preview
    assert "SQLite" in preview


def test_runtime_logs_can_export_txt(tmp_path: Path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")

    response = handle_command(db, user_id=123, text="/logs file 25")
    assert response.startswith(_FILE_SENTINEL)
    report_path = Path(response[len(_FILE_SENTINEL) :])
    try:
        text = report_path.read_text(encoding="utf-8")
        assert "OBSERVER SANDBOX RUNTIME DIAGNOSTICS" in text
        assert "STRUCTURED SNAPSHOT" in text
    finally:
        report_path.unlink(missing_ok=True)

from __future__ import annotations

from pathlib import Path

from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_runtime_bot import _FILE_SENTINEL, handle_command


def test_runtime_logs_are_creator_only_and_expose_focused_modes(tmp_path: Path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "456")

    denied = handle_command(db, user_id=456, text="/logs")
    assert "Creator authority required" in denied

    summary = handle_command(db, user_id=123, text="/logs")
    assert "ERROR SUMMARY" in summary
    assert "/logs errors" in summary
    assert "/logs system" in summary
    assert "/logs runtime" in summary

    errors = handle_command(db, user_id=123, text="/logs errors 5")
    assert "ERROR LOG" in errors

    runtime = handle_command(db, user_id=123, text="/logs runtime")
    assert "RUNTIME CONTEXT" in runtime
    assert "SQLite" in runtime


def test_runtime_logs_can_export_consolidated_txt(tmp_path: Path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")

    response = handle_command(db, user_id=123, text="/logs file 25")
    assert response.startswith(_FILE_SENTINEL)
    report_path = Path(response[len(_FILE_SENTINEL) :])
    try:
        text = report_path.read_text(encoding="utf-8")
        assert "OBSERVER SANDBOX DIAGNOSTICS V2" in text
        assert "ERROR SUMMARY" in text
        assert "SYSTEM SERVICE STATE" in text
        assert "APPLICATION WARNINGS / ERRORS / TRACEBACKS" in text
        assert "RECENT SYSTEM JOURNAL" in text
        assert "CONCISE RUNTIME CONTEXT" in text
        assert "cognition_context_snapshots_v1" not in text
    finally:
        report_path.unlink(missing_ok=True)

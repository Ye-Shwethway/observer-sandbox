from __future__ import annotations

from pathlib import Path

from observer_sandbox.runtime import initialize
from observer_sandbox import runtime_diagnostics as diagnostics


def test_runtime_diagnostics_read_production_shape_without_mutation(tmp_path: Path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    log_path = tmp_path / "runtime.log"
    log_path.write_text(
        "2026-08-17T00:00:00Z INFO observer_sandbox.runtime MainThread service.main:1 service_ready\n"
        "2026-08-17T00:00:01Z ERROR observer_sandbox.runtime MainThread service.main:2 service_loop_fatal\n"
        "Traceback (most recent call last):\nValueError: boom\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(diagnostics, "RUNTIME_LOG_PATH", log_path)
    monkeypatch.setattr(
        diagnostics,
        "collect_system_snapshot",
        lambda **_: {
            "properties": {
                "ActiveState": "active",
                "SubState": "running",
                "Result": "success",
                "MainPID": "123",
                "NRestarts": "0",
                "ExecMainCode": "0",
                "ExecMainStatus": "0",
            },
            "systemctl_error": None,
            "journal": "journal-line",
            "journal_error": None,
        },
    )

    snapshot = diagnostics.collect_runtime_snapshot(db)
    assert snapshot["db_exists"] is True
    assert snapshot["sqlite_quick_check"] == "ok"
    assert snapshot["schema_version"] is not None
    assert set(snapshot["runtime_state"]).issubset({"paused", "speed"})
    assert isinstance(snapshot["recent_runtime_events"], list)

    report = diagnostics.build_diagnostics_report(db, lines=20)
    assert "OBSERVER SANDBOX DIAGNOSTICS V2" in report
    assert "ERROR SUMMARY" in report
    assert "SYSTEM SERVICE STATE" in report
    assert "APPLICATION WARNINGS / ERRORS / TRACEBACKS" in report
    assert "ValueError: boom" in report
    assert "RECENT SYSTEM JOURNAL" in report
    assert "CONCISE RUNTIME CONTEXT" in report
    assert "cognition_context_snapshots_v1" not in report
    assert "OBSERVER_TELEGRAM_BOT_TOKEN" not in report


def test_runtime_log_tail_is_bounded_and_error_blocks_keep_traceback(tmp_path: Path):
    log_path = tmp_path / "runtime.log"
    log_path.write_text(
        "one\n"
        "2026-08-17T00:00:01Z ERROR observer_sandbox.runtime MainThread service.main:2 failed\n"
        "Traceback (most recent call last):\n"
        "RuntimeError: diagnostic-test\n"
        "2026-08-17T00:00:02Z INFO observer_sandbox.runtime MainThread service.main:3 recovered\n",
        encoding="utf-8",
    )

    assert diagnostics.tail_runtime_log(2, log_path) == ["RuntimeError: diagnostic-test", "2026-08-17T00:00:02Z INFO observer_sandbox.runtime MainThread service.main:3 recovered"]
    errors = diagnostics._error_blocks(20, log_path)
    assert any("ERROR" in line for line in errors)
    assert "RuntimeError: diagnostic-test" in errors


def test_system_snapshot_gracefully_preserves_systemd_and_journal_failures(monkeypatch):
    responses = iter(
        [
            {"ok": False, "returncode": 1, "stdout": "", "stderr": "systemd unavailable"},
            {"ok": False, "returncode": 1, "stdout": "", "stderr": "journal permission denied"},
        ]
    )
    monkeypatch.setattr(diagnostics, "_run_readonly", lambda *args, **kwargs: next(responses))

    snapshot = diagnostics.collect_system_snapshot()
    assert snapshot["systemctl_ok"] is False
    assert snapshot["journal_ok"] is False
    assert "systemd unavailable" in snapshot["systemctl_error"]
    assert "permission denied" in snapshot["journal_error"]

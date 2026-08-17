from __future__ import annotations

from pathlib import Path

from observer_sandbox.runtime import initialize
from observer_sandbox.runtime_diagnostics import (
    build_diagnostics_report,
    collect_runtime_snapshot,
    tail_runtime_log,
)


def test_runtime_diagnostics_read_production_shape_without_mutation(tmp_path: Path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    snapshot = collect_runtime_snapshot(db)

    assert snapshot["db_exists"] is True
    assert snapshot["sqlite_quick_check"] == "ok"
    assert snapshot["schema_version"] is not None
    assert isinstance(snapshot["runtime_state"], dict)
    assert isinstance(snapshot["recent_runtime_events"], list)

    report = build_diagnostics_report(db, lines=10)
    assert "OBSERVER SANDBOX RUNTIME DIAGNOSTICS" in report
    assert "STRUCTURED SNAPSHOT" in report
    assert "RUNTIME LOG" in report
    assert "OBSERVER_TELEGRAM_BOT_TOKEN" not in report


def test_runtime_log_tail_is_bounded_and_readable(tmp_path: Path):
    log_path = tmp_path / "runtime.log"
    log_path.write_text("one\ntwo\nthree\n", encoding="utf-8")

    assert tail_runtime_log(2, log_path) == ["two", "three"]

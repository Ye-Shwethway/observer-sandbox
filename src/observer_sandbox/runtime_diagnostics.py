from __future__ import annotations

import json
import logging
import logging.handlers
import os
import sqlite3
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
RUNTIME_LOG_PATH = Path(os.environ.get("OBSERVER_RUNTIME_LOG", "/var/lib/observer-sandbox/runtime.log"))
_LOGGER_NAME = "observer_sandbox.runtime"
_CONFIGURED = False


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def configure_runtime_logging(path: str | Path | None = None) -> logging.Logger:
    """Install a bounded app-owned production log without depending on journald access."""
    global _CONFIGURED
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    if _CONFIGURED:
        return logger

    target = Path(path) if path is not None else RUNTIME_LOG_PATH
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        handler = logging.handlers.RotatingFileHandler(
            target,
            maxBytes=2 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8",
        )
        formatter = logging.Formatter(
            "%(asctime)sZ %(levelname)s %(threadName)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        formatter.converter = time.gmtime
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except OSError:
        # Diagnostics must never prevent the runtime from starting.
        logger.addHandler(logging.NullHandler())

    previous_excepthook = sys.excepthook

    def _sys_hook(exc_type, exc_value, exc_traceback) -> None:
        try:
            logger.critical("uncaught_main_exception", exc_info=(exc_type, exc_value, exc_traceback))
        finally:
            previous_excepthook(exc_type, exc_value, exc_traceback)

    sys.excepthook = _sys_hook

    previous_thread_hook = threading.excepthook

    def _thread_hook(args: threading.ExceptHookArgs) -> None:
        try:
            logger.critical(
                "uncaught_thread_exception thread=%s",
                getattr(args.thread, "name", "unknown"),
                exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
            )
        finally:
            previous_thread_hook(args)

    threading.excepthook = _thread_hook
    _CONFIGURED = True
    logger.info("runtime_logging_ready path=%s pid=%s", target, os.getpid())
    return logger


def runtime_logger() -> logging.Logger:
    return configure_runtime_logging()


def tail_runtime_log(lines: int = 40, path: str | Path | None = None) -> list[str]:
    limit = max(1, min(int(lines), 2000))
    target = Path(path) if path is not None else RUNTIME_LOG_PATH
    if not target.exists():
        return []
    try:
        content = target.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    return content[-limit:]


def _safe_json(value: str | None) -> Any:
    if value is None:
        return None
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return {"unparsed": str(value)[:500]}


def collect_runtime_snapshot(db_path: str | Path | None = None) -> dict[str, Any]:
    db = Path(db_path) if db_path is not None else DEFAULT_DB_PATH
    snapshot: dict[str, Any] = {
        "generated_utc": _utc_stamp(),
        "pid": os.getpid(),
        "python": sys.version.split()[0],
        "cwd": os.getcwd(),
        "db_path": str(db),
        "db_exists": db.exists(),
        "db_size_bytes": db.stat().st_size if db.exists() else None,
        "log_path": str(RUNTIME_LOG_PATH),
        "log_exists": RUNTIME_LOG_PATH.exists(),
        "log_size_bytes": RUNTIME_LOG_PATH.stat().st_size if RUNTIME_LOG_PATH.exists() else None,
    }
    if not db.exists():
        return snapshot

    uri = f"file:{db}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            check = conn.execute("PRAGMA quick_check").fetchone()
            snapshot["sqlite_quick_check"] = check[0] if check else None

            version = conn.execute(
                "SELECT value FROM schema_meta WHERE key=?",
                ("schema_version",),
            ).fetchone()
            snapshot["schema_version"] = version[0] if version else None

            runtime_rows = conn.execute(
                "SELECT key,value_json FROM runtime_state ORDER BY key"
            ).fetchall()
            snapshot["runtime_state"] = {
                str(row["key"]): _safe_json(row["value_json"]) for row in runtime_rows
            }

            try:
                actor_rows = conn.execute(
                    """SELECT actor_id,autonomy_enabled,autonomy_mode,pending_action_id,
                              retry_failures,retry_last_error,updated_at
                       FROM actor_runtime ORDER BY actor_id"""
                ).fetchall()
                snapshot["actor_runtime"] = [dict(row) for row in actor_rows]
            except sqlite3.Error as exc:
                snapshot["actor_runtime_error"] = f"{type(exc).__name__}: {exc}"

            event_rows = conn.execute(
                """SELECT id,sim_time,actor_id,event_type,payload_json,created_at
                   FROM events
                   WHERE event_type IN (
                       'autonomy_error','autonomy_recovery','cognition_provider_recovered',
                       'action_started','action_completed'
                   )
                   ORDER BY id DESC LIMIT 30"""
            ).fetchall()
            snapshot["recent_runtime_events"] = [
                {
                    "id": row["id"],
                    "sim_time": row["sim_time"],
                    "actor_id": row["actor_id"],
                    "event_type": row["event_type"],
                    "payload": _safe_json(row["payload_json"]),
                    "created_at": row["created_at"],
                }
                for row in event_rows
            ]
        finally:
            conn.close()
    except Exception as exc:
        snapshot["db_error"] = f"{type(exc).__name__}: {exc}"
    return snapshot


def format_log_preview(db_path: str | Path | None = None, *, lines: int = 30) -> str:
    snapshot = collect_runtime_snapshot(db_path)
    log_lines = tail_runtime_log(lines)
    state = snapshot.get("runtime_state") or {}
    paused = state.get("paused")
    speed = state.get("speed")
    latest_events = snapshot.get("recent_runtime_events") or []
    latest_error = next((e for e in latest_events if e.get("event_type") == "autonomy_error"), None)
    text = [
        "🧰 RUNTIME DIAGNOSTICS",
        "━━━━━━━━━━━━━━━━━━",
        f"🟢 Process PID · {snapshot.get('pid')}",
        f"💾 SQLite · {snapshot.get('sqlite_quick_check', 'unknown')}",
        f"🧬 Schema · {snapshot.get('schema_version', 'unknown')}",
        f"⏸ Paused · {paused}",
        f"⚡ Speed · {speed}",
        f"📄 Log · {snapshot.get('log_size_bytes') or 0} bytes",
    ]
    if snapshot.get("db_error"):
        text.append(f"❌ DB · {snapshot['db_error']}")
    if latest_error:
        payload = latest_error.get("payload") or {}
        text.extend([
            "",
            "⚠️ Latest autonomy error",
            f"• Sim time: {latest_error.get('sim_time')}",
            f"• Type: {payload.get('error_type') or 'unknown'}",
            f"• Stage: {payload.get('stage') or 'unknown'}",
            f"• Message: {str(payload.get('message') or '')[:500]}",
        ])
    text.extend(["", f"📜 Last {max(1, min(int(lines), 2000))} runtime log lines"])
    if log_lines:
        text.extend(log_lines)
    else:
        text.append("(runtime.log has no lines yet)")
    text.extend(["", "Use /logs file [lines] for a downloadable diagnostic report."])
    return "\n".join(text)[-4096:]


def build_diagnostics_report(db_path: str | Path | None = None, *, lines: int = 500) -> str:
    snapshot = collect_runtime_snapshot(db_path)
    payload = json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False, default=str)
    log_lines = tail_runtime_log(lines)
    return (
        "OBSERVER SANDBOX RUNTIME DIAGNOSTICS\n"
        "====================================\n"
        f"Generated: {_utc_stamp()}\n\n"
        "STRUCTURED SNAPSHOT\n"
        "-------------------\n"
        f"{payload}\n\n"
        f"RUNTIME LOG — LAST {max(1, min(int(lines), 2000))} LINES\n"
        "----------------------------------------\n"
        + ("\n".join(log_lines) if log_lines else "(no runtime log lines)")
        + "\n"
    )


def write_diagnostics_report(
    destination: str | Path,
    db_path: str | Path | None = None,
    *,
    lines: int = 500,
) -> Path:
    target = Path(destination)
    target.write_text(build_diagnostics_report(db_path, lines=lines), encoding="utf-8")
    return target

from __future__ import annotations

import json
import logging
import logging.handlers
import os
import re
import sqlite3
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_DB_PATH = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
RUNTIME_LOG_PATH = Path(os.environ.get("OBSERVER_RUNTIME_LOG", "/var/lib/observer-sandbox/runtime.log"))
SERVICE_NAME = os.environ.get("OBSERVER_SYSTEMD_SERVICE", "observer-sandbox.service")
_LOGGER_NAME = "observer_sandbox.runtime"
_CONFIGURED = False
_LOG_LEVEL_RE = re.compile(r"\b(DEBUG|INFO|WARNING|ERROR|CRITICAL)\b")


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def configure_runtime_logging(path: str | Path | None = None) -> logging.Logger:
    """Install a bounded app-owned production log with traceback-capable records."""
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
            "%(asctime)sZ %(levelname)s %(name)s %(threadName)s %(module)s.%(funcName)s:%(lineno)d %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        formatter.converter = time.gmtime
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    except OSError:
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


def _error_blocks(lines: int = 200, path: str | Path | None = None) -> list[str]:
    """Return error/warning records plus following traceback continuation lines."""
    raw = tail_runtime_log(max(lines * 4, 200), path)
    blocks: list[str] = []
    active = False
    for line in raw:
        match = _LOG_LEVEL_RE.search(line)
        if match:
            active = match.group(1) in {"WARNING", "ERROR", "CRITICAL"}
            if active:
                blocks.append(line)
            continue
        if active:
            blocks.append(line)
    return blocks[-max(1, min(int(lines), 2000)) :]


def _safe_json(value: str | None) -> Any:
    if value is None:
        return None
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return {"unparsed": str(value)[:500]}


def _run_readonly(command: list[str], *, timeout: int = 5) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env={**os.environ, "SYSTEMD_COLORS": "0", "SYSTEMD_PAGER": ""},
        )
        return {
            "ok": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "returncode": None, "stdout": "", "stderr": f"{type(exc).__name__}: {exc}"}


def collect_system_snapshot(*, journal_lines: int = 120, service_name: str = SERVICE_NAME) -> dict[str, Any]:
    """Read systemd and journal state without sudo or mutation."""
    show = _run_readonly(
        [
            "systemctl",
            "show",
            service_name,
            "--no-pager",
            "--property=ActiveState,SubState,Result,MainPID,NRestarts,ExecMainCode,ExecMainStatus,ActiveEnterTimestamp,StateChangeTimestamp",
        ]
    )
    properties: dict[str, str] = {}
    if show["stdout"]:
        for line in show["stdout"].splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                properties[key] = value

    journal = _run_readonly(
        [
            "journalctl",
            "-u",
            service_name,
            "--no-pager",
            "-n",
            str(max(1, min(int(journal_lines), 500))),
            "-o",
            "short-iso",
        ],
        timeout=8,
    )
    return {
        "service_name": service_name,
        "systemctl_ok": bool(show["ok"]),
        "properties": properties,
        "systemctl_error": show["stderr"] or None,
        "journal_ok": bool(journal["ok"]),
        "journal": journal["stdout"],
        "journal_error": journal["stderr"] or None,
    }


def collect_runtime_snapshot(db_path: str | Path | None = None) -> dict[str, Any]:
    """Return concise runtime context; intentionally excludes large cognition state dumps."""
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
            version = conn.execute("SELECT value FROM schema_meta WHERE key=?", ("schema_version",)).fetchone()
            snapshot["schema_version"] = version[0] if version else None

            runtime_keys = ("paused", "speed")
            state: dict[str, Any] = {}
            for key in runtime_keys:
                row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (key,)).fetchone()
                if row:
                    state[key] = _safe_json(row[0])
            snapshot["runtime_state"] = state

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
                   ORDER BY id DESC LIMIT 12"""
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


def _latest_runtime_error(snapshot: dict[str, Any]) -> dict[str, Any] | None:
    events = snapshot.get("recent_runtime_events") or []
    return next((event for event in events if event.get("event_type") == "autonomy_error"), None)


def _error_summary(snapshot: dict[str, Any], system: dict[str, Any], error_lines: list[str]) -> list[str]:
    props = system.get("properties") or {}
    latest_error = _latest_runtime_error(snapshot)
    latest_app = next((line for line in reversed(error_lines) if _LOG_LEVEL_RE.search(line)), None)
    lines = [
        "ERROR SUMMARY",
        "=============",
        f"Generated UTC: {snapshot.get('generated_utc')}",
        f"Service: {props.get('ActiveState', 'unknown')}/{props.get('SubState', 'unknown')}",
        f"Service result: {props.get('Result', 'unknown')}",
        f"Main PID: {props.get('MainPID', snapshot.get('pid', 'unknown'))}",
        f"Restarts: {props.get('NRestarts', 'unknown')}",
        f"Last exec: code={props.get('ExecMainCode', 'unknown')} status={props.get('ExecMainStatus', 'unknown')}",
        f"SQLite quick_check: {snapshot.get('sqlite_quick_check', 'unknown')}",
        f"Schema version: {snapshot.get('schema_version', 'unknown')}",
        f"Application log bytes: {snapshot.get('log_size_bytes') or 0}",
        f"Recent warning/error log lines: {len(error_lines)}",
    ]
    if latest_app:
        lines.append(f"Latest application warning/error: {latest_app[:1000]}")
    else:
        lines.append("Latest application warning/error: none in captured window")
    if latest_error:
        payload = latest_error.get("payload") or {}
        lines.append(
            "Latest autonomy error: "
            + f"{payload.get('error_type') or 'unknown'} at {payload.get('stage') or 'unknown'} — "
            + str(payload.get("message") or "")[:800]
        )
    else:
        lines.append("Latest autonomy error: none in concise runtime window")
    if system.get("journal_error"):
        lines.append(f"Journal access note: {system['journal_error'][:800]}")
    if snapshot.get("db_error"):
        lines.append(f"Database diagnostic error: {snapshot['db_error'][:800]}")
    return lines


def format_log_preview(db_path: str | Path | None = None, *, lines: int = 30, mode: str = "summary") -> str:
    limit = max(1, min(int(lines), 2000))
    snapshot = collect_runtime_snapshot(db_path)
    if mode == "runtime":
        actor = snapshot.get("actor_runtime") or []
        events = snapshot.get("recent_runtime_events") or []
        text = [
            "🧭 RUNTIME CONTEXT",
            "━━━━━━━━━━━━━━━━━━",
            f"💾 SQLite · {snapshot.get('sqlite_quick_check', 'unknown')}",
            f"🧬 Schema · {snapshot.get('schema_version', 'unknown')}",
            f"👤 Actors · {json.dumps(actor, ensure_ascii=False, default=str)[:1800]}",
            "",
            "Recent runtime events:",
        ]
        for event in events[:8]:
            text.append(f"• {event.get('event_type')} · {event.get('sim_time')} · {event.get('actor_id')}")
        return "\n".join(text)[-4096:]

    system = collect_system_snapshot(journal_lines=min(limit, 80))
    error_lines = _error_blocks(limit)
    props = system.get("properties") or {}
    if mode == "system":
        text = [
            "🖥 SYSTEM DIAGNOSTICS",
            "━━━━━━━━━━━━━━━━━━",
            f"Service · {props.get('ActiveState', 'unknown')}/{props.get('SubState', 'unknown')}",
            f"Result · {props.get('Result', 'unknown')}",
            f"PID · {props.get('MainPID', 'unknown')}",
            f"Restarts · {props.get('NRestarts', 'unknown')}",
            f"Exec · code={props.get('ExecMainCode', 'unknown')} status={props.get('ExecMainStatus', 'unknown')}",
            "",
            f"Journal last {min(limit, 80)} lines:",
            system.get("journal") or f"(unavailable: {system.get('journal_error') or 'no entries'})",
        ]
        return "\n".join(text)[-4096:]

    if mode == "errors":
        text = ["🚨 ERROR LOG", "━━━━━━━━━━━━━━━━━━"]
        text.extend(error_lines or ["No WARNING/ERROR/CRITICAL records in the captured window."])
        return "\n".join(text)[-4096:]

    summary = _error_summary(snapshot, system, error_lines)
    summary.extend(
        [
            "",
            "Commands:",
            "/logs errors [lines]",
            "/logs system [lines]",
            "/logs runtime",
            "/logs file [lines]",
        ]
    )
    return "\n".join(summary)[-4096:]


def build_diagnostics_report(db_path: str | Path | None = None, *, lines: int = 500) -> str:
    limit = max(1, min(int(lines), 2000))
    snapshot = collect_runtime_snapshot(db_path)
    system = collect_system_snapshot(journal_lines=min(limit, 500))
    error_lines = _error_blocks(limit)
    raw_lines = tail_runtime_log(limit)
    summary = "\n".join(_error_summary(snapshot, system, error_lines))
    props = json.dumps(system.get("properties") or {}, indent=2, sort_keys=True, ensure_ascii=False)
    runtime_payload = json.dumps(snapshot, indent=2, sort_keys=True, ensure_ascii=False, default=str)
    journal = system.get("journal") or f"(unavailable: {system.get('journal_error') or 'no entries'})"
    errors = "\n".join(error_lines) if error_lines else "(no WARNING/ERROR/CRITICAL records in captured application log window)"
    raw = "\n".join(raw_lines) if raw_lines else "(no runtime log lines)"
    return (
        "OBSERVER SANDBOX DIAGNOSTICS V2\n"
        "===============================\n"
        f"Generated: {_utc_stamp()}\n\n"
        f"{summary}\n\n"
        "SYSTEM SERVICE STATE\n"
        "====================\n"
        f"{props}\n"
        f"systemctl_error: {system.get('systemctl_error')}\n\n"
        "APPLICATION WARNINGS / ERRORS / TRACEBACKS\n"
        "==========================================\n"
        f"{errors}\n\n"
        "RECENT SYSTEM JOURNAL\n"
        "=====================\n"
        f"{journal}\n\n"
        "CONCISE RUNTIME CONTEXT\n"
        "=======================\n"
        f"{runtime_payload}\n\n"
        f"RAW APPLICATION LOG — LAST {limit} LINES\n"
        "========================================\n"
        f"{raw}\n"
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

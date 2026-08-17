from __future__ import annotations

import logging
import os
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

from . import telegram_bot as base
from . import telegram_creator_bot as creator  # noqa: F401  # installs existing Creator extensions
from .runtime_diagnostics import (
    build_diagnostics_report,
    configure_runtime_logging,
    format_log_preview,
)

_LOG = configure_runtime_logging()
_ORIGINAL_API = base._api
_ORIGINAL_SEND = base._send
_ORIGINAL_HELP = base._help
_ORIGINAL_HANDLE_COMMAND = base.handle_command
_FILE_SENTINEL = "__OBSERVER_RUNTIME_LOG_FILE__:"
_SERVICE_STDERR_LOG = Path(os.environ.get("OBSERVER_SERVICE_STDERR_LOG", "/var/lib/observer-sandbox/service-stderr.log"))


def _tail_text(path: Path, lines: int) -> str:
    try:
        values = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return ""
    return "\n".join(values[-max(1, min(int(lines), 2000)):])


def _inject_service_stderr(report: str, lines: int) -> str:
    stderr = _tail_text(_SERVICE_STDERR_LOG, lines) or "(empty or unavailable)"
    section = "SYSTEMD SERVICE STDERR\n======================\n" + stderr + "\n\n"
    marker = "SYSTEM SERVICE STATE\n"
    return report.replace(marker, section + marker, 1) if marker in report else report + "\n\n" + section


def _api(token: str, method: str, payload: dict[str, Any] | None = None, *, timeout: int = 30) -> Any:
    try:
        return _ORIGINAL_API(token, method, payload, timeout=timeout)
    except Exception:
        _LOG.exception("telegram_api_error method=%s", method)
        raise


def _multipart_send_document(token: str, chat_id: int, path: Path, *, caption: str) -> None:
    boundary = "----ObserverSandboxBoundary7MA4YWxkTrZu0gW"
    filename = path.name
    content = path.read_bytes()
    chunks = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"chat_id\"\r\n\r\n{chat_id}\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"caption\"\r\n\r\n{caption}\r\n".encode(),
        (f"--{boundary}\r\nContent-Disposition: form-data; name=\"document\"; filename=\"{filename}\"\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n").encode(),
        content,
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendDocument",
        data=b"".join(chunks),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        response.read()


def _send(token: str, chat_id: int, text: str, keyboard=None):
    if text.startswith(_FILE_SENTINEL):
        path = Path(text[len(_FILE_SENTINEL):])
        try:
            _multipart_send_document(token, chat_id, path, caption="Observer Sandbox diagnostics v2")
        except Exception:
            _LOG.exception("telegram_runtime_log_export_failed chat_id=%s", chat_id)
            _ORIGINAL_SEND(token, chat_id, "Diagnostic export failed. Use /logs for the inline summary.")
        finally:
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
        return None
    return _ORIGINAL_SEND(token, chat_id, text, keyboard)


def _help(role: str) -> str:
    text = _ORIGINAL_HELP(role)
    if role == "owner":
        text += "\n/logs — Error/system health summary"
        text += "\n/logs errors [lines] — App warnings, errors and tracebacks"
        text += "\n/logs system [lines] — systemd, stderr and journal diagnostics"
        text += "\n/logs runtime — Concise universe runtime context"
        text += "\n/logs file [lines] — Download consolidated diagnostics .txt"
    return text


def _parse_lines(raw: str | None, default: int) -> int:
    if not raw:
        return default
    try:
        return max(1, min(int(raw), 2000))
    except ValueError:
        raise ValueError("lines must be an integer from 1 to 2000")


def handle_command(db_path: str | Path, *, user_id: int, text: str) -> str:
    command_line = (text or "").strip()
    parts = command_line.split()
    first = parts[0] if parts else ""
    command = first.split("@", 1)[0].lower()
    role = base._user_role(user_id)

    if command == "/logs":
        if role != "owner":
            return "🔒 Creator authority required for runtime diagnostics."
        try:
            mode = parts[1].lower() if len(parts) >= 2 else "summary"
            if mode in {"file", "txt", "export"}:
                lines = _parse_lines(parts[2] if len(parts) >= 3 else None, 500)
                fd, raw_path = tempfile.mkstemp(prefix="observer-diagnostics-v2-", suffix=".txt")
                os.close(fd)
                path = Path(raw_path)
                report = _inject_service_stderr(build_diagnostics_report(db_path, lines=lines), lines)
                path.write_text(report, encoding="utf-8")
                _LOG.info("telegram_diagnostics_export_requested user_id=%s lines=%s", user_id, lines)
                return _FILE_SENTINEL + str(path)
            if mode in {"errors", "error"}:
                lines = _parse_lines(parts[2] if len(parts) >= 3 else None, 80)
                _LOG.info("telegram_diagnostics_errors_requested user_id=%s lines=%s", user_id, lines)
                return format_log_preview(db_path, lines=lines, mode="errors")
            if mode in {"system", "service", "journal"}:
                lines = _parse_lines(parts[2] if len(parts) >= 3 else None, 40)
                _LOG.info("telegram_diagnostics_system_requested user_id=%s lines=%s", user_id, lines)
                base_preview = format_log_preview(db_path, lines=lines, mode="system")
                stderr = _tail_text(_SERVICE_STDERR_LOG, lines) or "(empty or unavailable)"
                return (base_preview + "\n\nSYSTEMD STDERR\n" + stderr)[-4096:]
            if mode in {"runtime", "universe"}:
                _LOG.info("telegram_diagnostics_runtime_requested user_id=%s", user_id)
                return format_log_preview(db_path, lines=30, mode="runtime")
            if mode == "summary":
                _LOG.info("telegram_diagnostics_summary_requested user_id=%s", user_id)
                return format_log_preview(db_path, lines=30, mode="summary")
            lines = _parse_lines(parts[1], 30)
            _LOG.info("telegram_diagnostics_errors_requested user_id=%s lines=%s", user_id, lines)
            return format_log_preview(db_path, lines=lines, mode="errors")
        except ValueError as exc:
            return "Usage:\n/logs\n/logs errors [1-2000]\n/logs system [1-500]\n/logs runtime\n/logs file [1-2000]\n" + str(exc)
        except Exception:
            _LOG.exception("telegram_runtime_diagnostics_command_failed user_id=%s", user_id)
            return "Runtime diagnostics failed safely. Check the VPS runtime log or deployment diagnostic artifact."

    try:
        return _ORIGINAL_HANDLE_COMMAND(db_path, user_id=user_id, text=text)
    except Exception:
        _LOG.exception("telegram_command_error user_id=%s command=%s", user_id, command)
        raise


base._api = _api
base._send = _send
base._help = _help
base.handle_command = handle_command

run_polling = base.run_polling

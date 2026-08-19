from __future__ import annotations

import logging
import os
import tempfile
import urllib.request
from pathlib import Path
from typing import Any

from . import telegram_bot as base
from . import telegram_creator_bot as creator  # noqa: F401  # installs existing Creator extensions
from .creator_profile_edit import CreatorProfileEditError
from .db import connect, migrate
from .runtime_diagnostics import (
    build_diagnostics_report,
    configure_runtime_logging,
    format_log_preview,
)
from .telegram_profile_edit import (
    profile_apply_command,
    profile_edit_command,
    profile_edit_usage,
    profile_grade_command,
)
from .telegram_profile_edit_ui import (
    handle_profile_edit_text,
    pack_profile_edit_ui,
    profile_edit_callback_view,
    unpack_profile_edit_ui,
)

_LOG = configure_runtime_logging()
_ORIGINAL_API = base._api
_ORIGINAL_SEND = base._send
_ORIGINAL_HELP = base._help
_ORIGINAL_HANDLE_COMMAND = base.handle_command
_ORIGINAL_CALLBACK_VIEW = base._callback_view
_FILE_SENTINEL = "__OBSERVER_RUNTIME_LOG_FILE__:"


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
        (
            f"--{boundary}\r\n"
            f"Content-Disposition: form-data; name=\"document\"; filename=\"{filename}\"\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n\r\n"
        ).encode(),
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
    profile_ui = unpack_profile_edit_ui(text)
    if profile_ui is not None:
        ui_text, ui_keyboard = profile_ui
        return _ORIGINAL_SEND(token, chat_id, ui_text, ui_keyboard)
    if text.startswith(_FILE_SENTINEL):
        path = Path(text[len(_FILE_SENTINEL) :])
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


def _profile_menu_with_creator_edit(
    view: tuple[str, list[list[dict[str, str]]] | None],
    character_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    text, keyboard = view
    rows = [list(row) for row in (keyboard or [])]
    insert_at = max(0, len(rows) - 2)
    rows.insert(insert_at, [{"text": "✏️ Edit Profile", "callback_data": f"pedit:enter:{character_id}"}])
    return text, rows


def _callback_view(conn, user_id: int, callback_data: str):
    role = base._user_role(user_id)
    if callback_data.startswith("pedit:"):
        if role != "owner":
            return "🔒 Creator authority required for character profile editing.", [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]]
        try:
            view = profile_edit_callback_view(conn, user_id=user_id, callback_data=callback_data)
            if view is not None:
                return view
        except (CreatorProfileEditError, KeyError, ValueError, PermissionError, RuntimeError) as exc:
            _LOG.warning("telegram_profile_edit_callback_rejected user_id=%s callback=%s error=%s", user_id, callback_data, exc)
            return (
                f"Creator profile update rejected: {exc}\n\nUniverse remains paused while Creator Edit Mode is open.",
                [[{"text": "← Edit Profile", "callback_data": "pedit:home"}], [{"text": "✅ Done Editing", "callback_data": "pedit:done"}]],
            )
    view = _ORIGINAL_CALLBACK_VIEW(conn, user_id, callback_data)
    if role == "owner" and callback_data.startswith("prof:"):
        character_id = callback_data.split(":", 1)[1]
        return _profile_menu_with_creator_edit(view, character_id)
    return view


def _help(role: str) -> str:
    text = _ORIGINAL_HELP(role)
    if role == "owner":
        text += "\n/logs — Error/system health summary"
        text += "\n/logs errors [lines] — App warnings, errors and tracebacks"
        text += "\n/logs system [lines] — systemd and journal diagnostics"
        text += "\n/logs runtime — Concise universe runtime context"
        text += "\n/logs file [lines] — Download consolidated diagnostics .txt"
        text += "\n/profileedit <character_id> <field_key> <value> — Advanced direct profile preview"
        text += "\n/profilegrade <character_id> <group> <grade> [preserve|normalize] — Advanced grade-target preview"
        text += "\n/profileapply <token> — Apply an advanced Creator profile preview"
        text += "\nProfile → Edit Profile — Preferred paused Creator editing UX"
    return text


def _parse_lines(raw: str | None, default: int) -> int:
    if not raw:
        return default
    try:
        return max(1, min(int(raw), 2000))
    except ValueError:
        raise ValueError("lines must be an integer from 1 to 2000")


def _profile_control_command(db_path: str | Path, *, user_id: int, parts: list[str], command: str) -> str:
    requested_by = f"telegram:{user_id}"
    try:
        with connect(db_path) as conn:
            migrate(conn)
            if command == "/profileedit":
                if len(parts) == 1:
                    return profile_edit_usage()
                if len(parts) < 4:
                    return "Usage: /profileedit <character_id> <field_key> <value>"
                return profile_edit_command(
                    conn,
                    character_id=parts[1],
                    field_key=parts[2],
                    raw_value=" ".join(parts[3:]),
                    requested_by=requested_by,
                )
            if command == "/profilegrade":
                if len(parts) < 4 or len(parts) > 5:
                    return "Usage: /profilegrade <character_id> <group> <grade> [preserve|normalize]"
                mode = parts[4].lower() if len(parts) == 5 else "preserve"
                return profile_grade_command(
                    conn,
                    character_id=parts[1],
                    group=parts[2],
                    grade=parts[3],
                    mode=mode,
                    requested_by=requested_by,
                )
            if command == "/profileapply":
                if len(parts) != 2:
                    return "Usage: /profileapply <preview_token>"
                return profile_apply_command(conn, token=parts[1], requested_by=requested_by)
    except (CreatorProfileEditError, KeyError, ValueError, PermissionError, RuntimeError) as exc:
        return f"Creator profile update rejected: {exc}"
    raise AssertionError("unreachable profile control command")


def handle_command(db_path: str | Path, *, user_id: int, text: str) -> str:
    command_line = (text or "").strip()
    parts = command_line.split()
    first = parts[0] if parts else ""
    command = first.split("@", 1)[0].lower()
    role = base._user_role(user_id)

    if role == "owner" and command_line and not command_line.startswith("/"):
        try:
            with connect(db_path) as conn:
                migrate(conn)
                profile_ui = handle_profile_edit_text(conn, user_id=user_id, text=command_line)
                if profile_ui is not None:
                    return pack_profile_edit_ui(profile_ui)
        except (CreatorProfileEditError, KeyError, ValueError, PermissionError, RuntimeError) as exc:
            return pack_profile_edit_ui((
                f"Creator profile update rejected: {exc}\n\nNo profile value changed. Universe remains paused in Creator Edit Mode.",
                [[{"text": "← Edit Profile", "callback_data": "pedit:home"}], [{"text": "✅ Done Editing", "callback_data": "pedit:done"}]],
            ))

    if command in {"/profileedit", "/profilegrade", "/profileapply"}:
        if role != "owner":
            return "🔒 Creator authority required for character profile editing."
        return _profile_control_command(db_path, user_id=user_id, parts=parts, command=command)

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
                path.write_text(build_diagnostics_report(db_path, lines=lines), encoding="utf-8")
                _LOG.info("telegram_diagnostics_export_requested user_id=%s lines=%s", user_id, lines)
                return _FILE_SENTINEL + str(path)
            if mode in {"errors", "error"}:
                lines = _parse_lines(parts[2] if len(parts) >= 3 else None, 80)
                _LOG.info("telegram_diagnostics_errors_requested user_id=%s lines=%s", user_id, lines)
                return format_log_preview(db_path, lines=lines, mode="errors")
            if mode in {"system", "service", "journal"}:
                lines = _parse_lines(parts[2] if len(parts) >= 3 else None, 40)
                _LOG.info("telegram_diagnostics_system_requested user_id=%s lines=%s", user_id, lines)
                return format_log_preview(db_path, lines=lines, mode="system")
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
            return (
                "Usage:\n/logs\n/logs errors [1-2000]\n/logs system [1-500]\n"
                "/logs runtime\n/logs file [1-2000]\n" + str(exc)
            )
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
base._callback_view = _callback_view
base.handle_command = handle_command

from .telegram_creator_ux_polish import install_creator_ux_polish
install_creator_ux_polish()

run_polling = base.run_polling

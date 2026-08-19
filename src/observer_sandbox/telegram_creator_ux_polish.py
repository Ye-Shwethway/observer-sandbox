from __future__ import annotations

import json
import os
import threading
import urllib.request

from .db import connect, migrate

_REPO_COMMITS_URL = "https://api.github.com/repos/Ye-Shwethway/observer-sandbox/commits/main"
_PROMPT_MESSAGES: dict[int, int] = {}
_DELETE_AFTER_INPUT: set[int] = set()
_INSTALLED = False


def _is_creator_input_prompt(text: str) -> bool:
    first = (text or "").splitlines()[0].strip()
    return first in {
        "👤 CHARACTER · AI DRAFT",
        "👤 CHARACTER · MANUAL",
        "📍 LOCATION · AI DRAFT",
        "📍 LOCATION · MANUAL",
    }


def _record_prompt_edit(chat_id: int, message_id: int, text: str) -> None:
    chat_id = int(chat_id)
    message_id = int(message_id)
    if _is_creator_input_prompt(text):
        _PROMPT_MESSAGES[chat_id] = message_id
    elif _PROMPT_MESSAGES.get(chat_id) == message_id:
        _PROMPT_MESSAGES.pop(chat_id, None)


def _mark_studio_input_consumed(user_id: int) -> None:
    _DELETE_AFTER_INPUT.add(int(user_id))


def _take_prompt_delete(chat_id: int) -> int | None:
    chat_id = int(chat_id)
    if chat_id not in _DELETE_AFTER_INPUT:
        return None
    _DELETE_AFTER_INPUT.discard(chat_id)
    return _PROMPT_MESSAGES.pop(chat_id, None)


def _active_studio_input_mode(db_path: str, user_id: int) -> str | None:
    try:
        with connect(db_path) as conn:
            migrate(conn)
            row = conn.execute(
                """SELECT input_mode FROM creation_sandbox_studio_sessions
                WHERE sandbox_id='creator-default' AND user_id=?""",
                (int(user_id),),
            ).fetchone()
            return str(row["input_mode"]) if row else None
    except Exception:
        return None


def _meaningful_commit_summary(message: str) -> str:
    lines = [line.strip() for line in str(message or "").splitlines() if line.strip()]
    if not lines:
        return "Repository update"
    if lines[0].lower().startswith("merge pull request") and len(lines) > 1:
        return lines[-1]
    return lines[0]


def _repo_checkpoint() -> tuple[str, str] | None:
    request = urllib.request.Request(
        _REPO_COMMITS_URL,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "observer-sandbox/telegram-boot"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
        sha = str(data.get("sha") or "").strip()
        message = str(((data.get("commit") or {}).get("message")) or "")
        if not sha:
            return None
        return sha[:12], _meaningful_commit_summary(message)
    except Exception:
        return None


def _start_typing_pump(api, token: str, chat_id: int) -> tuple[threading.Event, threading.Thread] | None:
    if not token:
        return None
    stop = threading.Event()

    def pump() -> None:
        while not stop.is_set():
            try:
                api(token, "sendChatAction", {"chat_id": int(chat_id), "action": "typing"}, timeout=10)
            except Exception:
                pass
            if stop.wait(4.0):
                break

    thread = threading.Thread(target=pump, name=f"creator-studio-typing-{chat_id}", daemon=True)
    thread.start()
    return stop, thread


def _stop_typing_pump(pump: tuple[threading.Event, threading.Thread] | None) -> None:
    if pump is None:
        return
    stop, thread = pump
    stop.set()
    thread.join(timeout=1.0)


def _wrap_active_studio_router(base, api) -> bool:
    """Attach UX lifecycle to the one-shot Creator Studio router if it is active.

    Creator Studio dynamically replaces ``base.handle_command`` after a guided
    input card is opened. That router must therefore be wrapped after installation;
    wrapping only the long-lived runtime handler is insufficient.
    """
    routed = base.handle_command
    if not getattr(routed, "_creator_studio_input_router", False):
        return False
    if getattr(routed, "_creator_ux_wrapped", False):
        return True

    def routed_with_ux(db_path, *, user_id: int, text: str) -> str:
        raw = (text or "").strip()
        ordinary_input = bool(raw) and not raw.startswith("/")
        mode = _active_studio_input_mode(str(db_path), user_id) if ordinary_input else None
        if mode is not None:
            _mark_studio_input_consumed(user_id)
        pump = None
        if mode == "ai_generated":
            token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
            pump = _start_typing_pump(api, token, int(user_id))
        try:
            return routed(db_path, user_id=user_id, text=text)
        finally:
            _stop_typing_pump(pump)

    routed_with_ux._creator_studio_input_router = True  # type: ignore[attr-defined]
    routed_with_ux._creator_ux_wrapped = True  # type: ignore[attr-defined]
    base.handle_command = routed_with_ux
    return True


def install_creator_ux_polish() -> None:
    global _INSTALLED
    if _INSTALLED:
        return

    from . import telegram_bot as base
    from . import telegram_creator_studio as studio

    original_api = base._api
    original_send = base._send
    original_edit = base._edit
    original_handle = base.handle_command
    original_boot = base._boot_message
    original_install_input_router = studio._install_input_router

    def boot_message() -> str:
        text = original_boot()
        checkpoint = _repo_checkpoint()
        if checkpoint is None:
            return text
        sha, summary = checkpoint
        return (
            text
            + "\n\n🚀 Latest repository checkpoint"
            + f"\n🔖 Commit: {sha}"
            + f"\n🛠 {summary}"
        )

    def edit(token: str, chat_id: int, message_id: int, text: str, keyboard=None):
        _record_prompt_edit(chat_id, message_id, text)
        return original_edit(token, int(chat_id), int(message_id), text, keyboard)

    def handle_command(db_path, *, user_id: int, text: str) -> str:
        raw = (text or "").strip()
        command = raw.split()[0].split("@", 1)[0].lower() if raw else ""
        pump = None
        if command == "/createai":
            token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
            pump = _start_typing_pump(original_api, token, int(user_id))
        try:
            return original_handle(db_path, user_id=user_id, text=text)
        finally:
            _stop_typing_pump(pump)

    def send(token: str, chat_id: int, text: str, keyboard=None):
        prompt_message_id = _take_prompt_delete(chat_id)
        if prompt_message_id is not None:
            try:
                original_api(
                    token,
                    "deleteMessage",
                    {"chat_id": int(chat_id), "message_id": int(prompt_message_id)},
                    timeout=10,
                )
            except Exception:
                pass
        return original_send(token, int(chat_id), text, keyboard)

    def install_input_router_with_ux() -> None:
        original_install_input_router()
        _wrap_active_studio_router(base, original_api)

    base._boot_message = boot_message
    base._edit = edit
    base.handle_command = handle_command
    base._send = send
    studio._install_input_router = install_input_router_with_ux
    _wrap_active_studio_router(base, original_api)
    _INSTALLED = True


__all__ = [
    "install_creator_ux_polish",
    "_is_creator_input_prompt",
    "_record_prompt_edit",
    "_mark_studio_input_consumed",
    "_take_prompt_delete",
    "_meaningful_commit_summary",
    "_start_typing_pump",
    "_stop_typing_pump",
    "_wrap_active_studio_router",
]

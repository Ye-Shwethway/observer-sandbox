from __future__ import annotations

import json
import re
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from .db import connect, migrate
from .simulation import runtime_value, set_runtime_value

_COMMAND_RE = re.compile(r"/([a-z0-9_]{1,32})\b")
_SYNCED_CHAT_IDS_KEY = "telegram_command_menu:chat_ids"
_MAX_COMMANDS = 100


def _description_for_line(line: str) -> str:
    if "—" in line:
        description = line.split("—", 1)[1].strip()
    else:
        description = "Observer Sandbox command"
    description = " ".join(description.split())
    return description[:256] or "Observer Sandbox command"


def commands_from_help(help_text: str, *, include_help: bool = True) -> list[dict[str, str]]:
    """Build Telegram BotCommand payloads from the final role-aware help contract.

    Telegram command handling is assembled through bounded adapter extensions.
    Parsing the final help output avoids a second command catalogue that can drift
    from those extensions: adding a documented command automatically publishes it
    on the next bot restart/deploy.
    """
    commands: list[dict[str, str]] = []
    seen: set[str] = set()
    for raw_line in (help_text or "").splitlines():
        matches = list(_COMMAND_RE.finditer(raw_line.lower()))
        if not matches:
            continue
        description = _description_for_line(raw_line)
        for match in matches:
            command = match.group(1)
            if command in seen:
                continue
            seen.add(command)
            commands.append({"command": command, "description": description})

    if include_help and "help" not in seen:
        insertion = 1 if commands and commands[0]["command"] == "start" else 0
        commands.insert(insertion, {"command": "help", "description": "Show available commands"})

    if len(commands) > _MAX_COMMANDS:
        raise ValueError(f"Telegram command menu exceeds {_MAX_COMMANDS} commands")
    return commands


def _safe_default_commands() -> list[dict[str, str]]:
    return [
        {"command": "start", "description": "Connect to Observer Sandbox"},
        {"command": "whoami", "description": "Show your Telegram identity"},
    ]


def _scope_payload(scope: dict[str, Any], commands: list[dict[str, str]]) -> dict[str, str]:
    return {
        "commands": json.dumps(commands, separators=(",", ":")),
        "scope": json.dumps(scope, separators=(",", ":")),
    }


def _chat_scope(chat_id: int) -> dict[str, Any]:
    return {"type": "chat", "chat_id": int(chat_id)}


def sync_bot_commands(
    api: Callable[..., Any],
    token: str,
    db_path: str | Path,
    *,
    help_renderer: Callable[[str], str],
    owner_id: int | None,
    allowed_user_ids: Iterable[int],
) -> dict[str, int]:
    """Reconcile Telegram's command menus with current Observer permissions.

    Default scope exposes only safe connection/identity commands. Configured
    authorized chats receive a role-specific chat scope, so Creator-only commands
    are never advertised to ordinary authorized users. Previously configured chat
    scopes are remembered and deleted if an ID is later removed from configuration.
    """
    allowed_ids = {int(value) for value in allowed_user_ids}
    if owner_id is not None:
        allowed_ids.discard(int(owner_id))

    owner_commands = commands_from_help(help_renderer("owner")) if owner_id is not None else []
    allowed_commands = commands_from_help(help_renderer("allowed"))

    # A default menu prevents stale BotFather/global commands from exposing
    # Creator controls to unauthorized private chats.
    api(
        token,
        "setMyCommands",
        _scope_payload({"type": "default"}, _safe_default_commands()),
        timeout=15,
    )

    active_chat_ids = set(allowed_ids)
    if owner_id is not None:
        active_chat_ids.add(int(owner_id))

    with connect(db_path) as conn:
        migrate(conn)
        previous = {
            int(value)
            for value in runtime_value(conn, _SYNCED_CHAT_IDS_KEY, [])
            if isinstance(value, int) or (isinstance(value, str) and value.lstrip("-").isdigit())
        }

        for stale_chat_id in sorted(previous - active_chat_ids):
            api(
                token,
                "deleteMyCommands",
                {"scope": json.dumps(_chat_scope(stale_chat_id), separators=(",", ":"))},
                timeout=15,
            )

        for user_id in sorted(allowed_ids):
            api(
                token,
                "setMyCommands",
                _scope_payload(_chat_scope(user_id), allowed_commands),
                timeout=15,
            )

        if owner_id is not None:
            api(
                token,
                "setMyCommands",
                _scope_payload(_chat_scope(int(owner_id)), owner_commands),
                timeout=15,
            )

        set_runtime_value(conn, _SYNCED_CHAT_IDS_KEY, sorted(active_chat_ids))
        conn.commit()

    return {
        "default": len(_safe_default_commands()),
        "allowed": len(allowed_commands),
        "owner": len(owner_commands),
        "scoped_chats": len(active_chat_ids),
    }


__all__ = ["commands_from_help", "sync_bot_commands"]

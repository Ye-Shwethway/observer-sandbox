from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Any

from .actor_selection import resolve_actor_id
from .simulation import runtime_value, set_runtime_value

FALLBACK_KEY_PREFIX = "ai_cognition_fallback:"
LAST_FALLBACK_KEY_PREFIX = "ai_cognition_last_fallback:"


def _fallback_key(character_id: str, role: str) -> str:
    return f"{FALLBACK_KEY_PREFIX}{character_id}:{role}"


def _last_fallback_key(character_id: str, role: str) -> str:
    return f"{LAST_FALLBACK_KEY_PREFIX}{character_id}:{role}"


def get_fallback_binding(
    conn: sqlite3.Connection,
    *,
    character_id: str | None = None,
    role: str = "cognition",
) -> dict[str, Any] | None:
    character_id = resolve_actor_id(conn, character_id)
    value = runtime_value(conn, _fallback_key(character_id, role), None)
    if not isinstance(value, dict):
        return None
    provider_id = value.get("provider_id")
    model_id = value.get("model_id")
    if not provider_id or not model_id:
        return None
    return {
        "provider_id": str(provider_id),
        "model_id": str(model_id),
        "parameters": dict(value.get("parameters") or {}),
        "tested_at": value.get("tested_at"),
    }


def set_fallback_binding(
    conn: sqlite3.Connection,
    provider_id: str,
    model_id: str,
    *,
    character_id: str | None = None,
    role: str = "cognition",
    tested_at: str | None = None,
) -> dict[str, Any]:
    character_id = resolve_actor_id(conn, character_id)
    value = {
        "provider_id": str(provider_id),
        "model_id": str(model_id),
        "parameters": {},
        "tested_at": tested_at,
    }
    set_runtime_value(conn, _fallback_key(character_id, role), value)
    conn.commit()
    return value


def clear_fallback_binding(
    conn: sqlite3.Connection,
    *,
    character_id: str | None = None,
    role: str = "cognition",
) -> None:
    character_id = resolve_actor_id(conn, character_id)
    set_runtime_value(conn, _fallback_key(character_id, role), None)
    conn.commit()


def record_fallback_use(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    role: str,
    primary_provider_id: str,
    primary_model_id: str,
    fallback_provider_id: str,
    fallback_model_id: str,
    primary_error: str,
) -> dict[str, Any]:
    character_id = resolve_actor_id(conn, character_id)
    value = {
        "used_at": datetime.now(timezone.utc).isoformat(),
        "primary_provider_id": primary_provider_id,
        "primary_model_id": primary_model_id,
        "fallback_provider_id": fallback_provider_id,
        "fallback_model_id": fallback_model_id,
        "primary_error": primary_error[:500],
    }
    set_runtime_value(conn, _last_fallback_key(character_id, role), value)
    conn.commit()
    return value


def last_fallback_use(
    conn: sqlite3.Connection,
    *,
    character_id: str | None = None,
    role: str = "cognition",
) -> dict[str, Any] | None:
    character_id = resolve_actor_id(conn, character_id)
    value = runtime_value(conn, _last_fallback_key(character_id, role), None)
    return dict(value) if isinstance(value, dict) else None

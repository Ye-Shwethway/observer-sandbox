from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .simulation import runtime_value, set_runtime_value


SNAPSHOT_KEY_PREFIX = "cognition_context_snapshots_v1:"
SNAPSHOT_LIMIT = 3


def _key(character_id: str) -> str:
    return f"{SNAPSHOT_KEY_PREFIX}{character_id}"


def record_cognition_context_snapshot(
    conn,
    *,
    character_id: str,
    role: str,
    injection_type: str,
    provider_id: str,
    model_id: str,
    available_actions: list[str],
    context: dict[str, Any],
) -> dict[str, Any]:
    """Persist the exact compact runtime context prepared for one model injection."""
    snapshot = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "sim_time": context.get("sim_time"),
        "role": role,
        "injection_type": injection_type,
        "provider_id": provider_id,
        "model_id": model_id,
        "available_actions": list(available_actions),
        "context": context,
    }
    existing = runtime_value(conn, _key(character_id), [])
    rows = existing if isinstance(existing, list) else []
    set_runtime_value(conn, _key(character_id), [snapshot, *rows[: SNAPSHOT_LIMIT - 1]])
    return snapshot


def cognition_context_snapshots(conn, character_id: str) -> list[dict[str, Any]]:
    value = runtime_value(conn, _key(character_id), [])
    if not isinstance(value, list):
        return []
    return [item for item in value[:SNAPSHOT_LIMIT] if isinstance(item, dict)]

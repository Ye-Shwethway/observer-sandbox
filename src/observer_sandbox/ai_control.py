from __future__ import annotations

import json
import os
import sqlite3
import time
from datetime import datetime, timezone
from typing import Any

from . import ai as ai_backend
from . import ai_runtime
from .ai import AIConfigurationError, configure_provider, list_models, list_providers, resolve_binding, set_binding
from .secrets import load_runtime_secrets


class AIControlError(RuntimeError):
    pass


def provider_summaries(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return Creator-safe provider metadata without exposing credential values."""
    load_runtime_secrets()
    result: list[dict[str, Any]] = []
    for provider in list_providers(conn):
        item = dict(provider)
        ref = item.get("credential_ref")
        item["credential_present"] = bool(ref and os.environ.get(str(ref), "").strip())
        result.append(item)
    return result


def cognition_overview(
    conn: sqlite3.Connection,
    *,
    character_id: str = "char_darian",
    role: str = "cognition",
) -> dict[str, Any]:
    return {
        "character_id": character_id,
        "role": role,
        "binding": resolve_binding(conn, role=role, character_id=character_id),
        "providers": provider_summaries(conn),
    }


def _provider(conn: sqlite3.Connection, provider_id: str) -> sqlite3.Row:
    row = conn.execute("SELECT * FROM ai_providers WHERE id=?", (provider_id,)).fetchone()
    if row is None:
        raise AIConfigurationError(f"Unknown provider: {provider_id}")
    return row


def _fetch_models_without_activation(provider: sqlite3.Row) -> list[dict[str, Any]]:
    adapter = str(provider["adapter_type"])
    if adapter == "gemini":
        return ai_backend._fetch_gemini(provider)
    if adapter == "nanogpt":
        return ai_backend._fetch_nanogpt(provider)
    if adapter == "openai_compatible":
        return ai_backend._fetch_openai_compatible(provider)
    raise AIConfigurationError(f"Unsupported adapter type: {adapter}")


def refresh_provider_catalog(conn: sqlite3.Connection, provider_id: str) -> int:
    """Refresh a provider catalog without enabling it or changing any binding."""
    load_runtime_secrets()
    provider = _provider(conn, provider_id)
    try:
        models = _fetch_models_without_activation(provider)
        conn.execute("UPDATE ai_models SET active=0 WHERE provider_id=?", (provider_id,))
        for model in models:
            conn.execute(
                """
                INSERT INTO ai_models(
                    provider_id, model_id, display_name, capabilities_json,
                    context_window, metadata_json, active, last_seen_at
                ) VALUES (?, ?, ?, ?, ?, ?, 1, CURRENT_TIMESTAMP)
                ON CONFLICT(provider_id, model_id) DO UPDATE SET
                    display_name=excluded.display_name,
                    capabilities_json=excluded.capabilities_json,
                    context_window=excluded.context_window,
                    metadata_json=excluded.metadata_json,
                    active=1,
                    last_seen_at=CURRENT_TIMESTAMP
                """,
                (
                    provider_id,
                    model["model_id"],
                    model["display_name"],
                    json.dumps(model.get("capabilities") or {}),
                    model.get("context_window"),
                    json.dumps(model.get("metadata") or {}),
                ),
            )
        conn.execute(
            """
            UPDATE ai_catalog_sync
            SET last_refresh_at=CURRENT_TIMESTAMP, status='success', error_text=NULL, model_count=?
            WHERE provider_id=?
            """,
            (len(models), provider_id),
        )
        conn.commit()
        return len(models)
    except Exception as exc:
        conn.execute(
            """
            UPDATE ai_catalog_sync
            SET last_refresh_at=CURRENT_TIMESTAMP, status='error', error_text=?
            WHERE provider_id=?
            """,
            (str(exc)[:1000], provider_id),
        )
        conn.commit()
        raise


def _credential(provider: sqlite3.Row) -> str:
    load_runtime_secrets()
    ref = provider["credential_ref"]
    key = os.environ.get(str(ref), "").strip() if ref else ""
    if not key:
        raise AIConfigurationError(f"Missing credential environment variable: {ref}")
    return key


def probe_model(conn: sqlite3.Connection, provider_id: str, model_id: str) -> dict[str, Any]:
    """Perform one tiny real inference against a candidate without mutating bindings."""
    provider = _provider(conn, provider_id)
    exists = conn.execute(
        "SELECT 1 FROM ai_models WHERE provider_id=? AND model_id=? AND active=1",
        (provider_id, model_id),
    ).fetchone()
    if not exists:
        raise AIConfigurationError(f"Unknown or inactive model: {provider_id}/{model_id}")

    key = _credential(provider)
    prompt = (
        'Connectivity probe only. Return exactly action "idle", duration_minutes 1, '
        'target "", reason "probe" using the required structured response.'
    )
    started = time.monotonic()
    adapter = str(provider["adapter_type"])
    if adapter == "gemini":
        decision = ai_runtime._generate_gemini(provider, key, model_id, prompt, {})
    elif adapter == "nanogpt":
        decision = ai_runtime._generate_nanogpt(provider, key, model_id, prompt, {})
    elif adapter == "openai_compatible":
        decision = ai_runtime._generate_openai_compatible(provider, key, model_id, prompt, {})
    else:
        raise AIConfigurationError(f"Unsupported adapter type: {adapter}")
    latency_ms = max(0, round((time.monotonic() - started) * 1000))

    if not isinstance(decision, dict):
        raise ai_runtime.AIDecisionError("Probe response is not a JSON object")
    expected = {"action": "idle", "duration_minutes": 1, "target": "", "reason": "probe"}
    if decision != expected:
        raise ai_runtime.AIDecisionError("Model responded but did not satisfy the required cognition schema probe")
    return {
        "ok": True,
        "provider_id": provider_id,
        "model_id": model_id,
        "latency_ms": latency_ms,
        "tested_at": datetime.now(timezone.utc).isoformat(),
    }


def activate_cognition_model(
    conn: sqlite3.Connection,
    provider_id: str,
    model_id: str,
    *,
    character_id: str = "char_darian",
    role: str = "cognition",
) -> dict[str, Any]:
    """Make an already-tested candidate the active cognition binding."""
    configure_provider(conn, provider_id, enabled=True)
    set_binding(
        conn,
        scope_type="character",
        scope_id=character_id,
        role=role,
        provider_id=provider_id,
        model_id=model_id,
        parameters={},
    )
    binding = resolve_binding(conn, role=role, character_id=character_id)
    if binding is None:
        raise AIControlError("Cognition binding was not persisted")
    return binding


def models_for_provider(conn: sqlite3.Connection, provider_id: str) -> list[dict[str, Any]]:
    _provider(conn, provider_id)
    return list_models(conn, provider_id)

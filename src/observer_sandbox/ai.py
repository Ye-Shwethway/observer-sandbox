from __future__ import annotations

import json
import os
import sqlite3
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ProviderTemplate:
    id: str
    display_name: str
    adapter_type: str
    base_url: str | None
    credential_ref: str | None
    enabled: bool = False


BUILTIN_PROVIDERS = (
    ProviderTemplate(
        id="gemini",
        display_name="Google Gemini",
        adapter_type="gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        credential_ref="OBSERVER_GEMINI_API_KEY",
    ),
    ProviderTemplate(
        id="openai",
        display_name="OpenAI",
        adapter_type="openai_compatible",
        base_url="https://api.openai.com/v1",
        credential_ref="OBSERVER_OPENAI_API_KEY",
    ),
    ProviderTemplate(
        id="openrouter",
        display_name="OpenRouter",
        adapter_type="openai_compatible",
        base_url="https://openrouter.ai/api/v1",
        credential_ref="OBSERVER_OPENROUTER_API_KEY",
    ),
    ProviderTemplate(
        id="nanogpt",
        display_name="NanoGPT",
        adapter_type="nanogpt",
        base_url="https://nano-gpt.com/api",
        credential_ref="OBSERVER_NANOGPT_API_KEY",
    ),
)


class AIConfigurationError(RuntimeError):
    pass


class CatalogFetchError(RuntimeError):
    pass


def seed_builtin_providers(conn: sqlite3.Connection) -> None:
    for provider in BUILTIN_PROVIDERS:
        conn.execute(
            """
            INSERT INTO ai_providers(
                id, display_name, adapter_type, base_url, credential_ref, enabled
            ) VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                display_name=excluded.display_name,
                adapter_type=excluded.adapter_type,
                base_url=CASE
                    WHEN ai_providers.base_url IS NULL OR ai_providers.id='nanogpt'
                    THEN excluded.base_url
                    ELSE ai_providers.base_url
                END,
                credential_ref=COALESCE(ai_providers.credential_ref, excluded.credential_ref)
            """,
            (
                provider.id,
                provider.display_name,
                provider.adapter_type,
                provider.base_url,
                provider.credential_ref,
                int(provider.enabled),
            ),
        )
        conn.execute(
            "INSERT INTO ai_catalog_sync(provider_id) VALUES (?) ON CONFLICT(provider_id) DO NOTHING",
            (provider.id,),
        )
    conn.commit()


def list_providers(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT p.*, s.last_refresh_at, s.status AS catalog_status, s.model_count
        FROM ai_providers p
        LEFT JOIN ai_catalog_sync s ON s.provider_id = p.id
        ORDER BY p.id
        """
    ).fetchall()
    return [dict(row) for row in rows]


def list_models(conn: sqlite3.Connection, provider_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """
        SELECT provider_id, model_id, display_name, capabilities_json,
               context_window, metadata_json, active, last_seen_at
        FROM ai_models
        WHERE provider_id = ? AND active = 1
        ORDER BY display_name, model_id
        """,
        (provider_id,),
    ).fetchall()
    result = []
    for row in rows:
        item = dict(row)
        item["capabilities"] = json.loads(item.pop("capabilities_json"))
        item["metadata"] = json.loads(item.pop("metadata_json"))
        result.append(item)
    return result


def configure_provider(
    conn: sqlite3.Connection,
    provider_id: str,
    *,
    enabled: bool | None = None,
    base_url: str | None = None,
    credential_ref: str | None = None,
) -> None:
    row = conn.execute("SELECT id FROM ai_providers WHERE id = ?", (provider_id,)).fetchone()
    if row is None:
        raise AIConfigurationError(f"Unknown provider: {provider_id}")
    if enabled is not None:
        conn.execute("UPDATE ai_providers SET enabled = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (int(enabled), provider_id))
    if base_url is not None:
        conn.execute("UPDATE ai_providers SET base_url = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (base_url.rstrip('/'), provider_id))
    if credential_ref is not None:
        conn.execute("UPDATE ai_providers SET credential_ref = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?", (credential_ref, provider_id))
    conn.commit()


def _get_json(url: str, headers: dict[str, str] | None = None, timeout: float = 20.0) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers or {}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise CatalogFetchError(str(exc)) from exc


def _credential(provider: sqlite3.Row) -> str | None:
    ref = provider["credential_ref"]
    return os.environ.get(ref) if ref else None


def _auth_headers(provider: sqlite3.Row) -> dict[str, str]:
    key = _credential(provider)
    if not key:
        raise AIConfigurationError(f"Missing credential environment variable: {provider['credential_ref']}")
    return {"Authorization": f"Bearer {key}", "Accept": "application/json"}


def _fetch_gemini(provider: sqlite3.Row) -> list[dict[str, Any]]:
    key = _credential(provider)
    if not key:
        raise AIConfigurationError(f"Missing credential environment variable: {provider['credential_ref']}")
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError("Gemini base_url is not configured")
    models: list[dict[str, Any]] = []
    page_token: str | None = None
    while True:
        query = {"key": key, "pageSize": "1000"}
        if page_token:
            query["pageToken"] = page_token
        payload = _get_json(f"{base.rstrip('/')}/models?{urllib.parse.urlencode(query)}")
        for raw in payload.get("models", []):
            full_name = raw.get("name", "")
            model_id = raw.get("baseModelId") or full_name.removeprefix("models/")
            actions = raw.get("supportedGenerationMethods", raw.get("supportedActions", []))
            models.append(
                {
                    "model_id": model_id,
                    "display_name": raw.get("displayName") or model_id,
                    "context_window": raw.get("inputTokenLimit"),
                    "capabilities": {"actions": actions},
                    "metadata": raw,
                }
            )
        page_token = payload.get("nextPageToken")
        if not page_token:
            break
    return models


def _fetch_openai_compatible(provider: sqlite3.Row) -> list[dict[str, Any]]:
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError(f"Provider {provider['id']} requires a base_url")
    payload = _get_json(
        f"{base.rstrip('/')}/models",
        headers=_auth_headers(provider),
    )
    models = []
    for raw in payload.get("data", []):
        model_id = raw.get("id")
        if not model_id:
            continue
        architecture = raw.get("architecture") or {}
        capabilities = {
            "input_modalities": architecture.get("input_modalities", []),
            "output_modalities": architecture.get("output_modalities", []),
            "supported_parameters": raw.get("supported_parameters", []),
        }
        models.append(
            {
                "model_id": model_id,
                "display_name": raw.get("name") or model_id,
                "context_window": raw.get("context_length"),
                "capabilities": capabilities,
                "metadata": raw,
            }
        )
    return models


def _fetch_nanogpt(provider: sqlite3.Row) -> list[dict[str, Any]]:
    """Fetch only subscription-included NanoGPT text models by default."""
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError("NanoGPT base_url is not configured")
    payload = _get_json(
        f"{base.rstrip('/')}/subscription/v1/models?detailed=true",
        headers=_auth_headers(provider),
    )
    models: list[dict[str, Any]] = []
    for raw in payload.get("data", []):
        model_id = raw.get("id")
        if not model_id:
            continue
        capabilities = raw.get("capabilities") or {}
        models.append(
            {
                "model_id": model_id,
                "display_name": raw.get("name") or model_id,
                "context_window": raw.get("context_length") or raw.get("context_window"),
                "capabilities": capabilities,
                "metadata": raw,
            }
        )
    return models


def nanogpt_subscription_usage(conn: sqlite3.Connection) -> dict[str, Any]:
    provider = conn.execute("SELECT * FROM ai_providers WHERE id='nanogpt'").fetchone()
    if provider is None:
        raise AIConfigurationError("NanoGPT provider is not configured")
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError("NanoGPT base_url is not configured")
    return _get_json(
        f"{base.rstrip('/')}/subscription/v1/usage",
        headers=_auth_headers(provider),
    )


def refresh_catalog(conn: sqlite3.Connection, provider_id: str) -> int:
    provider = conn.execute("SELECT * FROM ai_providers WHERE id = ?", (provider_id,)).fetchone()
    if provider is None:
        raise AIConfigurationError(f"Unknown provider: {provider_id}")
    if not provider["enabled"]:
        raise AIConfigurationError(f"Provider is disabled: {provider_id}")
    try:
        if provider["adapter_type"] == "gemini":
            models = _fetch_gemini(provider)
        elif provider["adapter_type"] == "nanogpt":
            models = _fetch_nanogpt(provider)
        elif provider["adapter_type"] == "openai_compatible":
            models = _fetch_openai_compatible(provider)
        else:
            raise AIConfigurationError(f"Unsupported adapter type: {provider['adapter_type']}")

        conn.execute("UPDATE ai_models SET active = 0 WHERE provider_id = ?", (provider_id,))
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
                    json.dumps(model["capabilities"]),
                    model["context_window"],
                    json.dumps(model["metadata"]),
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
            (str(exc), provider_id),
        )
        conn.commit()
        raise


def set_binding(
    conn: sqlite3.Connection,
    *,
    scope_type: str,
    scope_id: str,
    role: str,
    provider_id: str,
    model_id: str,
    parameters: dict[str, Any] | None = None,
) -> None:
    if scope_type not in {"global", "character", "engine", "task"}:
        raise AIConfigurationError(f"Invalid scope_type: {scope_type}")
    exists = conn.execute(
        "SELECT 1 FROM ai_models WHERE provider_id=? AND model_id=? AND active=1",
        (provider_id, model_id),
    ).fetchone()
    if not exists:
        raise AIConfigurationError(f"Unknown or inactive model: {provider_id}/{model_id}")
    conn.execute(
        """
        INSERT INTO ai_bindings(scope_type, scope_id, role, provider_id, model_id, parameters_json)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(scope_type, scope_id, role) DO UPDATE SET
            provider_id=excluded.provider_id,
            model_id=excluded.model_id,
            parameters_json=excluded.parameters_json,
            enabled=1,
            updated_at=CURRENT_TIMESTAMP
        """,
        (scope_type, scope_id, role, provider_id, model_id, json.dumps(parameters or {})),
    )
    conn.commit()


def resolve_binding(
    conn: sqlite3.Connection,
    *,
    role: str,
    character_id: str | None = None,
    engine_id: str | None = None,
    task_id: str | None = None,
) -> dict[str, Any] | None:
    candidates: list[tuple[str, str, str]] = []
    if task_id:
        candidates.append(("task", task_id, role))
    if character_id:
        candidates.append(("character", character_id, role))
    if engine_id:
        candidates.append(("engine", engine_id, role))
    if character_id and role != "default":
        candidates.append(("character", character_id, "default"))
    candidates.append(("global", "default", role))
    if role != "default":
        candidates.append(("global", "default", "default"))

    for scope_type, scope_id, candidate_role in candidates:
        row = conn.execute(
            """
            SELECT * FROM ai_bindings
            WHERE scope_type=? AND scope_id=? AND role=? AND enabled=1
            """,
            (scope_type, scope_id, candidate_role),
        ).fetchone()
        if row:
            result = dict(row)
            result["parameters"] = json.loads(result.pop("parameters_json"))
            return result
    return None

from __future__ import annotations

import json
import sqlite3
from typing import Any

from .ai import AIConfigurationError
from .ai_runtime import AIDecisionError, _post_json, _provider_and_key, nanogpt_model_billing_scope


def generate_structured(
    conn: sqlite3.Connection,
    *,
    provider_id: str,
    model_id: str,
    prompt: str,
    schema: dict[str, Any],
    schema_name: str,
    parameters: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run one real structured inference through the existing provider registry.

    This helper is deliberately role-neutral. It reuses the canonical provider,
    credential, endpoint and NanoGPT billing semantics without borrowing the
    cognition decision schema.
    """
    provider, key = _provider_and_key(conn, provider_id)
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError(f"Provider {provider_id} base_url is not configured")
    adapter = str(provider["adapter_type"])
    generation_parameters = dict(parameters or {})

    if adapter == "gemini":
        response = _post_json(
            f"{base.rstrip('/')}/models/{model_id}:generateContent",
            headers={"x-goog-api-key": key, "Accept": "application/json"},
            payload={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "responseMimeType": "application/json",
                    "responseJsonSchema": schema,
                    **generation_parameters,
                },
            },
        )
        try:
            text = response["candidates"][0]["content"]["parts"][0]["text"]
            value = json.loads(text)
        except Exception as exc:
            raise AIDecisionError("Gemini returned unusable structured output") from exc
    elif adapter in {"openai_compatible", "nanogpt"}:
        route = "chat/completions"
        if adapter == "nanogpt":
            scope = nanogpt_model_billing_scope(conn, model_id)
            route = f"{'subscription/v1' if scope == 'subscription' else 'v1'}/chat/completions"
        payload: dict[str, Any] = {
            "model": model_id,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "response_format": {
                "type": "json_schema",
                "json_schema": {"name": schema_name, "strict": True, "schema": schema},
            },
        }
        payload.update(generation_parameters)
        response = _post_json(
            f"{base.rstrip('/')}/{route}",
            headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
            payload=payload,
        )
        try:
            content = response["choices"][0]["message"]["content"]
            value = json.loads(content) if isinstance(content, str) else content
        except Exception as exc:
            raise AIDecisionError(f"Provider {provider_id} returned unusable structured output") from exc
    else:
        raise AIConfigurationError(f"Structured generation is not enabled for provider type: {adapter}")

    if not isinstance(value, dict):
        raise AIDecisionError("Structured AI output must be a JSON object")
    return value

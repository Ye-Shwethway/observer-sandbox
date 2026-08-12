from __future__ import annotations

import json
import os
import sqlite3
import urllib.request
from typing import Any

from .ai import AIConfigurationError, resolve_binding


class AIDecisionError(RuntimeError):
    pass


DECISION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "action": {"type": "string"},
        "duration_minutes": {"type": "integer", "minimum": 1, "maximum": 720},
        "target": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": ["action", "duration_minutes", "target", "reason"],
    "additionalProperties": False,
}


def _post_json(url: str, *, headers: dict[str, str], payload: dict[str, Any], timeout: float = 45.0) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise AIDecisionError(str(exc)) from exc


def _provider_and_key(conn: sqlite3.Connection, provider_id: str) -> tuple[sqlite3.Row, str]:
    provider = conn.execute("SELECT * FROM ai_providers WHERE id=?", (provider_id,)).fetchone()
    if provider is None:
        raise AIConfigurationError(f"Unknown provider: {provider_id}")
    if not provider["enabled"]:
        raise AIConfigurationError(f"Provider is disabled: {provider_id}")
    credential_ref = provider["credential_ref"]
    key = os.environ.get(credential_ref) if credential_ref else None
    if not key:
        raise AIConfigurationError(f"Missing credential environment variable: {credential_ref}")
    return provider, key


def _decision_prompt(state: dict[str, Any], available_actions: list[str]) -> str:
    return (
        "You control one autonomous simulated human. Choose exactly one next action. "
        "Respect the supplied world topology and local capabilities. Do not invent rooms, objects, "
        "actions, or direct state changes. The runtime will reject invalid actions.\n\n"
        f"Available action names: {json.dumps(available_actions)}\n"
        f"Current state: {json.dumps(state, ensure_ascii=False, sort_keys=True)}\n\n"
        "Return only the structured decision. For actions that do not need a target, use an empty string. "
        "For move, target must be one of reachable_rooms. Keep reason short."
    )


def _generate_nanogpt(
    provider: sqlite3.Row,
    key: str,
    model_id: str,
    prompt: str,
    parameters: dict[str, Any],
) -> dict[str, Any]:
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError("NanoGPT base_url is not configured")
    payload: dict[str, Any] = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": "observer_sandbox_decision",
                "strict": True,
                "schema": DECISION_SCHEMA,
            },
        },
    }
    payload.update(parameters)
    response = _post_json(
        f"{base.rstrip('/')}/subscription/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        payload=payload,
    )
    try:
        content = response["choices"][0]["message"]["content"]
        return json.loads(content) if isinstance(content, str) else content
    except Exception as exc:
        raise AIDecisionError("NanoGPT returned an unusable structured decision") from exc


def _generate_gemini(
    provider: sqlite3.Row,
    key: str,
    model_id: str,
    prompt: str,
    parameters: dict[str, Any],
) -> dict[str, Any]:
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError("Gemini base_url is not configured")
    generation_config = {
        "responseFormat": {
            "text": {
                "mimeType": "application/json",
                "schema": DECISION_SCHEMA,
            }
        },
        **parameters,
    }
    response = _post_json(
        f"{base.rstrip('/')}/models/{model_id}:generateContent",
        headers={"x-goog-api-key": key, "Accept": "application/json"},
        payload={
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": generation_config,
        },
    )
    try:
        text = response["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except Exception as exc:
        raise AIDecisionError("Gemini returned an unusable structured decision") from exc


def generate_character_decision(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    role: str,
    state: dict[str, Any],
    available_actions: list[str],
) -> dict[str, Any]:
    binding = resolve_binding(conn, role=role, character_id=character_id)
    if binding is None:
        raise AIConfigurationError(f"No AI binding resolved for {character_id}/{role}")

    provider, key = _provider_and_key(conn, binding["provider_id"])
    prompt = _decision_prompt(state, available_actions)
    parameters = binding.get("parameters") or {}

    if provider["adapter_type"] == "nanogpt":
        decision = _generate_nanogpt(provider, key, binding["model_id"], prompt, parameters)
    elif provider["adapter_type"] == "gemini":
        decision = _generate_gemini(provider, key, binding["model_id"], prompt, parameters)
    else:
        raise AIConfigurationError(
            f"P1 live decision adapter not yet enabled for provider type: {provider['adapter_type']}"
        )

    if not isinstance(decision, dict):
        raise AIDecisionError("AI decision must be a JSON object")
    required = {"action", "duration_minutes", "target", "reason"}
    if set(decision) != required:
        raise AIDecisionError("AI decision keys do not match the required schema")
    if decision["action"] not in available_actions:
        raise AIDecisionError(f"AI selected unavailable action: {decision['action']}")
    if not isinstance(decision["duration_minutes"], int) or not 1 <= decision["duration_minutes"] <= 720:
        raise AIDecisionError("AI duration_minutes is out of bounds")
    if not isinstance(decision["target"], str) or not isinstance(decision["reason"], str):
        raise AIDecisionError("AI target/reason must be strings")
    return decision

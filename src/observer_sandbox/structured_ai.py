from __future__ import annotations

import copy
import json
import os
import sqlite3
from typing import Any

from .ai import AIConfigurationError
from .ai_runtime import AIDecisionError, _post_json, nanogpt_model_billing_scope
from .secrets import load_runtime_secrets
from .skill_vocabulary import (
    SKILL_DEFINITIONS,
    canonical_skill_keys,
    missing_background_skill_coverage,
    normalize_creator_skills,
)


def _provider_and_credential(conn: sqlite3.Connection, provider_id: str) -> tuple[sqlite3.Row, str]:
    load_runtime_secrets()
    provider = conn.execute("SELECT * FROM ai_providers WHERE id=?", (provider_id,)).fetchone()
    if provider is None:
        raise AIConfigurationError(f"Unknown provider: {provider_id}")
    credential_ref = provider["credential_ref"]
    key = os.environ.get(str(credential_ref), "").strip() if credential_ref else ""
    if not key:
        raise AIConfigurationError(f"Missing credential environment variable: {credential_ref}")
    return provider, key


def _prepare_creator_character_contract(
    prompt: str,
    schema: dict[str, Any],
    schema_name: str,
) -> tuple[str, dict[str, Any]]:
    if schema_name != "observer_creator_studio_character":
        return prompt, schema
    tightened = copy.deepcopy(schema)
    try:
        skill_key_schema = tightened["properties"]["properties"]["properties"]["character_profile"]["properties"]["skills"]["items"]["properties"]["skill_key"]
        skill_key_schema["enum"] = list(canonical_skill_keys())
    except (KeyError, TypeError):
        return prompt, schema

    mapping = "; ".join(
        f"{key} ({definition['category']}): {', '.join(definition.get('cues', ()))}"
        for key, definition in SKILL_DEFINITIONS.items()
    )
    strengthened_prompt = (
        prompt
        + " Universal Character skill vocabulary: "
        + mapping
        + ". Use only these skill_key values. Inspect the generated background itself before finalizing the JSON. "
          "Every material trained or professional competency explicitly established in background.origins or "
          "background.story_elements must have semantic coverage in the structured skills array. Related techniques "
          "may aggregate under one canonical skill (for example boxing and wrestling under hand_to_hand_combat), but "
          "distinct material domains such as navigation, climbing, emergency response, field medicine, survival, "
          "technology, tactical planning, firearms, or bladed weapons must not disappear when the background explicitly "
          "establishes them. Do not invent a competency in background prose unless you are also willing to represent it "
          "with its corresponding structured skill."
    )
    return strengthened_prompt, tightened


def _validate_creator_character_skill_contract(value: dict[str, Any], schema_name: str) -> None:
    if schema_name != "observer_creator_studio_character":
        return
    try:
        profile = value["properties"]["character_profile"]
        values = profile["values"]
        skills = profile["skills"]
    except (KeyError, TypeError) as exc:
        raise AIDecisionError("Creator Character output is missing structured profile skill data") from exc
    if not isinstance(values, dict) or not isinstance(skills, list):
        raise AIDecisionError("Creator Character profile values/skills have invalid structure")
    try:
        normalized = normalize_creator_skills(item for item in skills if isinstance(item, dict))
    except ValueError as exc:
        raise AIDecisionError(str(exc)) from exc
    missing = missing_background_skill_coverage(values, normalized)
    if missing:
        raise AIDecisionError(
            "Character background has trained competencies without structured skill coverage: "
            + ", ".join(sorted(missing))
        )
    profile["skills"] = normalized


def generate_structured(
    conn: sqlite3.Connection,
    *,
    provider_id: str,
    model_id: str,
    prompt: str,
    schema: dict[str, Any],
    schema_name: str,
    parameters: dict[str, Any] | None = None,
    timeout: float = 120.0,
) -> dict[str, Any]:
    """Run one real structured inference through the existing provider registry.

    Candidate probes may call a currently disabled provider without enabling it;
    activation remains an explicit later binding operation. Structured generation
    can produce materially larger responses than ordinary autonomy decisions, so it
    receives a separate bounded transport timeout.
    """
    model = conn.execute(
        "SELECT 1 FROM ai_models WHERE provider_id=? AND model_id=? AND active=1",
        (provider_id, model_id),
    ).fetchone()
    if model is None:
        raise AIConfigurationError(f"Unknown or inactive model: {provider_id}/{model_id}")
    provider, key = _provider_and_credential(conn, provider_id)
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError(f"Provider {provider_id} base_url is not configured")
    adapter = str(provider["adapter_type"])
    generation_parameters = dict(parameters or {})
    prompt, schema = _prepare_creator_character_contract(prompt, schema, schema_name)

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
            timeout=timeout,
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
            timeout=timeout,
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
    _validate_creator_character_skill_contract(value, schema_name)
    return value

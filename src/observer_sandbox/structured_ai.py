from __future__ import annotations

import copy
import json
import os
import sqlite3
from typing import Any

from .ai import AIConfigurationError
from .ai_runtime import AIDecisionError, _post_json, nanogpt_model_billing_scope
from .secrets import load_runtime_secrets
from .skill_vocabulary import canonical_skill_keys, normalize_creator_skills


_CREATOR_CHARACTER_SCHEMA = "observer_creator_studio_character"
_CREATOR_PROFILE_ALIAS_FIELDS = {"raps_pa.practical_skill"}


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


def _character_profile_schema(schema: dict[str, Any]) -> dict[str, Any]:
    return schema["properties"]["properties"]["properties"]["character_profile"]


def _prepare_creator_character_contract(
    prompt: str,
    schema: dict[str, Any],
    schema_name: str,
) -> tuple[str, dict[str, Any]]:
    """Turn the existing Character profile registry into one exact AI fill template.

    Every creation-owned canonical profile field exposed by Creator Studio is
    required exactly once. Runtime/derived fields are excluded upstream by the
    Character creation policy. Skills are a separate sparse collection: generated
    skills must use the shared canonical vocabulary, but a Character only needs rows
    for skills they actually possess.
    """
    if schema_name != _CREATOR_CHARACTER_SCHEMA:
        return prompt, schema

    tightened = copy.deepcopy(schema)
    try:
        profile = _character_profile_schema(tightened)
        values_schema = profile["properties"]["values"]
        value_properties = values_schema["properties"]
        for alias in _CREATOR_PROFILE_ALIAS_FIELDS:
            value_properties.pop(alias, None)
        value_keys = sorted(value_properties)
        values_schema["required"] = value_keys
        values_schema["minProperties"] = len(value_keys)
        values_schema["maxProperties"] = len(value_keys)
        values_schema["additionalProperties"] = False

        skills_schema = profile["properties"]["skills"]
        skill_item = skills_schema["items"]
        skill_item["properties"]["skill_key"]["enum"] = list(canonical_skill_keys())
        skill_item["properties"]["score"] = {"type": ["number", "null"], "minimum": 0, "maximum": 100}
        skill_item["properties"]["experience"] = {"type": ["number", "null"], "minimum": 0}
        skills_schema.pop("minItems", None)
        skills_schema.pop("maxItems", None)
    except (KeyError, TypeError):
        return prompt, schema

    strengthened_prompt = (
        prompt
        + " Fill the supplied Character seed schema exactly. Do not select, omit, rename, or invent profile fields. "
          "Every key under properties.character_profile.values is required and must receive one value of the declared type. "
          "The schema is the Character profile contract; do not summarize it into prose and do not add compatibility aliases. "
          "For properties.character_profile.skills, include only skills the Character actually has, using only the allowed "
          "canonical skill_key values. Do not add zero-value placeholder skills merely to fill the vocabulary. Preferences, "
          "hobbies, and habits may be empty arrays when genuinely absent. Return only the completed schema object."
    )
    return strengthened_prompt, tightened


def _validate_creator_character_contract(
    value: dict[str, Any],
    schema: dict[str, Any],
    schema_name: str,
) -> None:
    if schema_name != _CREATOR_CHARACTER_SCHEMA:
        return
    try:
        expected_profile = _character_profile_schema(schema)
        expected_value_keys = set(expected_profile["properties"]["values"]["properties"])
        profile = value["properties"]["character_profile"]
        values = profile["values"]
        skills = profile["skills"]
    except (KeyError, TypeError) as exc:
        raise AIDecisionError("Creator Character output is missing the exact Character seed structure") from exc

    if not isinstance(values, dict) or not isinstance(skills, list):
        raise AIDecisionError("Creator Character profile values/skills have invalid structure")

    actual_value_keys = set(str(key) for key in values)
    missing_values = sorted(expected_value_keys - actual_value_keys)
    extra_values = sorted(actual_value_keys - expected_value_keys)
    if missing_values or extra_values:
        details: list[str] = []
        if missing_values:
            details.append("missing=" + ", ".join(missing_values))
        if extra_values:
            details.append("extra=" + ", ".join(extra_values))
        raise AIDecisionError("Creator Character seed profile keys do not match the canonical template: " + "; ".join(details))

    try:
        normalized = normalize_creator_skills(item for item in skills if isinstance(item, dict))
    except ValueError as exc:
        raise AIDecisionError(str(exc)) from exc
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
    """Run one real structured inference through the existing provider registry."""
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
    _validate_creator_character_contract(value, schema, schema_name)
    return value

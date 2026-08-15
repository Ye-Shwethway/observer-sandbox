from __future__ import annotations

import json
import os
import sqlite3
import urllib.error
import urllib.request
from typing import Any

from .ai import AIConfigurationError, resolve_binding
from .ai_fallback import get_fallback_binding, record_fallback_use
from .duration_planning import enrich_action_options, normalize_duration
from .secrets import load_runtime_secrets


class AIDecisionError(RuntimeError):
    pass


DECISION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "action": {"type": "string"},
        "duration_minutes": {"type": "integer", "minimum": 1, "maximum": 720},
        "target": {"type": "string"},
        "reason": {"type": "string"},
        "resources": {
            "type": "array",
            "maxItems": 6,
            "items": {
                "type": "object",
                "properties": {
                    "stack_id": {"type": "string"},
                    "quantity": {"type": "number", "exclusiveMinimum": 0},
                },
                "required": ["stack_id", "quantity"],
                "additionalProperties": False,
            },
        },
        "training_movements": {
            "type": "array",
            "maxItems": 4,
            "items": {"type": "string"},
        },
    },
    "required": ["action", "duration_minutes", "target", "reason", "resources", "training_movements"],
    "additionalProperties": False,
}


def _post_json(url: str, *, headers: dict[str, str], payload: dict[str, Any], timeout: float = 45.0) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": "observer-sandbox/0.0.1",
            **headers,
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read().decode("utf-8", errors="replace").strip()
        except Exception:
            body = ""
        detail = f"HTTP {exc.code}: {exc.reason}"
        if body:
            detail = f"{detail}: {body[:1000]}"
        raise AIDecisionError(detail) from exc
    except Exception as exc:
        raise AIDecisionError(str(exc)) from exc


def _provider_and_key(conn: sqlite3.Connection, provider_id: str) -> tuple[sqlite3.Row, str]:
    load_runtime_secrets()
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


def _compact_prompt_state(state: dict[str, Any]) -> dict[str, Any]:
    """Remove duplicated derived metadata while preserving decision semantics."""
    prompt_state = dict(state)

    policy = prompt_state.get("autonomy_policy")
    if isinstance(policy, dict):
        prompt_state["autonomy_policy"] = {
            key: policy[key]
            for key in ("policy_revision", "decision_principles", "reason_style")
            if key in policy
        }

    familiarity = prompt_state.get("object_familiarity")
    if isinstance(familiarity, dict):
        prompt_state["object_familiarity"] = {
            key: familiarity[key]
            for key in ("source", "suppressed_inspect_count", "guidance")
            if key in familiarity
        }

    options = prompt_state.get("action_options")
    if isinstance(options, list):
        compact_options: list[dict[str, Any]] = []
        for raw in enrich_action_options(options):
            option = dict(raw)
            option.pop("training_load_guard", None)
            compact_options.append(option)
        prompt_state["action_options"] = compact_options

    return prompt_state


def _decision_prompt(state: dict[str, Any], available_actions: list[str]) -> str:
    prompt_state = _compact_prompt_state(state)
    return (
        "You control one autonomous simulated human. Choose exactly one next action. "
        "Act consistently with the supplied character traits, preferences, habits, skills, routine guidance, recent events, current time, and physiological state. "
        "Physiological needs and safety override routine preferences. Do not invent rooms, objects, actions, inventory stacks, movement ids, or direct state changes.\n\n"
        f"Known action vocabulary: {json.dumps(available_actions)}\n"
        f"Runtime context: {json.dumps(prompt_state, ensure_ascii=False, sort_keys=True)}\n\n"
        "The action_options array is authoritative. Choose an action/target pair that appears there. "
        "The solo_sexual_regulation context is also authoritative when present: it describes adult eligibility, current non-clinical drive, privacy/aloneness, recent release history, and reachable safe private rooms. "
        "Self-satisfaction is a legitimate discretionary self-regulation option only when it appears in action_options; it is never a weekly quota, mandatory routine, or reason to ignore a stronger physiological/safety need. "
        "If solo drive is meaningful but the current room is not safe/private, reachable_safe_private_locations may justify an ordinary move before reconsidering the behavior later. "
        "The duration field is the broad legal compatibility range. When preferred_duration is present, choose duration_minutes inside that narrower planning range; duration_purpose explains the intended ordinary use. "
        "Runtime-shaped legal duration bounds override ordinary authored preferences when they are tighter. "
        "For an eat action, choose one or more resources only from that option's meal_resources list. Copy each exact stack_id and choose a quantity within its min_quantity/max_quantity bounds. The engine calculates nutrients; do not invent or calculate macro values. "
        "For every non-eat action, resources must be an empty array. "
        "For a train action whose training_method has movement_options, choose one to four exact movement_id values from that selected option and return them in training_movements. Prefer movements that make the session coherent rather than an arbitrary full-catalog mix. "
        "For train actions without movement_options and for every non-train action, training_movements must be an empty array. "
        "For any selected option whose target is null, return an empty target string. Otherwise copy the exact target id from action_options. "
        "Return only the structured decision and keep reason short and character-grounded."
    )


def _generate_nanogpt(provider: sqlite3.Row, key: str, model_id: str, prompt: str, parameters: dict[str, Any]) -> dict[str, Any]:
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError("NanoGPT base_url is not configured")
    payload: dict[str, Any] = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "observer_sandbox_decision", "strict": True, "schema": DECISION_SCHEMA},
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


def _generate_openai_compatible(provider: sqlite3.Row, key: str, model_id: str, prompt: str, parameters: dict[str, Any]) -> dict[str, Any]:
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError(f"Provider {provider['id']} base_url is not configured")
    payload: dict[str, Any] = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "response_format": {
            "type": "json_schema",
            "json_schema": {"name": "observer_sandbox_decision", "strict": True, "schema": DECISION_SCHEMA},
        },
    }
    payload.update(parameters)
    response = _post_json(
        f"{base.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
        payload=payload,
    )
    try:
        content = response["choices"][0]["message"]["content"]
        return json.loads(content) if isinstance(content, str) else content
    except Exception as exc:
        raise AIDecisionError(f"Provider {provider['id']} returned an unusable structured decision") from exc


def _generate_gemini(provider: sqlite3.Row, key: str, model_id: str, prompt: str, parameters: dict[str, Any]) -> dict[str, Any]:
    base = provider["base_url"]
    if not base:
        raise AIConfigurationError("Gemini base_url is not configured")
    generation_config = {"responseMimeType": "application/json", "responseJsonSchema": DECISION_SCHEMA, **parameters}
    response = _post_json(
        f"{base.rstrip('/')}/models/{model_id}:generateContent",
        headers={"x-goog-api-key": key, "Accept": "application/json"},
        payload={"contents": [{"parts": [{"text": prompt}]}], "generationConfig": generation_config},
    )
    try:
        text = response["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(text)
    except Exception as exc:
        raise AIDecisionError("Gemini returned an unusable structured decision") from exc


def _generate_for_binding(
    conn: sqlite3.Connection,
    binding: dict[str, Any],
    prompt: str,
) -> dict[str, Any]:
    provider, key = _provider_and_key(conn, str(binding["provider_id"]))
    parameters = binding.get("parameters") or {}
    adapter = str(provider["adapter_type"])
    if adapter == "nanogpt":
        return _generate_nanogpt(provider, key, str(binding["model_id"]), prompt, parameters)
    if adapter == "gemini":
        return _generate_gemini(provider, key, str(binding["model_id"]), prompt, parameters)
    if adapter == "openai_compatible":
        return _generate_openai_compatible(provider, key, str(binding["model_id"]), prompt, parameters)
    raise AIConfigurationError(f"P1 live decision adapter not yet enabled for provider type: {adapter}")


def _provider_decision_with_fallback(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    role: str,
    primary_binding: dict[str, Any],
    prompt: str,
) -> dict[str, Any]:
    try:
        return _generate_for_binding(conn, primary_binding, prompt)
    except (AIDecisionError, AIConfigurationError) as primary_exc:
        fallback = get_fallback_binding(conn, character_id=character_id, role=role)
        if not fallback:
            raise
        primary_pair = (str(primary_binding["provider_id"]), str(primary_binding["model_id"]))
        fallback_pair = (str(fallback["provider_id"]), str(fallback["model_id"]))
        if fallback_pair == primary_pair:
            raise
        try:
            decision = _generate_for_binding(conn, fallback, prompt)
        except (AIDecisionError, AIConfigurationError) as fallback_exc:
            raise AIDecisionError(
                "Primary cognition provider/model failed and configured fallback also failed. "
                f"Primary: {str(primary_exc)[:450]} | Fallback: {str(fallback_exc)[:450]}"
            ) from fallback_exc
        record_fallback_use(
            conn,
            character_id=character_id,
            role=role,
            primary_provider_id=primary_pair[0],
            primary_model_id=primary_pair[1],
            fallback_provider_id=fallback_pair[0],
            fallback_model_id=fallback_pair[1],
            primary_error=str(primary_exc),
        )
        return decision


def _bounds(value: Any) -> tuple[int, int] | None:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        return None
    low, high = int(value[0]), int(value[1])
    if low <= 0 or high < low:
        return None
    return low, high


def _normalize_decision_duration(state: dict[str, Any], decision: dict[str, Any]) -> int:
    action = str(decision["action"])
    target = decision["target"] or None
    requested = int(decision["duration_minutes"])
    options = state.get("action_options")
    if isinstance(options, list):
        for raw_option in options:
            option = dict(raw_option)
            option_target = option.get("target") if isinstance(option.get("target"), str) else None
            if str(option.get("action")) != action or option_target != target:
                continue
            enriched_option = enrich_action_options([option])[0]
            preferred = _bounds(enriched_option.get("preferred_duration"))
            legal = _bounds(enriched_option.get("duration"))
            selected = preferred or legal
            if selected is not None:
                low, high = selected
                return max(low, min(high, requested))
            break
    return normalize_duration(action, target, requested)


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
    prompt = _decision_prompt(state, available_actions)
    decision = _provider_decision_with_fallback(
        conn,
        character_id=character_id,
        role=role,
        primary_binding=binding,
        prompt=prompt,
    )

    # Validation remains outside the provider/fallback boundary. An invalid
    # action/target/duration/resources result from a responding model is a
    # deterministic decision-validation failure and must never be hidden by
    # provider fallback.
    if not isinstance(decision, dict):
        raise AIDecisionError("AI decision must be a JSON object")
    legacy_required = {"action", "duration_minutes", "target", "reason"}
    eating_required = legacy_required | {"resources"}
    required = eating_required | {"training_movements"}
    if set(decision) == legacy_required:
        decision = {**decision, "resources": [], "training_movements": []}
    elif set(decision) == eating_required:
        decision = {**decision, "training_movements": []}
    if set(decision) != required:
        raise AIDecisionError("AI decision keys do not match the required schema")
    if decision["action"] not in available_actions:
        raise AIDecisionError(f"AI selected unavailable action: {decision['action']}")
    if not isinstance(decision["duration_minutes"], int) or not 1 <= decision["duration_minutes"] <= 720:
        raise AIDecisionError("AI duration_minutes is out of bounds")
    if not isinstance(decision["target"], str) or not isinstance(decision["reason"], str):
        raise AIDecisionError("AI target/reason must be strings")
    if not isinstance(decision["resources"], list):
        raise AIDecisionError("AI resources must be an array")
    for resource in decision["resources"]:
        if not isinstance(resource, dict) or set(resource) != {"stack_id", "quantity"}:
            raise AIDecisionError("AI resource entries must contain exactly stack_id and quantity")
        if not isinstance(resource["stack_id"], str) or not isinstance(resource["quantity"], (int, float)):
            raise AIDecisionError("AI resource stack_id/quantity types are invalid")
        if float(resource["quantity"]) <= 0.0:
            raise AIDecisionError("AI resource quantity must be positive")
    if not isinstance(decision["training_movements"], list) or len(decision["training_movements"]) > 4:
        raise AIDecisionError("AI training_movements must be an array with at most four items")
    if not all(isinstance(item, str) and item for item in decision["training_movements"]):
        raise AIDecisionError("AI training_movements entries must be non-empty strings")
    if decision["action"] != "train" and decision["training_movements"]:
        raise AIDecisionError("AI training_movements must be empty for non-training actions")
    decision = dict(decision)
    decision["duration_minutes"] = _normalize_decision_duration(state, decision)
    return decision

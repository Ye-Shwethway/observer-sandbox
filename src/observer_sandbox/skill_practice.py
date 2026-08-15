from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_PRACTICE_CONFIG_PATH = REPO_ROOT / "config" / "skill_practice_methods.v1.json"


@lru_cache(maxsize=1)
def load_skill_practice_config(path: str | Path = SKILL_PRACTICE_CONFIG_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def practice_method_for_target(
    target_id: str | None,
    *,
    config: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not target_id:
        return None
    source = config if config is not None else load_skill_practice_config()
    method_id = (source.get("target_bindings") or {}).get(target_id)
    if not isinstance(method_id, str) or not method_id:
        return None
    raw = (source.get("methods") or {}).get(method_id)
    if not isinstance(raw, dict):
        return None
    result = dict(raw)
    result["method_id"] = method_id
    result["revision"] = str(source.get("revision") or "skill-practice-methods-v1")
    return result


def is_registered_practice_target(target_id: str | None) -> bool:
    return practice_method_for_target(target_id) is not None


def validate_practice_target(
    *,
    action_name: str,
    target_id: str | None,
    duration_minutes: int,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    method = practice_method_for_target(target_id, config=config)
    if method is None:
        raise ValueError(f"Target {target_id} is not a registered skill-practice target")
    expected_action = str(method.get("action") or "practice")
    if action_name != expected_action:
        raise ValueError(f"Practice method {method['method_id']} requires action {expected_action}")
    minimum = int(method.get("min_duration_minutes") or 1)
    if int(duration_minutes) < minimum:
        raise ValueError(f"Practice method {method['method_id']} requires at least {minimum} minutes")
    relevance = method.get("skill_relevance")
    if not isinstance(relevance, dict) or not any(
        isinstance(value, (int, float)) and float(value) > 0.0 for value in relevance.values()
    ):
        raise ValueError(f"Practice method {method['method_id']} has no positive skill relevance")
    return method


def skill_practice_evidence(
    *,
    action_name: str,
    target_id: str | None,
    duration_minutes: int,
    config: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if action_name != "practice":
        return None
    method = validate_practice_target(
        action_name=action_name,
        target_id=target_id,
        duration_minutes=duration_minutes,
        config=config,
    )
    relevance = {
        str(key): float(value)
        for key, value in (method.get("skill_relevance") or {}).items()
        if isinstance(value, (int, float)) and float(value) > 0.0
    }
    return {
        "source": "skill-evidence-semantics-v1",
        "revision": method["revision"],
        "method_id": method["method_id"],
        "method_name": str(method.get("name") or method["method_id"]),
        "target_id": target_id,
        "effective_load": {
            "planned_minutes": int(duration_minutes),
            "effective_minutes": float(duration_minutes),
            "quality": 1.0,
        },
        "skill_relevance": relevance,
        "tags": list(method.get("tags") or []),
    }


def skill_practice_evidence_from_event(payload: dict[str, Any]) -> dict[str, Any] | None:
    value = payload.get("skill_practice")
    return value if isinstance(value, dict) else None

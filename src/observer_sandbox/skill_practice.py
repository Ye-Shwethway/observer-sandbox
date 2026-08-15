from __future__ import annotations

import json
import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_PRACTICE_CONFIG_PATH = REPO_ROOT / "config" / "skill_practice_methods.v1.json"
PRACTICE_ACTION = "practice"
PRACTICE_SOURCE = "skill-evidence-semantics-v1"


@lru_cache(maxsize=1)
def load_skill_practice_config(path: str | Path = SKILL_PRACTICE_CONFIG_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _target_definition(
    target_id: str | None,
    *,
    config: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not target_id:
        return None
    source = config if config is not None else load_skill_practice_config()
    raw = (source.get("targets") or {}).get(target_id)
    if not isinstance(raw, dict):
        return None
    result = dict(raw)
    result["target_id"] = target_id
    result["revision"] = str(source.get("revision") or "skill-practice-methods-v1")
    return result


def practice_method_for_target(
    target_id: str | None,
    *,
    config: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    source = config if config is not None else load_skill_practice_config()
    target = _target_definition(target_id, config=source)
    if target is None:
        return None
    method_id = target.get("method_id")
    if not isinstance(method_id, str) or not method_id:
        return None
    raw = (source.get("methods") or {}).get(method_id)
    if not isinstance(raw, dict):
        return None
    result = dict(raw)
    result["method_id"] = method_id
    result["revision"] = str(source.get("revision") or "skill-practice-methods-v1")
    result["target"] = target
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
    expected_action = str(method.get("action") or PRACTICE_ACTION)
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
    if action_name != PRACTICE_ACTION:
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
        "source": PRACTICE_SOURCE,
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


def seed_skill_practice_foundation(
    conn: sqlite3.Connection,
    *,
    config: dict[str, Any] | None = None,
) -> None:
    source = config if config is not None else load_skill_practice_config()
    revision = str(source.get("revision") or "skill-practice-methods-v1")

    conn.execute(
        """
        INSERT INTO action_definitions(
            action_type,label,min_duration_minutes,max_duration_minutes,target_mode,
            required_capability,requires_colocation,base_effects_json,conditions_json,modifiers_json,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(action_type) DO UPDATE SET
            label=excluded.label,
            min_duration_minutes=excluded.min_duration_minutes,
            max_duration_minutes=excluded.max_duration_minutes,
            target_mode=excluded.target_mode,
            required_capability=excluded.required_capability,
            requires_colocation=excluded.requires_colocation,
            metadata_json=excluded.metadata_json,
            updated_at=CURRENT_TIMESTAMP
        """,
        (
            PRACTICE_ACTION,
            "Practice",
            5,
            180,
            "object",
            PRACTICE_ACTION,
            1,
            json.dumps({}),
            json.dumps({}),
            json.dumps({}),
            json.dumps({"source": PRACTICE_SOURCE, "revision": revision}, sort_keys=True),
        ),
    )

    methods = source.get("methods") or {}
    targets = source.get("targets") or {}
    if not isinstance(methods, dict) or not isinstance(targets, dict):
        raise ValueError("Skill practice config requires object-valued methods and targets")

    for target_id, target in targets.items():
        if not isinstance(target_id, str) or not isinstance(target, dict):
            raise ValueError("Invalid skill practice target definition")
        method_id = target.get("method_id")
        if not isinstance(method_id, str) or method_id not in methods:
            raise ValueError(f"Skill practice target {target_id} references unknown method {method_id}")
        room_id = target.get("room")
        if not isinstance(room_id, str) or conn.execute(
            "SELECT 1 FROM entities WHERE id=? AND entity_type='location'", (room_id,)
        ).fetchone() is None:
            raise ValueError(f"Skill practice target {target_id} references unknown room {room_id}")
        capabilities = target.get("capabilities") or ["inspect", PRACTICE_ACTION]
        if not isinstance(capabilities, list) or PRACTICE_ACTION not in capabilities:
            raise ValueError(f"Skill practice target {target_id} must advertise practice capability")
        name = str(target.get("name") or target_id)
        conn.execute(
            """
            INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id)
            VALUES(?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
                entity_type=excluded.entity_type,
                name=excluded.name,
                capabilities_json=excluded.capabilities_json,
                definition_id=excluded.definition_id,
                updated_at=CURRENT_TIMESTAMP
            """,
            (target_id, "object", name, json.dumps(capabilities), f"skill_practice:{method_id}"),
        )
        conn.execute("DELETE FROM relations WHERE relation_type='contains' AND target_id=?", (target_id,))
        conn.execute(
            "INSERT OR IGNORE INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
            (room_id, "contains", target_id),
        )
    conn.commit()

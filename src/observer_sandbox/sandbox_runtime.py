from __future__ import annotations

import json
import sqlite3
import time
from datetime import datetime, timezone
from typing import Any, Iterable, Mapping

from .creation_sandbox import (
    CreationSandboxError,
    DEFAULT_SANDBOX_ID,
    ensure_sandbox,
    get_sandbox_object,
)


class SandboxRuntimeError(ValueError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _loads(value: str | None, fallback: Any) -> Any:
    try:
        return json.loads(value or "")
    except (TypeError, json.JSONDecodeError):
        return fallback


def _require_character(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    try:
        obj = get_sandbox_object(conn, object_id)
    except CreationSandboxError as exc:
        raise SandboxRuntimeError(str(exc)) from exc
    if obj["creation_type"] != "character":
        raise SandboxRuntimeError("Sandbox runtime target must be a character")
    if obj["lifecycle_status"] != "active":
        raise SandboxRuntimeError("Archived sandbox Character cannot enter runtime")
    return obj


def _ensure_actor_runtime(conn: sqlite3.Connection, character: Mapping[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO creation_sandbox_actor_runtime(object_id,sandbox_id,activation_status)
        VALUES(?,?,'created')
        ON CONFLICT(object_id) DO NOTHING
        """,
        (character["object_id"], character["sandbox_id"]),
    )


def ensure_sandbox_runtime(
    conn: sqlite3.Connection,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    ensure_sandbox(conn, sandbox_id)
    conn.execute(
        """
        INSERT INTO creation_sandbox_runtime(sandbox_id,sim_time,speed,paused,runtime_status)
        VALUES(?,NULL,1.0,1,'stopped')
        ON CONFLICT(sandbox_id) DO NOTHING
        """,
        (sandbox_id,),
    )
    conn.commit()
    return sandbox_runtime_status(conn, sandbox_id)


def sandbox_runtime_status(
    conn: sqlite3.Connection,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    ensure_sandbox(conn, sandbox_id)
    row = conn.execute(
        """
        SELECT sandbox_id,sim_time,speed,paused,pause_started_wall_time,runtime_status,updated_at
        FROM creation_sandbox_runtime WHERE sandbox_id=?
        """,
        (sandbox_id,),
    ).fetchone()
    if row is None:
        return {
            "sandbox_id": sandbox_id,
            "sim_time": None,
            "speed": 1.0,
            "paused": True,
            "pause_started_wall_time": None,
            "runtime_status": "stopped",
            "configured": False,
            "updated_at": None,
        }
    result = dict(row)
    result["speed"] = float(result["speed"])
    result["paused"] = bool(result["paused"])
    result["configured"] = bool(result["sim_time"])
    return result


def configure_sandbox_clock(
    conn: sqlite3.Connection,
    sim_time: str | datetime,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    ensure_sandbox_runtime(conn, sandbox_id)
    if isinstance(sim_time, datetime):
        value = sim_time
    else:
        try:
            value = datetime.fromisoformat(str(sim_time).replace("Z", "+00:00"))
        except ValueError as exc:
            raise SandboxRuntimeError("Sandbox sim_time must be ISO-8601") from exc
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    normalized = value.isoformat()
    conn.execute(
        """
        UPDATE creation_sandbox_runtime
        SET sim_time=?,runtime_status=CASE WHEN runtime_status='running' THEN 'running' ELSE 'stopped' END,
            updated_at=CURRENT_TIMESTAMP
        WHERE sandbox_id=?
        """,
        (normalized, sandbox_id),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,NULL,'sandbox_clock_configured',?)",
        (sandbox_id, _json({"sim_time": normalized})),
    )
    conn.commit()
    return sandbox_runtime_status(conn, sandbox_id)


def set_sandbox_speed(
    conn: sqlite3.Connection,
    speed: float,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    ensure_sandbox_runtime(conn, sandbox_id)
    value = float(speed)
    if value <= 0 or value > 3600:
        raise SandboxRuntimeError("Sandbox speed must be greater than 0 and at most 3600")
    previous = sandbox_runtime_status(conn, sandbox_id)["speed"]
    conn.execute(
        "UPDATE creation_sandbox_runtime SET speed=?,updated_at=CURRENT_TIMESTAMP WHERE sandbox_id=?",
        (value, sandbox_id),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,NULL,'sandbox_speed_changed',?)",
        (sandbox_id, _json({"previous_speed": previous, "speed": value})),
    )
    conn.commit()
    return sandbox_runtime_status(conn, sandbox_id)


def set_sandbox_paused(
    conn: sqlite3.Connection,
    paused: bool,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    now_wall: float | None = None,
) -> dict[str, Any]:
    ensure_sandbox_runtime(conn, sandbox_id)
    now = time.time() if now_wall is None else float(now_wall)
    current = sandbox_runtime_status(conn, sandbox_id)
    pause_started = current["pause_started_wall_time"]
    if paused and not current["paused"]:
        pause_started = now
    elif not paused:
        pause_started = None
    conn.execute(
        """
        UPDATE creation_sandbox_runtime
        SET paused=?,pause_started_wall_time=?,updated_at=CURRENT_TIMESTAMP
        WHERE sandbox_id=?
        """,
        (int(bool(paused)), pause_started, sandbox_id),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,NULL,?,?)",
        (
            sandbox_id,
            "sandbox_paused" if paused else "sandbox_resumed",
            _json({"paused": bool(paused)}),
        ),
    )
    conn.commit()
    return sandbox_runtime_status(conn, sandbox_id)


def bind_sandbox_character_ai(
    conn: sqlite3.Connection,
    character_object_id: str,
    provider_id: str,
    model_id: str,
    *,
    role: str = "cognition",
    parameters: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    character = _require_character(conn, character_object_id)
    role = str(role or "").strip() or "cognition"
    model = conn.execute(
        """
        SELECT m.provider_id,m.model_id,m.display_name,p.display_name AS provider_name
        FROM ai_models m JOIN ai_providers p ON p.id=m.provider_id
        WHERE m.provider_id=? AND m.model_id=? AND m.active=1 AND p.enabled=1
        """,
        (provider_id, model_id),
    ).fetchone()
    if model is None:
        raise SandboxRuntimeError(f"Unknown, inactive, or disabled model: {provider_id}/{model_id}")
    conn.execute(
        """
        INSERT INTO creation_sandbox_ai_bindings(
            sandbox_id,object_id,role,provider_id,model_id,parameters_json,enabled
        ) VALUES(?,?,?,?,?,?,1)
        ON CONFLICT(sandbox_id,object_id,role) DO UPDATE SET
            provider_id=excluded.provider_id,
            model_id=excluded.model_id,
            parameters_json=excluded.parameters_json,
            enabled=1,
            updated_at=CURRENT_TIMESTAMP
        """,
        (
            character["sandbox_id"],
            character_object_id,
            role,
            provider_id,
            model_id,
            _json(dict(parameters or {})),
        ),
    )
    _ensure_actor_runtime(conn, character)
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_ai_bound', ?)",
        (
            character["sandbox_id"],
            character_object_id,
            _json({"role": role, "provider_id": provider_id, "model_id": model_id}),
        ),
    )
    conn.commit()
    return sandbox_character_ai_binding(conn, character_object_id, role=role) or {}


def sandbox_character_ai_binding(
    conn: sqlite3.Connection,
    character_object_id: str,
    *,
    role: str = "cognition",
) -> dict[str, Any] | None:
    character = _require_character(conn, character_object_id)
    row = conn.execute(
        """
        SELECT b.sandbox_id,b.object_id,b.role,b.provider_id,b.model_id,b.parameters_json,
               m.display_name AS model_name,p.display_name AS provider_name
        FROM creation_sandbox_ai_bindings b
        JOIN ai_models m ON m.provider_id=b.provider_id AND m.model_id=b.model_id
        JOIN ai_providers p ON p.id=b.provider_id
        WHERE b.sandbox_id=? AND b.object_id=? AND b.role=? AND b.enabled=1
        """,
        (character["sandbox_id"], character_object_id, role),
    ).fetchone()
    if row is None:
        return None
    result = dict(row)
    result["parameters"] = _loads(result.pop("parameters_json"), {})
    return result


def replace_sandbox_runtime_options(
    conn: sqlite3.Connection,
    character_object_id: str,
    options: Iterable[Mapping[str, Any] | str],
) -> list[dict[str, Any]]:
    character = _require_character(conn, character_object_id)
    normalized: list[dict[str, Any]] = []
    for raw in options:
        if isinstance(raw, str):
            action_key = raw.strip()
            source_object_id = None
            metadata: dict[str, Any] = {}
        else:
            action_key = str(raw.get("action_key") or "").strip()
            source_object_id = raw.get("source_object_id")
            source_object_id = None if source_object_id is None else str(source_object_id)
            metadata = dict(raw.get("metadata") or {})
        if not action_key:
            raise SandboxRuntimeError("Sandbox runtime option requires action_key")
        if source_object_id:
            source = get_sandbox_object(conn, source_object_id)
            if source["sandbox_id"] != character["sandbox_id"]:
                raise SandboxRuntimeError("Runtime option source cannot cross sandbox namespaces")
            if source["lifecycle_status"] != "active":
                raise SandboxRuntimeError("Runtime option source must be active")
        normalized.append(
            {
                "action_key": action_key,
                "source_object_id": source_object_id,
                "metadata": metadata,
            }
        )
    conn.execute(
        "DELETE FROM creation_sandbox_runtime_options WHERE sandbox_id=? AND character_object_id=?",
        (character["sandbox_id"], character_object_id),
    )
    for option in normalized:
        conn.execute(
            """
            INSERT INTO creation_sandbox_runtime_options(
                sandbox_id,character_object_id,action_key,source_object_id,metadata_json,enabled
            ) VALUES(?,?,?,?,?,1)
            """,
            (
                character["sandbox_id"],
                character_object_id,
                option["action_key"],
                option["source_object_id"],
                _json(option["metadata"]),
            ),
        )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_runtime_options_changed', ?)",
        (
            character["sandbox_id"],
            character_object_id,
            _json({"count": len(normalized), "actions": [value["action_key"] for value in normalized]}),
        ),
    )
    conn.commit()
    return sandbox_runtime_options(conn, character_object_id)


def sandbox_runtime_options(
    conn: sqlite3.Connection,
    character_object_id: str,
) -> list[dict[str, Any]]:
    character = _require_character(conn, character_object_id)
    rows = conn.execute(
        """
        SELECT action_key,source_object_id,metadata_json
        FROM creation_sandbox_runtime_options
        WHERE sandbox_id=? AND character_object_id=? AND enabled=1
        ORDER BY action_key,id
        """,
        (character["sandbox_id"], character_object_id),
    ).fetchall()
    return [
        {
            "action_key": str(row["action_key"]),
            "source_object_id": row["source_object_id"],
            "metadata": _loads(row["metadata_json"], {}),
        }
        for row in rows
    ]


def sandbox_character_readiness(
    conn: sqlite3.Connection,
    character_object_id: str,
) -> dict[str, Any]:
    character = _require_character(conn, character_object_id)
    _ensure_actor_runtime(conn, character)
    actor = conn.execute(
        "SELECT * FROM creation_sandbox_actor_runtime WHERE object_id=?",
        (character_object_id,),
    ).fetchone()
    location_id = actor["current_location_object_id"] if actor else None
    if not location_id:
        relation = conn.execute(
            """
            SELECT target_object_id FROM creation_sandbox_relations
            WHERE sandbox_id=? AND source_object_id=? AND relation_type='located_in'
            ORDER BY id DESC LIMIT 1
            """,
            (character["sandbox_id"], character_object_id),
        ).fetchone()
        location_id = relation["target_object_id"] if relation else None
    location_ok = False
    if location_id:
        row = conn.execute(
            """
            SELECT creation_type,lifecycle_status FROM creation_sandbox_objects
            WHERE object_id=? AND sandbox_id=?
            """,
            (location_id, character["sandbox_id"]),
        ).fetchone()
        location_ok = bool(row and row["creation_type"] == "location" and row["lifecycle_status"] == "active")

    runtime = sandbox_runtime_status(conn, character["sandbox_id"])
    binding = sandbox_character_ai_binding(conn, character_object_id, role="cognition")
    options = sandbox_runtime_options(conn, character_object_id)

    gates = {
        "character_active": True,
        "location_assigned": location_ok,
        "runtime_options_available": bool(options),
        "cognition_ai_bound": binding is not None,
        "clock_configured": bool(runtime["configured"]),
    }
    missing = [key for key, value in gates.items() if not value]
    ready = not missing
    status = "runtime_ready" if ready else "configured" if any(gates.values()) else "created"
    conn.execute(
        """
        UPDATE creation_sandbox_actor_runtime
        SET activation_status=?,current_location_object_id=?,autonomy_enabled=0,updated_at=CURRENT_TIMESTAMP
        WHERE object_id=?
        """,
        (status, location_id if location_ok else None, character_object_id),
    )
    conn.commit()
    return {
        "sandbox_id": character["sandbox_id"],
        "character_object_id": character_object_id,
        "ready": ready,
        "activation_status": status,
        "gates": gates,
        "missing": missing,
        "location_object_id": location_id if location_ok else None,
        "runtime_options": options,
        "ai_binding": binding,
        "runtime": runtime,
    }


__all__ = [
    "SandboxRuntimeError",
    "bind_sandbox_character_ai",
    "configure_sandbox_clock",
    "ensure_sandbox_runtime",
    "replace_sandbox_runtime_options",
    "sandbox_character_ai_binding",
    "sandbox_character_readiness",
    "sandbox_runtime_options",
    "sandbox_runtime_status",
    "set_sandbox_paused",
    "set_sandbox_speed",
]

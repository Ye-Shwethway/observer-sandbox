from __future__ import annotations

import sqlite3
import time
from datetime import datetime, timezone
from typing import Any

from .ai import AIConfigurationError, resolve_binding, set_binding
from .creation_socket import validate_creation_proposal
from .structured_ai import generate_structured


CREATION_SCOPE_TYPE = "engine"
CREATION_SCOPE_ID = "creator_creation"
CREATION_ROLE = "creator_creation_assist"

CREATION_PROBE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "proposal_version": {"type": "integer", "enum": [1]},
        "creation_type": {"type": "string", "enum": ["location"]},
        "schema_version": {"type": "integer", "enum": [1]},
        "target_scope": {"type": "string", "enum": ["sandbox"]},
        "identity": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
            "additionalProperties": False,
        },
        "properties": {"type": "object"},
        "relationships": {"type": "array", "items": {"type": "object"}},
        "capabilities": {"type": "array", "items": {"type": "string"}},
        "provenance": {
            "type": "object",
            "properties": {
                "mode": {"type": "string", "enum": ["ai_generated"]},
                "requested_by": {"type": ["string", "null"]},
            },
            "required": ["mode", "requested_by"],
            "additionalProperties": False,
        },
    },
    "required": [
        "proposal_version",
        "creation_type",
        "schema_version",
        "target_scope",
        "identity",
        "properties",
        "relationships",
        "capabilities",
        "provenance",
    ],
    "additionalProperties": False,
}


def creator_creation_binding(conn: sqlite3.Connection) -> dict[str, Any] | None:
    return resolve_binding(conn, role=CREATION_ROLE, engine_id=CREATION_SCOPE_ID)


def activate_creator_creation_model(
    conn: sqlite3.Connection, provider_id: str, model_id: str
) -> dict[str, Any]:
    conn.execute(
        "UPDATE ai_providers SET enabled=1,updated_at=CURRENT_TIMESTAMP WHERE id=?",
        (provider_id,),
    )
    set_binding(
        conn,
        scope_type=CREATION_SCOPE_TYPE,
        scope_id=CREATION_SCOPE_ID,
        role=CREATION_ROLE,
        provider_id=provider_id,
        model_id=model_id,
    )
    binding = creator_creation_binding(conn)
    if binding is None:
        raise AIConfigurationError("Creator Creation AI binding did not persist")
    return binding


def probe_creator_creation_model(
    conn: sqlite3.Connection, provider_id: str, model_id: str
) -> dict[str, Any]:
    before = creator_creation_binding(conn)
    prompt = (
        "Creator Creation AI capability probe. Produce one harmless fictional location draft "
        "for the isolated Creation Sandbox. This is proposal generation only: do not claim it "
        "exists in the canonical universe and do not request transmigration. Return exactly the "
        "required structured schema. Use proposal_version=1, creation_type='location', "
        "schema_version=1, target_scope='sandbox', provenance.mode='ai_generated', and "
        "provenance.requested_by=null. Give the location a short non-empty name."
    )
    started = time.perf_counter()
    value = generate_structured(
        conn,
        provider_id=provider_id,
        model_id=model_id,
        prompt=prompt,
        schema=CREATION_PROBE_SCHEMA,
        schema_name="observer_sandbox_creator_creation_probe",
    )
    validate_creation_proposal(value)
    after = creator_creation_binding(conn)
    if before != after:
        raise RuntimeError("Creator Creation AI probe mutated the active binding")
    return {
        "ok": True,
        "provider_id": provider_id,
        "model_id": model_id,
        "latency_ms": int((time.perf_counter() - started) * 1000),
        "tested_at": datetime.now(timezone.utc).isoformat(),
    }


__all__ = [
    "CREATION_ROLE",
    "CREATION_SCOPE_ID",
    "CREATION_SCOPE_TYPE",
    "activate_creator_creation_model",
    "creator_creation_binding",
    "probe_creator_creation_model",
]

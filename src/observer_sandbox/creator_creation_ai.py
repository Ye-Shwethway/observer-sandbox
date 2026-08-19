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
        "creation_type": {"type": "string", "enum": ["character"]},
        "schema_version": {"type": "integer", "enum": [1]},
        "target_scope": {"type": "string", "enum": ["sandbox"]},
        "identity": {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
            "additionalProperties": False,
        },
        "properties": {
            "type": "object",
            "properties": {
                "character_profile": {
                    "type": "object",
                    "properties": {
                        "values": {
                            "type": "object",
                            "properties": {
                                "identity.full_name": {"type": "string"},
                                "identity.date_of_birth": {"type": "string"},
                                "body.height_in": {"type": "number"},
                                "body.weight_lb": {"type": "number"},
                                "genetics.height_max_in": {"type": "number"},
                                "raps_pa.strength": {"type": "number"},
                                "raps_ma.resilience": {"type": "number"},
                                "personality.primary_traits": {"type": "array", "items": {"type": "string"}},
                            },
                            "required": [
                                "identity.full_name",
                                "identity.date_of_birth",
                                "body.height_in",
                                "body.weight_lb",
                                "genetics.height_max_in",
                                "raps_pa.strength",
                                "raps_ma.resilience",
                                "personality.primary_traits",
                            ],
                            "additionalProperties": False,
                        },
                        "skills": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": 3,
                            "items": {
                                "type": "object",
                                "properties": {
                                    "skill_key": {"type": "string"},
                                    "score": {"type": "number"},
                                },
                                "required": ["skill_key", "score"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["values", "skills"],
                    "additionalProperties": False,
                },
                "compatibility_tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["character_profile", "compatibility_tags"],
            "additionalProperties": False,
        },
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


def _validate_character_probe(value: dict[str, Any]) -> None:
    validate_creation_proposal(value)
    profile = value.get("properties", {}).get("character_profile")
    if not isinstance(profile, dict):
        raise ValueError("Creator Creation AI probe omitted character_profile")
    values = profile.get("values")
    if not isinstance(values, dict):
        raise ValueError("Creator Creation AI probe omitted profile values")
    height = float(values["body.height_in"])
    height_max = float(values["genetics.height_max_in"])
    if height <= 0 or height_max <= 0 or height > height_max:
        raise ValueError("Creator Creation AI probe produced impossible height/genetic ceiling")
    for key in ("raps_pa.strength", "raps_ma.resilience"):
        score = float(values[key])
        if not 0 <= score <= 100:
            raise ValueError(f"Creator Creation AI probe produced out-of-range {key}")
    skills = profile.get("skills") or []
    if not skills:
        raise ValueError("Creator Creation AI probe omitted structured skills")
    for skill in skills:
        score = float(skill["score"])
        if not 0 <= score <= 100:
            raise ValueError("Creator Creation AI probe produced out-of-range skill score")


def probe_creator_creation_model(
    conn: sqlite3.Connection, provider_id: str, model_id: str
) -> dict[str, Any]:
    before = creator_creation_binding(conn)
    prompt = (
        "Creator Creation AI capability probe. Produce one harmless fictional adult Character draft for the isolated Creation Sandbox. "
        "This is proposal generation only: do not claim canonical existence and do not request transmigration. Return exactly the "
        "required nested JSON schema. Use proposal_version=1, creation_type='character', schema_version=1, target_scope='sandbox', "
        "provenance.mode='ai_generated', and provenance.requested_by=null. Give the Character a short non-empty name, a valid ISO DOB, "
        "plausible positive height/weight, a genetic height ceiling at least as high as current height, two ordinary 0-100 attributes, "
        "a short personality trait list, and one or two structured skills scored 0-100. Keep all values realistic and internally consistent."
    )
    started = time.perf_counter()
    value = generate_structured(
        conn,
        provider_id=provider_id,
        model_id=model_id,
        prompt=prompt,
        schema=CREATION_PROBE_SCHEMA,
        schema_name="observer_sandbox_creator_creation_character_probe",
    )
    _validate_character_probe(value)
    after = creator_creation_binding(conn)
    if before != after:
        raise RuntimeError("Creator Creation AI probe mutated the active binding")
    return {
        "ok": True,
        "provider_id": provider_id,
        "model_id": model_id,
        "probe_type": "representative_character",
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

from __future__ import annotations

import copy
import json
import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID, activate_creation_proposal, ensure_sandbox
from .creation_socket import build_creation_proposal, validate_creation_proposal
from .creator_creation_ai import creator_creation_binding
from .sandbox_character_facets import (
    replace_sandbox_habits,
    replace_sandbox_hobbies,
    replace_sandbox_preferences,
)
from .sandbox_representation import replace_sandbox_skills, set_sandbox_profile_values
from .structured_ai import generate_structured


class CreatorStudioError(ValueError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _loads(value: str) -> dict[str, Any]:
    loaded = json.loads(value)
    if not isinstance(loaded, dict):
        raise CreatorStudioError("Stored Creator Studio proposal is invalid")
    return loaded


def _profile_value_schema(conn: sqlite3.Connection) -> dict[str, Any]:
    rows = conn.execute(
        "SELECT field_key,data_type FROM profile_field_definitions ORDER BY field_key"
    ).fetchall()
    type_map: dict[str, Any] = {
        "integer": {"type": "integer"},
        "number": {"type": "number"},
        "text": {"type": "string"},
        "boolean": {"type": "boolean"},
        "date": {"type": "string"},
        "datetime": {"type": "string"},
        "json": {"type": ["object", "array", "string", "number", "boolean", "null"]},
    }
    return {
        "type": "object",
        "properties": {str(row["field_key"]): type_map[str(row["data_type"])] for row in rows},
        "additionalProperties": False,
        "minProperties": 4,
    }


def _character_profile_schema(conn: sqlite3.Connection) -> dict[str, Any]:
    return {
        "type": "object",
        "properties": {
            "values": _profile_value_schema(conn),
            "preferences": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "preference_type": {"type": "string", "enum": ["like", "dislike", "interest", "aversion"]},
                        "subject": {"type": "string"},
                        "intensity": {"type": ["number", "null"]},
                    },
                    "required": ["preference_type", "subject", "intensity"],
                    "additionalProperties": False,
                },
            },
            "hobbies": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "proficiency": {"type": ["number", "null"]},
                        "frequency": {"type": ["string", "null"]},
                        "enjoyment": {"type": ["number", "null"]},
                    },
                    "required": ["name", "proficiency", "frequency", "enjoyment"],
                    "additionalProperties": False,
                },
            },
            "habits": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "description": {"type": ["string", "null"]},
                        "frequency": {"type": ["string", "null"]},
                        "strength": {"type": ["number", "null"]},
                    },
                    "required": ["name", "description", "frequency", "strength"],
                    "additionalProperties": False,
                },
            },
            "skills": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "skill_key": {"type": "string"},
                        "category": {"type": ["string", "null"]},
                        "score": {"type": ["number", "null"]},
                        "tier": {"type": ["string", "null"]},
                        "experience": {"type": ["number", "null"]},
                    },
                    "required": ["skill_key", "category", "score", "tier", "experience"],
                    "additionalProperties": False,
                },
            },
        },
        "required": ["values", "preferences", "hobbies", "habits", "skills"],
        "additionalProperties": False,
    }


def _schema(conn: sqlite3.Connection, creation_type: str) -> dict[str, Any]:
    if creation_type not in {"character", "location"}:
        raise CreatorStudioError("Creator Studio currently supports Character and Location")
    properties_schema: dict[str, Any]
    if creation_type == "character":
        properties_schema = {
            "type": "object",
            "properties": {
                "character_profile": _character_profile_schema(conn),
                "compatibility_tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["character_profile", "compatibility_tags"],
            "additionalProperties": False,
        }
    else:
        properties_schema = {"type": "object", "additionalProperties": True}
    return {
        "type": "object",
        "properties": {
            "proposal_version": {"type": "integer", "enum": [1]},
            "creation_type": {"type": "string", "enum": [creation_type]},
            "schema_version": {"type": "integer", "enum": [1]},
            "target_scope": {"type": "string", "enum": ["sandbox"]},
            "identity": {
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"],
                "additionalProperties": True,
            },
            "properties": properties_schema,
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
            "proposal_version", "creation_type", "schema_version", "target_scope",
            "identity", "properties", "relationships", "capabilities", "provenance"
        ],
        "additionalProperties": False,
    }


def _canonical_reference(conn: sqlite3.Connection, prompt_text: str) -> dict[str, Any] | None:
    lowered = prompt_text.lower()
    rows = conn.execute(
        """SELECT e.id,e.name FROM entities e
        JOIN character_profiles p ON p.entity_id=e.id
        WHERE e.entity_type='character' AND p.status='active' ORDER BY length(e.name) DESC"""
    ).fetchall()
    match = next((row for row in rows if str(row["name"]).lower() in lowered), None)
    if match is None:
        return None
    entity_id = str(match["id"])
    values = {
        str(row["field_key"]): json.loads(row["value_json"])
        for row in conn.execute(
            "SELECT field_key,value_json FROM character_profile_values WHERE entity_id=? ORDER BY field_key",
            (entity_id,),
        ).fetchall()
    }
    skills = [dict(row) for row in conn.execute(
        "SELECT skill_key,category,score,tier,experience FROM character_skills WHERE entity_id=? ORDER BY skill_key",
        (entity_id,),
    ).fetchall()]
    preferences = [dict(row) for row in conn.execute(
        "SELECT preference_type,subject,intensity FROM character_preferences WHERE entity_id=? ORDER BY preference_type,subject",
        (entity_id,),
    ).fetchall()]
    hobbies = [dict(row) for row in conn.execute(
        "SELECT name,proficiency,frequency,enjoyment FROM character_hobbies WHERE entity_id=? ORDER BY name",
        (entity_id,),
    ).fetchall()]
    habits = [dict(row) for row in conn.execute(
        "SELECT name,description,frequency,strength FROM character_habits WHERE entity_id=? ORDER BY name",
        (entity_id,),
    ).fetchall()]
    return {
        "entity_id": entity_id,
        "name": str(match["name"]),
        "values": values,
        "skills": skills,
        "preferences": preferences,
        "hobbies": hobbies,
        "habits": habits,
    }


def _validate_character_payload(conn: sqlite3.Connection, proposal: dict[str, Any]) -> None:
    profile = proposal.get("properties", {}).get("character_profile")
    if not isinstance(profile, dict):
        raise CreatorStudioError("Character AI draft requires structured character_profile")
    values = profile.get("values")
    if not isinstance(values, dict):
        raise CreatorStudioError("Character AI draft profile values must be an object")
    known = {str(row[0]) for row in conn.execute("SELECT field_key FROM profile_field_definitions")}
    unknown = sorted(set(values) - known)
    if unknown:
        raise CreatorStudioError(f"Character AI draft used unknown profile fields: {', '.join(unknown)}")
    if not str(values.get("identity.full_name") or "").strip():
        values["identity.full_name"] = str(proposal.get("identity", {}).get("name") or "").strip()


def _save_draft(
    conn: sqlite3.Connection,
    user_id: int,
    proposal: dict[str, Any],
    *,
    draft_mode: str,
    prompt_text: str | None,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    ensure_sandbox(conn, sandbox_id)
    normalized = validate_creation_proposal(proposal)
    if normalized["creation_type"] == "character" and draft_mode == "ai_generated":
        _validate_character_payload(conn, normalized)
    existing = conn.execute(
        "SELECT revision FROM creation_sandbox_drafts WHERE sandbox_id=? AND user_id=?",
        (sandbox_id, int(user_id)),
    ).fetchone()
    revision = int(existing["revision"]) + 1 if existing else 1
    conn.execute(
        """
        INSERT INTO creation_sandbox_drafts(
            sandbox_id,user_id,creation_type,draft_mode,prompt_text,proposal_json,revision
        ) VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(sandbox_id,user_id) DO UPDATE SET
            creation_type=excluded.creation_type,
            draft_mode=excluded.draft_mode,
            prompt_text=excluded.prompt_text,
            proposal_json=excluded.proposal_json,
            revision=excluded.revision,
            updated_at=CURRENT_TIMESTAMP
        """,
        (
            sandbox_id, int(user_id), normalized["creation_type"], draft_mode,
            prompt_text, _json(normalized), revision,
        ),
    )
    conn.commit()
    return active_draft(conn, user_id, sandbox_id=sandbox_id) or {}


def manual_draft(
    conn: sqlite3.Connection,
    user_id: int,
    creation_type: str,
    name: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    clean_name = str(name or "").strip()
    if not clean_name:
        raise CreatorStudioError("Creation name is required")
    proposal = build_creation_proposal(
        creation_type,
        identity={"name": clean_name},
        provenance_mode="manual",
        requested_by=f"telegram:{int(user_id)}",
    )
    return _save_draft(conn, user_id, proposal, draft_mode="manual", prompt_text=None, sandbox_id=sandbox_id)


def ai_draft(
    conn: sqlite3.Connection,
    user_id: int,
    creation_type: str,
    prompt_text: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    prompt_text = str(prompt_text or "").strip()
    if not prompt_text:
        raise CreatorStudioError("AI creation prompt is required")
    binding = creator_creation_binding(conn)
    if not binding:
        raise CreatorStudioError("Creator Creation AI is not configured")
    reference = _canonical_reference(conn, prompt_text) if creation_type == "character" else None
    reference_text = ""
    if reference:
        reference_text = (
            " A canonical Character with the same explicit name exists. Use this read-only reference to preserve identity, "
            "genetic/appearance continuity and established facts while following the Creator's requested developmental stage. "
            "Do not mechanically scale mutable adult values and do not mutate the reference. Reference JSON: " + _json(reference)
        )
    character_rules = ""
    if creation_type == "character":
        character_rules = (
            " For Character drafts, properties.character_profile is authoritative structured data. Populate relevant canonical "
            "profile field keys from the supplied schema, plus structured preferences, hobbies, habits and skills. Omit profile "
            "fields that cannot be inferred rather than inventing alternate prose keys. Do not put Age, Physical Description, "
            "Personality or measurements into arbitrary properties keys when a canonical profile field exists. The proposal may "
            "summarize behavior through canonical personality/background fields, but the structured profile is the source of truth."
        )
    prompt = (
        f"Draft one fictional {creation_type} for the isolated Observer Sandbox Creation Sandbox. "
        "Return only the required JSON schema. This is a proposal, not a real-world mutation. "
        "Never claim canonical existence or transmigration. Use proposal_version=1, schema_version=1, "
        "target_scope='sandbox', provenance.mode='ai_generated', and provenance.requested_by exactly "
        f"'telegram:{int(user_id)}'.{character_rules}{reference_text} Creator intent: {prompt_text}"
    )
    value = generate_structured(
        conn,
        provider_id=str(binding["provider_id"]),
        model_id=str(binding["model_id"]),
        prompt=prompt,
        schema=_schema(conn, creation_type),
        schema_name=f"observer_creator_studio_{creation_type}",
        parameters=dict(binding.get("parameters") or {}),
    )
    value.setdefault("provenance", {})["mode"] = "ai_generated"
    value["provenance"]["requested_by"] = f"telegram:{int(user_id)}"
    return _save_draft(conn, user_id, value, draft_mode="ai_generated", prompt_text=prompt_text, sandbox_id=sandbox_id)


def active_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT sandbox_id,user_id,creation_type,draft_mode,prompt_text,proposal_json,revision,created_at,updated_at
        FROM creation_sandbox_drafts WHERE sandbox_id=? AND user_id=?
        """,
        (sandbox_id, int(user_id)),
    ).fetchone()
    if row is None:
        return None
    result = dict(row)
    result["proposal"] = _loads(result.pop("proposal_json"))
    return result


def reroll_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    if not draft:
        raise CreatorStudioError("No Creator Studio draft to reroll")
    if draft["draft_mode"] != "ai_generated" or not draft.get("prompt_text"):
        raise CreatorStudioError("Only AI-generated drafts can be rerolled")
    return ai_draft(conn, user_id, str(draft["creation_type"]), str(draft["prompt_text"]), sandbox_id=sandbox_id)


def cancel_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> bool:
    cursor = conn.execute(
        "DELETE FROM creation_sandbox_drafts WHERE sandbox_id=? AND user_id=?",
        (sandbox_id, int(user_id)),
    )
    conn.commit()
    return cursor.rowcount > 0


def approve_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    if not draft:
        raise CreatorStudioError("No Creator Studio draft to approve")
    proposal = copy.deepcopy(draft["proposal"])
    character_profile = None
    if proposal["creation_type"] == "character":
        character_profile = proposal.get("properties", {}).pop("character_profile", None)
    obj = activate_creation_proposal(conn, proposal, sandbox_id=sandbox_id)
    if character_profile:
        values = dict(character_profile.get("values") or {})
        if values:
            set_sandbox_profile_values(conn, obj["object_id"], values, source="creator-studio-ai-profile")
        replace_sandbox_preferences(conn, obj["object_id"], character_profile.get("preferences") or [])
        replace_sandbox_hobbies(conn, obj["object_id"], character_profile.get("hobbies") or [])
        replace_sandbox_habits(conn, obj["object_id"], character_profile.get("habits") or [])
        replace_sandbox_skills(conn, obj["object_id"], character_profile.get("skills") or [])
    cancel_draft(conn, user_id, sandbox_id=sandbox_id)
    return obj


__all__ = [
    "CreatorStudioError", "active_draft", "ai_draft", "approve_draft", "cancel_draft",
    "manual_draft", "reroll_draft"
]

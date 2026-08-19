from __future__ import annotations

import copy
import json
import re
import sqlite3
from datetime import date, datetime
from typing import Any

from .character_creation_policy import creation_field_keys, creation_field_rows, sanitize_creation_profile_values
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
    rows = creation_field_rows(conn)
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
    allowed = creation_field_keys(conn)
    values = {
        str(row["field_key"]): json.loads(row["value_json"])
        for row in conn.execute(
            "SELECT field_key,value_json FROM character_profile_values WHERE entity_id=? ORDER BY field_key",
            (entity_id,),
        ).fetchall()
        if str(row["field_key"]) in allowed
    }
    skills = [dict(row) for row in conn.execute(
        "SELECT skill_key,category,score,tier,experience FROM character_skills WHERE entity_id=? ORDER BY skill_key",
        (entity_id,),
    ).fetchall()]
    return {
        "entity_id": entity_id,
        "name": str(match["name"]),
        "values": values,
        "skills": skills,
    }


def _dedupe_skills(skills: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    aliases = {"weapon_mastery": "weapons"}
    for raw in skills:
        key = str(raw.get("skill_key") or "").strip()
        canonical = aliases.get(key, key)
        if not canonical or canonical in seen:
            continue
        item = dict(raw)
        item["skill_key"] = canonical
        score = item.get("score")
        if score is not None and (isinstance(score, bool) or not isinstance(score, (int, float)) or not 0 <= float(score) <= 100):
            raise CreatorStudioError(f"Character skill score out of range: {canonical}")
        experience = item.get("experience")
        if experience is not None and (isinstance(experience, bool) or not isinstance(experience, (int, float)) or float(experience) < 0):
            raise CreatorStudioError(f"Character skill experience cannot be negative: {canonical}")
        seen.add(canonical)
        result.append(item)
    return result


def _sim_reference_date(conn: sqlite3.Connection) -> date | None:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key='sim_time'").fetchone()
    if row is None:
        return None
    try:
        raw = json.loads(row["value_json"])
        return datetime.fromisoformat(str(raw)).date()
    except (TypeError, ValueError, json.JSONDecodeError):
        return None


def _explicit_requested_age(prompt_text: str | None) -> int | None:
    text = str(prompt_text or "")
    patterns = (
        r"\bage(?:d)?\s*[:=]?\s*(\d{1,3})\b",
        r"\b(\d{1,3})\s*(?:years? old|year-old)\b",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = int(match.group(1))
            if 0 <= value <= 130:
                return value
    return None


def _age_on(dob: date, reference_date: date) -> int:
    before_birthday = (reference_date.month, reference_date.day) < (dob.month, dob.day)
    return reference_date.year - dob.year - int(before_birthday)


def _validate_requested_age(
    conn: sqlite3.Connection,
    prompt_text: str | None,
    values: dict[str, Any],
) -> None:
    requested_age = _explicit_requested_age(prompt_text)
    dob_raw = values.get("identity.date_of_birth")
    reference_date = _sim_reference_date(conn)
    if requested_age is None or not isinstance(dob_raw, str) or reference_date is None:
        return
    try:
        dob = date.fromisoformat(dob_raw)
    except ValueError:
        return
    actual_age = _age_on(dob, reference_date)
    if actual_age != requested_age:
        raise CreatorStudioError(
            "Character date_of_birth conflicts with Creator-requested age: "
            f"requested {requested_age}, DOB {dob_raw} gives age {actual_age} on Universe date {reference_date.isoformat()}"
        )


def _requires_structured_skills(values: dict[str, Any]) -> bool:
    training_age = values.get("training.training_age_years")
    if isinstance(training_age, (int, float)) and not isinstance(training_age, bool) and float(training_age) > 0:
        return True
    background = " ".join(
        str(values.get(key) or "")
        for key in ("background.origins", "background.story_elements")
    ).lower()
    cues = (
        "trained", "training", "professional", "search-and-rescue", "search and rescue",
        "combat", "boxing", "wrestling", "navigation", "first aid", "fieldcraft",
    )
    return any(cue in background for cue in cues)


def _validate_character_payload(
    conn: sqlite3.Connection,
    proposal: dict[str, Any],
    reference: dict[str, Any] | None = None,
    *,
    prompt_text: str | None = None,
) -> None:
    profile = proposal.get("properties", {}).get("character_profile")
    if not isinstance(profile, dict):
        raise CreatorStudioError("Character AI draft requires structured character_profile")
    values = profile.get("values")
    if not isinstance(values, dict):
        raise CreatorStudioError("Character AI draft profile values must be an object")
    profile["values"] = sanitize_creation_profile_values(conn, values)
    if not str(profile["values"].get("identity.full_name") or "").strip():
        profile["values"]["identity.full_name"] = str(proposal.get("identity", {}).get("name") or "").strip()

    # A new independent Character must make an explicit age consistent with DOB on
    # the current Universe date. An exact-name canonical reference is different:
    # requested age is a developmental snapshot, and canonical DOB must be preserved.
    if reference is None:
        _validate_requested_age(conn, prompt_text, profile["values"])

    skills = _dedupe_skills([dict(item) for item in profile.get("skills") or [] if isinstance(item, dict)])
    if reference and reference.get("skills"):
        reference_keys = {str(item.get("skill_key") or "") for item in reference["skills"]}
        skills = [item for item in skills if str(item.get("skill_key") or "") in reference_keys]
    if not skills and _requires_structured_skills(profile["values"]):
        raise CreatorStudioError(
            "Character background establishes trained competencies but structured skills are empty"
        )
    profile["skills"] = skills


def _save_draft(
    conn: sqlite3.Connection,
    user_id: int,
    proposal: dict[str, Any],
    *,
    draft_mode: str,
    prompt_text: str | None,
    reference: dict[str, Any] | None = None,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    ensure_sandbox(conn, sandbox_id)
    normalized = validate_creation_proposal(proposal)
    if normalized["creation_type"] == "character" and draft_mode == "ai_generated":
        _validate_character_payload(conn, normalized, reference=reference, prompt_text=prompt_text)
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
            " A canonical Character with the same explicit name exists. Use this read-only reference only for stable identity, "
            "genetic/appearance continuity, established background and existing skill vocabulary while following the Creator's "
            "requested developmental stage. Preserve the canonical date_of_birth exactly; an explicit requested age describes a "
            "developmental snapshot and must not rewrite DOB to match the current Universe date. Do not mechanically scale mutable "
            "adult values and do not mutate the reference. Do not import live preferences, object associations, runtime state or "
            "current goals. Reference JSON: " + _json(reference)
        )
    character_rules = ""
    if creation_type == "character":
        reference_date = _sim_reference_date(conn)
        age_rule = ""
        if reference is None and reference_date is not None:
            age_rule = (
                f" The current Universe reference date is {reference_date.isoformat()}. If the Creator specifies an explicit age, "
                "identity.date_of_birth must make the new Character exactly that age on this reference date."
            )
        character_rules = (
            " For Character drafts, properties.character_profile is authoritative creation-owned structured data. The supplied "
            "schema intentionally excludes runtime-owned and derived fields. Populate only fields that are stable at creation or "
            "believable baseline/developmental traits. Never invent current emotion, needs, nutrition, physiology, sleep, current "
            "sexual state, current goals, narrative state, weekly counters, BMI, lean/fat mass or age-derived values. Preferences, "
            "hobbies and habits must be intrinsic personal tendencies only: never copy named furniture, inventory objects, locations, "
            "simulators, action-source labels or UI strings. Skills must use a clean non-duplicated taxonomy. Material trained "
            "competencies established by background history must be represented as structured skills rather than existing only as "
            "free-form capabilities. Keep current body measurements at or below their matching genetic ceilings, keep fixed anatomy "
            "consistent with fixed genetic values, and keep 0-100 attributes inside their legal range. Use the canonical field "
            "raps_pa.practical_skills; do not also emit the compatibility alias raps_pa.practical_skill. Omit uncertain optional "
            "details rather than filling every available field."
            + age_rule
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
    if creation_type == "character":
        _validate_character_payload(conn, value, reference=reference, prompt_text=prompt_text)
    return _save_draft(
        conn,
        user_id,
        value,
        draft_mode="ai_generated",
        prompt_text=prompt_text,
        reference=reference,
        sandbox_id=sandbox_id,
    )


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
        values = sanitize_creation_profile_values(conn, dict(character_profile.get("values") or {}))
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

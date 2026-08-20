from __future__ import annotations

import copy
import json
import sqlite3
from datetime import date, datetime
from typing import Any

from .character_creation_policy import creation_field_keys, sanitize_creation_profile_values
from .creation_sandbox import DEFAULT_SANDBOX_ID


class ManualCharacterCreationError(ValueError):
    pass


# These are the minimum stable facts required before a manually authored
# Character may leave draft state. Everything else remains available through
# the same creation-owned field registry and can be added when known.
MANUAL_CHARACTER_REQUIRED_FIELDS = (
    "identity.full_name",
    "identity.date_of_birth",
    "identity.sex",
    "identity.gender",
    "body.height_in",
    "body.weight_lb",
    "body.body_fat_pct",
    "personality.primary_motivation",
    "personality.primary_traits",
    "background.origins",
)

MANUAL_CHARACTER_COLLECTIONS = frozenset(
    {"skills", "preferences", "hobbies", "habits", "compatibility_tags"}
)


def empty_manual_character_profile(name: str) -> dict[str, Any]:
    return {
        "values": {"identity.full_name": str(name).strip()},
        "preferences": [],
        "hobbies": [],
        "habits": [],
        "skills": [],
    }


def _loads(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ManualCharacterCreationError("Stored manual Character draft is invalid") from exc
    if not isinstance(value, dict):
        raise ManualCharacterCreationError("Stored manual Character draft is invalid")
    return value


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _draft_row(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> sqlite3.Row:
    row = conn.execute(
        """
        SELECT sandbox_id,user_id,creation_type,draft_mode,prompt_text,proposal_json,revision
        FROM creation_sandbox_drafts
        WHERE sandbox_id=? AND user_id=?
        """,
        (sandbox_id, int(user_id)),
    ).fetchone()
    if row is None or str(row["creation_type"]) != "character" or str(row["draft_mode"]) != "manual":
        raise ManualCharacterCreationError("No manual Character draft is active")
    return row


def manual_character_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    row = _draft_row(conn, user_id, sandbox_id=sandbox_id)
    return {
        "sandbox_id": str(row["sandbox_id"]),
        "user_id": int(row["user_id"]),
        "creation_type": str(row["creation_type"]),
        "draft_mode": str(row["draft_mode"]),
        "prompt_text": row["prompt_text"],
        "revision": int(row["revision"]),
        "proposal": _loads(str(row["proposal_json"])),
    }


def _profile(proposal: dict[str, Any]) -> dict[str, Any]:
    profile = proposal.get("properties", {}).get("character_profile")
    if not isinstance(profile, dict):
        raise ManualCharacterCreationError("Manual Character draft requires structured character_profile")
    for collection in ("preferences", "hobbies", "habits", "skills"):
        if not isinstance(profile.get(collection), list):
            raise ManualCharacterCreationError(f"Manual Character draft {collection} must be an array")
    if not isinstance(profile.get("values"), dict):
        raise ManualCharacterCreationError("Manual Character draft values must be an object")
    return profile


def _save(
    conn: sqlite3.Connection,
    row: sqlite3.Row,
    proposal: dict[str, Any],
) -> dict[str, Any]:
    revision = int(row["revision"]) + 1
    conn.execute(
        """
        UPDATE creation_sandbox_drafts
        SET proposal_json=?,revision=?,updated_at=CURRENT_TIMESTAMP
        WHERE sandbox_id=? AND user_id=? AND revision=?
        """,
        (
            _json(proposal),
            revision,
            str(row["sandbox_id"]),
            int(row["user_id"]),
            int(row["revision"]),
        ),
    )
    if conn.execute("SELECT changes()").fetchone()[0] != 1:
        conn.rollback()
        raise ManualCharacterCreationError("Manual Character draft changed; reopen the current draft")
    conn.commit()
    return manual_character_draft(conn, int(row["user_id"]), sandbox_id=str(row["sandbox_id"]))


def _missing(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, dict)):
        return not value
    return False


def manual_character_missing_fields(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> list[str]:
    draft = manual_character_draft(conn, user_id, sandbox_id=sandbox_id)
    values = dict(_profile(draft["proposal"]).get("values") or {})
    return [key for key in MANUAL_CHARACTER_REQUIRED_FIELDS if _missing(values.get(key))]


def manual_character_baseline_status(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    missing = manual_character_missing_fields(conn, user_id, sandbox_id=sandbox_id)
    total = len(MANUAL_CHARACTER_REQUIRED_FIELDS)
    return {
        "ready": not missing,
        "complete": total - len(missing),
        "total": total,
        "missing": missing,
    }


def _coerce(data_type: str, raw: str) -> Any:
    value = str(raw or "").strip()
    if data_type == "text":
        if not value:
            raise ManualCharacterCreationError("Text value cannot be empty")
        return value
    if data_type == "date":
        if not value:
            raise ManualCharacterCreationError("Date value cannot be empty")
        try:
            date.fromisoformat(value)
        except ValueError as exc:
            raise ManualCharacterCreationError("Date must use YYYY-MM-DD") from exc
        return value
    if data_type == "datetime":
        if not value:
            raise ManualCharacterCreationError("Datetime value cannot be empty")
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ManualCharacterCreationError("Datetime must be ISO-8601") from exc
        return value
    if data_type == "number":
        try:
            return float(value)
        except ValueError as exc:
            raise ManualCharacterCreationError("Value must be numeric") from exc
    if data_type == "integer":
        try:
            return int(value)
        except ValueError as exc:
            raise ManualCharacterCreationError("Value must be an integer") from exc
    if data_type == "boolean":
        lowered = value.lower()
        if lowered in {"true", "yes", "1", "on"}:
            return True
        if lowered in {"false", "no", "0", "off"}:
            return False
        raise ManualCharacterCreationError("Boolean value must be true/false")
    if data_type == "json":
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ManualCharacterCreationError("Value must be valid JSON") from exc
    raise ManualCharacterCreationError(f"Unsupported manual field type: {data_type}")


def update_manual_character_field(
    conn: sqlite3.Connection,
    user_id: int,
    field_key: str,
    raw_value: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    row = _draft_row(conn, user_id, sandbox_id=sandbox_id)
    proposal = _loads(str(row["proposal_json"]))
    field_key = str(field_key or "").strip()
    if field_key not in creation_field_keys(conn):
        raise ManualCharacterCreationError(f"Field is not creation-owned or writable: {field_key}")
    definition = conn.execute(
        "SELECT data_type FROM profile_field_definitions WHERE field_key=?",
        (field_key,),
    ).fetchone()
    if definition is None:
        raise ManualCharacterCreationError(f"Unknown profile field: {field_key}")
    value = _coerce(str(definition["data_type"]), raw_value)
    profile = _profile(proposal)
    values = dict(profile.get("values") or {})
    values[field_key] = value
    try:
        profile["values"] = sanitize_creation_profile_values(conn, values)
    except ValueError as exc:
        raise ManualCharacterCreationError(str(exc)) from exc
    if field_key == "identity.full_name":
        proposal["identity"]["name"] = str(profile["values"][field_key]).strip()
    return _save(conn, row, proposal)


def _optional_number(item: dict[str, Any], key: str, collection: str) -> None:
    value = item.get(key)
    if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float))):
        raise ManualCharacterCreationError(f"{collection}.{key} must be numeric or null")


def _object_array(value: Any, collection: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ManualCharacterCreationError(f"{collection} must be a JSON array of objects")
    return [dict(item) for item in value]


def _validate_collection(collection: str, value: Any) -> Any:
    if collection == "compatibility_tags":
        if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
            raise ManualCharacterCreationError("compatibility_tags must be a JSON array of non-empty strings")
        return [str(item).strip() for item in value]

    items = _object_array(value, collection)
    if collection == "skills":
        seen: set[str] = set()
        normalized: list[dict[str, Any]] = []
        for item in items:
            key = str(item.get("skill_key") or "").strip()
            if not key:
                raise ManualCharacterCreationError("Each skill requires skill_key")
            key = "weapons" if key == "weapon_mastery" else key
            if key in seen:
                raise ManualCharacterCreationError(f"Duplicate skill: {key}")
            item["skill_key"] = key
            _optional_number(item, "score", collection)
            _optional_number(item, "experience", collection)
            score = item.get("score")
            if score is not None and not 0 <= float(score) <= 100:
                raise ManualCharacterCreationError(f"Character skill score out of range: {key}")
            experience = item.get("experience")
            if experience is not None and float(experience) < 0:
                raise ManualCharacterCreationError(f"Character skill experience cannot be negative: {key}")
            for text_key in ("category", "tier"):
                if item.get(text_key) is not None and not isinstance(item.get(text_key), str):
                    raise ManualCharacterCreationError(f"skills.{text_key} must be text or null")
            seen.add(key)
            normalized.append(item)
        return normalized

    if collection == "preferences":
        for item in items:
            if item.get("preference_type") not in {"like", "dislike", "interest", "aversion"}:
                raise ManualCharacterCreationError("Preference type must be like/dislike/interest/aversion")
            if not str(item.get("subject") or "").strip():
                raise ManualCharacterCreationError("Each preference requires subject")
            _optional_number(item, "intensity", collection)
        return items

    if collection == "hobbies":
        for item in items:
            if not str(item.get("name") or "").strip():
                raise ManualCharacterCreationError("Each hobby requires name")
            _optional_number(item, "proficiency", collection)
            _optional_number(item, "enjoyment", collection)
            if item.get("frequency") is not None and not isinstance(item.get("frequency"), str):
                raise ManualCharacterCreationError("hobbies.frequency must be text or null")
        return items

    if collection == "habits":
        for item in items:
            if not str(item.get("name") or "").strip():
                raise ManualCharacterCreationError("Each habit requires name")
            _optional_number(item, "strength", collection)
            for key in ("description", "frequency"):
                if item.get(key) is not None and not isinstance(item.get(key), str):
                    raise ManualCharacterCreationError(f"habits.{key} must be text or null")
        return items

    raise ManualCharacterCreationError(f"Unsupported manual Character collection: {collection}")


def update_manual_character_collection(
    conn: sqlite3.Connection,
    user_id: int,
    collection: str,
    raw_json: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    collection = str(collection or "").strip()
    if collection not in MANUAL_CHARACTER_COLLECTIONS:
        raise ManualCharacterCreationError(f"Unsupported manual Character collection: {collection}")
    try:
        decoded = json.loads(str(raw_json or "").strip())
    except json.JSONDecodeError as exc:
        raise ManualCharacterCreationError("Collection input must be valid JSON") from exc
    normalized = _validate_collection(collection, decoded)
    row = _draft_row(conn, user_id, sandbox_id=sandbox_id)
    proposal = copy.deepcopy(_loads(str(row["proposal_json"])))
    if collection == "compatibility_tags":
        proposal.setdefault("properties", {})["compatibility_tags"] = normalized
    else:
        _profile(proposal)[collection] = normalized
    return _save(conn, row, proposal)


__all__ = [
    "MANUAL_CHARACTER_COLLECTIONS",
    "MANUAL_CHARACTER_REQUIRED_FIELDS",
    "ManualCharacterCreationError",
    "empty_manual_character_profile",
    "manual_character_baseline_status",
    "manual_character_draft",
    "manual_character_missing_fields",
    "update_manual_character_collection",
    "update_manual_character_field",
]

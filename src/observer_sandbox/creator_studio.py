from __future__ import annotations

import json
import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID, activate_creation_proposal, ensure_sandbox
from .creation_socket import build_creation_proposal, validate_creation_proposal
from .creator_creation_ai import creator_creation_binding
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


def _schema(creation_type: str) -> dict[str, Any]:
    if creation_type not in {"character", "location"}:
        raise CreatorStudioError("Creator Studio currently supports Character and Location")
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
            "properties": {"type": "object", "additionalProperties": True},
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
    return _save_draft(
        conn, user_id, proposal, draft_mode="manual", prompt_text=None, sandbox_id=sandbox_id
    )


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
    prompt = (
        f"Draft one fictional {creation_type} for the isolated Observer Sandbox Creation Sandbox. "
        "Return only the required JSON schema. This is a proposal, not a real-world mutation. "
        "Never claim canonical existence or transmigration. Use proposal_version=1, schema_version=1, "
        "target_scope='sandbox', provenance.mode='ai_generated', and provenance.requested_by exactly "
        f"'telegram:{int(user_id)}'. Creator intent: {prompt_text}"
    )
    value = generate_structured(
        conn,
        provider_id=str(binding["provider_id"]),
        model_id=str(binding["model_id"]),
        prompt=prompt,
        schema=_schema(creation_type),
        schema_name=f"observer_creator_studio_{creation_type}",
        parameters=dict(binding.get("parameters") or {}),
    )
    value.setdefault("provenance", {})["mode"] = "ai_generated"
    value["provenance"]["requested_by"] = f"telegram:{int(user_id)}"
    return _save_draft(
        conn, user_id, value, draft_mode="ai_generated", prompt_text=prompt_text, sandbox_id=sandbox_id
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
    return ai_draft(
        conn, user_id, str(draft["creation_type"]), str(draft["prompt_text"]), sandbox_id=sandbox_id
    )


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
    obj = activate_creation_proposal(conn, draft["proposal"], sandbox_id=sandbox_id)
    cancel_draft(conn, user_id, sandbox_id=sandbox_id)
    return obj


__all__ = [
    "CreatorStudioError", "active_draft", "ai_draft", "approve_draft", "cancel_draft",
    "manual_draft", "reroll_draft"
]

from __future__ import annotations

import copy
import json
import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID
from .creation_socket import build_creation_proposal
from .creator_creation_ai import creator_creation_binding
from .creator_studio import CreatorStudioError, _save_draft, active_draft, cancel_draft
from .item_ai_contract import canonicalize_ai_item_batch_fill, item_batch_ai_fill_schema
from .sandbox_item_creation import create_sandbox_item_batch, preview_sandbox_item_batch
from .structured_ai import generate_structured


def _copy_entries(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return copy.deepcopy(entries)


def _validate_entries(conn: sqlite3.Connection, entries: Any, *, sandbox_id: str) -> list[dict[str, Any]]:
    if not isinstance(entries, list) or not entries:
        raise CreatorStudioError("Item batch must contain at least one entry")
    if not all(isinstance(entry, dict) for entry in entries):
        raise CreatorStudioError("Every Item batch entry must be an object")
    try:
        preview_sandbox_item_batch(conn, entries, sandbox_id=sandbox_id)
    except (ValueError, TypeError, KeyError) as exc:
        raise CreatorStudioError(f"Item batch contract rejected the draft: {exc}") from exc
    return _copy_entries(entries)


def _wrap_batch_proposal(entries: list[dict[str, Any]], *, mode: str, user_id: int) -> dict[str, Any]:
    return build_creation_proposal(
        "item",
        identity={"name": f"Item Batch ({len(entries)})"},
        properties={"item_batch": {"items": _copy_entries(entries)}},
        capabilities=[],
        provenance_mode=mode,
        requested_by=f"telegram:{int(user_id)}",
    )


def manual_item_batch_draft(
    conn: sqlite3.Connection,
    user_id: int,
    raw_json: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    try:
        candidate = json.loads(str(raw_json or ""))
    except json.JSONDecodeError as exc:
        raise CreatorStudioError(f"Item batch JSON is invalid: {exc.msg}") from exc
    if not isinstance(candidate, dict) or set(candidate) != {"items"}:
        raise CreatorStudioError("Item batch JSON must be one object with exactly an 'items' array")
    entries = _validate_entries(conn, candidate["items"], sandbox_id=sandbox_id)
    return _save_draft(
        conn,
        user_id,
        _wrap_batch_proposal(entries, mode="manual", user_id=user_id),
        draft_mode="manual",
        prompt_text=None,
        sandbox_id=sandbox_id,
    )


def ai_item_batch_draft(
    conn: sqlite3.Connection,
    user_id: int,
    prompt_text: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    intent = str(prompt_text or "").strip()
    if not intent:
        raise CreatorStudioError("AI Item batch creation prompt is required")
    binding = creator_creation_binding(conn)
    if not binding:
        raise CreatorStudioError("Creator Creation AI is not configured")
    prompt = (
        "Fill the supplied complete Item Batch schema for the isolated Creation Sandbox. "
        "Create one batch entry per distinct requested Item type. Use stable unique lowercase refs. "
        "For every Item payload, fill the full item-v1 form: use [] for unused arrays, null for unknown/unused nullable fields, and null for unused module slots. "
        "Do not omit, rename or invent schema fields. Preserve requested stack quantities. "
        "STACK INVARIANT: ordinary single objects are definition.stackable=false, instance.mode='unique', instance.quantity=null, instance.unit=null, and modules.stack=null. "
        "Only fungible/countable grouped goods are stackable: definition.stackable=true, instance.mode='stack', modules.stack must be non-null, and instance quantity/unit must agree with modules.stack.initial_quantity/canonical_unit. "
        "Never populate modules.stack for a non-stackable Item. "
        "For requested batch-local storage, use stored_in='$ref' and make the target a real container Item. "
        "Do not author derived grades. If monetary facts are not explicitly grounded, use economically_immaterial/excluded with null monetary values. "
        "This is proposal-only and does not create canonical state. "
        f"Creator intent: {intent}"
    )
    candidate = generate_structured(
        conn,
        provider_id=str(binding["provider_id"]),
        model_id=str(binding["model_id"]),
        prompt=prompt,
        schema=item_batch_ai_fill_schema(),
        schema_name="observer_creator_studio_item_batch_v1",
        parameters=dict(binding.get("parameters") or {}),
    )
    if not isinstance(candidate, dict) or set(candidate) != {"items"}:
        raise CreatorStudioError("Creation AI returned an invalid Item batch envelope")
    candidate = canonicalize_ai_item_batch_fill(candidate)
    entries = _validate_entries(conn, candidate["items"], sandbox_id=sandbox_id)
    return _save_draft(
        conn,
        user_id,
        _wrap_batch_proposal(entries, mode="ai_generated", user_id=user_id),
        draft_mode="ai_generated",
        prompt_text=intent,
        sandbox_id=sandbox_id,
    )


def reroll_item_batch_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    properties = draft.get("proposal", {}).get("properties", {}) if draft else {}
    if not draft or draft.get("creation_type") != "item" or not isinstance(properties.get("item_batch"), dict):
        raise CreatorStudioError("No Item batch draft to reroll")
    if draft.get("draft_mode") != "ai_generated" or not draft.get("prompt_text"):
        raise CreatorStudioError("Only AI-generated Item batch drafts can be rerolled")
    return ai_item_batch_draft(conn, user_id, str(draft["prompt_text"]), sandbox_id=sandbox_id)


def approve_item_batch_draft(
    conn: sqlite3.Connection,
    user_id: int,
    expected_revision: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> list[dict[str, Any]]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    if not draft or draft.get("creation_type") != "item":
        raise CreatorStudioError("No Item batch draft to approve")
    if int(draft["revision"]) != int(expected_revision):
        raise CreatorStudioError("Draft changed after confirmation. Review the current revision again.")
    batch = draft.get("proposal", {}).get("properties", {}).get("item_batch")
    if not isinstance(batch, dict) or not isinstance(batch.get("items"), list):
        raise CreatorStudioError("Stored Item batch draft payload is missing")
    entries = _validate_entries(conn, batch["items"], sandbox_id=sandbox_id)
    try:
        created = create_sandbox_item_batch(
            conn,
            entries,
            sandbox_id=sandbox_id,
            provenance_mode=str(draft.get("draft_mode") or "manual"),
            requested_by=f"telegram:{int(user_id)}",
        )
    except (ValueError, TypeError, KeyError) as exc:
        raise CreatorStudioError(f"Item batch approval failed: {exc}") from exc
    cancel_draft(conn, user_id, sandbox_id=sandbox_id)
    return created


__all__ = [
    "ai_item_batch_draft",
    "approve_item_batch_draft",
    "manual_item_batch_draft",
    "reroll_item_batch_draft",
]

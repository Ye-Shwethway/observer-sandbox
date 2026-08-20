from __future__ import annotations

import copy
import json
import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID
from .creation_socket import build_creation_proposal
from .creator_creation_ai import creator_creation_binding
from .creator_studio import CreatorStudioError, _save_draft, active_draft, cancel_draft
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
        "Draft a heterogeneous Item batch for the isolated Observer Sandbox Creation Sandbox. Return JSON only with exactly one top-level key: items. "
        "items is a non-empty array; every member has exactly {'ref': token, 'payload': item-v1-object}. Refs are unique lowercase stable tokens. "
        "Every payload has exactly schema_version,definition,instance,economic_policy,requirements,relationships and schema_version='item-v1'. "
        "definition has exactly key,name,kind,description,stackable,mobility,capabilities,tags,modules. "
        "Allowed kinds: object,fixture,equipment,consumable,container. Mobility: movable or fixed; fixtures are fixed. "
        "Allowed capabilities: inspect,eat,store,train,use,equip,wear. Allowed modules only: physical,stack,nutrition,container,resistance_training. "
        "Module exact shapes: physical={mass,length,width,height}, each known value is {'value':number,'unit':unit} and unknown entries are null; "
        "stack={'canonical_unit':token,'initial_quantity':positive-number}; "
        "nutrition={'basis_quantity':positive-number,'unit':token,'energy_kcal':number,'protein_g':number,'carbohydrate_g':number,'fat_g':number}; "
        "container={'capacity_volume':{'value':positive-number,'unit':volume-unit}}; "
        "resistance_training={'resistance_load':{'value':positive-number,'unit':mass-unit}}. "
        "Use only needed modules. For a requested storage target such as a backpack, make that Item a real container with a conservative plausible capacity if none was stated. "
        "For stackable Items, include stack module and instance={'mode':'stack','quantity':number,'unit':same-token}; otherwise instance={'mode':'unique'}. "
        "If nutrition is represented, its unit must match the stack canonical_unit. Do not author grades or unknown fields. "
        "economic_policy has exactly classification,currency_code,market_value_minor,replacement_value_minor,unit_value_minor,unit_quantity,unit_label,net_worth_treatment,included_in_parent_ref,valuation_method. "
        "Unless the Creator explicitly supplied grounded monetary facts, use classification='economically_immaterial', currency_code=null, all monetary/unit value fields=null, "
        "net_worth_treatment='excluded', included_in_parent_ref=null, valuation_method='creator_explicit'. "
        "requirements is exactly {'use':null} unless a typed requirement was explicitly requested. "
        "relationships has exactly located_at,stored_in,owned_by,carried_by,equipped_by. Leave them null except requested batch-local storage. "
        "For batch-local storage use stored_in='$ref' targeting a batch Item with the container module; never create self-links or cycles. "
        "Preserve requested quantities. This is proposal-only; never claim canonical existence. "
        f"Creator intent: {intent}"
    )
    candidate = generate_structured(
        conn,
        provider_id=str(binding["provider_id"]),
        model_id=str(binding["model_id"]),
        prompt=prompt,
        schema={
            "type": "object",
            "required": ["items"],
            "additionalProperties": False,
            "properties": {
                "items": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["ref", "payload"],
                        "additionalProperties": False,
                        "properties": {
                            "ref": {"type": "string"},
                            "payload": {"type": "object"},
                        },
                    },
                }
            },
        },
        schema_name="observer_creator_studio_item_batch_v1",
        parameters=dict(binding.get("parameters") or {}),
    )
    if not isinstance(candidate, dict) or set(candidate) != {"items"}:
        raise CreatorStudioError("Creation AI returned an invalid Item batch envelope")
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

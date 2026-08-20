from __future__ import annotations

import copy
import json
import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID
from .creation_socket import build_creation_proposal
from .creator_creation_ai import creator_creation_binding
from .creator_studio import CreatorStudioError, _save_draft, active_draft, cancel_draft
from .item_ai_contract import canonicalize_ai_item_fill, item_ai_fill_schema
from .item_creation_schema import validate_item_payload
from .sandbox_item_creation import create_sandbox_item
from .structured_ai import generate_structured


def _source_payload(value: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(value)
    payload.pop("derived", None)
    return payload


def _wrap_item_proposal(payload: dict[str, Any], *, mode: str, user_id: int) -> dict[str, Any]:
    definition = payload["definition"]
    return build_creation_proposal(
        "item",
        identity={"name": definition["name"]},
        properties={"item_payload": _source_payload(payload)},
        capabilities=list(definition.get("capabilities") or []),
        provenance_mode=mode,
        requested_by=f"telegram:{int(user_id)}",
    )


def manual_item_template() -> dict[str, Any]:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "steel_water_bottle",
            "name": "Steel Water Bottle",
            "kind": "object",
            "description": "Reusable steel water bottle.",
            "stackable": False,
            "mobility": "movable",
            "capabilities": ["inspect", "use"],
            "tags": ["bottle"],
            "modules": {
                "physical": {
                    "mass": {"value": 0.7, "unit": "lb"},
                    "length": None,
                    "width": None,
                    "height": {"value": 10, "unit": "in"},
                }
            },
        },
        "instance": {"mode": "unique"},
        "economic_policy": {
            "classification": "economically_immaterial",
            "currency_code": None,
            "market_value_minor": None,
            "replacement_value_minor": None,
            "unit_value_minor": None,
            "unit_quantity": None,
            "unit_label": None,
            "net_worth_treatment": "excluded",
            "included_in_parent_ref": None,
            "valuation_method": "creator_explicit",
        },
        "requirements": {"use": None},
        "relationships": {
            "located_at": None,
            "stored_in": None,
            "owned_by": None,
            "carried_by": None,
            "equipped_by": None,
        },
    }


def manual_item_draft(
    conn: sqlite3.Connection,
    user_id: int,
    raw_json: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    try:
        candidate = json.loads(str(raw_json or ""))
    except json.JSONDecodeError as exc:
        raise CreatorStudioError(f"Item JSON is invalid: {exc.msg}") from exc
    if not isinstance(candidate, dict):
        raise CreatorStudioError("Item draft must be one JSON object")
    try:
        validate_item_payload(candidate)
    except (ValueError, TypeError, KeyError) as exc:
        raise CreatorStudioError(f"Item contract rejected the draft: {exc}") from exc
    proposal = _wrap_item_proposal(candidate, mode="manual", user_id=user_id)
    return _save_draft(
        conn,
        user_id,
        proposal,
        draft_mode="manual",
        prompt_text=None,
        sandbox_id=sandbox_id,
    )


def ai_item_draft(
    conn: sqlite3.Connection,
    user_id: int,
    prompt_text: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    intent = str(prompt_text or "").strip()
    if not intent:
        raise CreatorStudioError("AI Item creation prompt is required")
    binding = creator_creation_binding(conn)
    if not binding:
        raise CreatorStudioError("Creator Creation AI is not configured")
    prompt = (
        "Fill the supplied complete item-v1 schema for exactly one Item in the isolated Creation Sandbox. "
        "Use [] for unused arrays, null for unknown/unused nullable fields, and null for unused module slots. "
        "Do not omit, rename or invent schema fields. Populate only facts supported by the Creator intent or conservative ordinary inference. "
        "Do not author derived grades. If monetary facts are not explicitly grounded, use economically_immaterial/excluded with null monetary values. "
        "This is proposal-only and does not create canonical state. "
        f"Creator intent: {intent}"
    )
    candidate = generate_structured(
        conn,
        provider_id=str(binding["provider_id"]),
        model_id=str(binding["model_id"]),
        prompt=prompt,
        schema=item_ai_fill_schema(),
        schema_name="observer_creator_studio_item_v1",
        parameters=dict(binding.get("parameters") or {}),
    )
    if not isinstance(candidate, dict):
        raise CreatorStudioError("Creation AI returned an invalid Item object")
    candidate = canonicalize_ai_item_fill(candidate)
    try:
        validate_item_payload(candidate)
    except (ValueError, TypeError, KeyError) as exc:
        raise CreatorStudioError(f"Creation AI Item failed exact validation: {exc}") from exc
    proposal = _wrap_item_proposal(candidate, mode="ai_generated", user_id=user_id)
    return _save_draft(
        conn,
        user_id,
        proposal,
        draft_mode="ai_generated",
        prompt_text=intent,
        sandbox_id=sandbox_id,
    )


def reroll_item_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    if not draft or draft.get("creation_type") != "item":
        raise CreatorStudioError("No Item draft to reroll")
    if draft.get("draft_mode") != "ai_generated" or not draft.get("prompt_text"):
        raise CreatorStudioError("Only AI-generated Item drafts can be rerolled")
    return ai_item_draft(conn, user_id, str(draft["prompt_text"]), sandbox_id=sandbox_id)


def approve_item_draft(
    conn: sqlite3.Connection,
    user_id: int,
    expected_revision: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    if not draft or draft.get("creation_type") != "item":
        raise CreatorStudioError("No Item draft to approve")
    if int(draft["revision"]) != int(expected_revision):
        raise CreatorStudioError("Draft changed after confirmation. Review the current revision again.")
    stored = draft["proposal"].get("properties", {}).get("item_payload")
    if not isinstance(stored, dict):
        raise CreatorStudioError("Stored Item draft payload is missing")
    try:
        validate_item_payload(stored)
    except (ValueError, TypeError, KeyError) as exc:
        raise CreatorStudioError(f"Item approval failed exact validation: {exc}") from exc
    obj = create_sandbox_item(
        conn,
        copy.deepcopy(stored),
        sandbox_id=sandbox_id,
        provenance_mode=str(draft.get("draft_mode") or "manual"),
        requested_by=f"telegram:{int(user_id)}",
    )
    cancel_draft(conn, user_id, sandbox_id=sandbox_id)
    return obj


__all__ = [
    "ai_item_draft",
    "approve_item_draft",
    "manual_item_draft",
    "manual_item_template",
    "reroll_item_draft",
]

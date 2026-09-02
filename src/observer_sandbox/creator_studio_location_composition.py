from __future__ import annotations

import copy
import json
import sqlite3
from typing import Any, Mapping

from .creation_sandbox import DEFAULT_SANDBOX_ID
from .creation_socket import build_creation_proposal
from .creator_studio import CreatorStudioError, _save_draft, active_draft, cancel_draft
from .creator_studio_item import manual_item_template
from .creator_studio_location import manual_location_template
from .sandbox_location_composition import (
    COMPOSITION_SCHEMA_VERSION,
    SandboxLocationCompositionError,
    materialize_location_composition,
    preview_location_composition,
)


def location_composition_template() -> dict[str, Any]:
    """Return the smallest useful exact Location composition starter."""
    property_payload = manual_location_template()
    property_payload["identity"].update(
        {
            "key": "place.creator.composition_test_property",
            "name": "Composition Test Property",
            "kind": "property",
            "description": "A Creator Studio property used as a nested composition root.",
        }
    )
    property_payload["structure"].update({"parent_ref": None, "exposure": "mixed"})

    room_payload = manual_location_template()
    room_payload["identity"].update(
        {
            "key": "place.creator.composition_test_property.room",
            "name": "Composition Test Room",
            "kind": "room",
            "description": "A child room represented inside the composition test property.",
        }
    )
    room_payload["structure"].update({"parent_ref": "$property", "exposure": "indoor"})

    item_payload = manual_item_template()
    item_payload["definition"].update(
        {
            "key": "item.creator.composition_test_bottle",
            "name": "Composition Test Bottle",
            "description": "A movable bottle placed in the child room for composition validation.",
        }
    )
    item_payload["relationships"]["located_at"] = "$room"

    return {
        "schema_version": COMPOSITION_SCHEMA_VERSION,
        "locations": [
            {"ref": "property", "payload": property_payload},
            {"ref": "room", "payload": room_payload},
        ],
        "items": [{"ref": "bottle", "payload": item_payload}],
    }


def _composition_name(envelope: Mapping[str, Any]) -> str:
    locations = envelope.get("locations")
    if isinstance(locations, list) and locations:
        first = locations[0]
        if isinstance(first, Mapping):
            payload = first.get("payload")
            if isinstance(payload, Mapping):
                identity = payload.get("identity")
                if isinstance(identity, Mapping):
                    name = str(identity.get("name") or "").strip()
                    if name:
                        return f"{name} Composition"
    return "Location Composition"


def _wrap_composition_proposal(
    envelope: Mapping[str, Any],
    *,
    mode: str,
    user_id: int,
) -> dict[str, Any]:
    return build_creation_proposal(
        "location",
        identity={"name": _composition_name(envelope)},
        properties={"location_composition": copy.deepcopy(dict(envelope))},
        capabilities=[],
        provenance_mode=mode,
        requested_by=f"telegram:{int(user_id)}",
    )


def _validate_composition(
    conn: sqlite3.Connection,
    envelope: Mapping[str, Any],
    *,
    sandbox_id: str,
    user_id: int,
) -> dict[str, Any]:
    try:
        return preview_location_composition(
            conn,
            envelope,
            sandbox_id=sandbox_id,
            provenance_mode="manual",
            requested_by=f"telegram:{int(user_id)}",
        )
    except (SandboxLocationCompositionError, ValueError, TypeError, KeyError) as exc:
        raise CreatorStudioError(f"Location composition rejected: {exc}") from exc


def start_location_composition_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    envelope = location_composition_template()
    _validate_composition(conn, envelope, sandbox_id=sandbox_id, user_id=user_id)
    return _save_draft(
        conn,
        user_id,
        _wrap_composition_proposal(envelope, mode="manual", user_id=user_id),
        draft_mode="manual",
        prompt_text=None,
        sandbox_id=sandbox_id,
    )


def manual_location_composition_draft(
    conn: sqlite3.Connection,
    user_id: int,
    raw_json: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    try:
        candidate = json.loads(str(raw_json or ""))
    except json.JSONDecodeError as exc:
        raise CreatorStudioError(f"Location composition JSON is invalid: {exc.msg}") from exc
    if not isinstance(candidate, dict):
        raise CreatorStudioError("Location composition must be one JSON object")
    _validate_composition(conn, candidate, sandbox_id=sandbox_id, user_id=user_id)
    return _save_draft(
        conn,
        user_id,
        _wrap_composition_proposal(candidate, mode="manual", user_id=user_id),
        draft_mode="manual",
        prompt_text=None,
        sandbox_id=sandbox_id,
    )


def composition_from_draft(draft: Mapping[str, Any] | None) -> dict[str, Any] | None:
    if not draft or draft.get("creation_type") != "location":
        return None
    proposal = draft.get("proposal")
    if not isinstance(proposal, Mapping):
        return None
    properties = proposal.get("properties")
    if not isinstance(properties, Mapping):
        return None
    envelope = properties.get("location_composition")
    return copy.deepcopy(dict(envelope)) if isinstance(envelope, Mapping) else None


def preview_location_composition_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    envelope = composition_from_draft(draft)
    if envelope is None:
        raise CreatorStudioError("No active Location composition draft")
    return _validate_composition(conn, envelope, sandbox_id=sandbox_id, user_id=user_id)


def approve_location_composition_draft(
    conn: sqlite3.Connection,
    user_id: int,
    expected_revision: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    envelope = composition_from_draft(draft)
    if draft is None or envelope is None:
        raise CreatorStudioError("No active Location composition draft to approve")
    if int(draft["revision"]) != int(expected_revision):
        raise CreatorStudioError("Draft changed after confirmation. Review the current revision again.")
    try:
        created = materialize_location_composition(
            conn,
            envelope,
            sandbox_id=sandbox_id,
            provenance_mode="manual",
            requested_by=f"telegram:{int(user_id)}",
        )
    except (SandboxLocationCompositionError, ValueError, TypeError, KeyError) as exc:
        raise CreatorStudioError(f"Location composition approval failed: {exc}") from exc
    cancel_draft(conn, user_id, sandbox_id=sandbox_id)
    return created


__all__ = [
    "approve_location_composition_draft",
    "composition_from_draft",
    "location_composition_template",
    "manual_location_composition_draft",
    "preview_location_composition_draft",
    "start_location_composition_draft",
]

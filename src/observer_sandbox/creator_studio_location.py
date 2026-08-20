from __future__ import annotations

import copy
import json
import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID
from .creation_socket import build_creation_proposal
from .creator_studio import CreatorStudioError, _save_draft, active_draft, cancel_draft
from .location_creation_schema_v2 import LocationCreationSchemaV2Error, validate_location_payload_v2
from .sandbox_location_v2 import SandboxLocationV2Error, materialize_sandbox_location_v2


def _source_payload(value: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(value)
    payload.pop("derived", None)
    return payload


def _wrap_location_proposal(payload: dict[str, Any], *, mode: str, user_id: int) -> dict[str, Any]:
    identity = payload["identity"]
    facilities = payload["facilities"]
    return build_creation_proposal(
        "location",
        identity={"name": identity["name"]},
        properties={"location_payload": _source_payload(payload)},
        capabilities=list(facilities.get("capabilities") or []),
        provenance_mode=mode,
        requested_by=f"telegram:{int(user_id)}",
    )


def manual_location_template() -> dict[str, Any]:
    """Return a complete, sparse, valid location-v2 authoring template.

    The template intentionally contains no Sandbox object references so it can be
    copied, edited and validated before any graph dependencies exist.
    """
    return {
        "schema_version": "location-v2",
        "identity": {
            "key": "place.example.room",
            "name": "Example Room",
            "kind": "room",
            "description": "A represented room in the Creation Sandbox.",
            "functional_classes": [],
            "tags": [],
        },
        "structure": {"parent_ref": None, "exposure": "indoor"},
        "geography": {
            "address_text": None,
            "locality": None,
            "region": None,
            "country_code": None,
            "position": None,
            "bounds": None,
        },
        "spatial": {
            "area": None,
            "length": None,
            "width": None,
            "height": None,
            "elevation": None,
            "terrain": None,
            "surface": "interior_floor",
            "orientation_notes": None,
        },
        "boundary": {"type": "physical", "enclosure": "enclosed", "notes": None},
        "access": {"policy": {"mode": "public"}},
        "operations": {"initial_state": "open"},
        "topology": {"interfaces": []},
        "facilities": {
            "capabilities": [],
            "facility_types": [],
            "resource_types": [],
            "utilities": [],
        },
        "environment": {"lighting_profile": "unknown", "weather_exposure": "unknown"},
        "control": {"ownership_class": "unknown", "owner_ref": None, "operator_ref": None},
        "economic_policy": None,
        "provenance": {"source_status": "creator_authored", "source_note": None},
    }


def _validate_location_creation_payload(candidate: dict[str, Any]) -> dict[str, Any]:
    try:
        return validate_location_payload_v2(candidate)
    except LocationCreationSchemaV2Error as exc:
        raise CreatorStudioError(f"Location contract rejected the draft: {exc}") from exc


def manual_location_draft(
    conn: sqlite3.Connection,
    user_id: int,
    raw_json: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    try:
        candidate = json.loads(str(raw_json or ""))
    except json.JSONDecodeError as exc:
        raise CreatorStudioError(f"Location JSON is invalid: {exc.msg}") from exc
    if not isinstance(candidate, dict):
        raise CreatorStudioError("Location draft must be one JSON object")
    validated = _validate_location_creation_payload(candidate)
    source = _source_payload(validated)
    return _save_draft(
        conn,
        user_id,
        _wrap_location_proposal(source, mode="manual", user_id=user_id),
        draft_mode="manual",
        prompt_text=None,
        sandbox_id=sandbox_id,
    )


def approve_location_draft(
    conn: sqlite3.Connection,
    user_id: int,
    expected_revision: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    if not draft or draft.get("creation_type") != "location":
        raise CreatorStudioError("No Location draft to approve")
    if int(draft["revision"]) != int(expected_revision):
        raise CreatorStudioError("Draft changed after confirmation. Review the current revision again.")
    stored = draft["proposal"].get("properties", {}).get("location_payload")
    if not isinstance(stored, dict):
        raise CreatorStudioError("Stored Location draft payload is missing")
    validated = _validate_location_creation_payload(copy.deepcopy(stored))
    try:
        obj = materialize_sandbox_location_v2(
            conn,
            _source_payload(validated),
            sandbox_id=sandbox_id,
        )
    except SandboxLocationV2Error as exc:
        raise CreatorStudioError(f"Location approval failed graph/materialization validation: {exc}") from exc
    cancel_draft(conn, user_id, sandbox_id=sandbox_id)
    return obj


__all__ = [
    "approve_location_draft",
    "manual_location_draft",
    "manual_location_template",
]

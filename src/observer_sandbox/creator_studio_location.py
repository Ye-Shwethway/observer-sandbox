from __future__ import annotations

import copy
import json
import sqlite3
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID
from .creation_socket import build_creation_proposal
from .creator_creation_ai import creator_creation_binding
from .creator_studio import CreatorStudioError, _save_draft, active_draft, cancel_draft
from .location_creation_schema_v2 import LocationCreationSchemaV2Error, validate_location_payload_v2
from .location_schema_registry_v2 import (
    BOUNDARY_TYPES,
    ENCLOSURES,
    EXPOSURES,
    FACILITY_TYPES,
    FUNCTIONAL_CLASSES,
    INTERFACE_KINDS,
    LIGHTING_PROFILES,
    LOCATION_CAPABILITIES,
    LOCATION_KINDS,
    OPERATING_STATES,
    OWNERSHIP_CLASSES,
    RESOURCE_TYPES,
    SOURCE_STATUSES,
    SURFACES,
    TRAVERSAL_MODES,
    UTILITIES,
    WEATHER_EXPOSURES,
)
from .sandbox_location_v2 import SandboxLocationV2Error, materialize_sandbox_location_v2
from .structured_ai import generate_structured


MANUAL_LOCATION_SECTIONS = (
    "identity",
    "structure",
    "geography",
    "spatial",
    "boundary",
    "access",
    "operations",
    "topology",
    "facilities",
    "environment",
    "control",
    "economic_policy",
    "provenance",
)


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
    """Return a complete, sparse, valid location-v2 authoring template."""
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


def start_manual_location_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    validated = _validate_location_creation_payload(manual_location_template())
    source = _source_payload(validated)
    return _save_draft(
        conn,
        user_id,
        _wrap_location_proposal(source, mode="manual", user_id=user_id),
        draft_mode="manual",
        prompt_text=None,
        sandbox_id=sandbox_id,
    )


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


def update_manual_location_section(
    conn: sqlite3.Connection,
    user_id: int,
    section_key: str,
    raw_json: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    if section_key not in MANUAL_LOCATION_SECTIONS:
        raise CreatorStudioError(f"Unknown Location section: {section_key}")
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    if not draft or draft.get("creation_type") != "location" or draft.get("draft_mode") != "manual":
        raise CreatorStudioError("No active manual Location draft")
    stored = draft.get("proposal", {}).get("properties", {}).get("location_payload")
    if not isinstance(stored, dict):
        raise CreatorStudioError("Stored Location draft payload is missing")
    try:
        section_value = json.loads(str(raw_json or ""))
    except json.JSONDecodeError as exc:
        raise CreatorStudioError(f"Location section JSON is invalid: {exc.msg}") from exc
    if section_key != "economic_policy" and not isinstance(section_value, dict):
        raise CreatorStudioError(f"Location section {section_key} must be one JSON object")
    if section_key == "economic_policy" and section_value is not None and not isinstance(section_value, dict):
        raise CreatorStudioError("Location economic_policy must be one JSON object or null")

    candidate = copy.deepcopy(stored)
    candidate[section_key] = section_value
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


def _tokens(values) -> str:
    return ",".join(sorted(str(value) for value in values))


def ai_location_draft(
    conn: sqlite3.Connection,
    user_id: int,
    prompt_text: str,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    intent = str(prompt_text or "").strip()
    if not intent:
        raise CreatorStudioError("AI Location creation prompt is required")
    binding = creator_creation_binding(conn)
    if not binding:
        raise CreatorStudioError("Creator Creation AI is not configured")

    skeleton = json.dumps(manual_location_template(), ensure_ascii=False, separators=(",", ":"))
    prompt = (
        "Draft exactly one Location for the isolated Observer Sandbox Creation Sandbox. Return one JSON object only. "
        "It MUST obey location-v2 exactly and contain every top-level/member field required by the contract. "
        f"Use this exact structural skeleton as the field-shape reference: {skeleton} "
        f"Allowed identity.kind: {_tokens(LOCATION_KINDS)}. "
        f"Allowed identity.functional_classes: {_tokens(FUNCTIONAL_CLASSES)}. "
        f"Allowed structure.exposure: {_tokens(EXPOSURES)}. Allowed spatial.surface: {_tokens(SURFACES)}. "
        f"Allowed boundary.type: {_tokens(BOUNDARY_TYPES)}; enclosure: {_tokens(ENCLOSURES)}. "
        f"Allowed operations.initial_state: {_tokens(OPERATING_STATES)}. "
        f"Allowed topology interface kinds: {_tokens(INTERFACE_KINDS)}; traversal modes: {_tokens(TRAVERSAL_MODES)}. "
        f"Allowed facilities.capabilities: {_tokens(LOCATION_CAPABILITIES)}. "
        f"Allowed facility_types: {_tokens(FACILITY_TYPES)}. resource_types: {_tokens(RESOURCE_TYPES)}. utilities: {_tokens(UTILITIES)}. "
        f"Allowed environment lighting_profile: {_tokens(LIGHTING_PROFILES)}; weather_exposure: {_tokens(WEATHER_EXPOSURES)}. "
        f"Allowed control.ownership_class: {_tokens(OWNERSHIP_CLASSES)}. provenance.source_status must be one of {_tokens(SOURCE_STATUSES)}. "
        "For AI proposals use provenance.source_status='provisional'. Never author grade, derived, evaluator, threshold or reference-profile fields. "
        "Never invent a Sandbox object reference. parent_ref, destination_ref, owner_ref, operator_ref and included_in_parent_ref MUST be null "
        "unless the Creator explicitly supplied an actual Sandbox object id. Do not turn names into fake refs. "
        "Unknown geography, coordinates, bounds, dimensions, monetary values and topology facts must remain null/empty rather than guessed. "
        "Use only supported shared physical quantity units. Keep access policy separate from operations state and ownership separate from economics. "
        "economic_policy may be null when value treatment is unknown. This is a proposal only; never claim canonical existence, runtime readiness or transmigration. "
        f"Creator intent: {intent}"
    )
    candidate = generate_structured(
        conn,
        provider_id=str(binding["provider_id"]),
        model_id=str(binding["model_id"]),
        prompt=prompt,
        schema={"type": "object"},
        schema_name="observer_creator_studio_location_v2",
        parameters=dict(binding.get("parameters") or {}),
    )
    if not isinstance(candidate, dict):
        raise CreatorStudioError("Creation AI returned an invalid Location object")
    try:
        validated = validate_location_payload_v2(candidate)
    except LocationCreationSchemaV2Error as exc:
        raise CreatorStudioError(f"Creation AI Location failed exact validation: {exc}") from exc
    source = _source_payload(validated)
    return _save_draft(
        conn,
        user_id,
        _wrap_location_proposal(source, mode="ai_generated", user_id=user_id),
        draft_mode="ai_generated",
        prompt_text=intent,
        sandbox_id=sandbox_id,
    )


def reroll_location_draft(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    draft = active_draft(conn, user_id, sandbox_id=sandbox_id)
    if not draft or draft.get("creation_type") != "location":
        raise CreatorStudioError("No Location draft to reroll")
    if draft.get("draft_mode") != "ai_generated" or not draft.get("prompt_text"):
        raise CreatorStudioError("Only AI-generated Location drafts can be rerolled")
    return ai_location_draft(conn, user_id, str(draft["prompt_text"]), sandbox_id=sandbox_id)


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
    "MANUAL_LOCATION_SECTIONS",
    "ai_location_draft",
    "approve_location_draft",
    "manual_location_draft",
    "manual_location_template",
    "reroll_location_draft",
    "start_manual_location_draft",
    "update_manual_location_section",
]

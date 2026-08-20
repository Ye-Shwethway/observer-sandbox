from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


class CreationProposalError(ValueError):
    pass


PROPOSAL_VERSION = 1
SANDBOX_SCOPE = "sandbox"
PROVENANCE_MODES = frozenset({"manual", "ai_generated", "imported"})


@dataclass(frozen=True)
class CreationSocketDefinition:
    type_id: str
    schema_version: int
    label: str
    required_identity_fields: tuple[str, ...]


SOCKETS: Mapping[str, CreationSocketDefinition] = {
    "character": CreationSocketDefinition(
        type_id="character",
        schema_version=1,
        label="Character",
        required_identity_fields=("name",),
    ),
    "location": CreationSocketDefinition(
        type_id="location",
        schema_version=1,
        label="Location",
        required_identity_fields=("name",),
    ),
    "item": CreationSocketDefinition(
        type_id="item",
        schema_version=1,
        label="Item",
        required_identity_fields=("name",),
    ),
}

_ALLOWED_TOP_LEVEL = frozenset(
    {
        "proposal_version",
        "creation_type",
        "schema_version",
        "target_scope",
        "identity",
        "properties",
        "relationships",
        "capabilities",
        "provenance",
    }
)


def socket_definition(creation_type: object) -> CreationSocketDefinition:
    key = str(creation_type or "").strip().lower()
    definition = SOCKETS.get(key)
    if definition is None:
        raise CreationProposalError(f"Unsupported creation socket: {key or '<empty>'}")
    return definition


def build_creation_proposal(
    creation_type: str,
    *,
    identity: Mapping[str, Any],
    properties: Mapping[str, Any] | None = None,
    relationships: list[Mapping[str, Any]] | None = None,
    capabilities: list[str] | None = None,
    provenance_mode: str = "manual",
    requested_by: str | None = None,
) -> dict[str, Any]:
    definition = socket_definition(creation_type)
    proposal = {
        "proposal_version": PROPOSAL_VERSION,
        "creation_type": definition.type_id,
        "schema_version": definition.schema_version,
        "target_scope": SANDBOX_SCOPE,
        "identity": dict(identity),
        "properties": dict(properties or {}),
        "relationships": [dict(value) for value in (relationships or [])],
        "capabilities": list(capabilities or []),
        "provenance": {
            "mode": provenance_mode,
            "requested_by": requested_by,
        },
    }
    return validate_creation_proposal(proposal)


def validate_creation_proposal(proposal: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(proposal, Mapping):
        raise CreationProposalError("Creation proposal must be an object")

    unknown = sorted(set(proposal) - _ALLOWED_TOP_LEVEL)
    if unknown:
        raise CreationProposalError(f"Unknown creation proposal fields: {', '.join(unknown)}")

    if int(proposal.get("proposal_version", 0)) != PROPOSAL_VERSION:
        raise CreationProposalError("Unsupported creation proposal version")

    definition = socket_definition(proposal.get("creation_type"))
    if int(proposal.get("schema_version", 0)) != definition.schema_version:
        raise CreationProposalError(
            f"Creation schema version mismatch for {definition.type_id}"
        )

    if str(proposal.get("target_scope") or "") != SANDBOX_SCOPE:
        raise CreationProposalError(
            "Creation proposals are sandbox-only until explicit transmigration validation"
        )

    identity = proposal.get("identity")
    if not isinstance(identity, Mapping):
        raise CreationProposalError("Creation identity must be an object")
    missing = [
        key
        for key in definition.required_identity_fields
        if not str(identity.get(key) or "").strip()
    ]
    if missing:
        raise CreationProposalError(
            f"{definition.label} identity requires: {', '.join(missing)}"
        )

    properties = proposal.get("properties")
    if not isinstance(properties, Mapping):
        raise CreationProposalError("Creation properties must be an object")

    relationships = proposal.get("relationships")
    if not isinstance(relationships, list) or not all(
        isinstance(value, Mapping) for value in relationships
    ):
        raise CreationProposalError("Creation relationships must be an array of objects")

    capabilities = proposal.get("capabilities")
    if not isinstance(capabilities, list) or not all(
        isinstance(value, str) and value.strip() for value in capabilities
    ):
        raise CreationProposalError("Creation capabilities must be an array of strings")

    provenance = proposal.get("provenance")
    if not isinstance(provenance, Mapping):
        raise CreationProposalError("Creation provenance must be an object")
    mode = str(provenance.get("mode") or "")
    if mode not in PROVENANCE_MODES:
        raise CreationProposalError(f"Unsupported creation provenance mode: {mode}")

    return {
        "proposal_version": PROPOSAL_VERSION,
        "creation_type": definition.type_id,
        "schema_version": definition.schema_version,
        "target_scope": SANDBOX_SCOPE,
        "identity": dict(identity),
        "properties": dict(properties),
        "relationships": [dict(value) for value in relationships],
        "capabilities": list(capabilities),
        "provenance": dict(provenance),
    }


__all__ = [
    "CreationProposalError",
    "CreationSocketDefinition",
    "PROPOSAL_VERSION",
    "SANDBOX_SCOPE",
    "SOCKETS",
    "build_creation_proposal",
    "socket_definition",
    "validate_creation_proposal",
]

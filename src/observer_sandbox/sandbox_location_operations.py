from __future__ import annotations

import hashlib
import json
import sqlite3
from copy import deepcopy
from typing import Any, Mapping

from .creation_sandbox import canonical_state_fingerprint, get_sandbox_object
from .location_creation_schema_v2 import LocationCreationSchemaV2Error, validate_location_payload_v2
from .sandbox_location_v2 import SandboxLocationV2Error, get_sandbox_location_v2


class SandboxLocationOperationError(ValueError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def location_source_fingerprint(source: Mapping[str, Any]) -> str:
    return hashlib.sha256(_json(source).encode("utf-8")).hexdigest()


def _active_location(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    try:
        location = get_sandbox_location_v2(conn, object_id)
    except SandboxLocationV2Error as exc:
        raise SandboxLocationOperationError(str(exc)) from exc
    if location["lifecycle_status"] != "active":
        raise SandboxLocationOperationError("Archived Sandbox Location cannot be mutated")
    return location


def _active_same_sandbox_object(conn: sqlite3.Connection, sandbox_id: str, object_id: str, *, label: str) -> dict[str, Any]:
    try:
        obj = get_sandbox_object(conn, object_id)
    except Exception as exc:
        raise SandboxLocationOperationError(f"{label} must reference an object in the same Sandbox") from exc
    if str(obj.get("sandbox_id")) != sandbox_id:
        raise SandboxLocationOperationError(f"{label} must reference an object in the same Sandbox")
    if str(obj.get("lifecycle_status")) != "active":
        raise SandboxLocationOperationError(f"{label} must reference an active Sandbox object")
    return obj


def _active_same_sandbox_location(conn: sqlite3.Connection, sandbox_id: str, object_id: str, *, label: str) -> dict[str, Any]:
    obj = _active_same_sandbox_object(conn, sandbox_id, object_id, label=label)
    if str(obj.get("creation_type")) != "location":
        raise SandboxLocationOperationError(f"{label} must reference a Location")
    try:
        location = get_sandbox_location_v2(conn, object_id)
    except SandboxLocationV2Error as exc:
        raise SandboxLocationOperationError(f"{label} must reference an active location-v2 object") from exc
    if location["lifecycle_status"] != "active":
        raise SandboxLocationOperationError(f"{label} must reference an active Sandbox Location")
    return location


def _validate_parent_cycle(conn: sqlite3.Connection, sandbox_id: str, object_id: str, parent_ref: str | None) -> None:
    if parent_ref is None:
        return
    current = str(parent_ref)
    seen: set[str] = set()
    while current:
        if current == object_id:
            raise SandboxLocationOperationError("Location parent change would create a structural cycle")
        if current in seen:
            raise SandboxLocationOperationError("Existing Sandbox Location parent graph contains a cycle")
        seen.add(current)
        parent = _active_same_sandbox_location(conn, sandbox_id, current, label="structure.parent_ref")
        next_parent = parent["source"]["structure"]["parent_ref"]
        current = "" if next_parent is None else str(next_parent)


def _validate_graph(conn: sqlite3.Connection, current: dict[str, Any], source: Mapping[str, Any]) -> None:
    sandbox_id = str(current["sandbox_id"])
    object_id = str(current["object_id"])
    parent_ref = source["structure"]["parent_ref"]
    _validate_parent_cycle(conn, sandbox_id, object_id, None if parent_ref is None else str(parent_ref))

    for interface in source["topology"]["interfaces"]:
        destination = interface["destination_ref"]
        if destination is not None:
            _active_same_sandbox_location(
                conn,
                sandbox_id,
                str(destination),
                label=f"topology.interfaces[{interface['key']}].destination_ref",
            )

    for field in ("owner_ref", "operator_ref"):
        target = source["control"][field]
        if target is not None:
            _active_same_sandbox_object(conn, sandbox_id, str(target), label=f"control.{field}")

    economic = source["economic_policy"]
    if economic is not None and economic["included_in_parent_ref"] is not None:
        _active_same_sandbox_location(
            conn,
            sandbox_id,
            str(economic["included_in_parent_ref"]),
            label="economic_policy.included_in_parent_ref",
        )


def preflight_sandbox_location_update_v2(
    conn: sqlite3.Connection,
    object_id: str,
    payload: Mapping[str, Any],
    *,
    expected_source_fingerprint: str,
) -> dict[str, Any]:
    current = _active_location(conn, object_id)
    current_source = deepcopy(current["source"])
    actual_fingerprint = location_source_fingerprint(current_source)
    if str(expected_source_fingerprint or "") != actual_fingerprint:
        raise SandboxLocationOperationError("Location changed since edit started; review the latest approved state before applying")
    try:
        validated = validate_location_payload_v2(payload)
    except LocationCreationSchemaV2Error as exc:
        raise SandboxLocationOperationError(str(exc)) from exc
    source = {key: deepcopy(value) for key, value in validated.items() if key != "derived"}
    if str(source["identity"]["key"]) != str(current_source["identity"]["key"]):
        raise SandboxLocationOperationError("Location identity key is immutable after creation")
    _validate_graph(conn, current, source)
    return {
        "current": current,
        "source": source,
        "before_fingerprint": actual_fingerprint,
        "after_fingerprint": location_source_fingerprint(source),
    }


def _interface_rows(object_id: str, source: Mapping[str, Any]) -> list[tuple[str, str, dict[str, Any]]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for interface in source["topology"]["interfaces"]:
        destination = interface["destination_ref"]
        if destination is None or not interface["enabled"]:
            continue
        pairs: list[tuple[str, str]] = []
        direction = interface["directionality"]
        if direction in {"two_way", "outbound"}:
            pairs.append((object_id, str(destination)))
        if direction in {"two_way", "inbound"}:
            pairs.append((str(destination), object_id))
        for pair in pairs:
            entry = grouped.setdefault(pair, {"interface_keys": [], "traversal_modes": set()})
            entry["interface_keys"].append(str(interface["key"]))
            entry["traversal_modes"].update(str(mode) for mode in interface["traversal_modes"])
    return [
        (
            src,
            dst,
            {
                "projection": "location-v2",
                "authoritative_interface_details": "creation_sandbox_location_profiles.source_json",
                "interface_keys": sorted(set(entry["interface_keys"])),
                "traversal_modes": sorted(entry["traversal_modes"]),
            },
        )
        for (src, dst), entry in grouped.items()
    ]


def update_sandbox_location_v2(
    conn: sqlite3.Connection,
    object_id: str,
    payload: Mapping[str, Any],
    *,
    expected_source_fingerprint: str,
) -> dict[str, Any]:
    preflight = preflight_sandbox_location_update_v2(
        conn,
        object_id,
        payload,
        expected_source_fingerprint=expected_source_fingerprint,
    )
    current = preflight["current"]
    source = preflight["source"]
    actual_fingerprint = str(preflight["before_fingerprint"])
    sandbox_id = str(current["sandbox_id"])
    canonical_before = canonical_state_fingerprint(conn)
    previous_connection_rows = _interface_rows(object_id, current["source"])

    try:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute(
            "DELETE FROM creation_sandbox_relations WHERE sandbox_id=? AND target_object_id=? AND relation_type='contains'",
            (sandbox_id, object_id),
        )
        # Replace only topology pairs projected by this Location's current source.
        # Do not erase unrelated incoming connected_to rows authored elsewhere.
        for old_source_id, old_target_id, _ in previous_connection_rows:
            conn.execute(
                """
                DELETE FROM creation_sandbox_relations
                WHERE sandbox_id=? AND relation_type='connected_to'
                  AND source_object_id=? AND target_object_id=?
                  AND metadata_json LIKE '%\"projection\":\"location-v2\"%'
                """,
                (sandbox_id, old_source_id, old_target_id),
            )
        conn.execute(
            "DELETE FROM creation_sandbox_relations WHERE sandbox_id=? AND source_object_id=? AND relation_type='owned_by'",
            (sandbox_id, object_id),
        )

        parent_ref = source["structure"]["parent_ref"]
        if parent_ref is not None:
            conn.execute(
                "INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json) VALUES(?,?, 'contains', ?,?)",
                (sandbox_id, str(parent_ref), object_id, _json({"projection": "location-v2", "structural": True})),
            )

        for source_id, target_id, metadata in _interface_rows(object_id, source):
            conn.execute(
                """
                INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json)
                VALUES(?,?, 'connected_to', ?,?)
                ON CONFLICT(sandbox_id,source_object_id,relation_type,target_object_id)
                DO UPDATE SET metadata_json=excluded.metadata_json
                """,
                (sandbox_id, source_id, target_id, _json(metadata)),
            )

        owner_ref = source["control"]["owner_ref"]
        if owner_ref is not None:
            conn.execute(
                "INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json) VALUES(?,?, 'owned_by', ?,?)",
                (sandbox_id, object_id, str(owner_ref), _json({"projection": "location-v2"})),
            )

        properties = {
            key: source[key]
            for key in (
                "structure", "geography", "spatial", "boundary", "access", "operations",
                "topology", "facilities", "environment", "control", "economic_policy",
            )
        }
        conn.execute(
            """
            UPDATE creation_sandbox_objects SET
                identity_json=?,properties_json=?,capabilities_json=?,provenance_json=?,updated_at=CURRENT_TIMESTAMP
            WHERE object_id=? AND sandbox_id=?
            """,
            (
                _json(source["identity"]),
                _json(properties),
                _json(source["facilities"]["capabilities"]),
                _json(source["provenance"]),
                object_id,
                sandbox_id,
            ),
        )
        conn.execute(
            """
            UPDATE creation_sandbox_location_profiles SET
                kind=?,source_json=?,updated_at=CURRENT_TIMESTAMP
            WHERE object_id=? AND sandbox_id=?
            """,
            (source["identity"]["kind"], _json(source), object_id, sandbox_id),
        )
        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_location_v2_updated', ?)",
            (
                sandbox_id,
                object_id,
                _json({
                    "before_fingerprint": actual_fingerprint,
                    "after_fingerprint": location_source_fingerprint(source),
                    "runtime_started": False,
                }),
            ),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    if canonical_state_fingerprint(conn) != canonical_before:
        raise SandboxLocationOperationError("Canonical Real World changed during Sandbox Location update")
    return get_sandbox_location_v2(conn, object_id)


__all__ = [
    "SandboxLocationOperationError",
    "location_source_fingerprint",
    "preflight_sandbox_location_update_v2",
    "update_sandbox_location_v2",
]

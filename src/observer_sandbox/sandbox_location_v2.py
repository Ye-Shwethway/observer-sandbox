from __future__ import annotations

import json
import sqlite3
import uuid
from collections import defaultdict
from copy import deepcopy
from typing import Any, Mapping

from .creation_sandbox import DEFAULT_SANDBOX_ID, CreationSandboxError, ensure_sandbox, get_sandbox_object
from .location_creation_schema_v2 import LocationCreationSchemaV2Error, validate_location_payload_v2
from .location_schema_registry_v2 import LOCATION_SCHEMA_VERSION


class SandboxLocationV2Error(ValueError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _loads(value: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except (TypeError, json.JSONDecodeError) as exc:
        raise SandboxLocationV2Error("Persisted Location v2 source is malformed") from exc
    if not isinstance(parsed, dict):
        raise SandboxLocationV2Error("Persisted Location v2 source must be an object")
    return parsed


def _source_only(validated: Mapping[str, Any]) -> dict[str, Any]:
    return {key: deepcopy(value) for key, value in validated.items() if key != "derived"}


def _new_location_object_id(conn: sqlite3.Connection) -> str:
    for _ in range(8):
        candidate = f"sbx_location_{uuid.uuid4().hex[:16]}"
        canonical = conn.execute("SELECT 1 FROM entities WHERE id=?", (candidate,)).fetchone()
        sandbox = conn.execute(
            "SELECT 1 FROM creation_sandbox_objects WHERE object_id=?", (candidate,)
        ).fetchone()
        if canonical is None and sandbox is None:
            return candidate
    raise SandboxLocationV2Error("Unable to allocate collision-free Sandbox Location id")


def _active_object(
    conn: sqlite3.Connection,
    sandbox_id: str,
    object_id: str,
    *,
    label: str,
) -> sqlite3.Row:
    row = conn.execute(
        """
        SELECT object_id,creation_type,lifecycle_status
        FROM creation_sandbox_objects
        WHERE object_id=? AND sandbox_id=?
        """,
        (object_id, sandbox_id),
    ).fetchone()
    if row is None:
        raise SandboxLocationV2Error(f"{label} must reference an object in the same Sandbox")
    if str(row["lifecycle_status"]) != "active":
        raise SandboxLocationV2Error(f"{label} must reference an active Sandbox object")
    return row


def _active_location_profile(
    conn: sqlite3.Connection,
    sandbox_id: str,
    object_id: str,
    *,
    label: str,
) -> dict[str, Any]:
    row = _active_object(conn, sandbox_id, object_id, label=label)
    if str(row["creation_type"]) != "location":
        raise SandboxLocationV2Error(f"{label} must reference a Location")
    profile = conn.execute(
        """
        SELECT source_json,schema_version
        FROM creation_sandbox_location_profiles
        WHERE object_id=? AND sandbox_id=?
        """,
        (object_id, sandbox_id),
    ).fetchone()
    if profile is None or str(profile["schema_version"]) != LOCATION_SCHEMA_VERSION:
        raise SandboxLocationV2Error(f"{label} must reference an active location-v2 object")
    return _loads(str(profile["source_json"]))


def _validate_existing_parent_chain(
    conn: sqlite3.Connection,
    sandbox_id: str,
    parent_object_id: str,
) -> None:
    seen: set[str] = set()
    current: str | None = parent_object_id
    while current is not None:
        if current in seen:
            raise SandboxLocationV2Error("Existing Sandbox Location parent graph contains a cycle")
        seen.add(current)
        source = _active_location_profile(
            conn,
            sandbox_id,
            current,
            label="structure.parent_ref",
        )
        structure = source.get("structure")
        if not isinstance(structure, Mapping):
            raise SandboxLocationV2Error("Persisted parent Location has invalid structure")
        next_parent = structure.get("parent_ref")
        current = None if next_parent is None else str(next_parent)


def _validate_graph_references(
    conn: sqlite3.Connection,
    sandbox_id: str,
    source: Mapping[str, Any],
) -> None:
    parent_ref = source["structure"]["parent_ref"]
    if parent_ref is not None:
        _active_location_profile(
            conn,
            sandbox_id,
            str(parent_ref),
            label="structure.parent_ref",
        )
        _validate_existing_parent_chain(conn, sandbox_id, str(parent_ref))

    for interface in source["topology"]["interfaces"]:
        destination = interface["destination_ref"]
        if destination is None:
            continue
        _active_location_profile(
            conn,
            sandbox_id,
            str(destination),
            label=f"topology.interfaces[{interface['key']}].destination_ref",
        )

    control = source["control"]
    for field in ("owner_ref", "operator_ref"):
        target = control[field]
        if target is not None:
            _active_object(conn, sandbox_id, str(target), label=f"control.{field}")

    economic = source["economic_policy"]
    if economic is not None and economic["included_in_parent_ref"] is not None:
        _active_location_profile(
            conn,
            sandbox_id,
            str(economic["included_in_parent_ref"]),
            label="economic_policy.included_in_parent_ref",
        )


def _interface_projection_rows(
    source_object_id: str,
    interfaces: list[Mapping[str, Any]],
) -> list[tuple[str, str, dict[str, Any]]]:
    grouped: dict[tuple[str, str], dict[str, Any]] = defaultdict(
        lambda: {"interface_keys": [], "traversal_modes": set()}
    )
    for interface in interfaces:
        destination = interface["destination_ref"]
        if destination is None or not interface["enabled"]:
            continue
        direction = interface["directionality"]
        pairs: list[tuple[str, str]] = []
        if direction in {"two_way", "outbound"}:
            pairs.append((source_object_id, str(destination)))
        if direction in {"two_way", "inbound"}:
            pairs.append((str(destination), source_object_id))
        for pair in pairs:
            entry = grouped[pair]
            entry["interface_keys"].append(str(interface["key"]))
            entry["traversal_modes"].update(str(mode) for mode in interface["traversal_modes"])

    rows: list[tuple[str, str, dict[str, Any]]] = []
    for (source_id, target_id), entry in grouped.items():
        rows.append(
            (
                source_id,
                target_id,
                {
                    "projection": "location-v2",
                    "authoritative_interface_details": "creation_sandbox_location_profiles.source_json",
                    "interface_keys": sorted(set(entry["interface_keys"])),
                    "traversal_modes": sorted(entry["traversal_modes"]),
                },
            )
        )
    return rows


def materialize_sandbox_location_v2(
    conn: sqlite3.Connection,
    payload: Mapping[str, Any],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
) -> dict[str, Any]:
    try:
        validated = validate_location_payload_v2(payload)
    except LocationCreationSchemaV2Error as exc:
        raise SandboxLocationV2Error(str(exc)) from exc
    source = _source_only(validated)

    sandbox = ensure_sandbox(conn, sandbox_id)
    if sandbox["status"] != "active":
        raise SandboxLocationV2Error("Creation Sandbox is archived")

    _validate_graph_references(conn, sandbox_id, source)
    object_id = _new_location_object_id(conn)
    parent_ref = source["structure"]["parent_ref"]

    conn.execute("SAVEPOINT sandbox_location_v2_materialize")
    try:
        conn.execute(
            """
            INSERT INTO creation_sandbox_objects(
                object_id,sandbox_id,creation_type,schema_version,lifecycle_status,
                identity_json,properties_json,relationships_json,capabilities_json,provenance_json
            ) VALUES(?,?, 'location',2,'active',?,?,?,?,?)
            """,
            (
                object_id,
                sandbox_id,
                _json(source["identity"]),
                _json({
                    key: source[key]
                    for key in (
                        "structure", "geography", "spatial", "boundary", "access", "operations",
                        "topology", "facilities", "environment", "control", "economic_policy",
                    )
                }),
                _json([]),
                _json(source["facilities"]["capabilities"]),
                _json(source["provenance"]),
            ),
        )
        conn.execute(
            """
            INSERT INTO creation_sandbox_location_profiles(
                object_id,sandbox_id,location_key,schema_version,kind,source_json
            ) VALUES(?,?,?,?,?,?)
            """,
            (
                object_id,
                sandbox_id,
                source["identity"]["key"],
                LOCATION_SCHEMA_VERSION,
                source["identity"]["kind"],
                _json(source),
            ),
        )

        if parent_ref is not None:
            conn.execute(
                """
                INSERT INTO creation_sandbox_relations(
                    sandbox_id,source_object_id,relation_type,target_object_id,metadata_json
                ) VALUES(?,?, 'contains', ?,?)
                """,
                (
                    sandbox_id,
                    str(parent_ref),
                    object_id,
                    _json({"projection": "location-v2", "structural": True}),
                ),
            )

        for source_id, target_id, metadata in _interface_projection_rows(
            object_id,
            source["topology"]["interfaces"],
        ):
            conn.execute(
                """
                INSERT INTO creation_sandbox_relations(
                    sandbox_id,source_object_id,relation_type,target_object_id,metadata_json
                ) VALUES(?,?, 'connected_to', ?,?)
                ON CONFLICT(sandbox_id,source_object_id,relation_type,target_object_id)
                DO UPDATE SET metadata_json=excluded.metadata_json
                """,
                (sandbox_id, source_id, target_id, _json(metadata)),
            )

        owner_ref = source["control"]["owner_ref"]
        if owner_ref is not None:
            conn.execute(
                """
                INSERT INTO creation_sandbox_relations(
                    sandbox_id,source_object_id,relation_type,target_object_id,metadata_json
                ) VALUES(?,?, 'owned_by', ?,?)
                """,
                (sandbox_id, object_id, str(owner_ref), _json({"projection": "location-v2"})),
            )

        conn.execute(
            """
            INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json)
            VALUES(?,?, 'sandbox_location_v2_materialized', ?)
            """,
            (
                sandbox_id,
                object_id,
                _json({
                    "schema_version": LOCATION_SCHEMA_VERSION,
                    "location_key": source["identity"]["key"],
                    "kind": source["identity"]["kind"],
                    "runtime_ready": False,
                }),
            ),
        )
        conn.execute("RELEASE SAVEPOINT sandbox_location_v2_materialize")
    except Exception as exc:
        conn.execute("ROLLBACK TO SAVEPOINT sandbox_location_v2_materialize")
        conn.execute("RELEASE SAVEPOINT sandbox_location_v2_materialize")
        if isinstance(exc, SandboxLocationV2Error):
            raise
        if isinstance(exc, sqlite3.IntegrityError):
            raise SandboxLocationV2Error(f"Unable to materialize Location v2 atomically: {exc}") from exc
        raise

    conn.commit()
    return get_sandbox_location_v2(conn, object_id)


def get_sandbox_location_v2(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    obj = get_sandbox_object(conn, object_id)
    if obj["creation_type"] != "location":
        raise SandboxLocationV2Error("Sandbox object is not a Location")
    row = conn.execute(
        """
        SELECT location_key,schema_version,kind,source_json,created_at,updated_at
        FROM creation_sandbox_location_profiles
        WHERE object_id=? AND sandbox_id=?
        """,
        (object_id, obj["sandbox_id"]),
    ).fetchone()
    if row is None or str(row["schema_version"]) != LOCATION_SCHEMA_VERSION:
        raise SandboxLocationV2Error("Sandbox Location does not have a location-v2 profile")
    source = _loads(str(row["source_json"]))
    validated = validate_location_payload_v2(source)
    return {
        "object_id": object_id,
        "sandbox_id": obj["sandbox_id"],
        "lifecycle_status": obj["lifecycle_status"],
        "schema_version": str(row["schema_version"]),
        "location_key": str(row["location_key"]),
        "kind": str(row["kind"]),
        "source": _source_only(validated),
        "derived": deepcopy(validated["derived"]),
        "resolved_relations": obj["resolved_relations"],
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def list_sandbox_locations_v2(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    include_archived: bool = False,
) -> list[dict[str, Any]]:
    sql = """
        SELECT p.object_id
        FROM creation_sandbox_location_profiles p
        JOIN creation_sandbox_objects o ON o.object_id=p.object_id
        WHERE p.sandbox_id=? AND p.schema_version=?
    """
    params: list[Any] = [sandbox_id, LOCATION_SCHEMA_VERSION]
    if not include_archived:
        sql += " AND o.lifecycle_status='active'"
    sql += " ORDER BY o.created_at,o.object_id"
    return [get_sandbox_location_v2(conn, str(row["object_id"])) for row in conn.execute(sql, params).fetchall()]


__all__ = [
    "SandboxLocationV2Error",
    "get_sandbox_location_v2",
    "list_sandbox_locations_v2",
    "materialize_sandbox_location_v2",
]

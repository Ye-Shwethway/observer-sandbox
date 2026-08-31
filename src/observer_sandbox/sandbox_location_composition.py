from __future__ import annotations

import copy
import json
import re
import sqlite3
from typing import Any, Mapping, Sequence

from .creation_sandbox import DEFAULT_SANDBOX_ID, _new_object_id, ensure_sandbox, get_sandbox_object
from .creation_socket import build_creation_proposal
from .item_creation_schema import ITEM_SCHEMA_VERSION, validate_item_payload
from .location_creation_schema_v2 import validate_location_payload_v2
from .location_schema_registry_v2 import LOCATION_SCHEMA_VERSION
from .sandbox_item_creation import (
    _definition_record,
    _existing_definition,
    _insert_definition,
    _target_is_container,
    _validate_definition_reuse,
    _validate_existing_target,
    get_sandbox_item,
)
from .sandbox_location_v2 import (
    _active_location_profile,
    _active_object,
    _interface_projection_rows,
    _new_location_object_id,
    _source_only,
    _validate_existing_parent_chain,
    get_sandbox_location_v2,
)


COMPOSITION_SCHEMA_VERSION = "location-composition-v1"
_LOCAL_REF_RE = re.compile(r"^[a-z][a-z0-9_-]*$")


class SandboxLocationCompositionError(ValueError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _local_ref(value: Any) -> str | None:
    if not isinstance(value, str) or not value.startswith("$"):
        return None
    ref = value[1:]
    if not _LOCAL_REF_RE.fullmatch(ref):
        raise SandboxLocationCompositionError(f"Invalid composition local ref: {value}")
    return ref


def _parse_member(raw: Any, index: int, *, kind: str) -> tuple[str, dict[str, Any]]:
    if not isinstance(raw, Mapping) or set(raw) != {"ref", "payload"}:
        raise SandboxLocationCompositionError(
            f"Composition {kind} member {index} must contain exactly ref and payload"
        )
    ref = str(raw["ref"] or "").strip().lower()
    if not _LOCAL_REF_RE.fullmatch(ref):
        raise SandboxLocationCompositionError(
            f"Composition {kind} ref must be a stable lowercase token: {ref!r}"
        )
    if not isinstance(raw["payload"], Mapping):
        raise SandboxLocationCompositionError(f"Composition {kind} payload must be an object")
    return ref, copy.deepcopy(dict(raw["payload"]))


def _validate_existing_location_ref(
    conn: sqlite3.Connection,
    sandbox_id: str,
    value: Any,
    *,
    label: str,
) -> None:
    if value is None:
        return
    if _local_ref(value) is not None:
        return
    _active_location_profile(conn, sandbox_id, str(value), label=label)


def _validate_location_members(
    conn: sqlite3.Connection,
    sandbox_id: str,
    members: Sequence[Mapping[str, Any]],
    all_refs: Mapping[str, str],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    location_refs = {ref for ref, kind in all_refs.items() if kind == "location"}
    seen_keys: set[str] = set()
    parent_edges: dict[str, str] = {}

    for index, raw in enumerate(members):
        ref, payload = _parse_member(raw, index, kind="Location")
        try:
            validated = validate_location_payload_v2(payload)
        except (ValueError, TypeError, KeyError) as exc:
            raise SandboxLocationCompositionError(f"Location ${ref} failed location-v2 validation: {exc}") from exc
        source = _source_only(validated)
        location_key = str(source["identity"]["key"])
        if location_key in seen_keys:
            raise SandboxLocationCompositionError(f"Duplicate Location key in composition: {location_key}")
        seen_keys.add(location_key)
        existing = conn.execute(
            "SELECT object_id FROM creation_sandbox_location_profiles WHERE sandbox_id=? AND location_key=?",
            (sandbox_id, location_key),
        ).fetchone()
        if existing is not None:
            raise SandboxLocationCompositionError(
                f"Location key already exists in Sandbox: {location_key}"
            )

        parent = source["structure"]["parent_ref"]
        local_parent = _local_ref(parent)
        if local_parent is not None:
            if local_parent not in location_refs:
                raise SandboxLocationCompositionError(
                    f"Location ${ref} parent must reference a local Location: {parent}"
                )
            if local_parent == ref:
                raise SandboxLocationCompositionError("Location cannot structurally contain itself")
            parent_edges[ref] = local_parent
        elif parent is not None:
            _active_location_profile(
                conn, sandbox_id, str(parent), label=f"${ref}.structure.parent_ref"
            )
            _validate_existing_parent_chain(conn, sandbox_id, str(parent))

        for interface in source["topology"]["interfaces"]:
            destination = interface["destination_ref"]
            local_destination = _local_ref(destination)
            if local_destination is not None:
                if local_destination not in location_refs:
                    raise SandboxLocationCompositionError(
                        f"Location ${ref} interface {interface['key']} must target a local Location"
                    )
                if local_destination == ref:
                    raise SandboxLocationCompositionError(
                        f"Location ${ref} interface {interface['key']} cannot target itself"
                    )
            elif destination is not None:
                _active_location_profile(
                    conn,
                    sandbox_id,
                    str(destination),
                    label=f"${ref}.topology.interfaces[{interface['key']}].destination_ref",
                )

        control = source["control"]
        for field in ("owner_ref", "operator_ref"):
            target = control[field]
            if _local_ref(target) is not None:
                raise SandboxLocationCompositionError(
                    f"Location ${ref} control.{field} cannot use a local ref until Character composition exists"
                )
            if target is not None:
                _active_object(conn, sandbox_id, str(target), label=f"${ref}.control.{field}")

        economic = source["economic_policy"]
        if economic is not None:
            included = economic["included_in_parent_ref"]
            local_included = _local_ref(included)
            if local_included is not None and local_included not in location_refs:
                raise SandboxLocationCompositionError(
                    f"Location ${ref} economic included_in_parent_ref must target a local Location"
                )
            if local_included == ref:
                raise SandboxLocationCompositionError(
                    f"Location ${ref} cannot include its own economic value in itself"
                )
            if included is not None and local_included is None:
                _active_location_profile(
                    conn,
                    sandbox_id,
                    str(included),
                    label=f"${ref}.economic_policy.included_in_parent_ref",
                )

        result.append({"ref": ref, "source": source, "derived": copy.deepcopy(validated["derived"])})

    for start in parent_edges:
        seen: set[str] = set()
        current = start
        while current in parent_edges:
            if current in seen:
                raise SandboxLocationCompositionError("Composition Location parent graph must be acyclic")
            seen.add(current)
            current = parent_edges[current]
    return result


def _validate_item_members(
    conn: sqlite3.Connection,
    sandbox_id: str,
    members: Sequence[Mapping[str, Any]],
    all_refs: Mapping[str, str],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    by_ref: dict[str, dict[str, Any]] = {}
    definitions: dict[str, dict[str, Any]] = {}

    for index, raw in enumerate(members):
        ref, payload = _parse_member(raw, index, kind="Item")
        try:
            normalized = validate_item_payload(payload)
        except (ValueError, TypeError, KeyError) as exc:
            raise SandboxLocationCompositionError(f"Item ${ref} failed item-v1 validation: {exc}") from exc
        definition_key = str(normalized["definition"]["key"])
        record = _definition_record(normalized)
        previous = definitions.get(definition_key)
        if previous is not None and previous != record:
            raise SandboxLocationCompositionError(
                f"Composition reuses Item definition key with different semantics: {definition_key}"
            )
        definitions[definition_key] = record
        try:
            _validate_definition_reuse(
                conn,
                sandbox_id=sandbox_id,
                definition_key=definition_key,
                normalized=normalized,
            )
        except ValueError as exc:
            raise SandboxLocationCompositionError(str(exc)) from exc
        entry = {"ref": ref, "normalized": normalized}
        result.append(entry)
        by_ref[ref] = entry

    storage_edges: dict[str, str] = {}
    for entry in result:
        ref = str(entry["ref"])
        normalized = entry["normalized"]
        resolved: list[dict[str, str]] = []
        for relation_type, raw_target in sorted(normalized["relationships"].items()):
            if raw_target is None:
                continue
            local = _local_ref(raw_target)
            if local is None:
                try:
                    _validate_existing_target(
                        conn,
                        sandbox_id=sandbox_id,
                        relation_type=relation_type,
                        target_id=str(raw_target),
                    )
                except ValueError as exc:
                    raise SandboxLocationCompositionError(str(exc)) from exc
                resolved.append({"relation_type": relation_type, "target_kind": "existing", "target": str(raw_target)})
                continue

            target_kind = all_refs.get(local)
            if target_kind is None:
                raise SandboxLocationCompositionError(f"Item ${ref} references unknown local target ${local}")
            if local == ref:
                raise SandboxLocationCompositionError("Item cannot reference itself inside a composition")
            if relation_type == "located_at":
                if target_kind != "location":
                    raise SandboxLocationCompositionError("Local located_at target must be a Location")
            elif relation_type == "stored_in":
                if target_kind == "item":
                    target_modules = by_ref[local]["normalized"]["definition"]["modules"]
                    if "container" not in target_modules:
                        raise SandboxLocationCompositionError("Local stored_in Item target must be a container Item")
                    storage_edges[ref] = local
                elif target_kind != "location":
                    raise SandboxLocationCompositionError("Local stored_in target must be a Location or container Item")
            else:
                raise SandboxLocationCompositionError(
                    f"Local {relation_type} target is not supported until Character composition exists"
                )
            resolved.append({"relation_type": relation_type, "target_kind": target_kind, "target": local})
        entry["resolved_relationships"] = resolved

    for start in storage_edges:
        seen: set[str] = set()
        current = start
        while current in storage_edges:
            if current in seen:
                raise SandboxLocationCompositionError("Composition stored_in Item graph must be acyclic")
            seen.add(current)
            current = storage_edges[current]
    return result


def preview_location_composition(
    conn: sqlite3.Connection,
    envelope: Mapping[str, Any],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    provenance_mode: str = "manual",
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Validate one complete Location/Item composition without materializing members."""
    if not isinstance(envelope, Mapping) or set(envelope) != {"schema_version", "locations", "items"}:
        raise SandboxLocationCompositionError(
            "Composition envelope must contain exactly schema_version, locations and items"
        )
    if envelope["schema_version"] != COMPOSITION_SCHEMA_VERSION:
        raise SandboxLocationCompositionError("Unsupported Location composition schema version")
    locations = envelope["locations"]
    items = envelope["items"]
    if not isinstance(locations, list) or not locations:
        raise SandboxLocationCompositionError("Location composition requires at least one Location member")
    if not isinstance(items, list):
        raise SandboxLocationCompositionError("Location composition items must be a list")

    sandbox = conn.execute(
        "SELECT status FROM creation_sandboxes WHERE sandbox_id=?", (sandbox_id,)
    ).fetchone()
    if sandbox is not None and str(sandbox["status"]) != "active":
        raise SandboxLocationCompositionError("Creation Sandbox is archived")

    all_refs: dict[str, str] = {}
    for kind, members in (("location", locations), ("item", items)):
        for index, raw in enumerate(members):
            ref, _ = _parse_member(raw, index, kind=kind.title())
            if ref in all_refs:
                raise SandboxLocationCompositionError(f"Duplicate composition ref: {ref}")
            all_refs[ref] = kind

    parsed_locations = _validate_location_members(conn, sandbox_id, locations, all_refs)
    parsed_items = _validate_item_members(conn, sandbox_id, items, all_refs)
    return {
        "schema_version": COMPOSITION_SCHEMA_VERSION,
        "sandbox_id": sandbox_id,
        "locations": parsed_locations,
        "items": parsed_items,
        "count": len(parsed_locations) + len(parsed_items),
        "provenance": {"mode": provenance_mode, "requested_by": requested_by},
    }


def _resolve_local(value: Any, object_ids: Mapping[str, str]) -> Any:
    ref = _local_ref(value)
    return object_ids[ref] if ref is not None else value


def _resolved_location_source(source: Mapping[str, Any], object_ids: Mapping[str, str]) -> dict[str, Any]:
    result = copy.deepcopy(dict(source))
    result["structure"]["parent_ref"] = _resolve_local(result["structure"]["parent_ref"], object_ids)
    for interface in result["topology"]["interfaces"]:
        interface["destination_ref"] = _resolve_local(interface["destination_ref"], object_ids)
    for field in ("owner_ref", "operator_ref"):
        result["control"][field] = _resolve_local(result["control"][field], object_ids)
    if result["economic_policy"] is not None:
        result["economic_policy"]["included_in_parent_ref"] = _resolve_local(
            result["economic_policy"]["included_in_parent_ref"], object_ids
        )
    return result


def _insert_location(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str,
    object_id: str,
    source: Mapping[str, Any],
) -> None:
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


def _insert_location_relations(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str,
    object_id: str,
    source: Mapping[str, Any],
) -> None:
    parent = source["structure"]["parent_ref"]
    if parent is not None:
        conn.execute(
            "INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json) VALUES(?,?, 'contains', ?,?)",
            (sandbox_id, str(parent), object_id, _json({"projection": "location-v2", "structural": True})),
        )
    for source_id, target_id, metadata in _interface_projection_rows(object_id, source["topology"]["interfaces"]):
        conn.execute(
            """
            INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json)
            VALUES(?,?, 'connected_to', ?,?)
            ON CONFLICT(sandbox_id,source_object_id,relation_type,target_object_id)
            DO UPDATE SET metadata_json=excluded.metadata_json
            """,
            (sandbox_id, source_id, target_id, _json(metadata)),
        )
    owner = source["control"]["owner_ref"]
    if owner is not None:
        conn.execute(
            "INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json) VALUES(?,?, 'owned_by', ?,?)",
            (sandbox_id, object_id, str(owner), _json({"projection": "location-v2"})),
        )


def _insert_item(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str,
    object_id: str,
    entry: Mapping[str, Any],
    object_ids: Mapping[str, str],
    provenance: Mapping[str, Any],
) -> None:
    normalized = entry["normalized"]
    definition = normalized["definition"]
    definition_key = str(definition["key"])
    _insert_definition(
        conn,
        sandbox_id=sandbox_id,
        definition_key=definition_key,
        normalized=normalized,
        provenance=provenance,
    )
    actual_relationships = [
        {
            "relation_type": str(relation["relation_type"]),
            "target_object_id": (
                object_ids[str(relation["target"])]
                if relation["target_kind"] in {"location", "item"}
                else str(relation["target"])
            ),
        }
        for relation in entry["resolved_relationships"]
    ]
    proposal = build_creation_proposal(
        "item",
        identity={"name": definition["name"], "definition_key": definition_key},
        properties={
            "item_schema_version": normalized["schema_version"],
            "definition_key": definition_key,
            "instance": normalized["instance"],
            "economic_policy": normalized["economic_policy"],
            "requirements": normalized["requirements"],
            "derived": normalized["derived"],
        },
        relationships=actual_relationships,
        capabilities=list(definition["capabilities"]),
        provenance_mode=str(provenance["mode"]),
        requested_by=provenance.get("requested_by"),
    )
    conn.execute(
        """
        INSERT INTO creation_sandbox_objects(
            object_id,sandbox_id,creation_type,schema_version,lifecycle_status,
            identity_json,properties_json,relationships_json,capabilities_json,provenance_json
        ) VALUES(?,?, 'item',1,'active',?,?,?,?,?)
        """,
        (
            object_id,
            sandbox_id,
            _json(proposal["identity"]),
            _json(proposal["properties"]),
            _json(actual_relationships),
            _json(proposal["capabilities"]),
            _json(proposal["provenance"]),
        ),
    )
    instance = normalized["instance"]
    conn.execute(
        "INSERT INTO creation_sandbox_item_instances(object_id,sandbox_id,definition_key,instance_mode,quantity,unit) VALUES(?,?,?,?,?,?)",
        (
            object_id,
            sandbox_id,
            definition_key,
            str(instance["mode"]),
            instance.get("quantity"),
            instance.get("unit"),
        ),
    )
    economic = normalized["economic_policy"]
    conn.execute(
        "INSERT INTO creation_sandbox_item_economic_profiles(object_id,sandbox_id,classification,policy_json) VALUES(?,?,?,?)",
        (object_id, sandbox_id, str(economic["classification"]), _json(economic)),
    )
    for relation in actual_relationships:
        conn.execute(
            "INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json) VALUES(?,?,?,?, '{}')",
            (sandbox_id, object_id, relation["relation_type"], relation["target_object_id"]),
        )


def materialize_location_composition(
    conn: sqlite3.Connection,
    envelope: Mapping[str, Any],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    provenance_mode: str = "manual",
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Validate the whole graph, then materialize all members in one transaction."""
    preview = preview_location_composition(
        conn,
        envelope,
        sandbox_id=sandbox_id,
        provenance_mode=provenance_mode,
        requested_by=requested_by,
    )
    sandbox = ensure_sandbox(conn, sandbox_id)
    if sandbox["status"] != "active":
        raise SandboxLocationCompositionError("Creation Sandbox is archived")

    location_ids = {
        str(entry["ref"]): _new_location_object_id(conn)
        for entry in preview["locations"]
    }
    item_ids = {
        str(entry["ref"]): _new_object_id(conn, "item")
        for entry in preview["items"]
    }
    object_ids = {**location_ids, **item_ids}
    resolved_locations = {
        str(entry["ref"]): _resolved_location_source(entry["source"], object_ids)
        for entry in preview["locations"]
    }

    try:
        conn.execute("BEGIN IMMEDIATE")
        for ref, source in resolved_locations.items():
            _insert_location(
                conn,
                sandbox_id=sandbox_id,
                object_id=location_ids[ref],
                source=source,
            )
        for ref, source in resolved_locations.items():
            _insert_location_relations(
                conn,
                sandbox_id=sandbox_id,
                object_id=location_ids[ref],
                source=source,
            )
            conn.execute(
                "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_location_v2_materialized', ?)",
                (
                    sandbox_id,
                    location_ids[ref],
                    _json({
                        "schema_version": LOCATION_SCHEMA_VERSION,
                        "location_key": source["identity"]["key"],
                        "kind": source["identity"]["kind"],
                        "runtime_ready": False,
                        "composition_ref": ref,
                    }),
                ),
            )

        for entry in preview["items"]:
            ref = str(entry["ref"])
            _insert_item(
                conn,
                sandbox_id=sandbox_id,
                object_id=item_ids[ref],
                entry=entry,
                object_ids=object_ids,
                provenance=preview["provenance"],
            )
            conn.execute(
                "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?, 'sandbox_item_materialized', ?)",
                (
                    sandbox_id,
                    item_ids[ref],
                    _json({
                        "composition_ref": ref,
                        "definition_key": entry["normalized"]["definition"]["key"],
                        "instance_mode": entry["normalized"]["instance"]["mode"],
                        "schema_version": ITEM_SCHEMA_VERSION,
                        "provenance_mode": preview["provenance"]["mode"],
                    }),
                ),
            )

        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,NULL,'sandbox_location_composition_materialized',?)",
            (
                sandbox_id,
                _json({
                    "schema_version": COMPOSITION_SCHEMA_VERSION,
                    "locations": location_ids,
                    "items": item_ids,
                }),
            ),
        )
        conn.commit()
    except Exception as exc:
        conn.rollback()
        if isinstance(exc, SandboxLocationCompositionError):
            raise
        if isinstance(exc, sqlite3.IntegrityError):
            raise SandboxLocationCompositionError(
                f"Unable to materialize Location composition atomically: {exc}"
            ) from exc
        raise

    return {
        "schema_version": COMPOSITION_SCHEMA_VERSION,
        "sandbox_id": sandbox_id,
        "refs": object_ids,
        "locations": [get_sandbox_location_v2(conn, location_ids[str(entry["ref"])]) for entry in preview["locations"]],
        "items": [get_sandbox_item(conn, item_ids[str(entry["ref"])]) for entry in preview["items"]],
    }


__all__ = [
    "COMPOSITION_SCHEMA_VERSION",
    "SandboxLocationCompositionError",
    "materialize_location_composition",
    "preview_location_composition",
]

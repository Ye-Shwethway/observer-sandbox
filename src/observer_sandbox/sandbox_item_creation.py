from __future__ import annotations

import json
import re
import sqlite3
from copy import deepcopy
from typing import Any, Mapping, Sequence

from .creation_sandbox import (
    DEFAULT_SANDBOX_ID,
    CreationSandboxError,
    _new_object_id,
    ensure_sandbox,
    get_sandbox_object,
)
from .creation_socket import build_creation_proposal
from .item_creation_schema import ITEM_SCHEMA_VERSION, validate_item_payload


class SandboxItemCreationError(ValueError):
    pass


_BATCH_REF_RE = re.compile(r"^[a-z][a-z0-9_-]*$")
_BATCH_REF_PREFIX = "$"


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _loads(value: str, fallback: Any) -> Any:
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return fallback


def _definition_record(normalized: Mapping[str, Any]) -> dict[str, Any]:
    definition = dict(normalized["definition"])
    return {
        "schema_version": str(normalized["schema_version"]),
        "name": str(definition["name"]),
        "kind": str(definition["kind"]),
        "description": str(definition["description"]),
        "stackable": bool(definition["stackable"]),
        "mobility": str(definition["mobility"]),
        "capabilities": list(definition["capabilities"]),
        "tags": list(definition["tags"]),
        "modules": deepcopy(definition["modules"]),
        "requirements": deepcopy(normalized["requirements"]),
        "derived": deepcopy(normalized["derived"]),
    }


def _existing_definition(conn: sqlite3.Connection, sandbox_id: str, definition_key: str) -> dict[str, Any] | None:
    row = conn.execute(
        """
        SELECT schema_version,name,kind,description,stackable,mobility,
               capabilities_json,tags_json,modules_json,requirements_json,derived_json
        FROM creation_sandbox_item_definitions
        WHERE sandbox_id=? AND definition_key=?
        """,
        (sandbox_id, definition_key),
    ).fetchone()
    if row is None:
        return None
    return {
        "schema_version": str(row["schema_version"]),
        "name": str(row["name"]),
        "kind": str(row["kind"]),
        "description": str(row["description"]),
        "stackable": bool(row["stackable"]),
        "mobility": str(row["mobility"]),
        "capabilities": _loads(row["capabilities_json"], []),
        "tags": _loads(row["tags_json"], []),
        "modules": _loads(row["modules_json"], {}),
        "requirements": _loads(row["requirements_json"], {}),
        "derived": _loads(row["derived_json"], {}),
    }


def _validate_definition_reuse(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str,
    definition_key: str,
    normalized: Mapping[str, Any],
) -> None:
    existing = _existing_definition(conn, sandbox_id, definition_key)
    if existing is None:
        return
    requested = _definition_record(normalized)
    if existing != requested:
        raise SandboxItemCreationError(
            f"Sandbox Item definition key already exists with different semantics: {definition_key}"
        )


def _target_object(conn: sqlite3.Connection, sandbox_id: str, target_id: str) -> dict[str, Any]:
    try:
        target = get_sandbox_object(conn, target_id)
    except CreationSandboxError as exc:
        raise SandboxItemCreationError(f"Item relation target does not exist in Creation Sandbox: {target_id}") from exc
    if target["sandbox_id"] != sandbox_id:
        raise SandboxItemCreationError("Item relations cannot cross Sandbox namespaces")
    if target["lifecycle_status"] != "active":
        raise SandboxItemCreationError(f"Item relation target is archived: {target_id}")
    return target


def _target_is_container(conn: sqlite3.Connection, sandbox_id: str, target_id: str) -> bool:
    row = conn.execute(
        """
        SELECT d.modules_json
        FROM creation_sandbox_item_instances i
        JOIN creation_sandbox_item_definitions d
          ON d.sandbox_id=i.sandbox_id AND d.definition_key=i.definition_key
        WHERE i.sandbox_id=? AND i.object_id=?
        """,
        (sandbox_id, target_id),
    ).fetchone()
    if row is None:
        return False
    modules = _loads(row["modules_json"], {})
    return isinstance(modules, dict) and "container" in modules


def _validate_existing_target(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str,
    relation_type: str,
    target_id: str,
) -> None:
    target = _target_object(conn, sandbox_id, target_id)
    if relation_type == "located_at" and target["creation_type"] != "location":
        raise SandboxItemCreationError("located_at Item target must be a Sandbox Location")
    if relation_type in {"owned_by", "carried_by", "equipped_by"} and target["creation_type"] != "character":
        raise SandboxItemCreationError(f"{relation_type} Item target must be a Sandbox Character")
    if relation_type == "stored_in":
        valid = target["creation_type"] == "location" or (
            target["creation_type"] == "item" and _target_is_container(conn, sandbox_id, target_id)
        )
        if not valid:
            raise SandboxItemCreationError("stored_in Item target must be a Sandbox Location or container Item")


def _insert_definition(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str,
    definition_key: str,
    normalized: Mapping[str, Any],
    provenance: Mapping[str, Any],
) -> None:
    if _existing_definition(conn, sandbox_id, definition_key) is not None:
        return
    definition = normalized["definition"]
    conn.execute(
        """
        INSERT INTO creation_sandbox_item_definitions(
            sandbox_id,definition_key,schema_version,name,kind,description,stackable,mobility,
            capabilities_json,tags_json,modules_json,requirements_json,derived_json,provenance_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            sandbox_id,
            definition_key,
            str(normalized["schema_version"]),
            str(definition["name"]),
            str(definition["kind"]),
            str(definition["description"]),
            1 if definition["stackable"] else 0,
            str(definition["mobility"]),
            _json(definition["capabilities"]),
            _json(definition["tags"]),
            _json(definition["modules"]),
            _json(normalized["requirements"]),
            _json(normalized["derived"]),
            _json(provenance),
        ),
    )


def _parse_batch_entry(raw: Any, index: int) -> tuple[str, dict[str, Any]]:
    if not isinstance(raw, Mapping) or set(raw) != {"ref", "payload"}:
        raise SandboxItemCreationError(f"Batch entry {index} must contain exactly ref and payload")
    ref = str(raw["ref"] or "").strip().lower()
    if not _BATCH_REF_RE.fullmatch(ref):
        raise SandboxItemCreationError(
            f"Batch entry {index} ref must be a stable lowercase token using letters, digits, _ or -"
        )
    normalized = validate_item_payload(raw["payload"])
    return ref, normalized


def _is_batch_ref(value: str) -> bool:
    return value.startswith(_BATCH_REF_PREFIX)


def _batch_target_ref(value: str) -> str:
    return value[len(_BATCH_REF_PREFIX) :]


def _validate_batch_definition_semantics(entries: Sequence[dict[str, Any]]) -> None:
    by_key: dict[str, dict[str, Any]] = {}
    for entry in entries:
        normalized = entry["normalized"]
        key = str(normalized["definition"]["key"])
        record = _definition_record(normalized)
        previous = by_key.get(key)
        if previous is not None and previous != record:
            raise SandboxItemCreationError(
                f"Batch reuses Item definition key with different semantics: {key}"
            )
        by_key[key] = record


def _validate_internal_storage_cycles(entries: Sequence[dict[str, Any]]) -> None:
    edges: dict[str, str] = {}
    for entry in entries:
        target = entry["normalized"]["relationships"].get("stored_in")
        if isinstance(target, str) and _is_batch_ref(target):
            edges[str(entry["ref"])] = _batch_target_ref(target)

    for start in edges:
        seen: set[str] = set()
        current = start
        while current in edges:
            if current in seen:
                raise SandboxItemCreationError("Batch stored_in relationships must be acyclic")
            seen.add(current)
            current = edges[current]


def preview_sandbox_item_batch(
    conn: sqlite3.Connection,
    entries: Sequence[Mapping[str, Any]],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    provenance_mode: str = "manual",
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Validate a complete Item batch and resolve dependencies without writing Item state."""

    if isinstance(entries, (str, bytes)) or not isinstance(entries, Sequence) or not entries:
        raise SandboxItemCreationError("Item batch must be a non-empty sequence")

    sandbox_row = conn.execute(
        "SELECT status FROM creation_sandboxes WHERE sandbox_id=?",
        (sandbox_id,),
    ).fetchone()
    if sandbox_row is not None and sandbox_row["status"] != "active":
        raise SandboxItemCreationError("Creation Sandbox is archived")

    parsed: list[dict[str, Any]] = []
    refs: set[str] = set()
    for index, raw in enumerate(entries):
        ref, normalized = _parse_batch_entry(raw, index)
        if ref in refs:
            raise SandboxItemCreationError(f"Duplicate batch ref: {ref}")
        refs.add(ref)
        parsed.append({"ref": ref, "normalized": normalized})

    _validate_batch_definition_semantics(parsed)
    by_ref = {str(entry["ref"]): entry for entry in parsed}
    for entry in parsed:
        normalized = entry["normalized"]
        definition_key = str(normalized["definition"]["key"])
        _validate_definition_reuse(
            conn,
            sandbox_id=sandbox_id,
            definition_key=definition_key,
            normalized=normalized,
        )
        resolved: list[dict[str, str]] = []
        for relation_type, target in sorted(normalized["relationships"].items()):
            if target is None:
                continue
            target_id = str(target)
            if _is_batch_ref(target_id):
                target_ref = _batch_target_ref(target_id)
                if target_ref not in by_ref:
                    raise SandboxItemCreationError(f"Unknown batch Item reference: {target_id}")
                if target_ref == entry["ref"]:
                    raise SandboxItemCreationError("Item cannot reference itself inside a batch")
                if relation_type != "stored_in":
                    raise SandboxItemCreationError(
                        f"Batch-local Item reference is not valid for {relation_type}; Item batches contain Items only"
                    )
                target_modules = by_ref[target_ref]["normalized"]["definition"]["modules"]
                if "container" not in target_modules:
                    raise SandboxItemCreationError("Batch-local stored_in target must be a container Item")
                resolved.append(
                    {"relation_type": relation_type, "target_kind": "batch_ref", "target": target_ref}
                )
            else:
                _validate_existing_target(
                    conn,
                    sandbox_id=sandbox_id,
                    relation_type=relation_type,
                    target_id=target_id,
                )
                resolved.append(
                    {"relation_type": relation_type, "target_kind": "existing", "target": target_id}
                )
        entry["resolved_relationships"] = resolved

        definition = normalized["definition"]
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
            relationships=[dict(value) for value in resolved],
            capabilities=list(definition["capabilities"]),
            provenance_mode=provenance_mode,
            requested_by=requested_by,
        )
        entry["proposal"] = proposal

    _validate_internal_storage_cycles(parsed)
    return {
        "sandbox_id": sandbox_id,
        "count": len(parsed),
        "entries": parsed,
        "provenance": {"mode": provenance_mode, "requested_by": requested_by},
    }


def _materialize_preview(
    conn: sqlite3.Connection,
    preview: Mapping[str, Any],
) -> list[dict[str, Any]]:
    sandbox_id = str(preview["sandbox_id"])
    entries = list(preview["entries"])
    ensure_sandbox(conn, sandbox_id)
    object_ids = {str(entry["ref"]): _new_object_id(conn, "item") for entry in entries}

    try:
        conn.execute("BEGIN IMMEDIATE")
        for entry in entries:
            normalized = entry["normalized"]
            proposal = entry["proposal"]
            definition = normalized["definition"]
            definition_key = str(definition["key"])
            provenance = dict(proposal["provenance"])
            object_id = object_ids[str(entry["ref"])]
            _insert_definition(
                conn,
                sandbox_id=sandbox_id,
                definition_key=definition_key,
                normalized=normalized,
                provenance=provenance,
            )
            actual_relationships: list[dict[str, str]] = []
            for relation in entry["resolved_relationships"]:
                target = str(relation["target"])
                target_id = object_ids[target] if relation["target_kind"] == "batch_ref" else target
                actual_relationships.append(
                    {"relation_type": str(relation["relation_type"]), "target_object_id": target_id}
                )
            properties = dict(proposal["properties"])
            conn.execute(
                """
                INSERT INTO creation_sandbox_objects(
                    object_id,sandbox_id,creation_type,schema_version,lifecycle_status,
                    identity_json,properties_json,relationships_json,capabilities_json,provenance_json
                ) VALUES(?,?,?,?, 'active', ?,?,?,?,?)
                """,
                (
                    object_id,
                    sandbox_id,
                    "item",
                    1,
                    _json(proposal["identity"]),
                    _json(properties),
                    _json(actual_relationships),
                    _json(proposal["capabilities"]),
                    _json(provenance),
                ),
            )
            instance = normalized["instance"]
            conn.execute(
                """
                INSERT INTO creation_sandbox_item_instances(
                    object_id,sandbox_id,definition_key,instance_mode,quantity,unit
                ) VALUES(?,?,?,?,?,?)
                """,
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
                """
                INSERT INTO creation_sandbox_item_economic_profiles(
                    object_id,sandbox_id,classification,policy_json
                ) VALUES(?,?,?,?)
                """,
                (object_id, sandbox_id, str(economic["classification"]), _json(economic)),
            )

        for entry in entries:
            source_id = object_ids[str(entry["ref"])]
            for relation in entry["resolved_relationships"]:
                target = str(relation["target"])
                target_id = object_ids[target] if relation["target_kind"] == "batch_ref" else target
                conn.execute(
                    """
                    INSERT INTO creation_sandbox_relations(
                        sandbox_id,source_object_id,relation_type,target_object_id,metadata_json
                    ) VALUES(?,?,?,?, '{}')
                    """,
                    (sandbox_id, source_id, str(relation["relation_type"]), target_id),
                )

        for entry in entries:
            normalized = entry["normalized"]
            object_id = object_ids[str(entry["ref"])]
            conn.execute(
                "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
                (
                    sandbox_id,
                    object_id,
                    "sandbox_item_materialized",
                    _json(
                        {
                            "batch_ref": entry["ref"],
                            "definition_key": normalized["definition"]["key"],
                            "instance_mode": normalized["instance"]["mode"],
                            "schema_version": ITEM_SCHEMA_VERSION,
                            "provenance_mode": preview["provenance"]["mode"],
                        }
                    ),
                ),
            )
        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,NULL,?,?)",
            (
                sandbox_id,
                "sandbox_item_batch_materialized",
                _json(
                    {
                        "count": len(entries),
                        "refs": {str(ref): object_id for ref, object_id in object_ids.items()},
                    }
                ),
            ),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return [get_sandbox_item(conn, object_ids[str(entry["ref"])]) for entry in entries]


def create_sandbox_item_batch(
    conn: sqlite3.Connection,
    entries: Sequence[Mapping[str, Any]],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    provenance_mode: str = "manual",
    requested_by: str | None = None,
) -> list[dict[str, Any]]:
    """Validate, preview and atomically materialize a heterogeneous Item batch."""

    preview = preview_sandbox_item_batch(
        conn,
        entries,
        sandbox_id=sandbox_id,
        provenance_mode=provenance_mode,
        requested_by=requested_by,
    )
    return _materialize_preview(conn, preview)


def create_sandbox_item(
    conn: sqlite3.Connection,
    payload: Mapping[str, Any],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    provenance_mode: str = "manual",
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Single Item creation is the same batch service with exactly one member."""

    return create_sandbox_item_batch(
        conn,
        [{"ref": "item", "payload": payload}],
        sandbox_id=sandbox_id,
        provenance_mode=provenance_mode,
        requested_by=requested_by,
    )[0]


def get_sandbox_item(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    obj = get_sandbox_object(conn, object_id)
    if obj["creation_type"] != "item":
        raise SandboxItemCreationError("Sandbox object is not an Item")
    row = conn.execute(
        """
        SELECT i.definition_key,i.instance_mode,i.quantity,i.unit,
               d.schema_version,d.name,d.kind,d.description,d.stackable,d.mobility,
               d.capabilities_json,d.tags_json,d.modules_json,d.requirements_json,d.derived_json,
               e.policy_json
        FROM creation_sandbox_item_instances i
        JOIN creation_sandbox_item_definitions d
          ON d.sandbox_id=i.sandbox_id AND d.definition_key=i.definition_key
        JOIN creation_sandbox_item_economic_profiles e ON e.object_id=i.object_id
        WHERE i.object_id=?
        """,
        (object_id,),
    ).fetchone()
    if row is None:
        raise SandboxItemCreationError(f"Sandbox Item materialization is incomplete: {object_id}")
    instance: dict[str, Any] = {"mode": str(row["instance_mode"])}
    if row["instance_mode"] == "stack":
        instance["quantity"] = float(row["quantity"])
        instance["unit"] = str(row["unit"])
    obj["item"] = {
        "schema_version": str(row["schema_version"]),
        "definition": {
            "key": str(row["definition_key"]),
            "name": str(row["name"]),
            "kind": str(row["kind"]),
            "description": str(row["description"]),
            "stackable": bool(row["stackable"]),
            "mobility": str(row["mobility"]),
            "capabilities": _loads(row["capabilities_json"], []),
            "tags": _loads(row["tags_json"], []),
            "modules": _loads(row["modules_json"], {}),
        },
        "instance": instance,
        "economic_policy": _loads(row["policy_json"], {}),
        "requirements": _loads(row["requirements_json"], {}),
        "derived": _loads(row["derived_json"], {}),
    }
    return obj


__all__ = [
    "SandboxItemCreationError",
    "create_sandbox_item",
    "create_sandbox_item_batch",
    "get_sandbox_item",
    "preview_sandbox_item_batch",
]

from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from typing import Any, Mapping

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


def _validate_relation_targets(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str,
    relationships: Mapping[str, str | None],
) -> dict[str, dict[str, Any]]:
    resolved: dict[str, dict[str, Any]] = {}
    for relation_type, target_id in relationships.items():
        if target_id is None:
            continue
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
        resolved[relation_type] = target
    return resolved


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


def create_sandbox_item(
    conn: sqlite3.Connection,
    payload: Mapping[str, Any],
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    provenance_mode: str = "manual",
    requested_by: str | None = None,
) -> dict[str, Any]:
    """Validate and atomically materialize one Item into isolated Creation Sandbox state."""

    normalized = validate_item_payload(payload)
    sandbox = ensure_sandbox(conn, sandbox_id)
    if sandbox["status"] != "active":
        raise SandboxItemCreationError("Creation Sandbox is archived")

    definition = normalized["definition"]
    definition_key = str(definition["key"])
    _validate_definition_reuse(
        conn,
        sandbox_id=sandbox_id,
        definition_key=definition_key,
        normalized=normalized,
    )
    _validate_relation_targets(conn, sandbox_id=sandbox_id, relationships=normalized["relationships"])

    relationship_rows = [
        {"relation_type": relation_type, "target_object_id": target_id}
        for relation_type, target_id in sorted(normalized["relationships"].items())
        if target_id is not None
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
        relationships=relationship_rows,
        capabilities=list(definition["capabilities"]),
        provenance_mode=provenance_mode,
        requested_by=requested_by,
    )
    provenance = dict(proposal["provenance"])
    object_id = _new_object_id(conn, "item")

    try:
        conn.execute("BEGIN IMMEDIATE")
        _insert_definition(
            conn,
            sandbox_id=sandbox_id,
            definition_key=definition_key,
            normalized=normalized,
            provenance=provenance,
        )
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
                _json(proposal["properties"]),
                _json(proposal["relationships"]),
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
        for relation_type, target_id in sorted(normalized["relationships"].items()):
            if target_id is None:
                continue
            conn.execute(
                """
                INSERT INTO creation_sandbox_relations(
                    sandbox_id,source_object_id,relation_type,target_object_id,metadata_json
                ) VALUES(?,?,?,?, '{}')
                """,
                (sandbox_id, object_id, relation_type, target_id),
            )
        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
            (
                sandbox_id,
                object_id,
                "sandbox_item_materialized",
                _json(
                    {
                        "definition_key": definition_key,
                        "instance_mode": instance["mode"],
                        "schema_version": ITEM_SCHEMA_VERSION,
                        "provenance_mode": provenance_mode,
                    }
                ),
            ),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise

    return get_sandbox_item(conn, object_id)


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
    "get_sandbox_item",
]

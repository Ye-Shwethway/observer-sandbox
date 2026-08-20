from __future__ import annotations

import json
import math
import sqlite3
from copy import deepcopy
from typing import Any, Mapping

from .creation_sandbox import DEFAULT_SANDBOX_ID, get_sandbox_object
from .item_creation_schema import ITEM_RELATION_TYPES, validate_item_payload
from .sandbox_item_creation import (
    SandboxItemCreationError,
    _definition_record,
    _existing_definition,
    _target_is_container,
    _validate_existing_target,
    get_sandbox_item,
)


class SandboxItemOperationError(ValueError):
    pass


_PHYSICAL_RELATIONS = frozenset({"located_at", "stored_in", "carried_by", "equipped_by"})


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _active_item(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    try:
        item = get_sandbox_item(conn, object_id)
    except SandboxItemCreationError as exc:
        raise SandboxItemOperationError(str(exc)) from exc
    if item["lifecycle_status"] != "active":
        raise SandboxItemOperationError("Archived Sandbox Item cannot be mutated")
    return item


def list_sandbox_items(
    conn: sqlite3.Connection,
    *,
    sandbox_id: str = DEFAULT_SANDBOX_ID,
    include_archived: bool = False,
) -> list[dict[str, Any]]:
    sql = "SELECT object_id FROM creation_sandbox_objects WHERE sandbox_id=? AND creation_type='item'"
    params: list[Any] = [sandbox_id]
    if not include_archived:
        sql += " AND lifecycle_status='active'"
    sql += " ORDER BY created_at,object_id"
    return [get_sandbox_item(conn, str(row["object_id"])) for row in conn.execute(sql, params).fetchall()]


def item_dependencies(conn: sqlite3.Connection, object_id: str) -> list[dict[str, Any]]:
    item = get_sandbox_item(conn, object_id)
    rows = conn.execute(
        """
        SELECT source_object_id,relation_type,metadata_json
        FROM creation_sandbox_relations
        WHERE sandbox_id=? AND target_object_id=?
        ORDER BY id
        """,
        (item["sandbox_id"], object_id),
    ).fetchall()
    return [
        {
            "source_object_id": str(row["source_object_id"]),
            "relation_type": str(row["relation_type"]),
            "metadata": json.loads(row["metadata_json"] or "{}"),
        }
        for row in rows
    ]


def _sync_relationship_snapshot(conn: sqlite3.Connection, object_id: str) -> None:
    rows = conn.execute(
        """
        SELECT relation_type,target_object_id
        FROM creation_sandbox_relations
        WHERE source_object_id=?
        ORDER BY relation_type,target_object_id
        """,
        (object_id,),
    ).fetchall()
    payload = [
        {"relation_type": str(row["relation_type"]), "target_object_id": str(row["target_object_id"])}
        for row in rows
    ]
    conn.execute(
        "UPDATE creation_sandbox_objects SET relationships_json=?,updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
        (_json(payload), object_id),
    )


def _storage_cycle(conn: sqlite3.Connection, source_id: str, target_id: str) -> bool:
    if source_id == target_id:
        return True
    current = target_id
    seen: set[str] = set()
    while current not in seen:
        if current == source_id:
            return True
        seen.add(current)
        row = conn.execute(
            """
            SELECT target_object_id FROM creation_sandbox_relations
            WHERE source_object_id=? AND relation_type='stored_in'
            LIMIT 1
            """,
            (current,),
        ).fetchone()
        if row is None:
            return False
        current = str(row["target_object_id"])
    return True


def set_sandbox_item_relation(
    conn: sqlite3.Connection,
    object_id: str,
    relation_type: str,
    target_object_id: str | None,
) -> dict[str, Any]:
    item = _active_item(conn, object_id)
    relation_type = str(relation_type or "").strip()
    if relation_type not in ITEM_RELATION_TYPES:
        raise SandboxItemOperationError(f"Unsupported Item relation: {relation_type}")

    target_id = None if target_object_id is None else str(target_object_id).strip()
    if target_id == "":
        target_id = None
    if target_id is not None:
        try:
            _validate_existing_target(
                conn,
                sandbox_id=item["sandbox_id"],
                relation_type=relation_type,
                target_id=target_id,
            )
        except SandboxItemCreationError as exc:
            raise SandboxItemOperationError(str(exc)) from exc
        mobility = str(item["item"]["definition"]["mobility"])
        if mobility == "fixed" and relation_type in {"carried_by", "equipped_by"}:
            raise SandboxItemOperationError("Fixed Item cannot be carried or equipped")
        if relation_type == "stored_in" and _storage_cycle(conn, object_id, target_id):
            raise SandboxItemOperationError("stored_in relation would create a container cycle")

    try:
        conn.execute("BEGIN IMMEDIATE")
        if relation_type in _PHYSICAL_RELATIONS:
            placeholders = ",".join("?" for _ in _PHYSICAL_RELATIONS)
            conn.execute(
                f"DELETE FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type IN ({placeholders})",
                (object_id, *sorted(_PHYSICAL_RELATIONS)),
            )
        else:
            conn.execute(
                "DELETE FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type=?",
                (object_id, relation_type),
            )
        if target_id is not None:
            conn.execute(
                """
                INSERT INTO creation_sandbox_relations(
                    sandbox_id,source_object_id,relation_type,target_object_id,metadata_json
                ) VALUES(?,?,?,?, '{}')
                """,
                (item["sandbox_id"], object_id, relation_type, target_id),
            )
        _sync_relationship_snapshot(conn, object_id)
        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
            (
                item["sandbox_id"], object_id, "sandbox_item_relation_changed",
                _json({"relation_type": relation_type, "target_object_id": target_id}),
            ),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return get_sandbox_item(conn, object_id)


def set_sandbox_item_quantity(
    conn: sqlite3.Connection,
    object_id: str,
    quantity: float | int,
) -> dict[str, Any]:
    item = _active_item(conn, object_id)
    if item["item"]["instance"]["mode"] != "stack":
        raise SandboxItemOperationError("Only stack Items have mutable quantity")
    if isinstance(quantity, bool) or not isinstance(quantity, (int, float)):
        raise SandboxItemOperationError("Stack quantity must be numeric")
    value = float(quantity)
    if not math.isfinite(value) or value < 0.0:
        raise SandboxItemOperationError("Stack quantity must be finite and non-negative")
    before = float(item["item"]["instance"]["quantity"])
    conn.execute(
        "UPDATE creation_sandbox_item_instances SET quantity=?,updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
        (value, object_id),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
        (item["sandbox_id"], object_id, "sandbox_item_quantity_changed", _json({"before": before, "after": value})),
    )
    conn.commit()
    return get_sandbox_item(conn, object_id)


def update_sandbox_item(
    conn: sqlite3.Connection,
    object_id: str,
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    current = _active_item(conn, object_id)
    normalized = validate_item_payload(payload)
    current_key = str(current["item"]["definition"]["key"])
    requested_key = str(normalized["definition"]["key"])
    if requested_key != current_key:
        raise SandboxItemOperationError("Item definition key is immutable after creation")
    if str(normalized["instance"]["mode"]) != str(current["item"]["instance"]["mode"]):
        raise SandboxItemOperationError("Item instance mode is immutable after creation")

    requested_definition = _definition_record(normalized)
    existing_definition = _existing_definition(conn, current["sandbox_id"], current_key)
    definition_changed = existing_definition != requested_definition
    if definition_changed:
        count = conn.execute(
            "SELECT COUNT(*) AS n FROM creation_sandbox_item_instances WHERE sandbox_id=? AND definition_key=?",
            (current["sandbox_id"], current_key),
        ).fetchone()["n"]
        if int(count) > 1:
            raise SandboxItemOperationError("Shared Item definition cannot be changed through one instance edit")

    # Validate all requested relation targets and storage cycles before writes.
    for relation_type, target in normalized["relationships"].items():
        if target is None:
            continue
        try:
            _validate_existing_target(
                conn,
                sandbox_id=current["sandbox_id"], relation_type=relation_type, target_id=str(target),
            )
        except SandboxItemCreationError as exc:
            raise SandboxItemOperationError(str(exc)) from exc
        if relation_type == "stored_in" and _storage_cycle(conn, object_id, str(target)):
            raise SandboxItemOperationError("stored_in relation would create a container cycle")

    try:
        conn.execute("BEGIN IMMEDIATE")
        if definition_changed:
            definition = normalized["definition"]
            conn.execute(
                """
                UPDATE creation_sandbox_item_definitions SET
                    name=?,kind=?,description=?,stackable=?,mobility=?,capabilities_json=?,tags_json=?,
                    modules_json=?,requirements_json=?,derived_json=?,updated_at=CURRENT_TIMESTAMP
                WHERE sandbox_id=? AND definition_key=?
                """,
                (
                    definition["name"], definition["kind"], definition["description"],
                    1 if definition["stackable"] else 0, definition["mobility"],
                    _json(definition["capabilities"]), _json(definition["tags"]), _json(definition["modules"]),
                    _json(normalized["requirements"]), _json(normalized["derived"]),
                    current["sandbox_id"], current_key,
                ),
            )
        else:
            conn.execute(
                "UPDATE creation_sandbox_item_definitions SET requirements_json=?,derived_json=?,updated_at=CURRENT_TIMESTAMP WHERE sandbox_id=? AND definition_key=?",
                (_json(normalized["requirements"]), _json(normalized["derived"]), current["sandbox_id"], current_key),
            )
        instance = normalized["instance"]
        conn.execute(
            "UPDATE creation_sandbox_item_instances SET quantity=?,unit=?,updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
            (instance.get("quantity"), instance.get("unit"), object_id),
        )
        economic = normalized["economic_policy"]
        conn.execute(
            "UPDATE creation_sandbox_item_economic_profiles SET classification=?,policy_json=?,updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
            (economic["classification"], _json(economic), object_id),
        )
        conn.execute("DELETE FROM creation_sandbox_relations WHERE source_object_id=?", (object_id,))
        for relation_type, target in sorted(normalized["relationships"].items()):
            if target is not None:
                conn.execute(
                    "INSERT INTO creation_sandbox_relations(sandbox_id,source_object_id,relation_type,target_object_id,metadata_json) VALUES(?,?,?,?, '{}')",
                    (current["sandbox_id"], object_id, relation_type, str(target)),
                )
        _sync_relationship_snapshot(conn, object_id)
        definition = normalized["definition"]
        properties = {
            "item_schema_version": normalized["schema_version"], "definition_key": current_key,
            "instance": normalized["instance"], "economic_policy": normalized["economic_policy"],
            "requirements": normalized["requirements"], "derived": normalized["derived"],
        }
        conn.execute(
            "UPDATE creation_sandbox_objects SET identity_json=?,properties_json=?,capabilities_json=?,updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
            (_json({"name": definition["name"], "definition_key": current_key}), _json(properties), _json(definition["capabilities"]), object_id),
        )
        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
            (current["sandbox_id"], object_id, "sandbox_item_updated", _json({"definition_changed": definition_changed})),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return get_sandbox_item(conn, object_id)


def archive_sandbox_item(
    conn: sqlite3.Connection,
    object_id: str,
    *,
    detach_dependents: bool = False,
) -> dict[str, Any]:
    item = _active_item(conn, object_id)
    dependencies = item_dependencies(conn, object_id)
    if dependencies and not detach_dependents:
        raise SandboxItemOperationError("Item has incoming dependencies; explicit detach_dependents=True is required")
    try:
        conn.execute("BEGIN IMMEDIATE")
        if detach_dependents:
            for dependency in dependencies:
                conn.execute(
                    "DELETE FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type=? AND target_object_id=?",
                    (dependency["source_object_id"], dependency["relation_type"], object_id),
                )
                _sync_relationship_snapshot(conn, dependency["source_object_id"])
        conn.execute("DELETE FROM creation_sandbox_relations WHERE source_object_id=?", (object_id,))
        conn.execute(
            "UPDATE creation_sandbox_objects SET lifecycle_status='archived',relationships_json='[]',updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
            (object_id,),
        )
        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
            (item["sandbox_id"], object_id, "sandbox_item_archived", _json({"detached_dependents": len(dependencies) if detach_dependents else 0})),
        )
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return get_sandbox_item(conn, object_id)


def delete_sandbox_item(
    conn: sqlite3.Connection,
    object_id: str,
    *,
    detach_dependents: bool = False,
) -> None:
    item = get_sandbox_item(conn, object_id)
    dependencies = item_dependencies(conn, object_id)
    if dependencies and not detach_dependents:
        raise SandboxItemOperationError("Item has incoming dependencies; explicit detach_dependents=True is required")
    definition_key = str(item["item"]["definition"]["key"])
    try:
        conn.execute("BEGIN IMMEDIATE")
        if detach_dependents:
            for dependency in dependencies:
                conn.execute(
                    "DELETE FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type=? AND target_object_id=?",
                    (dependency["source_object_id"], dependency["relation_type"], object_id),
                )
                _sync_relationship_snapshot(conn, dependency["source_object_id"])
        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,?,?)",
            (item["sandbox_id"], object_id, "sandbox_item_deleted", _json({"definition_key": definition_key})),
        )
        conn.execute("DELETE FROM creation_sandbox_objects WHERE object_id=?", (object_id,))
        remaining = conn.execute(
            "SELECT COUNT(*) AS n FROM creation_sandbox_item_instances WHERE sandbox_id=? AND definition_key=?",
            (item["sandbox_id"], definition_key),
        ).fetchone()["n"]
        if int(remaining) == 0:
            conn.execute(
                "DELETE FROM creation_sandbox_item_definitions WHERE sandbox_id=? AND definition_key=?",
                (item["sandbox_id"], definition_key),
            )
        conn.commit()
    except Exception:
        conn.rollback()
        raise


__all__ = [
    "SandboxItemOperationError",
    "archive_sandbox_item",
    "delete_sandbox_item",
    "item_dependencies",
    "list_sandbox_items",
    "set_sandbox_item_quantity",
    "set_sandbox_item_relation",
    "update_sandbox_item",
]

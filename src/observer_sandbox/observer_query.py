from __future__ import annotations

import json
import sqlite3
from typing import Any

from .action_privacy import action_visible_to_role
from .actor_selection import resolve_actor_id
from .autonomy import autonomy_status
from .location_runtime import current_location
from .simulation import snapshot
from .world import get_field


def _entity(conn: sqlite3.Connection, entity_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT id, entity_type, name, capabilities_json, definition_id FROM entities WHERE id=?",
        (entity_id,),
    ).fetchone()
    if row is None:
        return None
    return {
        "id": row["id"],
        "type": row["entity_type"],
        "name": row["name"],
        "capabilities": json.loads(row["capabilities_json"]),
        "definition_id": row["definition_id"],
    }


def _entity_name(conn: sqlite3.Connection, entity_id: str | None) -> str | None:
    if not entity_id:
        return None
    entity = _entity(conn, entity_id)
    return entity["name"] if entity else None


def _location_record(conn: sqlite3.Connection, entity: dict[str, Any]) -> dict[str, Any]:
    result = dict(entity)
    if entity["type"] == "location":
        result["kind"] = get_field(conn, entity["id"], "world.location_kind", "location")
        result["access"] = get_field(conn, entity["id"], "world.access", "open")
        result["canon"] = bool(get_field(conn, entity["id"], "world.canon", False))
        result["metadata"] = get_field(conn, entity["id"], "world.metadata", {}) or {}
    return result


def _definition(conn: sqlite3.Connection, definition_id: str | None) -> dict[str, Any] | None:
    if not definition_id:
        return None
    row = conn.execute(
        """
        SELECT id, entity_type, name, capabilities_json, properties_json, effects_json, metadata_json
        FROM entity_definitions WHERE id=?
        """,
        (definition_id,),
    ).fetchone()
    if row is None:
        return None
    return {
        "id": row["id"],
        "type": row["entity_type"],
        "name": row["name"],
        "capabilities": json.loads(row["capabilities_json"]),
        "properties": json.loads(row["properties_json"]),
        "effects": json.loads(row["effects_json"]),
        "metadata": json.loads(row["metadata_json"]),
    }


def _default_location_id(conn: sqlite3.Connection) -> str:
    rows = conn.execute(
        """
        SELECT child.id
        FROM entities parent
        JOIN relations r ON r.source_id=parent.id AND r.relation_type='contains'
        JOIN entities child ON child.id=r.target_id AND child.entity_type='location'
        WHERE parent.entity_type='world'
        ORDER BY child.id
        """
    ).fetchall()
    if len(rows) == 1:
        return str(rows[0][0])
    if not rows:
        raise KeyError("No top-level location is available")
    raise ValueError("Multiple top-level locations exist; pass location_id explicitly")


def _observer_action(action_name: str | None, role: str) -> str | None:
    if action_visible_to_role(action_name, role):
        return action_name
    return "private_activity" if action_name else action_name


def _observer_state(state: dict[str, Any], role: str) -> dict[str, Any]:
    result = dict(state)
    result["current_action"] = _observer_action(result.get("current_action"), role)
    return result


def list_worlds(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT id, entity_type, name, capabilities_json, definition_id FROM entities WHERE entity_type='world' ORDER BY name"
    ).fetchall()
    return [
        {
            "id": row["id"],
            "type": row["entity_type"],
            "name": row["name"],
            "capabilities": json.loads(row["capabilities_json"]),
            "definition_id": row["definition_id"],
        }
        for row in rows
    ]


def list_locations(conn: sqlite3.Connection, parent_id: str | None = None) -> list[dict[str, Any]]:
    if parent_id:
        rows = conn.execute(
            """
            SELECT e.id, e.entity_type, e.name, e.capabilities_json, e.definition_id
            FROM relations r
            JOIN entities e ON e.id=r.target_id
            WHERE r.source_id=? AND r.relation_type='contains' AND e.entity_type='location'
            ORDER BY e.name
            """,
            (parent_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, entity_type, name, capabilities_json, definition_id FROM entities WHERE entity_type='location' ORDER BY name"
        ).fetchall()
    return [
        _location_record(
            conn,
            {
                "id": row["id"],
                "type": row["entity_type"],
                "name": row["name"],
                "capabilities": json.loads(row["capabilities_json"]),
                "definition_id": row["definition_id"],
            },
        )
        for row in rows
    ]


def list_characters(conn: sqlite3.Connection, *, role: str = "owner") -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT id, entity_type, name, capabilities_json, definition_id FROM entities WHERE entity_type='character' ORDER BY name"
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        state = _observer_state(snapshot(conn, row["id"]), role)
        result.append(
            {
                "id": row["id"],
                "type": row["entity_type"],
                "name": row["name"],
                "capabilities": json.loads(row["capabilities_json"]),
                "definition_id": row["definition_id"],
                "location": state["location"],
                "location_name": state["location_name"],
                "current_action": state["current_action"],
            }
        )
    return result


def character_summary(conn: sqlite3.Connection, character_id: str | None = None, *, role: str = "owner") -> dict[str, Any]:
    character_id = resolve_actor_id(conn, character_id)
    entity = _entity(conn, character_id)
    if entity is None:
        raise KeyError(f"Unknown character: {character_id}")
    state = _observer_state(snapshot(conn, character_id), role)
    return {"character": entity, "state": state}


def object_summary(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    entity = _entity(conn, object_id)
    if entity is None or entity["type"] != "object":
        raise KeyError(f"Unknown object: {object_id}")

    definition = _definition(conn, entity.get("definition_id"))
    location_id = current_location(conn, object_id)
    location = _entity(conn, location_id) if location_id else None

    instance_effects = get_field(conn, object_id, "game.effects", {}) or {}
    definition_effects = (definition or {}).get("effects") or {}
    effective_effects = instance_effects or definition_effects

    instance_capabilities = entity.get("capabilities") or []
    definition_capabilities = (definition or {}).get("capabilities") or []
    effective_capabilities = instance_capabilities or definition_capabilities

    return {
        "object": entity,
        "definition": definition,
        "location": location,
        "capabilities": effective_capabilities,
        "effects": effective_effects,
    }


def recent_location_activity(
    conn: sqlite3.Connection,
    *,
    location_id: str,
    limit: int = 3,
    role: str = "owner",
) -> list[dict[str, Any]]:
    limit = max(1, min(int(limit), 20))
    rows = conn.execute(
        """
        SELECT id, sim_time, actor_id, event_type, payload_json
        FROM events
        WHERE location_id=? AND event_type='action_completed'
        ORDER BY id DESC
        LIMIT ?
        """,
        (location_id, max(limit * 3, limit)),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        payload = json.loads(row["payload_json"])
        action = payload.get("action")
        if not action_visible_to_role(action, role):
            continue
        target = payload.get("target")
        result.append(
            {
                "id": row["id"],
                "sim_time": row["sim_time"],
                "event_type": row["event_type"],
                "actor_id": row["actor_id"],
                "actor_name": _entity_name(conn, row["actor_id"]),
                "action": action,
                "target": target,
                "target_name": _entity_name(conn, target),
                "reason": payload.get("reason"),
            }
        )
        if len(result) >= limit:
            break
    return result


def location_summary(conn: sqlite3.Connection, location_id: str | None = None, *, role: str = "owner") -> dict[str, Any]:
    location_id = location_id or _default_location_id(conn)
    entity = _entity(conn, location_id)
    if entity is None:
        raise KeyError(f"Unknown location: {location_id}")
    location = _location_record(conn, entity)

    parent_row = conn.execute(
        """
        SELECT e.id, e.entity_type, e.name, e.capabilities_json, e.definition_id
        FROM relations r JOIN entities e ON e.id=r.source_id
        WHERE r.target_id=? AND r.relation_type='contains'
        ORDER BY CASE e.entity_type WHEN 'world' THEN 0 ELSE 1 END
        LIMIT 1
        """,
        (location_id,),
    ).fetchone()
    parent = None
    if parent_row is not None:
        parent = {
            "id": parent_row["id"],
            "type": parent_row["entity_type"],
            "name": parent_row["name"],
            "capabilities": json.loads(parent_row["capabilities_json"]),
            "definition_id": parent_row["definition_id"],
        }
        if parent["type"] == "location":
            parent = _location_record(conn, parent)

    children = conn.execute(
        """
        SELECT e.id, e.entity_type, e.name, e.capabilities_json, e.definition_id
        FROM relations r
        JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='contains'
        ORDER BY CASE e.entity_type WHEN 'location' THEN 0 ELSE 1 END, e.name
        """,
        (location_id,),
    ).fetchall()
    child_locations: list[dict[str, Any]] = []
    objects: list[dict[str, Any]] = []
    for row in children:
        record = {
            "id": row["id"],
            "type": row["entity_type"],
            "name": row["name"],
            "capabilities": json.loads(row["capabilities_json"]),
            "definition_id": row["definition_id"],
        }
        if row["entity_type"] == "location":
            child_locations.append(_location_record(conn, record))
        elif row["entity_type"] == "object":
            record["effects"] = get_field(conn, row["id"], "game.effects", {}) or {}
            objects.append(record)

    residents = conn.execute(
        """
        SELECT e.id, e.entity_type, e.name
        FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='resident'
        ORDER BY e.name
        """,
        (location_id,),
    ).fetchall()

    occupants: list[dict[str, Any]] = []
    if entity["type"] == "location":
        rows = conn.execute(
            "SELECT id, name FROM entities WHERE entity_type='character' ORDER BY name"
        ).fetchall()
        for row in rows:
            if current_location(conn, row["id"]) == location_id:
                state = _observer_state(snapshot(conn, row["id"]), role)
                occupants.append(
                    {
                        "id": row["id"],
                        "name": row["name"],
                        "current_action": state["current_action"],
                    }
                )

    exits = conn.execute(
        """
        SELECT e.id, e.name
        FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='connected_to' AND e.entity_type='location'
        ORDER BY e.name
        """,
        (location_id,),
    ).fetchall()

    return {
        "location": location,
        "parent": parent,
        "children": child_locations + objects,
        "child_locations": child_locations,
        "objects": objects,
        "residents": [dict(row) for row in residents],
        "occupants": occupants,
        "exits": [dict(row) for row in exits],
        "recent_activity": recent_location_activity(conn, location_id=location_id, limit=3, role=role),
    }


def recent_history(
    conn: sqlite3.Connection,
    *,
    character_id: str | None = None,
    limit: int = 8,
    role: str = "owner",
) -> list[dict[str, Any]]:
    """Return user-facing completed character actions, not internal engine receipts."""
    character_id = resolve_actor_id(conn, character_id)
    limit = max(1, min(int(limit), 50))
    rows = conn.execute(
        """
        SELECT id, sim_time, event_type, payload_json
        FROM events
        WHERE actor_id=? AND event_type='action_completed'
        ORDER BY id DESC
        LIMIT ?
        """,
        (character_id, max(limit * 3, limit)),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        payload = json.loads(row["payload_json"])
        action = payload.get("action")
        if action and not action_visible_to_role(action, role):
            continue
        target = payload.get("target")
        result.append(
            {
                "id": row["id"],
                "sim_time": row["sim_time"],
                "event_type": row["event_type"],
                "action": action,
                "target": target,
                "target_name": _entity_name(conn, target),
                "reason": payload.get("reason"),
                "payload": payload,
            }
        )
        if len(result) >= limit:
            break
    return result


def observer_status(conn: sqlite3.Connection, character_id: str | None = None, *, role: str = "owner") -> dict[str, Any]:
    character_id = resolve_actor_id(conn, character_id)
    status = autonomy_status(conn, character_id)
    status["character"] = _observer_state(dict(status["character"]), role)
    pending = status.get("pending_action")
    if pending:
        if action_visible_to_role(pending.get("action"), role):
            status["pending_target_name"] = _entity_name(conn, pending.get("target"))
        else:
            redacted = dict(pending)
            redacted.update({"action": "private_activity", "target": None, "reason": None, "resources": [], "conditions": {}, "modifiers": {}})
            status["pending_action"] = redacted
            status["pending_target_name"] = None
    status["recent_history"] = recent_history(conn, character_id=character_id, limit=5, role=role)
    return status

from __future__ import annotations

import json
import sqlite3
from typing import Any

from .autonomy import autonomy_status
from .simulation import snapshot
from .world import get_field


def _entity(conn: sqlite3.Connection, entity_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT id, entity_type, name, capabilities_json FROM entities WHERE id=?",
        (entity_id,),
    ).fetchone()
    if row is None:
        return None
    return {
        "id": row["id"],
        "type": row["entity_type"],
        "name": row["name"],
        "capabilities": json.loads(row["capabilities_json"]),
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


def list_worlds(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT id, entity_type, name, capabilities_json FROM entities WHERE entity_type='world' ORDER BY name"
    ).fetchall()
    return [
        {
            "id": row["id"],
            "type": row["entity_type"],
            "name": row["name"],
            "capabilities": json.loads(row["capabilities_json"]),
        }
        for row in rows
    ]


def list_locations(conn: sqlite3.Connection, parent_id: str | None = None) -> list[dict[str, Any]]:
    if parent_id:
        rows = conn.execute(
            """
            SELECT e.id, e.entity_type, e.name, e.capabilities_json
            FROM relations r
            JOIN entities e ON e.id=r.target_id
            WHERE r.source_id=? AND r.relation_type='contains' AND e.entity_type='location'
            ORDER BY e.name
            """,
            (parent_id,),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, entity_type, name, capabilities_json FROM entities WHERE entity_type='location' ORDER BY name"
        ).fetchall()
    return [
        _location_record(
            conn,
            {
                "id": row["id"],
                "type": row["entity_type"],
                "name": row["name"],
                "capabilities": json.loads(row["capabilities_json"]),
            },
        )
        for row in rows
    ]


def list_characters(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT id, entity_type, name, capabilities_json FROM entities WHERE entity_type='character' ORDER BY name"
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        state = snapshot(conn, row["id"])
        result.append(
            {
                "id": row["id"],
                "type": row["entity_type"],
                "name": row["name"],
                "capabilities": json.loads(row["capabilities_json"]),
                "location": state["location"],
                "location_name": state["location_name"],
                "current_action": state["current_action"],
            }
        )
    return result


def character_summary(conn: sqlite3.Connection, character_id: str = "char_darian") -> dict[str, Any]:
    entity = _entity(conn, character_id)
    if entity is None:
        raise KeyError(f"Unknown character: {character_id}")
    state = snapshot(conn, character_id)
    return {"character": entity, "state": state}


def location_summary(conn: sqlite3.Connection, location_id: str = "home") -> dict[str, Any]:
    entity = _entity(conn, location_id)
    if entity is None:
        raise KeyError(f"Unknown location: {location_id}")
    location = _location_record(conn, entity)

    parent_row = conn.execute(
        """
        SELECT e.id, e.entity_type, e.name, e.capabilities_json
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
        }
        if parent["type"] == "location":
            parent = _location_record(conn, parent)

    children = conn.execute(
        """
        SELECT e.id, e.entity_type, e.name, e.capabilities_json
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
            """
            SELECT e.id, e.name, f.value_json
            FROM entities e
            JOIN fields f ON f.entity_id=e.id AND f.field_key='runtime.location'
            WHERE e.entity_type='character'
            """
        ).fetchall()
        for row in rows:
            if json.loads(row["value_json"]) == location_id:
                occupants.append({"id": row["id"], "name": row["name"]})

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
    }


def recent_history(conn: sqlite3.Connection, *, character_id: str = "char_darian", limit: int = 8) -> list[dict[str, Any]]:
    limit = max(1, min(int(limit), 50))
    rows = conn.execute(
        "SELECT id, sim_time, event_type, payload_json FROM events WHERE actor_id=? ORDER BY id DESC LIMIT ?",
        (character_id, limit),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        payload = json.loads(row["payload_json"])
        target = payload.get("target")
        result.append(
            {
                "id": row["id"],
                "sim_time": row["sim_time"],
                "event_type": row["event_type"],
                "action": payload.get("action"),
                "target": target,
                "target_name": _entity_name(conn, target),
                "reason": payload.get("reason"),
                "payload": payload,
            }
        )
    return result


def observer_status(conn: sqlite3.Connection, character_id: str = "char_darian") -> dict[str, Any]:
    status = autonomy_status(conn, character_id)
    pending = status.get("pending_action")
    if pending:
        status["pending_target_name"] = _entity_name(conn, pending.get("target"))
    status["recent_history"] = recent_history(conn, character_id=character_id, limit=5)
    return status

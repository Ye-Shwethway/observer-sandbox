from __future__ import annotations

import json
import sqlite3
from typing import Any

from .autonomy import autonomy_status
from .simulation import snapshot


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

    children = conn.execute(
        """
        SELECT e.id, e.entity_type, e.name, e.capabilities_json
        FROM relations r
        JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='contains'
        ORDER BY e.entity_type, e.name
        """,
        (location_id,),
    ).fetchall()
    residents = conn.execute(
        """
        SELECT e.id, e.entity_type, e.name
        FROM relations r
        JOIN entities e ON e.id=r.target_id
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

    return {
        "location": entity,
        "children": [
            {
                "id": row["id"],
                "type": row["entity_type"],
                "name": row["name"],
                "capabilities": json.loads(row["capabilities_json"]),
            }
            for row in children
        ],
        "residents": [dict(row) for row in residents],
        "occupants": occupants,
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
        result.append(
            {
                "id": row["id"],
                "sim_time": row["sim_time"],
                "event_type": row["event_type"],
                "action": payload.get("action"),
                "target": payload.get("target"),
                "reason": payload.get("reason"),
                "payload": payload,
            }
        )
    return result


def observer_status(conn: sqlite3.Connection, character_id: str = "char_darian") -> dict[str, Any]:
    status = autonomy_status(conn, character_id)
    status["recent_history"] = recent_history(conn, character_id=character_id, limit=5)
    return status

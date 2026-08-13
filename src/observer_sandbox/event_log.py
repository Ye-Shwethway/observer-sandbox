from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any


def record_event(
    conn: sqlite3.Connection,
    *,
    sim_time: str,
    event_type: str,
    actor_id: str | None = None,
    action_id: str | None = None,
    location_id: str | None = None,
    participants: list[dict[str, str]] | None = None,
    caused_by_event_id: int | None = None,
    state_changes: dict[str, Any] | None = None,
    payload: dict[str, Any] | None = None,
) -> int:
    event_uuid = str(uuid.uuid4())
    cur = conn.execute(
        """INSERT INTO events(
            sim_time,actor_id,event_type,payload_json,event_uuid,action_id,location_id,caused_by_event_id,state_changes_json
        ) VALUES(?,?,?,?,?,?,?,?,?)""",
        (
            sim_time,
            actor_id,
            event_type,
            json.dumps(payload or {}, ensure_ascii=False),
            event_uuid,
            action_id,
            location_id,
            caused_by_event_id,
            json.dumps(state_changes or {}, ensure_ascii=False),
        ),
    )
    event_id = int(cur.lastrowid)
    rows = list(participants or [])
    if actor_id and not any(row.get("entity_id") == actor_id for row in rows):
        rows.append({"entity_id": actor_id, "role": "actor"})
    for row in rows:
        entity_id = row.get("entity_id")
        if entity_id:
            conn.execute(
                "INSERT OR IGNORE INTO event_participants(event_id,entity_id,role) VALUES(?,?,?)",
                (event_id, entity_id, row.get("role") or "participant"),
            )
    return event_id

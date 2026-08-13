from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any

from .training_methods import training_method_evidence, training_profile_for_target


def _enrich_training_method(payload: dict[str, Any], event_type: str) -> dict[str, Any]:
    if event_type != "action_completed" or payload.get("action") != "train" or "training_method" in payload:
        return payload
    target = payload.get("target")
    profile = training_profile_for_target(target if isinstance(target, str) else None)
    evidence = training_method_evidence(
        action_name="train",
        target=target if isinstance(target, str) else None,
        training_profile=profile,
        training_load=payload.get("training_load") if isinstance(payload.get("training_load"), dict) else None,
    )
    if evidence is None:
        return payload
    enriched = dict(payload)
    enriched["training_method"] = evidence
    return enriched


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
    event_payload = _enrich_training_method(dict(payload or {}), event_type)
    cur = conn.execute(
        """INSERT INTO events(
            sim_time,actor_id,event_type,payload_json,event_uuid,action_id,location_id,caused_by_event_id,state_changes_json
        ) VALUES(?,?,?,?,?,?,?,?,?)""",
        (
            sim_time,
            actor_id,
            event_type,
            json.dumps(event_payload, ensure_ascii=False),
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

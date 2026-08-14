from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any

from .eating_behavior import settle_eating_action
from .nutrition_energy import energy_expenditure_evidence, nutrition_intake_evidence
from .training_methods import training_method_evidence


def _enrich_training_method(payload: dict[str, Any], event_type: str) -> dict[str, Any]:
    if event_type != "action_completed" or payload.get("action") != "train" or "training_method" in payload:
        return payload
    target = payload.get("target")
    training_load = payload.get("training_load")
    evidence = training_method_evidence(
        action_name="train",
        target=target if isinstance(target, str) else None,
        training_load=training_load if isinstance(training_load, dict) else None,
    )
    if evidence is None:
        return payload
    enriched = dict(payload)
    enriched["training_method"] = evidence
    return enriched


def _enrich_nutrition_energy(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    event_type: str,
    *,
    actor_id: str | None,
    action_id: str | None,
    sim_time: str,
) -> dict[str, Any]:
    if event_type != "action_completed" or not actor_id:
        return payload
    action_name = payload.get("action")
    duration = payload.get("duration_minutes")
    if not isinstance(action_name, str) or not isinstance(duration, (int, float)):
        return payload
    target = payload.get("target")
    target_id = target if isinstance(target, str) else None
    enriched = dict(payload)

    if "nutrition_intake" not in enriched:
        nutrition = None
        if action_name == "eat" and action_id:
            try:
                nutrition = settle_eating_action(conn, action_id)
            except Exception:
                # Completion mutations and inventory settlement belong to one
                # transaction boundary. Roll back the whole completion before
                # surfacing the deterministic failure to autonomy handling.
                conn.rollback()
                raise
        if nutrition is None:
            # Compatibility path for pre-Eating-Behavior in-flight eat actions.
            nutrition = nutrition_intake_evidence(action_name=action_name, target=target_id)
        if nutrition is not None:
            enriched["nutrition_intake"] = nutrition

    if "energy_expenditure" not in enriched:
        reference_time = payload.get("action_started_sim_time")
        if not isinstance(reference_time, str):
            reference_time = sim_time
        energy = energy_expenditure_evidence(
            conn,
            actor_id,
            action_name=action_name,
            target=target_id,
            duration_minutes=float(duration),
            as_of_sim_time=reference_time,
        )
        if energy is not None:
            enriched["energy_expenditure"] = energy

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
    event_payload = _enrich_nutrition_energy(
        conn,
        event_payload,
        event_type,
        actor_id=actor_id,
        action_id=action_id,
        sim_time=sim_time,
    )
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

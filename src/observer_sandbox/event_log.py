from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any

from .controlled_h2h_runtime import (
    SPAR_ACTION,
    action_participants,
    controlled_h2h_application_evidence,
    controlled_h2h_outcome,
)
from .nutrition_energy import energy_expenditure_evidence, nutrition_intake_evidence
from .represented_skill_runtime_batch import (
    BATCH_ACTIONS,
    represented_skill_batch_application_evidence,
    represented_skill_batch_outcome,
)
from .skill_practice import skill_practice_evidence
from .tactical_assessment_runtime import (
    ASSESS_ACTION,
    tactical_assessment_application_evidence,
    tactical_assessment_outcome,
)
from .technology_diagnostic_runtime import (
    DIAGNOSE_ACTION,
    technology_diagnostic_application_evidence,
    technology_diagnostic_outcome,
)
from .training_methods import training_method_evidence


def _enrich_training_method(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    event_type: str,
    *,
    action_id: str | None,
) -> dict[str, Any]:
    if event_type != "action_completed" or payload.get("action") != "train" or "training_method" in payload:
        return payload
    target = payload.get("target")
    training_load = payload.get("training_load")
    conditions = payload.get("conditions")
    if not isinstance(conditions, dict) and action_id:
        row = conn.execute("SELECT conditions_json FROM action_instances WHERE id=?", (action_id,)).fetchone()
        if row is not None:
            parsed = json.loads(row[0] or "{}")
            conditions = parsed if isinstance(parsed, dict) else None
    training_movements = conditions.get("training_movements") if isinstance(conditions, dict) else None
    evidence = training_method_evidence(
        action_name="train",
        target=target if isinstance(target, str) else None,
        training_load=training_load if isinstance(training_load, dict) else None,
        training_movements=training_movements if isinstance(training_movements, list) else None,
    )
    if evidence is None:
        return payload
    enriched = dict(payload)
    enriched["training_method"] = evidence
    return enriched


def _enrich_skill_practice(payload: dict[str, Any], event_type: str) -> dict[str, Any]:
    if event_type != "action_completed" or payload.get("action") != "practice" or "skill_practice" in payload:
        return payload
    target = payload.get("target")
    duration = payload.get("duration_minutes")
    if not isinstance(target, str) or not isinstance(duration, (int, float)):
        return payload
    evidence = skill_practice_evidence(
        action_name="practice",
        target_id=target,
        duration_minutes=int(duration),
    )
    if evidence is None:
        return payload
    enriched = dict(payload)
    enriched["skill_practice"] = evidence
    return enriched


def _persist_represented_skill_evidence(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    *,
    action_id: str,
    outcome: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    enriched = dict(payload)
    enriched["represented_skill_task"] = outcome
    enriched["skill_application"] = evidence
    row = conn.execute(
        "SELECT outcome_json FROM action_instances WHERE id=?",
        (action_id,),
    ).fetchone()
    if row is not None:
        current = json.loads(row["outcome_json"] or "{}")
        if not isinstance(current, dict):
            current = {}
        current["represented_skill_task"] = outcome
        current["skill_application"] = evidence
        conn.execute(
            "UPDATE action_instances SET outcome_json=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (json.dumps(current, ensure_ascii=False), action_id),
        )
    return enriched


def _enrich_technology_diagnostic(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    event_type: str,
    *,
    actor_id: str | None,
    action_id: str | None,
) -> dict[str, Any]:
    if (
        event_type != "action_completed"
        or payload.get("action") != DIAGNOSE_ACTION
        or not actor_id
        or not action_id
        or "skill_application" in payload
    ):
        return payload
    target = payload.get("target")
    duration = payload.get("duration_minutes")
    if not isinstance(target, str) or not isinstance(duration, (int, float)):
        conn.rollback()
        raise ValueError("Completed diagnose action requires target and duration")

    try:
        diagnostic = technology_diagnostic_outcome(conn, actor_id, target)
        evidence = technology_diagnostic_application_evidence(
            diagnostic,
            action_id=action_id,
            actor_id=actor_id,
            duration_minutes=int(duration),
        )
        return _persist_represented_skill_evidence(
            conn,
            payload,
            action_id=action_id,
            outcome=diagnostic,
            evidence=evidence,
        )
    except Exception:
        conn.rollback()
        raise


def _enrich_tactical_assessment(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    event_type: str,
    *,
    actor_id: str | None,
    action_id: str | None,
) -> dict[str, Any]:
    if (
        event_type != "action_completed"
        or payload.get("action") != ASSESS_ACTION
        or not actor_id
        or not action_id
        or "skill_application" in payload
    ):
        return payload
    target = payload.get("target")
    duration = payload.get("duration_minutes")
    if not isinstance(target, str) or not isinstance(duration, (int, float)):
        conn.rollback()
        raise ValueError("Completed assess action requires target and duration")

    try:
        assessment = tactical_assessment_outcome(conn, actor_id, target)
        evidence = tactical_assessment_application_evidence(
            assessment,
            action_id=action_id,
            actor_id=actor_id,
            duration_minutes=int(duration),
        )
        return _persist_represented_skill_evidence(
            conn,
            payload,
            action_id=action_id,
            outcome=assessment,
            evidence=evidence,
        )
    except Exception:
        conn.rollback()
        raise


def _enrich_represented_skill_batch(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    event_type: str,
    *,
    actor_id: str | None,
    action_id: str | None,
) -> dict[str, Any]:
    action_name = payload.get("action")
    if (
        event_type != "action_completed"
        or action_name not in BATCH_ACTIONS
        or not actor_id
        or not action_id
        or "skill_application" in payload
    ):
        return payload
    target = payload.get("target")
    duration = payload.get("duration_minutes")
    if not isinstance(action_name, str) or not isinstance(target, str) or not isinstance(duration, (int, float)):
        conn.rollback()
        raise ValueError("Completed represented Skill batch action requires target and duration")

    try:
        outcome = represented_skill_batch_outcome(conn, actor_id, action_name, target)
        evidence = represented_skill_batch_application_evidence(
            outcome,
            action_id=action_id,
            actor_id=actor_id,
            duration_minutes=int(duration),
        )
        return _persist_represented_skill_evidence(
            conn,
            payload,
            action_id=action_id,
            outcome=outcome,
            evidence=evidence,
        )
    except Exception:
        conn.rollback()
        raise


def _enrich_controlled_h2h(
    conn: sqlite3.Connection,
    payload: dict[str, Any],
    event_type: str,
    *,
    actor_id: str | None,
    action_id: str | None,
) -> dict[str, Any]:
    if (
        event_type != "action_completed"
        or payload.get("action") != SPAR_ACTION
        or not actor_id
        or not action_id
        or "skill_application" in payload
    ):
        return payload
    target = payload.get("target")
    duration = payload.get("duration_minutes")
    if not isinstance(target, str) or not isinstance(duration, (int, float)):
        conn.rollback()
        raise ValueError("Completed spar action requires target and duration")

    try:
        participants = action_participants(conn, action_id)
        outcome = controlled_h2h_outcome(conn, actor_id, target, participants)
        evidence = controlled_h2h_application_evidence(
            outcome,
            action_id=action_id,
            actor_id=actor_id,
            duration_minutes=int(duration),
        )
        return _persist_represented_skill_evidence(
            conn,
            payload,
            action_id=action_id,
            outcome=outcome,
            evidence=evidence,
        )
    except Exception:
        conn.rollback()
        raise


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
            from .eating_behavior import settle_eating_action

            try:
                nutrition = settle_eating_action(conn, action_id)
            except Exception:
                conn.rollback()
                raise
        if nutrition is None:
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
    event_payload = _enrich_training_method(
        conn,
        dict(payload or {}),
        event_type,
        action_id=action_id,
    )
    event_payload = _enrich_skill_practice(event_payload, event_type)
    event_payload = _enrich_technology_diagnostic(
        conn,
        event_payload,
        event_type,
        actor_id=actor_id,
        action_id=action_id,
    )
    event_payload = _enrich_tactical_assessment(
        conn,
        event_payload,
        event_type,
        actor_id=actor_id,
        action_id=action_id,
    )
    event_payload = _enrich_represented_skill_batch(
        conn,
        event_payload,
        event_type,
        actor_id=actor_id,
        action_id=action_id,
    )
    event_payload = _enrich_controlled_h2h(
        conn,
        event_payload,
        event_type,
        actor_id=actor_id,
        action_id=action_id,
    )
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

    if event_type == "action_completed" and isinstance(event_payload.get("skill_application"), dict):
        evidence_payload = dict(event_payload["skill_application"])
        conn.execute(
            """INSERT INTO events(
                sim_time,actor_id,event_type,payload_json,event_uuid,action_id,location_id,
                caused_by_event_id,state_changes_json
            ) VALUES(?,?,?,?,?,?,?,?,?)""",
            (
                sim_time,
                actor_id,
                "skill_application_evidence",
                json.dumps(evidence_payload, ensure_ascii=False),
                str(uuid.uuid4()),
                action_id,
                location_id,
                event_id,
                json.dumps({}, ensure_ascii=False),
            ),
        )
    return event_id

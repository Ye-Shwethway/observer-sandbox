from __future__ import annotations

import json
import sqlite3
from typing import Any

from .casualty_state_lifecycle import initialize_casualty_state
from .event_log import record_event
from .location_runtime import current_location


SOURCE = "represented-accident-casualty-producer-v1"
EVENT_TYPE = "represented_accident_occurred"
ORIGIN_KIND = "represented_accident"
CASUALTY_ROLE = "casualty"

# V1 deliberately proves one accident invariant only. More producers should be
# added by pattern after this exemplar rather than by growing a generic engine.
ACCIDENT_KINDS = {"represented_fall"}
RISK_CLASS_TO_DETERIORATION = {
    "low": 25.0,
    "moderate": 50.0,
    "high": 75.0,
}


class RepresentedAccidentCasualtyError(ValueError):
    pass


def _validate_incident_id(incident_id: str) -> str:
    value = str(incident_id).strip()
    if not value:
        raise RepresentedAccidentCasualtyError("Represented accident incident_id is required")
    return value


def _validate_casualty_and_location(
    conn: sqlite3.Connection,
    casualty_id: str,
    location_id: str,
) -> None:
    casualty = conn.execute(
        "SELECT entity_type FROM entities WHERE id=?",
        (casualty_id,),
    ).fetchone()
    if casualty is None or casualty["entity_type"] != "character":
        raise RepresentedAccidentCasualtyError(
            "Represented accident casualty must be an existing character"
        )

    location = conn.execute(
        "SELECT entity_type FROM entities WHERE id=?",
        (location_id,),
    ).fetchone()
    if location is None or location["entity_type"] not in {"location", "world"}:
        raise RepresentedAccidentCasualtyError(
            "Represented accident location must be an existing spatial entity"
        )

    actual_location = current_location(conn, casualty_id)
    if actual_location != location_id:
        raise RepresentedAccidentCasualtyError(
            "Represented accident casualty must be located at the declared accident location"
        )


def _prior_incident(
    conn: sqlite3.Connection,
    incident_id: str,
) -> tuple[sqlite3.Row, dict[str, Any]] | None:
    rows = conn.execute(
        "SELECT id,actor_id,location_id,payload_json FROM events WHERE event_type=? ORDER BY id",
        (EVENT_TYPE,),
    ).fetchall()
    for row in rows:
        try:
            payload = json.loads(row["payload_json"] or "{}")
        except (TypeError, json.JSONDecodeError):
            continue
        if payload.get("source") == SOURCE and payload.get("incident_id") == incident_id:
            return row, payload
    return None


def record_represented_accident_casualty(
    conn: sqlite3.Connection,
    *,
    incident_id: str,
    casualty_id: str,
    location_id: str,
    sim_time: str,
    accident_kind: str,
    risk_class: str,
) -> dict[str, Any]:
    """Emit one typed represented accident and initialize casualty state.

    V1 accepts no free-form accident description and does not infer wounds,
    diagnoses, treatment, incapacity, or death. A finite risk class maps to the
    abstract deterioration-risk field owned by the casualty lifecycle contract.
    """

    incident_id = _validate_incident_id(incident_id)
    if accident_kind not in ACCIDENT_KINDS:
        raise RepresentedAccidentCasualtyError(
            f"Unsupported represented accident kind {accident_kind!r}"
        )
    if risk_class not in RISK_CLASS_TO_DETERIORATION:
        raise RepresentedAccidentCasualtyError(
            f"Unsupported represented accident risk class {risk_class!r}"
        )
    if not isinstance(sim_time, str) or not sim_time.strip():
        raise RepresentedAccidentCasualtyError("Represented accident sim_time is required")

    _validate_casualty_and_location(conn, casualty_id, location_id)
    deterioration_risk = RISK_CLASS_TO_DETERIORATION[risk_class]

    prior = _prior_incident(conn, incident_id)
    if prior is not None:
        event, payload = prior
        expected = {
            "casualty_id": casualty_id,
            "location_id": location_id,
            "accident_kind": accident_kind,
            "risk_class": risk_class,
        }
        actual = {
            "casualty_id": payload.get("casualty_id"),
            "location_id": event["location_id"],
            "accident_kind": payload.get("accident_kind"),
            "risk_class": payload.get("risk_class"),
        }
        if actual != expected:
            raise RepresentedAccidentCasualtyError(
                "Represented accident incident_id already exists with different semantics"
            )
        lifecycle = initialize_casualty_state(
            conn,
            casualty_id=casualty_id,
            deterioration_risk=deterioration_risk,
            source_event_id=int(event["id"]),
            origin_kind=ORIGIN_KIND,
        )
        return {
            "already_applied": True,
            "incident_id": incident_id,
            "source_event_id": int(event["id"]),
            "lifecycle_event_id": lifecycle["event_id"],
            "casualty_id": casualty_id,
            "deterioration_risk": lifecycle["deterioration_risk"],
        }

    conn.execute("SAVEPOINT represented_accident_casualty_v1")
    try:
        source_event_id = record_event(
            conn,
            sim_time=sim_time,
            event_type=EVENT_TYPE,
            actor_id=casualty_id,
            location_id=location_id,
            participants=[{"entity_id": casualty_id, "role": CASUALTY_ROLE}],
            payload={
                "source": SOURCE,
                "incident_id": incident_id,
                "casualty_id": casualty_id,
                "accident_kind": accident_kind,
                "risk_class": risk_class,
                "deterioration_risk": deterioration_risk,
                "injury_created": False,
                "diagnosis_created": False,
                "incapacity_created": False,
                "learning_evidence": False,
            },
        )
        lifecycle = initialize_casualty_state(
            conn,
            casualty_id=casualty_id,
            deterioration_risk=deterioration_risk,
            source_event_id=source_event_id,
            origin_kind=ORIGIN_KIND,
        )
        conn.execute("RELEASE SAVEPOINT represented_accident_casualty_v1")
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT represented_accident_casualty_v1")
        conn.execute("RELEASE SAVEPOINT represented_accident_casualty_v1")
        raise

    return {
        "already_applied": False,
        "incident_id": incident_id,
        "source_event_id": source_event_id,
        "lifecycle_event_id": lifecycle["event_id"],
        "casualty_id": casualty_id,
        "deterioration_risk": deterioration_risk,
    }

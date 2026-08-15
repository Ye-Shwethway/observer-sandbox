from __future__ import annotations

import json
import sqlite3
from typing import Any

from .event_log import record_event
from .field_medicine_stabilization import DETERIORATION_FIELD
from .world import get_field, set_field


SOURCE = "casualty-state-origin-lifecycle-v1"
AUTHORITY = "casualty_state_runtime"
INITIALIZED_EVENT = "casualty_state_initialized"
CLEARED_EVENT = "casualty_state_cleared"
CASUALTY_ROLE = "casualty"

ORIGIN_KINDS = {
    "represented_domain_consequence",
    "represented_environmental_hazard",
    "represented_accident",
}
RESOLUTION_KINDS = {
    "evacuated_or_handed_off",
    "casualty_context_resolved",
}


class CasualtyStateLifecycleError(ValueError):
    pass


def _source_event(
    conn: sqlite3.Connection,
    source_event_id: int,
    casualty_id: str,
) -> sqlite3.Row:
    event = conn.execute(
        "SELECT id,sim_time,actor_id,action_id,location_id,event_type FROM events WHERE id=?",
        (source_event_id,),
    ).fetchone()
    if event is None:
        raise CasualtyStateLifecycleError(
            f"Casualty lifecycle source event {source_event_id!r} does not exist"
        )
    participant = conn.execute(
        """SELECT 1 FROM event_participants
        WHERE event_id=? AND entity_id=? AND role=?""",
        (source_event_id, casualty_id, CASUALTY_ROLE),
    ).fetchone()
    if participant is None:
        raise CasualtyStateLifecycleError(
            "Casualty lifecycle source event must explicitly bind the character as role 'casualty'"
        )
    entity = conn.execute(
        "SELECT entity_type FROM entities WHERE id=?",
        (casualty_id,),
    ).fetchone()
    if entity is None or entity["entity_type"] != "character":
        raise CasualtyStateLifecycleError(
            "Casualty lifecycle subject must be a represented character"
        )
    return event


def _field_row(conn: sqlite3.Connection, casualty_id: str) -> sqlite3.Row | None:
    return conn.execute(
        """SELECT value_json,mode,authority,source FROM fields
        WHERE entity_id=? AND field_key=?""",
        (casualty_id, DETERIORATION_FIELD),
    ).fetchone()


def _numeric_risk(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CasualtyStateLifecycleError("Casualty deterioration risk must be numeric")
    value = float(value)
    if not 0.0 <= value <= 100.0:
        raise CasualtyStateLifecycleError(
            "Casualty deterioration risk must be within 0..100"
        )
    return value


def _prior_lifecycle_event(
    conn: sqlite3.Connection,
    *,
    event_type: str,
    source_event_id: int,
    casualty_id: str,
) -> dict[str, Any] | None:
    rows = conn.execute(
        """SELECT id,payload_json FROM events
        WHERE event_type=? AND caused_by_event_id=? ORDER BY id""",
        (event_type, source_event_id),
    ).fetchall()
    for row in rows:
        try:
            payload = json.loads(row["payload_json"] or "{}")
        except (TypeError, json.JSONDecodeError):
            continue
        if payload.get("source") == SOURCE and payload.get("casualty_id") == casualty_id:
            return {"event_id": int(row["id"]), "payload": payload}
    return None


def initialize_casualty_state(
    conn: sqlite3.Connection,
    *,
    casualty_id: str,
    deterioration_risk: float,
    source_event_id: int,
    origin_kind: str,
) -> dict[str, Any]:
    """Create the minimum represented casualty state from one explicit causal event.

    This is the only V1 owner of creating ``medical.deterioration_risk``. The
    source event must already exist and explicitly bind the subject with role
    ``casualty``. Nothing here infers injury, diagnosis, or treatment from prose.
    """

    if origin_kind not in ORIGIN_KINDS:
        raise CasualtyStateLifecycleError(
            f"Unsupported casualty origin kind {origin_kind!r}"
        )
    risk = _numeric_risk(deterioration_risk)
    source_event = _source_event(conn, source_event_id, casualty_id)

    prior = _prior_lifecycle_event(
        conn,
        event_type=INITIALIZED_EVENT,
        source_event_id=source_event_id,
        casualty_id=casualty_id,
    )
    if prior is not None:
        return {
            "already_applied": True,
            "event_id": prior["event_id"],
            "casualty_id": casualty_id,
            "deterioration_risk": get_field(conn, casualty_id, DETERIORATION_FIELD),
        }

    if _field_row(conn, casualty_id) is not None:
        raise CasualtyStateLifecycleError(
            "Casualty deterioration state already exists; origin cannot overwrite it"
        )

    conn.execute("SAVEPOINT casualty_state_initialize_v1")
    try:
        set_field(
            conn,
            casualty_id,
            DETERIORATION_FIELD,
            risk,
            mode="simulated",
            authority=AUTHORITY,
            source=SOURCE,
        )
        event_id = record_event(
            conn,
            sim_time=str(source_event["sim_time"]),
            event_type=INITIALIZED_EVENT,
            actor_id=source_event["actor_id"],
            action_id=source_event["action_id"],
            location_id=source_event["location_id"],
            participants=[{"entity_id": casualty_id, "role": CASUALTY_ROLE}],
            caused_by_event_id=source_event_id,
            state_changes={
                "fields": {
                    DETERIORATION_FIELD: {
                        "before": None,
                        "after": risk,
                        "operation": "create",
                    }
                }
            },
            payload={
                "source": SOURCE,
                "casualty_id": casualty_id,
                "origin_kind": origin_kind,
                "source_event_id": source_event_id,
                "source_event_type": source_event["event_type"],
                "state_field": DETERIORATION_FIELD,
                "learning_evidence": False,
                "diagnosis_created": False,
                "definitive_treatment_created": False,
            },
        )
        conn.execute("RELEASE SAVEPOINT casualty_state_initialize_v1")
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT casualty_state_initialize_v1")
        conn.execute("RELEASE SAVEPOINT casualty_state_initialize_v1")
        raise

    return {
        "already_applied": False,
        "event_id": event_id,
        "casualty_id": casualty_id,
        "deterioration_risk": risk,
    }


def clear_casualty_state(
    conn: sqlite3.Connection,
    *,
    casualty_id: str,
    source_event_id: int,
    resolution_kind: str,
) -> dict[str, Any]:
    """End the represented casualty context without asserting healing.

    Clearing is explicit and causal. Risk reaching zero is deliberately not an
    automatic lifecycle trigger because stabilization is not definitive treatment.
    """

    if resolution_kind not in RESOLUTION_KINDS:
        raise CasualtyStateLifecycleError(
            f"Unsupported casualty resolution kind {resolution_kind!r}"
        )
    source_event = _source_event(conn, source_event_id, casualty_id)

    prior = _prior_lifecycle_event(
        conn,
        event_type=CLEARED_EVENT,
        source_event_id=source_event_id,
        casualty_id=casualty_id,
    )
    if prior is not None:
        return {
            "already_applied": True,
            "event_id": prior["event_id"],
            "casualty_id": casualty_id,
        }

    row = _field_row(conn, casualty_id)
    if row is None:
        raise CasualtyStateLifecycleError("Casualty deterioration state does not exist")
    if row["mode"] != "simulated" or row["authority"] != AUTHORITY or row["source"] != SOURCE:
        raise CasualtyStateLifecycleError(
            "Casualty lifecycle may clear only state created by its own V1 authority"
        )
    try:
        before = _numeric_risk(json.loads(row["value_json"]))
    except (TypeError, json.JSONDecodeError) as exc:
        raise CasualtyStateLifecycleError(
            "Casualty deterioration state contains invalid JSON"
        ) from exc

    conn.execute("SAVEPOINT casualty_state_clear_v1")
    try:
        conn.execute(
            "DELETE FROM fields WHERE entity_id=? AND field_key=?",
            (casualty_id, DETERIORATION_FIELD),
        )
        event_id = record_event(
            conn,
            sim_time=str(source_event["sim_time"]),
            event_type=CLEARED_EVENT,
            actor_id=source_event["actor_id"],
            action_id=source_event["action_id"],
            location_id=source_event["location_id"],
            participants=[{"entity_id": casualty_id, "role": CASUALTY_ROLE}],
            caused_by_event_id=source_event_id,
            state_changes={
                "fields": {
                    DETERIORATION_FIELD: {
                        "before": before,
                        "after": None,
                        "operation": "delete",
                    }
                }
            },
            payload={
                "source": SOURCE,
                "casualty_id": casualty_id,
                "resolution_kind": resolution_kind,
                "source_event_id": source_event_id,
                "source_event_type": source_event["event_type"],
                "state_field": DETERIORATION_FIELD,
                "healing_asserted": False,
                "diagnosis_resolved": False,
                "learning_evidence": False,
            },
        )
        conn.execute("RELEASE SAVEPOINT casualty_state_clear_v1")
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT casualty_state_clear_v1")
        conn.execute("RELEASE SAVEPOINT casualty_state_clear_v1")
        raise

    return {
        "already_applied": False,
        "event_id": event_id,
        "casualty_id": casualty_id,
        "deterioration_risk_before_clear": before,
    }

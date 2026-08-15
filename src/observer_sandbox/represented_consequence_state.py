from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from typing import Any, Iterable

from .event_log import record_event


SOURCE = "represented-consequence-state-foundation-v1"
EVENT_TYPE = "represented_consequence_applied"
ALLOWED_OPERATIONS = {"add", "multiply", "set", "clamp_min", "clamp_max"}
ALLOWED_SUBJECT_ROLES = {"actor", "target", "participant"}


class RepresentedConsequenceStateError(ValueError):
    pass


@dataclass(frozen=True)
class StateMutation:
    field_key: str
    operation: str
    value: Any


@dataclass(frozen=True)
class ConsequenceAuthorization:
    consequence_id: str
    represented_task_id: str
    subject_id: str
    subject_role: str
    mutations: tuple[StateMutation, ...]


def _validate_authorization(authorization: ConsequenceAuthorization) -> None:
    if not authorization.consequence_id.strip():
        raise RepresentedConsequenceStateError("Consequence id must be non-empty")
    if not authorization.represented_task_id.strip():
        raise RepresentedConsequenceStateError("Represented task id must be non-empty")
    if not authorization.subject_id.strip():
        raise RepresentedConsequenceStateError("Consequence subject id must be non-empty")
    if authorization.subject_role not in ALLOWED_SUBJECT_ROLES:
        raise RepresentedConsequenceStateError(
            f"Unsupported consequence subject role {authorization.subject_role!r}"
        )
    if not authorization.mutations:
        raise RepresentedConsequenceStateError("At least one authorized state mutation is required")

    seen_fields: set[str] = set()
    for mutation in authorization.mutations:
        if not mutation.field_key.strip():
            raise RepresentedConsequenceStateError("Mutation field key must be non-empty")
        if mutation.field_key in seen_fields:
            raise RepresentedConsequenceStateError(
                f"Duplicate mutation field {mutation.field_key!r} is not allowed in v1"
            )
        seen_fields.add(mutation.field_key)
        if mutation.operation not in ALLOWED_OPERATIONS:
            raise RepresentedConsequenceStateError(
                f"Unsupported consequence operation {mutation.operation!r}"
            )


def _action_context(conn: sqlite3.Connection, action_id: str) -> sqlite3.Row:
    row = conn.execute(
        """SELECT id,action_type,actor_id,place_id,target_id,status,ended_sim_time,outcome_json
        FROM action_instances WHERE id=?""",
        (action_id,),
    ).fetchone()
    if row is None:
        raise RepresentedConsequenceStateError(f"Source action {action_id!r} does not exist")
    if row["status"] != "completed":
        raise RepresentedConsequenceStateError("Represented consequence requires a completed source action")
    if not row["ended_sim_time"]:
        raise RepresentedConsequenceStateError("Completed source action lacks ended simulation time")
    return row


def _represented_task_id(action: sqlite3.Row) -> str:
    try:
        outcome = json.loads(action["outcome_json"] or "{}")
    except (TypeError, json.JSONDecodeError) as exc:
        raise RepresentedConsequenceStateError("Source action outcome JSON is invalid") from exc
    if not isinstance(outcome, dict):
        raise RepresentedConsequenceStateError("Source action outcome must be an object")
    represented = outcome.get("represented_skill_task")
    if not isinstance(represented, dict):
        raise RepresentedConsequenceStateError(
            "Source action does not contain a validated represented Skill task outcome"
        )
    task = represented.get("task")
    if not isinstance(task, dict) or not isinstance(task.get("task_id"), str):
        raise RepresentedConsequenceStateError("Represented Skill task outcome lacks task identity")
    return str(task["task_id"])


def _validate_subject_relation(
    conn: sqlite3.Connection,
    action: sqlite3.Row,
    authorization: ConsequenceAuthorization,
) -> None:
    if conn.execute("SELECT 1 FROM entities WHERE id=?", (authorization.subject_id,)).fetchone() is None:
        raise RepresentedConsequenceStateError(
            f"Consequence subject {authorization.subject_id!r} does not exist"
        )

    if authorization.subject_role == "actor":
        allowed = authorization.subject_id == action["actor_id"]
    elif authorization.subject_role == "target":
        allowed = bool(action["target_id"]) and authorization.subject_id == action["target_id"]
    else:
        allowed = conn.execute(
            "SELECT 1 FROM action_participants WHERE action_id=? AND entity_id=?",
            (action["id"], authorization.subject_id),
        ).fetchone() is not None

    if not allowed:
        raise RepresentedConsequenceStateError(
            f"Consequence subject is not the authorized {authorization.subject_role} of source action"
        )


def _completion_event(conn: sqlite3.Connection, action_id: str) -> sqlite3.Row:
    row = conn.execute(
        """SELECT id,sim_time FROM events
        WHERE action_id=? AND event_type='action_completed'
        ORDER BY id DESC LIMIT 1""",
        (action_id,),
    ).fetchone()
    if row is None:
        raise RepresentedConsequenceStateError(
            "Represented consequence requires the source action completion event"
        )
    return row


def _prior_application(
    conn: sqlite3.Connection,
    action_id: str,
    authorization: ConsequenceAuthorization,
) -> dict[str, Any] | None:
    rows = conn.execute(
        """SELECT id,payload_json,state_changes_json FROM events
        WHERE action_id=? AND event_type=? ORDER BY id""",
        (action_id, EVENT_TYPE),
    ).fetchall()
    for row in rows:
        try:
            payload = json.loads(row["payload_json"] or "{}")
            changes = json.loads(row["state_changes_json"] or "{}")
        except (TypeError, json.JSONDecodeError):
            continue
        if not isinstance(payload, dict):
            continue
        if (
            payload.get("consequence_id") == authorization.consequence_id
            and payload.get("represented_task_id") == authorization.represented_task_id
            and payload.get("subject_id") == authorization.subject_id
        ):
            return {
                "event_id": int(row["id"]),
                "already_applied": True,
                "state_changes": changes if isinstance(changes, dict) else {},
                "payload": payload,
            }
    return None


def _field_rows(
    conn: sqlite3.Connection,
    subject_id: str,
    mutations: Iterable[StateMutation],
) -> dict[str, sqlite3.Row]:
    rows: dict[str, sqlite3.Row] = {}
    for mutation in mutations:
        row = conn.execute(
            """SELECT field_key,value_json,mode,authority,source FROM fields
            WHERE entity_id=? AND field_key=?""",
            (subject_id, mutation.field_key),
        ).fetchone()
        if row is None:
            raise RepresentedConsequenceStateError(
                f"Consequence field {mutation.field_key!r} must already exist"
            )
        if row["mode"] != "simulated":
            raise RepresentedConsequenceStateError(
                f"Consequence field {mutation.field_key!r} must be simulated, not {row['mode']!r}"
            )
        rows[mutation.field_key] = row
    return rows


def _numeric(value: Any, *, path: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RepresentedConsequenceStateError(f"{path} requires a numeric value")
    return float(value)


def _apply_operation(current: Any, mutation: StateMutation) -> Any:
    if mutation.operation == "set":
        return mutation.value

    current_number = _numeric(current, path=f"Current field {mutation.field_key!r}")
    operand = _numeric(mutation.value, path=f"Operation {mutation.operation!r}")
    if mutation.operation == "add":
        result = current_number + operand
    elif mutation.operation == "multiply":
        result = current_number * operand
    elif mutation.operation == "clamp_min":
        result = max(current_number, operand)
    elif mutation.operation == "clamp_max":
        result = min(current_number, operand)
    else:  # validated before this point
        raise RepresentedConsequenceStateError(
            f"Unsupported consequence operation {mutation.operation!r}"
        )
    if isinstance(current, int) and not isinstance(current, bool) and result.is_integer():
        return int(result)
    return result


def apply_represented_consequence(
    conn: sqlite3.Connection,
    *,
    action_id: str,
    authorization: ConsequenceAuthorization,
) -> dict[str, Any]:
    """Apply one explicitly authorized represented-task state consequence.

    V1 is intentionally narrow: the source action must already be completed and
    enriched with the exact represented task id; the subject must be the action's
    actor, target, or represented participant as declared; every field must
    already exist in simulated mode. This function does not derive authorization
    from Skill score, performance quality, model prose, or generic capabilities.

    The operation is idempotent per action/consequence/task/subject tuple and uses
    a savepoint so validation or event failures cannot leave partial field writes.
    """

    _validate_authorization(authorization)
    prior = _prior_application(conn, action_id, authorization)
    if prior is not None:
        return prior

    savepoint = "represented_consequence_state_v1"
    conn.execute(f"SAVEPOINT {savepoint}")
    try:
        action = _action_context(conn, action_id)
        actual_task_id = _represented_task_id(action)
        if actual_task_id != authorization.represented_task_id:
            raise RepresentedConsequenceStateError(
                "Consequence authorization task does not match the source action represented task"
            )
        _validate_subject_relation(conn, action, authorization)
        completion_event = _completion_event(conn, action_id)
        rows = _field_rows(conn, authorization.subject_id, authorization.mutations)

        field_changes: dict[str, Any] = {}
        for mutation in authorization.mutations:
            row = rows[mutation.field_key]
            try:
                before = json.loads(row["value_json"])
            except (TypeError, json.JSONDecodeError) as exc:
                raise RepresentedConsequenceStateError(
                    f"Consequence field {mutation.field_key!r} contains invalid JSON"
                ) from exc
            after = _apply_operation(before, mutation)
            # Validate JSON serializability before writing anything irreversible.
            encoded = json.dumps(after, ensure_ascii=False, allow_nan=False)
            conn.execute(
                """UPDATE fields SET value_json=?,updated_at=CURRENT_TIMESTAMP
                WHERE entity_id=? AND field_key=? AND mode='simulated'""",
                (encoded, authorization.subject_id, mutation.field_key),
            )
            field_changes[mutation.field_key] = {
                "before": before,
                "after": after,
                "operation": mutation.operation,
                "operand": mutation.value,
            }

        state_changes = {
            "subject_id": authorization.subject_id,
            "subject_role": authorization.subject_role,
            "consequence_id": authorization.consequence_id,
            "fields": field_changes,
        }
        payload = {
            "source": SOURCE,
            "consequence_id": authorization.consequence_id,
            "represented_task_id": authorization.represented_task_id,
            "subject_id": authorization.subject_id,
            "subject_role": authorization.subject_role,
            "authorization": "deterministic_consequence_contract",
            "learning_evidence": False,
        }
        participants = []
        if authorization.subject_id != action["actor_id"]:
            participants.append(
                {"entity_id": authorization.subject_id, "role": "consequence_subject"}
            )
        event_id = record_event(
            conn,
            sim_time=str(completion_event["sim_time"]),
            event_type=EVENT_TYPE,
            actor_id=str(action["actor_id"]),
            action_id=action_id,
            location_id=action["place_id"],
            participants=participants,
            caused_by_event_id=int(completion_event["id"]),
            state_changes=state_changes,
            payload=payload,
        )
        conn.execute(f"RELEASE {savepoint}")
        return {
            "event_id": event_id,
            "already_applied": False,
            "state_changes": state_changes,
            "payload": payload,
        }
    except Exception:
        conn.execute(f"ROLLBACK TO {savepoint}")
        conn.execute(f"RELEASE {savepoint}")
        raise

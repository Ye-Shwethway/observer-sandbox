from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable

from .world_stimulus import add_stimulus_scope, create_world_stimulus, set_stimulus_status, world_stimulus


COMMITMENT_TYPES = {"appointment", "promise", "deadline", "scheduled_responsibility"}
COMMITMENT_STATUSES = {"pending", "active", "completed", "cancelled", "missed"}
TERMINAL_STATUSES = {"completed", "cancelled", "missed"}
FLEXIBILITY_TYPES = {"fixed", "flexible", "reschedulable"}


def _json(value: dict[str, Any] | None) -> str:
    return json.dumps(value or {}, sort_keys=True, separators=(",", ":"))


def _require_member(value: str, allowed: set[str], *, name: str) -> str:
    normalized = str(value)
    if normalized not in allowed:
        raise ValueError(f"unsupported {name}: {normalized}")
    return normalized


def _require_character(conn: sqlite3.Connection, character_id: str) -> None:
    row = conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='character'", (character_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown character: {character_id}")


def _require_entity(conn: sqlite3.Connection, entity_id: str | None, *, name: str) -> None:
    if entity_id is None:
        return
    if conn.execute("SELECT 1 FROM entities WHERE id=?", (entity_id,)).fetchone() is None:
        raise ValueError(f"unknown {name}: {entity_id}")


def create_commitment(
    conn: sqlite3.Connection,
    *,
    commitment_id: str,
    character_id: str,
    commitment_type: str,
    title: str,
    start_sim_time: str | None = None,
    due_sim_time: str | None = None,
    details: str | None = None,
    target_entity_id: str | None = None,
    target_location_id: str | None = None,
    flexibility: str = "fixed",
    source_type: str | None = None,
    source_id: str | None = None,
    source_event_id: int | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create one factual future expectation without creating a Mind artifact or action plan."""
    if not str(commitment_id).strip():
        raise ValueError("commitment_id is required")
    if not str(title).strip():
        raise ValueError("title is required")
    if start_sim_time is None and due_sim_time is None:
        raise ValueError("commitment requires start_sim_time or due_sim_time")
    _require_character(conn, character_id)
    commitment_type = _require_member(commitment_type, COMMITMENT_TYPES, name="commitment_type")
    flexibility = _require_member(flexibility, FLEXIBILITY_TYPES, name="flexibility")
    _require_entity(conn, target_entity_id, name="target_entity")
    _require_entity(conn, target_location_id, name="target_location")

    conn.execute(
        """
        INSERT INTO commitments(
            commitment_id,character_id,commitment_type,title,details,start_sim_time,due_sim_time,
            target_entity_id,target_location_id,status,flexibility,source_type,source_id,
            source_event_id,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,'pending',?,?,?,?,?)
        """,
        (
            commitment_id,
            character_id,
            commitment_type,
            title,
            details,
            start_sim_time,
            due_sim_time,
            target_entity_id,
            target_location_id,
            flexibility,
            source_type,
            source_id,
            source_event_id,
            _json(metadata),
        ),
    )
    conn.commit()
    return commitment(conn, commitment_id)


def commitment(conn: sqlite3.Connection, commitment_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM commitments WHERE commitment_id=?", (commitment_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown commitment: {commitment_id}")
    result = dict(row)
    result["metadata"] = json.loads(result.pop("metadata_json"))
    return result


def character_commitments(
    conn: sqlite3.Connection,
    character_id: str,
    *,
    statuses: Iterable[str] | None = None,
    limit: int = 50,
) -> list[dict[str, Any]]:
    _require_character(conn, character_id)
    requested = None
    if statuses is not None:
        requested = {_require_member(value, COMMITMENT_STATUSES, name="status") for value in statuses}
    rows = conn.execute(
        """SELECT commitment_id,status FROM commitments
           WHERE character_id=?
           ORDER BY COALESCE(due_sim_time,start_sim_time),commitment_id
           LIMIT ?""",
        (character_id, max(1, int(limit) * 5)),
    ).fetchall()
    results: list[dict[str, Any]] = []
    for row in rows:
        if requested is not None and row["status"] not in requested:
            continue
        results.append(commitment(conn, str(row["commitment_id"])))
        if len(results) >= max(1, int(limit)):
            break
    return results


def set_commitment_status(conn: sqlite3.Connection, commitment_id: str, status: str) -> dict[str, Any]:
    status = _require_member(status, COMMITMENT_STATUSES, name="status")
    if conn.execute("SELECT 1 FROM commitments WHERE commitment_id=?", (commitment_id,)).fetchone() is None:
        raise ValueError(f"unknown commitment: {commitment_id}")
    conn.execute(
        "UPDATE commitments SET status=?,updated_at=CURRENT_TIMESTAMP WHERE commitment_id=?",
        (status, commitment_id),
    )
    conn.commit()
    if status in TERMINAL_STATUSES:
        rows = conn.execute(
            """SELECT stimulus_id FROM world_stimuli
               WHERE source_type='commitment' AND source_id=? AND status='active'""",
            (commitment_id,),
        ).fetchall()
        for row in rows:
            set_stimulus_status(conn, str(row["stimulus_id"]), "retired")
    return commitment(conn, commitment_id)


def publish_commitment_notice(
    conn: sqlite3.Connection,
    *,
    commitment_id: str,
    stimulus_id: str,
    notice_sim_time: str,
    subject: str | None = None,
    salience: float = 0.5,
    end_sim_time: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Publish W2 truth into W0 availability only; do not record exposure or cognition."""
    item = commitment(conn, commitment_id)
    if item["status"] in TERMINAL_STATUSES:
        raise ValueError(f"cannot publish notice for terminal commitment: {commitment_id}")
    stimulus = create_world_stimulus(
        conn,
        stimulus_id=stimulus_id,
        stimulus_type="obligation",
        channel="other",
        subject=subject or item["title"],
        start_sim_time=notice_sim_time,
        end_sim_time=end_sim_time,
        salience=salience,
        source_type="commitment",
        source_id=commitment_id,
        payload={
            "commitment_type": item["commitment_type"],
            "title": item["title"],
            "start_sim_time": item["start_sim_time"],
            "due_sim_time": item["due_sim_time"],
            "target_entity_id": item["target_entity_id"],
            "target_location_id": item["target_location_id"],
            "flexibility": item["flexibility"],
        },
        metadata=metadata,
    )
    add_stimulus_scope(
        conn,
        stimulus_id=stimulus_id,
        scope_type="character",
        scope_id=str(item["character_id"]),
        relation_role="targeted_to",
    )
    return world_stimulus(conn, str(stimulus["stimulus_id"]))

from __future__ import annotations

import json
import sqlite3
from typing import Any, Iterable


STIMULUS_TYPES = {
    "environment",
    "information",
    "communication",
    "financial",
    "obligation",
    "social",
    "system",
    "other",
}
CHANNELS = {
    "visual",
    "auditory",
    "tactile",
    "environmental",
    "device",
    "media",
    "direct",
    "mixed",
    "other",
}
SCOPE_TYPES = {"world", "location", "entity", "character", "audience"}
STIMULUS_STATUSES = {"active", "expired", "retired"}
EXPOSURE_STATUSES = {"exposed", "invalidated"}


def _json(value: dict[str, Any] | None) -> str:
    return json.dumps(value or {}, sort_keys=True, separators=(",", ":"))


def _clamp_unit(value: float, *, name: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return number


def _require_member(value: str, allowed: set[str], *, name: str) -> str:
    normalized = str(value)
    if normalized not in allowed:
        raise ValueError(f"unsupported {name}: {normalized}")
    return normalized


def create_world_stimulus(
    conn: sqlite3.Connection,
    *,
    stimulus_id: str,
    stimulus_type: str,
    channel: str,
    subject: str,
    start_sim_time: str,
    payload: dict[str, Any] | None = None,
    source_type: str | None = None,
    source_id: str | None = None,
    source_event_id: int | None = None,
    source_entity_id: str | None = None,
    salience: float = 0.5,
    end_sim_time: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create one authoritative externally available signal without exposing it to anyone."""
    stimulus_type = _require_member(stimulus_type, STIMULUS_TYPES, name="stimulus_type")
    channel = _require_member(channel, CHANNELS, name="channel")
    if not str(stimulus_id).strip():
        raise ValueError("stimulus_id is required")
    if not str(subject).strip():
        raise ValueError("subject is required")
    salience = _clamp_unit(salience, name="salience")

    conn.execute(
        """
        INSERT INTO world_stimuli(
            stimulus_id,stimulus_type,channel,subject,payload_json,source_type,source_id,
            source_event_id,source_entity_id,salience,start_sim_time,end_sim_time,status,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?, 'active', ?)
        """,
        (
            stimulus_id,
            stimulus_type,
            channel,
            subject,
            _json(payload),
            source_type,
            source_id,
            source_event_id,
            source_entity_id,
            salience,
            start_sim_time,
            end_sim_time,
            _json(metadata),
        ),
    )
    conn.commit()
    return world_stimulus(conn, stimulus_id)


def add_stimulus_scope(
    conn: sqlite3.Connection,
    *,
    stimulus_id: str,
    scope_type: str,
    scope_id: str,
    relation_role: str = "available_to",
    metadata: dict[str, Any] | None = None,
) -> None:
    scope_type = _require_member(scope_type, SCOPE_TYPES, name="scope_type")
    if not str(scope_id).strip():
        raise ValueError("scope_id is required")
    if conn.execute("SELECT 1 FROM world_stimuli WHERE stimulus_id=?", (stimulus_id,)).fetchone() is None:
        raise ValueError(f"unknown stimulus: {stimulus_id}")
    conn.execute(
        """INSERT OR IGNORE INTO world_stimulus_scopes(
               stimulus_id,scope_type,scope_id,relation_role,metadata_json
           ) VALUES(?,?,?,?,?)""",
        (stimulus_id, scope_type, scope_id, relation_role, _json(metadata)),
    )
    conn.commit()


def set_stimulus_status(conn: sqlite3.Connection, stimulus_id: str, status: str) -> None:
    status = _require_member(status, STIMULUS_STATUSES, name="status")
    cur = conn.execute(
        "UPDATE world_stimuli SET status=?,updated_at=CURRENT_TIMESTAMP WHERE stimulus_id=?",
        (status, stimulus_id),
    )
    if cur.rowcount != 1:
        raise ValueError(f"unknown stimulus: {stimulus_id}")
    conn.commit()


def world_stimulus(conn: sqlite3.Connection, stimulus_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM world_stimuli WHERE stimulus_id=?", (stimulus_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown stimulus: {stimulus_id}")
    result = dict(row)
    result["payload"] = json.loads(result.pop("payload_json"))
    result["metadata"] = json.loads(result.pop("metadata_json"))
    scopes = conn.execute(
        """SELECT scope_type,scope_id,relation_role,metadata_json
           FROM world_stimulus_scopes WHERE stimulus_id=?
           ORDER BY scope_type,scope_id,relation_role""",
        (stimulus_id,),
    ).fetchall()
    result["scopes"] = [
        {
            "scope_type": row["scope_type"],
            "scope_id": row["scope_id"],
            "relation_role": row["relation_role"],
            "metadata": json.loads(row["metadata_json"]),
        }
        for row in scopes
    ]
    return result


def eligible_world_stimuli(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    sim_time: str,
    location_id: str | None = None,
    entity_ids: Iterable[str] = (),
    audience_ids: Iterable[str] = (),
    channels: Iterable[str] | None = None,
    limit: int = 20,
) -> list[dict[str, Any]]:
    """Return bounded active stimuli whose explicit scope matches the represented actor context.

    Eligibility does not record exposure and does not imply perception.
    """
    if conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='character'", (character_id,)
    ).fetchone() is None:
        raise ValueError(f"unknown character: {character_id}")

    allowed_channels = None
    if channels is not None:
        allowed_channels = {_require_member(value, CHANNELS, name="channel") for value in channels}

    scope_pairs: set[tuple[str, str]] = {("world", "world"), ("character", character_id)}
    if location_id:
        scope_pairs.add(("location", location_id))
    scope_pairs.update(("entity", str(value)) for value in entity_ids)
    scope_pairs.update(("audience", str(value)) for value in audience_ids)

    rows = conn.execute(
        """
        SELECT * FROM world_stimuli
        WHERE status='active'
          AND start_sim_time<=?
          AND (end_sim_time IS NULL OR end_sim_time>=?)
        ORDER BY salience DESC,start_sim_time DESC,stimulus_id
        LIMIT ?
        """,
        (sim_time, sim_time, max(1, min(int(limit) * 5, 500))),
    ).fetchall()

    results: list[dict[str, Any]] = []
    for row in rows:
        if allowed_channels is not None and row["channel"] not in allowed_channels:
            continue
        scopes = conn.execute(
            "SELECT scope_type,scope_id FROM world_stimulus_scopes WHERE stimulus_id=?",
            (row["stimulus_id"],),
        ).fetchall()
        if not scopes:
            continue
        if not any((scope["scope_type"], scope["scope_id"]) in scope_pairs for scope in scopes):
            continue
        results.append(world_stimulus(conn, str(row["stimulus_id"])))
        if len(results) >= max(1, int(limit)):
            break
    return results


def record_character_exposure(
    conn: sqlite3.Connection,
    *,
    exposure_id: str,
    stimulus_id: str,
    character_id: str,
    sim_time: str,
    channel: str | None = None,
    source_location_id: str | None = None,
    source_entity_id: str | None = None,
    attention_hint: float | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Record that a represented stimulus reached the actor boundary; do not interpret it."""
    stimulus = world_stimulus(conn, stimulus_id)
    if conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='character'", (character_id,)
    ).fetchone() is None:
        raise ValueError(f"unknown character: {character_id}")
    actual_channel = _require_member(channel or str(stimulus["channel"]), CHANNELS, name="channel")
    if attention_hint is not None:
        attention_hint = _clamp_unit(attention_hint, name="attention_hint")

    conn.execute(
        """
        INSERT INTO character_exposures(
            exposure_id,stimulus_id,character_id,sim_time,channel,source_location_id,
            source_entity_id,attention_hint,status,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?, 'exposed', ?)
        """,
        (
            exposure_id,
            stimulus_id,
            character_id,
            sim_time,
            actual_channel,
            source_location_id,
            source_entity_id,
            attention_hint,
            _json(metadata),
        ),
    )
    conn.commit()
    return character_exposure(conn, exposure_id)


def invalidate_exposure(conn: sqlite3.Connection, exposure_id: str) -> None:
    cur = conn.execute(
        "UPDATE character_exposures SET status='invalidated' WHERE exposure_id=?", (exposure_id,)
    )
    if cur.rowcount != 1:
        raise ValueError(f"unknown exposure: {exposure_id}")
    conn.commit()


def character_exposure(conn: sqlite3.Connection, exposure_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM character_exposures WHERE exposure_id=?", (exposure_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown exposure: {exposure_id}")
    result = dict(row)
    result["metadata"] = json.loads(result.pop("metadata_json"))
    return result


def recent_character_exposures(
    conn: sqlite3.Connection,
    character_id: str,
    *,
    limit: int = 20,
    include_invalidated: bool = False,
) -> list[dict[str, Any]]:
    where = "character_id=?" if include_invalidated else "character_id=? AND status='exposed'"
    rows = conn.execute(
        f"SELECT exposure_id FROM character_exposures WHERE {where} ORDER BY sim_time DESC,created_at DESC LIMIT ?",
        (character_id, max(1, int(limit))),
    ).fetchall()
    return [character_exposure(conn, str(row["exposure_id"])) for row in rows]

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any

from .event_log import record_event
from .skill_practice import skill_practice_evidence_from_event
from .training_methods import training_method_evidence_from_event


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_PROGRESSION_CONFIG_PATH = REPO_ROOT / "config" / "skill_progression.v1.json"
SETTLEMENT_EVENT_TYPE = "skill_progression_settled"
SETTLEMENT_SOURCE = "skill-progression-foundation-v1"


@lru_cache(maxsize=1)
def load_skill_progression_config(path: str | Path = SKILL_PROGRESSION_CONFIG_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _skill_definition(skill_key: str, *, config: dict[str, Any] | None = None) -> dict[str, Any] | None:
    source = config if config is not None else load_skill_progression_config()
    raw = source.get("skills", {}).get(skill_key)
    if not isinstance(raw, dict):
        return None
    result = dict(raw)
    result["skill_key"] = skill_key
    result["revision"] = str(source.get("revision") or SETTLEMENT_SOURCE)
    return result


def _skill_row(conn: sqlite3.Connection, actor_id: str, skill_key: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT id,score,tier,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (actor_id, skill_key),
    ).fetchone()


def _settlement_rows(conn: sqlite3.Connection, actor_id: str, skill_key: str) -> list[sqlite3.Row]:
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
        (actor_id, SETTLEMENT_EVENT_TYPE),
    ).fetchall()
    result: list[sqlite3.Row] = []
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("skill_key") == skill_key:
            result.append(row)
    return result


def _consumed_action_event_ids(conn: sqlite3.Connection, actor_id: str, skill_key: str) -> set[int]:
    consumed: set[int] = set()
    for row in _settlement_rows(conn, actor_id, skill_key):
        payload = json.loads(row["payload_json"] or "{}")
        for event_id in payload.get("consumed_action_event_ids") or []:
            if isinstance(event_id, int):
                consumed.add(event_id)
    return consumed


def _eligible_training_events(
    conn: sqlite3.Connection,
    actor_id: str,
    skill_key: str,
    *,
    as_of_sim_time: str,
    config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    definition = _skill_definition(skill_key, config=config)
    if definition is None:
        return []
    eligible_methods = definition.get("eligible_methods") or {}
    if not isinstance(eligible_methods, dict):
        return []
    as_of = _dt(as_of_sim_time)
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id",
        (actor_id,),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        if _dt(str(row["sim_time"])) > as_of:
            continue
        payload = json.loads(row["payload_json"] or "{}")
        method = training_method_evidence_from_event(payload)
        evidence_kind = "training_method"
        if not isinstance(method, dict):
            method = skill_practice_evidence_from_event(payload)
            evidence_kind = "skill_practice"
        if not isinstance(method, dict):
            continue
        method_id = str(method.get("method_id") or "")
        weight = eligible_methods.get(method_id)
        if not isinstance(weight, (int, float)) or float(weight) <= 0.0:
            continue
        if evidence_kind == "skill_practice":
            relevance = method.get("skill_relevance") or {}
            skill_relevance = relevance.get(skill_key) if isinstance(relevance, dict) else None
            if not isinstance(skill_relevance, (int, float)) or float(skill_relevance) <= 0.0:
                continue
        load = method.get("effective_load") or {}
        effective_minutes = load.get("effective_minutes")
        if not isinstance(effective_minutes, (int, float)) or float(effective_minutes) <= 0.0:
            continue
        result.append(
            {
                "event_id": int(row["id"]),
                "sim_time": str(row["sim_time"]),
                "evidence_kind": evidence_kind,
                "method_id": method_id,
                "method_name": method.get("method_name"),
                "method_weight": float(weight),
                "effective_minutes": float(effective_minutes),
                "raw_learning_units": (float(effective_minutes) / 60.0) * float(weight),
            }
        )
    return result


def proficiency_factor(score: float) -> float:
    """Bounded diminishing returns as demonstrated proficiency approaches 100."""
    return max(0.05, min(1.0, (100.0 - float(score)) / 40.0))


def saturation_factor(recent_learning_units: float, *, half_units: float) -> float:
    half_units = max(0.001, float(half_units))
    return max(0.1, min(1.0, 1.0 / (1.0 + max(0.0, float(recent_learning_units)) / half_units)))


def _recent_units_before(
    events: list[dict[str, Any]],
    event: dict[str, Any],
    *,
    window_hours: float,
) -> float:
    event_time = _dt(str(event["sim_time"]))
    window_start = event_time - timedelta(hours=max(0.0, float(window_hours)))
    total = 0.0
    for candidate in events:
        candidate_time = _dt(str(candidate["sim_time"]))
        if candidate_time >= event_time:
            continue
        if candidate_time < window_start:
            continue
        total += float(candidate.get("raw_learning_units") or 0.0)
    return total


def _mark_active(conn: sqlite3.Connection, actor_id: str, skill_key: str, *, sim_time: str, revision: str) -> None:
    row = _skill_row(conn, actor_id, skill_key)
    if row is None:
        return
    metadata = json.loads(row["metadata_json"] or "{}")
    if not isinstance(metadata, dict):
        metadata = {}
    metadata["progression_active"] = True
    metadata["progression_revision"] = revision
    metadata.setdefault("progression_activated_at", sim_time)
    conn.execute(
        "UPDATE character_skills SET metadata_json=? WHERE entity_id=? AND skill_key=?",
        (json.dumps(metadata, ensure_ascii=False, sort_keys=True), actor_id, skill_key),
    )


def _project_compatibility_field(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    field_key: str | None,
    old_score: float,
    new_score: float,
    sim_time: str,
) -> None:
    if not field_key:
        return
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    if row is None:
        return
    old_projection = float(json.loads(row["value_json"]))
    new_projection = round(float(new_score), 6)
    if abs(old_projection - new_projection) < 1e-12:
        return
    value_json = json.dumps(new_projection)
    conn.execute(
        """
        UPDATE character_profile_values
        SET value_json=?,mode='simulated',authority=?,source=?,observed_at=?,updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND field_key=?
        """,
        (value_json, SETTLEMENT_SOURCE, SETTLEMENT_SOURCE, sim_time, actor_id, field_key),
    )
    conn.execute(
        """
        INSERT INTO character_profile_history(
            entity_id,field_key,old_value_json,new_value_json,mode,authority,reason,sim_time
        ) VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            actor_id,
            field_key,
            json.dumps(round(old_projection, 6)),
            value_json,
            "simulated",
            SETTLEMENT_SOURCE,
            "compatibility projection from authoritative character skill score",
            sim_time,
        ),
    )


def settle_skill_progression(
    conn: sqlite3.Connection,
    actor_id: str,
    skill_key: str,
    *,
    as_of_sim_time: str,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    definition = _skill_definition(skill_key, config=config)
    row = _skill_row(conn, actor_id, skill_key)
    if definition is None or row is None or row["score"] is None:
        return {"settled": False, "reason": "skill_not_represented", "skill_key": skill_key}

    score = float(row["score"])
    experience = float(row["experience"] or 0.0)
    events = _eligible_training_events(conn, actor_id, skill_key, as_of_sim_time=as_of_sim_time, config=config)
    settlements = _settlement_rows(conn, actor_id, skill_key)
    revision = str(definition["revision"])

    if not settlements:
        consumed = [int(event["event_id"]) for event in events]
        _mark_active(conn, actor_id, skill_key, sim_time=as_of_sim_time, revision=revision)
        settlement_event_id = record_event(
            conn,
            sim_time=as_of_sim_time,
            actor_id=actor_id,
            event_type=SETTLEMENT_EVENT_TYPE,
            payload={
                "source": revision,
                "skill_key": skill_key,
                "bootstrap": True,
                "consumed_action_event_ids": consumed,
                "old_score": round(score, 6),
                "new_score": round(score, 6),
                "score_delta": 0.0,
                "old_experience": round(experience, 6),
                "new_experience": round(experience, 6),
                "experience_gain": 0.0,
            },
        )
        conn.commit()
        return {
            "settled": True,
            "bootstrap": True,
            "skill_key": skill_key,
            "event_id": settlement_event_id,
            "consumed_action_event_ids": consumed,
            "old_score": score,
            "new_score": score,
            "score_delta": 0.0,
            "experience_gain": 0.0,
        }

    consumed = _consumed_action_event_ids(conn, actor_id, skill_key)
    pending = [event for event in events if int(event["event_id"]) not in consumed]
    if not pending:
        return {"settled": False, "reason": "no_new_learning_evidence", "skill_key": skill_key}

    current_score = score
    experience_gain = 0.0
    score_gain = 0.0
    evidence_rows: list[dict[str, Any]] = []
    window_hours = float(definition.get("recent_window_hours", 24.0))
    half_units = float(definition.get("saturation_half_units", 2.0))
    base_rate = float(definition.get("base_score_points_per_learning_unit", 0.12))
    score_cap = float(definition.get("score_cap", 100.0))

    for event in pending:
        recent_units = _recent_units_before(events, event, window_hours=window_hours)
        saturation = saturation_factor(recent_units, half_units=half_units)
        effective_units = max(0.0, float(event["raw_learning_units"])) * saturation
        level_factor = proficiency_factor(current_score)
        delta = min(max(0.0, score_cap - current_score), effective_units * base_rate * level_factor)
        current_score += delta
        experience_gain += effective_units
        score_gain += delta
        evidence_rows.append(
            {
                "action_event_id": int(event["event_id"]),
                "evidence_kind": event.get("evidence_kind", "training_method"),
                "method_id": event["method_id"],
                "method_weight": round(float(event["method_weight"]), 6),
                "effective_minutes": round(float(event["effective_minutes"]), 6),
                "recent_learning_units": round(recent_units, 6),
                "saturation_factor": round(saturation, 6),
                "effective_learning_units": round(effective_units, 6),
                "proficiency_factor": round(level_factor, 6),
                "score_delta": round(delta, 6),
            }
        )

    new_score = round(min(score_cap, current_score), 6)
    new_experience = round(experience + experience_gain, 6)
    metadata = json.loads(row["metadata_json"] or "{}")
    if not isinstance(metadata, dict):
        metadata = {}
    metadata["progression_active"] = True
    metadata["progression_revision"] = revision
    metadata.setdefault("progression_activated_at", as_of_sim_time)
    metadata["last_progression_sim_time"] = as_of_sim_time

    conn.execute(
        """
        UPDATE character_skills
        SET score=?,experience=?,metadata_json=?
        WHERE entity_id=? AND skill_key=?
        """,
        (
            new_score,
            new_experience,
            json.dumps(metadata, ensure_ascii=False, sort_keys=True),
            actor_id,
            skill_key,
        ),
    )
    _project_compatibility_field(
        conn,
        actor_id,
        field_key=definition.get("compatibility_profile_field"),
        old_score=score,
        new_score=new_score,
        sim_time=as_of_sim_time,
    )
    settlement_event_id = record_event(
        conn,
        sim_time=as_of_sim_time,
        actor_id=actor_id,
        event_type=SETTLEMENT_EVENT_TYPE,
        payload={
            "source": revision,
            "skill_key": skill_key,
            "bootstrap": False,
            "consumed_action_event_ids": [int(event["event_id"]) for event in pending],
            "old_score": round(score, 6),
            "new_score": new_score,
            "score_delta": round(score_gain, 6),
            "old_experience": round(experience, 6),
            "new_experience": new_experience,
            "experience_gain": round(experience_gain, 6),
            "evidence": evidence_rows,
        },
    )
    conn.commit()
    return {
        "settled": True,
        "bootstrap": False,
        "skill_key": skill_key,
        "event_id": settlement_event_id,
        "consumed_action_event_ids": [int(event["event_id"]) for event in pending],
        "old_score": score,
        "new_score": new_score,
        "score_delta": round(score_gain, 6),
        "old_experience": experience,
        "new_experience": new_experience,
        "experience_gain": round(experience_gain, 6),
        "evidence": evidence_rows,
    }


def maybe_settle_skill_progression(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
) -> list[dict[str, Any]]:
    config = load_skill_progression_config()
    skills = config.get("skills") or {}
    if not isinstance(skills, dict):
        return []
    results: list[dict[str, Any]] = []
    for skill_key in sorted(skills):
        if _skill_row(conn, actor_id, skill_key) is None:
            continue
        results.append(
            settle_skill_progression(
                conn,
                actor_id,
                skill_key,
                as_of_sim_time=as_of_sim_time,
                config=config,
            )
        )
    return results

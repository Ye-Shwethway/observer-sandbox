from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any


SOURCE = "preference_adaptation_v1"
LEDGER_PREFIX = "preference_adaptation_v1:"
POSITIVE_ENGAGEMENT_ACTIONS = {"read", "use"}
BASE_EVIDENCE_DELTA = 5.0
ESTABLISH_SCORE = 35.0
ESTABLISH_EFFECTIVE_EVIDENCE = 7.0
ESTABLISH_DISTINCT_DAYS = 4
NEUTRALIZE_SCORE = 12.0


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _temporal_weight(last_sim_time: str | None, ended_sim_time: str) -> float:
    if not last_sim_time:
        return 1.0
    elapsed_hours = max(
        0.0,
        (_parse_time(ended_sim_time) - _parse_time(last_sim_time)).total_seconds() / 3600.0,
    )
    if elapsed_hours < 6.0:
        return 0.25
    if elapsed_hours < 18.0:
        return 0.60
    return 1.0


def _entity_name(conn: sqlite3.Connection, entity_id: str) -> str:
    row = conn.execute("SELECT name FROM entities WHERE id=?", (entity_id,)).fetchone()
    return str(row[0]) if row is not None and row[0] else entity_id


def _ledger_key(actor_id: str, target_id: str) -> str:
    return f"{LEDGER_PREFIX}{actor_id}:{target_id}"


def _read_ledger(conn: sqlite3.Connection, actor_id: str, target_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT value_json FROM runtime_state WHERE key=?",
        (_ledger_key(actor_id, target_id),),
    ).fetchone()
    if row is None:
        return None
    value = json.loads(row[0])
    return value if isinstance(value, dict) else None


def _write_ledger(conn: sqlite3.Connection, actor_id: str, target_id: str, value: dict[str, Any]) -> None:
    conn.execute(
        """
        INSERT INTO runtime_state(key,value_json,updated_at)
        VALUES(?,?,CURRENT_TIMESTAMP)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=CURRENT_TIMESTAMP
        """,
        (_ledger_key(actor_id, target_id), json.dumps(value, ensure_ascii=False, sort_keys=True)),
    )


def _dynamic_projection(conn: sqlite3.Connection, actor_id: str, target_id: str) -> sqlite3.Row | None:
    rows = conn.execute(
        """
        SELECT id,preference_type,subject,intensity,metadata_json
        FROM character_preferences
        WHERE entity_id=? AND preference_type IN ('like','dislike')
        ORDER BY id
        """,
        (actor_id,),
    ).fetchall()
    for row in rows:
        metadata = json.loads(row["metadata_json"] or "{}")
        if isinstance(metadata, dict) and metadata.get("source") == SOURCE and metadata.get("target_id") == target_id:
            return row
    return None


def _sync_projection(
    conn: sqlite3.Connection,
    actor_id: str,
    target_id: str,
    *,
    score: float,
    effective_evidence: float,
    distinct_days: int,
) -> dict[str, Any]:
    projection = _dynamic_projection(conn, actor_id, target_id)
    established = (
        abs(score) >= ESTABLISH_SCORE
        and effective_evidence >= ESTABLISH_EFFECTIVE_EVIDENCE
        and distinct_days >= ESTABLISH_DISTINCT_DAYS
    )
    if projection is not None and abs(score) < NEUTRALIZE_SCORE:
        conn.execute("DELETE FROM character_preferences WHERE id=?", (projection["id"],))
        projection = None

    if not established:
        if projection is not None:
            conn.execute(
                "UPDATE character_preferences SET intensity=? WHERE id=?",
                (round(abs(score), 3), projection["id"]),
            )
        return {
            "status": "neutral" if abs(score) < NEUTRALIZE_SCORE else "emerging",
            "preference_type": str(projection["preference_type"]) if projection is not None else None,
        }

    preference_type = "like" if score > 0 else "dislike"
    subject = _entity_name(conn, target_id)
    metadata = {
        "source": SOURCE,
        "target_id": target_id,
        "authority": "deterministic_preference_adaptation",
    }
    if projection is None:
        conn.execute(
            """
            INSERT INTO character_preferences(entity_id,preference_type,subject,intensity,metadata_json)
            VALUES(?,?,?,?,?)
            """,
            (
                actor_id,
                preference_type,
                subject,
                round(abs(score), 3),
                json.dumps(metadata, ensure_ascii=False, sort_keys=True),
            ),
        )
    elif projection["preference_type"] == preference_type:
        conn.execute(
            "UPDATE character_preferences SET intensity=?,metadata_json=? WHERE id=?",
            (
                round(abs(score), 3),
                json.dumps(metadata, ensure_ascii=False, sort_keys=True),
                projection["id"],
            ),
        )
    else:
        conn.execute("DELETE FROM character_preferences WHERE id=?", (projection["id"],))
        conn.execute(
            """
            INSERT INTO character_preferences(entity_id,preference_type,subject,intensity,metadata_json)
            VALUES(?,?,?,?,?)
            """,
            (
                actor_id,
                preference_type,
                subject,
                round(abs(score), 3),
                json.dumps(metadata, ensure_ascii=False, sort_keys=True),
            ),
        )
    return {"status": "established", "preference_type": preference_type}


def settle_preference_evidence(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    target_id: str,
    valence: int,
    ended_sim_time: str,
    evidence_kind: str,
) -> dict[str, Any]:
    """Apply one explicit signed preference-evidence item.

    Positive evidence may come from repeated voluntary target engagement. Negative
    evidence must be supplied by a represented aversive/outcome contract; absence
    of choice is never negative evidence. The LLM has no direct mutation path.
    """
    if valence not in (-1, 1):
        raise ValueError("valence must be -1 or 1")
    if not target_id:
        raise ValueError("target_id is required")
    if not evidence_kind.strip():
        raise ValueError("evidence_kind is required")

    ledger = _read_ledger(conn, actor_id, target_id) or {
        "source": SOURCE,
        "target_id": target_id,
        "target_name": _entity_name(conn, target_id),
        "signed_score": 0.0,
        "evidence_count": 0,
        "effective_evidence": 0.0,
        "distinct_evidence_days": 0,
        "last_evidence_day": None,
        "last_evidence_sim_time": None,
        "positive_evidence": 0,
        "negative_evidence": 0,
    }
    weight = _temporal_weight(ledger.get("last_evidence_sim_time"), ended_sim_time)
    before = float(ledger.get("signed_score", 0.0))
    after = max(-100.0, min(100.0, round(before + valence * BASE_EVIDENCE_DELTA * weight, 3)))
    day = _parse_time(ended_sim_time).date().isoformat()
    distinct_days = int(ledger.get("distinct_evidence_days", 0))
    if ledger.get("last_evidence_day") != day:
        distinct_days += 1

    ledger.update(
        {
            "signed_score": after,
            "evidence_count": int(ledger.get("evidence_count", 0)) + 1,
            "effective_evidence": round(float(ledger.get("effective_evidence", 0.0)) + weight, 3),
            "distinct_evidence_days": distinct_days,
            "last_evidence_day": day,
            "last_evidence_sim_time": ended_sim_time,
            "positive_evidence": int(ledger.get("positive_evidence", 0)) + (1 if valence > 0 else 0),
            "negative_evidence": int(ledger.get("negative_evidence", 0)) + (1 if valence < 0 else 0),
            "last_evidence_kind": evidence_kind,
        }
    )
    _write_ledger(conn, actor_id, target_id, ledger)
    projection = _sync_projection(
        conn,
        actor_id,
        target_id,
        score=after,
        effective_evidence=float(ledger["effective_evidence"]),
        distinct_days=distinct_days,
    )
    return {
        "source": SOURCE,
        "target_id": target_id,
        "target_name": ledger["target_name"],
        "score_before": before,
        "score_after": after,
        "temporal_weight": weight,
        "effective_evidence": ledger["effective_evidence"],
        "distinct_evidence_days": distinct_days,
        **projection,
    }


def settle_preference_adaptation(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    action_name: str,
    target_id: str | None,
    ended_sim_time: str,
) -> dict[str, Any] | None:
    """Extract conservative positive preference evidence from a completed action."""
    if action_name not in POSITIVE_ENGAGEMENT_ACTIONS or not target_id:
        return None
    return settle_preference_evidence(
        conn,
        actor_id,
        target_id=target_id,
        valence=1,
        ended_sim_time=ended_sim_time,
        evidence_kind=f"completed_voluntary_{action_name}",
    )


def preference_adaptation_state(conn: sqlite3.Connection, actor_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        "SELECT key,value_json FROM runtime_state WHERE key LIKE ? ORDER BY key",
        (f"{LEDGER_PREFIX}{actor_id}:%",),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        item = json.loads(row["value_json"])
        if isinstance(item, dict):
            result.append(item)
    return result

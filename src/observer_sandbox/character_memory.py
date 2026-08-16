from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime
from typing import Any

from .memory_dynamics import (
    ACCESSIBILITY_FLOOR,
    recall_accessibility,
    reinforce_recalled_memories,
    settle_memory_dynamics,
)


def _entity_name(conn: sqlite3.Connection, entity_id: str | None) -> str | None:
    if not entity_id:
        return None
    row = conn.execute("SELECT name FROM entities WHERE id=?", (entity_id,)).fetchone()
    return str(row[0]) if row is not None else entity_id


def _event_salience(payload: dict[str, Any], state_changes: dict[str, Any], target_id: str | None) -> float:
    score = 0.4
    if target_id:
        score += 0.05
    if state_changes:
        score += 0.1
    for key in ("skill_application", "training_method", "represented_skill_task", "nutrition_intake"):
        if isinstance(payload.get(key), dict):
            score += 0.08
    return max(0.0, min(score, 1.0))


def _memory_signals(payload: dict[str, Any]) -> tuple[float, float]:
    raw = payload.get("memory_signals") if isinstance(payload.get("memory_signals"), dict) else {}
    arousal = max(0.0, min(float(raw.get("emotional_arousal", 0.1)), 1.0))
    relevance = max(0.0, min(float(raw.get("personal_relevance", 0.5)), 1.0))
    return arousal, relevance


def _event_summary(conn: sqlite3.Connection, *, action_name: str, target_id: str | None, location_id: str | None) -> str:
    action = action_name.replace("_", " ").strip().title()
    target_name = _entity_name(conn, target_id)
    location_name = _entity_name(conn, location_id)
    if target_name and target_id != location_id:
        return f"{action} — {target_name}" + (f" at {location_name}" if location_name else "")
    if target_name:
        return f"{action} — {target_name}"
    if location_name:
        return f"{action} at {location_name}"
    return action


def encode_completed_action_memory(
    conn: sqlite3.Connection,
    *, event_id: int, actor_id: str, sim_time: str, location_id: str | None,
    state_changes: dict[str, Any] | None, payload: dict[str, Any],
) -> str | None:
    if not actor_id or payload.get("action") is None:
        return None
    existing = conn.execute(
        "SELECT memory_id FROM character_memories WHERE character_id=? AND source_event_id=?",
        (actor_id, event_id),
    ).fetchone()
    if existing is not None:
        return str(existing[0])
    action_name = str(payload["action"])
    target = payload.get("target")
    target_id = target if isinstance(target, str) else None
    changes = dict(state_changes or {})
    memory_id = f"mem_{uuid.uuid4().hex}"
    arousal, relevance = _memory_signals(payload)
    content = {
        "action": action_name,
        "target_id": target_id,
        "location_id": location_id,
        "duration_minutes": payload.get("duration_minutes"),
        "reason": payload.get("reason"),
        "state_changes": changes,
    }
    conn.execute(
        """INSERT INTO character_memories(
            memory_id,character_id,memory_type,summary,content_json,source_type,source_event_id,
            event_sim_time,encoded_sim_time,salience,confidence,status,lifecycle_stage,
            emotional_arousal,personal_relevance,last_dynamics_sim_time,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            memory_id, actor_id, "episodic",
            _event_summary(conn, action_name=action_name, target_id=target_id, location_id=location_id),
            json.dumps(content, ensure_ascii=False), "event", int(event_id), sim_time, sim_time,
            _event_salience(payload, changes, target_id), 1.0, "active", "recent",
            arousal, relevance, sim_time, json.dumps({}, ensure_ascii=False),
        ),
    )
    for entity_id, role in [(location_id, "location"), (target_id, "target")]:
        if not entity_id or (role == "target" and entity_id == location_id):
            continue
        if conn.execute("SELECT 1 FROM entities WHERE id=?", (entity_id,)).fetchone() is not None:
            conn.execute(
                "INSERT OR IGNORE INTO character_memory_entities(memory_id,entity_id,relation_role) VALUES(?,?,?)",
                (memory_id, entity_id, role),
            )
    return memory_id


def create_semantic_memory(
    conn: sqlite3.Connection, *, character_id: str, summary: str, content: dict[str, Any],
    sim_time: str, source_type: str = "seed", salience: float = 0.6, confidence: float = 1.0,
    related_entities: list[tuple[str, str]] | None = None, metadata: dict[str, Any] | None = None,
) -> str:
    memory_id = f"mem_{uuid.uuid4().hex}"
    conn.execute(
        """INSERT INTO character_memories(
            memory_id,character_id,memory_type,summary,content_json,source_type,source_event_id,
            event_sim_time,encoded_sim_time,salience,confidence,status,lifecycle_stage,
            memory_strength,detail_strength,emotional_arousal,personal_relevance,
            consolidated_sim_time,last_dynamics_sim_time,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            memory_id, character_id, "semantic", summary, json.dumps(content, ensure_ascii=False), source_type,
            None, sim_time, sim_time, max(0.0, min(float(salience), 1.0)),
            max(0.0, min(float(confidence), 1.0)), "active", "consolidated", 1.0, 1.0,
            0.1, 0.7, sim_time, sim_time, json.dumps(metadata or {}, ensure_ascii=False),
        ),
    )
    for entity_id, role in related_entities or []:
        if conn.execute("SELECT 1 FROM entities WHERE id=?", (entity_id,)).fetchone() is not None:
            conn.execute(
                "INSERT OR IGNORE INTO character_memory_entities(memory_id,entity_id,relation_role) VALUES(?,?,?)",
                (memory_id, entity_id, role),
            )
    return memory_id


def _recency_score(event_sim_time: str, current_sim_time: str) -> float:
    try:
        event_time = datetime.fromisoformat(event_sim_time.replace("Z", "+00:00"))
        current_time = datetime.fromisoformat(current_sim_time.replace("Z", "+00:00"))
        hours = max(0.0, (current_time - event_time).total_seconds() / 3600.0)
    except (TypeError, ValueError):
        return 0.0
    return 1.0 / (1.0 + hours / 24.0)


def retrieve_relevant_memories(
    conn: sqlite3.Connection, character_id: str, *, current_sim_time: str,
    current_location_id: str | None = None, available_actions: list[str] | None = None,
    limit: int = 8, record_recall: bool = True,
) -> list[dict[str, Any]]:
    """Return bounded memories that are both relevant and currently recallable."""
    settle_memory_dynamics(conn, character_id, current_sim_time)
    limit = max(1, min(int(limit), 20))
    rows = conn.execute(
        """SELECT memory_id,memory_type,summary,content_json,event_sim_time,salience,confidence,
                  lifecycle_stage,memory_strength,detail_strength,emotional_arousal,personal_relevance
           FROM character_memories
           WHERE character_id=? AND status='active'
           ORDER BY event_sim_time DESC, created_at DESC LIMIT 128""",
        (character_id,),
    ).fetchall()
    action_set = {str(action) for action in (available_actions or [])}
    ranked: list[tuple[float, dict[str, Any]]] = []
    for row in rows:
        content = json.loads(row["content_json"] or "{}")
        associations = conn.execute(
            "SELECT entity_id,relation_role FROM character_memory_entities WHERE memory_id=? ORDER BY relation_role,entity_id",
            (row["memory_id"],),
        ).fetchall()
        related = [{"entity_id": a["entity_id"], "role": a["relation_role"]} for a in associations]
        location_match = bool(current_location_id and any(a["entity_id"] == current_location_id for a in associations))
        action_match = bool(action_set and content.get("action") in action_set)
        episodic_recency = _recency_score(str(row["event_sim_time"]), current_sim_time) if row["memory_type"] == "episodic" else 0.0
        relevance = (
            0.45 * float(row["salience"])
            + 0.35 * episodic_recency
            + (0.15 if location_match else 0.0)
            + (0.05 if action_match else 0.0)
        )
        cue_strength = (0.75 if location_match else 0.0) + (0.25 if action_match else 0.0)
        accessibility = recall_accessibility(
            conn, character_id,
            memory_strength=float(row["memory_strength"]),
            relevance_score=min(relevance, 1.0), cue_strength=min(cue_strength, 1.0),
        )
        if accessibility < ACCESSIBILITY_FLOOR:
            continue
        score = 0.68 * relevance + 0.32 * accessibility
        ranked.append((score, {
            "memory_id": row["memory_id"], "type": row["memory_type"], "sim_time": row["event_sim_time"],
            "summary": row["summary"], "salience": round(float(row["salience"]), 3),
            "confidence": round(float(row["confidence"]), 3), "lifecycle_stage": row["lifecycle_stage"],
            "memory_strength": round(float(row["memory_strength"]), 3),
            "detail_strength": round(float(row["detail_strength"]), 3),
            "accessibility": round(accessibility, 3), "related_entities": related,
        }))
    selected = [item for _, item in sorted(ranked, key=lambda item: item[0], reverse=True)[:limit]]
    if record_recall and selected:
        reinforce_recalled_memories(conn, character_id, [item["memory_id"] for item in selected], current_sim_time)
    return selected


def memory_overview(conn: sqlite3.Connection, character_id: str, *, current_sim_time: str | None = None) -> dict[str, Any]:
    if current_sim_time:
        settle_memory_dynamics(conn, character_id, current_sim_time)
    row = conn.execute(
        """SELECT COUNT(*) AS total,
                  SUM(CASE WHEN memory_type='episodic' THEN 1 ELSE 0 END) AS episodic,
                  SUM(CASE WHEN memory_type='semantic' THEN 1 ELSE 0 END) AS semantic,
                  SUM(CASE WHEN lifecycle_stage='recent' THEN 1 ELSE 0 END) AS recent,
                  SUM(CASE WHEN lifecycle_stage IN ('consolidated','remote') THEN 1 ELSE 0 END) AS long_term,
                  SUM(CASE WHEN lifecycle_stage='faded' THEN 1 ELSE 0 END) AS faded,
                  MAX(encoded_sim_time) AS latest_encoded
           FROM character_memories WHERE character_id=? AND status='active'""",
        (character_id,),
    ).fetchone()
    return {key: int(row[key] or 0) for key in ("total", "episodic", "semantic", "recent", "long_term", "faded")} | {
        "latest_encoded": row["latest_encoded"]
    }


def list_memories(
    conn: sqlite3.Connection, character_id: str, *, memory_type: str | None = None,
    limit: int = 50, current_sim_time: str | None = None,
) -> list[dict[str, Any]]:
    if current_sim_time:
        settle_memory_dynamics(conn, character_id, current_sim_time)
    params: list[Any] = [character_id]
    type_clause = ""
    if memory_type in {"episodic", "semantic"}:
        type_clause = " AND memory_type=?"
        params.append(memory_type)
    params.append(max(1, min(int(limit), 200)))
    rows = conn.execute(
        f"""SELECT memory_id,memory_type,summary,event_sim_time,encoded_sim_time,salience,confidence,
                   last_recalled_sim_time,recall_count,source_type,content_json,lifecycle_stage,
                   memory_strength,detail_strength,emotional_arousal,personal_relevance
            FROM character_memories WHERE character_id=? AND status='active'{type_clause}
            ORDER BY event_sim_time DESC, created_at DESC LIMIT ?""",
        tuple(params),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        related = conn.execute(
            "SELECT entity_id,relation_role FROM character_memory_entities WHERE memory_id=? ORDER BY relation_role,entity_id",
            (row["memory_id"],),
        ).fetchall()
        result.append({
            "memory_id": row["memory_id"], "type": row["memory_type"], "summary": row["summary"],
            "event_sim_time": row["event_sim_time"], "encoded_sim_time": row["encoded_sim_time"],
            "salience": float(row["salience"]), "confidence": float(row["confidence"]),
            "last_recalled_sim_time": row["last_recalled_sim_time"], "recall_count": int(row["recall_count"]),
            "source_type": row["source_type"], "lifecycle_stage": row["lifecycle_stage"],
            "memory_strength": float(row["memory_strength"]), "detail_strength": float(row["detail_strength"]),
            "emotional_arousal": float(row["emotional_arousal"]), "personal_relevance": float(row["personal_relevance"]),
            "content": json.loads(row["content_json"] or "{}"),
            "related_entities": [{"entity_id": a["entity_id"], "role": a["relation_role"]} for a in related],
        })
    return result

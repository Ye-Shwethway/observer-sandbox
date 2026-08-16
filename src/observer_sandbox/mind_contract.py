from __future__ import annotations

import json
import sqlite3
import uuid
from typing import Any

from .mind_schema import MIND_SCHEMA_VERSION


EPISODE_MODES = {
    "task_focused", "spontaneous", "reflective", "prospective", "social", "evaluative"
}
ARTIFACT_TYPES = {
    "concern", "goal", "intention", "plan", "social_inference", "appraisal", "working_item"
}
ARTIFACT_STATUSES = {"active", "dormant", "resolved", "retired"}
LINK_SOURCE_KINDS = {"cycle", "episode", "artifact"}
LINK_TARGET_KINDS = {"memory", "event", "entity", "action_instance", "cycle", "episode", "artifact"}


def _clamp01(value: float) -> float:
    return max(0.0, min(float(value), 1.0))


def _validate_character(conn: sqlite3.Connection, character_id: str) -> None:
    row = conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='character'", (character_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"Unknown character: {character_id}")


def create_mental_cycle(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    sim_time: str,
    trigger_type: str,
    trigger_source_type: str | None = None,
    trigger_source_id: str | None = None,
    provider_id: str | None = None,
    model_id: str | None = None,
    input_summary: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    _validate_character(conn, character_id)
    cycle_id = f"mind_cycle_{uuid.uuid4().hex}"
    conn.execute(
        """INSERT INTO mental_cycles(
            cycle_id,character_id,sim_time,trigger_type,trigger_source_type,trigger_source_id,
            status,schema_version,provider_id,model_id,input_summary_json,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            cycle_id, character_id, sim_time, trigger_type, trigger_source_type, trigger_source_id,
            "open", MIND_SCHEMA_VERSION, provider_id, model_id,
            json.dumps(input_summary or {}, ensure_ascii=False),
            json.dumps(metadata or {}, ensure_ascii=False),
        ),
    )
    return cycle_id


def complete_mental_cycle(
    conn: sqlite3.Connection,
    cycle_id: str,
    *,
    output_summary: dict[str, Any] | None = None,
    status: str = "completed",
) -> None:
    if status not in {"completed", "failed", "aborted"}:
        raise ValueError(f"Invalid terminal mental-cycle status: {status}")
    conn.execute(
        """UPDATE mental_cycles SET status=?,output_summary_json=?,updated_at=CURRENT_TIMESTAMP
           WHERE cycle_id=?""",
        (status, json.dumps(output_summary or {}, ensure_ascii=False), cycle_id),
    )


def record_mental_episode(
    conn: sqlite3.Connection,
    *,
    cycle_id: str,
    mode: str,
    summary: str,
    start_sim_time: str,
    content: dict[str, Any] | None = None,
    importance: float = 0.5,
    valence: float = 0.0,
    activation: float = 0.5,
    persistence: float = 0.0,
    end_sim_time: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    if mode not in EPISODE_MODES:
        raise ValueError(f"Unsupported mental episode mode: {mode}")
    row = conn.execute(
        "SELECT character_id FROM mental_cycles WHERE cycle_id=?", (cycle_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"Unknown mental cycle: {cycle_id}")
    episode_id = f"mind_episode_{uuid.uuid4().hex}"
    conn.execute(
        """INSERT INTO mental_episodes(
            episode_id,cycle_id,character_id,mode,summary,content_json,importance,valence,
            activation,persistence,status,start_sim_time,end_sim_time,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            episode_id, cycle_id, str(row["character_id"]), mode, summary,
            json.dumps(content or {}, ensure_ascii=False), _clamp01(importance),
            max(-1.0, min(float(valence), 1.0)), _clamp01(activation), _clamp01(persistence),
            "completed" if end_sim_time else "active", start_sim_time, end_sim_time,
            json.dumps(metadata or {}, ensure_ascii=False),
        ),
    )
    return episode_id


def create_mental_artifact(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    artifact_type: str,
    title: str,
    sim_time: str,
    content: dict[str, Any] | None = None,
    priority: float = 0.5,
    activation: float = 0.5,
    confidence: float = 1.0,
    source_cycle_id: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> str:
    _validate_character(conn, character_id)
    if artifact_type not in ARTIFACT_TYPES:
        raise ValueError(f"Unsupported mental artifact type: {artifact_type}")
    if source_cycle_id is not None:
        row = conn.execute(
            "SELECT character_id FROM mental_cycles WHERE cycle_id=?", (source_cycle_id,)
        ).fetchone()
        if row is None or str(row["character_id"]) != character_id:
            raise ValueError("Mental artifact source cycle must belong to the same character")
    artifact_id = f"mind_artifact_{uuid.uuid4().hex}"
    conn.execute(
        """INSERT INTO mental_artifacts(
            artifact_id,character_id,artifact_type,title,content_json,priority,activation,confidence,
            status,source_cycle_id,created_sim_time,updated_sim_time,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            artifact_id, character_id, artifact_type, title,
            json.dumps(content or {}, ensure_ascii=False), _clamp01(priority), _clamp01(activation),
            _clamp01(confidence), "active", source_cycle_id, sim_time, sim_time,
            json.dumps(metadata or {}, ensure_ascii=False),
        ),
    )
    return artifact_id


def set_mental_artifact_status(
    conn: sqlite3.Connection,
    artifact_id: str,
    *,
    status: str,
    sim_time: str,
) -> None:
    if status not in ARTIFACT_STATUSES:
        raise ValueError(f"Unsupported mental artifact status: {status}")
    conn.execute(
        """UPDATE mental_artifacts SET status=?,updated_sim_time=?,resolved_sim_time=?,updated_at=CURRENT_TIMESTAMP
           WHERE artifact_id=?""",
        (status, sim_time, sim_time if status == "resolved" else None, artifact_id),
    )


def _source_character(conn: sqlite3.Connection, source_kind: str, source_id: str) -> str:
    if source_kind == "cycle":
        table, key = "mental_cycles", "cycle_id"
    elif source_kind == "episode":
        table, key = "mental_episodes", "episode_id"
    elif source_kind == "artifact":
        table, key = "mental_artifacts", "artifact_id"
    else:
        raise ValueError(f"Unsupported mental-link source kind: {source_kind}")
    row = conn.execute(f"SELECT character_id FROM {table} WHERE {key}=?", (source_id,)).fetchone()
    if row is None:
        raise ValueError(f"Unknown mental-link source: {source_kind}:{source_id}")
    return str(row["character_id"])


def link_mental_reference(
    conn: sqlite3.Connection,
    *,
    source_kind: str,
    source_id: str,
    target_kind: str,
    target_id: str | int,
    relation_type: str = "related",
    metadata: dict[str, Any] | None = None,
) -> None:
    if source_kind not in LINK_SOURCE_KINDS:
        raise ValueError(f"Unsupported source kind: {source_kind}")
    if target_kind not in LINK_TARGET_KINDS:
        raise ValueError(f"Unsupported target kind: {target_kind}")
    character_id = _source_character(conn, source_kind, source_id)
    conn.execute(
        """INSERT OR IGNORE INTO mental_links(
            character_id,source_kind,source_id,target_kind,target_id,relation_type,metadata_json
        ) VALUES(?,?,?,?,?,?,?)""",
        (
            character_id, source_kind, source_id, target_kind, str(target_id), relation_type,
            json.dumps(metadata or {}, ensure_ascii=False),
        ),
    )


def active_mental_context(
    conn: sqlite3.Connection,
    character_id: str,
    *,
    episode_limit: int = 8,
    artifact_limit: int = 12,
) -> dict[str, Any]:
    """Read a bounded structured Mind surface without invoking cognition or choosing behavior."""
    _validate_character(conn, character_id)
    episodes = conn.execute(
        """SELECT episode_id,cycle_id,mode,summary,importance,valence,activation,persistence,
                  status,start_sim_time,end_sim_time
           FROM mental_episodes WHERE character_id=?
           ORDER BY start_sim_time DESC,created_at DESC LIMIT ?""",
        (character_id, max(1, min(int(episode_limit), 32))),
    ).fetchall()
    artifacts = conn.execute(
        """SELECT artifact_id,artifact_type,title,priority,activation,confidence,status,
                  created_sim_time,updated_sim_time,resolved_sim_time
           FROM mental_artifacts WHERE character_id=? AND status IN ('active','dormant')
           ORDER BY CASE status WHEN 'active' THEN 0 ELSE 1 END,priority DESC,activation DESC,updated_at DESC
           LIMIT ?""",
        (character_id, max(1, min(int(artifact_limit), 32))),
    ).fetchall()
    return {
        "character_id": character_id,
        "episodes": [dict(row) for row in episodes],
        "active_artifacts": [dict(row) for row in artifacts],
    }

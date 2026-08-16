from __future__ import annotations

import json
import math
import sqlite3
from datetime import datetime
from typing import Any


DEFAULT_MEMORY_TRAIT = 50.0
ACCESSIBILITY_FLOOR = 0.12
FADED_STRENGTH = 0.08
REMOTE_MIN_AGE_DAYS = 30.0
REMOTE_MIN_STRENGTH = 0.25


def _clamp(value: float) -> float:
    return max(0.0, min(float(value), 1.0))


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def memory_trait(conn: sqlite3.Connection, character_id: str, key: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (character_id, key),
    ).fetchone()
    if row is None:
        return DEFAULT_MEMORY_TRAIT
    try:
        value = float(json.loads(row[0]))
    except (TypeError, ValueError, json.JSONDecodeError):
        return DEFAULT_MEMORY_TRAIT
    return max(0.0, min(value, 100.0))


def initialize_trace_strengths(conn: sqlite3.Connection, character_id: str, current_sim_time: str) -> None:
    encoding = memory_trait(conn, character_id, "memory.encoding") / 100.0
    rows = conn.execute(
        """SELECT memory_id,salience,emotional_arousal,personal_relevance,memory_type,
                  lifecycle_stage,memory_strength,detail_strength,last_dynamics_sim_time
           FROM character_memories WHERE character_id=? AND status='active'""",
        (character_id,),
    ).fetchall()
    for row in rows:
        if row["last_dynamics_sim_time"]:
            continue
        if row["memory_type"] == "semantic":
            strength = max(float(row["memory_strength"]), 0.9)
            detail = max(float(row["detail_strength"]), 0.9)
            stage = "consolidated"
        else:
            salience = float(row["salience"])
            arousal = float(row["emotional_arousal"])
            relevance = float(row["personal_relevance"])
            strength = _clamp(0.38 + 0.26 * salience + 0.12 * arousal + 0.10 * relevance + 0.14 * encoding)
            detail = _clamp(0.42 + 0.24 * salience + 0.06 * arousal + 0.10 * relevance + 0.18 * encoding)
            stage = str(row["lifecycle_stage"] or "recent")
        conn.execute(
            """UPDATE character_memories SET lifecycle_stage=?,memory_strength=?,detail_strength=?,
                   last_dynamics_sim_time=?,updated_at=CURRENT_TIMESTAMP WHERE memory_id=?""",
            (stage, strength, detail, current_sim_time, row["memory_id"]),
        )


def _settled_values(row: sqlite3.Row, retention: float, current_sim_time: str) -> tuple[float, float, str]:
    last_raw = row["last_dynamics_sim_time"] or row["encoded_sim_time"]
    try:
        elapsed_days = max(0.0, (_parse_time(current_sim_time) - _parse_time(str(last_raw))).total_seconds() / 86400.0)
    except (TypeError, ValueError):
        elapsed_days = 0.0
    if elapsed_days <= 0:
        return float(row["memory_strength"]), float(row["detail_strength"]), str(row["lifecycle_stage"])

    stage = str(row["lifecycle_stage"] or "recent")
    base_decay = {"recent": 0.32, "consolidated": 0.018, "remote": 0.007, "faded": 0.012}.get(stage, 0.018)
    salience = float(row["salience"])
    arousal = float(row["emotional_arousal"])
    relevance = float(row["personal_relevance"])
    retention_factor = 1.15 - 0.75 * retention
    gist_protection = max(0.20, 1.0 - (0.38 * salience + 0.30 * relevance + 0.22 * arousal))
    detail_protection = max(0.30, 1.0 - (0.35 * salience + 0.30 * relevance + 0.08 * arousal))

    strength = _clamp(float(row["memory_strength"]) * math.exp(-base_decay * retention_factor * gist_protection * elapsed_days))
    detail = _clamp(float(row["detail_strength"]) * math.exp(-base_decay * 1.35 * retention_factor * detail_protection * elapsed_days))

    try:
        age_days = max(0.0, (_parse_time(current_sim_time) - _parse_time(str(row["event_sim_time"]))).total_seconds() / 86400.0)
    except (TypeError, ValueError):
        age_days = 0.0
    if strength < FADED_STRENGTH:
        stage = "faded"
    elif stage in {"consolidated", "faded"} and age_days >= REMOTE_MIN_AGE_DAYS and strength >= REMOTE_MIN_STRENGTH:
        stage = "remote"
    return strength, detail, stage


def settle_memory_dynamics(conn: sqlite3.Connection, character_id: str, current_sim_time: str) -> None:
    initialize_trace_strengths(conn, character_id, current_sim_time)
    retention = memory_trait(conn, character_id, "memory.retention") / 100.0
    rows = conn.execute(
        """SELECT memory_id,memory_type,event_sim_time,encoded_sim_time,salience,lifecycle_stage,
                  memory_strength,detail_strength,emotional_arousal,personal_relevance,last_dynamics_sim_time
           FROM character_memories WHERE character_id=? AND status='active'""",
        (character_id,),
    ).fetchall()
    for row in rows:
        strength, detail, stage = _settled_values(row, retention, current_sim_time)
        conn.execute(
            """UPDATE character_memories SET memory_strength=?,detail_strength=?,lifecycle_stage=?,
                   last_dynamics_sim_time=?,updated_at=CURRENT_TIMESTAMP WHERE memory_id=?""",
            (strength, detail, stage, current_sim_time, row["memory_id"]),
        )


def consolidate_after_sleep(conn: sqlite3.Connection, character_id: str, current_sim_time: str) -> int:
    settle_memory_dynamics(conn, character_id, current_sim_time)
    encoding = memory_trait(conn, character_id, "memory.encoding") / 100.0
    rows = conn.execute(
        """SELECT memory_id,salience,memory_strength,detail_strength,emotional_arousal,personal_relevance
           FROM character_memories
           WHERE character_id=? AND status='active' AND memory_type='episodic' AND lifecycle_stage='recent'""",
        (character_id,),
    ).fetchall()
    count = 0
    for row in rows:
        significance = _clamp(
            0.42 * float(row["salience"])
            + 0.23 * float(row["personal_relevance"])
            + 0.20 * float(row["emotional_arousal"])
            + 0.15 * encoding
        )
        strength = _clamp(float(row["memory_strength"]) * (0.92 + 0.16 * significance))
        detail = _clamp(float(row["detail_strength"]) * (0.90 + 0.12 * significance))
        if strength < FADED_STRENGTH:
            continue
        conn.execute(
            """UPDATE character_memories SET lifecycle_stage='consolidated',memory_strength=?,detail_strength=?,
                   consolidated_sim_time=?,last_dynamics_sim_time=?,updated_at=CURRENT_TIMESTAMP WHERE memory_id=?""",
            (strength, detail, current_sim_time, current_sim_time, row["memory_id"]),
        )
        count += 1
    return count


def recall_accessibility(
    conn: sqlite3.Connection,
    character_id: str,
    *,
    memory_strength: float,
    relevance_score: float,
    cue_strength: float,
) -> float:
    recall = memory_trait(conn, character_id, "memory.recall") / 100.0
    return _clamp(0.58 * memory_strength + 0.20 * recall + 0.14 * relevance_score + 0.20 * cue_strength)


def reinforce_recalled_memories(
    conn: sqlite3.Connection,
    character_id: str,
    memory_ids: list[str],
    current_sim_time: str,
) -> None:
    if not memory_ids:
        return
    recall = memory_trait(conn, character_id, "memory.recall") / 100.0
    for memory_id in memory_ids:
        row = conn.execute(
            "SELECT memory_strength,detail_strength,lifecycle_stage FROM character_memories WHERE memory_id=? AND character_id=?",
            (memory_id, character_id),
        ).fetchone()
        if row is None:
            continue
        strength = _clamp(float(row["memory_strength"]) + 0.025 + 0.025 * recall)
        detail = _clamp(float(row["detail_strength"]) + 0.010 + 0.015 * recall)
        stage = str(row["lifecycle_stage"])
        if stage == "faded" and strength >= FADED_STRENGTH:
            stage = "remote"
        conn.execute(
            """UPDATE character_memories SET memory_strength=?,detail_strength=?,lifecycle_stage=?,
                   recall_count=recall_count+1,last_recalled_sim_time=?,last_dynamics_sim_time=?,updated_at=CURRENT_TIMESTAMP
               WHERE memory_id=? AND character_id=?""",
            (strength, detail, stage, current_sim_time, current_sim_time, memory_id, character_id),
        )

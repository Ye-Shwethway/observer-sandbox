from __future__ import annotations

import sqlite3

from observer_sandbox.training_load_guard import (
    shape_training_options_for_load,
    training_behavior_balance,
    training_load_status,
)


def _conn() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """CREATE TABLE action_instances (
            id INTEGER PRIMARY KEY,
            actor_id TEXT NOT NULL,
            action_type TEXT NOT NULL,
            status TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            planned_sim_time TEXT NOT NULL,
            started_sim_time TEXT,
            ended_sim_time TEXT,
            modifiers_json TEXT,
            outcome_json TEXT
        )"""
    )
    return conn


def _insert_training(
    conn: sqlite3.Connection,
    *,
    row_id: int,
    started: str,
    ended: str,
    minutes: int,
    effective_minutes: float | None = None,
) -> None:
    outcome = "{}" if effective_minutes is None else f'{{"training_load":{{"effective_minutes":{effective_minutes}}}}}'
    conn.execute(
        """INSERT INTO action_instances(
            id,actor_id,action_type,status,duration_minutes,planned_sim_time,
            started_sim_time,ended_sim_time,modifiers_json,outcome_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?)""",
        (row_id, "char_darian", "train", "completed", minutes, started, started, ended, "{}", outcome),
    )


def test_repetition_pressure_rises_with_recent_dose_frequency_and_recovery_strain() -> None:
    conn = _conn()
    now = "2026-08-16T15:00:00"
    empty_status = training_load_status(conn, "char_darian", sim_time=now)
    low = training_behavior_balance(
        conn,
        "char_darian",
        state={"sim_time": now, "fatigue": 20.0, "energy": 85.0},
        load_status=empty_status,
    )

    _insert_training(
        conn,
        row_id=1,
        started="2026-08-16T10:00:00",
        ended="2026-08-16T10:30:00",
        minutes=30,
        effective_minutes=30.0,
    )
    _insert_training(
        conn,
        row_id=2,
        started="2026-08-16T13:30:00",
        ended="2026-08-16T14:00:00",
        minutes=30,
        effective_minutes=30.0,
    )
    loaded_status = training_load_status(conn, "char_darian", sim_time=now)
    higher = training_behavior_balance(
        conn,
        "char_darian",
        state={"sim_time": now, "fatigue": 55.0, "energy": 45.0},
        load_status=loaded_status,
    )

    assert low["hard_block"] is False
    assert higher["hard_block"] is False
    assert higher["completed_training_bouts_24h"] == 2
    assert higher["repetition_pressure"] > low["repetition_pressure"]
    assert higher["level"] in {"moderate", "high"}


def test_soft_balance_never_removes_training_when_hard_load_guard_allows_it() -> None:
    conn = _conn()
    _insert_training(
        conn,
        row_id=1,
        started="2026-08-16T09:00:00",
        ended="2026-08-16T09:30:00",
        minutes=30,
        effective_minutes=30.0,
    )
    _insert_training(
        conn,
        row_id=2,
        started="2026-08-16T12:00:00",
        ended="2026-08-16T12:30:00",
        minutes=30,
        effective_minutes=30.0,
    )
    state = {"sim_time": "2026-08-16T15:00:00", "fatigue": 60.0, "energy": 40.0}
    options = [
        {
            "action": "train",
            "target": "obj_training_station",
            "duration": (10, 60),
            "modifiers": {"training_readiness": {"effectiveness": 1.0}},
        },
        {"action": "rest", "duration": (10, 60)},
    ]

    shaped, status = shape_training_options_for_load(
        conn,
        "char_darian",
        state=state,
        action_options=options,
    )

    train = next(option for option in shaped if option["action"] == "train")
    assert status["allowed"] is True
    assert status["behavioral_balance"]["hard_block"] is False
    assert train["training_behavior_balance"] == status["behavioral_balance"]
    assert train["duration"][1] > 0

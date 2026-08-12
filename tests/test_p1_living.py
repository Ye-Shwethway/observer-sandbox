from __future__ import annotations

from datetime import timedelta

import pytest

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, ensure_sim_clock, run_one_simulated_day, snapshot, validate_action


def test_p1_home_seed_and_darian_instantiation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM entities WHERE entity_type='location'").fetchone()[0] == 5
        assert conn.execute("SELECT COUNT(*) FROM entities WHERE entity_type='object'").fetchone()[0] == 15
        assert conn.execute("SELECT name FROM entities WHERE id='char_darian'").fetchone()[0] == "Darian Thorne"
        state = snapshot(conn)
        assert state["location"] == "room_bedroom"
        assert state["current_action"] == "idle"
        assert 0 <= state["energy"] <= 100
        assert 0 <= state["hunger"] <= 100
        assert 0 <= state["thirst"] <= 100
        assert 0 <= state["sleepiness"] <= 100


def test_p1_runtime_rejects_non_adjacent_move(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        with pytest.raises(ValueError):
            validate_action(conn, "char_darian", Action("move", 5, "room_gym"))


def test_p1_darian_completes_one_simulated_day_autonomously(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        start = ensure_sim_clock(conn)
        trace = run_one_simulated_day(conn)
        end = ensure_sim_clock(conn)
        assert end == start + timedelta(hours=24)
        assert 1 <= len(trace) <= 200

        events = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id='char_darian' AND event_type='action_completed'"
        ).fetchall()
        assert len(events) == len(trace)

        action_names = {
            __import__("json").loads(row[0])["action"] for row in events
        }
        assert "move" in action_names
        assert action_names & {"train", "eat", "drink", "sleep", "read", "rest"}

        final = snapshot(conn)
        for key in ("energy", "hunger", "thirst", "sleepiness", "cleanliness"):
            assert 0 <= final[key] <= 100
        assert final["current_action"] == "idle"

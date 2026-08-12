from __future__ import annotations

import pytest

from observer_sandbox.autonomy import (
    CANARY_MODE,
    MODE_KEY,
    PENDING_KEY,
    arm_canary_once,
    autonomy_tick,
    run_canary_once,
    set_autonomy_enabled,
    set_autonomy_paused,
    set_autonomy_speed,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, runtime_value, set_runtime_value, snapshot, validate_action


class FixedProvider:
    def __init__(self, action: Action):
        self.action = action
        self.calls = 0

    def choose(self, state, available_actions):
        self.calls += 1
        return self.action


def _enable(conn, *, speed=60.0):
    set_runtime_value(conn, "autonomy_enabled", True)
    set_runtime_value(conn, "paused", False)
    set_runtime_value(conn, "speed", speed)
    conn.commit()


def test_action_contract_rejects_wrong_or_remote_targets(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        for action in (
            Action("rest", 30, "obj_weights"),
            Action("train", 60, "obj_bed"),
            Action("idle", 10, "obj_bed"),
            Action("sleep", 5, "obj_bed"),
        ):
            with pytest.raises(ValueError):
                validate_action(conn, "char_darian", action)
        validate_action(conn, "char_darian", Action("rest", 30, "obj_bed"))


def test_scheduler_does_not_call_model_when_disabled_or_paused(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 30, "obj_bed", "recover"))
    with connect(db) as conn:
        assert autonomy_tick(conn, provider=provider, now_wall=1000)["state"] == "disabled"
        assert provider.calls == 0
        _enable(conn)
        set_runtime_value(conn, "paused", True)
        conn.commit()
        assert autonomy_tick(conn, provider=provider, now_wall=1000)["state"] == "paused"
        assert provider.calls == 0


def test_scheduler_persists_then_completes_one_action(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 30, "obj_bed", "short recovery"))
    with connect(db) as conn:
        _enable(conn, speed=60.0)
        before = snapshot(conn)
        planned = autonomy_tick(conn, provider=provider, now_wall=1000)
        assert planned["state"] == "planned"
        pending = runtime_value(conn, PENDING_KEY, None)
        assert pending["action"] == "rest"
        assert pending["due_wall_time"] == 1030.0
        assert snapshot(conn)["sim_time"] == before["sim_time"]
        assert snapshot(conn)["current_action"] == "rest"
        assert provider.calls == 1

        active = autonomy_tick(conn, provider=provider, now_wall=1015)
        assert active["state"] == "in_progress"
        assert provider.calls == 1

        completed = autonomy_tick(conn, provider=provider, now_wall=1030)
        assert completed["state"] == "completed"
        assert runtime_value(conn, PENDING_KEY, None) is None
        after = snapshot(conn)
        assert after["current_action"] == "idle"
        assert after["sim_time"] != before["sim_time"]
        completed_events = conn.execute("SELECT COUNT(*) FROM events WHERE event_type='action_completed'").fetchone()[0]
        assert completed_events == 1


def test_scheduler_recovers_completed_pending_without_duplicate(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 30, "obj_bed", "short recovery"))
    with connect(db) as conn:
        _enable(conn, speed=60.0)
        planned = autonomy_tick(conn, provider=provider, now_wall=1000)
        action_id = planned["pending"]["action_id"]
        from observer_sandbox.simulation import apply_action
        apply_action(conn, Action("rest", 30, "obj_bed", "short recovery"), action_id=action_id)
        assert runtime_value(conn, PENDING_KEY, None) is not None
        recovered = autonomy_tick(conn, provider=provider, now_wall=1031)
        assert recovered["state"] == "recovered_completed"
        assert runtime_value(conn, PENDING_KEY, None) is None
        completed_events = conn.execute("SELECT payload_json FROM events WHERE event_type='action_completed'").fetchall()
        assert len(completed_events) == 1


def test_canary_runs_exactly_one_action_then_disables(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 30, "obj_bed", "bounded canary recovery"))
    with connect(db) as conn:
        set_autonomy_speed(conn, 60.0)
        armed = arm_canary_once(conn)
        assert armed["autonomy_enabled"] is True
        assert armed["mode"] == CANARY_MODE

        planned = autonomy_tick(conn, provider=provider, now_wall=1000)
        assert planned["state"] == "planned"
        assert planned["pending"]["autonomy_mode"] == CANARY_MODE

        completed = autonomy_tick(conn, provider=provider, now_wall=1030)
        assert completed["state"] == "completed"
        assert runtime_value(conn, "autonomy_enabled", True) is False
        assert runtime_value(conn, MODE_KEY, None) == "normal"
        assert runtime_value(conn, PENDING_KEY, None) is None
        assert provider.calls == 1
        assert conn.execute("SELECT COUNT(*) FROM events WHERE event_type='action_completed'").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM events WHERE event_type='autonomy_canary_completed'").fetchone()[0] == 1

        assert autonomy_tick(conn, provider=provider, now_wall=1031)["state"] == "disabled"
        assert provider.calls == 1


def test_synchronous_canary_command_completes_without_wall_time_wait(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 30, "obj_bed", "bounded synchronous canary"))
    with connect(db) as conn:
        before = snapshot(conn)
        result = run_canary_once(conn, provider=provider, now_wall=1000)
        assert result["ok"] is True
        assert result["state"] == "completed"
        assert result["plan"]["pending"]["due_wall_time"] == 2800.0
        assert result["completion"]["state"] == "completed"
        assert result["after"]["autonomy_enabled"] is False
        assert result["after"]["mode"] == "normal"
        assert result["after"]["pending_action"] is None
        assert result["after"]["character"]["sim_time"] != before["sim_time"]
        assert provider.calls == 1
        assert conn.execute("SELECT COUNT(*) FROM events WHERE event_type='action_completed'").fetchone()[0] == 1


def test_canary_decision_failure_disables_immediately(tmp_path):
    class BadProvider:
        def choose(self, state, available_actions):
            raise RuntimeError("fixture failure")

    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        result = run_canary_once(conn, provider=BadProvider(), now_wall=1000)
        assert result["ok"] is False
        assert result["state"] == "decision_error"
        assert runtime_value(conn, "autonomy_enabled", True) is False
        assert runtime_value(conn, MODE_KEY, None) == "normal"
        assert conn.execute("SELECT COUNT(*) FROM events WHERE event_type='autonomy_canary_failed'").fetchone()[0] == 1


def test_control_guards_pending_action_and_speed(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 30, "obj_bed", "recover"))
    with connect(db) as conn:
        set_autonomy_paused(conn, False)
        with pytest.raises(ValueError):
            set_autonomy_speed(conn, 0)
        with pytest.raises(ValueError):
            set_autonomy_speed(conn, 3601)
        set_autonomy_speed(conn, 60)
        set_autonomy_enabled(conn, True)
        autonomy_tick(conn, provider=provider, now_wall=1000)
        with pytest.raises(ValueError):
            set_autonomy_enabled(conn, False)
        with pytest.raises(ValueError):
            set_autonomy_speed(conn, 5)

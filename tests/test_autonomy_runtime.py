from __future__ import annotations

import pytest

from observer_sandbox.actor_runtime import actor_runtime, pending_action, set_actor_runtime
from observer_sandbox.autonomy import CANARY_MODE, arm_canary_once, autonomy_tick, run_canary_once, set_autonomy_enabled, set_autonomy_paused, set_autonomy_speed
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, set_runtime_value, snapshot, validate_action

BED = "obj_thorne_estate_master_bed"
WEIGHTS = "obj_thorne_estate_gym_free_weights"


class FixedProvider:
    def __init__(self, action: Action):
        self.action = action
        self.calls = 0
    def choose(self, state, available_actions):
        self.calls += 1
        return self.action


def _enable(conn, *, speed=60.0, actor_id="char_darian"):
    set_actor_runtime(conn, actor_id, autonomy_enabled=True, autonomy_mode="normal", wake_reason="test_enable")
    set_runtime_value(conn, "paused", False)
    set_runtime_value(conn, "speed", speed)
    conn.commit()


def test_action_contract_rejects_wrong_or_remote_targets(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db)
    with connect(db) as conn:
        for action in (Action("rest", 30, WEIGHTS), Action("train", 60, BED), Action("idle", 10, BED), Action("sleep", 5, BED)):
            with pytest.raises(ValueError): validate_action(conn, "char_darian", action)
        validate_action(conn, "char_darian", Action("rest", 30, BED))


def test_scheduler_does_not_call_model_when_disabled_or_paused(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db); provider = FixedProvider(Action("rest", 30, BED, "recover"))
    with connect(db) as conn:
        assert autonomy_tick(conn, provider=provider, now_wall=1000)["state"] == "disabled"; assert provider.calls == 0
        _enable(conn); set_runtime_value(conn, "paused", True); conn.commit()
        assert autonomy_tick(conn, provider=provider, now_wall=1000)["state"] == "paused"; assert provider.calls == 0


def test_scheduler_persists_first_class_action_then_completes(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db); provider = FixedProvider(Action("rest", 30, BED, "short recovery"))
    with connect(db) as conn:
        _enable(conn, speed=60.0); before = snapshot(conn)
        planned = autonomy_tick(conn, provider=provider, now_wall=1000)
        assert planned["state"] == "planned"; pending = pending_action(conn, "char_darian")
        assert pending["action"] == "rest"; assert pending["due_wall_time"] == 1030.0
        row = conn.execute("SELECT actor_id,place_id,status FROM action_instances WHERE id=?", (pending["action_id"],)).fetchone()
        assert row["actor_id"] == "char_darian" and row["place_id"] == before["location"] and row["status"] == "in_progress"
        assert snapshot(conn)["sim_time"] == before["sim_time"] and snapshot(conn)["current_action"] == "rest" and provider.calls == 1
        assert autonomy_tick(conn, provider=provider, now_wall=1015)["state"] == "in_progress" and provider.calls == 1
        completed = autonomy_tick(conn, provider=provider, now_wall=1030)
        assert completed["state"] == "completed" and pending_action(conn, "char_darian") is None
        action_row = conn.execute("SELECT status,ended_sim_time FROM action_instances WHERE id=?", (planned["pending"]["action_id"],)).fetchone()
        assert action_row["status"] == "completed" and action_row["ended_sim_time"] is not None
        event = conn.execute("SELECT action_id,location_id,state_changes_json FROM events WHERE event_type='action_completed'").fetchone()
        assert event["action_id"] == planned["pending"]["action_id"] and event["location_id"] is not None and event["state_changes_json"] != "{}"


def test_scheduler_recovers_completed_pending_without_duplicate(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db); provider = FixedProvider(Action("rest", 30, BED, "short recovery"))
    with connect(db) as conn:
        _enable(conn, speed=60.0); planned = autonomy_tick(conn, provider=provider, now_wall=1000); action_id = planned["pending"]["action_id"]
        apply_action(conn, Action("rest", 30, BED, "short recovery"), action_id=action_id)
        assert pending_action(conn, "char_darian") is not None
        assert autonomy_tick(conn, provider=provider, now_wall=1031)["state"] == "recovered_completed"
        assert pending_action(conn, "char_darian") is None
        assert conn.execute("SELECT COUNT(*) FROM events WHERE event_type='action_completed' AND action_id=?", (action_id,)).fetchone()[0] == 1


def test_canary_runs_exactly_one_action_then_disables(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db); provider = FixedProvider(Action("rest", 30, BED, "bounded canary recovery"))
    with connect(db) as conn:
        set_autonomy_speed(conn, 60.0); armed = arm_canary_once(conn)
        assert armed["autonomy_enabled"] is True and armed["mode"] == CANARY_MODE
        planned = autonomy_tick(conn, provider=provider, now_wall=1000); assert planned["state"] == "planned"
        assert planned["pending"]["autonomy_mode"] == CANARY_MODE
        assert autonomy_tick(conn, provider=provider, now_wall=1030)["state"] == "completed"
        state = actor_runtime(conn, "char_darian")
        assert state["autonomy_enabled"] is False and state["autonomy_mode"] == "normal" and state["pending_action_id"] is None
        assert provider.calls == 1
        assert conn.execute("SELECT COUNT(*) FROM events WHERE event_type='action_completed'").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM events WHERE event_type='autonomy_canary_completed'").fetchone()[0] == 1


def test_synchronous_canary_command_completes_without_wall_time_wait(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db); provider = FixedProvider(Action("rest", 30, BED, "bounded synchronous canary"))
    with connect(db) as conn:
        before = snapshot(conn); result = run_canary_once(conn, provider=provider, now_wall=1000)
        assert result["ok"] is True and result["state"] == "completed"
        assert result["plan"]["pending"]["due_wall_time"] == 2800.0
        assert result["after"]["autonomy_enabled"] is False and result["after"]["pending_action"] is None
        assert result["after"]["character"]["sim_time"] != before["sim_time"] and provider.calls == 1


def test_canary_decision_failure_disables_immediately(tmp_path):
    class BadProvider:
        def choose(self, state, available_actions): raise RuntimeError("fixture failure")
    db = tmp_path / "observer.sqlite3"; initialize(db)
    with connect(db) as conn:
        result = run_canary_once(conn, provider=BadProvider(), now_wall=1000)
        assert result["ok"] is False and result["state"] == "decision_error"
        state = actor_runtime(conn, "char_darian")
        assert state["autonomy_enabled"] is False and state["autonomy_mode"] == "normal"
        assert conn.execute("SELECT COUNT(*) FROM events WHERE event_type='autonomy_canary_failed'").fetchone()[0] == 1


def test_control_guards_global_speed_when_any_actor_pending(tmp_path):
    db = tmp_path / "observer.sqlite3"; initialize(db); provider = FixedProvider(Action("rest", 30, BED, "recover"))
    with connect(db) as conn:
        set_autonomy_paused(conn, False)
        with pytest.raises(ValueError): set_autonomy_speed(conn, 0)
        with pytest.raises(ValueError): set_autonomy_speed(conn, 3601)
        set_autonomy_speed(conn, 60); set_autonomy_enabled(conn, True); autonomy_tick(conn, provider=provider, now_wall=1000)
        with pytest.raises(ValueError): set_autonomy_enabled(conn, False)
        with pytest.raises(ValueError): set_autonomy_speed(conn, 5)

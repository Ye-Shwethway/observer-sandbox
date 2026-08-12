from __future__ import annotations

from observer_sandbox.autonomy import PENDING_KEY, autonomy_tick
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
            try:
                validate_action(conn, "char_darian", action)
            except ValueError:
                pass
            else:
                raise AssertionError(f"Expected invalid action contract: {action}")
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
        # Simulate a crash after durable completion but before pending cleanup.
        assert runtime_value(conn, PENDING_KEY, None) is not None
        recovered = autonomy_tick(conn, provider=provider, now_wall=1031)
        assert recovered["state"] == "recovered_completed"
        assert runtime_value(conn, PENDING_KEY, None) is None
        completed_events = conn.execute("SELECT payload_json FROM events WHERE event_type='action_completed'").fetchall()
        assert len(completed_events) == 1

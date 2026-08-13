from __future__ import annotations

import pytest

from observer_sandbox.actor_runtime import pending_action, set_actor_runtime
from observer_sandbox.autonomy import autonomy_tick, set_autonomy_paused, set_autonomy_speed
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, set_runtime_value

BED = "obj_thorne_estate_master_bed"


class FixedProvider:
    def __init__(self, action: Action):
        self.action = action

    def choose(self, state, available_actions):
        return self.action


def _enable(conn, *, speed: float = 1.0) -> None:
    set_actor_runtime(conn, "char_darian", autonomy_enabled=True, autonomy_mode="normal", wake_reason="test_enable")
    set_runtime_value(conn, "paused", False)
    set_runtime_value(conn, "speed", speed)
    conn.commit()


def test_speed_change_reschedules_running_action_without_cancelling(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 60, BED, "recover"))
    with connect(db) as conn:
        _enable(conn, speed=1.0)
        planned = autonomy_tick(conn, provider=provider, now_wall=1000.0)
        action_id = planned["pending"]["action_id"]
        assert planned["pending"]["due_wall_time"] == 4600.0

        status = set_autonomy_speed(conn, 60.0, now_wall=1600.0)
        pending = pending_action(conn, "char_darian")
        assert status["speed"] == 60.0
        assert pending["action_id"] == action_id
        assert pending["speed_at_plan"] == 60.0
        # Ten sim minutes elapsed at 1x; fifty sim minutes remain and now take 50 seconds at 60x.
        assert pending["due_wall_time"] == pytest.approx(1650.0)
        assert autonomy_tick(conn, provider=provider, now_wall=1649.0)["state"] == "in_progress"
        assert autonomy_tick(conn, provider=provider, now_wall=1650.0)["state"] == "completed"


def test_repeated_speed_changes_preserve_remaining_simulated_time(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 60, BED, "recover"))
    with connect(db) as conn:
        _enable(conn, speed=1.0)
        autonomy_tick(conn, provider=provider, now_wall=1000.0)
        set_autonomy_speed(conn, 10.0, now_wall=1600.0)
        first = pending_action(conn, "char_darian")
        assert first["due_wall_time"] == pytest.approx(1900.0)

        # Fifty seconds at 10x consumes 8.333... sim minutes, leaving 41.666... sim minutes.
        set_autonomy_speed(conn, 50.0, now_wall=1650.0)
        second = pending_action(conn, "char_darian")
        assert second["due_wall_time"] == pytest.approx(1700.0)
        assert second["speed_at_plan"] == 50.0


def test_pause_freezes_pending_wall_countdown_and_resume_shifts_due_time(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 60, BED, "recover"))
    with connect(db) as conn:
        _enable(conn, speed=60.0)
        autonomy_tick(conn, provider=provider, now_wall=1000.0)
        assert pending_action(conn, "char_darian")["due_wall_time"] == 1060.0

        set_autonomy_paused(conn, True, now_wall=1020.0)
        assert autonomy_tick(conn, provider=provider, now_wall=1100.0)["state"] == "paused"
        set_autonomy_paused(conn, False, now_wall=1120.0)
        pending = pending_action(conn, "char_darian")
        # The 100 real seconds spent paused do not consume action countdown.
        assert pending["due_wall_time"] == pytest.approx(1160.0)


def test_speed_can_change_while_paused_without_consuming_paused_time(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("rest", 60, BED, "recover"))
    with connect(db) as conn:
        _enable(conn, speed=1.0)
        autonomy_tick(conn, provider=provider, now_wall=1000.0)
        set_autonomy_paused(conn, True, now_wall=1600.0)
        set_autonomy_speed(conn, 60.0, now_wall=2000.0)
        paused_pending = pending_action(conn, "char_darian")
        # Speed change is anchored to pause start; paused wall time does not count.
        assert paused_pending["due_wall_time"] == pytest.approx(1650.0)

        set_autonomy_paused(conn, False, now_wall=2200.0)
        resumed = pending_action(conn, "char_darian")
        assert resumed["due_wall_time"] == pytest.approx(2250.0)


def test_speed_bounds_remain_guarded(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        with pytest.raises(ValueError):
            set_autonomy_speed(conn, 0)
        with pytest.raises(ValueError):
            set_autonomy_speed(conn, 3601)

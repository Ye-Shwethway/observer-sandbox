from observer_sandbox.autonomy import autonomy_tick, set_autonomy_enabled, set_autonomy_paused, set_autonomy_speed
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action


class FixedProvider:
    def __init__(self, action: Action):
        self.action = action

    def choose(self, state, available_actions):
        return self.action


def test_one_sim_minute_action_remains_positive_and_completes_at_3600x(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider(Action("idle", 1, None, "minimum timing boundary"))

    with connect(db) as conn:
        set_autonomy_paused(conn, False)
        set_autonomy_speed(conn, 3600.0, now_wall=1000.0)
        set_autonomy_enabled(conn, True)

        planned = autonomy_tick(conn, provider=provider, now_wall=1000.0)
        due = float(planned["pending"]["due_wall_time"])
        assert due > 1000.0
        assert abs((due - 1000.0) - (1.0 / 60.0)) < 1e-9

        assert autonomy_tick(conn, provider=provider, now_wall=due - 0.000001)["state"] == "in_progress"
        assert autonomy_tick(conn, provider=provider, now_wall=due + 0.000001)["state"] == "completed"

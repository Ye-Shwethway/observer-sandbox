from observer_sandbox.autonomy import autonomy_tick, set_autonomy_enabled
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action
from observer_sandbox.telegram_bot import _boot_message


class FixedProvider:
    def __init__(self):
        self.calls = 0

    def choose(self, state, available_actions):
        self.calls += 1
        return Action("rest", 30, "obj_bed", "bounded recovery")


def test_mind_wakes_only_at_decision_boundaries(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    provider = FixedProvider()

    with connect(db) as conn:
        set_autonomy_enabled(conn, True)
        planned = autonomy_tick(conn, provider=provider, now_wall=1000)
        assert planned["state"] == "planned"
        assert provider.calls == 1

        stats = conn.execute("SELECT value_json FROM runtime_state WHERE key='cognition_wake_stats'").fetchone()
        assert '"decision_calls": 1' in stats[0]

        for now in (1001, 1010, 1500, 2000, 2799):
            assert autonomy_tick(conn, provider=provider, now_wall=now)["state"] == "in_progress"
        assert provider.calls == 1

        assert autonomy_tick(conn, provider=provider, now_wall=2800)["state"] == "completed"
        assert provider.calls == 1

        status = autonomy_tick(conn, provider=provider, now_wall=2801)
        assert status["state"] == "planned"
        assert provider.calls == 2


def test_universe_boot_message_is_creator_facing():
    message = _boot_message()
    assert "Universe is alive!" in message
    assert "wake-on-demand" in message
    assert "/status" in message

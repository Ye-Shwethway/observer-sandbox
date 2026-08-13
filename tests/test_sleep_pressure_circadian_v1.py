from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, set_runtime_value, snapshot
from observer_sandbox.sleep_pressure import sleep_pressure_signal
from observer_sandbox.world import set_field


MASTER_SUITE = "loc_thorne_estate_master_suite"
MASTER_BED = "obj_thorne_estate_master_bed"


def test_rest_recovers_fatigue_without_reducing_sleepiness(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "physiology.fatigue", 50.0)
        set_field(conn, "char_darian", "needs.sleepiness", 30.0)
        conn.commit()
        before = snapshot(conn, "char_darian")
        after = apply_action(conn, Action("rest", 60, None, "physical recovery"), "char_darian")
        assert after["fatigue"] < before["fatigue"]
        assert after["sleepiness"] > before["sleepiness"]
        assert after["sleepiness"] == 33.0


def test_deep_night_long_awake_state_routes_to_real_overnight_sleep(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        apply_action(conn, Action("idle", 10, None, "start observed day"), "char_darian")
        set_runtime_value(conn, "sim_time", "2025-05-02T02:30:00+00:00")
        set_field(conn, "char_darian", "runtime.location", MASTER_SUITE)
        set_field(conn, "char_darian", "needs.sleepiness", 32.0)
        conn.commit()

        state = snapshot(conn, "char_darian")
        enriched = ModelDecisionProvider(conn, character_id="char_darian")._enrich_state(state)
        pressure = enriched["decision_signals"]["sleep_pressure"]

        assert pressure["level"] == "critical"
        assert pressure["hours_awake"] >= 19.0
        assert "deep_night_circadian_pressure" in pressure["reasons"]
        assert enriched["decision_signals"]["highest_priority"]["need"] == "sleepiness"
        assert enriched["decision_signals"]["recommended_duration"]["action"] == "sleep"
        assert enriched["decision_signals"]["recommended_duration"]["min_minutes"] == 360
        assert enriched["decision_signals"]["recommended_duration"]["max_minutes"] == 540
        assert {option["action"] for option in enriched["action_options"]} == {"sleep"}
        sleep_option = enriched["action_options"][0]
        assert sleep_option["target"] == MASTER_BED
        assert sleep_option["duration"] == (360, 540)


def test_recent_restorative_sleep_keeps_daytime_pressure_comfortable(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_runtime_value(conn, "sim_time", "2025-05-01T22:00:00+00:00")
        set_field(conn, "char_darian", "runtime.location", MASTER_SUITE)
        set_field(conn, "char_darian", "needs.sleepiness", 70.0)
        conn.commit()
        apply_action(conn, Action("sleep", 480, MASTER_BED, "normal overnight sleep"), "char_darian")

        set_runtime_value(conn, "sim_time", "2025-05-02T12:00:00+00:00")
        set_field(conn, "char_darian", "needs.sleepiness", 20.0)
        conn.commit()
        state = snapshot(conn, "char_darian")
        pressure = sleep_pressure_signal(conn, state=state, actor_id="char_darian")

        assert pressure["last_restorative_sleep_end"] == "2025-05-02T06:00:00+00:00"
        assert pressure["hours_awake"] == 6.0
        assert pressure["level"] == "comfortable"
        assert pressure["night_window"] is False

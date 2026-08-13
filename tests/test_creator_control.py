from observer_sandbox.creator_control import BASIC_STAT_BASELINE, restore_basic_stats
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot
from observer_sandbox.telegram_bot import _callback_view, handle_command
from observer_sandbox.world import set_field


def _make_unhealthy(conn):
    set_field(conn, "char_darian", "needs.energy", 12.0)
    set_field(conn, "char_darian", "needs.hunger", 82.0)
    set_field(conn, "char_darian", "needs.thirst", 76.0)
    set_field(conn, "char_darian", "needs.sleepiness", 74.0)
    set_field(conn, "char_darian", "physiology.cleanliness", 18.0)
    set_field(conn, "char_darian", "physiology.fatigue", 63.0)
    set_field(conn, "char_darian", "runtime.current_action", "rest")
    conn.commit()


def test_restore_basic_stats_preserves_world_context_and_records_audit_event(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _make_unhealthy(conn)
        before = snapshot(conn, "char_darian")
        result = restore_basic_stats(conn, "char_darian", requested_by="test-suite")
        after = result["after"]

        assert after["energy"] == BASIC_STAT_BASELINE["needs.energy"]
        assert after["hunger"] == BASIC_STAT_BASELINE["needs.hunger"]
        assert after["thirst"] == BASIC_STAT_BASELINE["needs.thirst"]
        assert after["sleepiness"] == BASIC_STAT_BASELINE["needs.sleepiness"]
        assert after["cleanliness"] == BASIC_STAT_BASELINE["physiology.cleanliness"]
        assert after["fatigue"] == BASIC_STAT_BASELINE["physiology.fatigue"]
        assert after["current_action"] == "idle"
        assert after["location"] == before["location"]
        assert after["sim_time"] == before["sim_time"]

        event = conn.execute(
            "SELECT event_type,actor_id,location_id,state_changes_json,payload_json FROM events WHERE event_type=? ORDER BY id DESC LIMIT 1",
            ("creator_basic_stats_restored",),
        ).fetchone()
        assert event is not None
        assert event["actor_id"] == "char_darian"
        assert event["location_id"] == before["location"]
        assert "energy" in event["state_changes_json"]
        assert "test-suite" in event["payload_json"]


def test_telegram_restore_is_owner_only_and_has_confirmation_ui(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")

    with connect(db) as conn:
        _make_unhealthy(conn)
        _, owner_keyboard = _callback_view(conn, 111, "char:char_darian")
        assert any(
            button["callback_data"] == "ctl:restore_prompt:char_darian"
            for row in owner_keyboard
            for button in row
        )

        _, allowed_keyboard = _callback_view(conn, 222, "char:char_darian")
        assert not any(
            button["callback_data"].startswith("ctl:restore_")
            for row in allowed_keyboard
            for button in row
        )

        prompt, prompt_keyboard = _callback_view(conn, 111, "ctl:restore_prompt:char_darian")
        assert "RESTORE DARIAN THORNE BASIC STATS" in prompt
        assert prompt_keyboard[0][0]["callback_data"] == "ctl:restore_apply:char_darian"

        denied, _ = _callback_view(conn, 222, "ctl:restore_apply:char_darian")
        assert "Creator authority required" in denied
        assert snapshot(conn, "char_darian")["energy"] == 12.0

        applied, _ = _callback_view(conn, 111, "ctl:restore_apply:char_darian")
        assert "CREATOR RESTORE APPLIED" in applied
        assert snapshot(conn, "char_darian")["energy"] == 75.0
        assert snapshot(conn, "char_darian")["fatigue"] == 0.0


def test_restorestats_command_is_owner_only(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")

    with connect(db) as conn:
        _make_unhealthy(conn)

    denied = handle_command(db, user_id=222, text="/restorestats")
    assert "Creator authority required" in denied
    with connect(db) as conn:
        assert snapshot(conn, "char_darian")["energy"] == 12.0

    applied = handle_command(db, user_id=111, text="/restorestats")
    assert "CREATOR RESTORE APPLIED" in applied
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        assert state["energy"] == 75.0
        assert state["hunger"] == 20.0
        assert state["fatigue"] == 0.0

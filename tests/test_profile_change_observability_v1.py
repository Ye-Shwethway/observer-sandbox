import json

from observer_sandbox.db import connect
from observer_sandbox.profile_change_observer import (
    attach_profile_display_deltas,
    capture_profile_change_state,
    observe_profile_changes,
    set_stat_notifications,
    stat_notifications_enabled,
)
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view, handle_command
from observer_sandbox.telegram_profile_browser import _fmt_profile_section
from observer_sandbox import telegram_profile_notifications


def _set_profile_number(conn, field_key: str, value: float) -> None:
    conn.execute(
        "UPDATE character_profile_values SET value_json=? WHERE entity_id='char_darian' AND field_key=?",
        (json.dumps(float(value)), field_key),
    )
    conn.commit()


def test_body_measurement_delta_accumulates_until_fine_grained_visibility_threshold(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        initial = capture_profile_change_state(conn, "char_darian")
        starting = initial["body.biceps_flexed_in"]["value"]

        _set_profile_number(conn, "body.biceps_flexed_in", starting + 0.02)
        second = capture_profile_change_state(conn, "char_darian")
        assert observe_profile_changes(conn, "char_darian", initial, second, sim_time="2025-05-06T01:00:00+00:00") == []

        _set_profile_number(conn, "body.biceps_flexed_in", starting + 0.04)
        third = capture_profile_change_state(conn, "char_darian")
        assert observe_profile_changes(conn, "char_darian", second, third, sim_time="2025-05-06T02:00:00+00:00") == []

        _set_profile_number(conn, "body.biceps_flexed_in", starting + 0.06)
        fourth = capture_profile_change_state(conn, "char_darian")
        surfaced = observe_profile_changes(conn, "char_darian", third, fourth, sim_time="2025-05-06T03:00:00+00:00")
        change = next(item for item in surfaced if item["key"] == "body.biceps_flexed_in")
        assert change["delta"] == 0.06
        assert change["beneficial"] is None

        body = profile_section(conn, "char_darian", "body", role="owner")
        attach_profile_display_deltas(conn, "char_darian", body)
        text = _fmt_profile_section(body)
        assert "Biceps" in text
        assert '▲ 0.06"' in text


def test_grade_transition_surfaces_even_below_numeric_threshold(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _set_profile_number(conn, "raps_pa.strength", 89.98)
        before = capture_profile_change_state(conn, "char_darian")
        observe_profile_changes(conn, "char_darian", before, before, sim_time="2025-05-06T01:00:00+00:00")

        _set_profile_number(conn, "raps_pa.strength", 90.01)
        after = capture_profile_change_state(conn, "char_darian")
        surfaced = observe_profile_changes(conn, "char_darian", before, after, sim_time="2025-05-06T02:00:00+00:00")
        strength = next(item for item in surfaced if item["key"] == "raps_pa.strength")

        assert strength["delta"] == 0.03
        assert strength["grade_changed"] is True
        assert strength["old_grade"]["grade"] == "A"
        assert strength["new_grade"]["grade"] == "S"
        assert strength["beneficial"] is True


def test_per_character_stat_notification_toggle_resets_without_backlog(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        assert stat_notifications_enabled(conn, 111, "char_darian") is True
        assert set_stat_notifications(conn, 111, "char_darian", False) is False
        assert stat_notifications_enabled(conn, 111, "char_darian") is False

        _set_profile_number(conn, "raps_pa.strength", 91.0)
        assert set_stat_notifications(conn, 111, "char_darian", True) is True
        assert stat_notifications_enabled(conn, 111, "char_darian") is True

        current = capture_profile_change_state(conn, "char_darian")
        from observer_sandbox.profile_change_observer import pending_stat_notification_changes
        assert pending_stat_notification_changes(
            conn,
            111,
            "char_darian",
            current,
            current,
            sim_time="2025-05-06T03:00:00+00:00",
        ) == []


def test_statnotify_command_and_character_button_show_scoped_state(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    reply = handle_command(db, user_id=111, text="/statnotify Darian Thorne off")
    assert "Darian Thorne stat updates OFF" in reply
    assert "no historical backlog" in reply

    with connect(db) as conn:
        assert stat_notifications_enabled(conn, 111, "char_darian") is False
        _, keyboard = _callback_view(conn, 111, "char:char_darian")
        button_texts = [button["text"] for row in keyboard for button in row]
        assert "🔔 Stat Updates: OFF" in button_texts

    status = handle_command(db, user_id=111, text="/statnotify")
    assert "Darian Thorne · OFF" in status


def test_profile_notification_is_aggregated_and_respects_character_gate(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_BOT_TOKEN", "test-token")

    sent = []
    monkeypatch.setattr(telegram_profile_notifications, "_send", lambda token, user_id, message: sent.append((user_id, message)))

    with connect(db) as conn:
        before = capture_profile_change_state(conn, "char_darian")
        _set_profile_number(conn, "raps_pa.strength", before["raps_pa.strength"]["value"] + 0.2)
        _set_profile_number(conn, "body.biceps_flexed_in", before["body.biceps_flexed_in"]["value"] + 0.06)
        current = capture_profile_change_state(conn, "char_darian")

        count = telegram_profile_notifications.dispatch_profile_change_notifications(
            conn,
            actor_id="char_darian",
            before=before,
            current=current,
            sim_time="2025-05-06T04:00:00+00:00",
        )
        assert count == 1
        assert len(sent) == 1
        assert "📈 CHARACTER PROGRESSION" in sent[0][1]
        assert "Strength" in sent[0][1]
        assert "Biceps" in sent[0][1]

        set_stat_notifications(conn, 111, "char_darian", False)
        _set_profile_number(conn, "raps_pa.strength", current["raps_pa.strength"]["value"] + 0.4)
        later = capture_profile_change_state(conn, "char_darian")
        count = telegram_profile_notifications.dispatch_profile_change_notifications(
            conn,
            actor_id="char_darian",
            before=current,
            current=later,
            sim_time="2025-05-06T05:00:00+00:00",
        )
        assert count == 0
        assert len(sent) == 1

import json

from observer_sandbox import telegram_profile_notifications
from observer_sandbox.db import connect
from observer_sandbox.profile_change_observer import capture_profile_change_state
from observer_sandbox.runtime import initialize


def _set_number(conn, field_key: str, value: float) -> None:
    conn.execute(
        "UPDATE character_profile_values SET value_json=? WHERE entity_id='char_darian' AND field_key=?",
        (json.dumps(float(value)), field_key),
    )
    conn.commit()


def test_ordinary_stat_notifications_debounce_and_accumulate(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_BOT_TOKEN", "test-token")
    sent = []
    monkeypatch.setattr(telegram_profile_notifications, "_send", lambda token, user_id, message: sent.append(message))

    with connect(db) as conn:
        before = capture_profile_change_state(conn, "char_darian")
        _set_number(conn, "raps_pa.strength", before["raps_pa.strength"]["value"] + 0.2)
        first = capture_profile_change_state(conn, "char_darian")
        assert telegram_profile_notifications.dispatch_profile_change_notifications(
            conn, actor_id="char_darian", before=before, current=first,
            sim_time="2025-05-06T01:00:00+00:00", now_wall=1000.0,
        ) == 1

        _set_number(conn, "raps_pa.strength", first["raps_pa.strength"]["value"] + 0.2)
        second = capture_profile_change_state(conn, "char_darian")
        assert telegram_profile_notifications.dispatch_profile_change_notifications(
            conn, actor_id="char_darian", before=first, current=second,
            sim_time="2025-05-06T01:10:00+00:00", now_wall=1100.0,
        ) == 0
        assert len(sent) == 1

        assert telegram_profile_notifications.dispatch_profile_change_notifications(
            conn, actor_id="char_darian", before=first, current=second,
            sim_time="2025-05-06T01:20:00+00:00", now_wall=1301.0,
        ) == 1
        assert len(sent) == 2
        assert "▲0.2" in sent[1]


def test_grade_transition_bypasses_debounce(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_BOT_TOKEN", "test-token")
    sent = []
    monkeypatch.setattr(telegram_profile_notifications, "_send", lambda token, user_id, message: sent.append(message))

    with connect(db) as conn:
        _set_number(conn, "raps_pa.strength", 89.7)
        before = capture_profile_change_state(conn, "char_darian")
        _set_number(conn, "raps_pa.strength", 89.9)
        first = capture_profile_change_state(conn, "char_darian")
        assert telegram_profile_notifications.dispatch_profile_change_notifications(
            conn, actor_id="char_darian", before=before, current=first,
            sim_time="2025-05-06T02:00:00+00:00", now_wall=2000.0,
        ) == 1

        _set_number(conn, "raps_pa.strength", 90.01)
        crossed = capture_profile_change_state(conn, "char_darian")
        assert telegram_profile_notifications.dispatch_profile_change_notifications(
            conn, actor_id="char_darian", before=first, current=crossed,
            sim_time="2025-05-06T02:01:00+00:00", now_wall=2010.0,
        ) == 1
        assert len(sent) == 2
        assert "A→S" in sent[1]

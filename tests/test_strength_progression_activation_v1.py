from datetime import datetime, timedelta, timezone
import json

from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.runtime import initialize
from observer_sandbox.strength_progression import SETTLEMENT_EVENT_TYPE
from observer_sandbox.strength_progression_activation import (
    maybe_settle_strength_progression,
    strength_progression_due,
)


def _healthy() -> dict:
    return {"energy": 75, "sleepiness": 25, "fatigue": 20}


def _stimulus(units: float = 1.0) -> dict:
    return {"training_stimulus": {"domain": "strength", "stimulus_units": units}}


def _settlement_count(conn) -> int:
    return conn.execute(
        "SELECT COUNT(*) FROM events WHERE actor_id=? AND event_type=?",
        ("char_darian", SETTLEMENT_EVENT_TYPE),
    ).fetchone()[0]


def test_activation_bootstraps_once_then_skips_same_and_short_boundaries(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        due = strength_progression_due(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy())
        assert due.due is True
        assert due.reason == "bootstrap"

        first = maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy())
        assert first["state"] == "settled"
        assert first["reason"] == "bootstrap"
        assert first["settlement"]["status"] == "bootstrapped"
        assert _settlement_count(conn) == 1

        same = maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy())
        assert same["state"] == "skipped"
        short = maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=(t0 + timedelta(hours=6)).isoformat(), state=_healthy())
        assert short["state"] == "skipped"
        assert _settlement_count(conn) == 1


def test_no_strength_history_does_not_create_daily_checkpoint_spam(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, 0, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy())
        for days in (1, 2, 5, 20):
            result = maybe_settle_strength_progression(
                conn,
                "char_darian",
                as_of_sim_time=(t0 + timedelta(days=days)).isoformat(),
                state=_healthy(),
            )
            assert result["state"] == "skipped"
        assert _settlement_count(conn) == 1


def test_strength_history_enables_at_most_daily_pure_detraining_checkpoint(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, 0, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(
            conn,
            sim_time=(t0 - timedelta(days=1)).isoformat(),
            actor_id="char_darian",
            event_type="action_completed",
            payload=_stimulus(),
        )
        conn.commit()
        maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy())
        assert _settlement_count(conn) == 1

        not_yet = strength_progression_due(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=23, minutes=59)).isoformat(),
            state=_healthy(),
        )
        assert not_yet.due is False

        due = strength_progression_due(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=24)).isoformat(),
            state=_healthy(),
        )
        assert due.due is True
        assert due.reason == "detraining_checkpoint"
        settled = maybe_settle_strength_progression(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=24)).isoformat(),
            state=_healthy(),
        )
        assert settled["state"] == "settled"
        assert _settlement_count(conn) == 2

        again = maybe_settle_strength_progression(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=25)).isoformat(),
            state=_healthy(),
        )
        assert again["state"] == "skipped"
        assert _settlement_count(conn) == 2


def test_eligible_unconsumed_stimulus_is_due_before_daily_checkpoint(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, 0, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy())
        stimulus_id = record_event(
            conn,
            sim_time=(t0 + timedelta(minutes=1)).isoformat(),
            actor_id="char_darian",
            event_type="action_completed",
            payload=_stimulus(),
        )
        conn.commit()

        due = strength_progression_due(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=48, minutes=1)).isoformat(),
            state=_healthy(),
        )
        assert due.due is True
        assert due.reason == "eligible_stimulus"
        assert due.eligible_stimulus_event_ids == (stimulus_id,)

        result = maybe_settle_strength_progression(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=48, minutes=1)).isoformat(),
            state=_healthy(),
        )
        assert result["settlement"]["status"] == "applied"
        assert stimulus_id in result["settlement"]["consumed_stimulus_event_ids"]
        assert 0 < result["settlement"]["positive_delta"] < 0.01


def test_fatigue_blocked_stimulus_remains_pending_until_recovery(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, 0, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        maybe_settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy())
        stimulus_id = record_event(
            conn,
            sim_time=(t0 + timedelta(minutes=1)).isoformat(),
            actor_id="char_darian",
            event_type="action_completed",
            payload=_stimulus(),
        )
        conn.commit()

        blocked_state = {"energy": 80, "sleepiness": 15, "fatigue": 70}
        blocked_due = strength_progression_due(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=48, minutes=1)).isoformat(),
            state=blocked_state,
        )
        # A 24h checkpoint may still be due for cursor/detraining, but the stimulus
        # itself must not be presented as eligible while recovery is hard-blocked.
        assert stimulus_id not in blocked_due.eligible_stimulus_event_ids
        maybe_settle_strength_progression(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=48, minutes=1)).isoformat(),
            state=blocked_state,
        )
        consumed = set()
        rows = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id=? AND event_type=?",
            ("char_darian", SETTLEMENT_EVENT_TYPE),
        ).fetchall()
        for row in rows:
            consumed.update(json.loads(row["payload_json"] or "{}").get("consumed_stimulus_event_ids") or [])
        assert stimulus_id not in consumed

        recovered_due = strength_progression_due(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=49)).isoformat(),
            state=_healthy(),
        )
        assert recovered_due.reason == "eligible_stimulus"
        assert stimulus_id in recovered_due.eligible_stimulus_event_ids

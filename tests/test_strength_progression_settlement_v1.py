from datetime import datetime, timedelta, timezone
import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.runtime import initialize
from observer_sandbox.strength_progression import (
    SETTLEMENT_EVENT_TYPE,
    integrated_detraining_time_factor_days,
    settle_strength_progression,
)


def _stimulus_payload(units: float = 1.0) -> dict:
    return {"training_stimulus": {"domain": "strength", "stimulus_units": units}}


def _strength(conn) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        ("char_darian", "raps_pa.strength"),
    ).fetchone()
    return float(json.loads(row["value_json"]))


def _healthy_state() -> dict:
    return {"energy": 75, "sleepiness": 25, "fatigue": 20}


def test_first_settlement_is_non_mutating_bootstrap_and_consumes_history(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 4, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        old_event = record_event(
            conn,
            sim_time=(now - timedelta(days=2)).isoformat(),
            actor_id="char_darian",
            event_type="action_completed",
            payload=_stimulus_payload(1.0),
        )
        conn.commit()
        before = _strength(conn)
        result = settle_strength_progression(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            state=_healthy_state(),
        )
        assert result["status"] == "bootstrapped"
        assert result["consumed_stimulus_event_ids"] == [old_event]
        assert result["net_delta"] == 0.0
        assert _strength(conn) == before == 90.0
        history = conn.execute("SELECT COUNT(*) FROM character_profile_history WHERE entity_id=? AND field_key=?", ("char_darian", "raps_pa.strength")).fetchone()[0]
        assert history == 0


def test_new_fully_recovered_stimulus_applies_tiny_decimal_gain_once(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy_state())
        stimulus_id = record_event(
            conn,
            sim_time=(t0 + timedelta(hours=1)).isoformat(),
            actor_id="char_darian",
            event_type="action_completed",
            payload=_stimulus_payload(1.0),
        )
        conn.commit()

        settle_time = t0 + timedelta(hours=49)
        applied = settle_strength_progression(
            conn,
            "char_darian",
            as_of_sim_time=settle_time.isoformat(),
            state=_healthy_state(),
        )
        assert applied["status"] == "applied"
        assert applied["consumed_stimulus_event_ids"] == [stimulus_id]
        assert applied["positive_delta"] > 0.0
        assert applied["positive_delta"] < 0.01
        assert applied["negative_delta"] == 0.0
        assert applied["new_strength"] > 90.0
        first_strength = _strength(conn)
        assert first_strength == pytest.approx(applied["new_strength"])

        replay = settle_strength_progression(
            conn,
            "char_darian",
            as_of_sim_time=settle_time.isoformat(),
            state=_healthy_state(),
        )
        assert replay["status"] == "no_change"
        assert replay["net_delta"] == 0.0
        assert _strength(conn) == first_strength

        history = conn.execute(
            "SELECT old_value_json,new_value_json,mode,authority FROM character_profile_history WHERE entity_id=? AND field_key=? ORDER BY id DESC LIMIT 1",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        assert history is not None
        assert history["mode"] == "simulated"
        assert history["authority"] == "strength-progression-settlement-v1"
        assert float(json.loads(history["new_value_json"])) > float(json.loads(history["old_value_json"]))


def test_unrecovered_or_fatigue_blocked_stimulus_is_not_consumed(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy_state())
        stimulus_id = record_event(conn, sim_time=(t0 + timedelta(hours=1)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_stimulus_payload())
        conn.commit()

        too_early = settle_strength_progression(conn, "char_darian", as_of_sim_time=(t0 + timedelta(hours=24)).isoformat(), state=_healthy_state())
        assert stimulus_id not in too_early["consumed_stimulus_event_ids"]
        assert _strength(conn) == 90.0

        blocked = settle_strength_progression(
            conn,
            "char_darian",
            as_of_sim_time=(t0 + timedelta(hours=72)).isoformat(),
            state={"energy": 80, "sleepiness": 15, "fatigue": 70},
        )
        assert stimulus_id not in blocked["consumed_stimulus_event_ids"]
        assert _strength(conn) == 90.0

        recovered = settle_strength_progression(conn, "char_darian", as_of_sim_time=(t0 + timedelta(hours=73)).isoformat(), state=_healthy_state())
        assert stimulus_id in recovered["consumed_stimulus_event_ids"]
        assert recovered["positive_delta"] > 0


def test_detraining_integral_resets_when_strength_training_occurs(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    start = datetime(2025, 5, 1, 0, 0, tzinfo=timezone.utc)
    end = start + timedelta(days=60)
    with connect(db) as conn:
        record_event(conn, sim_time=start.isoformat(), actor_id="char_darian", event_type="action_completed", payload=_stimulus_payload())
        conn.commit()
        no_reset = integrated_detraining_time_factor_days(conn, "char_darian", start_sim_time=start.isoformat(), end_sim_time=end.isoformat())
        record_event(conn, sim_time=(start + timedelta(days=40)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_stimulus_payload())
        conn.commit()
        with_reset = integrated_detraining_time_factor_days(conn, "char_darian", start_sim_time=start.isoformat(), end_sim_time=end.isoformat())
        assert no_reset > 0
        assert with_reset < no_reset


def test_prolonged_untrained_interval_applies_slow_negative_delta_once(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    training_time = datetime(2025, 5, 1, 0, 0, tzinfo=timezone.utc)
    bootstrap_time = training_time + timedelta(days=1)
    with connect(db) as conn:
        record_event(conn, sim_time=training_time.isoformat(), actor_id="char_darian", event_type="action_completed", payload=_stimulus_payload())
        conn.commit()
        settle_strength_progression(conn, "char_darian", as_of_sim_time=bootstrap_time.isoformat(), state=_healthy_state())
        before = _strength(conn)

        end = training_time + timedelta(days=74)
        result = settle_strength_progression(conn, "char_darian", as_of_sim_time=end.isoformat(), state=_healthy_state())
        assert result["status"] == "applied"
        assert result["positive_delta"] == 0.0
        assert result["integrated_detraining_time_factor_days"] > 0.0
        assert 0.0 < result["negative_delta"] < 1.0
        assert result["new_strength"] < before
        after = _strength(conn)

        replay = settle_strength_progression(conn, "char_darian", as_of_sim_time=end.isoformat(), state=_healthy_state())
        assert replay["status"] == "no_change"
        assert _strength(conn) == after


def test_settlement_event_is_auditable_even_when_cursor_advances_without_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, 0, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        settle_strength_progression(conn, "char_darian", as_of_sim_time=t0.isoformat(), state=_healthy_state())
        advanced = settle_strength_progression(conn, "char_darian", as_of_sim_time=(t0 + timedelta(hours=1)).isoformat(), state=_healthy_state())
        assert advanced["status"] == "advanced"
        assert advanced["net_delta"] == 0.0
        rows = conn.execute("SELECT payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id", ("char_darian", SETTLEMENT_EVENT_TYPE)).fetchall()
        assert len(rows) == 2
        payload = json.loads(rows[-1]["payload_json"])
        assert payload["stat_mutated"] is False
        assert payload["settled_through_sim_time"] == (t0 + timedelta(hours=1)).isoformat()

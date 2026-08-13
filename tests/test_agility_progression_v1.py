from datetime import datetime, timedelta, timezone

import pytest

from observer_sandbox.agility_progression import (
    AGILITY_FIELD_KEY,
    BASE_POSITIVE_SCALE,
    FULL_RECOVERY_HOURS,
    SETTLEMENT_SOURCE,
    STIMULUS_MINUTES_PER_UNIT,
    agility_level_factor,
    agility_saturation_factor,
    agility_stimulus_events,
    recent_agility_stimulus_units,
    settle_agility_progression,
)
from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.runtime import initialize


ACTOR = "char_darian"


def healthy():
    return {"energy": 90, "sleepiness": 10, "fatigue": 10}


def agility_payload(minutes=30.0):
    return {
        "action": "train",
        "training_method": {
            "method_id": "speed_agility_drills",
            "source": "training-method-semantics-v1",
            "workload_channels": ["conditioning", "movement"],
            "tags": ["interval", "coordination", "speed_agility"],
            "effective_load": {"effective_minutes": minutes},
        },
    }


def profile_value(conn, key):
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    import json
    return float(json.loads(row["value_json"]))


def test_agility_bootstrap_consumes_history_without_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    with connect(db) as conn:
        old_id = record_event(
            conn,
            sim_time=(t0 - timedelta(days=1)).isoformat(),
            actor_id=ACTOR,
            event_type="action_completed",
            payload=agility_payload(),
        )
        conn.commit()
        before = profile_value(conn, AGILITY_FIELD_KEY)
        result = settle_agility_progression(conn, ACTOR, as_of_sim_time=t0.isoformat(), state=healthy())
        assert result["status"] == "bootstrapped"
        assert old_id in result["consumed_stimulus_event_ids"]
        assert result["net_delta"] == 0.0
        assert profile_value(conn, AGILITY_FIELD_KEY) == before


def test_agility_realizes_after_20_hours_once(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    with connect(db) as conn:
        settle_agility_progression(conn, ACTOR, as_of_sim_time=t0.isoformat(), state=healthy())
        event_time = t0 + timedelta(minutes=1)
        event_id = record_event(
            conn,
            sim_time=event_time.isoformat(),
            actor_id=ACTOR,
            event_type="action_completed",
            payload=agility_payload(30.0),
        )
        conn.commit()
        before = profile_value(conn, AGILITY_FIELD_KEY)
        strength_before = profile_value(conn, "raps_pa.strength")
        stamina_before = profile_value(conn, "raps_pa.stamina")

        early = settle_agility_progression(
            conn,
            ACTOR,
            as_of_sim_time=(event_time + timedelta(hours=FULL_RECOVERY_HOURS - 1)).isoformat(),
            state=healthy(),
        )
        assert early["positive_delta"] == 0.0
        assert event_id not in early["consumed_stimulus_event_ids"]

        eligible_time = event_time + timedelta(hours=FULL_RECOVERY_HOURS)
        recent = recent_agility_stimulus_units(conn, ACTOR, as_of_sim_time=event_time.isoformat())
        expected = (
            BASE_POSITIVE_SCALE
            * (30.0 / STIMULUS_MINUTES_PER_UNIT)
            * agility_level_factor(before)
            * agility_saturation_factor(recent)
        )
        settled = settle_agility_progression(
            conn,
            ACTOR,
            as_of_sim_time=eligible_time.isoformat(),
            state=healthy(),
        )
        assert settled["positive_delta"] == pytest.approx(expected, abs=1e-8)
        assert settled["consumed_stimulus_event_ids"] == [event_id]
        assert settled["new_agility"] > before
        assert profile_value(conn, "raps_pa.strength") == strength_before
        assert profile_value(conn, "raps_pa.stamina") == stamina_before

        replay = settle_agility_progression(
            conn,
            ACTOR,
            as_of_sim_time=eligible_time.isoformat(),
            state=healthy(),
        )
        assert replay["status"] == "no_change"

        history = conn.execute(
            "SELECT authority,mode FROM character_profile_history WHERE entity_id=? AND field_key=? ORDER BY id DESC LIMIT 1",
            (ACTOR, AGILITY_FIELD_KEY),
        ).fetchone()
        assert history is not None
        assert history["authority"] == SETTLEMENT_SOURCE
        assert history["mode"] == "simulated"


def test_agility_requires_exact_authored_movement_contract(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    with connect(db) as conn:
        good_id = record_event(
            conn,
            sim_time=t0.isoformat(),
            actor_id=ACTOR,
            event_type="action_completed",
            payload=agility_payload(),
        )
        bad = agility_payload()
        bad["training_method"]["workload_channels"] = ["conditioning"]
        record_event(
            conn,
            sim_time=t0.isoformat(),
            actor_id=ACTOR,
            event_type="action_completed",
            payload=bad,
        )
        conn.commit()
        events = agility_stimulus_events(conn, ACTOR, as_of_sim_time=t0.isoformat())
        assert [event.event_id for event in events] == [good_id]


def test_high_fatigue_keeps_agility_stimulus_pending(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    t0 = datetime(2025, 5, 1, tzinfo=timezone.utc)
    with connect(db) as conn:
        settle_agility_progression(conn, ACTOR, as_of_sim_time=t0.isoformat(), state=healthy())
        event_time = t0 + timedelta(minutes=1)
        event_id = record_event(
            conn,
            sim_time=event_time.isoformat(),
            actor_id=ACTOR,
            event_type="action_completed",
            payload=agility_payload(),
        )
        conn.commit()
        result = settle_agility_progression(
            conn,
            ACTOR,
            as_of_sim_time=(event_time + timedelta(hours=21)).isoformat(),
            state={"energy": 90, "sleepiness": 10, "fatigue": 70},
        )
        assert result["positive_delta"] == 0.0
        assert event_id not in result["consumed_stimulus_event_ids"]

from datetime import datetime, timedelta, timezone

import pytest

from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.recovery_realization import (
    latest_strength_stimulus_sim_time,
    recovery_state_quality,
    recovery_time_factor,
    strength_recovery_realization_evidence,
)
from observer_sandbox.runtime import initialize


def _strength_payload(units: float = 1.0) -> dict:
    return {"training_stimulus": {"domain": "strength", "stimulus_units": units}}


def test_recovery_time_curve_is_zero_then_ramps_to_full():
    assert recovery_time_factor(0) == 0.0
    assert recovery_time_factor(6) == 0.0
    assert recovery_time_factor(27) == pytest.approx(0.5)
    assert recovery_time_factor(48) == 1.0
    assert recovery_time_factor(72) == 1.0


def test_state_quality_uses_energy_alertness_and_fatigue():
    quality, parts = recovery_state_quality({"energy": 75, "sleepiness": 25, "fatigue": 20})
    assert quality == 1.0
    assert parts == {"energy": 1.0, "alertness": 1.0, "fatigue_recovery": 1.0}

    degraded, _ = recovery_state_quality({"energy": 47.5, "sleepiness": 52.5, "fatigue": 45})
    assert degraded == pytest.approx(0.5)


def test_recovery_realization_uses_latest_strength_stimulus_by_sim_time(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 4, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        # Intentionally insert newer simulated event first and older event second.
        newer = (now - timedelta(hours=24)).isoformat()
        older = (now - timedelta(hours=60)).isoformat()
        record_event(conn, sim_time=newer, actor_id="char_darian", event_type="action_completed", payload=_strength_payload())
        record_event(conn, sim_time=older, actor_id="char_darian", event_type="action_completed", payload=_strength_payload())
        record_event(conn, sim_time=(now - timedelta(hours=2)).isoformat(), actor_id="char_darian", event_type="action_completed", payload={"training_stimulus": {"domain": "endurance", "stimulus_units": 9}})
        conn.commit()

        assert latest_strength_stimulus_sim_time(conn, "char_darian", as_of_sim_time=now.isoformat()) == newer
        evidence = strength_recovery_realization_evidence(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            state={"energy": 75, "sleepiness": 25, "fatigue": 20},
        )
        assert evidence.elapsed_hours == 24.0
        assert evidence.time_factor == pytest.approx(18 / 42)
        assert evidence.state_quality == 1.0
        assert evidence.recovery_factor == pytest.approx(18 / 42)


def test_high_fatigue_hard_blocks_realization_and_multiplier_is_abstract(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 4, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(conn, sim_time=(now - timedelta(hours=72)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload())
        conn.commit()

        blocked = strength_recovery_realization_evidence(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            state={"energy": 80, "sleepiness": 15, "fatigue": 70},
        )
        assert blocked.blocked is True
        assert blocked.recovery_factor == 0.0

        boosted = strength_recovery_realization_evidence(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            state={"energy": 60, "sleepiness": 35, "fatigue": 30},
            recovery_multiplier=1.2,
        )
        assert boosted.blocked is False
        assert 0.0 < boosted.recovery_factor <= 1.0


def test_no_strength_stimulus_means_no_recovery_realization(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        evidence = strength_recovery_realization_evidence(
            conn,
            "char_darian",
            as_of_sim_time="2025-05-04T12:00:00+00:00",
            state={"energy": 75, "sleepiness": 25, "fatigue": 20},
        )
        assert evidence.latest_stimulus_sim_time is None
        assert evidence.recovery_factor == 0.0

from datetime import datetime, timedelta, timezone

import pytest

from observer_sandbox.db import connect
from observer_sandbox.detraining_decay import (
    detraining_level_exposure,
    detraining_time_factor,
    strength_detraining_decay_evidence,
)
from observer_sandbox.event_log import record_event
from observer_sandbox.runtime import initialize


def _strength_payload(units: float = 1.0) -> dict:
    return {"training_stimulus": {"domain": "strength", "stimulus_units": units}}


def test_detraining_time_curve_has_14_day_grace_and_slow_asymptote():
    assert detraining_time_factor(0) == (0.0, 0.0)
    assert detraining_time_factor(14) == (0.0, 0.0)
    overdue, factor_30 = detraining_time_factor(30)
    assert overdue == 16.0
    assert 0.2 < factor_30 < 0.3
    _, factor_74 = detraining_time_factor(74)
    assert factor_74 == pytest.approx(1 - 2.718281828459045 ** -1, rel=1e-6)
    _, factor_180 = detraining_time_factor(180)
    assert factor_180 > factor_74
    assert factor_180 < 1.0


def test_high_level_stats_have_more_detraining_exposure():
    assert detraining_level_exposure(90) == pytest.approx(0.81)
    assert detraining_level_exposure(60) == pytest.approx(0.36)
    assert detraining_level_exposure(20) == pytest.approx(0.04)
    assert detraining_level_exposure(90) > detraining_level_exposure(60) > detraining_level_exposure(20)


def test_strength_decay_pressure_uses_elapsed_untrained_time_and_level(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 8, 1, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        last = (now - timedelta(days=74)).isoformat()
        record_event(conn, sim_time=last, actor_id="char_darian", event_type="action_completed", payload=_strength_payload())
        conn.commit()

        evidence = strength_detraining_decay_evidence(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            current_strength=90,
        )
        assert evidence.last_strength_stimulus_sim_time == last
        assert evidence.untrained_days == 74.0
        assert evidence.overdue_days == 60.0
        assert evidence.time_factor == pytest.approx(1 - 2.718281828459045 ** -1, rel=1e-6)
        assert evidence.level_exposure == pytest.approx(0.81)
        assert evidence.decay_pressure == pytest.approx(evidence.time_factor * 0.81, rel=1e-6)
        assert evidence.eligible is True


def test_grace_period_and_no_history_do_not_create_decay(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 20, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        no_history = strength_detraining_decay_evidence(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            current_strength=90,
        )
        assert no_history.eligible is False
        assert no_history.decay_pressure == 0.0

        record_event(conn, sim_time=(now - timedelta(days=10)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload())
        conn.commit()
        within_grace = strength_detraining_decay_evidence(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            current_strength=90,
        )
        assert within_grace.untrained_days == 10.0
        assert within_grace.eligible is False
        assert within_grace.decay_pressure == 0.0


def test_abstract_detraining_multiplier_is_bounded_and_non_mutating(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 8, 1, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(conn, sim_time=(now - timedelta(days=120)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload())
        conn.commit()
        before = conn.execute(
            "SELECT value_json,mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        base = strength_detraining_decay_evidence(conn, "char_darian", as_of_sim_time=now.isoformat(), current_strength=90)
        boosted = strength_detraining_decay_evidence(conn, "char_darian", as_of_sim_time=now.isoformat(), current_strength=90, detraining_multiplier=1.5)
        assert boosted.decay_pressure >= base.decay_pressure
        assert boosted.decay_pressure <= 1.0
        after = conn.execute(
            "SELECT value_json,mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        assert dict(after) == dict(before)

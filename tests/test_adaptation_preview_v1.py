from datetime import datetime, timedelta, timezone

import pytest

from observer_sandbox.adaptation_preview import strength_adaptation_preview
from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.runtime import initialize


def _strength_payload(units: float = 1.0) -> dict:
    return {"training_stimulus": {"domain": "strength", "stimulus_units": units}}


def test_recent_recovered_stimulus_produces_tiny_positive_delta_at_strength_90(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 4, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(conn, sim_time=(now - timedelta(hours=48)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload(1.0))
        conn.commit()
        before = conn.execute(
            "SELECT value_json,mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        preview = strength_adaptation_preview(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            current_strength=90,
            state={"energy": 75, "sleepiness": 25, "fatigue": 20},
        )
        assert preview.recent_stimulus_units == 1.0
        assert preview.level_factor == pytest.approx(0.01)
        assert preview.saturation_factor == pytest.approx(1 / 1.3)
        assert preview.recovery_factor == 1.0
        assert preview.positive_delta == pytest.approx(0.25 * 0.01 * (1 / 1.3), rel=1e-6)
        assert preview.negative_delta == 0.0
        assert preview.net_delta == preview.positive_delta
        after = conn.execute(
            "SELECT value_json,mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        assert dict(after) == dict(before)


def test_prolonged_untrained_state_produces_negative_daily_preview_only(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 8, 1, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(conn, sim_time=(now - timedelta(days=74)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload(1.0))
        conn.commit()
        preview = strength_adaptation_preview(
            conn,
            "char_darian",
            as_of_sim_time=now.isoformat(),
            current_strength=90,
            state={"energy": 75, "sleepiness": 25, "fatigue": 20},
        )
        assert preview.recent_stimulus_units == 0.0
        assert preview.positive_delta == 0.0
        assert preview.decay_pressure > 0.5
        assert preview.negative_delta == pytest.approx(0.02 * preview.decay_pressure, rel=1e-6)
        assert preview.net_delta == pytest.approx(-preview.negative_delta)


def test_high_level_gain_is_much_slower_than_low_level_gain(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 4, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(conn, sim_time=(now - timedelta(hours=48)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload(1.0))
        conn.commit()
        common = dict(conn=conn, actor_id="char_darian", as_of_sim_time=now.isoformat(), state={"energy": 75, "sleepiness": 25, "fatigue": 20})
        low = strength_adaptation_preview(current_strength=40, **common)
        high = strength_adaptation_preview(current_strength=90, **common)
        assert low.positive_delta > high.positive_delta * 30


def test_abstract_modifiers_are_factorized_and_preview_is_non_mutating(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 4, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(conn, sim_time=(now - timedelta(hours=48)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload(1.0))
        conn.commit()
        base = strength_adaptation_preview(conn, "char_darian", as_of_sim_time=now.isoformat(), current_strength=90, state={"energy": 75, "sleepiness": 25, "fatigue": 20})
        rate_boost = strength_adaptation_preview(conn, "char_darian", as_of_sim_time=now.isoformat(), current_strength=90, state={"energy": 75, "sleepiness": 25, "fatigue": 20}, adaptation_rate_multiplier=2.0)
        ceiling_boost = strength_adaptation_preview(conn, "char_darian", as_of_sim_time=now.isoformat(), current_strength=90, state={"energy": 75, "sleepiness": 25, "fatigue": 20}, ceiling_multiplier=1.05)
        assert rate_boost.positive_delta == pytest.approx(base.positive_delta * 2, rel=1e-6)
        assert ceiling_boost.level_factor > base.level_factor
        assert ceiling_boost.positive_delta > base.positive_delta


def test_no_history_means_zero_positive_and_negative_preview(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        preview = strength_adaptation_preview(
            conn,
            "char_darian",
            as_of_sim_time="2025-05-04T12:00:00+00:00",
            current_strength=90,
            state={"energy": 75, "sleepiness": 25, "fatigue": 20},
        )
        assert preview.positive_delta == 0.0
        assert preview.negative_delta == 0.0
        assert preview.net_delta == 0.0

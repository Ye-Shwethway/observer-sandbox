from datetime import datetime, timedelta, timezone

import pytest

from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.runtime import initialize
from observer_sandbox.stimulus_saturation import (
    recent_strength_stimulus_units,
    saturation_factor,
    strength_stimulus_saturation_evidence,
)


def _strength_payload(units: float) -> dict:
    return {
        "training_stimulus": {
            "domain": "strength",
            "target": "obj_thorne_estate_gym_free_weights",
            "effective_minutes": units * 60.0,
            "stimulus_units": units,
            "unit": "session_strength_stimulus",
            "source": "minimum-training-stimulus-v1",
        }
    }


def test_saturation_curve_reduces_marginal_yield():
    assert saturation_factor(0) == pytest.approx(1.0)
    assert saturation_factor(1) == pytest.approx(1 / 1.3)
    assert saturation_factor(2) == pytest.approx(1 / 1.6)
    assert saturation_factor(4) == pytest.approx(1 / 2.2)
    assert saturation_factor(8) < saturation_factor(4) < saturation_factor(2) < saturation_factor(1)


def test_recent_strength_stimulus_uses_72h_event_window_and_ignores_other_domains(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 4, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(conn, sim_time=(now - timedelta(hours=12)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload(1.0))
        record_event(conn, sim_time=(now - timedelta(hours=48)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload(0.5))
        record_event(conn, sim_time=(now - timedelta(hours=80)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload(10.0))
        record_event(
            conn,
            sim_time=(now - timedelta(hours=6)).isoformat(),
            actor_id="char_darian",
            event_type="action_completed",
            payload={"training_stimulus": {"domain": "endurance", "stimulus_units": 5.0}},
        )
        conn.commit()

        assert recent_strength_stimulus_units(conn, "char_darian", as_of_sim_time=now.isoformat()) == pytest.approx(1.5)
        evidence = strength_stimulus_saturation_evidence(conn, "char_darian", as_of_sim_time=now.isoformat())
        assert evidence.recent_stimulus_units == pytest.approx(1.5)
        assert evidence.window_hours == 72.0
        assert evidence.alpha == 0.3
        assert evidence.saturation_factor == pytest.approx(1 / (1 + 0.3 * 1.5))


def test_saturation_query_does_not_mutate_strength_or_events(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    now = datetime(2025, 5, 2, 12, 0, tzinfo=timezone.utc)
    with connect(db) as conn:
        record_event(conn, sim_time=(now - timedelta(hours=2)).isoformat(), actor_id="char_darian", event_type="action_completed", payload=_strength_payload(1.0))
        conn.commit()
        before_strength = conn.execute(
            "SELECT value_json,mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        before_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

        evidence = strength_stimulus_saturation_evidence(conn, "char_darian", as_of_sim_time=now.isoformat())
        assert evidence.saturation_factor < 1.0

        after_strength = conn.execute(
            "SELECT value_json,mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        after_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        assert dict(after_strength) == dict(before_strength)
        assert after_count == before_count


def test_invalid_saturation_inputs_rejected():
    with pytest.raises(ValueError):
        saturation_factor(-0.01)
    with pytest.raises(ValueError):
        saturation_factor(1.0, alpha=-0.1)

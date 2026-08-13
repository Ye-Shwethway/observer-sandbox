from __future__ import annotations

import json
from datetime import datetime, timedelta

import pytest

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, ensure_sim_clock
from observer_sandbox.stamina_progression import (
    BASE_POSITIVE_SCALE,
    FULL_RECOVERY_HOURS,
    SETTLEMENT_SOURCE,
    STAMINA_FIELD_KEY,
    recent_stamina_stimulus_units,
    settle_stamina_progression,
    stamina_level_factor,
    stamina_saturation_factor,
    stamina_stimulus_events,
)
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
TREADMILL = "obj_thorne_estate_gym_high_speed_treadmill"


def _profile_value(conn, field_key: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key=?",
        (field_key,),
    ).fetchone()
    assert row is not None
    return float(json.loads(row[0]))


def _state(conn) -> dict[str, float]:
    return {
        "energy": 90.0,
        "sleepiness": 10.0,
        "fatigue": 10.0,
    }


def _prepare_treadmill(conn) -> None:
    set_field(conn, "char_darian", "runtime.location", HOME_GYM)
    set_field(conn, "char_darian", "needs.energy", 90.0)
    set_field(conn, "char_darian", "needs.sleepiness", 10.0)
    set_field(conn, "char_darian", "physiology.fatigue", 0.0, authority="physiology_engine", source="stamina-test")
    conn.commit()


def test_stamina_bootstrap_is_non_mutating_and_consumes_only_history(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        now = ensure_sim_clock(conn).isoformat()
        before = _profile_value(conn, STAMINA_FIELD_KEY)
        result = settle_stamina_progression(conn, "char_darian", as_of_sim_time=now, state=_state(conn))
        assert result["status"] == "bootstrapped"
        assert result["old_stamina"] == before
        assert result["new_stamina"] == before
        assert result["consumed_stimulus_event_ids"] == []
        assert _profile_value(conn, STAMINA_FIELD_KEY) == before


def test_treadmill_stimulus_realizes_after_30_hours_once(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        start = ensure_sim_clock(conn)
        settle_stamina_progression(conn, "char_darian", as_of_sim_time=start.isoformat(), state=_state(conn))
        _prepare_treadmill(conn)
        strength_before = _profile_value(conn, "raps_pa.strength")
        stamina_before = _profile_value(conn, STAMINA_FIELD_KEY)

        apply_action(conn, Action("train", 45, TREADMILL, "steady conditioning"))
        stimuli = stamina_stimulus_events(conn, "char_darian", as_of_sim_time=(start + timedelta(hours=1)).isoformat())
        assert len(stimuli) == 1
        stimulus = stimuli[0]
        assert stimulus.stimulus_units > 0

        too_early = settle_stamina_progression(
            conn,
            "char_darian",
            as_of_sim_time=(datetime.fromisoformat(stimulus.sim_time) + timedelta(hours=FULL_RECOVERY_HOURS - 1)).isoformat(),
            state=_state(conn),
        )
        assert too_early["positive_delta"] == 0.0
        assert _profile_value(conn, STAMINA_FIELD_KEY) == stamina_before

        eligible_time = datetime.fromisoformat(stimulus.sim_time) + timedelta(hours=FULL_RECOVERY_HOURS)
        recent = recent_stamina_stimulus_units(conn, "char_darian", as_of_sim_time=stimulus.sim_time)
        expected = (
            BASE_POSITIVE_SCALE
            * stimulus.stimulus_units
            * stamina_level_factor(stamina_before)
            * stamina_saturation_factor(recent)
        )
        settled = settle_stamina_progression(
            conn,
            "char_darian",
            as_of_sim_time=eligible_time.isoformat(),
            state=_state(conn),
        )
        assert settled["positive_delta"] == pytest.approx(expected, abs=1e-8)
        assert settled["new_stamina"] > stamina_before
        assert settled["consumed_stimulus_event_ids"] == [stimulus.event_id]
        assert _profile_value(conn, "raps_pa.strength") == strength_before

        replay = settle_stamina_progression(
            conn,
            "char_darian",
            as_of_sim_time=eligible_time.isoformat(),
            state=_state(conn),
        )
        assert replay["status"] == "no_change"
        assert replay["net_delta"] == 0.0

        history = conn.execute(
            "SELECT mode,authority FROM character_profile_history WHERE entity_id='char_darian' AND field_key=? ORDER BY id DESC LIMIT 1",
            (STAMINA_FIELD_KEY,),
        ).fetchone()
        assert history is not None
        assert history["mode"] == "simulated"
        assert history["authority"] == SETTLEMENT_SOURCE


def test_high_fatigue_keeps_recovered_stimulus_pending(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        start = ensure_sim_clock(conn)
        settle_stamina_progression(conn, "char_darian", as_of_sim_time=start.isoformat(), state=_state(conn))
        _prepare_treadmill(conn)
        apply_action(conn, Action("train", 45, TREADMILL, "steady conditioning"))
        stimulus = stamina_stimulus_events(conn, "char_darian", as_of_sim_time=(start + timedelta(hours=1)).isoformat())[0]
        stamina_before = _profile_value(conn, STAMINA_FIELD_KEY)
        blocked_state = {"energy": 90.0, "sleepiness": 10.0, "fatigue": 75.0}
        result = settle_stamina_progression(
            conn,
            "char_darian",
            as_of_sim_time=(datetime.fromisoformat(stimulus.sim_time) + timedelta(hours=31)).isoformat(),
            state=blocked_state,
        )
        assert result["positive_delta"] == 0.0
        assert result["consumed_stimulus_event_ids"] == []
        assert _profile_value(conn, STAMINA_FIELD_KEY) == stamina_before

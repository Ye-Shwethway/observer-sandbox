import json
from datetime import datetime, timedelta

from observer_sandbox.body_measurement_progression import (
    _project_field,
    _regional_detraining_state,
    load_body_measurement_policy,
    maybe_settle_body_measurements,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot

ACTOR = "char_darian"


def _insert_movement_training(conn, start: datetime, *, regional_load: dict[str, float], minutes: float = 60.0) -> None:
    end = start + timedelta(minutes=minutes)
    payload = {
        "action": "train",
        "duration_minutes": minutes,
        "action_started_sim_time": start.isoformat(),
        "action_ended_sim_time": end.isoformat(),
        "training_method": {
            "source": "training-method-semantics-v1",
            "method_id": "free_weight_strength",
            "family": "resistance",
            "workload_channels": ["resistance"],
            "effective_load": {"effective_minutes": minutes},
            "movement_anatomy": {
                "movement_ids": ["synthetic_test_pattern"],
                "regional_load": regional_load,
                "source": "training-anatomy-v1",
            },
        },
    }
    conn.execute(
        "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
        (end.isoformat(), ACTOR, "action_completed", json.dumps(payload)),
    )


def test_regional_detraining_has_grace_then_ramps_without_training(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        activation = datetime.fromisoformat(state["sim_time"])
        maybe_settle_body_measurements(conn, ACTOR, as_of_sim_time=activation.isoformat(), state=state)
        before_grace = _regional_detraining_state(
            conn,
            ACTOR,
            activation_sim_time=activation.isoformat(),
            end_sim_time=(activation + timedelta(days=20)).isoformat(),
        )
        after_grace = _regional_detraining_state(
            conn,
            ACTOR,
            activation_sim_time=activation.isoformat(),
            end_sim_time=(activation + timedelta(days=42)).isoformat(),
        )

    assert before_grace["biceps"]["pressure"] == 0.0
    assert before_grace["thighs"]["pressure"] == 0.0
    assert 0.0 < after_grace["biceps"]["pressure"] < 1.0
    assert after_grace["biceps"]["last_qualifying_exposure_sim_time"] is None


def test_recent_regional_training_resets_only_qualifying_regions(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        activation = datetime.fromisoformat(state["sim_time"])
        maybe_settle_body_measurements(conn, ACTOR, as_of_sim_time=activation.isoformat(), state=state)
        _insert_movement_training(
            conn,
            activation + timedelta(days=35),
            regional_load={"chest": 1.0, "triceps": 0.8, "shoulders": 0.6},
        )
        conn.commit()
        result = _regional_detraining_state(
            conn,
            ACTOR,
            activation_sim_time=activation.isoformat(),
            end_sim_time=(activation + timedelta(days=42)).isoformat(),
        )

    assert result["chest"]["pressure"] == 0.0
    assert result["triceps"]["pressure"] == 0.0
    assert result["chest"]["last_qualifying_exposure_sim_time"] is not None
    assert result["calves"]["pressure"] > 0.0
    assert result["calves"]["last_qualifying_exposure_sim_time"] is None


def test_detraining_only_erodes_post_activation_excess_and_never_authored_baseline():
    cfg = load_body_measurement_policy()["fields"]["body.biceps_flexed_in"]
    projected, detail = _project_field(
        current=18.0,
        cfg=cfg,
        global_ffm_headroom_lb=20.0,
        partition_ffm_delta_lb=0.0,
        rt_ffm_gain_lb=0.0,
        fm_delta_lb=0.0,
        old_fm_lb=20.0,
        region_exposure=0.0,
        detraining_pressure=1.0,
        settlement_days=1.0,
        genetic_max=19.0,
        waist_target=None,
        activation_value=17.5,
    )
    baseline_projected, baseline_detail = _project_field(
        current=17.5,
        cfg=cfg,
        global_ffm_headroom_lb=20.0,
        partition_ffm_delta_lb=0.0,
        rt_ffm_gain_lb=0.0,
        fm_delta_lb=0.0,
        old_fm_lb=20.0,
        region_exposure=0.0,
        detraining_pressure=1.0,
        settlement_days=1.0,
        genetic_max=19.0,
        waist_target=None,
        activation_value=17.5,
    )

    assert 17.5 <= projected < 18.0
    assert detail["regional_detraining_delta_in"] < 0.0
    assert baseline_projected == 17.5
    assert baseline_detail["regional_detraining_delta_in"] == 0.0


def test_systemic_ffm_loss_suppresses_extra_regional_detraining_double_count():
    cfg = load_body_measurement_policy()["fields"]["body.biceps_flexed_in"]
    projected, detail = _project_field(
        current=18.0,
        cfg=cfg,
        global_ffm_headroom_lb=20.0,
        partition_ffm_delta_lb=-0.5,
        rt_ffm_gain_lb=0.0,
        fm_delta_lb=0.0,
        old_fm_lb=20.0,
        region_exposure=0.0,
        detraining_pressure=1.0,
        settlement_days=1.0,
        genetic_max=19.0,
        waist_target=None,
        activation_value=17.5,
    )

    assert projected < 18.0
    assert detail["lean_loss_delta_in"] < 0.0
    assert detail["regional_detraining_delta_in"] == 0.0

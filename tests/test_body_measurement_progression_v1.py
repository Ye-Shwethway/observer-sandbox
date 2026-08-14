import json
from datetime import datetime, timedelta

from observer_sandbox.body_measurement_progression import (
    body_measurement_snapshot,
    maybe_settle_body_measurements,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot

ACTOR = "char_darian"


def _insert_bc2(conn, start: datetime, end: datetime, *, rt_gain: float = 0.20, partition_ffm: float = 0.05, fm_delta: float = -0.08):
    old = {
        "weight_lb": 215.0,
        "body_fat_pct": 9.0,
        "fat_mass_lb": 19.35,
        "lean_mass_lb": 195.65,
        "bmi": 26.167763,
    }
    new_fm = old["fat_mass_lb"] + fm_delta
    new_ffm = old["lean_mass_lb"] + partition_ffm + rt_gain
    new_weight = new_fm + new_ffm
    payload = {
        "source": "body-composition-progression-v1",
        "status": "applied",
        "settled_from_sim_time": start.isoformat(),
        "settled_through_sim_time": end.isoformat(),
        "old": old,
        "new": {
            "weight_lb": new_weight,
            "body_fat_pct": 100.0 * new_fm / new_weight,
            "fat_mass_lb": new_fm,
            "lean_mass_lb": new_ffm,
            "bmi": 703.0 * new_weight / (76.0 * 76.0),
        },
        "partition": {
            "partition_delta_ffm_lb": partition_ffm,
            "partition_delta_fm_lb": fm_delta,
        },
        "rt_recomposition": {
            "rt_ffm_gain_lb": rt_gain,
            "rt_fm_energy_cost_lb": 0.0,
        },
        "stat_mutated": True,
    }
    cur = conn.execute(
        "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
        (end.isoformat(), ACTOR, "body_composition_progression_settled", json.dumps(payload)),
    )
    return int(cur.lastrowid)


def _insert_bench_training(conn, start: datetime, *, minutes: float = 60.0):
    end = start + timedelta(minutes=minutes)
    payload = {
        "action": "train",
        "duration_minutes": minutes,
        "action_started_sim_time": start.isoformat(),
        "action_ended_sim_time": end.isoformat(),
        "training_method": {
            "source": "training-method-semantics-v1",
            "method_id": "bench_resistance_work",
            "family": "resistance",
            "workload_channels": ["resistance"],
            "effective_load": {"effective_minutes": minutes},
        },
    }
    conn.execute(
        "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
        (end.isoformat(), ACTOR, "action_completed", json.dumps(payload)),
    )


def test_bc3_activation_preserves_authored_values_and_does_not_invent_hips(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        before = body_measurement_snapshot(conn, ACTOR)
        result = maybe_settle_body_measurements(conn, ACTOR, as_of_sim_time=state["sim_time"], state=state)
        after = body_measurement_snapshot(conn, ACTOR)
        rows = conn.execute(
            "SELECT field_key,mode,authority FROM character_profile_values WHERE entity_id=? AND field_key LIKE 'body.%_in' ORDER BY field_key",
            (ACTOR,),
        ).fetchall()
        hip = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key='body.hips_in'",
            (ACTOR,),
        ).fetchone()

    assert result["status"] == "bootstrapped"
    assert before == after
    assert "body.hips_in" in result["deferred_fields"]
    assert hip is None
    activated = set(result["activated_measurements"])
    assert activated == set(before)
    assert all(row["mode"] == "simulated" and row["authority"] == "body_progression_engine" for row in rows if row["field_key"] in activated)


def test_bc3_defers_partial_pre_activation_bc2_window_without_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        activation = datetime.fromisoformat(state["sim_time"])
        before = body_measurement_snapshot(conn, ACTOR)
        maybe_settle_body_measurements(conn, ACTOR, as_of_sim_time=activation.isoformat(), state=state)
        _insert_bc2(conn, activation - timedelta(hours=12), activation + timedelta(hours=12))
        conn.commit()
        result = maybe_settle_body_measurements(
            conn,
            ACTOR,
            as_of_sim_time=(activation + timedelta(hours=12)).isoformat(),
            state=state,
        )
        after = body_measurement_snapshot(conn, ACTOR)

    assert result["status"] == "deferred_partial_pre_activation_window"
    assert after == before


def test_bc3_full_window_uses_regional_resistance_and_body_composition_signals(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        activation = datetime.fromisoformat(state["sim_time"])
        maybe_settle_body_measurements(conn, ACTOR, as_of_sim_time=activation.isoformat(), state=state)
        before = body_measurement_snapshot(conn, ACTOR)
        start = activation
        end = activation + timedelta(hours=24)
        _insert_bench_training(conn, activation + timedelta(hours=8))
        bc2_id = _insert_bc2(conn, start, end)
        conn.commit()
        result = maybe_settle_body_measurements(conn, ACTOR, as_of_sim_time=end.isoformat(), state=state)
        after = body_measurement_snapshot(conn, ACTOR)
        event = conn.execute(
            "SELECT caused_by_event_id,payload_json,state_changes_json FROM events WHERE actor_id=? AND event_type='body_measurement_progression_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        payload = json.loads(event["payload_json"])
        changes = json.loads(event["state_changes_json"])

    assert result["status"] == "applied"
    assert event["caused_by_event_id"] == bc2_id
    assert payload["regional_training_exposure"]["chest"] == 1.0
    assert payload["regional_training_exposure"]["triceps"] == 1.0
    assert payload["regional_training_exposure"].get("calves", 0.0) == 0.0
    assert after["body.chest_in"] > before["body.chest_in"]
    assert after["body.triceps_in"] > before["body.triceps_in"]
    assert after["body.calves_in"] <= before["body.calves_in"]
    assert after["body.waist_in"] < before["body.waist_in"]
    assert "body.hips_in" in payload["deferred_fields"]
    assert "body.hips_in" not in after
    for key, change in changes.items():
        assert abs(float(change["delta"])) <= 0.1500001
        assert key in after


def test_bc3_profile_history_and_event_are_atomic_for_batched_fields(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        activation = datetime.fromisoformat(state["sim_time"])
        maybe_settle_body_measurements(conn, ACTOR, as_of_sim_time=activation.isoformat(), state=state)
        before_history = conn.execute(
            "SELECT COUNT(*) FROM character_profile_history WHERE entity_id=? AND authority='body_progression_engine'",
            (ACTOR,),
        ).fetchone()[0]
        _insert_bench_training(conn, activation + timedelta(hours=4))
        _insert_bc2(conn, activation, activation + timedelta(hours=24))
        conn.commit()
        result = maybe_settle_body_measurements(
            conn,
            ACTOR,
            as_of_sim_time=(activation + timedelta(hours=24)).isoformat(),
            state=state,
        )
        after_history = conn.execute(
            "SELECT COUNT(*) FROM character_profile_history WHERE entity_id=? AND authority='body_progression_engine'",
            (ACTOR,),
        ).fetchone()[0]
        event = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id=? AND event_type='body_measurement_progression_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        payload = json.loads(event["payload_json"])

    assert result["status"] == "applied"
    assert after_history == before_history + len(result["changes"])
    assert payload["stat_mutated"] is True
    assert payload["source"] == "body-measurement-progression-v1"

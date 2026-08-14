import json
from datetime import datetime, timedelta

from observer_sandbox.body_composition_progression import body_composition_snapshot, maybe_settle_body_composition
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot

ACTOR = "char_darian"


def _profile_row(conn, key):
    return conn.execute(
        "SELECT value_json,mode,authority FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, key),
    ).fetchone()


def _insert_hour(conn, start: datetime, index: int, *, train: bool = False, eat: bool = False, resistance: bool = True):
    action_start = start + timedelta(hours=index)
    action_end = action_start + timedelta(hours=1)
    payload = {
        "action": "train" if train else ("eat" if eat else "idle"),
        "duration_minutes": 60,
        "action_started_sim_time": action_start.isoformat(),
        "action_ended_sim_time": action_end.isoformat(),
        "energy_expenditure": {"estimated_kcal": 420.0 if train else 95.0},
    }
    if eat:
        payload["nutrition_intake"] = {
            "energy_kcal": 650.0,
            "protein_g": 48.0,
            "carbohydrate_g": 70.0,
            "fat_g": 20.0,
            "source": "eating-behavior-v1",
        }
    if train:
        payload["training_method"] = {
            "source": "training-method-semantics-v1",
            "method_id": "free_weight_strength" if resistance else "steady_state_cardio",
            "family": "resistance" if resistance else "conditioning",
            "workload_channels": ["resistance"] if resistance else ["conditioning"],
            "effective_load": {"effective_minutes": 60.0},
        }
    conn.execute(
        "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
        (action_end.isoformat(), ACTOR, "action_completed", json.dumps(payload)),
    )


def test_bc2_bootstrap_preserves_values_and_activates_coupled_fields(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        before = body_composition_snapshot(conn, ACTOR)
        result = maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=state["sim_time"], state=state)
        after = body_composition_snapshot(conn, ACTOR)
        weight = _profile_row(conn, "body.weight_lb")
        bf = _profile_row(conn, "body.body_fat_pct")
        history = conn.execute(
            "SELECT field_key,old_value_json,new_value_json FROM character_profile_history WHERE entity_id=? AND field_key IN ('body.weight_lb','body.body_fat_pct') ORDER BY id DESC LIMIT 2",
            (ACTOR,),
        ).fetchall()

    assert result["status"] == "bootstrapped"
    assert after == before
    assert weight["mode"] == "simulated" and weight["authority"] == "physiology_engine"
    assert bf["mode"] == "simulated" and bf["authority"] == "physiology_engine"
    assert len(history) == 2
    assert all(json.loads(row["old_value_json"]) == json.loads(row["new_value_json"]) for row in history)


def test_bc2_complete_daily_window_mutates_weight_and_bf_atomically_and_bounded(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        base_state = snapshot(conn, ACTOR)
        base = datetime.fromisoformat(base_state["sim_time"])
        assert maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=base.isoformat(), state=base_state)["status"] == "bootstrapped"
        before = body_composition_snapshot(conn, ACTOR)
        for hour in range(24):
            _insert_hour(conn, base, hour, train=(hour == 8), eat=(hour in {2, 7, 13, 19}))
        conn.commit()
        end = base + timedelta(hours=24)
        state = dict(base_state)
        state.update({"sim_time": end.isoformat(), "fatigue": 12.0, "energy": 78.0, "hunger": 35.0, "sleepiness": 18.0, "thirst": 20.0})
        result = maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=end.isoformat(), state=state)
        after = body_composition_snapshot(conn, ACTOR)
        event = conn.execute(
            "SELECT payload_json,state_changes_json FROM events WHERE actor_id=? AND event_type='body_composition_progression_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        payload, changes = json.loads(event["payload_json"]), json.loads(event["state_changes_json"])

    assert result["status"] == "applied"
    assert abs(after["weight_lb"] - before["weight_lb"]) <= 0.55
    assert abs(after["weight_lb"] - after["lean_mass_lb"] - after["fat_mass_lb"]) < 1e-5
    assert abs(after["body_fat_pct"] - 100.0 * after["fat_mass_lb"] / after["weight_lb"]) < 1e-4
    assert payload["energy_balance"]["complete"] is True
    assert payload["resistance_training_effective_minutes"] == 60.0
    assert payload["partition"]["forbes_ffm_share"] > 0.0
    assert payload["rt_recomposition"]["protein_factor"] > 0.0
    assert payload["rt_recomposition"]["training_factor"] == 1.0
    assert "body.weight_lb" in changes and "body.body_fat_pct" in changes


def test_bc2_non_resistance_training_does_not_create_hypertrophy_signal(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        base_state = snapshot(conn, ACTOR)
        base = datetime.fromisoformat(base_state["sim_time"])
        maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=base.isoformat(), state=base_state)
        for hour in range(24):
            _insert_hour(conn, base, hour, train=(hour == 8), resistance=False, eat=(hour in {2, 7, 13, 19}))
        conn.commit()
        end = base + timedelta(hours=24)
        state = dict(base_state)
        state.update({"sim_time": end.isoformat(), "fatigue": 10.0, "energy": 80.0})
        maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=end.isoformat(), state=state)
        row = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id=? AND event_type='body_composition_progression_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        payload = json.loads(row["payload_json"])

    assert payload["resistance_training_effective_minutes"] == 0.0
    assert payload["rt_recomposition"]["training_factor"] == 0.0
    assert payload["rt_recomposition"]["rt_ffm_gain_lb"] == 0.0


def test_bc2_incomplete_window_advances_cursor_without_body_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        base_state = snapshot(conn, ACTOR)
        base = datetime.fromisoformat(base_state["sim_time"])
        maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=base.isoformat(), state=base_state)
        before = body_composition_snapshot(conn, ACTOR)
        _insert_hour(conn, base, 0, eat=True)
        conn.commit()
        end = base + timedelta(hours=24)
        state = dict(base_state)
        state["sim_time"] = end.isoformat()
        result = maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=end.isoformat(), state=state)
        after = body_composition_snapshot(conn, ACTOR)

    assert result["status"] == "deferred_incomplete_evidence"
    assert after == before
    assert result["settled_through_sim_time"] == end.isoformat()

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from observer_sandbox.body_measurement_progression import (
    body_measurement_snapshot,
    maybe_settle_body_measurements,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot

ACTOR = "char_darian"


def _insert_training(conn, start: datetime, method_id: str, weights_case: str) -> None:
    end = start + timedelta(minutes=60)
    payload = {
        "action": "train",
        "duration_minutes": 60,
        "action_started_sim_time": start.isoformat(),
        "action_ended_sim_time": end.isoformat(),
        "training_method": {
            "source": "training-method-semantics-v1",
            "method_id": method_id,
            "family": "resistance",
            "workload_channels": ["resistance"],
            "effective_load": {"effective_minutes": 60.0},
            "validation_case": weights_case,
        },
    }
    conn.execute(
        "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
        (end.isoformat(), ACTOR, "action_completed", json.dumps(payload)),
    )


def _insert_bc2(conn, start: datetime, end: datetime, *, fm_delta: float, partition_ffm: float, rt_ffm: float) -> int:
    old = {
        "weight_lb": 215.0,
        "body_fat_pct": 9.0,
        "fat_mass_lb": 19.35,
        "lean_mass_lb": 195.65,
        "bmi": 26.167763,
    }
    new_fm = old["fat_mass_lb"] + fm_delta
    new_ffm = old["lean_mass_lb"] + partition_ffm + rt_ffm
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
            "rt_ffm_gain_lb": rt_ffm,
            "rt_fm_energy_cost_lb": 0.0,
        },
        "stat_mutated": True,
        "validation_case": True,
    }
    cur = conn.execute(
        "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
        (end.isoformat(), ACTOR, "body_composition_progression_settled", json.dumps(payload)),
    )
    return int(cur.lastrowid)


def _latest_bc3(conn):
    return conn.execute(
        "SELECT sim_time,payload_json FROM events WHERE actor_id=? AND event_type='body_measurement_progression_settled' ORDER BY id DESC LIMIT 1",
        (ACTOR,),
    ).fetchone()


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    # Exercise the real candidate upgrade path on the disposable production copy.
    # Re-initialization adds newly authored canonical/static fields while the seed
    # importer preserves already simulated engine-owned values.
    initialize(db_path)

    with connect(db_path) as conn:
        live_state = snapshot(conn, ACTOR)
        live_time = datetime.fromisoformat(str(live_state["sim_time"]))
        before = body_measurement_snapshot(conn, ACTOR)
        before_history = conn.execute(
            "SELECT COUNT(*) FROM character_profile_history WHERE entity_id=? AND authority='body_progression_engine'",
            (ACTOR,),
        ).fetchone()[0]

        existing = _latest_bc3(conn)
        bootstrap_history_count = 0
        partial_pre_activation_window_deferred = False
        if existing is None:
            activation = live_time
            bootstrap = maybe_settle_body_measurements(
                conn,
                ACTOR,
                as_of_sim_time=activation.isoformat(),
                state=live_state,
            )
            assert bootstrap["status"] == "bootstrapped"
            assert body_measurement_snapshot(conn, ACTOR) == before
            assert "body.hips_in" not in bootstrap["deferred_fields"]
            activated_fields = sorted(bootstrap["activated_measurements"])
            bootstrap_history_count = len(activated_fields)

            partial_end = activation + timedelta(hours=12)
            _insert_bc2(
                conn,
                activation - timedelta(hours=12),
                partial_end,
                fm_delta=-0.02,
                partition_ffm=0.02,
                rt_ffm=0.05,
            )
            conn.commit()
            partial = maybe_settle_body_measurements(
                conn,
                ACTOR,
                as_of_sim_time=partial_end.isoformat(),
                state=live_state,
            )
            assert partial["status"] == "deferred_partial_pre_activation_window"
            assert body_measurement_snapshot(conn, ACTOR) == before
            partial_pre_activation_window_deferred = True
            full_start = partial_end
        else:
            existing_payload = json.loads(existing["payload_json"] or "{}")
            activation_raw = existing_payload.get("activation_sim_time") or existing["sim_time"]
            activation = datetime.fromisoformat(str(activation_raw))
            activated_fields = sorted(before)
            # Production may naturally advance between validation runs. The
            # acceptance must validate the candidate against either state rather
            # than requiring a one-time bootstrap event forever.
            catch_up = maybe_settle_body_measurements(
                conn,
                ACTOR,
                as_of_sim_time=live_time.isoformat(),
                state=live_state,
            )
            assert catch_up["status"] in {"not_due", "advanced", "applied", "deferred_partial_pre_activation_window", "deferred_incomplete_body_composition_evidence"}
            latest = _latest_bc3(conn)
            latest_payload = json.loads(latest["payload_json"] or "{}")
            cursor_raw = latest_payload.get("settled_through_sim_time") or latest["sim_time"]
            full_start = max(live_time, datetime.fromisoformat(str(cursor_raw))) + timedelta(minutes=1)

        hip = conn.execute(
            "SELECT value_json,mode,authority FROM character_profile_values WHERE entity_id=? AND field_key='body.hips_in'",
            (ACTOR,),
        ).fetchone()
        assert hip is not None
        assert json.loads(hip["value_json"]) == 39.0
        assert hip["mode"] == "simulated"
        assert hip["authority"] == "body_progression_engine"

        modes = conn.execute(
            "SELECT field_key,mode,authority FROM character_profile_values WHERE entity_id=? AND authority='body_progression_engine' ORDER BY field_key",
            (ACTOR,),
        ).fetchall()
        assert activated_fields
        assert "body.hips_in" in activated_fields
        assert all(
            row["mode"] == "simulated" and row["authority"] == "body_progression_engine"
            for row in modes if row["field_key"] in set(activated_fields)
        )

        baseline = body_measurement_snapshot(conn, ACTOR)
        history_before_applied = conn.execute(
            "SELECT COUNT(*) FROM character_profile_history WHERE entity_id=? AND authority='body_progression_engine'",
            (ACTOR,),
        ).fetchone()[0]
        full_end = full_start + timedelta(hours=24)
        _insert_training(conn, full_start + timedelta(hours=8), "bench_resistance_work", "upper_body")
        bc2_id = _insert_bc2(
            conn,
            full_start,
            full_end,
            fm_delta=-0.08,
            partition_ffm=0.05,
            rt_ffm=0.20,
        )
        conn.commit()
        applied = maybe_settle_body_measurements(
            conn,
            ACTOR,
            as_of_sim_time=full_end.isoformat(),
            state=live_state,
        )
        after = body_measurement_snapshot(conn, ACTOR)
        assert applied["status"] == "applied"
        assert after["body.chest_in"] > baseline["body.chest_in"]
        assert after["body.triceps_in"] > baseline["body.triceps_in"]
        assert after["body.waist_in"] < baseline["body.waist_in"]
        assert "body.hips_in" in after

        latest = conn.execute(
            "SELECT caused_by_event_id,payload_json,state_changes_json FROM events WHERE actor_id=? AND event_type='body_measurement_progression_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        payload = json.loads(latest["payload_json"])
        changes = json.loads(latest["state_changes_json"])
        assert latest["caused_by_event_id"] == bc2_id
        assert payload["regional_training_exposure"]["chest"] == 1.0
        assert payload["regional_training_exposure"]["triceps"] == 1.0
        assert payload["regional_training_exposure"].get("calves", 0.0) == 0.0
        assert payload["body_composition_signal"]["rt_ffm_gain_lb"] == 0.20
        assert payload["deferred_fields"] == []
        assert payload["stat_mutated"] is True
        assert all(abs(float(change["delta"])) <= 0.1500001 for change in changes.values())
        calf_delta = after["body.calves_in"] - baseline["body.calves_in"]
        chest_delta = after["body.chest_in"] - baseline["body.chest_in"]
        triceps_delta = after["body.triceps_in"] - baseline["body.triceps_in"]
        assert chest_delta > calf_delta
        assert triceps_delta > calf_delta

        after_history = conn.execute(
            "SELECT COUNT(*) FROM character_profile_history WHERE entity_id=? AND authority='body_progression_engine'",
            (ACTOR,),
        ).fetchone()[0]
        assert after_history == history_before_applied + len(changes)
        assert after_history >= before_history + bootstrap_history_count

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "actor_id": ACTOR,
            "candidate_initialize_exercised": True,
            "activation_state_at_start": "fresh" if existing is None else "already_active",
            "activation_value_preserved": True,
            "activated_fields": activated_fields,
            "partial_pre_activation_window_deferred": partial_pre_activation_window_deferred,
            "regional_bench_chest_exposure": payload["regional_training_exposure"]["chest"],
            "regional_bench_triceps_exposure": payload["regional_training_exposure"]["triceps"],
            "changed_fields": sorted(changes),
            "model_calls": 0,
            "telegram_calls": 0,
            "production_mutated_by_validation": False
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

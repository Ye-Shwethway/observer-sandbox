from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from observer_sandbox.body_composition_progression import body_composition_snapshot, maybe_settle_body_composition
from observer_sandbox.db import connect
from observer_sandbox.simulation import snapshot

ACTOR = "char_darian"


def _insert_hour(conn, base: datetime, hour: int, *, train: bool = False, eat: bool = False) -> None:
    started = base + timedelta(hours=hour)
    ended = started + timedelta(hours=1)
    payload = {
        "action": "train" if train else ("eat" if eat else "idle"),
        "duration_minutes": 60,
        "action_started_sim_time": started.isoformat(),
        "action_ended_sim_time": ended.isoformat(),
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
            "method_id": "free_weight_strength",
            "family": "resistance",
            "workload_channels": ["resistance"],
            "effective_load": {"effective_minutes": 60.0},
        }
    conn.execute(
        "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
        (ended.isoformat(), ACTOR, "action_completed", json.dumps(payload)),
    )


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    with connect(db_path) as conn:
        live_copy_state = snapshot(conn, ACTOR)
        base = datetime.fromisoformat(str(live_copy_state["sim_time"]))
        before = body_composition_snapshot(conn, ACTOR)
        before_history = conn.execute(
            "SELECT COUNT(*) FROM character_profile_history WHERE entity_id=? AND field_key IN ('body.weight_lb','body.body_fat_pct')",
            (ACTOR,),
        ).fetchone()[0]

        bootstrap = maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=base.isoformat(), state=live_copy_state)
        assert bootstrap["status"] == "bootstrapped"
        assert body_composition_snapshot(conn, ACTOR) == before
        modes = conn.execute(
            "SELECT field_key,mode,authority FROM character_profile_values WHERE entity_id=? AND field_key IN ('body.weight_lb','body.body_fat_pct') ORDER BY field_key",
            (ACTOR,),
        ).fetchall()
        assert len(modes) == 2
        assert all(row["mode"] == "simulated" and row["authority"] == "physiology_engine" for row in modes)

        for hour in range(24):
            _insert_hour(conn, base, hour, train=(hour == 8), eat=(hour in {2, 7, 13, 19}))
        conn.commit()

        end = base + timedelta(hours=24)
        settlement_state = dict(live_copy_state)
        settlement_state.update({
            "sim_time": end.isoformat(), "fatigue": 12.0, "energy": 78.0,
            "hunger": 35.0, "sleepiness": 18.0, "thirst": 20.0,
        })
        applied = maybe_settle_body_composition(conn, ACTOR, as_of_sim_time=end.isoformat(), state=settlement_state)
        after = body_composition_snapshot(conn, ACTOR)
        assert applied["status"] == "applied"
        assert abs(after["weight_lb"] - before["weight_lb"]) <= 0.55
        assert abs(after["weight_lb"] - after["lean_mass_lb"] - after["fat_mass_lb"]) < 1e-5
        assert abs(after["body_fat_pct"] - 100.0 * after["fat_mass_lb"] / after["weight_lb"]) < 1e-4

        latest = conn.execute(
            "SELECT payload_json,state_changes_json FROM events WHERE actor_id=? AND event_type='body_composition_progression_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        payload = json.loads(latest["payload_json"])
        changes = json.loads(latest["state_changes_json"])
        assert payload["energy_balance"]["complete"] is True
        assert payload["resistance_training_effective_minutes"] == 60.0
        assert payload["partition"]["forbes_ffm_share"] > 0.0
        assert payload["rt_recomposition"]["protein_factor"] > 0.0
        assert payload["rt_recomposition"]["training_factor"] == 1.0
        assert "body.weight_lb" in changes and "body.body_fat_pct" in changes

        after_history = conn.execute(
            "SELECT COUNT(*) FROM character_profile_history WHERE entity_id=? AND field_key IN ('body.weight_lb','body.body_fat_pct')",
            (ACTOR,),
        ).fetchone()[0]
        assert after_history >= before_history + 4

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "actor_id": ACTOR,
            "activation_value_preserved": True,
            "before": before,
            "after": after,
            "weight_delta_lb": round(after["weight_lb"] - before["weight_lb"], 6),
            "body_fat_delta_pct": round(after["body_fat_pct"] - before["body_fat_pct"], 6),
            "evidence_complete": payload["energy_balance"]["complete"],
            "resistance_training_effective_minutes": payload["resistance_training_effective_minutes"],
            "model_calls": 0,
            "telegram_calls": 0,
            "production_mutated_by_validation": False,
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

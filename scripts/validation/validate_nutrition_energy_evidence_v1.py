from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.nutrition_energy import resting_energy_reference
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field


ACTOR = "char_darian"
KITCHEN = "loc_thorne_estate_kitchen"
MEAL = "obj_thorne_estate_kitchen_meal_ingredients"


def profile_value(conn, key: str):
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return json.loads(row["value_json"])


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    with connect(db_path) as conn:
        before_weight = profile_value(conn, "body.weight_lb")
        before_bf = profile_value(conn, "body.body_fat_pct")
        before_event_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        before_sim_time = snapshot(conn, ACTOR)["sim_time"]

        reference = resting_energy_reference(conn, ACTOR, as_of_sim_time=before_sim_time)
        assert reference is not None
        assert reference["ree_kcal_day"] > 0.0
        assert reference["sex"] == "male"

        # The live actor may be anywhere when the disposable copy is taken.
        # Use the canonical dynamic-location relation rather than only changing
        # the compatibility cache field before exercising a Kitchen target.
        set_dynamic_location(conn, ACTOR, KITCHEN)
        set_field(conn, ACTOR, "runtime.current_action", "idle")
        set_field(conn, ACTOR, "needs.hunger", 70.0)
        conn.commit()

        apply_action(
            conn,
            Action("eat", 25, MEAL, "disposable BC-1 nutrition/energy evidence acceptance"),
            ACTOR,
            action_id="bc1-nutrition-energy-acceptance",
        )
        row = conn.execute(
            "SELECT payload_json FROM events WHERE action_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
            ("bc1-nutrition-energy-acceptance",),
        ).fetchone()
        assert row is not None
        payload = json.loads(row["payload_json"] or "{}")
        nutrition = payload["nutrition_intake"]
        expenditure = payload["energy_expenditure"]
        assert nutrition["target"] == MEAL
        assert nutrition["energy_kcal"] == 800.0
        assert nutrition["protein_g"] == 50.0
        assert expenditure["estimated_kcal"] > 0.0
        assert expenditure["activity_multiplier"] == 1.5
        assert expenditure["resting_reference"]["formula"] == "mifflin-st-jeor-1990"

        assert profile_value(conn, "body.weight_lb") == before_weight
        assert profile_value(conn, "body.body_fat_pct") == before_bf
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] > before_event_count

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "actor_id": ACTOR,
            "resting_reference": reference,
            "nutrition_intake": nutrition,
            "energy_expenditure": expenditure,
            "body_weight_unchanged": True,
            "body_fat_unchanged": True,
            "model_calls": 0,
            "telegram_calls": 0,
            "production_mutated_by_validation": False
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

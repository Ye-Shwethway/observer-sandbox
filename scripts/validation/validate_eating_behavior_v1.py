from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.eating_behavior import meal_resource_choices, settle_eating_action, validate_proposed_resources
from observer_sandbox.inventory import stack_state


ACTOR = "char_darian"
KITCHEN = "loc_thorne_estate_kitchen"
MEAL_TARGET = "obj_thorne_estate_kitchen_meal_ingredients"
PROBE_ACTION = "acceptance-eating-behavior-v1"


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    with connect(db_path) as conn:
        schema = int(conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0])
        assert schema == 5
        sim_time = json.loads(conn.execute("SELECT value_json FROM runtime_state WHERE key='sim_time'").fetchone()[0])
        actor_runtime_before = dict(conn.execute("SELECT * FROM actor_runtime WHERE actor_id=?", (ACTOR,)).fetchone())

        legacy_pending_checked = False
        pending_id = actor_runtime_before.get("pending_action_id")
        if pending_id:
            pending = conn.execute(
                "SELECT action_type,resources_json FROM action_instances WHERE id=?",
                (pending_id,),
            ).fetchone()
            if pending and pending["action_type"] == "eat" and not json.loads(pending["resources_json"] or "[]"):
                totals_before = conn.execute("SELECT SUM(quantity) FROM inventory_stacks").fetchone()[0]
                assert settle_eating_action(conn, str(pending_id)) is None
                totals_after = conn.execute("SELECT SUM(quantity) FROM inventory_stacks").fetchone()[0]
                assert totals_after == totals_before
                legacy_pending_checked = True

        choices = meal_resource_choices(conn, KITCHEN)
        assert len(choices) >= 2
        selected = [
            {"stack_id": row["stack_id"], "quantity": row["default_quantity"]}
            for row in choices[:2]
        ]
        normalized = validate_proposed_resources(
            conn,
            action_name="eat",
            location_id=KITCHEN,
            resources=selected,
        )
        assert len(normalized) == 2

        before_quantities = {row["stack_id"]: stack_state(conn, row["stack_id"]).quantity for row in selected}
        conn.execute("SAVEPOINT eating_acceptance_probe")
        try:
            conn.execute(
                """INSERT INTO action_instances(
                    id,action_type,actor_id,place_id,target_id,status,duration_minutes,intent,
                    participants_json,resources_json,conditions_json,modifiers_json,planned_sim_time
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    PROBE_ACTION,
                    "eat",
                    ACTOR,
                    KITCHEN,
                    MEAL_TARGET,
                    "in_progress",
                    20,
                    "disposable Eating Behavior v1 acceptance",
                    "[]",
                    json.dumps(selected),
                    "{}",
                    "{}",
                    sim_time,
                ),
            )
            nutrition = settle_eating_action(conn, PROBE_ACTION)
            assert nutrition is not None
            assert nutrition["source"] == "eating-behavior-v1"
            assert nutrition["energy_kcal"] > 0.0
            assert nutrition["protein_g"] >= 0.0
            for row in selected:
                assert stack_state(conn, row["stack_id"]).quantity < before_quantities[row["stack_id"]]
        finally:
            conn.execute("ROLLBACK TO SAVEPOINT eating_acceptance_probe")
            conn.execute("RELEASE SAVEPOINT eating_acceptance_probe")

        for stack_id, quantity in before_quantities.items():
            assert stack_state(conn, stack_id).quantity == quantity
        assert dict(conn.execute("SELECT * FROM actor_runtime WHERE actor_id=?", (ACTOR,)).fetchone()) == actor_runtime_before

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "schema": schema,
            "sim_time_preserved": sim_time,
            "actor_runtime_preserved": True,
            "legacy_empty_resource_pending_compatible": legacy_pending_checked if pending_id else "not_present",
            "structured_resource_count": len(selected),
            "combined_energy_kcal": nutrition["energy_kcal"],
            "combined_protein_g": nutrition["protein_g"],
            "probe_rolled_back": True,
            "model_calls": 0,
            "telegram_calls": 0,
            "production_mutated_by_validation": False,
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

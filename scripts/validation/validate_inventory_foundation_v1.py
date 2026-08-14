from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.inventory import consume_stack, stack_state
from observer_sandbox.runtime import initialize, status


APPLE_STACK = "stack_estate_apples"


def runtime_json(conn, key: str):
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (key,)).fetchone()
    return None if row is None else json.loads(row["value_json"])


def profile_value(conn, actor_id: str, field_key: str):
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    return None if row is None else json.loads(row["value_json"])


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    with connect(db_path) as conn:
        before_schema = int(conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0])
        before_world = runtime_json(conn, "world_identity_revision")
        before_sim_time = runtime_json(conn, "sim_time")
        before_default_actor = runtime_json(conn, "default_actor_id")
        actor_id = before_default_actor or "char_darian"
        before_weight = profile_value(conn, actor_id, "body.weight_lb")
        before_bf = profile_value(conn, actor_id, "body.body_fat_pct")
        actor_runtime_before = conn.execute(
            "SELECT autonomy_enabled,autonomy_mode,pending_action_id,retry_failures,retry_after,retry_last_error FROM actor_runtime WHERE actor_id=?",
            (actor_id,),
        ).fetchone()
        assert actor_runtime_before is not None
        actor_runtime_before = tuple(actor_runtime_before)

    assert before_schema == 4, f"expected production-copy schema v4 before migration, got {before_schema}"

    initialize(db_path)
    migrated = status(db_path)
    assert migrated.schema_version == 5
    assert migrated.runtime_state["inventory_seed_revision"] == "thorne-estate-inventory-v1"

    with connect(db_path) as conn:
        assert runtime_json(conn, "world_identity_revision") == before_world
        assert runtime_json(conn, "sim_time") == before_sim_time
        assert profile_value(conn, actor_id, "body.weight_lb") == before_weight
        assert profile_value(conn, actor_id, "body.body_fat_pct") == before_bf
        actor_runtime_after = conn.execute(
            "SELECT autonomy_enabled,autonomy_mode,pending_action_id,retry_failures,retry_after,retry_last_error FROM actor_runtime WHERE actor_id=?",
            (actor_id,),
        ).fetchone()
        assert actor_runtime_after is not None
        assert tuple(actor_runtime_after) == actor_runtime_before

        apples = stack_state(conn, APPLE_STACK)
        assert apples.definition_id == "item.food.apple"
        assert apples.quantity == 12.0
        assert apples.container_id == "obj_thorne_estate_kitchen_refrigerator"
        assert apples.owner_id == "loc_thorne_estate"

        consumed = consume_stack(conn, APPLE_STACK, 2.0)
        assert consumed["remaining_quantity"] == 10.0
        assert consumed["energy_kcal"] == 190.0

    initialize(db_path)

    with connect(db_path) as conn:
        assert stack_state(conn, APPLE_STACK).quantity == 10.0
        assert int(conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0]) == 5

    print(json.dumps({
        "ok": True,
        "disposable_production_copy": True,
        "schema_before": before_schema,
        "schema_after": 5,
        "world_revision_preserved": before_world,
        "sim_time_preserved": before_sim_time,
        "actor_id": actor_id,
        "actor_runtime_preserved": True,
        "body_weight_preserved": True,
        "body_fat_preserved": True,
        "inventory_seed_revision": "thorne-estate-inventory-v1",
        "apple_definition_id": "item.food.apple",
        "apple_quantity_after_test_consumption": 10.0,
        "reinitialize_did_not_refill": True,
        "model_calls": 0,
        "telegram_calls": 0,
        "production_mutated_by_validation": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

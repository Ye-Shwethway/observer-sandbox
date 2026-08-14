from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.creator_control import replenish_inventory_stack
from observer_sandbox.db import connect
from observer_sandbox.inventory import inventory_for_entity, stack_state
from observer_sandbox.runtime import initialize


ACTOR = "char_darian"
APPLE_STACK = "stack_estate_apples"
MIGRATION_KEY = "inventory_stock_migration:thorne-estate-wealthy-food-reserve-v1"


def _profile_value(conn, key: str):
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return json.loads(row[0])


def _runtime_json(conn, key: str):
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (key,)).fetchone()
    assert row is not None
    return json.loads(row[0])


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    with connect(db_path) as conn:
        schema_before = int(conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0])
        assert schema_before == 5
        sim_time_before = _runtime_json(conn, "sim_time")
        world_revision_before = _runtime_json(conn, "world_identity_revision")
        actor_runtime_before = dict(conn.execute(
            "SELECT * FROM actor_runtime WHERE actor_id=?", (ACTOR,)
        ).fetchone())
        weight_before = _profile_value(conn, "body.weight_lb")
        bf_before = _profile_value(conn, "body.body_fat_pct")
        apple_before = stack_state(conn, APPLE_STACK).quantity
        migration_was_present = conn.execute(
            "SELECT 1 FROM runtime_state WHERE key=?", (MIGRATION_KEY,)
        ).fetchone() is not None

    initialize(db_path)

    with connect(db_path) as conn:
        schema_after = int(conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0])
        assert schema_after == 5
        assert _runtime_json(conn, "sim_time") == sim_time_before
        assert _runtime_json(conn, "world_identity_revision") == world_revision_before
        assert dict(conn.execute(
            "SELECT * FROM actor_runtime WHERE actor_id=?", (ACTOR,)
        ).fetchone()) == actor_runtime_before
        assert _profile_value(conn, "body.weight_lb") == weight_before
        assert _profile_value(conn, "body.body_fat_pct") == bf_before

        apple_after_migration = stack_state(conn, APPLE_STACK).quantity
        assert apple_after_migration >= 120.0 or migration_was_present
        assert conn.execute("SELECT 1 FROM runtime_state WHERE key=?", (MIGRATION_KEY,)).fetchone() is not None

        estate_inventory = inventory_for_entity(conn, "loc_thorne_estate")
        assert any(stack.entity_id == APPLE_STACK for stack in estate_inventory["stacks"])

        reduced_quantity = max(1.0, apple_after_migration - 7.0)
        conn.execute(
            "UPDATE inventory_stacks SET quantity=? WHERE entity_id=?",
            (reduced_quantity, APPLE_STACK),
        )
        conn.commit()

    initialize(db_path)

    with connect(db_path) as conn:
        after_reinitialize = stack_state(conn, APPLE_STACK).quantity
        assert after_reinitialize == reduced_quantity

        control = replenish_inventory_stack(
            conn,
            APPLE_STACK,
            24.0,
            requested_by="production-copy-acceptance",
        )
        assert control["after_quantity"] == reduced_quantity + 24.0
        assert control["physical_location_id"] == "loc_thorne_estate_kitchen"
        event = conn.execute(
            "SELECT payload_json FROM events WHERE event_type='creator_inventory_replenished' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert event is not None
        payload = json.loads(event[0])
        assert payload["authority"] == "creator"
        assert payload["requested_by"] == "production-copy-acceptance"

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "schema_before": schema_before,
            "schema_after": schema_after,
            "sim_time_preserved": sim_time_before,
            "world_revision_preserved": world_revision_before,
            "actor_runtime_preserved": True,
            "body_weight_preserved": True,
            "body_fat_preserved": True,
            "apple_quantity_before": apple_before,
            "wealthy_reserve_after_migration": apple_after_migration,
            "reinitialize_did_not_refill": True,
            "creator_replenish_added": 24.0,
            "creator_replenish_after": control["after_quantity"],
            "physical_location_id": control["physical_location_id"],
            "model_calls": 0,
            "telegram_calls": 0,
            "production_mutated_by_validation": False,
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

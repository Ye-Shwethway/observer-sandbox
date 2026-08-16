from __future__ import annotations

import json

import pytest

from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.inventory import (
    container_inventory,
    consume_stack,
    nutrition_for_stack_quantity,
    stack_state,
)
from observer_sandbox.runtime import initialize, status


WEALTHY_APPLE_RESERVE = 120.0


def test_schema_seeds_universal_food_definitions_and_estate_stacks(tmp_path):
    db_path = tmp_path / "observer.sqlite3"
    initialize(db_path)

    runtime = status(db_path)
    assert runtime.schema_version == SCHEMA_VERSION
    assert runtime.runtime_state["inventory_seed_revision"] == "thorne-estate-inventory-v1"

    with connect(db_path) as conn:
        apple_definition = conn.execute(
            "SELECT id,name,properties_json FROM entity_definitions WHERE id='item.food.apple'"
        ).fetchone()
        assert apple_definition is not None
        assert apple_definition["name"] == "Apple"
        properties = json.loads(apple_definition["properties_json"])
        assert properties["canonical_unit"] == "piece"
        assert properties["stackable"] is True
        assert properties["nutrition"]["energy_kcal"] == 95.0

        apples = stack_state(conn, "stack_estate_apples")
        assert apples.definition_id == "item.food.apple"
        assert apples.quantity == WEALTHY_APPLE_RESERVE
        assert apples.unit == "piece"
        assert apples.container_id == "obj_thorne_estate_kitchen_refrigerator"
        assert apples.owner_id == "loc_thorne_estate"

        fridge = container_inventory(conn, "obj_thorne_estate_kitchen_refrigerator")
        assert "stack_estate_apples" in {row.entity_id for row in fridge}


def test_nutrition_is_definition_based_and_scales_with_quantity(tmp_path):
    db_path = tmp_path / "observer.sqlite3"
    initialize(db_path)

    with connect(db_path) as conn:
        evidence = nutrition_for_stack_quantity(conn, "stack_estate_chicken_breast", 200.0)
        assert evidence["definition_id"] == "item.food.chicken_breast_cooked"
        assert evidence["quantity"] == 200.0
        assert evidence["unit"] == "g"
        assert evidence["energy_kcal"] == 330.0
        assert evidence["protein_g"] == 62.0

        two_apples = nutrition_for_stack_quantity(conn, "stack_estate_apples", 2.0)
        assert two_apples["energy_kcal"] == 190.0
        assert two_apples["carbohydrate_g"] == 50.0


def test_consumption_is_atomic_and_reinitialize_does_not_refill_stock(tmp_path):
    db_path = tmp_path / "observer.sqlite3"
    initialize(db_path)

    with connect(db_path) as conn:
        consumed = consume_stack(conn, "stack_estate_apples", 2.0)
        expected_remaining = WEALTHY_APPLE_RESERVE - 2.0
        assert consumed["remaining_quantity"] == expected_remaining
        assert stack_state(conn, "stack_estate_apples").quantity == expected_remaining

        with pytest.raises(ValueError, match="Insufficient quantity"):
            consume_stack(conn, "stack_estate_apples", expected_remaining + 1.0)
        assert stack_state(conn, "stack_estate_apples").quantity == expected_remaining

    initialize(db_path)

    with connect(db_path) as conn:
        assert stack_state(conn, "stack_estate_apples").quantity == expected_remaining


def test_structural_contains_is_not_reused_for_mutable_inventory_containment(tmp_path):
    db_path = tmp_path / "observer.sqlite3"
    initialize(db_path)

    with connect(db_path) as conn:
        stored = conn.execute(
            "SELECT target_id FROM relations WHERE source_id='stack_estate_apples' AND relation_type='stored_in'"
        ).fetchone()
        assert stored is not None
        assert stored["target_id"] == "obj_thorne_estate_kitchen_refrigerator"

        structural = conn.execute(
            "SELECT 1 FROM relations WHERE source_id='stack_estate_apples' AND relation_type='contains'"
        ).fetchone()
        assert structural is None

        mobility = conn.execute(
            "SELECT value_json FROM fields WHERE entity_id='obj_thorne_estate_kitchen_refrigerator' AND field_key='inventory.container_mobility'"
        ).fetchone()
        assert mobility is not None
        assert json.loads(mobility["value_json"]) == "fixed"

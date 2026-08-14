import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.eating_behavior import (
    enrich_eating_action_options,
    meal_resource_choices,
    validate_proposed_resources,
)
from observer_sandbox.inventory import stack_state
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot


KITCHEN = "loc_thorne_estate_kitchen"
MEAL_TARGET = "obj_thorne_estate_kitchen_meal_ingredients"


def _move_to_kitchen(conn):
    set_dynamic_location(conn, "char_darian", KITCHEN)
    conn.commit()


def test_kitchen_eat_option_exposes_deterministic_inventory_portions(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_to_kitchen(conn)
        options = enrich_eating_action_options(conn, KITCHEN, action_options(conn, "char_darian"))
        eat = next(row for row in options if row["action"] == "eat")
        resources = {row["stack_id"]: row for row in eat["meal_resources"]}

    chicken = resources["stack_estate_chicken_breast"]
    assert chicken["unit"] == "g"
    assert chicken["min_quantity"] == 100.0
    assert chicken["default_quantity"] == 200.0
    assert chicken["max_quantity"] == 400.0
    assert chicken["default_nutrition"]["energy_kcal"] == 330.0
    assert chicken["default_nutrition"]["protein_g"] == 62.0


def test_structured_multi_item_meal_consumes_stocks_and_snapshots_combined_macros(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_to_kitchen(conn)
        apple_before = stack_state(conn, "stack_estate_apples").quantity
        chicken_before = stack_state(conn, "stack_estate_chicken_breast").quantity

        apply_action(
            conn,
            Action(
                "eat",
                20,
                MEAL_TARGET,
                "eat a balanced meal",
                resources=(
                    {"stack_id": "stack_estate_apples", "quantity": 1.0},
                    {"stack_id": "stack_estate_chicken_breast", "quantity": 200.0},
                ),
            ),
            "char_darian",
        )

        assert stack_state(conn, "stack_estate_apples").quantity == apple_before - 1.0
        assert stack_state(conn, "stack_estate_chicken_breast").quantity == chicken_before - 200.0
        event = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id='char_darian' AND event_type='action_completed' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        payload = json.loads(event[0])
        nutrition = payload["nutrition_intake"]

    assert nutrition["source"] == "eating-behavior-v1"
    assert nutrition["energy_kcal"] == 425.0
    assert nutrition["protein_g"] == 62.5
    assert nutrition["carbohydrate_g"] == 25.0
    assert nutrition["fat_g"] == 7.5
    assert {row["stack_id"] for row in nutrition["items"]} == {
        "stack_estate_apples",
        "stack_estate_chicken_breast",
    }


def test_failed_meal_settlement_rolls_back_inventory_and_action_completion_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_to_kitchen(conn)
        before_state = snapshot(conn, "char_darian")
        apple_before = stack_state(conn, "stack_estate_apples").quantity

        with pytest.raises(ValueError, match="Meal quantity"):
            apply_action(
                conn,
                Action(
                    "eat",
                    20,
                    MEAL_TARGET,
                    "invalid oversized meal",
                    resources=(
                        {"stack_id": "stack_estate_apples", "quantity": 1.0},
                        {"stack_id": "stack_estate_chicken_breast", "quantity": 500.0},
                    ),
                ),
                "char_darian",
            )

        assert stack_state(conn, "stack_estate_apples").quantity == apple_before
        assert snapshot(conn, "char_darian") == before_state


def test_legacy_empty_resource_eat_can_complete_without_inventory_decrement(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_to_kitchen(conn)
        apple_before = stack_state(conn, "stack_estate_apples").quantity
        apply_action(conn, Action("eat", 20, MEAL_TARGET, "legacy in-flight meal"), "char_darian")
        assert stack_state(conn, "stack_estate_apples").quantity == apple_before
        event = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id='char_darian' AND event_type='action_completed' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        nutrition = json.loads(event[0])["nutrition_intake"]

    assert nutrition["source"] != "eating-behavior-v1"


def test_new_proposals_require_resources_only_for_eat(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _move_to_kitchen(conn)
        with pytest.raises(ValueError, match="at least one"):
            validate_proposed_resources(conn, action_name="eat", location_id=KITCHEN, resources=[])
        with pytest.raises(ValueError, match="Only eat actions"):
            validate_proposed_resources(
                conn,
                action_name="idle",
                location_id=KITCHEN,
                resources=[{"stack_id": "stack_estate_apples", "quantity": 1.0}],
            )


def test_meal_resource_discovery_is_not_estate_or_darian_specific(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json) VALUES('loc_market_test','location','Test Market','[]')"
        )
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json) VALUES('obj_market_crate','object','Produce Crate','[]')"
        )
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            ('stack_market_banana','item','Banana','[\"eat\",\"inspect\"]','item.food.banana'),
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES('loc_market_test','contains','obj_market_crate')"
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES('stack_market_banana','stored_in','obj_market_crate')"
        )
        conn.execute(
            "INSERT INTO inventory_stacks(entity_id,quantity,unit,seed_revision,metadata_json) VALUES('stack_market_banana',20,'piece','test','{}')"
        )
        conn.commit()

        choices = meal_resource_choices(conn, "loc_market_test")

    assert len(choices) == 1
    assert choices[0]["stack_id"] == "stack_market_banana"
    assert choices[0]["default_quantity"] == 1.0

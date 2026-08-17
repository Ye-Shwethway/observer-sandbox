from __future__ import annotations

import pytest

from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.economic_value import (
    estate_inventory_stock_value_minor,
    inventory_stack_value_minor,
    require_entity_value_policy,
    validate_current_value_coverage,
    value_profile,
)
from observer_sandbox.economy import economic_net_worth
from observer_sandbox.economy_schema import ECONOMY_SCHEMA_VERSION
from observer_sandbox.runtime import initialize


DARIAN_ECON = "econ_char_darian"


def test_w31_schema_and_current_world_value_coverage(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert int(conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0]) == SCHEMA_VERSION
        assert int(conn.execute("SELECT value FROM schema_meta WHERE key='economy_schema_version'").fetchone()[0]) == ECONOMY_SCHEMA_VERSION == 2
        validate_current_value_coverage(conn)

        object_count = conn.execute("SELECT COUNT(*) FROM entities WHERE entity_type='object'").fetchone()[0]
        covered_objects = conn.execute(
            "SELECT COUNT(*) FROM economic_value_profiles WHERE subject_type='entity'"
        ).fetchone()[0]
        assert covered_objects == object_count

        definition_count = conn.execute(
            "SELECT COUNT(*) FROM entity_definitions WHERE entity_type='item'"
        ).fetchone()[0]
        covered_definitions = conn.execute(
            "SELECT COUNT(*) FROM economic_value_profiles WHERE subject_type='entity_definition'"
        ).fetchone()[0]
        assert covered_definitions == definition_count


def test_estate_components_have_values_without_double_counting_net_worth(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        ai_sim = require_entity_value_policy(conn, "obj_thorne_estate_training_ai_combat_sim")
        assert ai_sim["classification"] == "component"
        assert ai_sim["replacement_value_minor"] == 45_000_000
        assert ai_sim["net_worth_treatment"] == "included_in_parent"
        assert ai_sim["included_in_asset_id"] == "asset_thorne_estate"

        diagnostic = require_entity_value_policy(conn, "obj_thorne_estate_medical_diagnostic_station")
        assert diagnostic["replacement_value_minor"] == 30_000_000
        assert diagnostic["included_in_asset_id"] == "asset_thorne_estate"

        assert economic_net_worth(conn, DARIAN_ECON) == 2_500_000_000


def test_resource_proxies_do_not_duplicate_inventory_stock(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        for entity_id in (
            "obj_thorne_estate_food_storage_provisions",
            "obj_thorne_estate_kitchen_drinking_water",
            "obj_thorne_estate_kitchen_meal_ingredients",
        ):
            profile = value_profile(conn, "entity", entity_id)
            assert profile["classification"] == "resource_proxy"
            assert profile["net_worth_treatment"] == "excluded"
            assert profile["market_value_minor"] is None
            assert profile["replacement_value_minor"] is None


def test_inventory_stock_value_derives_from_live_quantity_and_unit_policy(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        # Wealthy-estate stock migration has already established the represented
        # reserve. The current canonical food stock values to USD 2,443.50.
        assert estate_inventory_stock_value_minor(conn) == 244_350
        assert inventory_stack_value_minor(conn, "stack_estate_apples") == 15_000

        conn.execute(
            "UPDATE inventory_stacks SET quantity=quantity-10 WHERE entity_id='stack_estate_apples'"
        )
        conn.commit()
        assert inventory_stack_value_minor(conn, "stack_estate_apples") == 13_750
        assert estate_inventory_stock_value_minor(conn) == 243_100


def test_new_world_object_without_value_policy_fails_closed(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json) VALUES(?,?,?,?)",
            ("obj_fixture_unvalued", "object", "Unvalued Fixture", "[]"),
        )
        conn.commit()
        with pytest.raises(ValueError, match="missing economic value policy coverage"):
            validate_current_value_coverage(conn)
        with pytest.raises(ValueError, match="missing economic value policy"):
            require_entity_value_policy(conn, "obj_fixture_unvalued")

import json

from observer_sandbox.creator_control import replenish_inventory_stack
from observer_sandbox.db import connect
from observer_sandbox.inventory import inventory_for_entity, list_inventory_scopes, stack_state
from observer_sandbox.runtime import initialize
from observer_sandbox.world import set_field


WEALTHY_MINIMUMS = {
    "stack_estate_apples": 120.0,
    "stack_estate_bananas": 90.0,
    "stack_estate_chicken_breast": 30000.0,
    "stack_estate_white_rice": 36000.0,
    "stack_estate_eggs": 240.0,
    "stack_estate_oats": 15000.0,
    "stack_estate_greek_yogurt": 16000.0,
    "stack_estate_mixed_vegetables": 30000.0,
    "stack_estate_olive_oil": 8000.0,
    "stack_estate_whey_protein": 10000.0,
}


def _insert_entity(conn, entity_id: str, entity_type: str, name: str, *, definition_id=None):
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
        (entity_id, entity_type, name, "[]", definition_id),
    )


def _insert_relation(conn, source_id: str, relation_type: str, target_id: str):
    conn.execute(
        "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
        (source_id, relation_type, target_id),
    )


def test_wealthy_estate_reserve_is_one_time_migration(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        marker = conn.execute(
            "SELECT value_json FROM runtime_state WHERE key=?",
            ("inventory_stock_migration:thorne-estate-wealthy-food-reserve-v1",),
        ).fetchone()
        assert marker is not None
        assert json.loads(marker[0])["applied"] is True
        for stack_id, minimum in WEALTHY_MINIMUMS.items():
            assert stack_state(conn, stack_id).quantity >= minimum

        conn.execute(
            "UPDATE inventory_stacks SET quantity=37 WHERE entity_id='stack_estate_apples'"
        )
        conn.commit()

    initialize(db)
    with connect(db) as conn:
        assert stack_state(conn, "stack_estate_apples").quantity == 37.0
        event_count = conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type='creator_inventory_stock_baseline_applied'"
        ).fetchone()[0]
        assert event_count == 1


def test_creator_replenish_is_typed_audited_and_preserves_sim_time(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before_time = json.loads(
            conn.execute("SELECT value_json FROM runtime_state WHERE key='sim_time'").fetchone()[0]
        )
        before = stack_state(conn, "stack_estate_apples")
        result = replenish_inventory_stack(
            conn,
            "stack_estate_apples",
            24,
            requested_by="test:creator",
        )
        after_time = json.loads(
            conn.execute("SELECT value_json FROM runtime_state WHERE key='sim_time'").fetchone()[0]
        )

        assert result["before_quantity"] == before.quantity
        assert result["after_quantity"] == before.quantity + 24.0
        assert result["physical_location_id"] == "loc_thorne_estate_kitchen"
        assert after_time == before_time

        row = conn.execute(
            "SELECT location_id,payload_json FROM events WHERE event_type='creator_inventory_replenished' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert row is not None
        assert row["location_id"] == "loc_thorne_estate_kitchen"
        payload = json.loads(row["payload_json"])
        assert payload["authority"] == "creator"
        assert payload["requested_by"] == "test:creator"
        assert payload["added_quantity"] == 24.0


def test_universal_location_scope_finds_non_estate_inventory(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _insert_entity(conn, "loc_synthetic_market", "location", "Synthetic Market")
        _insert_entity(conn, "obj_synthetic_crate", "object", "Market Produce Crate")
        _insert_entity(
            conn,
            "stack_synthetic_apples",
            "item",
            "Apple",
            definition_id="item.food.apple",
        )
        _insert_relation(conn, "world_observer_universe", "contains", "loc_synthetic_market")
        _insert_relation(conn, "loc_synthetic_market", "contains", "obj_synthetic_crate")
        _insert_relation(conn, "stack_synthetic_apples", "stored_in", "obj_synthetic_crate")
        _insert_relation(conn, "stack_synthetic_apples", "owned_by", "loc_synthetic_market")
        set_field(
            conn,
            "obj_synthetic_crate",
            "inventory.container_kind",
            "produce_crate",
            mode="static",
            authority="test",
            source="test",
        )
        set_field(
            conn,
            "obj_synthetic_crate",
            "inventory.container_mobility",
            "movable",
            mode="static",
            authority="test",
            source="test",
        )
        conn.execute(
            "INSERT INTO inventory_stacks(entity_id,quantity,unit,seed_revision,metadata_json) VALUES(?,?,?,?,?)",
            ("stack_synthetic_apples", 42.0, "piece", "synthetic", "{}"),
        )
        conn.commit()

        scoped = inventory_for_entity(conn, "loc_synthetic_market")
        assert scoped["scope"]["name"] == "Synthetic Market"
        assert {stack.entity_id for stack in scoped["stacks"]} == {"stack_synthetic_apples"}
        assert scoped["containers"][0]["id"] == "obj_synthetic_crate"

        locations = list_inventory_scopes(conn, "locations")
        market = next(row for row in locations if row["id"] == "loc_synthetic_market")
        assert market["stack_count"] == 1
        assert market["container_count"] == 1


def test_universal_character_scope_finds_owned_or_carried_inventory(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _insert_entity(conn, "char_synthetic", "character", "Synthetic Character")
        _insert_entity(conn, "obj_synthetic_backpack", "object", "Synthetic Backpack")
        _insert_entity(
            conn,
            "stack_synthetic_bananas",
            "item",
            "Banana",
            definition_id="item.food.banana",
        )
        _insert_relation(conn, "obj_synthetic_backpack", "owned_by", "char_synthetic")
        _insert_relation(conn, "obj_synthetic_backpack", "carried_by", "char_synthetic")
        _insert_relation(conn, "stack_synthetic_bananas", "stored_in", "obj_synthetic_backpack")
        _insert_relation(conn, "stack_synthetic_bananas", "owned_by", "char_synthetic")
        set_field(
            conn,
            "obj_synthetic_backpack",
            "inventory.container_kind",
            "backpack",
            mode="static",
            authority="test",
            source="test",
        )
        set_field(
            conn,
            "obj_synthetic_backpack",
            "inventory.container_mobility",
            "movable",
            mode="static",
            authority="test",
            source="test",
        )
        conn.execute(
            "INSERT INTO inventory_stacks(entity_id,quantity,unit,seed_revision,metadata_json) VALUES(?,?,?,?,?)",
            ("stack_synthetic_bananas", 5.0, "piece", "synthetic", "{}"),
        )
        conn.commit()

        scoped = inventory_for_entity(conn, "char_synthetic")
        assert {stack.entity_id for stack in scoped["stacks"]} == {"stack_synthetic_bananas"}
        assert {row["id"] for row in scoped["containers"]} == {"obj_synthetic_backpack"}

        characters = list_inventory_scopes(conn, "characters")
        synthetic = next(row for row in characters if row["id"] == "char_synthetic")
        assert synthetic["stack_count"] == 1
        assert synthetic["container_count"] == 1

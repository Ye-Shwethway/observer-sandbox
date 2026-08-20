from observer_sandbox.creation_sandbox import reset_sandbox
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import create_sandbox_item


def _item():
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "reset.cleanup.item", "name": "Reset Cleanup Item", "kind": "object",
            "description": "Reset cleanup proof.", "stackable": False, "mobility": "movable",
            "capabilities": ["inspect"], "tags": ["test"], "modules": {},
        },
        "instance": {"mode": "unique"},
        "economic_policy": {
            "classification": "standalone_asset", "currency_code": "USD",
            "market_value_minor": 100, "replacement_value_minor": 100,
            "unit_value_minor": None, "unit_quantity": None, "unit_label": None,
            "net_worth_treatment": "independent", "included_in_parent_ref": None,
            "valuation_method": "creator_explicit",
        },
        "requirements": {"use": None},
        "relationships": {"located_at": None, "stored_in": None, "owned_by": None, "carried_by": None, "equipped_by": None},
    }


def test_reset_clears_item_objects_instances_economics_and_shared_definitions(tmp_path):
    db = tmp_path / "db.sqlite3"
    initialize(db)
    with connect(db) as conn:
        create_sandbox_item(conn, _item())
        assert conn.execute("SELECT COUNT(*) AS n FROM creation_sandbox_item_definitions").fetchone()["n"] == 1
        reset_sandbox(conn)
        assert conn.execute("SELECT COUNT(*) AS n FROM creation_sandbox_objects WHERE creation_type='item'").fetchone()["n"] == 0
        assert conn.execute("SELECT COUNT(*) AS n FROM creation_sandbox_item_instances").fetchone()["n"] == 0
        assert conn.execute("SELECT COUNT(*) AS n FROM creation_sandbox_item_economic_profiles").fetchone()["n"] == 0
        assert conn.execute("SELECT COUNT(*) AS n FROM creation_sandbox_item_definitions").fetchone()["n"] == 0

from __future__ import annotations

from copy import deepcopy

import pytest

from observer_sandbox.creation_sandbox import activate_creation_proposal, canonical_state_fingerprint
from observer_sandbox.creation_socket import build_creation_proposal
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import create_sandbox_item, create_sandbox_item_batch
from observer_sandbox.sandbox_item_operations import (
    SandboxItemOperationError,
    archive_sandbox_item,
    delete_sandbox_item,
    item_dependencies,
    list_sandbox_items,
    set_sandbox_item_quantity,
    set_sandbox_item_relation,
    update_sandbox_item,
)


def rels(**values):
    out = {"located_at": None, "stored_in": None, "owned_by": None, "carried_by": None, "equipped_by": None}
    out.update(values)
    return out


def payload(key: str, *, container=False, stack=False):
    capabilities = ["inspect"]
    modules = {}
    kind = "object"
    instance = {"mode": "unique"}
    economic = {
        "classification": "standalone_asset", "currency_code": "USD",
        "market_value_minor": 1000, "replacement_value_minor": 1200,
        "unit_value_minor": None, "unit_quantity": None, "unit_label": None,
        "net_worth_treatment": "independent", "included_in_parent_ref": None,
        "valuation_method": "creator_explicit",
    }
    if container:
        kind = "container"; capabilities.append("store")
        modules["container"] = {"capacity_volume": {"value": 20, "unit": "L"}}
    if stack:
        kind = "consumable"; capabilities.append("eat")
        modules["stack"] = {"canonical_unit": "piece", "initial_quantity": 5}
        modules["nutrition"] = {"basis_quantity": 1, "unit": "piece", "energy_kcal": 60, "protein_g": 1, "carbohydrate_g": 12, "fat_g": 0}
        instance = {"mode": "stack", "quantity": 5, "unit": "piece"}
        economic = {
            "classification": "consumable_stock", "currency_code": "USD",
            "market_value_minor": None, "replacement_value_minor": None,
            "unit_value_minor": 75, "unit_quantity": 1, "unit_label": "piece",
            "net_worth_treatment": "derived_stock", "included_in_parent_ref": None,
            "valuation_method": "creator_explicit",
        }
    return {
        "schema_version": "item-v1",
        "definition": {"key": key, "name": key, "kind": kind, "description": f"Test {key}", "stackable": stack, "mobility": "movable", "capabilities": capabilities, "tags": ["test"], "modules": modules},
        "instance": instance, "economic_policy": economic, "requirements": {"use": None}, "relationships": rels(),
    }


def location(conn, name="Room"):
    return activate_creation_proposal(conn, build_creation_proposal("location", identity={"name": name}))["object_id"]


def character(conn, name="Owner"):
    return activate_creation_proposal(conn, build_creation_proposal("character", identity={"name": name}))["object_id"]


def test_browse_and_quantity_operations_preserve_canonical_state(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        stack = create_sandbox_item(conn, payload("ops.stock", stack=True))
        unique = create_sandbox_item(conn, payload("ops.unique"))
        assert {x["object_id"] for x in list_sandbox_items(conn)} == {stack["object_id"], unique["object_id"]}
        changed = set_sandbox_item_quantity(conn, stack["object_id"], 0)
        assert changed["item"]["instance"]["quantity"] == 0.0
        with pytest.raises(SandboxItemOperationError, match="Only stack"):
            set_sandbox_item_quantity(conn, unique["object_id"], 2)
        assert canonical_state_fingerprint(conn) == before


def test_move_storage_carry_and_ownership_relations_remain_distinct(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        room = location(conn); owner = character(conn)
        item = create_sandbox_item(conn, payload("ops.move"))
        moved = set_sandbox_item_relation(conn, item["object_id"], "located_at", room)
        assert {(r["relation_type"], r["target_object_id"]) for r in moved["resolved_relations"]} == {("located_at", room)}
        owned = set_sandbox_item_relation(conn, item["object_id"], "owned_by", owner)
        assert {(r["relation_type"], r["target_object_id"]) for r in owned["resolved_relations"]} == {("located_at", room), ("owned_by", owner)}
        carried = set_sandbox_item_relation(conn, item["object_id"], "carried_by", owner)
        assert {(r["relation_type"], r["target_object_id"]) for r in carried["resolved_relations"]} == {("carried_by", owner), ("owned_by", owner)}
        cleared = set_sandbox_item_relation(conn, item["object_id"], "carried_by", None)
        assert {(r["relation_type"], r["target_object_id"]) for r in cleared["resolved_relations"]} == {("owned_by", owner)}


def test_container_storage_cycle_is_rejected(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        a = create_sandbox_item(conn, payload("ops.container.a", container=True))
        b = create_sandbox_item(conn, payload("ops.container.b", container=True))
        set_sandbox_item_relation(conn, a["object_id"], "stored_in", b["object_id"])
        with pytest.raises(SandboxItemOperationError, match="cycle"):
            set_sandbox_item_relation(conn, b["object_id"], "stored_in", a["object_id"])


def test_full_edit_validates_schema_and_shared_definition_is_protected(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        original = payload("ops.shared")
        first, second = create_sandbox_item_batch(conn, [{"ref": "a", "payload": original}, {"ref": "b", "payload": original}])
        edited = deepcopy(original); edited["definition"]["description"] = "Changed shared definition"
        with pytest.raises(SandboxItemOperationError, match="Shared Item definition"):
            update_sandbox_item(conn, first["object_id"], edited)
        assert second["item"]["definition"]["description"] == "Test ops.shared"

        sole_payload = payload("ops.sole")
        sole = create_sandbox_item(conn, sole_payload)
        sole_edit = deepcopy(sole_payload); sole_edit["definition"]["description"] = "Creator revised description"; sole_edit["economic_policy"]["market_value_minor"] = 1500
        revised = update_sandbox_item(conn, sole["object_id"], sole_edit)
        assert revised["item"]["definition"]["description"] == "Creator revised description"
        assert revised["item"]["economic_policy"]["market_value_minor"] == 1500


def test_archive_container_requires_explicit_dependency_detach(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        container = create_sandbox_item(conn, payload("ops.archive.container", container=True))
        stock_payload = payload("ops.archive.stock", stack=True); stock_payload["relationships"]["stored_in"] = container["object_id"]
        stock = create_sandbox_item(conn, stock_payload)
        deps = item_dependencies(conn, container["object_id"])
        assert deps == [{"source_object_id": stock["object_id"], "relation_type": "stored_in", "metadata": {}}]
        with pytest.raises(SandboxItemOperationError, match="incoming dependencies"):
            archive_sandbox_item(conn, container["object_id"])
        archived = archive_sandbox_item(conn, container["object_id"], detach_dependents=True)
        assert archived["lifecycle_status"] == "archived"
        assert create_sandbox_item  # keep import/use explicit for static analyzers
        refreshed_stock = next(x for x in list_sandbox_items(conn) if x["object_id"] == stock["object_id"])
        assert refreshed_stock["resolved_relations"] == []


def test_delete_container_dependency_policy_and_definition_cleanup(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        shared = payload("ops.delete.shared")
        a, b = create_sandbox_item_batch(conn, [{"ref": "a", "payload": shared}, {"ref": "b", "payload": shared}])
        delete_sandbox_item(conn, a["object_id"])
        assert conn.execute("SELECT 1 FROM creation_sandbox_item_definitions WHERE definition_key='ops.delete.shared'").fetchone() is not None
        delete_sandbox_item(conn, b["object_id"])
        assert conn.execute("SELECT 1 FROM creation_sandbox_item_definitions WHERE definition_key='ops.delete.shared'").fetchone() is None

        container = create_sandbox_item(conn, payload("ops.delete.container", container=True))
        stock_payload = payload("ops.delete.stock", stack=True); stock_payload["relationships"]["stored_in"] = container["object_id"]
        stock = create_sandbox_item(conn, stock_payload)
        with pytest.raises(SandboxItemOperationError, match="incoming dependencies"):
            delete_sandbox_item(conn, container["object_id"])
        delete_sandbox_item(conn, container["object_id"], detach_dependents=True)
        assert conn.execute("SELECT 1 FROM creation_sandbox_objects WHERE object_id=?", (container["object_id"],)).fetchone() is None
        assert next(x for x in list_sandbox_items(conn) if x["object_id"] == stock["object_id"])["resolved_relations"] == []

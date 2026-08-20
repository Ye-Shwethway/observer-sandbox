from __future__ import annotations

from copy import deepcopy

import pytest

from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import (
    SandboxItemCreationError,
    create_sandbox_item,
    create_sandbox_item_batch,
    preview_sandbox_item_batch,
)


def rels(**values):
    result = {"located_at": None, "stored_in": None, "owned_by": None, "carried_by": None, "equipped_by": None}
    result.update(values)
    return result


def item(key: str, *, container: bool = False, stack: bool = False):
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
        kind = "container"
        capabilities.append("store")
        modules["container"] = {"capacity_volume": {"value": 10, "unit": "L"}}
    if stack:
        kind = "consumable"
        capabilities.append("eat")
        modules["stack"] = {"canonical_unit": "piece", "initial_quantity": 6}
        modules["nutrition"] = {
            "basis_quantity": 1, "unit": "piece", "energy_kcal": 50,
            "protein_g": 1, "carbohydrate_g": 10, "fat_g": 0,
        }
        instance = {"mode": "stack", "quantity": 6, "unit": "piece"}
        economic = {
            "classification": "consumable_stock", "currency_code": "USD",
            "market_value_minor": None, "replacement_value_minor": None,
            "unit_value_minor": 50, "unit_quantity": 1, "unit_label": "piece",
            "net_worth_treatment": "derived_stock", "included_in_parent_ref": None,
            "valuation_method": "creator_explicit",
        }
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": key, "name": key, "kind": kind, "description": f"Test {key}",
            "stackable": stack, "mobility": "movable", "capabilities": capabilities,
            "tags": ["test"], "modules": modules,
        },
        "instance": instance, "economic_policy": economic,
        "requirements": {"use": None}, "relationships": rels(),
    }


def counts(conn):
    return tuple(conn.execute(f"SELECT COUNT(*) AS n FROM {table}").fetchone()["n"] for table in (
        "creation_sandbox_objects", "creation_sandbox_item_definitions",
        "creation_sandbox_item_instances", "creation_sandbox_item_economic_profiles",
    ))


def test_preview_is_write_free_and_supports_forward_internal_refs(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        before = counts(conn)
        stock = item("batch.stock", stack=True); stock["relationships"]["stored_in"] = "$crate"
        preview = preview_sandbox_item_batch(conn, [
            {"ref": "stock", "payload": stock}, {"ref": "crate", "payload": item("batch.crate", container=True)},
        ])
        assert preview["count"] == 2
        assert preview["entries"][0]["resolved_relationships"][0]["target"] == "crate"
        assert counts(conn) == before


def test_heterogeneous_batch_is_atomic_and_canonical_state_unchanged(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        stock = item("batch.stock", stack=True); stock["relationships"]["stored_in"] = "$crate"
        created = create_sandbox_item_batch(conn, [
            {"ref": "stock", "payload": stock},
            {"ref": "crate", "payload": item("batch.crate", container=True)},
            {"ref": "tool", "payload": item("batch.tool")},
        ])
        assert len(created) == 3
        assert canonical_state_fingerprint(conn) == before
        crate_id = next(x["object_id"] for x in created if x["item"]["definition"]["key"] == "batch.crate")
        stock_obj = next(x for x in created if x["item"]["definition"]["key"] == "batch.stock")
        assert ("stored_in", crate_id) in {(r["relation_type"], r["target_object_id"]) for r in stock_obj["resolved_relations"]}
        event = conn.execute("SELECT payload_json FROM creation_sandbox_events WHERE event_type='sandbox_item_batch_materialized' ORDER BY id DESC LIMIT 1").fetchone()
        assert event is not None


def test_invalid_refs_and_non_container_targets_leave_zero_item_writes(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        baseline = counts(conn)
        for target, match in (("$missing", "Unknown batch"), ("$plain", "container Item")):
            stock = item("batch.stock." + target[1:], stack=True); stock["relationships"]["stored_in"] = target
            entries = [{"ref": "stock", "payload": stock}]
            if target == "$plain": entries.append({"ref": "plain", "payload": item("batch.plain")})
            with pytest.raises(SandboxItemCreationError, match=match): create_sandbox_item_batch(conn, entries)
            assert counts(conn) == baseline


def test_duplicate_self_and_storage_cycle_fail_closed(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        baseline = counts(conn)
        with pytest.raises(SandboxItemCreationError, match="Duplicate batch ref"):
            create_sandbox_item_batch(conn, [{"ref": "a", "payload": item("dup.a")}, {"ref": "a", "payload": item("dup.b")}])
        a = item("self.a", container=True); a["relationships"]["stored_in"] = "$a"
        with pytest.raises(SandboxItemCreationError, match="reference itself"):
            create_sandbox_item_batch(conn, [{"ref": "a", "payload": a}])
        a = item("cycle.a", container=True); b = item("cycle.b", container=True)
        a["relationships"]["stored_in"] = "$b"; b["relationships"]["stored_in"] = "$a"
        with pytest.raises(SandboxItemCreationError, match="acyclic"):
            create_sandbox_item_batch(conn, [{"ref": "a", "payload": a}, {"ref": "b", "payload": b}])
        assert counts(conn) == baseline


def test_definition_conflict_inside_batch_rejected_before_write(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        first = item("same.key"); second = deepcopy(first); second["definition"]["description"] = "Different semantics"
        baseline = counts(conn)
        with pytest.raises(SandboxItemCreationError, match="different semantics"):
            create_sandbox_item_batch(conn, [{"ref": "a", "payload": first}, {"ref": "b", "payload": second}])
        assert counts(conn) == baseline


def test_one_invalid_member_means_zero_batch_materialization(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        bad = item("bad.member"); bad["definition"]["unknown"] = True
        baseline = counts(conn)
        with pytest.raises(Exception):
            create_sandbox_item_batch(conn, [{"ref": "good", "payload": item("good.member")}, {"ref": "bad", "payload": bad}])
        assert counts(conn) == baseline


def test_single_creation_reuses_batch_path_and_emits_batch_event(tmp_path):
    db = tmp_path / "db.sqlite3"; initialize(db)
    with connect(db) as conn:
        created = create_sandbox_item(conn, item("single.via.batch"))
        assert created["item"]["definition"]["key"] == "single.via.batch"
        row = conn.execute("SELECT payload_json FROM creation_sandbox_events WHERE event_type='sandbox_item_batch_materialized' ORDER BY id DESC LIMIT 1").fetchone()
        assert '"count":1' in row["payload_json"]

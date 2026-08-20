from __future__ import annotations

import json

import pytest

from observer_sandbox.creation_sandbox import (
    activate_creation_proposal,
    canonical_state_fingerprint,
)
from observer_sandbox.creation_socket import build_creation_proposal, socket_definition
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import (
    SandboxItemCreationError,
    create_sandbox_item,
    get_sandbox_item,
)


def _unique_training_item() -> dict:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "equipment.training.adjustable_dumbbell",
            "name": "Adjustable Dumbbell",
            "kind": "equipment",
            "description": "A plate-loaded adjustable dumbbell.",
            "stackable": False,
            "mobility": "movable",
            "capabilities": ["inspect", "train", "use"],
            "tags": ["training", "strength"],
            "modules": {
                "physical": {
                    "mass": {"value": 55.0, "unit": "lb"},
                    "length": None,
                    "width": None,
                    "height": None,
                },
                "stack": None,
                "nutrition": None,
                "container": None,
                "resistance_training": {
                    "resistance_load": {"value": 55.0, "unit": "lb"},
                    "load_adjustable": True,
                },
                "metrics": {},
            },
        },
        "instance": {
            "mode": "unique",
            "quantity": None,
            "condition": "good",
        },
        "economic_policy": {
            "classification": "standalone_asset",
            "currency_code": "USD",
            "unit_value_minor": 30000,
            "replacement_value_minor": 30000,
            "net_worth_treatment": "independent",
            "included_in_parent_ref": None,
            "valuation_method": "creator_estimate",
        },
        "requirements": {"use": None},
        "relationships": {
            "located_at": None,
            "stored_in": None,
            "owned_by": None,
            "carried_by": None,
            "equipped_by": None,
        },
    }


def _food_stack_item() -> dict:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "food.fruit.apple",
            "name": "Apple",
            "kind": "consumable",
            "description": "A fresh apple.",
            "stackable": True,
            "mobility": "movable",
            "capabilities": ["inspect", "eat"],
            "tags": ["food", "fruit"],
            "modules": {
                "physical": {"mass": None, "length": None, "width": None, "height": None},
                "stack": {"canonical_unit": "piece"},
                "nutrition": {
                    "basis_quantity": 1.0,
                    "unit": "piece",
                    "energy_kcal": 95.0,
                    "protein_g": 0.5,
                    "carbohydrate_g": 25.0,
                    "fat_g": 0.3,
                },
                "container": None,
                "resistance_training": None,
                "metrics": {},
            },
        },
        "instance": {"mode": "stack", "quantity": {"value": 6.0, "unit": "piece"}, "condition": "fresh"},
        "economic_policy": {
            "classification": "consumable_stock",
            "currency_code": "USD",
            "unit_value_minor": 125,
            "replacement_value_minor": None,
            "net_worth_treatment": "derived_stock",
            "included_in_parent_ref": None,
            "valuation_method": "creator_estimate",
        },
        "requirements": {"use": None},
        "relationships": {
            "located_at": None,
            "stored_in": None,
            "owned_by": None,
            "carried_by": None,
            "equipped_by": None,
        },
    }


def _sandbox_location(conn) -> str:
    proposal = build_creation_proposal(
        "location",
        identity={"name": "Item Test Location"},
        provenance_mode="manual",
        requested_by="test",
    )
    return str(activate_creation_proposal(conn, proposal)["object_id"])


def _sandbox_character(conn) -> str:
    proposal = build_creation_proposal(
        "character",
        identity={"name": "Item Test Character"},
        provenance_mode="manual",
        requested_by="test",
    )
    return str(activate_creation_proposal(conn, proposal)["object_id"])


def test_item_socket_is_registered_without_changing_character_contract() -> None:
    assert socket_definition("item").schema_version == 1
    assert socket_definition("item").required_identity_fields == ("name",)
    assert socket_definition("character").schema_version == 1
    # Location is intentionally the current development domain and has now
    # advanced to the explicit location-v2 contract.
    assert socket_definition("location").schema_version == 2


def test_single_unique_item_materializes_definition_instance_economy_and_event(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        item = create_sandbox_item(
            conn,
            _unique_training_item(),
            provenance={"mode": "manual", "requested_by": "test"},
        )
        after = canonical_state_fingerprint(conn)
        assert before == after
        assert item["definition"]["key"] == "equipment.training.adjustable_dumbbell"
        assert item["definition"]["modules"]["resistance_training"]["resistance_load"]["unit"] == "kg"
        assert item["instance"]["mode"] == "unique"
        assert item["economic_policy"]["classification"] == "standalone_asset"
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_events WHERE object_id=? AND event_type='sandbox_item_created'",
            (item["object_id"],),
        ).fetchone() is not None


def test_stack_item_materializes_quantity_without_character_runtime(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        item = create_sandbox_item(
            conn,
            _food_stack_item(),
            provenance={"mode": "manual", "requested_by": "test"},
        )
        assert item["instance"]["mode"] == "stack"
        assert item["instance"]["quantity"] == pytest.approx(6.0)
        assert item["instance"]["unit"] == "piece"
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_actor_runtime WHERE object_id=?",
            (item["object_id"],),
        ).fetchone() is None


def test_item_relationship_targets_must_be_same_sandbox_and_active(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        location_id = _sandbox_location(conn)
        owner_id = _sandbox_character(conn)
        value = _unique_training_item()
        value["relationships"]["located_at"] = location_id
        value["relationships"]["owned_by"] = owner_id
        item = create_sandbox_item(
            conn,
            value,
            provenance={"mode": "manual", "requested_by": "test"},
        )
        assert {row["relation_type"] for row in item["relations"]} == {"located_at", "owned_by"}


def test_item_relationship_target_type_contract_rejects_invalid_owner(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        location_id = _sandbox_location(conn)
        value = _unique_training_item()
        value["relationships"]["owned_by"] = location_id
        with pytest.raises(SandboxItemCreationError, match="owned_by target must be"):
            create_sandbox_item(
                conn,
                value,
                provenance={"mode": "manual", "requested_by": "test"},
            )


def test_duplicate_definition_key_reuses_definition_when_exactly_compatible(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        first = create_sandbox_item(conn, _unique_training_item(), provenance={"mode": "manual"})
        second = create_sandbox_item(conn, _unique_training_item(), provenance={"mode": "manual"})
        assert first["object_id"] != second["object_id"]
        assert first["definition"]["key"] == second["definition"]["key"]
        assert conn.execute(
            "SELECT COUNT(*) FROM creation_sandbox_item_definitions WHERE definition_key=?",
            (first["definition"]["key"],),
        ).fetchone()[0] == 1


def test_duplicate_definition_key_rejects_incompatible_redefinition_atomically(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        first = create_sandbox_item(conn, _unique_training_item(), provenance={"mode": "manual"})
        before_objects = conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]
        value = _unique_training_item()
        value["definition"]["name"] = "Conflicting Dumbbell"
        with pytest.raises(SandboxItemCreationError, match="already exists with different semantics"):
            create_sandbox_item(conn, value, provenance={"mode": "manual"})
        assert conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0] == before_objects
        assert get_sandbox_item(conn, first["object_id"])["definition"]["name"] == "Adjustable Dumbbell"


def test_item_readback_contains_derived_grade_but_persisted_definition_keeps_raw_truth(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        item = create_sandbox_item(conn, _unique_training_item(), provenance={"mode": "manual"})
        assert item["derived"]["grades"]["resistance_load"]["grade"] == "S"
        persisted = conn.execute(
            "SELECT derived_json FROM creation_sandbox_item_definitions WHERE sandbox_id=? AND definition_key=?",
            (item["sandbox_id"], item["definition"]["key"]),
        ).fetchone()
        assert json.loads(persisted["derived_json"])["grades"]["resistance_load"]["grade"] == "S"

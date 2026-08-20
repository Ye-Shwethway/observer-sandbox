from __future__ import annotations

from copy import deepcopy

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


def _empty_relationships() -> dict[str, str | None]:
    return {
        "located_at": None,
        "stored_in": None,
        "owned_by": None,
        "carried_by": None,
        "equipped_by": None,
    }


def _unique_training_item() -> dict[str, object]:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "training.dumbbell.55lb",
            "name": "55 lb Dumbbell",
            "kind": "equipment",
            "description": "A fixed-weight training dumbbell.",
            "stackable": False,
            "mobility": "movable",
            "capabilities": ["inspect", "train", "use"],
            "tags": ["training", "strength"],
            "modules": {
                "physical": {
                    "mass": {"value": 55, "unit": "lb"},
                    "length": None,
                    "width": None,
                    "height": None,
                },
                "resistance_training": {
                    "resistance_load": {"value": 55, "unit": "lb"},
                },
            },
        },
        "instance": {"mode": "unique"},
        "economic_policy": {
            "classification": "standalone_asset",
            "currency_code": "USD",
            "market_value_minor": 6500,
            "replacement_value_minor": 7000,
            "unit_value_minor": None,
            "unit_quantity": None,
            "unit_label": None,
            "net_worth_treatment": "independent",
            "included_in_parent_ref": None,
            "valuation_method": "creator_explicit",
        },
        "requirements": {"use": None},
        "relationships": _empty_relationships(),
    }


def _stack_food_item() -> dict[str, object]:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "food.apple.creator",
            "name": "Apple",
            "kind": "consumable",
            "description": "Fresh whole apples.",
            "stackable": True,
            "mobility": "movable",
            "capabilities": ["inspect", "eat"],
            "tags": ["food", "fruit"],
            "modules": {
                "stack": {"canonical_unit": "piece", "initial_quantity": 12},
                "nutrition": {
                    "basis_quantity": 1,
                    "unit": "piece",
                    "energy_kcal": 95,
                    "protein_g": 0.5,
                    "carbohydrate_g": 25,
                    "fat_g": 0.3,
                },
            },
        },
        "instance": {"mode": "stack", "quantity": 12, "unit": "piece"},
        "economic_policy": {
            "classification": "consumable_stock",
            "currency_code": "USD",
            "market_value_minor": None,
            "replacement_value_minor": None,
            "unit_value_minor": 100,
            "unit_quantity": 1,
            "unit_label": "piece",
            "net_worth_treatment": "derived_stock",
            "included_in_parent_ref": None,
            "valuation_method": "creator_explicit",
        },
        "requirements": {"use": None},
        "relationships": _empty_relationships(),
    }


def _sandbox_location(conn) -> str:
    proposal = build_creation_proposal(
        "location",
        identity={"name": "Item Test Room"},
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
    assert socket_definition("location").schema_version == 2


def test_single_unique_item_materializes_definition_instance_economy_and_event(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        item = create_sandbox_item(
            conn,
            _unique_training_item(),
            provenance_mode="manual",
            requested_by="creator-test",
        )
        after = canonical_state_fingerprint(conn)

        assert before == after
        assert item["creation_type"] == "item"
        assert item["item"]["definition"]["key"] == "training.dumbbell.55lb"
        assert item["item"]["instance"] == {"mode": "unique"}
        assert item["item"]["economic_policy"]["classification"] == "standalone_asset"
        assert item["item"]["derived"]["grades"]["resistance_load"]["grade"] == "S"
        assert conn.execute(
            "SELECT 1 FROM entities WHERE id=?", (item["object_id"],)
        ).fetchone() is None
        assert conn.execute(
            "SELECT 1 FROM economic_value_profiles WHERE subject_id=?", (item["object_id"],)
        ).fetchone() is None
        event = conn.execute(
            "SELECT event_type FROM creation_sandbox_events WHERE object_id=? ORDER BY id DESC LIMIT 1",
            (item["object_id"],),
        ).fetchone()
        assert event["event_type"] == "sandbox_item_materialized"


def test_stack_item_preserves_definition_vs_instance_semantics(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        item = create_sandbox_item(conn, _stack_food_item(), requested_by="creator-test")
        definition = conn.execute(
            "SELECT definition_key,stackable,modules_json FROM creation_sandbox_item_definitions WHERE sandbox_id=? AND definition_key=?",
            (item["sandbox_id"], "food.apple.creator"),
        ).fetchone()
        instance = conn.execute(
            "SELECT instance_mode,quantity,unit FROM creation_sandbox_item_instances WHERE object_id=?",
            (item["object_id"],),
        ).fetchone()

        assert definition["definition_key"] == "food.apple.creator"
        assert definition["stackable"] == 1
        assert instance["instance_mode"] == "stack"
        assert instance["quantity"] == pytest.approx(12.0)
        assert instance["unit"] == "piece"
        assert item["item"]["economic_policy"]["net_worth_treatment"] == "derived_stock"


def test_same_definition_can_back_multiple_instances_only_when_semantics_match(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        first = create_sandbox_item(conn, _unique_training_item())
        second = create_sandbox_item(conn, _unique_training_item())
        assert first["object_id"] != second["object_id"]
        assert conn.execute(
            "SELECT COUNT(*) AS n FROM creation_sandbox_item_definitions WHERE definition_key='training.dumbbell.55lb'"
        ).fetchone()["n"] == 1
        assert conn.execute(
            "SELECT COUNT(*) AS n FROM creation_sandbox_item_instances WHERE definition_key='training.dumbbell.55lb'"
        ).fetchone()["n"] == 2

        changed = _unique_training_item()
        changed["definition"]["description"] = "Conflicting semantics under the same stable key."
        before_objects = conn.execute(
            "SELECT COUNT(*) AS n FROM creation_sandbox_objects WHERE creation_type='item'"
        ).fetchone()["n"]
        with pytest.raises(SandboxItemCreationError, match="different semantics"):
            create_sandbox_item(conn, changed)
        after_objects = conn.execute(
            "SELECT COUNT(*) AS n FROM creation_sandbox_objects WHERE creation_type='item'"
        ).fetchone()["n"]
        assert after_objects == before_objects


def test_item_relations_materialize_only_to_valid_active_same_sandbox_targets(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        location_id = _sandbox_location(conn)
        owner_id = _sandbox_character(conn)
        payload = _unique_training_item()
        payload["relationships"]["located_at"] = location_id
        payload["relationships"]["owned_by"] = owner_id

        item = create_sandbox_item(conn, payload)
        relations = {(row["relation_type"], row["target_object_id"]) for row in item["resolved_relations"]}
        assert ("located_at", location_id) in relations
        assert ("owned_by", owner_id) in relations

        wrong = _unique_training_item()
        wrong["definition"]["key"] = "training.dumbbell.bad-target"
        wrong["relationships"]["located_at"] = owner_id
        with pytest.raises(SandboxItemCreationError, match="located_at"):
            create_sandbox_item(conn, wrong)


def test_stored_in_accepts_location_or_container_item_but_rejects_plain_item(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        location_id = _sandbox_location(conn)
        apple = _stack_food_item()
        apple["relationships"]["stored_in"] = location_id
        stored = create_sandbox_item(conn, apple)
        assert any(row["relation_type"] == "stored_in" for row in stored["resolved_relations"])

        plain = create_sandbox_item(conn, _unique_training_item())
        second = _stack_food_item()
        second["definition"]["key"] = "food.apple.bad-container"
        second["relationships"]["stored_in"] = plain["object_id"]
        with pytest.raises(SandboxItemCreationError, match="container Item"):
            create_sandbox_item(conn, second)


def test_invalid_relation_target_produces_zero_item_materialization(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        payload = _unique_training_item()
        payload["relationships"]["located_at"] = "sbx_location_missing"
        before = conn.execute(
            "SELECT COUNT(*) AS n FROM creation_sandbox_objects WHERE creation_type='item'"
        ).fetchone()["n"]

        with pytest.raises(SandboxItemCreationError, match="does not exist"):
            create_sandbox_item(conn, payload)

        after = conn.execute(
            "SELECT COUNT(*) AS n FROM creation_sandbox_objects WHERE creation_type='item'"
        ).fetchone()["n"]
        assert after == before
        assert conn.execute("SELECT COUNT(*) AS n FROM creation_sandbox_item_instances").fetchone()["n"] == 0
        assert conn.execute("SELECT COUNT(*) AS n FROM creation_sandbox_item_economic_profiles").fetchone()["n"] == 0


def test_get_sandbox_item_rejects_non_item_objects(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        location_id = _sandbox_location(conn)
        with pytest.raises(SandboxItemCreationError, match="not an Item"):
            get_sandbox_item(conn, location_id)


def test_item_materialization_tables_are_additive_and_global_schema_version_stays_21(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        tables = {
            row["name"]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'creation_sandbox_item_%'"
            ).fetchall()
        }
        assert tables == {
            "creation_sandbox_item_definitions",
            "creation_sandbox_item_instances",
            "creation_sandbox_item_economic_profiles",
        }
        assert conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()["value"] == "21"

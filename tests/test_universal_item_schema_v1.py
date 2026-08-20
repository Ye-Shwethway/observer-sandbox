from __future__ import annotations

import copy
import math
import sqlite3

import pytest

from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.db import migrate
from observer_sandbox.item_creation_schema import ItemSchemaError, validate_item_payload


def _relationships(**overrides: str | None) -> dict[str, str | None]:
    values: dict[str, str | None] = {
        "located_at": None,
        "stored_in": None,
        "owned_by": None,
        "carried_by": None,
        "equipped_by": None,
    }
    values.update(overrides)
    return values


def _standalone_policy(*, replacement_value_minor: int = 12000) -> dict[str, object]:
    return {
        "classification": "standalone_asset",
        "currency_code": "USD",
        "market_value_minor": None,
        "replacement_value_minor": replacement_value_minor,
        "unit_value_minor": None,
        "unit_quantity": None,
        "unit_label": None,
        "net_worth_treatment": "independent",
        "included_in_parent_ref": None,
        "valuation_method": "creator_estimate",
    }


def _dumbbell_payload(*, load_value: float = 55, load_unit: str = "lb") -> dict[str, object]:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "training.dumbbell.fixed_55",
            "name": "55 lb Fixed Dumbbell",
            "kind": "equipment",
            "description": "A fixed-weight dumbbell for resistance training.",
            "stackable": False,
            "mobility": "movable",
            "capabilities": ["inspect", "train", "use"],
            "tags": ["training", "dumbbell"],
            "modules": {
                "physical": {
                    "mass": {"value": load_value, "unit": load_unit},
                    "length": None,
                    "width": None,
                    "height": None,
                },
                "resistance_training": {
                    "resistance_load": {"value": load_value, "unit": load_unit},
                },
            },
        },
        "instance": {"mode": "unique"},
        "economic_policy": _standalone_policy(),
        "requirements": {
            "use": {
                "type": "minimum_grade",
                "domain": "character",
                "dimension": "strength",
                "minimum": "B",
            }
        },
        "relationships": _relationships(located_at="sbx_location_home_gym"),
    }


def _apple_payload() -> dict[str, object]:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "food.apple",
            "name": "Apple",
            "kind": "consumable",
            "description": "A fresh eating apple.",
            "stackable": True,
            "mobility": "movable",
            "capabilities": ["inspect", "eat"],
            "tags": ["fruit", "raw", "plant"],
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
            "unit_value_minor": 125,
            "unit_quantity": 1,
            "unit_label": "piece",
            "net_worth_treatment": "derived_stock",
            "included_in_parent_ref": None,
            "valuation_method": "creator_unit_estimate",
        },
        "requirements": {"use": None},
        "relationships": _relationships(stored_in="sbx_object_refrigerator", owned_by="sbx_location_estate"),
    }


def _container_payload() -> dict[str, object]:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "container.gym_bag",
            "name": "Gym Bag",
            "kind": "container",
            "description": "A movable training bag with represented internal capacity.",
            "stackable": False,
            "mobility": "movable",
            "capabilities": ["inspect", "store", "use"],
            "tags": ["bag", "training"],
            "modules": {
                "physical": {
                    "mass": {"value": 2.2, "unit": "lb"},
                    "length": {"value": 20, "unit": "in"},
                    "width": {"value": 10, "unit": "in"},
                    "height": {"value": 10, "unit": "in"},
                },
                "container": {"capacity_volume": {"value": 35, "unit": "l"}},
            },
        },
        "instance": {"mode": "unique"},
        "economic_policy": _standalone_policy(replacement_value_minor=6500),
        "requirements": {"use": None},
        "relationships": _relationships(owned_by="sbx_character_adrian"),
    }


def test_exact_item_schema_normalizes_unique_equipment_and_derives_grade() -> None:
    result = validate_item_payload(_dumbbell_payload())

    assert result["schema_version"] == "item-v1"
    assert result["definition"]["stackable"] is False
    assert result["instance"] == {"mode": "unique"}
    assert result["definition"]["modules"]["physical"]["mass"]["unit"] == "kg"
    assert result["definition"]["modules"]["resistance_training"]["resistance_load"]["unit"] == "kg"
    assert result["derived"]["grades"]["resistance_load"]["grade"] == "S"
    assert result["derived"]["grades"]["resistance_load"]["domain"] == "item"
    assert result["requirements"]["use"]["domain"] == "character"
    assert result["requirements"]["use"]["minimum"] == "B"


def test_imperial_and_metric_payloads_produce_equivalent_physical_truth_and_grade() -> None:
    imperial = validate_item_payload(_dumbbell_payload(load_value=55, load_unit="lb"))
    metric = validate_item_payload(_dumbbell_payload(load_value=24.94758035, load_unit="kg"))

    imperial_mass = imperial["definition"]["modules"]["physical"]["mass"]["value"]
    metric_mass = metric["definition"]["modules"]["physical"]["mass"]["value"]
    assert math.isclose(float(imperial_mass), float(metric_mass), rel_tol=0.0, abs_tol=1e-12)
    assert imperial["derived"]["grades"]["resistance_load"]["grade"] == metric["derived"]["grades"]["resistance_load"]["grade"] == "S"


def test_stackable_consumable_reuses_definition_stack_and_nutrition_semantics() -> None:
    result = validate_item_payload(_apple_payload())

    assert result["instance"] == {"mode": "stack", "quantity": 12.0, "unit": "piece"}
    assert result["definition"]["modules"]["nutrition"] == {
        "basis_quantity": 1.0,
        "unit": "piece",
        "energy_kcal": 95.0,
        "protein_g": 0.5,
        "carbohydrate_g": 25.0,
        "fat_g": 0.3,
    }
    assert result["economic_policy"]["classification"] == "consumable_stock"
    assert result["economic_policy"]["net_worth_treatment"] == "derived_stock"


def test_container_module_uses_normalized_volume_without_collapsing_storage_relation() -> None:
    result = validate_item_payload(_container_payload())

    capacity = result["definition"]["modules"]["container"]["capacity_volume"]
    assert capacity["unit"] == "m3"
    assert capacity["value"] == pytest.approx(0.035)
    assert result["relationships"]["stored_in"] is None
    assert result["relationships"]["owned_by"] == "sbx_character_adrian"


def test_unknown_top_level_core_module_and_capability_fields_fail_closed() -> None:
    payload = _dumbbell_payload()
    payload["surprise"] = True
    with pytest.raises(ItemSchemaError, match="unknown field"):
        validate_item_payload(payload)

    payload = _dumbbell_payload()
    payload["definition"]["mystery"] = 7
    with pytest.raises(ItemSchemaError, match="definition has unknown field"):
        validate_item_payload(payload)

    payload = _dumbbell_payload()
    payload["definition"]["modules"]["teleportation"] = {"range": 10}
    with pytest.raises(ItemSchemaError, match="unregistered module"):
        validate_item_payload(payload)

    payload = _dumbbell_payload()
    payload["definition"]["capabilities"].append("teleport")
    with pytest.raises(ItemSchemaError, match="unregistered capability"):
        validate_item_payload(payload)


def test_required_core_and_conditional_modules_fail_closed() -> None:
    payload = _dumbbell_payload()
    del payload["economic_policy"]
    with pytest.raises(ItemSchemaError, match="missing required field"):
        validate_item_payload(payload)

    payload = _dumbbell_payload()
    del payload["definition"]["modules"]["resistance_training"]
    with pytest.raises(ItemSchemaError, match="train capability requires"):
        validate_item_payload(payload)

    payload = _apple_payload()
    del payload["definition"]["modules"]["nutrition"]
    with pytest.raises(ItemSchemaError, match="eat capability requires"):
        validate_item_payload(payload)

    payload = _container_payload()
    del payload["definition"]["modules"]["container"]
    with pytest.raises(ItemSchemaError, match="store capability requires"):
        validate_item_payload(payload)


def test_unique_and_stackable_instance_semantics_cannot_conflict() -> None:
    payload = _dumbbell_payload()
    payload["definition"]["stackable"] = True
    with pytest.raises(ItemSchemaError, match="requires modules.stack"):
        validate_item_payload(payload)

    payload = _apple_payload()
    payload["instance"] = {"mode": "unique"}
    with pytest.raises(ItemSchemaError, match="instance"):
        validate_item_payload(payload)

    payload = _apple_payload()
    payload["instance"]["quantity"] = 11
    with pytest.raises(ItemSchemaError, match="must match modules.stack.initial_quantity"):
        validate_item_payload(payload)


def test_economic_policy_is_mandatory_and_coherent() -> None:
    payload = _apple_payload()
    payload["economic_policy"]["unit_value_minor"] = None
    with pytest.raises(ItemSchemaError, match="consumable_stock requires"):
        validate_item_payload(payload)

    payload = _apple_payload()
    payload["economic_policy"]["net_worth_treatment"] = "independent"
    with pytest.raises(ItemSchemaError, match="requires derived_stock"):
        validate_item_payload(payload)

    payload = _dumbbell_payload()
    payload["economic_policy"]["net_worth_treatment"] = "included_in_parent"
    with pytest.raises(ItemSchemaError, match="requires economic_policy.included_in_parent_ref"):
        validate_item_payload(payload)

    payload = _dumbbell_payload()
    payload["economic_policy"] = {
        "classification": "economically_immaterial",
        "currency_code": None,
        "market_value_minor": None,
        "replacement_value_minor": None,
        "unit_value_minor": None,
        "unit_quantity": None,
        "unit_label": None,
        "net_worth_treatment": "excluded",
        "included_in_parent_ref": None,
        "valuation_method": "explicit_policy",
    }
    assert validate_item_payload(payload)["economic_policy"]["classification"] == "economically_immaterial"


def test_item_grade_and_use_requirement_remain_separate_contracts() -> None:
    payload = _dumbbell_payload()
    payload["requirements"]["use"]["minimum"] = "A"
    result = validate_item_payload(payload)

    assert result["derived"]["grades"]["resistance_load"]["grade"] == "S"
    assert result["requirements"]["use"] == {
        "type": "minimum_grade",
        "domain": "character",
        "dimension": "strength",
        "minimum": "A",
    }

    payload["requirements"]["use"]["minimum"] = "Z"
    with pytest.raises(ItemSchemaError, match="Unknown grade"):
        validate_item_payload(payload)


def test_definition_identity_does_not_encode_current_owner_or_location() -> None:
    payload = _dumbbell_payload()
    payload["relationships"]["owned_by"] = "sbx_character_adrian"
    result = validate_item_payload(payload)

    assert "owned_by" not in result["definition"]
    assert "located_at" not in result["definition"]
    assert result["relationships"]["owned_by"] == "sbx_character_adrian"
    assert result["relationships"]["located_at"] == "sbx_location_home_gym"


def test_current_physical_placement_modes_are_mutually_exclusive() -> None:
    payload = _dumbbell_payload()
    payload["relationships"]["carried_by"] = "sbx_character_adrian"

    with pytest.raises(ItemSchemaError, match="only one current physical placement mode"):
        validate_item_payload(payload)


def test_manual_and_ai_shaped_payloads_converge_on_same_normalized_contract() -> None:
    manual = _container_payload()
    ai = {
        "relationships": copy.deepcopy(manual["relationships"]),
        "requirements": copy.deepcopy(manual["requirements"]),
        "economic_policy": copy.deepcopy(manual["economic_policy"]),
        "instance": copy.deepcopy(manual["instance"]),
        "definition": copy.deepcopy(manual["definition"]),
        "schema_version": manual["schema_version"],
    }

    assert validate_item_payload(manual) == validate_item_payload(ai)


def test_validation_is_pure_and_does_not_mutate_canonical_database_state() -> None:
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    migrate(conn)
    before = canonical_state_fingerprint(conn)

    validate_item_payload(_dumbbell_payload())
    validate_item_payload(_apple_payload())
    validate_item_payload(_container_payload())

    assert canonical_state_fingerprint(conn) == before

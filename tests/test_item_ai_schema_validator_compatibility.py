from copy import deepcopy

import pytest

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import (
    canonicalize_ai_item_batch_fill,
    canonicalize_ai_item_fill,
    item_ai_fill_schema,
)
from observer_sandbox.item_creation_schema import (
    ITEM_CAPABILITIES,
    ITEM_KINDS,
    ITEM_MOBILITY,
    ITEM_MODULES,
    ItemSchemaError,
    validate_item_payload,
)
from observer_sandbox.item_metrics import DEFAULT_ITEM_METRIC_REGISTRY


def test_ai_schema_registry_surfaces_match_validator_registries():
    schema = item_ai_fill_schema()
    definition = schema["properties"]["definition"]["properties"]
    modules = definition["modules"]["properties"]

    assert set(definition["kind"]["enum"]) == set(ITEM_KINDS)
    assert set(definition["mobility"]["enum"]) == set(ITEM_MOBILITY)
    assert set(definition["capabilities"]["items"]["enum"]) == set(ITEM_CAPABILITIES)
    assert set(modules) == set(ITEM_MODULES)

    metrics_any_of = modules["metrics"]["anyOf"]
    metric_object = next(branch for branch in metrics_any_of if branch.get("type") == "object")
    assert set(metric_object["properties"]) == set(DEFAULT_ITEM_METRIC_REGISTRY.metric_ids())


def test_human_readable_token_fields_canonicalize_before_strict_validation():
    payload = manual_item_template()
    payload["definition"]["key"] = "LED Camping Flashlight 1000"
    payload["definition"]["name"] = "LED Camping Flashlight"
    payload["definition"]["tags"] = [
        "Camping Gear",
        "LED Light",
        "1000 Lumens",
        "Water Resistant / Outdoor",
        "Camping Gear",
    ]
    payload["economic_policy"]["valuation_method"] = "AI Estimate"

    candidate = canonicalize_ai_item_fill(payload)
    normalized = validate_item_payload(candidate)

    assert candidate["definition"]["key"] == "led_camping_flashlight_1000"
    assert candidate["definition"]["tags"] == [
        "camping_gear",
        "led_light",
        "tag_1000_lumens",
        "water_resistant_outdoor",
    ]
    assert normalized["economic_policy"]["valuation_method"] == "ai_estimate"


def test_empty_physical_and_metrics_slots_are_removed_before_validation():
    payload = manual_item_template()
    payload["definition"]["modules"] = {
        "physical": {"mass": None, "length": None, "width": None, "height": None},
        "stack": None,
        "nutrition": None,
        "container": None,
        "resistance_training": None,
        "metrics": {metric_id: None for metric_id in DEFAULT_ITEM_METRIC_REGISTRY.metric_ids()},
    }
    payload["instance"] = {"mode": "unique", "quantity": None, "unit": None}

    candidate = canonicalize_ai_item_fill(payload)
    normalized = validate_item_payload(candidate)

    assert candidate["definition"]["modules"] == {}
    assert candidate["instance"] == {"mode": "unique"}
    assert normalized["definition"]["modules"] == {}


def test_explicit_non_stackable_drops_accidental_stack_slot():
    payload = manual_item_template()
    payload["definition"]["stackable"] = False
    payload["definition"]["modules"]["stack"] = {"canonical_unit": "item", "initial_quantity": 1}
    payload["instance"] = {"mode": "unique", "quantity": None, "unit": None}

    candidate = canonicalize_ai_item_fill(payload)
    normalized = validate_item_payload(candidate)

    assert "stack" not in candidate["definition"]["modules"]
    assert candidate["instance"] == {"mode": "unique"}
    assert normalized["definition"]["stackable"] is False


def test_stack_module_aligns_stack_instance_and_nutrition_units_when_stackable():
    payload = manual_item_template()
    payload["definition"].update(
        {
            "key": "Energy Bars",
            "name": "Energy Bars",
            "kind": "consumable",
            "stackable": True,
            "capabilities": ["inspect", "use"],
            "tags": ["Energy Bar", "Trail Food"],
            "modules": {
                "physical": None,
                "stack": {"canonical_unit": "Bars", "initial_quantity": 6},
                "nutrition": {
                    "basis_quantity": 1,
                    "unit": "Serving",
                    "energy_kcal": 220,
                    "protein_g": 8,
                    "carbohydrate_g": 28,
                    "fat_g": 9,
                },
                "container": None,
                "resistance_training": None,
                "metrics": None,
            },
        }
    )
    payload["instance"] = {"mode": "unique", "quantity": None, "unit": None}
    payload["economic_policy"] = {
        "classification": "consumable_stock",
        "currency_code": "usd",
        "market_value_minor": None,
        "replacement_value_minor": None,
        "unit_value_minor": 150,
        "unit_quantity": 1,
        "unit_label": "Each Bar",
        "net_worth_treatment": "derived_stock",
        "included_in_parent_ref": None,
        "valuation_method": "AI Estimate",
    }

    candidate = canonicalize_ai_item_fill(payload)
    normalized = validate_item_payload(candidate)

    assert candidate["definition"]["stackable"] is True
    assert candidate["definition"]["modules"]["stack"]["canonical_unit"] == "bars"
    assert candidate["definition"]["modules"]["nutrition"]["unit"] == "bars"
    assert candidate["instance"] == {"mode": "stack", "quantity": 6, "unit": "bars"}
    assert candidate["economic_policy"]["currency_code"] == "USD"
    assert candidate["economic_policy"]["unit_label"] == "bars"
    assert normalized["instance"]["quantity"] == 6


def test_stack_instance_can_reconstruct_missing_stack_module_without_inventing_quantity():
    payload = manual_item_template()
    payload["definition"]["stackable"] = True
    payload["definition"]["modules"] = {
        "physical": payload["definition"]["modules"]["physical"],
        "stack": None,
        "nutrition": None,
        "container": None,
        "resistance_training": None,
        "metrics": None,
    }
    payload["instance"] = {"mode": "stack", "quantity": 4, "unit": "Battery Cells"}

    candidate = canonicalize_ai_item_fill(payload)
    normalized = validate_item_payload(candidate)

    assert candidate["definition"]["modules"]["stack"] == {
        "canonical_unit": "battery_cells",
        "initial_quantity": 4,
    }
    assert normalized["instance"] == {"mode": "stack", "quantity": 4.0, "unit": "battery_cells"}


def test_module_capabilities_are_reconciled_both_directions():
    payload = manual_item_template()
    payload["definition"]["capabilities"] = ["inspect", "use", "eat", "store", "train"]
    payload["definition"]["modules"]["resistance_training"] = {
        "resistance_load": {"value": 55, "unit": "lb"}
    }

    candidate = canonicalize_ai_item_fill(payload)
    normalized = validate_item_payload(candidate)

    assert "train" in candidate["definition"]["capabilities"]
    assert "eat" not in candidate["definition"]["capabilities"]
    assert "store" not in candidate["definition"]["capabilities"]
    assert "train" in normalized["definition"]["capabilities"]


def test_container_module_adds_store_capability_and_validates():
    payload = manual_item_template()
    payload["definition"]["capabilities"] = ["inspect", "use"]
    payload["definition"]["modules"]["container"] = {
        "capacity_volume": {"value": 30, "unit": "l"}
    }

    candidate = canonicalize_ai_item_fill(payload)
    normalized = validate_item_payload(candidate)

    assert "store" in candidate["definition"]["capabilities"]
    assert "container" in normalized["definition"]["modules"]


def test_batch_human_refs_and_parent_economic_refs_share_one_alias_map():
    backpack = manual_item_template()
    backpack["definition"]["key"] = "30 L Hiking Backpack"
    backpack["definition"]["name"] = "30 L Hiking Backpack"
    backpack["definition"]["capabilities"] = ["inspect", "use"]
    backpack["definition"]["modules"]["container"] = {
        "capacity_volume": {"value": 30, "unit": "l"}
    }

    pouch = manual_item_template()
    pouch["definition"]["key"] = "Repair Pouch"
    pouch["definition"]["name"] = "Repair Pouch"
    pouch["relationships"]["stored_in"] = "30 L Hiking Backpack"
    pouch["economic_policy"].update(
        {
            "classification": "component",
            "net_worth_treatment": "included_in_parent",
            "included_in_parent_ref": "$30 L Hiking Backpack",
        }
    )

    candidate = canonicalize_ai_item_batch_fill(
        {
            "items": [
                {"ref": "30 L Hiking Backpack", "payload": backpack},
                {"ref": "Repair Pouch", "payload": pouch},
            ]
        }
    )

    assert candidate["items"][0]["ref"] == "item_30_l_hiking_backpack"
    child = candidate["items"][1]["payload"]
    assert child["relationships"]["stored_in"] == "$item_30_l_hiking_backpack"
    assert child["economic_policy"]["included_in_parent_ref"] == "$item_30_l_hiking_backpack"
    validate_item_payload(candidate["items"][0]["payload"])
    validate_item_payload(child)


def test_non_mechanical_semantic_gaps_still_fail_closed():
    payload = manual_item_template()
    payload["definition"]["modules"]["nutrition"] = {
        "basis_quantity": 1,
        "unit": "serving",
        "energy_kcal": 100,
        "protein_g": 1,
        "carbohydrate_g": 20,
        "fat_g": 1,
    }
    payload["definition"]["capabilities"] = ["inspect", "use"]

    candidate = canonicalize_ai_item_fill(payload)
    with pytest.raises(ItemSchemaError, match="nutrition requires a stackable Item"):
        validate_item_payload(candidate)

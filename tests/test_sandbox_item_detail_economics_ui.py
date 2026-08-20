from __future__ import annotations

import copy

import observer_sandbox.creator_studio_item as single_studio
import observer_sandbox.creator_studio_item_batch as batch_studio
from observer_sandbox.item_creation_economics import DEFAULT_ITEM_ECONOMIC_INSTRUCTION
from observer_sandbox.telegram_world_layers_item_extension import approved_item_detail_text


def _energy_bar() -> dict:
    return {
        "object_id": "sbx_item_energy",
        "lifecycle_status": "active",
        "resolved_relations": [],
        "item": {
            "schema_version": "item-v1",
            "definition": {
                "key": "energy-bar",
                "name": "Energy Bar",
                "kind": "consumable",
                "description": "Compact energy bar.",
                "stackable": True,
                "mobility": "movable",
                "capabilities": ["eat"],
                "tags": ["food"],
                "modules": {
                    "nutrition": {
                        "basis_quantity": 1,
                        "unit": "bar",
                        "energy_kcal": 200,
                        "protein_g": 10,
                        "carbohydrate_g": 25,
                        "fat_g": 7,
                    },
                    "physical": {
                        "mass": {"value": 0.05, "unit": "kg"},
                        "length": {"value": 10, "unit": "cm"},
                        "width": {"value": 5, "unit": "cm"},
                        "height": {"value": 2, "unit": "cm"},
                    },
                    "stack": {"canonical_unit": "bar", "initial_quantity": 6},
                },
            },
            "instance": {"mode": "stack", "quantity": 6, "unit": "bar"},
            "economic_policy": {
                "classification": "economically_immaterial",
                "currency_code": None,
                "market_value_minor": None,
                "replacement_value_minor": None,
                "unit_value_minor": None,
                "unit_quantity": None,
                "unit_label": None,
                "net_worth_treatment": "excluded",
                "included_in_parent_ref": None,
                "valuation_method": "creator_explicit",
            },
            "requirements": {"use": None},
            "relationships": {
                "located_at": None,
                "stored_in": None,
                "owned_by": None,
                "carried_by": None,
                "equipped_by": None,
            },
        },
    }


def test_approved_legacy_energy_bar_surfaces_nutrition_and_clear_missing_value():
    text = approved_item_detail_text(None, _energy_bar())
    assert "Quantity    6 bar" in text
    assert "Value not assigned" in text
    assert "NUTRIENT FACTS · DEFAULT PORTION" in text
    assert "Energy      200 kcal" in text
    assert "Protein     10 g" in text
    assert "Carbs       25 g" in text
    assert "Fat         7 g" in text
    assert "Mass        0.05 kg" in text
    assert "Size        10 × 5 × 2 cm" in text
    assert "economically immaterial" not in text.lower()
    assert "sbx_item_energy" not in text


def test_approved_valued_energy_bar_derives_current_stock_and_unit_value():
    value = copy.deepcopy(_energy_bar())
    value["item"]["economic_policy"].update({
        "classification": "consumable_stock",
        "currency_code": "USD",
        "unit_value_minor": 150,
        "unit_quantity": 1,
        "unit_label": "bar",
        "net_worth_treatment": "derived_stock",
        "valuation_method": "ai_estimate",
    })
    text = approved_item_detail_text(None, value)
    assert "Current stock  $9.00" in text
    assert "Unit value     $1.50 / 1 bar" in text


def test_single_and_batch_share_market_value_creation_instruction():
    assert single_studio.DEFAULT_ITEM_ECONOMIC_INSTRUCTION == DEFAULT_ITEM_ECONOMIC_INSTRUCTION
    assert batch_studio.DEFAULT_ITEM_ECONOMIC_INSTRUCTION == DEFAULT_ITEM_ECONOMIC_INSTRUCTION
    assert "standalone_asset" in DEFAULT_ITEM_ECONOMIC_INSTRUCTION
    assert "consumable_stock" in DEFAULT_ITEM_ECONOMIC_INSTRUCTION
    assert "USD" in DEFAULT_ITEM_ECONOMIC_INSTRUCTION
    assert "economically immaterial merely because the Creator did not state a price" in DEFAULT_ITEM_ECONOMIC_INSTRUCTION
    assert "Physical storage inside another Item does not make the stored Item an economic component" in DEFAULT_ITEM_ECONOMIC_INSTRUCTION

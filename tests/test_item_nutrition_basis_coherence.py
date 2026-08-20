from copy import deepcopy

import pytest

import observer_sandbox.creator_studio_item as item_studio
from observer_sandbox.creator_studio_item import ai_item_draft, manual_item_template
from observer_sandbox.db import connect
from observer_sandbox.item_creation_realism import ItemRealismError, validate_item_default_realism
from observer_sandbox.runtime import initialize


def _energy_bars(*, basis_quantity: float) -> dict:
    payload = manual_item_template()
    payload["definition"].update(
        {
            "key": "energy_bars",
            "name": "Energy Bars",
            "kind": "consumable",
            "stackable": True,
            "capabilities": ["eat"],
            "modules": {
                "physical": {
                    "mass": {"value": 50, "unit": "g"},
                    "length": {"value": 12, "unit": "cm"},
                    "width": {"value": 7, "unit": "cm"},
                    "height": {"value": 2, "unit": "cm"},
                },
                "stack": {"canonical_unit": "bar", "initial_quantity": 12},
                "nutrition": {
                    "basis_quantity": basis_quantity,
                    "unit": "bar",
                    "energy_kcal": 220,
                    "protein_g": 8,
                    "carbohydrate_g": 28,
                    "fat_g": 10,
                },
            },
        }
    )
    payload["instance"] = {"mode": "stack", "quantity": 12, "unit": "bar"}
    payload["economic_policy"] = {
        "classification": "consumable_stock",
        "currency_code": "USD",
        "market_value_minor": None,
        "replacement_value_minor": None,
        "unit_value_minor": 250,
        "unit_quantity": 1,
        "unit_label": "bar",
        "net_worth_treatment": "derived_stock",
        "included_in_parent_ref": None,
        "valuation_method": "ai_estimate",
    }
    return payload


def test_live_style_mass_copied_into_bar_basis_is_rejected():
    payload = _energy_bars(basis_quantity=50)

    with pytest.raises(ItemRealismError, match="nutrition basis_quantity exceeds"):
        validate_item_default_realism(payload)


def test_per_bar_nutrition_basis_passes():
    validate_item_default_realism(_energy_bars(basis_quantity=1))


def test_nutrition_basis_may_cover_multiple_units_within_stack():
    validate_item_default_realism(_energy_bars(basis_quantity=2))


def test_item_ai_self_correction_can_fix_bad_nutrition_basis(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    bad = _energy_bars(basis_quantity=50)
    good = _energy_bars(basis_quantity=1)
    calls = []

    monkeypatch.setattr(
        item_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "p", "model_id": "m", "parameters": {}},
    )

    def fake_generate(conn, **kwargs):
        calls.append(kwargs["prompt"])
        return deepcopy(bad if len(calls) == 1 else good)

    monkeypatch.setattr(item_studio, "generate_structured", fake_generate)

    with connect(db) as conn:
        draft = ai_item_draft(conn, 91, "Create twelve peanut butter energy bars")

    assert draft["draft_mode"] == "ai_generated"
    assert len(calls) == 2
    assert "nutrition basis_quantity exceeds" in calls[1]
    stored = draft["proposal"]["properties"]["item_payload"]
    assert stored["definition"]["modules"]["nutrition"]["basis_quantity"] == 1

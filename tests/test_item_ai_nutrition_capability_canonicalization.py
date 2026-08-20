from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill
from observer_sandbox.item_creation_schema import validate_item_payload


def test_nutrition_module_adds_eat_capability_for_stackable_item():
    payload = manual_item_template()
    payload["definition"]["stackable"] = True
    payload["definition"]["capabilities"] = ["inspect", "use"]
    payload["definition"]["modules"]["stack"] = {
        "canonical_unit": "bar",
        "initial_quantity": 6,
    }
    payload["definition"]["modules"]["nutrition"] = {
        "basis_quantity": 1,
        "unit": "bar",
        "energy_kcal": 220,
        "protein_g": 8,
        "carbohydrate_g": 30,
        "fat_g": 8,
    }
    payload["instance"] = {"mode": "stack", "quantity": 6, "unit": "bar"}
    payload["economic_policy"].update({
        "classification": "consumable_stock",
        "currency_code": "USD",
        "market_value_minor": None,
        "replacement_value_minor": None,
        "unit_value_minor": 150,
        "unit_quantity": 1,
        "unit_label": "bar",
        "net_worth_treatment": "derived_stock",
        "included_in_parent_ref": None,
        "valuation_method": "ai_estimate",
    })

    canonical = canonicalize_ai_item_fill(payload)

    assert "eat" in canonical["definition"]["capabilities"]
    validate_item_payload(canonical)

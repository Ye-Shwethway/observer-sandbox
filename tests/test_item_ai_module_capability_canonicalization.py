from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill
from observer_sandbox.item_creation_schema import validate_item_payload


def test_resistance_training_module_adds_train_capability():
    payload = manual_item_template()
    payload["definition"]["capabilities"] = ["inspect", "use"]
    payload["definition"]["modules"]["resistance_training"] = {
        "resistance_load": {"value": 55, "unit": "lb"}
    }

    canonical = canonicalize_ai_item_fill(payload)

    assert "train" in canonical["definition"]["capabilities"]
    validate_item_payload(canonical)


def test_container_module_adds_store_capability():
    payload = manual_item_template()
    payload["definition"]["capabilities"] = ["inspect", "use"]
    payload["definition"]["modules"]["container"] = {
        "capacity_volume": {"value": 30, "unit": "l"}
    }

    canonical = canonicalize_ai_item_fill(payload)

    assert "store" in canonical["definition"]["capabilities"]
    validate_item_payload(canonical)

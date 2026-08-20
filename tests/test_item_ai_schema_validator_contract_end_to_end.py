from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import canonicalize_ai_item_batch_fill
from observer_sandbox.item_creation_schema import validate_item_payload


def test_batch_schema_shaped_items_canonicalize_into_validator_accepted_payloads():
    first = manual_item_template()
    first["definition"]["key"] = "LED Camping Flashlight"
    first["definition"]["name"] = "LED Camping Flashlight"
    first["definition"]["tags"] = ["Camping Gear", "LED", "Water Resistant / Outdoor"]

    second = manual_item_template()
    second["definition"]["key"] = "Adjustable Dumbbell"
    second["definition"]["name"] = "Adjustable Dumbbell"
    second["definition"]["capabilities"] = ["inspect", "use"]
    second["definition"]["modules"]["resistance_training"] = {
        "resistance_load": {"value": 55, "unit": "lb"}
    }

    batch = canonicalize_ai_item_batch_fill(
        {
            "items": [
                {"ref": "LED Camping Flashlight", "payload": first},
                {"ref": "Adjustable Dumbbell", "payload": second},
            ]
        }
    )

    assert batch["items"][0]["ref"] == "led_camping_flashlight"
    assert "train" in batch["items"][1]["payload"]["definition"]["capabilities"]
    for entry in batch["items"]:
        validate_item_payload(entry["payload"])

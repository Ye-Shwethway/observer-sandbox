from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill
from observer_sandbox.item_creation_schema import validate_item_payload


def test_plain_human_labels_are_normalized_before_validation():
    payload = manual_item_template()
    payload["definition"]["key"] = "LED Camping Flashlight"
    payload["definition"]["tags"] = ["Outdoor Gear", "Water Resistant / Outdoor"]
    candidate = canonicalize_ai_item_fill(payload)
    validate_item_payload(candidate)

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill
from observer_sandbox.item_creation_schema import validate_item_payload


def test_live_style_human_readable_tags_do_not_reach_validator_unmodified():
    payload = manual_item_template()
    payload["definition"]["name"] = "LED Camping Flashlight"
    payload["definition"]["tags"] = [
        "camping",
        "flashlight",
        "LED",
        "Water Resistant / Outdoor",
    ]

    candidate = canonicalize_ai_item_fill(payload)
    normalized = validate_item_payload(candidate)

    assert candidate["definition"]["tags"] == [
        "camping",
        "flashlight",
        "led",
        "water_resistant_outdoor",
    ]
    assert normalized["definition"]["tags"] == candidate["definition"]["tags"]

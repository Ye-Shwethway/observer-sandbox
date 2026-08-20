from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.db import connect
from observer_sandbox.item_ai_contract import canonicalize_ai_item_batch_fill
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import preview_sandbox_item_batch


def _item(key: str, name: str):
    payload = manual_item_template()
    payload["definition"]["key"] = key
    payload["definition"]["name"] = name
    return payload


def test_human_readable_batch_refs_are_canonicalized_with_local_relationships(tmp_path):
    backpack = _item("hiking_backpack", "30 L Hiking Backpack")
    backpack["definition"]["capabilities"] = ["inspect", "use", "store"]
    backpack["definition"]["modules"]["container"] = {
        "capacity_volume": {"value": 30, "unit": "l"}
    }

    flashlight = _item("led_camping_flashlight", "LED Camping Flashlight")
    flashlight["relationships"]["stored_in"] = "30 L Hiking Backpack"

    power_bank = _item("portable_power_bank", "Portable Power Bank")
    power_bank["relationships"]["stored_in"] = "$30 L Hiking Backpack"

    dumbbell = _item("adjustable_dumbbell", "Adjustable Dumbbell")
    dry_bag = _item("waterproof_dry_bag", "Waterproof Dry Bag")

    candidate = canonicalize_ai_item_batch_fill({
        "items": [
            {"ref": "LED Camping Flashlight", "payload": flashlight},
            {"ref": "30 L Hiking Backpack", "payload": backpack},
            {"ref": "Portable Power Bank", "payload": power_bank},
            {"ref": "Adjustable Dumbbell", "payload": dumbbell},
            {"ref": "Waterproof Dry Bag", "payload": dry_bag},
        ]
    })

    assert [entry["ref"] for entry in candidate["items"]] == [
        "led_camping_flashlight",
        "item_30_l_hiking_backpack",
        "portable_power_bank",
        "adjustable_dumbbell",
        "waterproof_dry_bag",
    ]
    assert candidate["items"][0]["payload"]["relationships"]["stored_in"] == "$item_30_l_hiking_backpack"
    assert candidate["items"][2]["payload"]["relationships"]["stored_in"] == "$item_30_l_hiking_backpack"

    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        preview = preview_sandbox_item_batch(conn, candidate["items"])
    assert preview["count"] == 5

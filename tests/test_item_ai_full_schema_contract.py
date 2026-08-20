from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import (
    canonicalize_ai_item_batch_fill,
    canonicalize_ai_item_fill,
    item_ai_fill_schema,
    item_batch_ai_fill_schema,
)
from observer_sandbox.item_creation_schema import validate_item_payload


def test_single_item_ai_schema_is_complete_not_generic_object():
    schema = item_ai_fill_schema()
    assert schema["additionalProperties"] is False
    assert schema["required"] == [
        "schema_version", "definition", "instance", "economic_policy", "requirements", "relationships"
    ]
    definition = schema["properties"]["definition"]
    assert definition["required"] == [
        "key", "name", "kind", "description", "stackable", "mobility", "capabilities", "tags", "modules"
    ]
    modules = definition["properties"]["modules"]
    assert modules["required"] == ["physical", "stack", "nutrition", "container", "resistance_training"]
    assert modules["properties"]["container"]["anyOf"][1] == {"type": "null"}
    relationships = schema["properties"]["relationships"]
    assert relationships["required"] == ["located_at", "stored_in", "owned_by", "carried_by", "equipped_by"]


def test_batch_members_reuse_exact_single_item_schema():
    single = item_ai_fill_schema()
    batch = item_batch_ai_fill_schema()
    payload = batch["properties"]["items"]["items"]["properties"]["payload"]
    assert payload == single


def test_full_ai_fill_null_placeholders_canonicalize_to_valid_sparse_item():
    payload = manual_item_template()
    payload["definition"]["modules"] = {
        "physical": payload["definition"]["modules"]["physical"],
        "stack": None,
        "nutrition": None,
        "container": None,
        "resistance_training": None,
    }
    payload["instance"] = {"mode": "unique", "quantity": None, "unit": None}

    canonical = canonicalize_ai_item_fill(payload)
    assert set(canonical["definition"]["modules"]) == {"physical"}
    assert canonical["instance"] == {"mode": "unique"}
    validate_item_payload(canonical)


def test_batch_ai_bare_stored_in_ref_normalizes_to_explicit_local_ref():
    backpack = manual_item_template()
    backpack["definition"]["key"] = "backpack"
    backpack["definition"]["name"] = "Backpack"
    backpack["definition"]["modules"]["container"] = {
        "capacity_volume": {"value": 30, "unit": "l"}
    }

    bars = manual_item_template()
    bars["definition"]["key"] = "energy_bars"
    bars["definition"]["name"] = "Energy Bars"
    bars["relationships"]["stored_in"] = "backpack"

    candidate = canonicalize_ai_item_batch_fill({
        "items": [
            {"ref": "backpack", "payload": backpack},
            {"ref": "energy_bars", "payload": bars},
        ]
    })

    assert candidate["items"][1]["payload"]["relationships"]["stored_in"] == "$backpack"


def test_batch_ai_unknown_bare_stored_in_target_is_not_guessed():
    payload = manual_item_template()
    payload["relationships"]["stored_in"] = "garage_shelf"

    candidate = canonicalize_ai_item_batch_fill({
        "items": [{"ref": "flashlight", "payload": payload}]
    })

    assert candidate["items"][0]["payload"]["relationships"]["stored_in"] == "garage_shelf"

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.db import connect
from observer_sandbox.item_ai_contract import (
    canonicalize_ai_item_batch_fill,
    canonicalize_ai_item_fill,
    item_ai_fill_schema,
    item_batch_ai_fill_schema,
)
from observer_sandbox.item_creation_schema import validate_item_payload
from observer_sandbox.item_metrics import DEFAULT_ITEM_METRIC_REGISTRY
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import preview_sandbox_item_batch


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
    assert modules["required"] == ["physical", "stack", "nutrition", "container", "resistance_training", "metrics"]
    assert modules["properties"]["container"]["anyOf"][1] == {"type": "null"}
    metrics = modules["properties"]["metrics"]["anyOf"][0]
    assert set(metrics["properties"]) == set(DEFAULT_ITEM_METRIC_REGISTRY.metric_ids())
    assert metrics["additionalProperties"] is False
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
        "metrics": {metric_id: None for metric_id in DEFAULT_ITEM_METRIC_REGISTRY.metric_ids()},
    }
    payload["instance"] = {"mode": "unique", "quantity": None, "unit": None}

    canonical = canonicalize_ai_item_fill(payload)
    assert set(canonical["definition"]["modules"]) == {"physical"}
    assert canonical["instance"] == {"mode": "unique"}
    validate_item_payload(canonical)


def test_immaterial_ai_fill_empty_valuation_method_uses_canonical_policy_default():
    payload = manual_item_template()
    payload["economic_policy"]["valuation_method"] = ""

    canonical = canonicalize_ai_item_fill(payload)

    assert canonical["economic_policy"]["valuation_method"] == "creator_explicit"
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


def test_camping_batch_ai_boundary_normalization_reaches_whole_graph_preview(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    backpack = manual_item_template()
    backpack["definition"]["key"] = "backpack"
    backpack["definition"]["name"] = "Backpack"
    backpack["definition"]["capabilities"] = ["inspect", "use", "store"]
    backpack["definition"]["modules"] = {
        "physical": backpack["definition"]["modules"]["physical"],
        "stack": {"canonical_unit": "item", "initial_quantity": 1},
        "nutrition": None,
        "container": {"capacity_volume": {"value": 30, "unit": "l"}},
        "resistance_training": None,
        "metrics": None,
    }
    backpack["economic_policy"]["valuation_method"] = ""
    backpack["instance"] = {"mode": "unique", "quantity": None, "unit": None}

    bars = manual_item_template()
    bars["definition"].update({
        "key": "energy_bars",
        "name": "Energy Bars",
        "kind": "consumable",
        "stackable": True,
        "capabilities": ["inspect", "eat", "use"],
    })
    bars["definition"]["modules"] = {
        "physical": None,
        "stack": {"canonical_unit": "bar", "initial_quantity": 6},
        "nutrition": {
            "basis_quantity": 1,
            "unit": "bar",
            "energy_kcal": 200,
            "protein_g": 5,
            "carbohydrate_g": 30,
            "fat_g": 7,
        },
        "container": None,
        "resistance_training": None,
        "metrics": None,
    }
    bars["instance"] = {"mode": "stack", "quantity": 6, "unit": "bar"}
    bars["economic_policy"]["valuation_method"] = ""
    bars["relationships"]["stored_in"] = "backpack"

    candidate = canonicalize_ai_item_batch_fill({
        "items": [
            {"ref": "backpack", "payload": backpack},
            {"ref": "energy_bars", "payload": bars},
        ]
    })

    assert candidate["items"][0]["payload"]["definition"]["modules"].get("stack") is None
    assert candidate["items"][0]["payload"]["economic_policy"]["valuation_method"] == "creator_explicit"
    assert candidate["items"][1]["payload"]["economic_policy"]["valuation_method"] == "creator_explicit"
    assert candidate["items"][1]["payload"]["relationships"]["stored_in"] == "$backpack"

    with connect(db) as conn:
        preview = preview_sandbox_item_batch(conn, candidate["items"])

    assert preview["count"] == 2
    assert preview["entries"][1]["resolved_relationships"] == [
        {"relation_type": "stored_in", "target_kind": "batch_ref", "target": "backpack"}
    ]

from copy import deepcopy

import pytest

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.db import connect
from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill, item_ai_fill_schema
from observer_sandbox.item_creation_schema import ItemSchemaError, validate_item_payload
from observer_sandbox.item_grading import resolve_item_grading
from observer_sandbox.item_metrics import DEFAULT_ITEM_METRIC_REGISTRY
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import create_sandbox_item
from observer_sandbox.telegram_item_draft_review import item_detail_view
from observer_sandbox.telegram_world_layers_item_extension import approved_item_detail_text


def _flashlight():
    payload = manual_item_template()
    payload["definition"].update(
        {
            "key": "camping_flashlight_1000lm",
            "name": "LED Camping Flashlight",
            "kind": "equipment",
            "description": "Waterproof LED flashlight with 1000 lumens output and 10-hour battery life.",
            "tags": ["flashlight", "camping"],
        }
    )
    payload["definition"]["modules"]["metrics"] = {
        "luminous_flux": {"value": 1, "unit": "klm"},
        "runtime": {"value": 600, "unit": "min"},
        "beam_distance": {"value": 300, "unit": "m"},
    }
    return payload


def _draft(payload):
    return {
        "revision": 1,
        "draft_mode": "manual",
        "proposal": {"properties": {"item_payload": payload}},
    }


def test_metric_registry_normalizes_common_units_deterministically():
    assert DEFAULT_ITEM_METRIC_REGISTRY.normalize("luminous_flux", {"value": 1, "unit": "klm"}) == {
        "value": 1000.0,
        "unit": "lm",
    }
    assert DEFAULT_ITEM_METRIC_REGISTRY.normalize("runtime", {"value": 600, "unit": "min"}) == {
        "value": 10.0,
        "unit": "h",
    }
    assert DEFAULT_ITEM_METRIC_REGISTRY.normalize("payload_capacity", {"value": 44.09245244, "unit": "lb"})["unit"] == "kg"


def test_unknown_metric_and_unit_fail_closed():
    payload = _flashlight()
    payload["definition"]["modules"]["metrics"]["magic_power"] = {"value": 10, "unit": "spark"}
    with pytest.raises(ItemSchemaError, match="unregistered metric"):
        validate_item_payload(payload)

    payload = _flashlight()
    payload["definition"]["modules"]["metrics"]["runtime"] = {"value": 10, "unit": "days"}
    with pytest.raises(ItemSchemaError, match="unit must be one of"):
        validate_item_payload(payload)


def test_ai_fill_schema_is_registry_driven_and_null_metrics_canonicalize_sparse():
    schema = item_ai_fill_schema()
    metrics_schema = schema["properties"]["definition"]["properties"]["modules"]["properties"]["metrics"]["anyOf"][0]
    assert set(metrics_schema["properties"]) == set(DEFAULT_ITEM_METRIC_REGISTRY.metric_ids())

    payload = _flashlight()
    fill = deepcopy(payload)
    slots = {metric_id: None for metric_id in DEFAULT_ITEM_METRIC_REGISTRY.metric_ids()}
    slots["luminous_flux"] = {"value": 1000, "unit": "lm"}
    slots["runtime"] = {"value": 10, "unit": "h"}
    fill["definition"]["modules"]["metrics"] = slots
    fill["instance"] = {"mode": "unique", "quantity": None, "unit": None}
    canonical = canonicalize_ai_item_fill(fill)
    assert set(canonical["definition"]["modules"]["metrics"]) == {"luminous_flux", "runtime"}
    assert canonical["instance"] == {"mode": "unique"}


def test_flashlight_metrics_normalize_and_derive_multiple_grades():
    normalized = validate_item_payload(_flashlight())
    metrics = normalized["definition"]["modules"]["metrics"]
    assert metrics["luminous_flux"] == {"value": 1000.0, "unit": "lm"}
    assert metrics["runtime"] == {"value": 10.0, "unit": "h"}

    source = deepcopy(normalized)
    source.pop("derived")
    plan, profile = resolve_item_grading(source)
    assert profile is not None
    assert profile.overall is None
    assert profile.dimensions["luminous_flux"].grade == "A"
    assert profile.dimensions["runtime"].grade == "B"
    assert profile.dimensions["beam_distance"].grade == "B"
    assert {row.dimension_id for row in plan.dimensions} >= {"luminous_flux", "runtime", "beam_distance"}


def test_container_capacity_grades_existing_container_module_without_duplicate_metric():
    payload = manual_item_template()
    payload["definition"].update(
        {
            "key": "camping_backpack_30l",
            "name": "Camping Backpack",
            "kind": "container",
            "capabilities": ["inspect", "store", "use"],
            "tags": ["backpack", "camping"],
            "modules": {
                "physical": payload["definition"]["modules"]["physical"],
                "container": {"capacity_volume": {"value": 30, "unit": "l"}},
            },
        }
    )
    normalized = validate_item_payload(payload)
    assert "metrics" not in normalized["definition"]["modules"]
    source = deepcopy(normalized)
    source.pop("derived")
    _, profile = resolve_item_grading(source)
    assert profile is not None
    assert profile.dimensions["storage_capacity"].grade == "B"


def test_charge_time_is_represented_but_not_monotonic_high_graded():
    payload = manual_item_template()
    payload["definition"]["modules"]["metrics"] = {"charge_time": {"value": 90, "unit": "min"}}
    normalized = validate_item_payload(payload)
    assert normalized["definition"]["modules"]["metrics"]["charge_time"] == {"value": 1.5, "unit": "h"}
    source = deepcopy(normalized)
    source.pop("derived")
    plan, profile = resolve_item_grading(source)
    assert all(row.dimension_id != "charge_time" for row in plan.dimensions)
    assert profile is None


def test_normalized_metric_payload_is_revalidatable_for_edit_boundary():
    normalized = validate_item_payload(_flashlight())
    source = deepcopy(normalized)
    source.pop("derived")
    again = validate_item_payload(source)
    assert again["definition"]["modules"]["metrics"] == normalized["definition"]["modules"]["metrics"]


def test_flashlight_draft_and_approved_views_show_metrics_and_grades(tmp_path):
    detail, _ = item_detail_view(_draft(_flashlight()), 0)
    assert "PERFORMANCE METRICS" in detail
    assert "Luminous Flux: 1 klm" in detail
    assert "Runtime: 600 min" in detail
    assert "Luminous Flux: A · Advanced" in detail
    assert "Runtime: B · Skilled" in detail

    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        created = create_sandbox_item(conn, _flashlight(), requested_by="test")
        approved = approved_item_detail_text(conn, created)
    assert "⚙️ PERFORMANCE METRICS" in approved
    assert "Luminous Flux: 1000 lm" in approved
    assert "Runtime: 10 h" in approved
    assert "Luminous Flux: A · Advanced" in approved
    assert "Runtime: B · Skilled" in approved
    assert "Overall" not in approved

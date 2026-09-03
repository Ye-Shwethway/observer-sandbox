from __future__ import annotations

from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.creator_studio_location_composition import (
    approve_location_composition_draft,
    start_location_composition_draft,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_v2 import materialize_sandbox_location_v2
from observer_sandbox.telegram_world_layers import world_layer_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if button.get("callback_data")
    }


def test_location_detail_is_human_friendly_and_omits_raw_nested_dict_dump(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        draft = start_location_composition_draft(conn, 501)
        created = approve_location_composition_draft(conn, 501, int(draft["revision"]))
        property_id = created["refs"]["property"]
        room_id = created["refs"]["room"]

        property_text, property_keyboard = world_layer_callback_view(conn, f"sw:o:{property_id}")
        room_text, room_keyboard = world_layer_callback_view(conn, f"sw:o:{room_id}")

        for text in (property_text, room_text):
            assert "Creation Sandbox · Active" in text
            assert "🔐 ACCESS & CONTROL" in text
            assert "Access: Public" in text
            assert "📐 PHYSICAL" in text
            assert "📊 LOCATION GRADE PROFILE" in text
            assert "Completeness:" in text
            assert "Overall: Not defined" in text
            assert "{'" not in text
            assert "None" not in text
            assert "Properties" not in text
            assert "canonical universe unchanged" in text.lower()

        assert "📍 Composition Test Property" in property_text
        assert "📍 Composition Test Room" in room_text
        assert "Parent: Composition Test Property" in room_text
        assert "nav:sandbox" in _callbacks(property_keyboard)
        assert "sw:list:location" in _callbacks(room_keyboard)


def test_location_detail_formats_quantities_resources_topology_and_economics_humanly(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        destination_payload = manual_location_template()
        destination_payload["identity"].update({
            "key": "place.detail.garden",
            "name": "Back Garden",
            "kind": "outdoor_zone",
            "description": "A small garden behind the house.",
        })
        destination = materialize_sandbox_location_v2(conn, destination_payload)

        house_payload = manual_location_template()
        house_payload["identity"].update({
            "key": "place.detail.house",
            "name": "Detail House",
            "kind": "building",
            "description": "A test house with represented detail.",
            "functional_classes": ["residential"],
        })
        house_payload["spatial"]["area"] = {"kind": "area", "value": 110.0, "unit": "m2"}
        house_payload["facilities"]["capabilities"] = ["cook", "rest"]
        house_payload["facilities"]["facility_types"] = ["living_space"]
        house_payload["facilities"]["resource_types"] = ["potable_water", "storage_capacity"]
        house_payload["facilities"]["utilities"] = ["electricity", "potable_water"]
        house_payload["topology"]["interfaces"] = [{
            "key": "garden_door",
            "name": "Garden Door",
            "kind": "door",
            "destination_ref": destination["object_id"],
            "directionality": "two_way",
            "enabled": True,
            "traversal_modes": ["walk"],
            "base_duration_minutes": 1.0,
            "distance": {"kind": "length", "value": 5.0, "unit": "m"},
        }]
        house_payload["economic_policy"] = {
            "classification": "standalone_asset",
            "currency_code": "USD",
            "market_value_minor": 25000000,
            "replacement_value_minor": 20000000,
            "net_worth_treatment": "include",
            "included_in_parent_ref": None,
            "valuation_method": "test evidence",
        }
        house = materialize_sandbox_location_v2(conn, house_payload)

        text, _ = world_layer_callback_view(conn, f"sw:o:{house['object_id']}")

        assert "• Area: 110 m²" in text
        assert "• Resources: Potable Water, Storage Capacity" in text
        assert "🔗 TOPOLOGY" in text
        assert "Garden Door · Door · Enabled" in text
        assert "→ Back Garden · Two Way" in text
        assert "Modes: Walk" in text
        assert "Distance: 5 m" in text
        assert "💰 ECONOMICS" in text
        assert "Classification: Standalone Asset" in text
        assert "Currency: USD" in text
        assert "Market value: 25,000,000 minor units" in text
        assert "📊 LOCATION GRADE PROFILE" in text
        assert "Completeness:" in text
        assert "{'" not in text

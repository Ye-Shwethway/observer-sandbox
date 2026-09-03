from __future__ import annotations

from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.location_grading_v2 import location_grade_profile_v2
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_composition import (
    materialize_location_composition,
    preview_location_composition,
)


def _location(
    ref: str,
    *,
    key: str,
    name: str,
    kind: str,
    parent_ref: str | None = None,
    exposure: str,
    surface: str,
    boundary_type: str,
    enclosure: str,
):
    payload = manual_location_template()
    payload["identity"].update(
        {
            "key": key,
            "name": name,
            "kind": kind,
            "description": f"Representative L11.7 acceptance Location: {name}.",
        }
    )
    payload["structure"].update({"parent_ref": parent_ref, "exposure": exposure})
    payload["spatial"]["surface"] = surface
    payload["boundary"].update(
        {
            "type": boundary_type,
            "enclosure": enclosure,
            "notes": None,
        }
    )
    return {"ref": ref, "payload": payload}


def _interface(destination_ref: str):
    return {
        "key": "door.to_garden",
        "name": "Door to Garden",
        "kind": "door",
        "destination_ref": destination_ref,
        "directionality": "two_way",
        "enabled": True,
        "traversal_modes": ["walk"],
        "base_duration_minutes": 0.5,
        "distance": {"value": 12, "unit": "ft"},
    }


def _container_item(ref: str, *, located_at: str):
    payload = manual_item_template()
    payload["definition"].update(
        {
            "key": "item.acceptance.storage_box",
            "name": "Storage Box",
            "kind": "container",
            "description": "Container Item embedded in the Location acceptance graph.",
            "capabilities": ["inspect", "store", "use"],
            "tags": ["storage", "acceptance"],
        }
    )
    payload["definition"]["modules"]["container"] = {
        "capacity_volume": {"value": 20, "unit": "l"}
    }
    payload["relationships"]["located_at"] = located_at
    return {"ref": ref, "payload": payload}


def _object_item(ref: str, *, stored_in: str):
    payload = manual_item_template()
    payload["definition"].update(
        {
            "key": "item.acceptance.flashlight",
            "name": "Flashlight",
            "kind": "object",
            "description": "Ordinary object Item stored in the acceptance container.",
            "capabilities": ["inspect", "use"],
            "tags": ["light", "acceptance"],
        }
    )
    payload["relationships"]["stored_in"] = stored_in
    return {"ref": ref, "payload": payload}


def _representative_envelope():
    property_member = _location(
        "property",
        key="place.acceptance.property",
        name="Acceptance Property",
        kind="property",
        exposure="mixed",
        surface="mixed",
        boundary_type="mixed",
        enclosure="partially_enclosed",
    )
    property_payload = property_member["payload"]
    property_payload["geography"].update(
        {
            "address_text": None,
            "locality": "South Lake Tahoe",
            "region": "California",
            "country_code": "US",
            "position": None,
            "bounds": None,
        }
    )
    property_payload["facilities"].update(
        {
            "capabilities": ["enter", "leave", "inspect"],
            "facility_types": ["living_space"],
            "resource_types": ["electric_power", "potable_water"],
            "utilities": ["electricity", "potable_water"],
        }
    )

    building_member = _location(
        "building",
        key="place.acceptance.property.house",
        name="Acceptance House",
        kind="building",
        parent_ref="$property",
        exposure="indoor",
        surface="interior_floor",
        boundary_type="physical",
        enclosure="enclosed",
    )
    building_member["payload"]["facilities"].update(
        {
            "capabilities": ["enter", "leave", "rest", "work"],
            "facility_types": ["living_space"],
            "resource_types": ["electric_power", "data_network"],
            "utilities": ["electricity", "internet"],
        }
    )

    room_member = _location(
        "room",
        key="place.acceptance.property.house.study",
        name="Acceptance Study",
        kind="room",
        parent_ref="$building",
        exposure="indoor",
        surface="interior_floor",
        boundary_type="physical",
        enclosure="enclosed",
    )
    room_member["payload"]["facilities"].update(
        {
            "capabilities": ["inspect", "read", "research", "work"],
            "facility_types": ["research"],
            "resource_types": ["data_network"],
            "utilities": ["electricity", "internet"],
        }
    )
    room_member["payload"]["environment"].update(
        {"lighting_profile": "mixed", "weather_exposure": "protected"}
    )
    room_member["payload"]["topology"]["interfaces"] = [_interface("$garden")]

    garden_member = _location(
        "garden",
        key="place.acceptance.property.garden",
        name="Acceptance Garden",
        kind="outdoor_zone",
        parent_ref="$property",
        exposure="outdoor",
        surface="grass",
        boundary_type="open",
        enclosure="unenclosed",
    )
    garden_member["payload"]["facilities"].update(
        {
            "capabilities": ["inspect", "recreate"],
            "facility_types": ["recreation"],
            "resource_types": [],
            "utilities": [],
        }
    )
    garden_member["payload"]["environment"].update(
        {"lighting_profile": "natural", "weather_exposure": "exposed"}
    )

    return {
        "schema_version": "location-composition-v1",
        "locations": [property_member, building_member, room_member, garden_member],
        "items": [
            _container_item("box", located_at="$room"),
            _object_item("flashlight", stored_in="$box"),
        ],
    }


def _counts(conn):
    return {
        "objects": conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0],
        "locations": conn.execute("SELECT COUNT(*) FROM creation_sandbox_location_profiles").fetchone()[0],
        "items": conn.execute("SELECT COUNT(*) FROM creation_sandbox_item_instances").fetchone()[0],
        "relations": conn.execute("SELECT COUNT(*) FROM creation_sandbox_relations").fetchone()[0],
    }


def test_l11_7_representative_property_building_room_outdoor_vertical(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    envelope = _representative_envelope()

    with connect(db) as conn:
        canonical_before = canonical_state_fingerprint(conn)
        counts_before = _counts(conn)
        preview = preview_location_composition(conn, envelope)

        assert preview["count"] == 6
        assert [entry["ref"] for entry in preview["locations"]] == [
            "property",
            "building",
            "room",
            "garden",
        ]
        assert _counts(conn) == counts_before
        assert canonical_state_fingerprint(conn) == canonical_before

        created = materialize_location_composition(conn, envelope, requested_by="l11.7-acceptance")
        refs = created["refs"]
        assert len(created["locations"]) == 4
        assert len(created["items"]) == 2

        by_key = {value["location_key"]: value for value in created["locations"]}
        property_location = by_key["place.acceptance.property"]
        building = by_key["place.acceptance.property.house"]
        room = by_key["place.acceptance.property.house.study"]
        garden = by_key["place.acceptance.property.garden"]

        assert building["source"]["structure"]["parent_ref"] == refs["property"]
        assert room["source"]["structure"]["parent_ref"] == refs["building"]
        assert garden["source"]["structure"]["parent_ref"] == refs["property"]
        assert garden["source"]["identity"]["kind"] == "outdoor_zone"
        assert garden["source"]["boundary"] == {
            "type": "open",
            "enclosure": "unenclosed",
            "notes": None,
        }
        assert room["source"]["boundary"]["enclosure"] == "enclosed"

        assert property_location["source"]["geography"]["locality"] == "South Lake Tahoe"
        assert property_location["source"]["geography"]["position"] is None
        assert property_location["source"]["geography"]["bounds"] is None
        assert set(room["source"]["facilities"]["capabilities"]) == {
            "inspect",
            "read",
            "research",
            "work",
        }
        assert room["source"]["facilities"]["resource_types"] == ["data_network"]
        assert room["source"]["facilities"]["utilities"] == ["electricity", "internet"]

        interface = room["source"]["topology"]["interfaces"][0]
        assert interface["destination_ref"] == refs["garden"]
        assert interface["kind"] == "door"
        assert interface["traversal_modes"] == ["walk"]
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='connected_to' AND target_object_id=?",
            (refs["room"], refs["garden"]),
        ).fetchone() is not None
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='connected_to' AND target_object_id=?",
            (refs["garden"], refs["room"]),
        ).fetchone() is not None

        profile = location_grade_profile_v2(room)
        assert profile is not None
        assert profile.overall is None
        assert "completeness" in profile.dimensions
        assert profile.dimensions["completeness"].grade is not None

        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_actor_runtime WHERE object_id IN (?,?,?,?,?,?) LIMIT 1",
            (
                refs["property"],
                refs["building"],
                refs["room"],
                refs["garden"],
                refs["box"],
                refs["flashlight"],
            ),
        ).fetchone() is None
        assert canonical_state_fingerprint(conn) == canonical_before


def test_l11_7_embedded_item_kinds_and_storage_relationships_are_preserved(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    envelope = _representative_envelope()

    with connect(db) as conn:
        canonical_before = canonical_state_fingerprint(conn)
        created = materialize_location_composition(conn, envelope, requested_by="l11.7-items")
        refs = created["refs"]

        rows = conn.execute(
            "SELECT object_id,definition_key,source_json FROM creation_sandbox_item_instances ORDER BY definition_key"
        ).fetchall()
        assert len(rows) == 2
        kinds = {}
        import json

        for row in rows:
            source = json.loads(row["source_json"])
            kinds[row["definition_key"]] = source["definition"]["kind"]
        assert kinds == {
            "item.acceptance.flashlight": "object",
            "item.acceptance.storage_box": "container",
        }

        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='located_at' AND target_object_id=?",
            (refs["box"], refs["room"]),
        ).fetchone() is not None
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='stored_in' AND target_object_id=?",
            (refs["flashlight"], refs["box"]),
        ).fetchone() is not None
        assert canonical_state_fingerprint(conn) == canonical_before

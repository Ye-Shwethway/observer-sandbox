from copy import deepcopy

import pytest

from observer_sandbox.location_creation_schema_v2 import (
    LocationCreationSchemaV2Error,
    validate_location_payload_v2,
)
from observer_sandbox.location_grading_v2 import location_grade_profile_v2


def base():
    return {
        "schema_version": "location-v2",
        "identity": {
            "key": "place.test.room",
            "name": "Test Room",
            "kind": "room",
            "description": "A represented test room.",
            "functional_classes": [],
            "tags": [],
        },
        "structure": {"parent_ref": None, "exposure": "indoor"},
        "geography": {
            "address_text": None,
            "locality": None,
            "region": None,
            "country_code": None,
            "position": None,
            "bounds": None,
        },
        "spatial": {
            "area": None,
            "length": None,
            "width": None,
            "height": None,
            "elevation": None,
            "terrain": None,
            "surface": "interior_floor",
            "orientation_notes": None,
        },
        "boundary": {"type": "physical", "enclosure": "enclosed", "notes": None},
        "access": {"policy": {"mode": "public"}},
        "operations": {"initial_state": "open"},
        "topology": {"interfaces": []},
        "facilities": {"capabilities": [], "facility_types": [], "resource_types": [], "utilities": []},
        "environment": {"lighting_profile": "unknown", "weather_exposure": "unknown"},
        "control": {"ownership_class": "unknown", "owner_ref": None, "operator_ref": None},
        "economic_policy": None,
        "provenance": {"source_status": "creator_authored", "source_note": None},
    }


def interface(destination="sbx_location_hall"):
    return {
        "key": "door.main",
        "name": "Main Door",
        "kind": "door",
        "destination_ref": destination,
        "directionality": "two_way",
        "enabled": True,
        "traversal_modes": ["walk"],
        "base_duration_minutes": 0.2,
        "distance": {"value": 3.0, "unit": "ft"},
    }


def source_only(validated):
    return {key: deepcopy(value) for key, value in validated.items() if key != "derived"}


def test_v2_unknown_precision_remains_null_and_grades_completeness_only():
    result = validate_location_payload_v2(base())
    assert result["geography"]["position"] is None
    assert result["spatial"]["area"] is None
    assert result["derived"]["completeness_level"] == "L0"
    assert result["derived"]["completeness_grade"]["grade"] == "E"
    profile = location_grade_profile_v2(result)
    assert profile is not None
    assert profile.overall is None
    assert profile.dimensions["completeness"].grade == "E"


def test_v2_normalized_source_revalidates_without_derived_authority():
    value = base()
    value["structure"]["parent_ref"] = "sbx_location_floor"
    value["spatial"]["area"] = {"value": 400.0, "unit": "ft2"}
    value["spatial"]["length"] = {"value": 20.0, "unit": "ft"}
    first = validate_location_payload_v2(value)
    normalized_source = source_only(first)
    second = validate_location_payload_v2(normalized_source)
    assert second["spatial"]["area"] == first["spatial"]["area"]
    assert second["spatial"]["length"] == first["spatial"]["length"]
    assert second["derived"] == first["derived"]


def test_v2_rejects_authored_grade_or_derived_fields():
    value = base()
    value["derived"] = {"completeness_level": "L4"}
    with pytest.raises(LocationCreationSchemaV2Error, match="unknown field"):
        validate_location_payload_v2(value)
    value = base()
    value["grade"] = "S"
    with pytest.raises(LocationCreationSchemaV2Error, match="unknown field"):
        validate_location_payload_v2(value)


def test_v2_geography_validates_coordinates_country_and_bounds():
    value = base()
    value["geography"] = {
        "address_text": None,
        "locality": "South Lake Tahoe",
        "region": "California",
        "country_code": "us",
        "position": {"latitude": 38.94, "longitude": -119.98},
        "bounds": {"south": 38.9, "west": -120.1, "north": 39.0, "east": -119.9},
    }
    result = validate_location_payload_v2(value)
    assert result["geography"]["country_code"] == "US"
    bad = deepcopy(value)
    bad["geography"]["position"]["latitude"] = 91
    with pytest.raises(LocationCreationSchemaV2Error, match="latitude"):
        validate_location_payload_v2(bad)
    bad = deepcopy(value)
    bad["geography"]["bounds"] = {"south": 40, "west": -120, "north": 39, "east": -119}
    with pytest.raises(LocationCreationSchemaV2Error, match="south"):
        validate_location_payload_v2(bad)


def test_v2_access_policy_is_separate_from_initial_operating_state():
    value = base()
    value["access"]["policy"] = {"mode": "restricted"}
    value["operations"]["initial_state"] = "open"
    result = validate_location_payload_v2(value)
    assert result["access"]["policy"] == {"mode": "restricted"}
    assert result["operations"]["initial_state"] == "open"


def test_v2_interface_kind_distance_and_modes_are_strict():
    value = base()
    value["structure"]["parent_ref"] = "sbx_location_floor"
    value["topology"]["interfaces"] = [interface()]
    result = validate_location_payload_v2(value)
    assert result["topology"]["interfaces"][0]["kind"] == "door"
    assert result["topology"]["interfaces"][0]["distance"] == {"kind": "length", "value": pytest.approx(0.9144), "unit": "m"}
    bad = deepcopy(value)
    bad["topology"]["interfaces"][0]["kind"] = "wormhole"
    with pytest.raises(LocationCreationSchemaV2Error, match="interface kind"):
        validate_location_payload_v2(bad)
    bad = deepcopy(value)
    bad["topology"]["interfaces"][0]["traversal_modes"] = ["teleport"]
    with pytest.raises(LocationCreationSchemaV2Error, match="traversal_modes"):
        validate_location_payload_v2(bad)


def test_v2_registry_backed_facility_evidence_rejects_unknown_tokens():
    value = base()
    value["facilities"]["facility_types"] = ["strength_training"]
    assert validate_location_payload_v2(value)["facilities"]["facility_types"] == ["strength_training"]
    value["facilities"]["facility_types"] = ["magic_everything_room"]
    with pytest.raises(LocationCreationSchemaV2Error, match="facility_types"):
        validate_location_payload_v2(value)


def test_v2_completeness_requires_resolved_traversal_evidence_for_l2_plus():
    value = base()
    value["structure"]["parent_ref"] = "sbx_location_floor"
    assert validate_location_payload_v2(value)["derived"]["completeness_level"] == "L1"
    value["topology"]["interfaces"] = [interface(destination=None)]
    assert validate_location_payload_v2(value)["derived"]["completeness_level"] == "L1"
    value["topology"]["interfaces"] = [interface()]
    assert validate_location_payload_v2(value)["derived"]["completeness_level"] == "L2"
    value["facilities"]["facility_types"] = ["strength_training"]
    assert validate_location_payload_v2(value)["derived"]["completeness_level"] == "L3"
    value["environment"]["lighting_profile"] = "mixed"
    assert validate_location_payload_v2(value)["derived"]["completeness_level"] == "L4"


def test_v2_control_and_economic_relationships_remain_separate():
    value = base()
    value["control"] = {"ownership_class": "private", "owner_ref": "sbx_character_owner", "operator_ref": None}
    value["economic_policy"] = {
        "classification": "component",
        "currency_code": "USD",
        "market_value_minor": None,
        "replacement_value_minor": None,
        "net_worth_treatment": "included_in_parent",
        "included_in_parent_ref": "sbx_location_parent",
        "valuation_method": "included_in_parent",
    }
    result = validate_location_payload_v2(value)
    assert result["control"]["owner_ref"] == "sbx_character_owner"
    assert result["economic_policy"]["included_in_parent_ref"] == "sbx_location_parent"
    assert result["access"]["policy"] == {"mode": "public"}

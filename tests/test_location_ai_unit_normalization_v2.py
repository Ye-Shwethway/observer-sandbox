from observer_sandbox.location_ai_contract import location_ai_fill_schema, repair_location_ai_candidate
from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.location_creation_schema_v2 import validate_location_payload_v2


def test_location_ai_schema_constrains_area_and_length_units() -> None:
    schema = location_ai_fill_schema()
    spatial = schema["properties"]["spatial"]["properties"]

    area = spatial["area"]["anyOf"][0]["properties"]["unit"]["enum"]
    length = spatial["length"]["anyOf"][0]["properties"]["unit"]["enum"]

    assert set(area) == {"m2", "cm2", "in2", "ft2", "yd2"}
    assert set(length) == {"m", "cm", "mm", "in", "ft", "yd"}
    assert "square_meters" not in area


def test_location_ai_repair_normalizes_square_meters_without_changing_value() -> None:
    candidate = manual_location_template()
    candidate["identity"]["key"] = "place.test.house"
    candidate["identity"]["name"] = "Test House"
    candidate["provenance"] = {"source_status": "provisional", "source_note": None}
    candidate["spatial"]["area"] = {
        "kind": "area",
        "value": 110,
        "unit": "square_meters",
    }

    repaired = repair_location_ai_candidate(candidate)

    assert repaired["spatial"]["area"] == {
        "kind": "area",
        "value": 110,
        "unit": "m2",
    }
    validated = validate_location_payload_v2(repaired)
    assert validated["spatial"]["area"] == {
        "kind": "area",
        "value": 110.0,
        "unit": "m2",
    }


def test_location_ai_repair_normalizes_common_imperial_area_alias() -> None:
    candidate = manual_location_template()
    candidate["spatial"]["area"] = {
        "kind": "area",
        "value": 1200,
        "unit": "square_feet",
    }

    repaired = repair_location_ai_candidate(candidate)

    assert repaired["spatial"]["area"]["value"] == 1200
    assert repaired["spatial"]["area"]["unit"] == "ft2"

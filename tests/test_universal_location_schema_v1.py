from copy import deepcopy

import pytest

from observer_sandbox.location_creation_schema import LocationCreationSchemaError, validate_location_payload


def base():
    return {
        "schema_version": "location-v1",
        "identity": {"key":"place.test.room","name":"Test Room","kind":"room","description":"A represented test room.","functional_class":"residence"},
        "structure": {"parent_ref": None, "exposure":"indoor"},
        "spatial": {"area":None,"length":None,"width":None,"height":None,"elevation":None,"terrain":None,"orientation_notes":None},
        "access": {"policy":{"mode":"public"},"operating_state":"open"},
        "topology": {"interfaces":[]},
        "facilities": {"capabilities":[],"facilities":[],"resources":[]},
        "environment": {"lighting":None,"weather_exposure":None,"utilities":[]},
        "economic_policy": None,
        "provenance": {"source_status":"creator_authored","source_note":None},
    }


def interface():
    return {"key":"door.main","name":"Main Door","destination_ref":"sbx_location_hall","directionality":"two_way","enabled":True,"traversal_modes":["walk"],"base_duration_minutes":0.2}


def test_unknown_precision_remains_none_and_identity_placeholder_is_l0():
    result = validate_location_payload(base())
    assert result["spatial"]["area"] is None
    assert result["spatial"]["length"] is None
    assert result["derived"]["completeness_level"] == "L0"
    assert result["derived"]["completeness_grade"]["grade"] == "E"


def test_physical_extent_normalizes_units_without_making_them_required():
    value = base(); value["structure"]["parent_ref"] = "sbx_location_floor"
    value["spatial"]["area"] = {"value": 400, "unit":"ft2"}
    value["spatial"]["length"] = {"value": 20, "unit":"ft"}
    result = validate_location_payload(value)
    assert result["spatial"]["area"]["base_unit"] == "m2"
    assert result["spatial"]["area"]["base_value"] == pytest.approx(37.161216)
    assert result["spatial"]["length"]["base_unit"] == "m"
    assert result["derived"]["completeness_level"] == "L1"


def test_access_policy_and_operating_state_are_separate_contracts():
    value = base(); value["access"] = {"policy":{"mode":"restricted"},"operating_state":"open"}
    result = validate_location_payload(value)
    assert result["access"]["policy"]["mode"] == "restricted"
    assert result["access"]["operating_state"] == "open"
    value["access"] = {"policy":{"mode":"public"},"operating_state":"closed"}
    assert validate_location_payload(value)["access"]["operating_state"] == "closed"


def test_l2_l3_l4_are_derived_from_traversability_affordance_and_living_state():
    value = base(); value["structure"]["parent_ref"] = "sbx_location_floor"; value["topology"]["interfaces"] = [interface()]
    l2 = validate_location_payload(value); assert l2["derived"]["completeness_level"] == "L2"; assert l2["derived"]["completeness_grade"]["grade"] == "C"
    value["facilities"]["facilities"] = ["strength_training"]
    l3 = validate_location_payload(value); assert l3["derived"]["completeness_level"] == "L3"; assert l3["derived"]["completeness_grade"]["grade"] == "B"
    value["environment"]["utilities"] = ["power"]
    l4 = validate_location_payload(value); assert l4["derived"]["completeness_level"] == "L4"; assert l4["derived"]["completeness_grade"]["grade"] == "A"


def test_topology_is_explicit_and_does_not_infer_connection_from_parent():
    value = base(); value["structure"]["parent_ref"] = "sbx_location_floor"
    result = validate_location_payload(value)
    assert result["topology"]["interfaces"] == []
    assert result["derived"]["completeness_level"] == "L1"


def test_interface_contract_rejects_unknown_modes_duplicate_keys_and_invalid_duration():
    value = base(); value["topology"]["interfaces"] = [interface()]
    bad = deepcopy(value); bad["topology"]["interfaces"][0]["traversal_modes"] = ["teleport"]
    with pytest.raises(LocationCreationSchemaError, match="traversal_modes"): validate_location_payload(bad)
    bad = deepcopy(value); bad["topology"]["interfaces"] = [interface(), interface()]
    with pytest.raises(LocationCreationSchemaError, match="unique"): validate_location_payload(bad)
    bad = deepcopy(value); bad["topology"]["interfaces"][0]["base_duration_minutes"] = 0
    with pytest.raises(LocationCreationSchemaError, match="positive"): validate_location_payload(bad)


def test_economic_policy_reuses_value_semantics_without_becoming_access():
    value = base(); value["economic_policy"] = {"classification":"standalone_asset","currency_code":"USD","market_value_minor":500000,"replacement_value_minor":550000,"net_worth_treatment":"independent","included_in_parent_ref":None,"valuation_method":"creator_explicit"}
    result = validate_location_payload(value)
    assert result["economic_policy"]["classification"] == "standalone_asset"
    assert result["access"]["policy"] == {"mode":"public"}


def test_schema_is_exact_and_rejects_fabricated_or_unknown_fields():
    value = base(); value["coordinates"] = {"lat":1,"lon":2}
    with pytest.raises(LocationCreationSchemaError, match="unknown field"): validate_location_payload(value)
    value = base(); value["identity"]["kind"] = "castle_magic_dimension"
    with pytest.raises(LocationCreationSchemaError, match="kind"): validate_location_payload(value)


def test_requirement_access_policy_shape_is_validated_fail_closed():
    value = base(); value["access"]["policy"] = {"mode":"requirements","requirements":{"type":"minimum_grade","domain":"character","dimension":"attribute_capability","minimum":"Z"}}
    with pytest.raises(LocationCreationSchemaError, match="Unknown grade"): validate_location_payload(value)

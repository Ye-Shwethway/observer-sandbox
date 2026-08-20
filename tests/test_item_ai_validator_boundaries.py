import pytest

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill
from observer_sandbox.item_creation_schema import ItemSchemaError, validate_item_payload


def test_unknown_capability_is_not_silently_dropped():
    payload = manual_item_template()
    payload["definition"]["capabilities"].append("teleport")
    candidate = canonicalize_ai_item_fill(payload)
    with pytest.raises(ItemSchemaError, match="unregistered capability"):
        validate_item_payload(candidate)


def test_conflicting_physical_placement_is_not_silently_rewritten():
    payload = manual_item_template()
    payload["relationships"]["located_at"] = "location_a"
    payload["relationships"]["carried_by"] = "character_a"
    candidate = canonicalize_ai_item_fill(payload)
    with pytest.raises(ItemSchemaError, match="only one current physical placement mode"):
        validate_item_payload(candidate)


def test_unsupported_metric_is_not_silently_removed():
    payload = manual_item_template()
    payload["definition"]["modules"]["metrics"] = {
        "magic_power": {"value": 100, "unit": "mana"}
    }
    candidate = canonicalize_ai_item_fill(payload)
    with pytest.raises(ItemSchemaError, match="unregistered metric"):
        validate_item_payload(candidate)

from copy import deepcopy

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill
from observer_sandbox.item_creation_schema import validate_item_payload


def _base():
    return manual_item_template()


def test_token_and_capability_matrix_reaches_strict_validator():
    cases = []

    plain = _base()
    plain["definition"]["key"] = "Trail Light 2"
    plain["definition"]["tags"] = ["Outdoor Gear", "2 Pack"]
    cases.append(plain)

    container = _base()
    container["definition"]["modules"]["container"] = {"capacity_volume": {"value": 20, "unit": "l"}}
    container["definition"]["capabilities"] = ["inspect", "use"]
    cases.append(container)

    resistance = _base()
    resistance["definition"]["modules"]["resistance_training"] = {"resistance_load": {"value": 55, "unit": "lb"}}
    resistance["definition"]["capabilities"] = ["inspect", "use"]
    cases.append(resistance)

    for raw in cases:
        candidate = canonicalize_ai_item_fill(deepcopy(raw))
        validate_item_payload(candidate)

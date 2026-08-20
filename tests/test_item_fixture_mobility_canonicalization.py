from copy import deepcopy

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_authoring import DEFAULT_ITEM_AI_AUTHORING_INSTRUCTION
from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill
from observer_sandbox.item_creation_schema import validate_item_payload


def test_fixture_movable_ai_output_reconciles_to_fixed_and_validates():
    payload = manual_item_template()
    payload["definition"]["key"] = "gym_rack"
    payload["definition"]["name"] = "Gym Rack"
    payload["definition"]["kind"] = "fixture"
    payload["definition"]["mobility"] = "movable"

    canonical = canonicalize_ai_item_fill(payload)

    assert canonical["definition"]["mobility"] == "fixed"
    validate_item_payload(canonical)


def test_non_fixture_movable_item_is_not_forced_fixed():
    payload = manual_item_template()
    payload["definition"]["kind"] = "equipment"
    payload["definition"]["mobility"] = "movable"

    canonical = canonicalize_ai_item_fill(deepcopy(payload))

    assert canonical["definition"]["mobility"] == "movable"
    validate_item_payload(canonical)


def test_item_ai_prompt_explains_fixture_mobility_contract():
    instruction = DEFAULT_ITEM_AI_AUTHORING_INSTRUCTION
    assert "fixture Items are structurally fixed" in instruction
    assert "mobility='fixed'" in instruction
    assert "ordinary portable gear" in instruction

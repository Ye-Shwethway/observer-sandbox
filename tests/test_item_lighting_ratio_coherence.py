import pytest

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_authoring import DEFAULT_ITEM_AI_AUTHORING_INSTRUCTION
from observer_sandbox.item_creation_realism import ItemRealismError, validate_item_default_realism


def _flashlight(*, lumens: float, power_w: float | None):
    payload = manual_item_template()
    payload["definition"]["key"] = "lighting_ratio_flashlight"
    payload["definition"]["name"] = "LED Camping Flashlight"
    payload["definition"]["description"] = "Rechargeable LED flashlight for camping use"
    payload["definition"]["kind"] = "equipment"
    payload["definition"]["capabilities"] = ["use"]
    metrics = {
        "luminous_flux": {"value": lumens, "unit": "lm"},
        "runtime": {"value": 10, "unit": "h"},
        "energy_capacity": {"value": 80, "unit": "Wh"},
    }
    if power_w is not None:
        metrics["power"] = {"value": power_w, "unit": "W"}
    payload["definition"]["modules"]["metrics"] = metrics
    return payload


def test_live_1000_lumen_one_watt_flashlight_is_rejected():
    payload = _flashlight(lumens=1000, power_w=1)
    with pytest.raises(ItemRealismError, match="luminous efficacy"):
        validate_item_default_realism(payload)


def test_plausible_1000_lumen_eight_watt_flashlight_passes():
    payload = _flashlight(lumens=1000, power_w=8)
    validate_item_default_realism(payload)


def test_unknown_power_can_be_left_unrepresented():
    payload = _flashlight(lumens=1000, power_w=None)
    validate_item_default_realism(payload)


def test_authoring_prompt_warns_against_implausible_lumen_power_pairs():
    instruction = DEFAULT_ITEM_AI_AUTHORING_INSTRUCTION
    assert "luminous_flux and power together imply luminous efficacy" in instruction
    assert "If power is uncertain, prefer null" in instruction

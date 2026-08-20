from copy import deepcopy

import pytest

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_ai_self_correction import generate_validated_item_candidate
from observer_sandbox.item_creation_realism import ItemRealismError, validate_item_default_realism
from observer_sandbox.item_creation_schema import validate_item_payload


def _flashlight():
    payload = manual_item_template()
    payload["definition"].update({
        "key": "camping_flashlight",
        "name": "Camping Flashlight",
        "kind": "equipment",
        "description": "Compact water-resistant LED flashlight for camping",
        "capabilities": ["use"],
        "tags": ["camping", "lighting", "outdoor"],
        "modules": {
            "physical": {
                "mass": {"value": 0.2, "unit": "kg"},
                "length": {"value": 15, "unit": "cm"},
                "width": {"value": 3, "unit": "cm"},
                "height": {"value": 3, "unit": "cm"},
            },
            "metrics": {
                "luminous_flux": {"value": 1000, "unit": "lm"},
                "power": {"value": 5, "unit": "W"},
                "runtime": {"value": 8, "unit": "h"},
                "energy_capacity": {"value": 3.7, "unit": "Wh"},
            },
        },
    })
    return payload


def _validate(candidate):
    validate_item_payload(candidate)
    validate_item_default_realism(candidate)


def test_gross_energy_budget_inconsistency_rejects():
    payload = _flashlight()
    validate_item_payload(payload)
    with pytest.raises(ItemRealismError, match="grossly inconsistent"):
        validate_item_default_realism(payload)


def test_plausible_energy_budget_passes():
    payload = _flashlight()
    payload["definition"]["modules"]["metrics"]["energy_capacity"] = {"value": 20, "unit": "Wh"}
    _validate(payload)


def test_noncanonical_allowed_metric_units_are_normalized_for_coherence():
    payload = _flashlight()
    metrics = payload["definition"]["modules"]["metrics"]
    metrics["luminous_flux"] = {"value": 1, "unit": "klm"}
    metrics["runtime"] = {"value": 480, "unit": "min"}
    metrics["energy_capacity"] = {"value": 20_000, "unit": "mWh"}
    _validate(payload)


def test_generic_water_resistant_wording_does_not_justify_numeric_depth():
    payload = _flashlight()
    payload["definition"]["modules"]["metrics"].pop("energy_capacity")
    payload["definition"]["modules"]["metrics"]["water_resistance_depth"] = {"value": 1, "unit": "m"}
    validate_item_payload(payload)
    with pytest.raises(ItemRealismError, match="requires explicit waterproof"):
        validate_item_default_realism(payload)


def test_explicit_waterproof_evidence_allows_numeric_depth():
    payload = _flashlight()
    payload["definition"]["description"] = "Compact waterproof LED flashlight rated for brief submersion"
    payload["definition"]["modules"]["metrics"].pop("energy_capacity")
    payload["definition"]["modules"]["metrics"]["water_resistance_depth"] = {"value": 1, "unit": "m"}
    _validate(payload)


def test_self_correction_can_replace_incoherent_metrics_on_second_attempt():
    bad = _flashlight()
    good = deepcopy(bad)
    good["definition"]["description"] = "Compact LED flashlight for camping"
    good["definition"]["modules"]["metrics"].pop("energy_capacity")

    outputs = [bad, good]
    prompts = []

    def generator(conn, **kwargs):
        prompts.append(kwargs["prompt"])
        return deepcopy(outputs[len(prompts) - 1])

    result = generate_validated_item_candidate(
        None,
        generator=generator,
        binding={"provider_id": "test", "model_id": "test", "parameters": {}},
        prompt="Create a camping flashlight",
        schema={},
        schema_name="test",
        canonicalize=lambda value: value,
        validate=_validate,
    )

    assert len(prompts) == 2
    assert "grossly inconsistent" in prompts[1]
    assert "energy_capacity" not in result["definition"]["modules"]["metrics"]

from __future__ import annotations

from observer_sandbox.item_ai_contract import canonicalize_ai_item_fill


def _provider_fill(*, stackable: bool, mode: str) -> dict:
    return {
        "schema_version": "item-v1",
        "definition": {
            "key": "flashlight",
            "name": "Flashlight",
            "kind": "tool",
            "description": "A portable flashlight.",
            "stackable": stackable,
            "mobility": "movable",
            "capabilities": [],
            "tags": [],
            "modules": {
                "physical": None,
                "stack": {"canonical_unit": "piece", "initial_quantity": 1},
                "nutrition": None,
                "container": None,
                "resistance_training": None,
            },
        },
        "instance": {"mode": mode, "quantity": 1, "unit": "piece"},
        "economic_policy": {},
        "requirements": {"use": None},
        "relationships": {},
    }


def test_non_stackable_provider_fill_drops_accidental_stack_slot():
    normalized = canonicalize_ai_item_fill(_provider_fill(stackable=False, mode="unique"))

    assert "stack" not in normalized["definition"]["modules"]
    assert "quantity" not in normalized["instance"]
    assert "unit" not in normalized["instance"]


def test_stackable_provider_fill_keeps_stack_module_for_strict_validation():
    normalized = canonicalize_ai_item_fill(_provider_fill(stackable=True, mode="stack"))

    assert normalized["definition"]["modules"]["stack"] == {
        "canonical_unit": "piece",
        "initial_quantity": 1,
    }
    assert normalized["instance"] == {"mode": "stack", "quantity": 1, "unit": "piece"}

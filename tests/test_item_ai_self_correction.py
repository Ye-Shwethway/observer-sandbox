from __future__ import annotations

import pytest

from observer_sandbox.item_ai_self_correction import generate_validated_item_candidate


def test_item_ai_retries_once_with_exact_validation_reason():
    prompts = []
    outputs = iter([{"value": 45}, {"value": 25}])

    def generator(conn, **kwargs):
        prompts.append(kwargs["prompt"])
        return next(outputs)

    def validate(candidate):
        if candidate["value"] > 30:
            raise ValueError("capacity exceeds outer bounding volume (45 L > 30 L)")

    result = generate_validated_item_candidate(
        object(),
        generator=generator,
        binding={"provider_id": "fake", "model_id": "fake", "parameters": {}},
        prompt="Create a realistic container.",
        schema={"type": "object"},
        schema_name="test_item",
        canonicalize=lambda value: value,
        validate=validate,
    )

    assert result == {"value": 25}
    assert len(prompts) == 2
    assert "capacity exceeds outer bounding volume (45 L > 30 L)" in prompts[1]
    assert "same schema and Creator intent" in prompts[1]


def test_item_ai_stops_after_one_correction_attempt():
    calls = 0

    def generator(conn, **kwargs):
        nonlocal calls
        calls += 1
        return {"value": 45}

    def validate(candidate):
        raise ValueError("still impossible")

    with pytest.raises(ValueError, match="still impossible"):
        generate_validated_item_candidate(
            object(),
            generator=generator,
            binding={"provider_id": "fake", "model_id": "fake", "parameters": {}},
            prompt="Create a realistic container.",
            schema={"type": "object"},
            schema_name="test_item",
            canonicalize=lambda value: value,
            validate=validate,
        )
    assert calls == 2

from __future__ import annotations

from typing import Any, Callable


MAX_ITEM_AI_ATTEMPTS = 2


def generate_validated_item_candidate(
    conn,
    *,
    generator: Callable[..., dict[str, Any]],
    binding: dict[str, Any],
    prompt: str,
    schema: dict[str, Any],
    schema_name: str,
    canonicalize: Callable[[dict[str, Any]], dict[str, Any]],
    validate: Callable[[dict[str, Any]], None],
) -> dict[str, Any]:
    """Generate once, then allow one bounded schema-preserving correction pass."""

    current_prompt = prompt
    last_error: Exception | None = None
    for attempt in range(MAX_ITEM_AI_ATTEMPTS):
        candidate = generator(
            conn,
            provider_id=str(binding["provider_id"]),
            model_id=str(binding["model_id"]),
            prompt=current_prompt,
            schema=schema,
            schema_name=schema_name,
            parameters=dict(binding.get("parameters") or {}),
        )
        if not isinstance(candidate, dict):
            raise ValueError("Creation AI returned a non-object structured candidate")
        candidate = canonicalize(candidate)
        try:
            validate(candidate)
            return candidate
        except (ValueError, TypeError, KeyError) as exc:
            last_error = exc
            if attempt + 1 >= MAX_ITEM_AI_ATTEMPTS:
                break
            current_prompt = (
                prompt
                + "\nThe previous complete candidate was rejected by deterministic validation. "
                "Generate a fresh complete candidate under the exact same schema and Creator intent. "
                "Do not weaken, bypass, or reinterpret the rule. Correct the conflicting facts themselves. "
                "Deterministic rejection: "
                + str(exc)
            )
    assert last_error is not None
    raise last_error


__all__ = ["MAX_ITEM_AI_ATTEMPTS", "generate_validated_item_candidate"]

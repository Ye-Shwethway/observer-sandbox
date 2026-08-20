from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .grading_socket import GradingSocketError, GradingSocketRegistry
from .item_creation_schema import ItemSchemaError, validate_item_payload
from .item_grading_coverage import ITEM_COVERAGE_POLICY_ID, ITEM_GRADING_COVERAGE_REGISTRY


def _grading_source(value: Mapping[str, Any]) -> dict[str, Any]:
    """Return normalized Item facts suitable for socket grading."""

    source: Mapping[str, Any] = value
    nested = value.get("item")
    if isinstance(nested, Mapping):
        source = nested

    payload = deepcopy(dict(source))
    if "relationships" in payload:
        payload.pop("derived", None)
        return validate_item_payload(payload)
    return payload


def resolve_item_grading(
    value: Mapping[str, Any],
    *,
    universe_policy_id: str = ITEM_COVERAGE_POLICY_ID,
    registry: GradingSocketRegistry = ITEM_GRADING_COVERAGE_REGISTRY,
):
    source = _grading_source(value)
    return registry.resolve("item", source, universe_policy_id=universe_policy_id)


def item_grading_lines(
    value: Mapping[str, Any],
    *,
    heading: str = "GRADING",
    universe_policy_id: str = ITEM_COVERAGE_POLICY_ID,
    registry: GradingSocketRegistry = ITEM_GRADING_COVERAGE_REGISTRY,
) -> list[str]:
    lines = [heading]
    try:
        plan, profile = resolve_item_grading(
            value,
            universe_policy_id=universe_policy_id,
            registry=registry,
        )
    except (ItemSchemaError, GradingSocketError, TypeError, ValueError):
        lines.append("• Grading unavailable for this payload under the current registered contract.")
        return lines

    if profile is None:
        lines.append("• No registered grading dimensions apply to this Item yet.")
        return lines

    for row in plan.dimensions:
        result = profile.dimensions.get(row.dimension_id)
        if result is None:
            continue
        lines.append(f"• {row.label}: {result.grade} · {result.label}")
    if len(lines) == 1:
        lines.append("• No registered grading dimensions apply to this Item yet.")
    return lines


__all__ = ["item_grading_lines", "resolve_item_grading"]

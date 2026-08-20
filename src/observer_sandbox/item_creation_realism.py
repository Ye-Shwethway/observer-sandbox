from __future__ import annotations

from typing import Any, Mapping

from .physical_quantity import PhysicalQuantityError, normalize_physical_quantity


DEFAULT_ITEM_REALISM_INSTRUCTION = (
    "REALISM INVARIANT: unless the target universe explicitly declares different physical laws, "
    "all generated physical facts must obey ordinary real-world physics, geometry, scale and mutual consistency. "
    "Treat dimensions as the external bounding dimensions of the Item. Container internal capacity must fit inside "
    "that external envelope and therefore must never exceed the outer bounding volume. Keep mass, dimensions, capacity, "
    "nutrition and other numeric facts mutually plausible for the described object. Do not invent false precision: when "
    "a numeric fact cannot be conservatively supported, use null for the nullable slot instead of guessing. "
)


class ItemRealismError(ValueError):
    pass


def _quantity_base(raw: Any, *, kind: str, label: str) -> float | None:
    if raw is None:
        return None
    if not isinstance(raw, Mapping) or set(raw) != {"value", "unit"}:
        raise ItemRealismError(f"{label} must be a physical quantity object")
    try:
        return float(normalize_physical_quantity(kind, raw["value"], str(raw["unit"])).base_value)
    except (PhysicalQuantityError, TypeError, ValueError) as exc:
        raise ItemRealismError(f"{label} could not be normalized: {exc}") from exc


def validate_item_default_realism(payload: Mapping[str, Any]) -> None:
    """Reject clear physical impossibilities for the default Creation Sandbox.

    This intentionally implements only objective cross-field checks. It is not a
    general realism oracle and does not infer missing facts. Future universes may
    replace/extend this policy when their physical-law contract differs.
    """

    if not isinstance(payload, Mapping):
        raise ItemRealismError("Item payload must be an object")
    definition = payload.get("definition")
    if not isinstance(definition, Mapping):
        return
    modules = definition.get("modules")
    if not isinstance(modules, Mapping):
        return
    physical = modules.get("physical")
    container = modules.get("container")
    if not isinstance(physical, Mapping) or not isinstance(container, Mapping):
        return

    length = _quantity_base(physical.get("length"), kind="length", label="modules.physical.length")
    width = _quantity_base(physical.get("width"), kind="length", label="modules.physical.width")
    height = _quantity_base(physical.get("height"), kind="length", label="modules.physical.height")
    capacity = _quantity_base(container.get("capacity_volume"), kind="volume", label="modules.container.capacity_volume")
    if None in (length, width, height, capacity):
        return

    outer_volume_m3 = float(length) * float(width) * float(height)
    if float(capacity) > outer_volume_m3 * (1.0 + 1e-9):
        raise ItemRealismError(
            "container capacity exceeds the Item's outer bounding volume "
            f"({float(capacity) * 1000:g} L > {outer_volume_m3 * 1000:g} L); "
            "dimensions and capacity are physically inconsistent"
        )


__all__ = [
    "DEFAULT_ITEM_REALISM_INSTRUCTION",
    "ItemRealismError",
    "validate_item_default_realism",
]

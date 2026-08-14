from __future__ import annotations

"""Reusable movement-pattern anatomy for resistance-training evidence.

Movement definitions are universal and actor-independent. They describe relative
regional loading only; progression magnitude remains owned by downstream domain
engines such as BC-3.
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
TRAINING_MOVEMENTS_PATH = REPO_ROOT / "config" / "training_movements.v1.json"


@lru_cache(maxsize=1)
def load_training_movement_catalog(path: str | Path = TRAINING_MOVEMENTS_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def movement_definition(
    movement_id: str | None,
    *,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    if not movement_id:
        return None
    source = catalog if catalog is not None else load_training_movement_catalog()
    raw = source.get("movements", {}).get(movement_id)
    if not isinstance(raw, dict):
        return None
    result = dict(raw)
    result["movement_id"] = movement_id
    result["source"] = str(source.get("revision", "training-anatomy-v1"))
    return result


def movement_options(
    movement_ids: list[str] | tuple[str, ...] | None,
    *,
    catalog: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    source = catalog if catalog is not None else load_training_movement_catalog()
    result: list[dict[str, Any]] = []
    for movement_id in movement_ids or []:
        definition = movement_definition(str(movement_id), catalog=source)
        if definition is None:
            continue
        result.append(
            {
                "movement_id": definition["movement_id"],
                "name": definition["name"],
                "tags": list(definition.get("tags", [])),
            }
        )
    return result


def validate_selected_movements(
    selected: list[str] | tuple[str, ...] | None,
    *,
    allowed: list[str] | tuple[str, ...] | None,
) -> tuple[str, ...]:
    allowed_set = {str(item) for item in allowed or []}
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in selected or []:
        movement_id = str(raw)
        if movement_id in seen:
            continue
        if movement_id not in allowed_set:
            raise ValueError(f"Training movement {movement_id} is not allowed for the selected method")
        seen.add(movement_id)
        normalized.append(movement_id)
    return tuple(normalized)


def movement_anatomy_evidence(
    movement_ids: list[str] | tuple[str, ...] | None,
    *,
    catalog: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    ids = [str(item) for item in movement_ids or []]
    if not ids:
        return None
    source = catalog if catalog is not None else load_training_movement_catalog()
    regional_totals: dict[str, float] = {}
    accepted: list[str] = []
    for movement_id in ids:
        definition = movement_definition(movement_id, catalog=source)
        if definition is None:
            raise ValueError(f"Unknown training movement: {movement_id}")
        accepted.append(movement_id)
        weights = definition.get("region_weights", {})
        if not isinstance(weights, dict):
            continue
        for region, raw_weight in weights.items():
            weight = max(0.0, min(1.0, float(raw_weight)))
            regional_totals[str(region)] = regional_totals.get(str(region), 0.0) + weight
    divisor = max(1, len(accepted))
    regional_load = {
        region: round(max(0.0, min(1.0, total / divisor)), 6)
        for region, total in sorted(regional_totals.items())
    }
    return {
        "movement_ids": accepted,
        "regional_load": regional_load,
        "source": str(source.get("revision", "training-anatomy-v1")),
    }

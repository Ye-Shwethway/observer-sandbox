from __future__ import annotations

import json
import math
import sqlite3
from typing import Any

from .inventory import inventory_for_entity, item_definition, nutrition_for_stack_quantity


EATING_BEHAVIOR_SOURCE = "eating-behavior-v1"
MAX_MEAL_RESOURCES = 6


def _portion_bounds(definition: dict[str, Any], unit: str, available: float) -> tuple[float, float, float] | None:
    properties = definition.get("properties")
    if not isinstance(properties, dict):
        return None
    default = float(properties.get("default_portion_quantity", 0.0))
    if default <= 0.0 or available <= 0.0:
        return None
    if unit == "piece":
        minimum = float(max(1, math.ceil(default * 0.5)))
        maximum = float(max(int(minimum), math.floor(default * 2.0)))
    else:
        minimum = round(default * 0.5, 6)
        maximum = round(default * 2.0, 6)
    maximum = min(maximum, float(available))
    if maximum + 1e-9 < minimum:
        return None
    selected_default = min(default, maximum)
    if unit == "piece":
        selected_default = float(max(int(minimum), min(int(maximum), round(selected_default))))
    return round(minimum, 6), round(selected_default, 6), round(maximum, 6)


def _scope_chain(conn: sqlite3.Connection, location_id: str) -> list[str]:
    """Return location then nearest structural ancestors, without named-world assumptions."""
    result = [location_id]
    frontier = [location_id]
    seen = {location_id}
    while frontier:
        current = frontier.pop(0)
        rows = conn.execute(
            "SELECT source_id FROM relations WHERE target_id=? AND relation_type='contains' ORDER BY id",
            (current,),
        ).fetchall()
        for row in rows:
            parent = str(row[0])
            if parent in seen:
                continue
            seen.add(parent)
            result.append(parent)
            frontier.append(parent)
    return result


def _choices_for_scope(conn: sqlite3.Connection, scope_id: str) -> list[dict[str, Any]]:
    scoped = inventory_for_entity(conn, scope_id)
    choices: list[dict[str, Any]] = []
    for stack in scoped["stacks"]:
        definition = item_definition(stack.definition_id)
        capabilities = definition.get("capabilities") or []
        if "eat" not in capabilities or not isinstance(definition.get("nutrition"), dict):
            continue
        bounds = _portion_bounds(definition, stack.unit, stack.quantity)
        if bounds is None:
            continue
        minimum, default, maximum = bounds
        default_nutrition = nutrition_for_stack_quantity(conn, stack.entity_id, default)
        choices.append(
            {
                "stack_id": stack.entity_id,
                "name": stack.name,
                "unit": stack.unit,
                "available_quantity": round(float(stack.quantity), 6),
                "min_quantity": minimum,
                "default_quantity": default,
                "max_quantity": maximum,
                "access_scope_id": scope_id,
                "default_nutrition": {
                    "energy_kcal": default_nutrition["energy_kcal"],
                    "protein_g": default_nutrition["protein_g"],
                    "carbohydrate_g": default_nutrition["carbohydrate_g"],
                    "fat_g": default_nutrition["fat_g"],
                },
            }
        )
    return sorted(choices, key=lambda row: (str(row["name"]).lower(), str(row["stack_id"])))


def meal_resource_choices(conn: sqlite3.Connection, location_id: str) -> list[dict[str, Any]]:
    """Return edible stock reachable through the nearest enclosing inventory scope.

    Direct room inventory wins. If a food-access room has no concrete stack of its
    own, the nearest structural ancestor with edible stock is used. This preserves
    site-level provisioning without making arbitrary remote inventory globally
    accessible; cognition only receives these choices on a local eat-capable action.
    """
    for scope_id in _scope_chain(conn, location_id):
        choices = _choices_for_scope(conn, scope_id)
        if choices:
            return choices
    return []


def enrich_eating_action_options(
    conn: sqlite3.Connection,
    location_id: str,
    action_options: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    choices: list[dict[str, Any]] | None = None
    result: list[dict[str, Any]] = []
    for raw in action_options:
        option = dict(raw)
        if option.get("action") != "eat":
            result.append(option)
            continue
        if choices is None:
            choices = meal_resource_choices(conn, location_id)
        if not choices:
            continue
        option["meal_resources"] = choices
        option["meal_resource_policy"] = {
            "max_items": MAX_MEAL_RESOURCES,
            "instruction": "Choose one or more listed stack_id values and quantities within each listed min/max bound. Quantities are deterministic inventory units; do not calculate nutrients yourself.",
            "source": EATING_BEHAVIOR_SOURCE,
        }
        result.append(option)
    return result


def validate_meal_resources(
    conn: sqlite3.Connection,
    *,
    location_id: str,
    resources: list[dict[str, Any]] | tuple[dict[str, Any], ...],
) -> list[dict[str, Any]]:
    rows = list(resources)
    if not rows:
        raise ValueError("Eat action requires at least one inventory food resource")
    if len(rows) > MAX_MEAL_RESOURCES:
        raise ValueError(f"Eat action supports at most {MAX_MEAL_RESOURCES} food resources")
    choices = {str(row["stack_id"]): row for row in meal_resource_choices(conn, location_id)}
    seen: set[str] = set()
    normalized: list[dict[str, Any]] = []
    for raw in rows:
        if not isinstance(raw, dict) or set(raw) != {"stack_id", "quantity"}:
            raise ValueError("Meal resources must contain exactly stack_id and quantity")
        stack_id = str(raw["stack_id"])
        if stack_id in seen:
            raise ValueError(f"Duplicate meal resource stack: {stack_id}")
        seen.add(stack_id)
        choice = choices.get(stack_id)
        if choice is None:
            raise ValueError(f"Meal resource is not edible and available at {location_id}: {stack_id}")
        quantity = float(raw["quantity"])
        minimum = float(choice["min_quantity"])
        maximum = float(choice["max_quantity"])
        if quantity + 1e-9 < minimum or quantity > maximum + 1e-9:
            raise ValueError(
                f"Meal quantity for {stack_id} must be between {minimum} and {maximum} {choice['unit']}"
            )
        if choice["unit"] == "piece" and abs(quantity - round(quantity)) > 1e-9:
            raise ValueError(f"Piece-based meal quantity must be a whole number: {stack_id}")
        normalized.append({"stack_id": stack_id, "quantity": round(quantity, 6)})
    return normalized


def validate_proposed_resources(
    conn: sqlite3.Connection,
    *,
    action_name: str,
    location_id: str,
    resources: Any,
) -> tuple[dict[str, Any], ...]:
    if resources is None:
        rows: list[Any] = []
    elif isinstance(resources, (list, tuple)):
        rows = list(resources)
    else:
        raise ValueError("Action resources must be an array")
    if action_name != "eat":
        if rows:
            raise ValueError("Only eat actions may propose food resources in Eating Behavior v1")
        return ()
    return tuple(validate_meal_resources(conn, location_id=location_id, resources=rows))


def _aggregate_nutrition(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "items": items,
        "energy_kcal": round(sum(float(row["energy_kcal"]) for row in items), 3),
        "protein_g": round(sum(float(row["protein_g"]) for row in items), 3),
        "carbohydrate_g": round(sum(float(row["carbohydrate_g"]) for row in items), 3),
        "fat_g": round(sum(float(row["fat_g"]) for row in items), 3),
        "source": EATING_BEHAVIOR_SOURCE,
    }


def settle_eating_action(conn: sqlite3.Connection, action_id: str) -> dict[str, Any] | None:
    """Atomically consume a structured meal already persisted on an action instance.

    Empty resources intentionally return None so an in-flight pre-v1 legacy eat
    action can finish under its existing target-based BC-1 evidence semantics.
    New model-planned eats are required to carry resources before scheduling.
    """
    row = conn.execute(
        "SELECT action_type,place_id,resources_json FROM action_instances WHERE id=?",
        (action_id,),
    ).fetchone()
    if row is None or str(row["action_type"]) != "eat":
        return None
    raw_resources = json.loads(row["resources_json"] or "[]")
    if not raw_resources:
        return None
    if not isinstance(raw_resources, list):
        raise ValueError("Persisted meal resources must be an array")
    location_id = str(row["place_id"])
    resources = validate_meal_resources(conn, location_id=location_id, resources=raw_resources)

    evidence = [nutrition_for_stack_quantity(conn, item["stack_id"], item["quantity"]) for item in resources]
    conn.execute("SAVEPOINT eating_behavior_v1")
    try:
        settled_items: list[dict[str, Any]] = []
        for item, nutrition in zip(resources, evidence, strict=True):
            stack_id = item["stack_id"]
            quantity = float(item["quantity"])
            cur = conn.execute(
                """UPDATE inventory_stacks
                SET quantity=quantity-?,updated_at=CURRENT_TIMESTAMP
                WHERE entity_id=? AND quantity+1e-9>=?""",
                (quantity, stack_id, quantity),
            )
            if cur.rowcount != 1:
                raise ValueError(f"Inventory quantity changed before meal settlement: {stack_id}")
            remaining = float(
                conn.execute("SELECT quantity FROM inventory_stacks WHERE entity_id=?", (stack_id,)).fetchone()[0]
            )
            if remaining < 1e-9:
                conn.execute("UPDATE inventory_stacks SET quantity=0 WHERE entity_id=?", (stack_id,))
                remaining = 0.0
            settled_items.append({**nutrition, "remaining_quantity": round(remaining, 6)})
        conn.execute("RELEASE SAVEPOINT eating_behavior_v1")
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT eating_behavior_v1")
        conn.execute("RELEASE SAVEPOINT eating_behavior_v1")
        raise
    return _aggregate_nutrition(settled_items)

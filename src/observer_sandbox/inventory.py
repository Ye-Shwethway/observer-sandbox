from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from .world import set_field


REPO_ROOT = Path(__file__).resolve().parents[2]
ITEMS_PATH = REPO_ROOT / "config" / "items.v1.json"
HOME_INVENTORY_PATH = REPO_ROOT / "config" / "worlds" / "home.inventory.v1.json"
INVENTORY_CONTAINMENT_RELATION = "stored_in"
OWNERSHIP_RELATION = "owned_by"


@dataclass(frozen=True)
class InventoryStack:
    entity_id: str
    definition_id: str
    name: str
    quantity: float
    unit: str
    container_id: str | None
    owner_id: str | None


@lru_cache(maxsize=1)
def load_item_catalog(path: str | Path = ITEMS_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def load_home_inventory_seed(path: str | Path = HOME_INVENTORY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _definitions_by_id() -> dict[str, dict[str, Any]]:
    source = load_item_catalog()
    rows = source.get("definitions", [])
    return {str(row["id"]): dict(row) for row in rows if isinstance(row, dict) and row.get("id")}


def item_definition(definition_id: str) -> dict[str, Any]:
    raw = _definitions_by_id().get(definition_id)
    if raw is None:
        raise KeyError(f"Unknown item definition: {definition_id}")
    return raw


def seed_item_definitions(conn: sqlite3.Connection) -> None:
    source = load_item_catalog()
    for raw in source.get("definitions", []):
        if not isinstance(raw, dict):
            continue
        definition_id = str(raw["id"])
        properties = dict(raw.get("properties", {}))
        effects = dict(raw.get("effects", {}))
        nutrition = raw.get("nutrition")
        if isinstance(nutrition, dict):
            properties["nutrition"] = dict(nutrition)
        conn.execute(
            """INSERT INTO entity_definitions(
                id,entity_type,name,capabilities_json,properties_json,effects_json,metadata_json
            ) VALUES(?,?,?,?,?,?,?)
            ON CONFLICT(id) DO UPDATE SET
                entity_type=excluded.entity_type,
                name=excluded.name,
                capabilities_json=excluded.capabilities_json,
                properties_json=excluded.properties_json,
                effects_json=excluded.effects_json,
                metadata_json=excluded.metadata_json,
                updated_at=CURRENT_TIMESTAMP""",
            (
                definition_id,
                str(raw.get("entity_type", "item")),
                str(raw["name"]),
                json.dumps(list(raw.get("capabilities", []))),
                json.dumps(properties, ensure_ascii=False),
                json.dumps(effects, ensure_ascii=False),
                json.dumps({"source": source.get("revision", "universal-items-v1")}),
            ),
        )
    conn.commit()


def _ensure_stack_entity(
    conn: sqlite3.Connection,
    *,
    stack_id: str,
    definition_id: str,
    name: str,
    capabilities: list[str],
) -> None:
    conn.execute(
        """INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id)
        VALUES(?,?,?,?,?)
        ON CONFLICT(id) DO UPDATE SET
            entity_type='item',
            name=excluded.name,
            capabilities_json=excluded.capabilities_json,
            definition_id=excluded.definition_id,
            updated_at=CURRENT_TIMESTAMP""",
        (stack_id, "item", name, json.dumps(capabilities), definition_id),
    )


def _replace_single_relation(
    conn: sqlite3.Connection,
    source_id: str,
    relation_type: str,
    target_id: str,
) -> None:
    conn.execute(
        "DELETE FROM relations WHERE source_id=? AND relation_type=? AND target_id<>?",
        (source_id, relation_type, target_id),
    )
    conn.execute(
        "INSERT OR IGNORE INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
        (source_id, relation_type, target_id),
    )


def seed_home_inventory(conn: sqlite3.Connection) -> None:
    seed_item_definitions(conn)
    seed = load_home_inventory_seed()
    owner_id = str(seed["owner_id"])
    definitions = _definitions_by_id()

    for container in seed.get("containers", []):
        container_id = str(container["entity_id"])
        if conn.execute("SELECT 1 FROM entities WHERE id=?", (container_id,)).fetchone() is None:
            raise KeyError(f"Inventory container does not exist in world: {container_id}")
        set_field(
            conn,
            container_id,
            "inventory.container_mobility",
            str(container.get("mobility", "fixed")),
            mode="static",
            authority="inventory_definition",
            source=str(seed.get("revision", "home-inventory-v1")),
        )
        set_field(
            conn,
            container_id,
            "inventory.container_kind",
            str(container.get("kind", "storage")),
            mode="static",
            authority="inventory_definition",
            source=str(seed.get("revision", "home-inventory-v1")),
        )

    for stack in seed.get("stacks", []):
        stack_id = str(stack["id"])
        definition_id = str(stack["definition_id"])
        definition = definitions.get(definition_id)
        if definition is None:
            raise KeyError(f"Unknown inventory seed definition: {definition_id}")
        properties = definition.get("properties", {})
        unit = str(stack["unit"])
        expected_unit = str(properties.get("canonical_unit", unit))
        if unit != expected_unit:
            raise ValueError(f"Stack {stack_id} unit {unit} does not match definition unit {expected_unit}")
        quantity = float(stack["quantity"])
        if quantity <= 0.0:
            raise ValueError(f"Stack {stack_id} must seed with positive quantity")
        container_id = str(stack["container_id"])
        if conn.execute("SELECT 1 FROM entities WHERE id=?", (container_id,)).fetchone() is None:
            raise KeyError(f"Inventory stack container does not exist: {container_id}")
        _ensure_stack_entity(
            conn,
            stack_id=stack_id,
            definition_id=definition_id,
            name=str(definition["name"]),
            capabilities=list(definition.get("capabilities", [])),
        )
        # Seed quantity is first-install data only. Normal initialize/deploy must
        # never replenish or reset a live stack that has already changed.
        conn.execute(
            """INSERT OR IGNORE INTO inventory_stacks(entity_id,quantity,unit,seed_revision,metadata_json)
            VALUES(?,?,?,?,?)""",
            (
                stack_id,
                quantity,
                unit,
                str(seed.get("revision", "home-inventory-v1")),
                json.dumps({}, ensure_ascii=False),
            ),
        )
        _replace_single_relation(conn, stack_id, INVENTORY_CONTAINMENT_RELATION, container_id)
        _replace_single_relation(conn, stack_id, OWNERSHIP_RELATION, owner_id)

    conn.execute(
        """INSERT INTO runtime_state(key,value_json) VALUES('inventory_seed_revision',?)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=CURRENT_TIMESTAMP""",
        (json.dumps(str(seed.get("revision", "home-inventory-v1"))),),
    )
    conn.commit()


def stack_state(conn: sqlite3.Connection, stack_id: str) -> InventoryStack:
    row = conn.execute(
        """SELECT e.id,e.definition_id,e.name,s.quantity,s.unit
        FROM entities e JOIN inventory_stacks s ON s.entity_id=e.id
        WHERE e.id=?""",
        (stack_id,),
    ).fetchone()
    if row is None:
        raise KeyError(f"Unknown inventory stack: {stack_id}")
    container = conn.execute(
        "SELECT target_id FROM relations WHERE source_id=? AND relation_type=?",
        (stack_id, INVENTORY_CONTAINMENT_RELATION),
    ).fetchone()
    owner = conn.execute(
        "SELECT target_id FROM relations WHERE source_id=? AND relation_type=?",
        (stack_id, OWNERSHIP_RELATION),
    ).fetchone()
    return InventoryStack(
        entity_id=str(row["id"]),
        definition_id=str(row["definition_id"]),
        name=str(row["name"]),
        quantity=float(row["quantity"]),
        unit=str(row["unit"]),
        container_id=None if container is None else str(container["target_id"]),
        owner_id=None if owner is None else str(owner["target_id"]),
    )


def container_inventory(conn: sqlite3.Connection, container_id: str, *, include_depleted: bool = False) -> list[InventoryStack]:
    rows = conn.execute(
        """SELECT s.entity_id
        FROM inventory_stacks s
        JOIN relations r ON r.source_id=s.entity_id AND r.relation_type=?
        WHERE r.target_id=?
        ORDER BY s.entity_id""",
        (INVENTORY_CONTAINMENT_RELATION, container_id),
    ).fetchall()
    result = [stack_state(conn, str(row["entity_id"])) for row in rows]
    return result if include_depleted else [row for row in result if row.quantity > 0.0]


def nutrition_for_stack_quantity(conn: sqlite3.Connection, stack_id: str, quantity: float) -> dict[str, Any]:
    stack = stack_state(conn, stack_id)
    amount = float(quantity)
    if amount <= 0.0:
        raise ValueError("Consumption quantity must be positive")
    if amount > stack.quantity + 1e-9:
        raise ValueError(f"Insufficient quantity in {stack_id}: requested {amount} {stack.unit}, available {stack.quantity}")
    definition = item_definition(stack.definition_id)
    nutrition = definition.get("nutrition")
    if not isinstance(nutrition, dict):
        raise ValueError(f"Item definition {stack.definition_id} has no nutrition semantics")
    basis = float(nutrition["basis_quantity"])
    if basis <= 0.0 or str(nutrition["unit"]) != stack.unit:
        raise ValueError(f"Invalid nutrition basis for {stack.definition_id}")
    factor = amount / basis
    return {
        "definition_id": stack.definition_id,
        "stack_id": stack.entity_id,
        "quantity": round(amount, 6),
        "unit": stack.unit,
        "energy_kcal": round(float(nutrition["energy_kcal"]) * factor, 3),
        "protein_g": round(float(nutrition.get("protein_g", 0.0)) * factor, 3),
        "carbohydrate_g": round(float(nutrition.get("carbohydrate_g", 0.0)) * factor, 3),
        "fat_g": round(float(nutrition.get("fat_g", 0.0)) * factor, 3),
        "source": "universal-item-nutrition-v1",
    }


def consume_stack(conn: sqlite3.Connection, stack_id: str, quantity: float) -> dict[str, Any]:
    evidence = nutrition_for_stack_quantity(conn, stack_id, quantity)
    amount = float(evidence["quantity"])
    cur = conn.execute(
        """UPDATE inventory_stacks
        SET quantity=quantity-?,updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND quantity+1e-9>=?""",
        (amount, stack_id, amount),
    )
    if cur.rowcount != 1:
        raise ValueError(f"Inventory quantity changed before consumption could commit: {stack_id}")
    remaining = float(conn.execute("SELECT quantity FROM inventory_stacks WHERE entity_id=?", (stack_id,)).fetchone()[0])
    if remaining < 1e-9:
        conn.execute("UPDATE inventory_stacks SET quantity=0 WHERE entity_id=?", (stack_id,))
        remaining = 0.0
    conn.commit()
    evidence["remaining_quantity"] = round(remaining, 6)
    return evidence

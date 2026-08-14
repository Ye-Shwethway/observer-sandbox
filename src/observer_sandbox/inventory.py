from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from .event_log import record_event
from .world import set_field


REPO_ROOT = Path(__file__).resolve().parents[2]
ITEMS_PATH = REPO_ROOT / "config" / "items.v1.json"
HOME_INVENTORY_PATH = REPO_ROOT / "config" / "worlds" / "home.inventory.v1.json"
INVENTORY_CONTAINMENT_RELATION = "stored_in"
OWNERSHIP_RELATION = "owned_by"
CARRIAGE_RELATION = "carried_by"
EQUIPPED_RELATION = "equipped_by"


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


def _sim_time(conn: sqlite3.Connection) -> str:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key='sim_time'").fetchone()
    if row is None:
        raise RuntimeError("Inventory migration requires initialized simulation time")
    value = json.loads(row[0])
    if not isinstance(value, str) or not value:
        raise RuntimeError("Inventory migration requires valid simulation time")
    return value


def _apply_stock_migrations(conn: sqlite3.Connection, seed: dict[str, Any]) -> None:
    owner_id = str(seed["owner_id"])
    for migration in seed.get("stock_migrations", []):
        if not isinstance(migration, dict):
            continue
        revision = str(migration.get("revision") or "").strip()
        if not revision:
            raise ValueError("Inventory stock migration requires a revision")
        marker_key = f"inventory_stock_migration:{revision}"
        if conn.execute("SELECT 1 FROM runtime_state WHERE key=?", (marker_key,)).fetchone() is not None:
            continue
        if migration.get("mode") != "ensure_minimum":
            raise ValueError(f"Unsupported inventory stock migration mode: {migration.get('mode')}")
        before_after: dict[str, dict[str, float]] = {}
        for stack_id, target_raw in dict(migration.get("minimum_quantities", {})).items():
            target = float(target_raw)
            if target <= 0.0:
                raise ValueError(f"Inventory migration target must be positive: {stack_id}")
            row = conn.execute(
                "SELECT quantity FROM inventory_stacks WHERE entity_id=?",
                (str(stack_id),),
            ).fetchone()
            if row is None:
                raise KeyError(f"Inventory migration references unknown stack: {stack_id}")
            before = float(row[0])
            after = max(before, target)
            if after != before:
                conn.execute(
                    "UPDATE inventory_stacks SET quantity=?,updated_at=CURRENT_TIMESTAMP WHERE entity_id=?",
                    (after, str(stack_id)),
                )
            before_after[str(stack_id)] = {"before": before, "after": after}

        conn.execute(
            "INSERT INTO runtime_state(key,value_json) VALUES(?,?)",
            (marker_key, json.dumps({"applied": True, "revision": revision})),
        )
        record_event(
            conn,
            sim_time=_sim_time(conn),
            event_type="creator_inventory_stock_baseline_applied",
            location_id=owner_id,
            state_changes={"inventory_stacks": before_after},
            payload={
                "authority": "creator",
                "requested_by": "canonical-stock-migration",
                "revision": revision,
                "mode": "ensure_minimum",
                "reason": migration.get("reason"),
                "owner_id": owner_id,
                "stacks": before_after,
            },
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
    _apply_stock_migrations(conn, seed)
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


def all_inventory_stacks(conn: sqlite3.Connection, *, include_depleted: bool = False) -> list[InventoryStack]:
    rows = conn.execute("SELECT entity_id FROM inventory_stacks ORDER BY entity_id").fetchall()
    result = [stack_state(conn, str(row["entity_id"])) for row in rows]
    return result if include_depleted else [stack for stack in result if stack.quantity > 0.0]


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


def _structural_scope_ids(conn: sqlite3.Connection, entity_id: str) -> set[str]:
    rows = conn.execute(
        """WITH RECURSIVE descendants(id) AS (
            SELECT ?
            UNION
            SELECT r.target_id
            FROM relations r JOIN descendants d ON r.source_id=d.id
            WHERE r.relation_type='contains'
        )
        SELECT id FROM descendants""",
        (entity_id,),
    ).fetchall()
    return {str(row[0]) for row in rows}


def _related_container_ids_for_character(conn: sqlite3.Connection, character_id: str) -> set[str]:
    rows = conn.execute(
        """SELECT DISTINCT source_id FROM relations
        WHERE target_id=? AND relation_type IN (?,?,?)""",
        (character_id, OWNERSHIP_RELATION, CARRIAGE_RELATION, EQUIPPED_RELATION),
    ).fetchall()
    result: set[str] = set()
    for row in rows:
        entity_id = str(row[0])
        container_flag = conn.execute(
            "SELECT 1 FROM fields WHERE entity_id=? AND field_key='inventory.container_kind'",
            (entity_id,),
        ).fetchone()
        if container_flag is not None:
            result.add(entity_id)
    return result


def inventory_for_entity(
    conn: sqlite3.Connection,
    entity_id: str,
    *,
    include_depleted: bool = False,
) -> dict[str, Any]:
    entity = conn.execute(
        "SELECT id,entity_type,name FROM entities WHERE id=?",
        (entity_id,),
    ).fetchone()
    if entity is None:
        raise KeyError(f"Unknown inventory scope entity: {entity_id}")

    scope_ids = _structural_scope_ids(conn, entity_id)
    if str(entity["entity_type"]) == "character":
        scope_ids.update(_related_container_ids_for_character(conn, entity_id))

    related: list[InventoryStack] = []
    for stack in all_inventory_stacks(conn, include_depleted=True):
        relation_targets = {target for target in (stack.container_id, stack.owner_id) if target}
        direct_relation = conn.execute(
            """SELECT 1 FROM relations
            WHERE source_id=? AND target_id=? AND relation_type IN (?,?,?) LIMIT 1""",
            (stack.entity_id, entity_id, OWNERSHIP_RELATION, CARRIAGE_RELATION, EQUIPPED_RELATION),
        ).fetchone()
        if relation_targets.intersection(scope_ids) or direct_relation is not None:
            if include_depleted or stack.quantity > 0.0:
                related.append(stack)

    containers: list[dict[str, Any]] = []
    for scope_id in sorted(scope_ids):
        row = conn.execute(
            """SELECT e.id,e.name,f.value_json
            FROM entities e JOIN fields f ON f.entity_id=e.id
            WHERE e.id=? AND f.field_key='inventory.container_kind'""",
            (scope_id,),
        ).fetchone()
        if row is None:
            continue
        mobility_row = conn.execute(
            "SELECT value_json FROM fields WHERE entity_id=? AND field_key='inventory.container_mobility'",
            (scope_id,),
        ).fetchone()
        containers.append({
            "id": str(row["id"]),
            "name": str(row["name"]),
            "kind": json.loads(row["value_json"]),
            "mobility": None if mobility_row is None else json.loads(mobility_row["value_json"]),
        })

    return {
        "scope": {"id": str(entity["id"]), "type": str(entity["entity_type"]), "name": str(entity["name"])},
        "containers": containers,
        "stacks": sorted(related, key=lambda stack: (stack.name.lower(), stack.entity_id)),
    }


def list_inventory_scopes(conn: sqlite3.Connection, scope_type: str) -> list[dict[str, Any]]:
    normalized = scope_type.strip().lower()
    if normalized == "locations":
        rows = conn.execute("SELECT id,entity_type,name FROM entities WHERE entity_type='location' ORDER BY name").fetchall()
    elif normalized == "characters":
        rows = conn.execute("SELECT id,entity_type,name FROM entities WHERE entity_type='character' ORDER BY name").fetchall()
    elif normalized == "containers":
        rows = conn.execute(
            """SELECT DISTINCT e.id,e.entity_type,e.name
            FROM entities e JOIN fields f ON f.entity_id=e.id
            WHERE f.field_key='inventory.container_kind'
            ORDER BY e.name"""
        ).fetchall()
    else:
        raise ValueError("scope_type must be locations, characters, or containers")

    result: list[dict[str, Any]] = []
    for row in rows:
        scoped = inventory_for_entity(conn, str(row["id"]), include_depleted=True)
        positive = [stack for stack in scoped["stacks"] if stack.quantity > 0.0]
        result.append({
            "id": str(row["id"]),
            "type": str(row["entity_type"]),
            "name": str(row["name"]),
            "stack_count": len(positive),
            "container_count": len(scoped["containers"]),
        })
    return result


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

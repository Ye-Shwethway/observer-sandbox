from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .profile_seed import import_seed, load_seed


REPO_ROOT = Path(__file__).resolve().parents[2]
HOME_SEED_PATH = REPO_ROOT / "config" / "worlds" / "home.v1.json"
DARIAN_SEED_PATH = REPO_ROOT / "config" / "characters" / "darian.canonical.json"
DARIAN_RUNTIME_DEFAULTS_PATH = REPO_ROOT / "config" / "characters" / "darian.runtime-defaults.json"


def load_world_seed(path: str | Path = HOME_SEED_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _upsert_entity(
    conn: sqlite3.Connection,
    entity_id: str,
    entity_type: str,
    name: str,
    capabilities: list[str] | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO entities(id, entity_type, name, capabilities_json)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            entity_type=excluded.entity_type,
            name=excluded.name,
            capabilities_json=excluded.capabilities_json,
            updated_at=CURRENT_TIMESTAMP
        """,
        (entity_id, entity_type, name, json.dumps(capabilities or [])),
    )


def _upsert_relation(
    conn: sqlite3.Connection,
    source_id: str,
    relation_type: str,
    target_id: str,
) -> None:
    conn.execute(
        """
        INSERT INTO relations(source_id, relation_type, target_id)
        VALUES (?, ?, ?)
        ON CONFLICT(source_id, relation_type, target_id) DO NOTHING
        """,
        (source_id, relation_type, target_id),
    )


def set_field(
    conn: sqlite3.Connection,
    entity_id: str,
    field_key: str,
    value: Any,
    *,
    mode: str = "simulated",
    authority: str = "living_runtime",
    source: str = "p1-runtime",
) -> None:
    conn.execute(
        """
        INSERT INTO fields(entity_id, field_key, value_json, mode, authority, source)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(entity_id, field_key) DO UPDATE SET
            value_json=excluded.value_json,
            mode=excluded.mode,
            authority=excluded.authority,
            source=excluded.source,
            updated_at=CURRENT_TIMESTAMP
        """,
        (entity_id, field_key, json.dumps(value, ensure_ascii=False), mode, authority, source),
    )


def get_field(conn: sqlite3.Connection, entity_id: str, field_key: str, default: Any = None) -> Any:
    row = conn.execute(
        "SELECT value_json FROM fields WHERE entity_id=? AND field_key=?",
        (entity_id, field_key),
    ).fetchone()
    return default if row is None else json.loads(row[0])


def _normalized_locations(world: dict[str, Any]) -> list[dict[str, Any]]:
    if world.get("locations"):
        return list(world["locations"])
    # Backward-compatible support for the original flat Home v1 format.
    return [
        {
            "id": room["id"],
            "name": room["name"],
            "parent": world["world_id"],
            "kind": "room",
            "access": "open",
            "canon": False,
        }
        for room in world.get("rooms", [])
    ]


def _rebuild_seed_topology(conn: sqlite3.Connection, world: dict[str, Any], locations: list[dict[str, Any]]) -> None:
    location_ids = [loc["id"] for loc in locations]
    object_ids = [obj["id"] for obj in world.get("objects", [])]

    # Each authored location/object has one seed-owned containment parent. Remove
    # the old seed relationship first so a flat Home -> Room graph can migrate to
    # Universe -> Estate -> Floor -> Room without duplicate parents.
    for target_id in location_ids + object_ids:
        conn.execute("DELETE FROM relations WHERE relation_type='contains' AND target_id=?", (target_id,))

    # Adjacency among authored locations is seed-owned. This preserves entity ids,
    # runtime.location values, event history, and pending action targets while
    # allowing the mansion's internal route graph to evolve safely.
    if location_ids:
        placeholders = ",".join("?" for _ in location_ids)
        conn.execute(
            f"DELETE FROM relations WHERE relation_type='connected_to' AND source_id IN ({placeholders})",
            location_ids,
        )
        conn.execute(
            f"DELETE FROM relations WHERE relation_type='connected_to' AND target_id IN ({placeholders})",
            location_ids,
        )


def seed_home_and_darian(conn: sqlite3.Connection) -> None:
    world = load_world_seed()
    locations = _normalized_locations(world)
    revision = world.get("revision", "home-v1")

    _upsert_entity(conn, world["world_id"], "world", world["name"], ["contains"])
    _rebuild_seed_topology(conn, world, locations)

    for loc in locations:
        capabilities = ["inspect"]
        if loc.get("kind") == "room" and loc.get("access") != "locked":
            capabilities.extend(["enter", "leave"])
        _upsert_entity(conn, loc["id"], "location", loc["name"], capabilities)
        _upsert_relation(conn, loc.get("parent", world["world_id"]), "contains", loc["id"])
        set_field(conn, loc["id"], "world.location_kind", loc.get("kind", "location"), mode="static", authority="world_definition", source=revision)
        set_field(conn, loc["id"], "world.access", loc.get("access", "open"), mode="static", authority="world_definition", source=revision)
        set_field(conn, loc["id"], "world.canon", bool(loc.get("canon", False)), mode="static", authority="world_definition", source=revision)
        set_field(conn, loc["id"], "world.metadata", loc.get("metadata", {}), mode="static", authority="world_definition", source=revision)

    for obj in world["objects"]:
        _upsert_entity(conn, obj["id"], "object", obj["name"], obj.get("capabilities", []))
        _upsert_relation(conn, obj["room"], "contains", obj["id"])
        set_field(
            conn,
            obj["id"],
            "game.effects",
            obj.get("effects", {}),
            mode="static",
            authority="world_definition",
            source=revision,
        )

    locked = set(world.get("traversal_boundaries", []))
    for left, right in world["connections"]:
        if left in locked or right in locked:
            continue
        _upsert_relation(conn, left, "connected_to", right)
        _upsert_relation(conn, right, "connected_to", left)

    import_seed(conn, load_seed(DARIAN_SEED_PATH))

    defaults = load_seed(DARIAN_RUNTIME_DEFAULTS_PATH)
    for field_key, record in defaults.get("values", {}).items():
        set_field(
            conn,
            defaults["entity_id"],
            field_key,
            record["value"],
            mode=record["mode"],
            authority=record["authority"],
            source=defaults.get("runtime_profile_defaults_revision", "runtime-defaults"),
        )

    initial = {
        "runtime.location": world["start_location"],
        "runtime.current_action": "idle",
        "needs.energy": 75.0,
        "needs.hunger": 20.0,
        "needs.thirst": 15.0,
        "needs.sleepiness": 15.0,
        "physiology.cleanliness": 80.0,
    }
    for key, value in initial.items():
        if conn.execute(
            "SELECT 1 FROM fields WHERE entity_id='char_darian' AND field_key=?",
            (key,),
        ).fetchone() is None:
            set_field(conn, "char_darian", key, value)

    # `home` is now the estate location node rather than the world root. Keeping
    # the stable id preserves existing observer links/history while allowing a
    # future South Lake Tahoe node to become its parent without another id migration.
    conn.execute("DELETE FROM relations WHERE relation_type='resident' AND target_id='char_darian'")
    _upsert_relation(conn, "home", "resident", "char_darian")
    conn.commit()

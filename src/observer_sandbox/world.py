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

LEGACY_LOCATION_ID_MAP = {
    "home": "loc_thorne_estate",
    "zone_ground": "loc_thorne_estate_ground_floor",
    "zone_second": "loc_thorne_estate_second_floor",
    "zone_third": "loc_thorne_estate_third_floor",
    "zone_underground": "loc_thorne_estate_underground",
    "room_foyer": "loc_thorne_estate_foyer",
    "room_living": "loc_thorne_estate_living_room",
    "room_kitchen": "loc_thorne_estate_kitchen",
    "room_dining": "loc_thorne_estate_dining_area",
    "room_library": "loc_thorne_estate_library",
    "room_garage": "loc_thorne_estate_garage",
    "room_bedroom": "loc_thorne_estate_master_suite",
    "room_bathroom": "loc_thorne_estate_master_bathroom",
    "room_quasi": "loc_thorne_estate_quasi_room",
    "room_guest": "loc_thorne_estate_guest_rooms",
    "room_intel": "loc_thorne_estate_intelligence_hub",
    "room_comms": "loc_thorne_estate_comms",
    "room_training": "loc_thorne_estate_training_hall",
    "room_gym": "loc_thorne_estate_home_gym",
    "room_medical": "loc_thorne_estate_medical_bay",
    "room_armory": "loc_thorne_estate_armory",
    "room_food_storage": "loc_thorne_estate_food_storage",
    "room_bunker": "loc_thorne_estate_bunker",
    "boundary_exterior": "loc_thorne_estate_exterior_boundary",
}

LEGACY_OBJECT_IDS = {
    "obj_bed",
    "obj_nightstand",
    "obj_shower",
    "obj_sink",
    "obj_toilet",
    "obj_fridge",
    "obj_pantry",
    "obj_stove",
    "obj_table",
    "obj_sofa",
    "obj_bookshelf",
    "obj_water",
    "obj_meal_stock",
    "obj_weights",
    "obj_heavy_bag",
}

LEGACY_SPATIAL_IDS = set(LEGACY_LOCATION_ID_MAP) | LEGACY_OBJECT_IDS | {"observer_universe"}


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


def _runtime_value(conn: sqlite3.Connection, key: str, default: Any = None) -> Any:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (key,)).fetchone()
    return default if row is None else json.loads(row[0])


def _set_runtime_value(conn: sqlite3.Connection, key: str, value: Any) -> None:
    conn.execute(
        """
        INSERT INTO runtime_state(key, value_json) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json, updated_at=CURRENT_TIMESTAMP
        """,
        (key, json.dumps(value, ensure_ascii=False)),
    )


def _normalized_locations(world: dict[str, Any]) -> list[dict[str, Any]]:
    if world.get("locations"):
        return list(world["locations"])
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


def _legacy_spatial_graph_exists(conn: sqlite3.Connection) -> bool:
    placeholders = ",".join("?" for _ in LEGACY_SPATIAL_IDS)
    row = conn.execute(
        f"SELECT 1 FROM entities WHERE id IN ({placeholders}) LIMIT 1",
        tuple(sorted(LEGACY_SPATIAL_IDS)),
    ).fetchone()
    return row is not None


def _prepare_scoped_identity_migration(conn: sqlite3.Connection, world: dict[str, Any]) -> bool:
    revision = world.get("revision", "world")
    if _runtime_value(conn, "world_identity_revision") == revision:
        return False
    if not _legacy_spatial_graph_exists(conn):
        return False

    previous_paused = bool(_runtime_value(conn, "paused", False))
    _set_runtime_value(conn, "world_identity_resume_paused", previous_paused)
    _set_runtime_value(conn, "paused", True)
    _set_runtime_value(conn, "autonomy_pending_action", None)
    _set_runtime_value(conn, "autonomy_lease", None)
    _set_runtime_value(conn, "autonomy_retry", None)
    _set_runtime_value(conn, "cognition_wake_reason", "world_identity_migrated")

    current_location = get_field(conn, "char_darian", "runtime.location", None)
    mapped_location = LEGACY_LOCATION_ID_MAP.get(current_location, world["start_location"])
    set_field(conn, "char_darian", "runtime.location", mapped_location)
    set_field(conn, "char_darian", "runtime.current_action", "idle")

    # Commit the pause before destructive graph work so the still-running old
    # service cannot complete a stale legacy-id action during deployment.
    conn.commit()

    placeholders = ",".join("?" for _ in LEGACY_SPATIAL_IDS)
    conn.execute(
        f"DELETE FROM entities WHERE id IN ({placeholders})",
        tuple(sorted(LEGACY_SPATIAL_IDS)),
    )
    _set_runtime_value(conn, "world_id", world["world_id"])
    conn.commit()
    return True


def _restore_pause_after_migration(conn: sqlite3.Connection, revision: str, migrated_now: bool) -> None:
    if migrated_now:
        return
    if _runtime_value(conn, "world_identity_revision") != revision:
        return
    resume_value = _runtime_value(conn, "world_identity_resume_paused", None)
    if resume_value is None:
        return
    _set_runtime_value(conn, "paused", bool(resume_value))
    conn.execute("DELETE FROM runtime_state WHERE key='world_identity_resume_paused'")


def _rebuild_seed_topology(conn: sqlite3.Connection, world: dict[str, Any], locations: list[dict[str, Any]]) -> None:
    location_ids = [loc["id"] for loc in locations]
    object_ids = [obj["id"] for obj in world.get("objects", [])]

    for target_id in location_ids + object_ids:
        conn.execute("DELETE FROM relations WHERE relation_type='contains' AND target_id=?", (target_id,))

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
    migrated_now = _prepare_scoped_identity_migration(conn, world)

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

    conn.execute("DELETE FROM relations WHERE relation_type='resident' AND target_id='char_darian'")
    _upsert_relation(conn, "loc_thorne_estate", "resident", "char_darian")
    _set_runtime_value(conn, "world_id", world["world_id"])
    _set_runtime_value(conn, "world_identity_revision", revision)
    _restore_pause_after_migration(conn, revision, migrated_now)
    conn.commit()

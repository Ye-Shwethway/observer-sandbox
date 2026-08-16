from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .world import set_field


REPO_ROOT = Path(__file__).resolve().parents[2]
CAMPUS_SEED_PATH = REPO_ROOT / "config" / "worlds" / "estate_campus.v1.json"


def load_estate_campus_seed(path: str | Path = CAMPUS_SEED_PATH) -> dict[str, Any]:
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


def _set_runtime_value(conn: sqlite3.Connection, key: str, value: Any) -> None:
    conn.execute(
        """
        INSERT INTO runtime_state(key, value_json) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET
            value_json=excluded.value_json,
            updated_at=CURRENT_TIMESTAMP
        """,
        (key, json.dumps(value, ensure_ascii=False)),
    )


def seed_estate_campus(conn: sqlite3.Connection) -> None:
    """Seed the bounded private Estate campus without opening any outside-world edge."""
    seed = load_estate_campus_seed()
    revision = str(seed["revision"])

    for location in seed.get("locations", []):
        location_id = str(location["id"])
        _upsert_entity(conn, location_id, "location", str(location["name"]), ["inspect", "enter", "leave"])
        _upsert_relation(conn, str(location["parent"]), "contains", location_id)
        set_field(
            conn,
            location_id,
            "world.location_kind",
            location.get("kind", "location"),
            mode="static",
            authority="world_definition",
            source=revision,
        )
        set_field(
            conn,
            location_id,
            "world.access",
            location.get("access", "resident"),
            mode="static",
            authority="world_definition",
            source=revision,
        )
        set_field(
            conn,
            location_id,
            "world.canon",
            bool(location.get("canon", False)),
            mode="static",
            authority="world_definition",
            source=revision,
        )
        set_field(
            conn,
            location_id,
            "world.metadata",
            location.get("metadata", {}),
            mode="static",
            authority="world_definition",
            source=revision,
        )
        set_field(
            conn,
            location_id,
            "world.spatial_container",
            location.get("spatial", {}),
            mode="static",
            authority="world_definition",
            source=revision,
        )

    for obj in seed.get("objects", []):
        object_id = str(obj["id"])
        _upsert_entity(
            conn,
            object_id,
            "object",
            str(obj["name"]),
            list(obj.get("capabilities", [])),
        )
        _upsert_relation(conn, str(obj["location"]), "contains", object_id)
        set_field(
            conn,
            object_id,
            "game.effects",
            obj.get("effects", {}),
            mode="static",
            authority="world_definition",
            source=revision,
        )

    for left, right in seed.get("connections", []):
        _upsert_relation(conn, str(left), "connected_to", str(right))
        _upsert_relation(conn, str(right), "connected_to", str(left))

    # Deliberately no external edge is seeded from the Main Security Gate,
    # Concealed Forest Passage, Hidden Dock, or the legacy exterior boundary.
    _set_runtime_value(conn, "estate_campus_revision", revision)
    conn.commit()

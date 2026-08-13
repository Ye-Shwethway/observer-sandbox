from __future__ import annotations

import sqlite3

from .world import get_field, set_field


DYNAMIC_LOCATION_RELATION = "located_at"


def current_location(conn: sqlite3.Connection, entity_id: str, default: str | None = None) -> str | None:
    """Return an entity's current physical location.

    `located_at` is the generic dynamic-location relation. During the character
    compatibility period, `runtime.location` remains a mirrored cache/fallback.
    Static fixtures may still derive their place from structural `contains`.
    """
    row = conn.execute(
        "SELECT target_id FROM relations WHERE source_id=? AND relation_type=? ORDER BY id DESC LIMIT 1",
        (entity_id, DYNAMIC_LOCATION_RELATION),
    ).fetchone()
    if row is not None:
        return str(row[0])

    cached = get_field(conn, entity_id, "runtime.location", None)
    if cached is not None:
        return str(cached)

    row = conn.execute(
        """SELECT source_id FROM relations
        WHERE target_id=? AND relation_type='contains'
        ORDER BY id DESC LIMIT 1""",
        (entity_id,),
    ).fetchone()
    return str(row[0]) if row is not None else default


def set_dynamic_location(conn: sqlite3.Connection, entity_id: str, location_id: str) -> None:
    row = conn.execute(
        "SELECT entity_type FROM entities WHERE id=?",
        (location_id,),
    ).fetchone()
    if row is None or row[0] not in {"location", "world"}:
        raise ValueError(f"Dynamic location target does not exist or is not spatial: {location_id}")

    conn.execute(
        "DELETE FROM relations WHERE source_id=? AND relation_type=?",
        (entity_id, DYNAMIC_LOCATION_RELATION),
    )
    conn.execute(
        "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
        (entity_id, DYNAMIC_LOCATION_RELATION, location_id),
    )

    entity = conn.execute("SELECT entity_type FROM entities WHERE id=?", (entity_id,)).fetchone()
    if entity is not None and entity[0] == "character":
        set_field(conn, entity_id, "runtime.location", location_id)

from __future__ import annotations

import json
import sqlite3


DEFAULT_ACTOR_KEY = "default_actor_id"


def list_actor_ids(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute(
        "SELECT id FROM entities WHERE entity_type='character' ORDER BY id"
    ).fetchall()
    return [str(row[0]) for row in rows]


def _runtime_default(conn: sqlite3.Connection) -> str | None:
    row = conn.execute(
        "SELECT value_json FROM runtime_state WHERE key=?",
        (DEFAULT_ACTOR_KEY,),
    ).fetchone()
    if row is None:
        return None
    value = json.loads(row[0])
    return value if isinstance(value, str) and value else None


def _is_character(conn: sqlite3.Connection, actor_id: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='character'",
        (actor_id,),
    ).fetchone()
    return row is not None


def ensure_default_actor_id(conn: sqlite3.Connection) -> str | None:
    configured = _runtime_default(conn)
    if configured and _is_character(conn, configured):
        return configured

    actors = list_actor_ids(conn)
    if len(actors) != 1:
        return None

    actor_id = actors[0]
    conn.execute(
        "INSERT OR REPLACE INTO runtime_state(key,value_json) VALUES(?,?)",
        (DEFAULT_ACTOR_KEY, json.dumps(actor_id)),
    )
    conn.commit()
    return actor_id


def resolve_actor_id(conn: sqlite3.Connection, actor_id: str | None = None) -> str:
    if actor_id is not None:
        value = str(actor_id)
        if not _is_character(conn, value):
            raise KeyError(f"Unknown character: {value}")
        return value

    configured = _runtime_default(conn)
    if configured and _is_character(conn, configured):
        return configured

    actors = list_actor_ids(conn)
    if len(actors) == 1:
        return actors[0]
    if not actors:
        raise KeyError("No character is available")
    raise ValueError(
        "Multiple characters exist and no valid default_actor_id is configured; pass actor_id explicitly"
    )

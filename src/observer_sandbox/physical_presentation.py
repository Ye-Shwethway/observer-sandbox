from __future__ import annotations

import json
import sqlite3
from typing import Any


def _profile_number(conn: sqlite3.Connection, actor_id: str, field_key: str) -> float | None:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    if row is None:
        return None
    try:
        return float(json.loads(row["value_json"]))
    except (TypeError, ValueError, json.JSONDecodeError):
        return None


def abdominal_definition_from_composition(
    body_fat_pct: float,
    sustainable_floor_pct: float,
) -> str:
    """Return a qualitative current-definition label without sex-specific magic thresholds.

    Definition is modeled relative to the actor's authored sustainable body-fat
    floor. This avoids encoding a universal population cutoff while ensuring the
    presentation changes when the authoritative composition changes.
    """
    delta = max(0.0, float(body_fat_pct) - float(sustainable_floor_pct))
    if delta <= 1.5:
        return "peak definition"
    if delta <= 4.0:
        return "high definition"
    if delta <= 7.0:
        return "moderate definition"
    return "limited definition"


def derived_physical_profile_items(
    conn: sqlite3.Connection,
    actor_id: str,
    domains: tuple[str, ...],
) -> list[dict[str, Any]]:
    if "body" not in domains:
        return []
    body_fat = _profile_number(conn, actor_id, "body.body_fat_pct")
    floor = _profile_number(conn, actor_id, "genetics.body_fat_floor_pct")
    if body_fat is None or floor is None:
        return []
    return [
        {
            "kind": "derived",
            "field_key": "body.abdominal_definition",
            "domain": "body",
            "label": "Visible abdominal definition",
            "value": abdominal_definition_from_composition(body_fat, floor),
            "data_type": "text",
            "unit": None,
            "mode": "derived",
        }
    ]

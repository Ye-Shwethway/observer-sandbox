from __future__ import annotations

import json
import sqlite3
from typing import Any

SOURCE = "physical-presentation-v1"


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


def abdominal_definition_from_composition(body_fat_pct: float, sustainable_floor_pct: float) -> str:
    """Return a current-definition label relative to the actor's authored floor."""
    delta = max(0.0, float(body_fat_pct) - float(sustainable_floor_pct))
    if delta <= 1.5:
        return "peak definition"
    if delta <= 4.0:
        return "high definition"
    if delta <= 7.0:
        return "moderate definition"
    return "limited definition"


def refresh_physical_presentation(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
) -> dict[str, Any]:
    """Refresh materialized deterministic presentation fields after body settlement."""
    body_fat = _profile_number(conn, actor_id, "body.body_fat_pct")
    floor = _profile_number(conn, actor_id, "genetics.body_fat_floor_pct")
    if body_fat is None or floor is None:
        return {"status": "deferred_missing_inputs", "mutated": False}

    value = abdominal_definition_from_composition(body_fat, floor)
    value_json = json.dumps(value)
    old = conn.execute(
        "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, "body.abdominal_definition"),
    ).fetchone()
    changed = old is None or old["value_json"] != value_json or old["mode"] != "derived" or old["authority"] != "appearance_engine" or old["source"] != SOURCE

    if changed and old is not None and old["value_json"] != value_json:
        conn.execute(
            """
            INSERT INTO character_profile_history(
                entity_id, field_key, old_value_json, new_value_json, mode, authority, reason, observed_at
            ) VALUES (?, 'body.abdominal_definition', ?, ?, 'derived', 'appearance_engine', 'physical presentation refresh', ?)
            """,
            (actor_id, old["value_json"], value_json, as_of_sim_time),
        )

    conn.execute(
        """
        INSERT INTO character_profile_values(
            entity_id, field_key, value_json, mode, authority, source, confidence, observed_at
        ) VALUES (?, 'body.abdominal_definition', ?, 'derived', 'appearance_engine', ?, 1.0, ?)
        ON CONFLICT(entity_id, field_key) DO UPDATE SET
            value_json=excluded.value_json,
            mode=excluded.mode,
            authority=excluded.authority,
            source=excluded.source,
            confidence=excluded.confidence,
            observed_at=excluded.observed_at,
            updated_at=CURRENT_TIMESTAMP
        """,
        (actor_id, value_json, SOURCE, as_of_sim_time),
    )
    conn.commit()
    return {
        "status": "applied" if changed else "stable",
        "mutated": changed,
        "body_fat_pct": body_fat,
        "sustainable_floor_pct": floor,
        "abdominal_definition": value,
        "source": SOURCE,
    }


def derived_physical_profile_items(conn: sqlite3.Connection, actor_id: str, domains: tuple[str, ...]) -> list[dict[str, Any]]:
    if "body" not in domains:
        return []
    body_fat = _profile_number(conn, actor_id, "body.body_fat_pct")
    floor = _profile_number(conn, actor_id, "genetics.body_fat_floor_pct")
    if body_fat is None or floor is None:
        return []
    return [{
        "kind": "derived",
        "field_key": "body.abdominal_definition",
        "domain": "body",
        "label": "Visible abdominal definition",
        "value": abdominal_definition_from_composition(body_fat, floor),
        "data_type": "text",
        "unit": None,
        "mode": "derived",
    }]

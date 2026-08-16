from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any

from .world import get_field, set_field


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FAMILIARITY_PATH = REPO_ROOT / "config" / "characters" / "darian.spatial_familiarity.v1.json"
FAMILIARITY_FIELD = "world.spatial_familiarity"
FAMILIARITY_LEVELS = ("unknown", "aware", "familiar", "intimate")


def load_spatial_familiarity_seed(path: str | Path = DEFAULT_FAMILIARITY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _validate_seed(conn: sqlite3.Connection, seed: dict[str, Any]) -> tuple[str, str, dict[str, dict[str, Any]]]:
    revision = str(seed.get("revision") or "").strip()
    actor_id = str(seed.get("actor_id") or "").strip()
    if not revision or not actor_id:
        raise ValueError("Spatial familiarity seed requires revision and actor_id")
    actor = conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='character'",
        (actor_id,),
    ).fetchone()
    if actor is None:
        raise ValueError(f"Unknown spatial familiarity actor: {actor_id}")

    authored: dict[str, dict[str, Any]] = {}
    for raw in seed.get("locations", []):
        if not isinstance(raw, dict):
            continue
        location_id = str(raw.get("location_id") or "").strip()
        level = str(raw.get("familiarity") or "unknown").strip()
        if not location_id or level not in FAMILIARITY_LEVELS:
            raise ValueError(f"Invalid spatial familiarity row: {raw!r}")
        exists = conn.execute(
            "SELECT 1 FROM entities WHERE id=? AND entity_type='location'",
            (location_id,),
        ).fetchone()
        if exists is None:
            raise ValueError(f"Unknown spatial familiarity location: {location_id}")
        authored[location_id] = {
            "familiarity": level,
            "secret": bool(raw.get("secret", False)),
            "basis": str(raw.get("basis") or "authored_character_knowledge"),
        }
    return revision, actor_id, authored


def seed_spatial_familiarity(
    conn: sqlite3.Connection,
    *,
    path: str | Path = DEFAULT_FAMILIARITY_PATH,
) -> None:
    """Seed explicit character-known geography without inventing episodic memory.

    This is authored world knowledge, not a general memory system. Unlisted
    locations remain unspecified/unknown to cognition rather than being inferred
    from world existence or event history.
    """
    seed = load_spatial_familiarity_seed(path)
    revision, actor_id, authored = _validate_seed(conn, seed)
    set_field(
        conn,
        actor_id,
        FAMILIARITY_FIELD,
        {
            "revision": revision,
            "levels": list(FAMILIARITY_LEVELS),
            "locations": authored,
        },
        mode="static",
        authority="character_definition",
        source=revision,
    )
    conn.execute(
        """
        INSERT INTO runtime_state(key,value_json) VALUES('spatial_familiarity_revision',?)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=CURRENT_TIMESTAMP
        """,
        (json.dumps(revision),),
    )
    conn.commit()


def spatial_familiarity_state(conn: sqlite3.Connection, actor_id: str) -> dict[str, Any] | None:
    value = get_field(conn, actor_id, FAMILIARITY_FIELD, None)
    return value if isinstance(value, dict) else None


def location_familiarity(conn: sqlite3.Connection, actor_id: str, location_id: str) -> dict[str, Any] | None:
    state = spatial_familiarity_state(conn, actor_id)
    if state is None:
        return None
    locations = state.get("locations")
    if not isinstance(locations, dict):
        return None
    row = locations.get(location_id)
    return dict(row) if isinstance(row, dict) else None


def location_known(conn: sqlite3.Connection, actor_id: str, location_id: str) -> bool:
    state = spatial_familiarity_state(conn, actor_id)
    if state is None:
        # Characters without an authored familiarity model keep legacy behavior.
        return True
    row = location_familiarity(conn, actor_id, location_id)
    return bool(row and row.get("familiarity") in {"aware", "familiar", "intimate"})


def filter_cognition_action_options(
    conn: sqlite3.Connection,
    actor_id: str,
    action_options: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Hide movement targets the actor does not know without changing world truth.

    Deterministic movement topology remains authoritative. This gate only shapes
    autonomous character cognition; Creator/manual runtime authority is not
    rewritten into a memory rule.
    """
    if spatial_familiarity_state(conn, actor_id) is None:
        return action_options
    filtered: list[dict[str, Any]] = []
    for option in action_options:
        if option.get("action") == "move":
            target = option.get("target")
            if isinstance(target, str) and not location_known(conn, actor_id, target):
                continue
        filtered.append(option)
    return filtered


def location_is_globally_hidden(conn: sqlite3.Connection, location_id: str) -> bool:
    metadata = get_field(conn, location_id, "world.metadata", {}) or {}
    return isinstance(metadata, dict) and metadata.get("discovery_visibility") == "hidden"


def spatial_familiarity_context(conn: sqlite3.Connection, actor_id: str) -> dict[str, Any]:
    state = spatial_familiarity_state(conn, actor_id)
    if state is None:
        return {
            "mode": "legacy_unspecified",
            "guidance": "No authored spatial familiarity model exists for this character; do not infer hidden knowledge from this field.",
        }

    raw_locations = state.get("locations") if isinstance(state.get("locations"), dict) else {}
    known_ids = {
        location_id
        for location_id, row in raw_locations.items()
        if isinstance(row, dict) and row.get("familiarity") in {"aware", "familiar", "intimate"}
    }
    grouped: dict[str, list[str]] = {"aware": [], "familiar": [], "intimate": []}
    id_to_name: dict[str, str] = {}
    for location_id in sorted(known_ids):
        row = conn.execute(
            "SELECT name FROM entities WHERE id=? AND entity_type='location'",
            (location_id,),
        ).fetchone()
        if row is None:
            continue
        name = str(row["name"])
        id_to_name[location_id] = name
        level = str(raw_locations[location_id]["familiarity"])
        grouped[level].append(name)

    connections: list[list[str]] = []
    seen_pairs: set[tuple[str, str]] = set()
    if known_ids:
        placeholders = ",".join("?" for _ in known_ids)
        rows = conn.execute(
            f"""
            SELECT source_id,target_id FROM relations
            WHERE relation_type='connected_to'
              AND source_id IN ({placeholders})
              AND target_id IN ({placeholders})
            ORDER BY source_id,target_id
            """,
            tuple(sorted(known_ids)) + tuple(sorted(known_ids)),
        ).fetchall()
        for row in rows:
            left, right = str(row["source_id"]), str(row["target_id"])
            if left not in id_to_name or right not in id_to_name:
                continue
            pair = tuple(sorted((left, right)))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            connections.append([id_to_name[pair[0]], id_to_name[pair[1]]])

    known_secrets = sorted(
        id_to_name[location_id]
        for location_id in known_ids
        if location_id in id_to_name
        and isinstance(raw_locations.get(location_id), dict)
        and bool(raw_locations[location_id].get("secret"))
    )
    return {
        "mode": "authored_spatial_familiarity_v1",
        "revision": state.get("revision"),
        "known_locations_by_familiarity": grouped,
        "known_connections": connections,
        "known_secret_or_concealed_locations": known_secrets,
        "guidance": (
            "This is character knowledge for planning, not immediate reachability. The character may know a distant familiar place while still needing ordinary multi-step movement to reach it. "
            "Locations absent from this projection must not be assumed known. Exact executable movement remains limited to current action_options."
        ),
    }

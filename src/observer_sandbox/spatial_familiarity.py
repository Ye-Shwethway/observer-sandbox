from __future__ import annotations

import json
import sqlite3
from typing import Any

from .semantic_memory_seed import SPATIAL_FAMILIARITY_LEVELS, seed_initial_semantic_memories
from .world import get_field


FAMILIARITY_LEVELS = SPATIAL_FAMILIARITY_LEVELS


def seed_spatial_familiarity(conn: sqlite3.Connection) -> None:
    """Compatibility entrypoint for generic semantic-memory initialization.

    Spatial knowledge is no longer stored in a named-character familiarity file
    or compatibility field. The underlying authority is actor-owned semantic
    Character Memory.
    """
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key='sim_time'").fetchone()
    sim_time = json.loads(row[0]) if row is not None else "2025-05-01T07:00:00+00:00"
    seed_initial_semantic_memories(conn, sim_time=str(sim_time))


def spatial_familiarity_state(conn: sqlite3.Connection, actor_id: str) -> dict[str, Any] | None:
    rows = conn.execute(
        """SELECT memory_id,content_json,metadata_json
           FROM character_memories
           WHERE character_id=? AND memory_type='semantic' AND status='active'
             AND json_extract(content_json,'$.knowledge_kind')='spatial_familiarity'
           ORDER BY memory_id""",
        (actor_id,),
    ).fetchall()
    if not rows:
        return None

    locations: dict[str, dict[str, Any]] = {}
    revisions: set[str] = set()
    for row in rows:
        content = json.loads(row["content_json"] or "{}")
        metadata = json.loads(row["metadata_json"] or "{}")
        location_id = str(content.get("location_id") or "").strip()
        familiarity = str(content.get("familiarity") or "unknown").strip()
        if not location_id or familiarity not in FAMILIARITY_LEVELS:
            continue
        locations[location_id] = {
            "familiarity": familiarity,
            "secret": bool(content.get("secret", False)),
            "basis": str(content.get("basis") or "semantic_memory"),
            "memory_id": str(row["memory_id"]),
        }
        revision = str(metadata.get("seed_revision") or "").strip()
        if revision:
            revisions.add(revision)
    if not locations:
        return None
    return {
        "revision": sorted(revisions)[-1] if revisions else "dynamic-semantic-memory",
        "levels": list(FAMILIARITY_LEVELS),
        "locations": locations,
        "source": "character_semantic_memory",
    }


def location_familiarity(conn: sqlite3.Connection, actor_id: str, location_id: str) -> dict[str, Any] | None:
    state = spatial_familiarity_state(conn, actor_id)
    if state is None:
        return None
    row = state["locations"].get(location_id)
    return dict(row) if isinstance(row, dict) else None


def location_known(conn: sqlite3.Connection, actor_id: str, location_id: str) -> bool:
    state = spatial_familiarity_state(conn, actor_id)
    if state is None:
        # Characters without represented spatial knowledge retain legacy behavior
        # until their knowledge is explicitly initialized or learned.
        return True
    row = location_familiarity(conn, actor_id, location_id)
    return bool(row and row.get("familiarity") in {"aware", "familiar", "intimate"})


def filter_cognition_action_options(
    conn: sqlite3.Connection,
    actor_id: str,
    action_options: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Hide unknown movement targets from cognition without changing topology."""
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


def _outdoor_lifestyle_destination(
    conn: sqlite3.Connection,
    location_id: str,
    *,
    familiarity: str,
) -> dict[str, Any] | None:
    spatial = get_field(conn, location_id, "world.spatial_container", {}) or {}
    if not isinstance(spatial, dict):
        return None
    if spatial.get("exposure") != "outdoor" or not bool(spatial.get("lifestyle_destination")):
        return None
    affordances = [str(value) for value in spatial.get("affordances", []) if isinstance(value, str)]
    if not affordances:
        return None
    row = conn.execute(
        "SELECT name FROM entities WHERE id=? AND entity_type='location'",
        (location_id,),
    ).fetchone()
    if row is None:
        return None
    return {
        "location_name": str(row["name"]),
        "familiarity": familiarity,
        "activities": affordances,
        "atmosphere_tags": [
            str(value) for value in spatial.get("atmosphere_tags", []) if isinstance(value, str)
        ],
        "planning_only": True,
    }


def spatial_familiarity_context(conn: sqlite3.Connection, actor_id: str) -> dict[str, Any]:
    state = spatial_familiarity_state(conn, actor_id)
    if state is None:
        return {
            "mode": "legacy_unspecified",
            "guidance": "No represented spatial knowledge exists for this character; do not infer hidden knowledge from objective world truth.",
        }

    raw_locations = state["locations"]
    known_ids = {
        location_id
        for location_id, row in raw_locations.items()
        if isinstance(row, dict) and row.get("familiarity") in {"aware", "familiar", "intimate"}
    }
    grouped: dict[str, list[str]] = {"aware": [], "familiar": [], "intimate": []}
    id_to_name: dict[str, str] = {}
    outdoor_lifestyle_destinations: list[dict[str, Any]] = []
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
        lifestyle = _outdoor_lifestyle_destination(conn, location_id, familiarity=level)
        if lifestyle is not None and not bool(raw_locations[location_id].get("secret")):
            outdoor_lifestyle_destinations.append(lifestyle)

    connections: list[list[str]] = []
    seen_pairs: set[tuple[str, str]] = set()
    if known_ids:
        placeholders = ",".join("?" for _ in known_ids)
        rows = conn.execute(
            f"""SELECT source_id,target_id FROM relations
                WHERE relation_type='connected_to'
                  AND source_id IN ({placeholders})
                  AND target_id IN ({placeholders})
                ORDER BY source_id,target_id""",
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
        if location_id in id_to_name and bool(raw_locations[location_id].get("secret"))
    )
    return {
        "mode": "semantic_memory_spatial_familiarity_v1",
        "revision": state.get("revision"),
        "known_locations_by_familiarity": grouped,
        "known_connections": connections,
        "known_secret_or_concealed_locations": known_secrets,
        "outdoor_lifestyle_destinations": outdoor_lifestyle_destinations,
        "outdoor_guidance": (
            "Known outdoor lifestyle destinations are ordinary lived spaces, not merely transit nodes. Walking, quiet relaxation, and observing represented surroundings may be worthwhile discretionary activities when no stronger need dominates. Treat them as alternatives, never quotas or forced outings."
        ),
        "guidance": (
            "This projection is retrieved actor knowledge for planning, not immediate reachability. A known distant place still requires ordinary multi-step movement. Locations absent from represented semantic memory must not be assumed known. Exact executable movement remains limited to current action_options."
        ),
    }

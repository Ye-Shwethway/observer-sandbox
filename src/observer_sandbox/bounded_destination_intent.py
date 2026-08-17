from __future__ import annotations

import sqlite3
from collections import deque
from typing import Any

from .location_runtime import current_location
from .simulation import action_options
from .spatial_familiarity import spatial_familiarity_state
from .world import get_field


MAX_ROUTE_HOPS = 4
MAX_ROUTE_HINTS = 12


def _location_name(conn: sqlite3.Connection, location_id: str) -> str | None:
    row = conn.execute(
        "SELECT name FROM entities WHERE id=? AND entity_type='location'",
        (location_id,),
    ).fetchone()
    return str(row["name"]) if row is not None else None


def _location_affordances(conn: sqlite3.Connection, location_id: str) -> list[str]:
    spatial = get_field(conn, location_id, "world.spatial_container", {}) or {}
    if not isinstance(spatial, dict):
        return []
    return sorted({
        str(value)
        for value in spatial.get("affordances", [])
        if isinstance(value, str)
    })


def _known_neighbors(
    conn: sqlite3.Connection,
    node_id: str,
    known_ids: set[str],
) -> list[str]:
    rows = conn.execute(
        """SELECT target_id FROM relations
           WHERE source_id=? AND relation_type='connected_to'
           ORDER BY target_id""",
        (node_id,),
    ).fetchall()
    return [str(row["target_id"]) for row in rows if str(row["target_id"]) in known_ids]


def bounded_destination_intent_awareness(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    max_hops: int = MAX_ROUTE_HOPS,
    max_hints: int = MAX_ROUTE_HINTS,
) -> dict[str, Any]:
    """Expose bounded actor-known multi-hop route purpose without granting action authority.

    The returned route hints intentionally omit technical destination IDs. They make
    a distant known destination and its first ordinary hop legible to cognition,
    while the only executable target remains an exact current ``action_options``
    move target. No intention/plan artifact is stored; the hints are recomputed at
    every decision boundary from current topology, actor knowledge and location.
    """
    state = spatial_familiarity_state(conn, actor_id)
    if state is None:
        return {
            "mode": "unavailable_without_represented_spatial_knowledge",
            "max_hops": int(max_hops),
            "routes": [],
            "guidance": (
                "No multi-step route preview is exposed because this actor has no represented spatial knowledge."
            ),
        }

    origin = current_location(conn, actor_id)
    if not origin:
        return {
            "mode": "unavailable_without_current_location",
            "max_hops": int(max_hops),
            "routes": [],
            "guidance": "No multi-step route preview is available without a current location.",
        }

    known_ids = {
        str(location_id)
        for location_id, row in (state.get("locations") or {}).items()
        if isinstance(row, dict) and row.get("familiarity") in {"aware", "familiar", "intimate"}
    }
    if origin not in known_ids:
        return {
            "mode": "current_location_not_represented_as_known",
            "max_hops": int(max_hops),
            "routes": [],
            "guidance": (
                "The current location is not represented in actor spatial knowledge, so objective topology is not projected as actor-known planning context."
            ),
        }

    legal_first_hops = {
        str(option["target"]): str(option.get("target_name") or "")
        for option in action_options(conn, actor_id)
        if option.get("action") == "move"
        and isinstance(option.get("target"), str)
        and str(option["target"]) in known_ids
    }
    if not legal_first_hops:
        return {
            "mode": "bounded_route_awareness_v1",
            "max_hops": int(max_hops),
            "routes": [],
            "guidance": "No currently legal known first hop exists for a multi-step destination.",
        }

    max_hops = max(2, min(int(max_hops), MAX_ROUTE_HOPS))
    max_hints = max(1, min(int(max_hints), MAX_ROUTE_HINTS))
    queue: deque[tuple[str, int, str]] = deque()
    best_distance: dict[str, int] = {origin: 0}
    first_hop_for: dict[str, str] = {}

    for first_hop in sorted(legal_first_hops):
        best_distance[first_hop] = 1
        first_hop_for[first_hop] = first_hop
        queue.append((first_hop, 1, first_hop))

    while queue:
        node, distance, first_hop = queue.popleft()
        if distance >= max_hops:
            continue
        for neighbor in _known_neighbors(conn, node, known_ids):
            next_distance = distance + 1
            prior = best_distance.get(neighbor)
            if prior is not None and prior <= next_distance:
                continue
            best_distance[neighbor] = next_distance
            first_hop_for[neighbor] = first_hop
            queue.append((neighbor, next_distance, first_hop))

    candidates: list[dict[str, Any]] = []
    for destination, route_hops in best_distance.items():
        if destination == origin or route_hops < 2 or route_hops > max_hops:
            continue
        first_hop = first_hop_for.get(destination)
        if first_hop not in legal_first_hops:
            continue
        destination_name = _location_name(conn, destination)
        if not destination_name:
            continue
        affordances = _location_affordances(conn, destination)
        candidates.append({
            "destination_name": destination_name,
            "first_hop_name": legal_first_hops[first_hop],
            "route_hops": int(route_hops),
            "arrival_affordances": affordances,
            "planning_only": True,
        })

    candidates.sort(
        key=lambda row: (
            0 if row["arrival_affordances"] else 1,
            int(row["route_hops"]),
            str(row["destination_name"]),
        )
    )
    routes = candidates[:max_hints]
    return {
        "mode": "bounded_route_awareness_v1",
        "max_hops": max_hops,
        "routes": routes,
        "guidance": (
            "These are actor-known planning hints, not plans or action authority. To pursue a distant destination, choose its first_hop_name only when the matching exact move target is present in current action_options. Re-evaluate after every move; needs, access or topology changes may interrupt or redirect the route."
        ),
    }

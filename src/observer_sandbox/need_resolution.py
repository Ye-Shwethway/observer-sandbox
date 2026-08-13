from __future__ import annotations

import json
import sqlite3
from collections import deque
from typing import Any


HUNGER_FIELD_KEY = "needs.hunger"


def _effect_reduces_field(spec: Any, *, current_value: float) -> bool:
    if isinstance(spec, (int, float)):
        return float(spec) < 0.0
    if not isinstance(spec, dict):
        return False
    if isinstance(spec.get("add"), (int, float)) and float(spec["add"]) < 0.0:
        return True
    if isinstance(spec.get("multiply"), (int, float)) and 0.0 <= float(spec["multiply"]) < 1.0:
        return True
    if isinstance(spec.get("set"), (int, float)) and float(spec["set"]) < current_value:
        return True
    if isinstance(spec.get("clamp_max"), (int, float)) and float(spec["clamp_max"]) < current_value:
        return True
    return False


def _option_reduces_hunger(option: dict[str, Any], *, current_hunger: float) -> bool:
    if option.get("action") != "eat":
        return False
    effects = option.get("effects")
    if not isinstance(effects, dict):
        return False
    return _effect_reduces_field(effects.get(HUNGER_FIELD_KEY), current_value=current_hunger)


def _hunger_resolver_rooms(conn: sqlite3.Connection, *, current_hunger: float) -> set[str]:
    rows = conn.execute(
        """
        SELECT r.source_id AS room_id,e.capabilities_json,f.value_json
        FROM relations r
        JOIN entities e ON e.id=r.target_id
        JOIN fields f ON f.entity_id=e.id AND f.field_key='game.effects'
        WHERE r.relation_type='contains' AND e.entity_type='object'
        """
    ).fetchall()
    rooms: set[str] = set()
    for row in rows:
        capabilities = json.loads(row["capabilities_json"] or "[]")
        if "eat" not in capabilities:
            continue
        effects = json.loads(row["value_json"] or "{}")
        eat_effects = effects.get("eat") if isinstance(effects, dict) else None
        if not isinstance(eat_effects, dict):
            continue
        if _effect_reduces_field(eat_effects.get(HUNGER_FIELD_KEY), current_value=current_hunger):
            rooms.add(str(row["room_id"]))
    return rooms


def _nearest_first_hops(
    conn: sqlite3.Connection,
    *,
    start_room: str,
    destination_rooms: set[str],
) -> set[str]:
    if not destination_rooms or start_room in destination_rooms:
        return set()

    rows = conn.execute(
        "SELECT source_id,target_id FROM relations WHERE relation_type='connected_to'"
    ).fetchall()
    adjacency: dict[str, set[str]] = {}
    for row in rows:
        adjacency.setdefault(str(row["source_id"]), set()).add(str(row["target_id"]))

    queue: deque[tuple[str, str | None, int]] = deque([(start_room, None, 0)])
    best_seen: dict[str, int] = {start_room: 0}
    best_distance: int | None = None
    first_hops: set[str] = set()

    while queue:
        node, first_hop, distance = queue.popleft()
        if best_distance is not None and distance >= best_distance:
            continue
        for neighbor in sorted(adjacency.get(node, set())):
            next_distance = distance + 1
            hop = neighbor if first_hop is None else first_hop
            if neighbor in destination_rooms:
                if best_distance is None or next_distance < best_distance:
                    best_distance = next_distance
                    first_hops = {hop}
                elif next_distance == best_distance:
                    first_hops.add(hop)
                continue
            previous_distance = best_seen.get(neighbor)
            if previous_distance is not None and previous_distance < next_distance:
                continue
            best_seen[neighbor] = next_distance
            queue.append((neighbor, hop, next_distance))
    return first_hops


def shape_action_options_for_needs(
    conn: sqlite3.Connection,
    *,
    state: dict[str, Any],
    action_options: list[dict[str, Any]],
    decision_signals: dict[str, Any],
) -> list[dict[str, Any]]:
    """Prevent causally useless discretionary behavior under strong hunger.

    v1 deliberately covers hunger only. If strong/critical hunger is active and no
    different critical physiological need competes for priority, expose only a
    local authored hunger-reducing eat action, or otherwise only shortest-path
    movement that makes causal progress toward a room containing such a resolver.

    If no authored resolver or route exists, preserve the original options rather
    than deadlocking autonomy; that missing-world-data condition remains observable.
    """
    attention = decision_signals.get("needs_attention") or []
    hunger_signal = next((item for item in attention if item.get("need") == "hunger"), None)
    if not isinstance(hunger_signal, dict):
        return action_options

    competing_critical = any(
        item.get("level") == "critical" and item.get("need") != "hunger"
        for item in attention
        if isinstance(item, dict)
    )
    if competing_critical:
        return action_options

    current_hunger = float(state["hunger"])
    local_resolvers = [
        option
        for option in action_options
        if _option_reduces_hunger(option, current_hunger=current_hunger)
    ]
    if local_resolvers:
        return local_resolvers

    destination_rooms = _hunger_resolver_rooms(conn, current_hunger=current_hunger)
    first_hops = _nearest_first_hops(
        conn,
        start_room=str(state["location"]),
        destination_rooms=destination_rooms,
    )
    if not first_hops:
        return action_options

    movement = [
        option
        for option in action_options
        if option.get("action") == "move" and option.get("target") in first_hops
    ]
    return movement or action_options

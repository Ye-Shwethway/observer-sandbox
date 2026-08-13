from __future__ import annotations

import json
import sqlite3
from collections import deque
from typing import Any


NEED_RESOLVERS: dict[str, dict[str, str]] = {
    "hunger": {"field_key": "needs.hunger", "action": "eat"},
    "thirst": {"field_key": "needs.thirst", "action": "drink"},
}


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


def _option_reduces_need(
    option: dict[str, Any],
    *,
    action: str,
    field_key: str,
    current_value: float,
) -> bool:
    if option.get("action") != action:
        return False
    effects = option.get("effects")
    if not isinstance(effects, dict):
        return False
    return _effect_reduces_field(effects.get(field_key), current_value=current_value)


def _resolver_rooms(
    conn: sqlite3.Connection,
    *,
    action: str,
    field_key: str,
    current_value: float,
) -> set[str]:
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
        if action not in capabilities:
            continue
        effects = json.loads(row["value_json"] or "{}")
        action_effects = effects.get(action) if isinstance(effects, dict) else None
        if not isinstance(action_effects, dict):
            continue
        if _effect_reduces_field(action_effects.get(field_key), current_value=current_value):
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


def _active_supported_need(decision_signals: dict[str, Any]) -> dict[str, Any] | None:
    """Return the highest-priority need only when this guard can resolve it.

    needs_attention is already ordered by the authored autonomy policy. Never skip
    over an unsupported higher-priority need to force a lower thirst/hunger action.
    """
    attention = decision_signals.get("needs_attention") or []
    first = next((item for item in attention if isinstance(item, dict)), None)
    if not isinstance(first, dict):
        return None
    return first if first.get("need") in NEED_RESOLVERS else None


def shape_action_options_for_needs(
    conn: sqlite3.Connection,
    *,
    state: dict[str, Any],
    action_options: list[dict[str, Any]],
    decision_signals: dict[str, Any],
) -> list[dict[str, Any]]:
    """Expose only causal recovery choices for supported strong physiological needs.

    v2 covers hunger and thirst using the same authored-affordance pattern. When the
    highest-priority strong/critical need is supported, expose only a local action
    whose authored effect reduces that need, or otherwise shortest-path movement
    toward the nearest room containing such a resolver.

    If no authored resolver or route exists, preserve the original options rather
    than deadlocking autonomy; the missing-world-data condition remains observable.
    """
    active = _active_supported_need(decision_signals)
    if active is None:
        return action_options

    need = str(active["need"])
    resolver = NEED_RESOLVERS[need]
    field_key = resolver["field_key"]
    action = resolver["action"]
    current_value = float(state[need])

    local_resolvers = [
        option
        for option in action_options
        if _option_reduces_need(
            option,
            action=action,
            field_key=field_key,
            current_value=current_value,
        )
    ]
    if local_resolvers:
        return local_resolvers

    destination_rooms = _resolver_rooms(
        conn,
        action=action,
        field_key=field_key,
        current_value=current_value,
    )
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

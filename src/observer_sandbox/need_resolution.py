from __future__ import annotations

import json
import sqlite3
from collections import deque
from typing import Any


NEEDS: dict[str, dict[str, Any]] = {
    "sleepiness": {"field": "needs.sleepiness", "state": "sleepiness", "direction": -1, "strong": ("rest", "sleep"), "critical": ("sleep",)},
    "energy": {"field": "needs.energy", "state": "energy", "direction": 1, "strong": ("rest", "sleep"), "critical": ("rest", "sleep")},
    "thirst": {"field": "needs.thirst", "state": "thirst", "direction": -1, "strong": ("drink",), "critical": ("drink",)},
    "hunger": {"field": "needs.hunger", "state": "hunger", "direction": -1, "strong": ("eat",), "critical": ("eat",)},
    "cleanliness": {"field": "physiology.cleanliness", "state": "cleanliness", "direction": 1, "strong": ("shower",), "critical": ("shower",)},
}


def _better(spec: Any, current: float, direction: int) -> bool:
    if isinstance(spec, (int, float)):
        return float(spec) * direction > 0
    if not isinstance(spec, dict):
        return False
    add = spec.get("add")
    if isinstance(add, (int, float)) and float(add) * direction > 0:
        return True
    mul = spec.get("multiply")
    if isinstance(mul, (int, float)) and current > 0:
        return (float(mul) - 1.0) * direction > 0
    target = spec.get("set")
    if isinstance(target, (int, float)) and (float(target) - current) * direction > 0:
        return True
    low, high = spec.get("clamp_min"), spec.get("clamp_max")
    return bool((direction > 0 and isinstance(low, (int, float)) and float(low) > current) or (direction < 0 and isinstance(high, (int, float)) and float(high) < current))


def _option_better(option: dict[str, Any], cfg: dict[str, Any], actions: tuple[str, ...], current: float) -> bool:
    if option.get("action") not in actions:
        return False
    direct = option.get("effects") or {}
    intrinsic = option.get("effects_per_hour") or {}
    return _better(direct.get(cfg["field"]), current, cfg["direction"]) or _better(intrinsic.get(cfg["state"]), current, cfg["direction"])


def _resolver_rooms(conn: sqlite3.Connection, cfg: dict[str, Any], actions: tuple[str, ...], current: float, intrinsic: dict[str, dict[str, float]]) -> set[str]:
    rows = conn.execute("""
        SELECT r.source_id room_id,e.capabilities_json,COALESCE(f.value_json,'{}') value_json
        FROM relations r JOIN entities e ON e.id=r.target_id
        LEFT JOIN fields f ON f.entity_id=e.id AND f.field_key='game.effects'
        WHERE r.relation_type='contains' AND e.entity_type='object'
    """).fetchall()
    rooms: set[str] = set()
    for row in rows:
        caps = json.loads(row["capabilities_json"] or "[]")
        direct = json.loads(row["value_json"] or "{}")
        for action in actions:
            if action not in caps:
                continue
            action_effects = direct.get(action, {}) if isinstance(direct, dict) else {}
            if _better(action_effects.get(cfg["field"]), current, cfg["direction"]) or _better(intrinsic.get(action, {}).get(cfg["state"]), current, cfg["direction"]):
                rooms.add(str(row["room_id"]))
                break
    return rooms


def _first_hops(conn: sqlite3.Connection, start: str, goals: set[str]) -> set[str]:
    if not goals or start in goals:
        return set()
    graph: dict[str, set[str]] = {}
    for row in conn.execute("SELECT source_id,target_id FROM relations WHERE relation_type='connected_to'"):
        graph.setdefault(str(row["source_id"]), set()).add(str(row["target_id"]))
    q = deque([(start, None, 0)])
    seen = {start: 0}
    best = None
    hops: set[str] = set()
    while q:
        node, first, dist = q.popleft()
        if best is not None and dist >= best:
            continue
        for nxt in sorted(graph.get(node, set())):
            nd = dist + 1
            hop = nxt if first is None else first
            if nxt in goals:
                if best is None or nd < best:
                    best, hops = nd, {hop}
                elif nd == best:
                    hops.add(hop)
                continue
            if seen.get(nxt, nd) < nd:
                continue
            seen[nxt] = nd
            q.append((nxt, hop, nd))
    return hops


def shape_action_options_for_needs(conn: sqlite3.Connection, *, state: dict[str, Any], action_options: list[dict[str, Any]], decision_signals: dict[str, Any], intrinsic_effects_per_hour: dict[str, dict[str, float]] | None = None) -> list[dict[str, Any]]:
    attention = decision_signals.get("needs_attention") or []
    active = next((x for x in attention if isinstance(x, dict)), None)
    if not active or active.get("need") not in NEEDS:
        return action_options
    cfg = NEEDS[str(active["need"])]
    actions = tuple(cfg["critical"] if active.get("level") == "critical" else cfg["strong"])
    current = float(state[cfg["state"]])
    intrinsic = intrinsic_effects_per_hour or {}
    local = [o for o in action_options if _option_better(o, cfg, actions, current)]
    if local:
        return local
    goals = _resolver_rooms(conn, cfg, actions, current, intrinsic)
    hops = _first_hops(conn, str(state["location"]), goals)
    movement = [o for o in action_options if o.get("action") == "move" and o.get("target") in hops]
    return movement or action_options

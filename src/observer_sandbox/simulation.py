from __future__ import annotations

import json
import sqlite3
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Protocol

from .world import get_field, set_field


@dataclass(frozen=True)
class Action:
    name: str
    duration_minutes: int
    target: str | None = None
    reason: str | None = None


class DecisionProvider(Protocol):
    def choose(self, snapshot: dict[str, Any], available_actions: list[str]) -> Action: ...


ACTION_NAMES = ["move", "sleep", "eat", "drink", "shower", "rest", "inspect", "use", "train", "read", "idle"]

ACTION_DURATION_BOUNDS: dict[str, tuple[int, int]] = {
    "move": (1, 30), "sleep": (30, 720), "eat": (5, 90), "drink": (1, 30),
    "shower": (5, 60), "rest": (5, 240), "inspect": (1, 60), "use": (1, 120),
    "train": (10, 240), "read": (5, 240), "idle": (1, 120),
}

ACTION_CAPABILITY: dict[str, str] = {
    "sleep": "sleep", "eat": "eat", "drink": "drink", "shower": "shower", "rest": "rest",
    "inspect": "inspect", "use": "use", "train": "train", "read": "read",
}

PHYSIOLOGY_FIELDS = {
    "needs.energy": "energy",
    "needs.hunger": "hunger",
    "needs.thirst": "thirst",
    "needs.sleepiness": "sleepiness",
    "physiology.cleanliness": "cleanliness",
}

PASSIVE_DRIFT_PER_HOUR = {
    "energy": -2.0,
    "hunger": 2.5,
    "thirst": 3.0,
    "sleepiness": 3.0,
    "cleanliness": -0.8,
}

ACTION_EFFECTS_PER_HOUR: dict[str, dict[str, float]] = {
    "sleep": {"energy": 11.0, "sleepiness": -15.0, "hunger": 0.5, "thirst": 0.75},
    "rest": {"energy": 10.0, "sleepiness": -4.0},
    "train": {"energy": -10.0, "hunger": 4.0, "thirst": 6.0, "cleanliness": -6.0},
    "read": {"energy": -0.5},
    "idle": {"energy": 3.0},
}

MASTER_SUITE = "loc_thorne_estate_master_suite"
MASTER_BATHROOM = "loc_thorne_estate_master_bathroom"
LIVING_ROOM = "loc_thorne_estate_living_room"
KITCHEN = "loc_thorne_estate_kitchen"
HOME_GYM = "loc_thorne_estate_home_gym"
LIBRARY = "loc_thorne_estate_library"

MASTER_BED = "obj_thorne_estate_master_bed"
MASTER_SHOWER = "obj_thorne_estate_master_shower"
DRINKING_WATER = "obj_thorne_estate_kitchen_drinking_water"
MEAL_INGREDIENTS = "obj_thorne_estate_kitchen_meal_ingredients"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"
LIBRARY_BOOKSHELF = "obj_thorne_estate_library_bookshelf"
LIVING_SOFA = "obj_thorne_estate_living_sofa"


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, round(value, 3)))


def runtime_value(conn: sqlite3.Connection, key: str, default: Any) -> Any:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (key,)).fetchone()
    return default if row is None else json.loads(row[0])


def set_runtime_value(conn: sqlite3.Connection, key: str, value: Any) -> None:
    conn.execute(
        """INSERT INTO runtime_state(key, value_json) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json, updated_at=CURRENT_TIMESTAMP""",
        (key, json.dumps(value)),
    )


def ensure_sim_clock(conn: sqlite3.Connection) -> datetime:
    raw = runtime_value(conn, "sim_time", None)
    if raw is None:
        start = datetime(2025, 5, 1, 7, 0, tzinfo=timezone.utc)
        set_runtime_value(conn, "sim_time", start.isoformat())
        conn.commit()
        return start
    return datetime.fromisoformat(raw)


def snapshot(conn: sqlite3.Connection, actor_id: str = "char_darian") -> dict[str, Any]:
    location = get_field(conn, actor_id, "runtime.location", MASTER_SUITE)
    room = conn.execute("SELECT name FROM entities WHERE id=?", (location,)).fetchone()
    return {
        "actor_id": actor_id, "sim_time": ensure_sim_clock(conn).isoformat(), "location": location,
        "location_name": room[0] if room else location,
        "current_action": get_field(conn, actor_id, "runtime.current_action", "idle"),
        "energy": float(get_field(conn, actor_id, "needs.energy", 75.0)),
        "hunger": float(get_field(conn, actor_id, "needs.hunger", 20.0)),
        "thirst": float(get_field(conn, actor_id, "needs.thirst", 15.0)),
        "sleepiness": float(get_field(conn, actor_id, "needs.sleepiness", 15.0)),
        "cleanliness": float(get_field(conn, actor_id, "physiology.cleanliness", 80.0)),
    }


def _connected(conn: sqlite3.Connection, left: str, right: str) -> bool:
    return conn.execute("SELECT 1 FROM relations WHERE source_id=? AND relation_type='connected_to' AND target_id=?", (left, right)).fetchone() is not None


def _object_effects(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    value = get_field(conn, object_id, "game.effects", {})
    return value if isinstance(value, dict) else {}


def local_objects(conn: sqlite3.Connection, room_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """SELECT e.id, e.name, e.capabilities_json FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='contains' AND e.entity_type='object' ORDER BY e.id""",
        (room_id,),
    ).fetchall()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "capabilities": json.loads(row["capabilities_json"]),
            "effects": _object_effects(conn, row["id"]),
        }
        for row in rows
    ]


def reachable_rooms(conn: sqlite3.Connection, room_id: str) -> list[dict[str, str]]:
    rows = conn.execute(
        """SELECT e.id, e.name FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='connected_to' AND e.entity_type='location' ORDER BY e.id""",
        (room_id,),
    ).fetchall()
    return [{"id": row["id"], "name": row["name"]} for row in rows]


def action_options(conn: sqlite3.Connection, actor_id: str = "char_darian") -> list[dict[str, Any]]:
    room_id = snapshot(conn, actor_id)["location"]
    options: list[dict[str, Any]] = []
    for room in reachable_rooms(conn, room_id):
        options.append({"action": "move", "target": room["id"], "target_name": room["name"], "duration": ACTION_DURATION_BOUNDS["move"]})
    for obj in local_objects(conn, room_id):
        for action, capability in ACTION_CAPABILITY.items():
            if capability in obj["capabilities"]:
                option = {"action": action, "target": obj["id"], "target_name": obj["name"], "duration": ACTION_DURATION_BOUNDS[action]}
                effects = obj["effects"].get(action)
                if effects:
                    option["effects"] = effects
                options.append(option)
    options.append({"action": "rest", "target": None, "target_name": None, "duration": ACTION_DURATION_BOUNDS["rest"], "effects_per_hour": ACTION_EFFECTS_PER_HOUR["rest"]})
    options.append({"action": "idle", "target": None, "target_name": None, "duration": ACTION_DURATION_BOUNDS["idle"], "effects_per_hour": ACTION_EFFECTS_PER_HOUR["idle"]})
    return options


def validate_action(conn: sqlite3.Connection, actor_id: str, action: Action) -> None:
    if action.name not in ACTION_NAMES:
        raise ValueError(f"Unknown action: {action.name}")
    low, high = ACTION_DURATION_BOUNDS[action.name]
    if action.duration_minutes < low or action.duration_minutes > high:
        raise ValueError(f"Action {action.name} duration must be between {low} and {high} minutes")
    location = get_field(conn, actor_id, "runtime.location", MASTER_SUITE)
    if action.name == "move":
        if not action.target:
            raise ValueError("move requires a target room")
        if not _connected(conn, location, action.target):
            raise ValueError(f"Room {action.target} is not reachable from {location}")
        return
    if action.name == "idle":
        if action.target:
            raise ValueError("idle must not specify a target")
        return
    if action.name == "rest" and action.target is None:
        return
    capability = ACTION_CAPABILITY[action.name]
    if not action.target:
        raise ValueError(f"Action {action.name} requires a target object")
    row = conn.execute(
        """SELECT e.capabilities_json FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='contains' AND e.id=? AND e.entity_type='object'""",
        (location, action.target),
    ).fetchone()
    if row is None:
        raise ValueError(f"Target {action.target} is not a local object in {location}")
    if capability not in json.loads(row[0]):
        raise ValueError(f"Target {action.target} does not support {action.name}")
    if action.name in {"eat", "drink", "shower"} and action.name not in _object_effects(conn, action.target):
        raise ValueError(f"Target {action.target} has no authored {action.name} physiological effect")


def _apply_effect_spec(values: dict[str, float], effects: dict[str, Any]) -> None:
    for field_key, spec in effects.items():
        stat = PHYSIOLOGY_FIELDS.get(field_key)
        if stat is None:
            continue
        if isinstance(spec, (int, float)):
            values[stat] += float(spec)
        elif isinstance(spec, dict) and "set" in spec:
            values[stat] = float(spec["set"])


def _advance_needs(conn: sqlite3.Connection, actor_id: str, action: Action) -> None:
    hours = action.duration_minutes / 60.0
    values = {
        "energy": float(get_field(conn, actor_id, "needs.energy", 75.0)),
        "hunger": float(get_field(conn, actor_id, "needs.hunger", 20.0)),
        "thirst": float(get_field(conn, actor_id, "needs.thirst", 15.0)),
        "sleepiness": float(get_field(conn, actor_id, "needs.sleepiness", 15.0)),
        "cleanliness": float(get_field(conn, actor_id, "physiology.cleanliness", 80.0)),
    }
    for stat, rate in PASSIVE_DRIFT_PER_HOUR.items():
        values[stat] += rate * hours
    for stat, rate in ACTION_EFFECTS_PER_HOUR.get(action.name, {}).items():
        values[stat] += rate * hours
    if action.target:
        target_effects = _object_effects(conn, action.target).get(action.name, {})
        if isinstance(target_effects, dict):
            _apply_effect_spec(values, target_effects)
    set_field(conn, actor_id, "needs.energy", _clamp(values["energy"]))
    set_field(conn, actor_id, "needs.hunger", _clamp(values["hunger"]))
    set_field(conn, actor_id, "needs.thirst", _clamp(values["thirst"]))
    set_field(conn, actor_id, "needs.sleepiness", _clamp(values["sleepiness"]))
    set_field(conn, actor_id, "physiology.cleanliness", _clamp(values["cleanliness"]))


def apply_action(conn: sqlite3.Connection, action: Action, actor_id: str = "char_darian", *, action_id: str | None = None) -> dict[str, Any]:
    if action_id:
        rows = conn.execute("SELECT payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 50").fetchall()
        if any(json.loads(row[0]).get("action_id") == action_id for row in rows):
            return snapshot(conn, actor_id)
    validate_action(conn, actor_id, action)
    before = snapshot(conn, actor_id)
    started = datetime.fromisoformat(before["sim_time"])
    set_field(conn, actor_id, "runtime.current_action", action.name)
    if action.name == "move" and action.target:
        set_field(conn, actor_id, "runtime.location", action.target)
    _advance_needs(conn, actor_id, action)
    ended = started + timedelta(minutes=action.duration_minutes)
    set_runtime_value(conn, "sim_time", ended.isoformat())
    set_field(conn, actor_id, "runtime.current_action", "idle")
    after = snapshot(conn, actor_id)
    conn.execute(
        "INSERT INTO events(sim_time, actor_id, event_type, payload_json) VALUES (?, ?, 'action_completed', ?)",
        (ended.isoformat(), actor_id, json.dumps({"action_id": action_id, "action": action.name, "target": action.target, "duration_minutes": action.duration_minutes, "reason": action.reason, "before": before, "after": after}, ensure_ascii=False)),
    )
    conn.commit()
    return after


def _move_toward(conn: sqlite3.Connection, location: str, destination: str, reason: str) -> Action:
    if location == destination:
        raise ValueError("move_toward called while already at destination")
    queue: deque[tuple[str, str | None]] = deque([(location, None)])
    seen = {location}
    while queue:
        node, first_hop = queue.popleft()
        for neighbor in reachable_rooms(conn, node):
            target = neighbor["id"]
            if target in seen:
                continue
            hop = target if first_hop is None else first_hop
            if target == destination:
                return Action("move", 5, hop, reason)
            seen.add(target)
            queue.append((target, hop))
    raise ValueError(f"No authored route from {location} to {destination}")


class BaselineLivingPolicy:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def choose(self, state: dict[str, Any], available_actions: list[str]) -> Action:
        location = state["location"]
        if state["sleepiness"] >= 72:
            return Action("sleep", 480, MASTER_BED, "recover from high sleep pressure") if location == MASTER_SUITE else _move_toward(self.conn, location, MASTER_SUITE, "go to bed")
        if state["energy"] <= 28:
            return Action("rest", 60, None, "recover low energy")
        if state["thirst"] >= 55:
            return Action("drink", 5, DRINKING_WATER, "respond to thirst") if location == KITCHEN else _move_toward(self.conn, location, KITCHEN, "get water")
        if state["hunger"] >= 60:
            return Action("eat", 25, MEAL_INGREDIENTS, "respond to hunger") if location == KITCHEN else _move_toward(self.conn, location, KITCHEN, "get food")
        if state["cleanliness"] <= 45:
            return Action("shower", 15, MASTER_SHOWER, "restore cleanliness") if location == MASTER_BATHROOM else _move_toward(self.conn, location, MASTER_BATHROOM, "take a shower")
        hour = datetime.fromisoformat(state["sim_time"]).hour
        if 8 <= hour < 11 and state["energy"] >= 50:
            return Action("train", 60, FREE_WEIGHTS, "morning training block") if location == HOME_GYM else _move_toward(self.conn, location, HOME_GYM, "start morning training")
        if 19 <= hour < 22:
            return Action("read", 45, LIBRARY_BOOKSHELF, "evening wind-down") if location == LIBRARY else _move_toward(self.conn, location, LIBRARY, "wind down with reading")
        if location == LIVING_ROOM:
            return Action("rest", 30, LIVING_SOFA, "unstructured recovery time")
        return _move_toward(self.conn, location, LIVING_ROOM, "return to common area")


def run_until(conn: sqlite3.Connection, end_time: datetime, *, decision_provider: DecisionProvider | None = None, actor_id: str = "char_darian", max_actions: int = 200) -> list[dict[str, Any]]:
    provider = decision_provider or BaselineLivingPolicy(conn)
    trace: list[dict[str, Any]] = []
    for _ in range(max_actions):
        state = snapshot(conn, actor_id)
        now = datetime.fromisoformat(state["sim_time"])
        if now >= end_time:
            break
        action = provider.choose(state, ACTION_NAMES)
        remaining = max(1, int((end_time - now).total_seconds() // 60))
        if action.duration_minutes > remaining:
            low, _ = ACTION_DURATION_BOUNDS[action.name]
            action = Action("idle", min(remaining, ACTION_DURATION_BOUNDS["idle"][1]), None, "finish bounded simulation window") if remaining < low else Action(action.name, remaining, action.target, action.reason)
        trace.append(apply_action(conn, action, actor_id))
    else:
        raise RuntimeError("P1 autonomous loop exceeded max_actions before reaching target time")
    return trace


def run_one_simulated_day(conn: sqlite3.Connection, actor_id: str = "char_darian") -> list[dict[str, Any]]:
    start = ensure_sim_clock(conn)
    return run_until(conn, start + timedelta(hours=24), actor_id=actor_id)

from __future__ import annotations

import json
import sqlite3
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

NEXT_HOP = {
    ("room_bedroom", "room_bathroom"): "room_bathroom", ("room_bedroom", "room_living"): "room_living",
    ("room_bedroom", "room_kitchen"): "room_bathroom", ("room_bedroom", "room_gym"): "room_living",
    ("room_bathroom", "room_bedroom"): "room_bedroom", ("room_bathroom", "room_living"): "room_bedroom",
    ("room_bathroom", "room_kitchen"): "room_kitchen", ("room_bathroom", "room_gym"): "room_bedroom",
    ("room_living", "room_bedroom"): "room_bedroom", ("room_living", "room_bathroom"): "room_bedroom",
    ("room_living", "room_kitchen"): "room_kitchen", ("room_living", "room_gym"): "room_gym",
    ("room_kitchen", "room_bedroom"): "room_bathroom", ("room_kitchen", "room_bathroom"): "room_bathroom",
    ("room_kitchen", "room_living"): "room_living", ("room_kitchen", "room_gym"): "room_living",
    ("room_gym", "room_bedroom"): "room_living", ("room_gym", "room_bathroom"): "room_living",
    ("room_gym", "room_kitchen"): "room_living", ("room_gym", "room_living"): "room_living",
}


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
    location = get_field(conn, actor_id, "runtime.location", "room_bedroom")
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


def local_objects(conn: sqlite3.Connection, room_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """SELECT e.id, e.name, e.capabilities_json FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='contains' AND e.entity_type='object' ORDER BY e.id""",
        (room_id,),
    ).fetchall()
    return [{"id": row["id"], "name": row["name"], "capabilities": json.loads(row["capabilities_json"])} for row in rows]


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
                options.append({"action": action, "target": obj["id"], "target_name": obj["name"], "duration": ACTION_DURATION_BOUNDS[action]})
    options.append({"action": "rest", "target": None, "target_name": None, "duration": ACTION_DURATION_BOUNDS["rest"]})
    options.append({"action": "idle", "target": None, "target_name": None, "duration": ACTION_DURATION_BOUNDS["idle"]})
    return options


def validate_action(conn: sqlite3.Connection, actor_id: str, action: Action) -> None:
    if action.name not in ACTION_NAMES:
        raise ValueError(f"Unknown action: {action.name}")
    low, high = ACTION_DURATION_BOUNDS[action.name]
    if action.duration_minutes < low or action.duration_minutes > high:
        raise ValueError(f"Action {action.name} duration must be between {low} and {high} minutes")
    location = get_field(conn, actor_id, "runtime.location", "room_bedroom")
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


def _advance_needs(conn: sqlite3.Connection, actor_id: str, action: Action) -> None:
    hours = action.duration_minutes / 60.0
    energy = float(get_field(conn, actor_id, "needs.energy", 75.0))
    hunger = float(get_field(conn, actor_id, "needs.hunger", 20.0))
    thirst = float(get_field(conn, actor_id, "needs.thirst", 15.0))
    sleepiness = float(get_field(conn, actor_id, "needs.sleepiness", 15.0))
    cleanliness = float(get_field(conn, actor_id, "physiology.cleanliness", 80.0))

    energy -= 3.0 * hours
    hunger += 4.0 * hours
    thirst += 5.0 * hours
    sleepiness += 3.5 * hours
    cleanliness -= 1.2 * hours

    if action.name == "sleep":
        energy += 15.0 * hours
        sleepiness -= 16.0 * hours
        hunger += 1.0 * hours
        thirst += 1.5 * hours
    elif action.name == "eat":
        hunger -= 40.0
        energy += 4.0
    elif action.name == "drink":
        thirst -= 45.0
    elif action.name == "shower":
        cleanliness = 100.0
    elif action.name == "rest":
        energy += 12.0 * hours
        sleepiness -= 6.0 * hours
    elif action.name == "train":
        energy -= 12.0 * hours
        hunger += 7.0 * hours
        thirst += 10.0 * hours
        cleanliness -= 10.0 * hours
    elif action.name == "read":
        energy -= 1.0 * hours
    elif action.name == "idle":
        energy += 4.0 * hours

    set_field(conn, actor_id, "needs.energy", _clamp(energy))
    set_field(conn, actor_id, "needs.hunger", _clamp(hunger))
    set_field(conn, actor_id, "needs.thirst", _clamp(thirst))
    set_field(conn, actor_id, "needs.sleepiness", _clamp(sleepiness))
    set_field(conn, actor_id, "physiology.cleanliness", _clamp(cleanliness))


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


def _move_toward(location: str, destination: str, reason: str) -> Action:
    if location == destination:
        raise ValueError("move_toward called while already at destination")
    target = NEXT_HOP.get((location, destination))
    if target is None:
        raise ValueError(f"No authored Home v1 route from {location} to {destination}")
    return Action("move", 5, target, reason)


class BaselineLivingPolicy:
    def choose(self, state: dict[str, Any], available_actions: list[str]) -> Action:
        location = state["location"]
        if state["sleepiness"] >= 72:
            return Action("sleep", 480, "obj_bed", "recover from high sleep pressure") if location == "room_bedroom" else _move_toward(location, "room_bedroom", "go to bed")
        if state["energy"] <= 28:
            return Action("rest", 60, None, "recover low energy")
        if state["thirst"] >= 55:
            return Action("drink", 5, "obj_water", "respond to thirst") if location == "room_kitchen" else _move_toward(location, "room_kitchen", "get water")
        if state["hunger"] >= 60:
            return Action("eat", 25, "obj_meal_stock", "respond to hunger") if location == "room_kitchen" else _move_toward(location, "room_kitchen", "get food")
        if state["cleanliness"] <= 45:
            return Action("shower", 15, "obj_shower", "restore cleanliness") if location == "room_bathroom" else _move_toward(location, "room_bathroom", "take a shower")
        hour = datetime.fromisoformat(state["sim_time"]).hour
        if 8 <= hour < 11 and state["energy"] >= 50:
            return Action("train", 60, "obj_weights", "morning training block") if location == "room_gym" else _move_toward(location, "room_gym", "start morning training")
        if 19 <= hour < 22:
            return Action("read", 45, "obj_bookshelf", "evening wind-down") if location == "room_living" else _move_toward(location, "room_living", "wind down in living room")
        if location == "room_living":
            return Action("rest", 30, "obj_sofa", "unstructured recovery time")
        return _move_toward(location, "room_living", "return to common area")


def run_until(conn: sqlite3.Connection, end_time: datetime, *, decision_provider: DecisionProvider | None = None, actor_id: str = "char_darian", max_actions: int = 200) -> list[dict[str, Any]]:
    provider = decision_provider or BaselineLivingPolicy()
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

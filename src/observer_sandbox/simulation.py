from __future__ import annotations

import json
import sqlite3
import uuid
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Protocol

from .event_log import record_event
from .training_modifiers import training_readiness_modifier
from .training_stimulus import training_stimulus_evidence
from .world import get_field, set_field


@dataclass(frozen=True)
class Action:
    name: str
    duration_minutes: int
    target: str | None = None
    reason: str | None = None
    participants: tuple[str, ...] = ()
    resources: tuple[str, ...] = ()
    conditions: dict[str, Any] = field(default_factory=dict)
    modifiers: dict[str, Any] = field(default_factory=dict)


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
    "needs.energy": "energy", "needs.hunger": "hunger", "needs.thirst": "thirst",
    "needs.sleepiness": "sleepiness", "physiology.cleanliness": "cleanliness",
    "physiology.fatigue": "fatigue",
}
PASSIVE_DRIFT_PER_HOUR = {
    "energy": -2.0, "hunger": 2.5, "thirst": 3.0, "sleepiness": 3.0,
    "cleanliness": -0.8, "fatigue": -1.5,
}
ACTION_EFFECTS_PER_HOUR: dict[str, dict[str, float]] = {
    "sleep": {"energy": 11.0, "sleepiness": -15.0, "hunger": 0.5, "thirst": 0.75, "fatigue": -10.0},
    "rest": {"energy": 10.0, "fatigue": -7.0},
    "train": {"energy": -10.0, "hunger": 4.0, "thirst": 6.0, "cleanliness": -6.0, "fatigue": 20.0},
    "read": {"energy": -0.5, "fatigue": -1.0},
    "idle": {"energy": 3.0, "fatigue": -2.0},
}

TRAINING_FATIGUE_LIMIT = 70.0
BASELINE_TRAINING_FATIGUE_LIMIT = 55.0

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
        """INSERT INTO runtime_state(key,value_json) VALUES(?,?)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=CURRENT_TIMESTAMP""",
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
        "actor_id": actor_id,
        "sim_time": ensure_sim_clock(conn).isoformat(),
        "location": location,
        "location_name": room[0] if room else location,
        "current_action": get_field(conn, actor_id, "runtime.current_action", "idle"),
        "energy": float(get_field(conn, actor_id, "needs.energy", 75.0)),
        "hunger": float(get_field(conn, actor_id, "needs.hunger", 20.0)),
        "thirst": float(get_field(conn, actor_id, "needs.thirst", 15.0)),
        "sleepiness": float(get_field(conn, actor_id, "needs.sleepiness", 15.0)),
        "cleanliness": float(get_field(conn, actor_id, "physiology.cleanliness", 80.0)),
        "fatigue": float(get_field(conn, actor_id, "physiology.fatigue", 0.0)),
    }


def action_definition(conn: sqlite3.Connection, action_type: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM action_definitions WHERE action_type=?", (action_type,)).fetchone()
    if row is None:
        raise ValueError(f"Unknown action: {action_type}")
    return {
        "action_type": row["action_type"],
        "label": row["label"],
        "min_duration_minutes": int(row["min_duration_minutes"]),
        "max_duration_minutes": int(row["max_duration_minutes"]),
        "target_mode": row["target_mode"],
        "required_capability": row["required_capability"],
        "requires_colocation": bool(row["requires_colocation"]),
        "base_effects": json.loads(row["base_effects_json"] or "{}"),
        "conditions": json.loads(row["conditions_json"] or "{}"),
        "modifiers": json.loads(row["modifiers_json"] or "{}"),
    }


def _connected(conn: sqlite3.Connection, left: str, right: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM relations WHERE source_id=? AND relation_type='connected_to' AND target_id=?",
        (left, right),
    ).fetchone() is not None


def _object_effects(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    value = get_field(conn, object_id, "game.effects", {})
    return value if isinstance(value, dict) else {}


def local_objects(conn: sqlite3.Connection, room_id: str) -> list[dict[str, Any]]:
    rows = conn.execute(
        """SELECT e.id,e.name,e.capabilities_json,e.definition_id
        FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='contains' AND e.entity_type='object'
        ORDER BY e.id""",
        (room_id,),
    ).fetchall()
    return [
        {
            "id": row["id"],
            "name": row["name"],
            "definition_id": row["definition_id"],
            "capabilities": json.loads(row["capabilities_json"]),
            "effects": _object_effects(conn, row["id"]),
        }
        for row in rows
    ]


def reachable_rooms(conn: sqlite3.Connection, room_id: str) -> list[dict[str, str]]:
    rows = conn.execute(
        """SELECT e.id,e.name
        FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='connected_to' AND e.entity_type='location'
        ORDER BY e.id""",
        (room_id,),
    ).fetchall()
    return [{"id": row["id"], "name": row["name"]} for row in rows]


def action_options(conn: sqlite3.Connection, actor_id: str = "char_darian") -> list[dict[str, Any]]:
    state = snapshot(conn, actor_id)
    room_id = state["location"]
    options: list[dict[str, Any]] = []
    move_def = action_definition(conn, "move")
    move_duration = (move_def["min_duration_minutes"], move_def["max_duration_minutes"])
    for room in reachable_rooms(conn, room_id):
        options.append({"action": "move", "target": room["id"], "target_name": room["name"], "duration": move_duration})

    definitions = {
        row["action_type"]: action_definition(conn, row["action_type"])
        for row in conn.execute("SELECT action_type FROM action_definitions")
    }
    for obj in local_objects(conn, room_id):
        for name, definition in definitions.items():
            if name == "train" and state["fatigue"] >= TRAINING_FATIGUE_LIMIT:
                continue
            capability = definition["required_capability"]
            if capability and capability in obj["capabilities"]:
                option = {
                    "action": name,
                    "target": obj["id"],
                    "target_name": obj["name"],
                    "duration": (definition["min_duration_minutes"], definition["max_duration_minutes"]),
                }
                effects = obj["effects"].get(name)
                if effects:
                    option["effects"] = effects
                if name in ACTION_EFFECTS_PER_HOUR:
                    option["effects_per_hour"] = ACTION_EFFECTS_PER_HOUR[name]
                if name == "train":
                    option["modifiers"] = {"training_readiness": training_readiness_modifier(state)}
                options.append(option)

    for name in ("rest", "idle"):
        definition = definitions[name]
        option = {
            "action": name,
            "target": None,
            "target_name": None,
            "duration": (definition["min_duration_minutes"], definition["max_duration_minutes"]),
        }
        if name in ACTION_EFFECTS_PER_HOUR:
            option["effects_per_hour"] = ACTION_EFFECTS_PER_HOUR[name]
        options.append(option)
    return options


def validate_action(conn: sqlite3.Connection, actor_id: str, action: Action) -> None:
    definition = action_definition(conn, action.name)
    low, high = definition["min_duration_minutes"], definition["max_duration_minutes"]
    if not low <= action.duration_minutes <= high:
        raise ValueError(f"Action {action.name} duration must be between {low} and {high} minutes")
    if action.name == "train" and snapshot(conn, actor_id)["fatigue"] >= TRAINING_FATIGUE_LIMIT:
        raise ValueError("Training is unavailable while systemic fatigue is too high")

    location = get_field(conn, actor_id, "runtime.location", MASTER_SUITE)
    target_mode = definition["target_mode"]
    if target_mode == "location":
        if not action.target or not _connected(conn, location, action.target):
            raise ValueError(f"Location target {action.target} is not reachable from {location}")
        return
    if target_mode == "none":
        if action.target:
            raise ValueError(f"{action.name} must not specify a target")
        return
    if action.name == "rest" and action.target is None:
        return
    if target_mode == "object" and not action.target:
        raise ValueError(f"Action {action.name} requires a target object")
    if not action.target:
        return

    row = conn.execute(
        """SELECT e.capabilities_json
        FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='contains' AND e.id=? AND e.entity_type='object'""",
        (location, action.target),
    ).fetchone()
    if row is None:
        raise ValueError(f"Target {action.target} is not a local object in {location}")
    capability = definition["required_capability"]
    if capability and capability not in json.loads(row[0]):
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
        elif isinstance(spec, dict):
            if "add" in spec:
                values[stat] += float(spec["add"])
            if "multiply" in spec:
                values[stat] *= float(spec["multiply"])
            if "set" in spec:
                values[stat] = float(spec["set"])
            if "clamp_min" in spec:
                values[stat] = max(values[stat], float(spec["clamp_min"]))
            if "clamp_max" in spec:
                values[stat] = min(values[stat], float(spec["clamp_max"]))


def _training_load_evidence(action: Action) -> dict[str, Any] | None:
    if action.name != "train":
        return None
    modifier = action.modifiers.get("training_readiness")
    if not isinstance(modifier, dict):
        return None
    effectiveness = max(0.0, min(1.0, float(modifier.get("effectiveness", modifier.get("readiness", 1.0)))))
    return {
        "planned_minutes": int(action.duration_minutes),
        "effectiveness": round(effectiveness, 3),
        "effective_minutes": round(float(action.duration_minutes) * effectiveness, 3),
        "source": "p3.5-effective-training-load-v1",
    }


def _advance_needs(conn: sqlite3.Connection, actor_id: str, action: Action) -> None:
    hours = action.duration_minutes / 60.0
    values = {
        "energy": float(get_field(conn, actor_id, "needs.energy", 75.0)),
        "hunger": float(get_field(conn, actor_id, "needs.hunger", 20.0)),
        "thirst": float(get_field(conn, actor_id, "needs.thirst", 15.0)),
        "sleepiness": float(get_field(conn, actor_id, "needs.sleepiness", 15.0)),
        "cleanliness": float(get_field(conn, actor_id, "physiology.cleanliness", 80.0)),
        "fatigue": float(get_field(conn, actor_id, "physiology.fatigue", 0.0)),
    }
    for stat, rate in PASSIVE_DRIFT_PER_HOUR.items():
        values[stat] += rate * hours
    readiness = action.modifiers.get("training_readiness") if action.name == "train" else None
    fatigue_multiplier = float(readiness.get("fatigue_cost_multiplier", 1.0)) if isinstance(readiness, dict) else 1.0
    effectiveness = (
        max(0.0, min(1.0, float(readiness.get("effectiveness", readiness.get("readiness", 1.0)))))
        if isinstance(readiness, dict)
        else 1.0
    )
    for stat, rate in ACTION_EFFECTS_PER_HOUR.get(action.name, {}).items():
        effective_rate = rate
        if action.name == "train":
            if stat == "fatigue":
                effective_rate = rate * fatigue_multiplier
            else:
                effective_rate = rate * effectiveness
        values[stat] += effective_rate * hours
    if action.target:
        effects = _object_effects(conn, action.target).get(action.name, {})
        if isinstance(effects, dict):
            _apply_effect_spec(values, effects)

    set_field(conn, actor_id, "needs.energy", _clamp(values["energy"]))
    set_field(conn, actor_id, "needs.hunger", _clamp(values["hunger"]))
    set_field(conn, actor_id, "needs.thirst", _clamp(values["thirst"]))
    set_field(conn, actor_id, "needs.sleepiness", _clamp(values["sleepiness"]))
    set_field(conn, actor_id, "physiology.cleanliness", _clamp(values["cleanliness"]))
    set_field(
        conn,
        actor_id,
        "physiology.fatigue",
        _clamp(values["fatigue"]),
        authority="physiology_engine",
        source="p3-training-recovery-v1",
    )


def _state_changes(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key in ("location", "energy", "hunger", "thirst", "sleepiness", "cleanliness", "fatigue"):
        if before.get(key) != after.get(key):
            result[key] = {"before": before.get(key), "after": after.get(key)}
    return result


def ensure_action_instance(
    conn: sqlite3.Connection,
    action: Action,
    actor_id: str,
    *,
    action_id: str | None = None,
    status: str = "in_progress",
    planned_wall_time: float | None = None,
    due_wall_time: float | None = None,
    speed_at_plan: float | None = None,
) -> str:
    action_id = action_id or str(uuid.uuid4())
    before = snapshot(conn, actor_id)
    modifiers = dict(action.modifiers)
    if action.name == "train" and "training_readiness" not in modifiers:
        modifiers["training_readiness"] = training_readiness_modifier(before)
    conn.execute(
        """INSERT OR IGNORE INTO action_instances(
        id,action_type,actor_id,place_id,target_id,status,duration_minutes,intent,participants_json,resources_json,
        conditions_json,modifiers_json,planned_sim_time,started_sim_time,planned_wall_time,due_wall_time,speed_at_plan
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            action_id, action.name, actor_id, before["location"], action.target, status, action.duration_minutes,
            action.reason, json.dumps(list(action.participants)), json.dumps(list(action.resources)),
            json.dumps(action.conditions), json.dumps(modifiers), before["sim_time"],
            before["sim_time"] if status == "in_progress" else None, planned_wall_time, due_wall_time, speed_at_plan,
        ),
    )
    for participant in action.participants:
        conn.execute(
            "INSERT OR IGNORE INTO action_participants(action_id,entity_id,role) VALUES(?,?,?)",
            (action_id, participant, "participant"),
        )
    return action_id


def apply_action(
    conn: sqlite3.Connection,
    action: Action,
    actor_id: str = "char_darian",
    *,
    action_id: str | None = None,
) -> dict[str, Any]:
    if action_id and conn.execute(
        "SELECT 1 FROM action_instances WHERE id=? AND status='completed'", (action_id,)
    ).fetchone():
        return snapshot(conn, actor_id)

    validate_action(conn, actor_id, action)
    action_id = ensure_action_instance(conn, action, actor_id, action_id=action_id)
    instance = conn.execute(
        "SELECT planned_sim_time,modifiers_json FROM action_instances WHERE id=?",
        (action_id,),
    ).fetchone()
    persisted_modifiers = json.loads(instance["modifiers_json"] or "{}") if instance else dict(action.modifiers)
    if persisted_modifiers != action.modifiers:
        action = Action(
            action.name, action.duration_minutes, action.target, action.reason, action.participants,
            action.resources, action.conditions, persisted_modifiers,
        )
    current_clock = ensure_sim_clock(conn)
    started = datetime.fromisoformat(instance["planned_sim_time"]) if instance and instance["planned_sim_time"] else current_clock
    ended = started + timedelta(minutes=action.duration_minutes)

    before = snapshot(conn, actor_id)
    before["sim_time"] = started.isoformat()
    set_field(conn, actor_id, "runtime.current_action", action.name)
    if action.name == "move" and action.target:
        set_field(conn, actor_id, "runtime.location", action.target)
    _advance_needs(conn, actor_id, action)

    universe_clock = max(current_clock, ended)
    set_runtime_value(conn, "sim_time", universe_clock.isoformat())
    set_field(conn, actor_id, "runtime.current_action", "idle")
    after = snapshot(conn, actor_id)
    changes = _state_changes(before, after)
    training_load = _training_load_evidence(action)
    training_stimulus = training_stimulus_evidence(
        action_name=action.name, target=action.target, training_load=training_load
    )
    outcome: dict[str, Any] = {"state_changes": changes, "modifiers": action.modifiers}
    if training_load is not None:
        outcome["training_load"] = training_load
    if training_stimulus is not None:
        outcome["training_stimulus"] = training_stimulus

    conn.execute(
        """UPDATE action_instances
        SET status='completed',started_sim_time=COALESCE(started_sim_time,?),ended_sim_time=?,outcome_json=?,updated_at=CURRENT_TIMESTAMP
        WHERE id=?""",
        (
            started.isoformat(), ended.isoformat(),
            json.dumps(outcome, ensure_ascii=False), action_id,
        ),
    )
    participants = [{"entity_id": participant, "role": "participant"} for participant in action.participants]
    payload: dict[str, Any] = {
        "action_id": action_id,
        "action": action.name,
        "target": action.target,
        "duration_minutes": action.duration_minutes,
        "reason": action.reason,
        "modifiers": action.modifiers,
        "before": before,
        "after": after,
        "action_started_sim_time": started.isoformat(),
        "action_ended_sim_time": ended.isoformat(),
    }
    if training_load is not None:
        payload["training_load"] = training_load
    if training_stimulus is not None:
        payload["training_stimulus"] = training_stimulus
    record_event(
        conn,
        sim_time=ended.isoformat(),
        actor_id=actor_id,
        event_type="action_completed",
        action_id=action_id,
        location_id=after["location"],
        participants=participants,
        state_changes=changes,
        payload=payload,
    )
    conn.commit()
    return after


def _move_toward(conn: sqlite3.Connection, location: str, destination: str, reason: str) -> Action:
    if location == destination:
        raise ValueError("move_toward called while already at destination")
    queue: deque[tuple[str, str | None]] = deque([(location, None)])
    seen = {location}
    while queue:
        node, first = queue.popleft()
        for neighbor in reachable_rooms(conn, node):
            target = neighbor["id"]
            if target in seen:
                continue
            hop = target if first is None else first
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
        if state["fatigue"] >= 65:
            return Action("rest", 60, None, "recover from accumulated training fatigue")
        if state["energy"] <= 28:
            return Action("rest", 60, None, "recover low energy")
        if state["thirst"] >= 55:
            return Action("drink", 5, DRINKING_WATER, "respond to thirst") if location == KITCHEN else _move_toward(self.conn, location, KITCHEN, "get water")
        if state["hunger"] >= 60:
            return Action("eat", 25, MEAL_INGREDIENTS, "respond to hunger") if location == KITCHEN else _move_toward(self.conn, location, KITCHEN, "get food")
        if state["cleanliness"] <= 45:
            return Action("shower", 15, MASTER_SHOWER, "restore cleanliness") if location == MASTER_BATHROOM else _move_toward(self.conn, location, MASTER_BATHROOM, "take a shower")
        hour = datetime.fromisoformat(state["sim_time"]).hour
        if 8 <= hour < 11 and state["energy"] >= 50 and state["fatigue"] < BASELINE_TRAINING_FATIGUE_LIMIT:
            return Action("train", 60, FREE_WEIGHTS, "morning training block") if location == HOME_GYM else _move_toward(self.conn, location, HOME_GYM, "start morning training")
        if 19 <= hour < 22:
            return Action("read", 45, LIBRARY_BOOKSHELF, "evening wind-down") if location == LIBRARY else _move_toward(self.conn, location, LIBRARY, "wind down with reading")
        if location == LIVING_ROOM:
            return Action("rest", 30, LIVING_SOFA, "unstructured recovery time")
        return _move_toward(self.conn, location, LIVING_ROOM, "return to common area")


def run_until(
    conn: sqlite3.Connection,
    end_time: datetime,
    *,
    decision_provider: DecisionProvider | None = None,
    actor_id: str = "char_darian",
    max_actions: int = 200,
) -> list[dict[str, Any]]:
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
            definition = action_definition(conn, action.name)
            low = definition["min_duration_minutes"]
            idle_def = action_definition(conn, "idle")
            if remaining < low:
                action = Action("idle", min(remaining, idle_def["max_duration_minutes"]), None, "finish bounded simulation window")
            else:
                action = Action(
                    action.name, remaining, action.target, action.reason, action.participants,
                    action.resources, action.conditions, action.modifiers,
                )
        trace.append(apply_action(conn, action, actor_id))
    else:
        raise RuntimeError("P1 autonomous loop exceeded max_actions before reaching target time")
    return trace


def run_one_simulated_day(conn: sqlite3.Connection, actor_id: str = "char_darian") -> list[dict[str, Any]]:
    start = ensure_sim_clock(conn)
    return run_until(conn, start + timedelta(hours=24), actor_id=actor_id)

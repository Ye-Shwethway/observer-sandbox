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


ACTION_NAMES = [
    "move",
    "sleep",
    "eat",
    "drink",
    "shower",
    "rest",
    "inspect",
    "use",
    "train",
    "read",
    "idle",
]


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, round(value, 3)))


def _runtime_value(conn: sqlite3.Connection, key: str, default: Any) -> Any:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (key,)).fetchone()
    return default if row is None else json.loads(row[0])


def _set_runtime_value(conn: sqlite3.Connection, key: str, value: Any) -> None:
    conn.execute(
        """
        INSERT INTO runtime_state(key, value_json) VALUES (?, ?)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json, updated_at=CURRENT_TIMESTAMP
        """,
        (key, json.dumps(value)),
    )


def ensure_sim_clock(conn: sqlite3.Connection) -> datetime:
    raw = _runtime_value(conn, "sim_time", None)
    if raw is None:
        start = datetime(2025, 5, 1, 7, 0, tzinfo=timezone.utc)
        _set_runtime_value(conn, "sim_time", start.isoformat())
        conn.commit()
        return start
    return datetime.fromisoformat(raw)


def snapshot(conn: sqlite3.Connection, actor_id: str = "char_darian") -> dict[str, Any]:
    location = get_field(conn, actor_id, "runtime.location", "room_bedroom")
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
    }


def _connected(conn: sqlite3.Connection, left: str, right: str) -> bool:
    return conn.execute(
        "SELECT 1 FROM relations WHERE source_id=? AND relation_type='connected_to' AND target_id=?",
        (left, right),
    ).fetchone() is not None


def _room_has_capability(conn: sqlite3.Connection, room_id: str, capability: str) -> bool:
    rows = conn.execute(
        """
        SELECT e.capabilities_json
        FROM relations r JOIN entities e ON e.id=r.target_id
        WHERE r.source_id=? AND r.relation_type='contains'
        """,
        (room_id,),
    ).fetchall()
    return any(capability in json.loads(row[0]) for row in rows)


def validate_action(conn: sqlite3.Connection, actor_id: str, action: Action) -> None:
    if action.name not in ACTION_NAMES:
        raise ValueError(f"Unknown action: {action.name}")
    if action.duration_minutes <= 0 or action.duration_minutes > 720:
        raise ValueError("Action duration must be between 1 and 720 minutes")

    location = get_field(conn, actor_id, "runtime.location", "room_bedroom")
    if action.name == "move":
        if not action.target:
            raise ValueError("move requires a target room")
        if not _connected(conn, location, action.target):
            raise ValueError(f"Room {action.target} is not reachable from {location}")
        return

    capability = {
        "sleep": "sleep",
        "eat": "eat",
        "drink": "drink",
        "shower": "shower",
        "rest": "rest",
        "inspect": "inspect",
        "use": "use",
        "train": "train",
        "read": "read",
    }.get(action.name)
    if capability and not _room_has_capability(conn, location, capability):
        raise ValueError(f"Action {action.name} is not available in {location}")


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
        energy += 10.0 * hours
        sleepiness -= 15.0 * hours
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
        energy += 6.0 * hours
        sleepiness -= 2.0 * hours
    elif action.name == "train":
        energy -= 12.0 * hours
        hunger += 7.0 * hours
        thirst += 10.0 * hours
        cleanliness -= 10.0 * hours
    elif action.name == "read":
        energy -= 1.0 * hours
    elif action.name == "idle":
        energy += 1.0 * hours

    set_field(conn, actor_id, "needs.energy", _clamp(energy))
    set_field(conn, actor_id, "needs.hunger", _clamp(hunger))
    set_field(conn, actor_id, "needs.thirst", _clamp(thirst))
    set_field(conn, actor_id, "needs.sleepiness", _clamp(sleepiness))
    set_field(conn, actor_id, "physiology.cleanliness", _clamp(cleanliness))


def apply_action(conn: sqlite3.Connection, action: Action, actor_id: str = "char_darian") -> dict[str, Any]:
    validate_action(conn, actor_id, action)
    before = snapshot(conn, actor_id)
    started = datetime.fromisoformat(before["sim_time"])

    set_field(conn, actor_id, "runtime.current_action", action.name)
    if action.name == "move" and action.target:
        set_field(conn, actor_id, "runtime.location", action.target)

    _advance_needs(conn, actor_id, action)
    ended = started + timedelta(minutes=action.duration_minutes)
    _set_runtime_value(conn, "sim_time", ended.isoformat())
    set_field(conn, actor_id, "runtime.current_action", "idle")

    after = snapshot(conn, actor_id)
    conn.execute(
        """
        INSERT INTO events(sim_time, actor_id, event_type, payload_json)
        VALUES (?, ?, 'action_completed', ?)
        """,
        (
            ended.isoformat(),
            actor_id,
            json.dumps(
                {
                    "action": action.name,
                    "target": action.target,
                    "duration_minutes": action.duration_minutes,
                    "reason": action.reason,
                    "before": before,
                    "after": after,
                },
                ensure_ascii=False,
            ),
        ),
    )
    conn.commit()
    return after


class BaselineLivingPolicy:
    """Deterministic P1 acceptance policy behind the same boundary used by future LLM decisions."""

    def choose(self, state: dict[str, Any], available_actions: list[str]) -> Action:
        location = state["location"]
        if state["sleepiness"] >= 72 or state["energy"] <= 28:
            if location == "room_bedroom":
                return Action("sleep", 480, reason="recover from high sleep pressure")
            return Action("move", 5, "room_bedroom", "go to bed")
        if state["thirst"] >= 55:
            if location == "room_kitchen":
                return Action("drink", 5, reason="respond to thirst")
            return Action("move", 5, "room_kitchen", "get water")
        if state["hunger"] >= 60:
            if location == "room_kitchen":
                return Action("eat", 25, reason="respond to hunger")
            return Action("move", 5, "room_kitchen", "get food")
        if state["cleanliness"] <= 45:
            if location == "room_bathroom":
                return Action("shower", 15, reason="restore cleanliness")
            return Action("move", 5, "room_bathroom", "take a shower")

        hour = datetime.fromisoformat(state["sim_time"]).hour
        if 8 <= hour < 11 and state["energy"] >= 50:
            if location == "room_gym":
                return Action("train", 60, reason="morning training block")
            return Action("move", 5, "room_gym", "start morning training")
        if 19 <= hour < 22:
            if location == "room_living":
                return Action("read", 45, reason="evening wind-down")
            return Action("move", 5, "room_living", "wind down in living room")
        if location == "room_living":
            return Action("rest", 30, reason="unstructured recovery time")
        return Action("move", 5, "room_living", "return to common area")


def run_until(
    conn: sqlite3.Connection,
    end_time: datetime,
    *,
    decision_provider: DecisionProvider | None = None,
    actor_id: str = "char_darian",
    max_actions: int = 200,
) -> list[dict[str, Any]]:
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
            action = Action(action.name, remaining, action.target, action.reason)
        trace.append(apply_action(conn, action, actor_id))
    else:
        raise RuntimeError("P1 autonomous loop exceeded max_actions before reaching target time")
    return trace


def run_one_simulated_day(conn: sqlite3.Connection, actor_id: str = "char_darian") -> list[dict[str, Any]]:
    start = ensure_sim_clock(conn)
    return run_until(conn, start + timedelta(hours=24), actor_id=actor_id)

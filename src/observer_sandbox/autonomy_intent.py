from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime
from typing import Any

from .actor_runtime import pending_action
from .actor_selection import resolve_actor_id
from .autonomy import autonomy_tick as _core_autonomy_tick
from .model_decision import ModelDecisionProvider
from .simulation import Action, snapshot


SOURCE = "autonomy_intent_continuity_v1"
STATE_PREFIX = "autonomy_intent_v1:"
CONDITION_KEY = "autonomy_intent_transition"
MAX_INTENT_AGE_HOURS = 12.0
MAX_MOVEMENT_STEPS = 4
INTERRUPT_ACTIONS = {"sleep", "eat", "drink", "shower", "rest"}


def _state_key(actor_id: str) -> str:
    return f"{STATE_PREFIX}{actor_id}"


def _parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value)


def active_intent(conn: sqlite3.Connection, actor_id: str, *, as_of_sim_time: str | None = None) -> dict[str, Any] | None:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (_state_key(actor_id),)).fetchone()
    if row is None:
        return None
    value = json.loads(row[0])
    if not isinstance(value, dict) or value.get("status") != "active":
        return None
    if as_of_sim_time and value.get("created_sim_time"):
        age_hours = (_parse_time(as_of_sim_time) - _parse_time(str(value["created_sim_time"]))).total_seconds() / 3600.0
        if age_hours > MAX_INTENT_AGE_HOURS:
            return None
    return value


def intent_context(conn: sqlite3.Connection, actor_id: str, *, as_of_sim_time: str) -> dict[str, Any]:
    current = active_intent(conn, actor_id, as_of_sim_time=as_of_sim_time)
    if current is None:
        return {
            "active": False,
            "guidance": (
                "No ongoing cross-action intent is active. Purposeful movement may establish a short bounded intent that can guide the immediate follow-up action."
            ),
        }
    return {
        "active": True,
        "intent_id": current["intent_id"],
        "summary": current["summary"],
        "origin_location_id": current.get("origin_location_id"),
        "destination_location_id": current.get("destination_location_id"),
        "movement_steps": int(current.get("movement_steps", 0)),
        "interruptions": int(current.get("interruptions", 0)),
        "guidance": (
            "This is a bounded ongoing purpose, not an order. If it is still appropriate, prefer a legal action that advances or fulfills it. Physiological needs, safety, and authoritative action_options override it. An unrelated local action may naturally end the intent."
        ),
    }


def _normalize_summary(reason: str | None) -> str | None:
    text = " ".join(str(reason or "").split()).strip()
    if len(text) < 8:
        return None
    return text[:220]


def transition_for_action(
    current: dict[str, Any] | None,
    action: Action,
    *,
    actor_id: str,
    sim_time: str,
    origin_location_id: str,
) -> dict[str, Any]:
    if current is None:
        summary = _normalize_summary(action.reason)
        if action.name != "move" or not action.target or summary is None:
            return {"mode": "none", "source": SOURCE}
        return {
            "mode": "start",
            "source": SOURCE,
            "intent_id": str(uuid.uuid4()),
            "summary": summary,
            "actor_id": actor_id,
            "created_sim_time": sim_time,
            "origin_location_id": origin_location_id,
            "destination_location_id": action.target,
            "movement_steps": 1,
            "interruptions": 0,
        }

    if action.name == "move" and action.target:
        if int(current.get("movement_steps", 0)) >= MAX_MOVEMENT_STEPS:
            return {"mode": "abandon", "source": SOURCE, "intent_id": current["intent_id"], "reason": "movement_step_bound"}
        return {
            "mode": "continue",
            "source": SOURCE,
            "intent_id": current["intent_id"],
            "destination_location_id": action.target,
        }

    if action.name in INTERRUPT_ACTIONS:
        return {"mode": "interrupt", "source": SOURCE, "intent_id": current["intent_id"]}

    return {"mode": "finish_after_completion", "source": SOURCE, "intent_id": current["intent_id"]}


def _write_active(conn: sqlite3.Connection, actor_id: str, value: dict[str, Any]) -> None:
    conn.execute(
        """INSERT INTO runtime_state(key,value_json,updated_at) VALUES(?,?,CURRENT_TIMESTAMP)
        ON CONFLICT(key) DO UPDATE SET value_json=excluded.value_json,updated_at=CURRENT_TIMESTAMP""",
        (_state_key(actor_id), json.dumps(value, ensure_ascii=False, sort_keys=True)),
    )


def _clear(conn: sqlite3.Connection, actor_id: str) -> None:
    conn.execute("DELETE FROM runtime_state WHERE key=?", (_state_key(actor_id),))


def expire_stale_intent(conn: sqlite3.Connection, actor_id: str, *, as_of_sim_time: str) -> bool:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (_state_key(actor_id),)).fetchone()
    if row is None:
        return False
    value = json.loads(row[0])
    created = value.get("created_sim_time") if isinstance(value, dict) else None
    if not created:
        _clear(conn, actor_id)
        conn.commit()
        return True
    age_hours = (_parse_time(as_of_sim_time) - _parse_time(str(created))).total_seconds() / 3600.0
    if age_hours <= MAX_INTENT_AGE_HOURS:
        return False
    _clear(conn, actor_id)
    conn.commit()
    return True


def commit_planned_transition(conn: sqlite3.Connection, actor_id: str, transition: dict[str, Any] | None) -> None:
    if not isinstance(transition, dict):
        return
    mode = transition.get("mode")
    if mode == "start":
        value = dict(transition)
        value.pop("mode", None)
        value["status"] = "active"
        _write_active(conn, actor_id, value)
        conn.commit()
        return

    current = active_intent(conn, actor_id)
    if current is None or transition.get("intent_id") != current.get("intent_id"):
        return
    if mode == "continue":
        current = dict(current)
        current["movement_steps"] = int(current.get("movement_steps", 0)) + 1
        current["destination_location_id"] = transition.get("destination_location_id")
        _write_active(conn, actor_id, current)
        conn.commit()
    elif mode == "interrupt":
        current = dict(current)
        current["interruptions"] = int(current.get("interruptions", 0)) + 1
        _write_active(conn, actor_id, current)
        conn.commit()
    elif mode == "abandon":
        _clear(conn, actor_id)
        conn.commit()


def settle_completed_transition(conn: sqlite3.Connection, actor_id: str, transition: dict[str, Any] | None) -> None:
    if not isinstance(transition, dict) or transition.get("mode") != "finish_after_completion":
        return
    current = active_intent(conn, actor_id)
    if current is None or transition.get("intent_id") != current.get("intent_id"):
        return
    _clear(conn, actor_id)
    conn.commit()


class _IntentAwareProvider:
    def __init__(self, conn: sqlite3.Connection, actor_id: str, inner: Any) -> None:
        self.conn = conn
        self.actor_id = actor_id
        self.inner = inner

    def choose(self, state: dict[str, Any], available_actions: list[str]) -> Action:
        enriched = dict(state)
        current = active_intent(self.conn, self.actor_id, as_of_sim_time=str(state["sim_time"]))
        enriched["autonomy_intent"] = intent_context(
            self.conn,
            self.actor_id,
            as_of_sim_time=str(state["sim_time"]),
        )
        action = self.inner.choose(enriched, available_actions)
        transition = transition_for_action(
            current,
            action,
            actor_id=self.actor_id,
            sim_time=str(state["sim_time"]),
            origin_location_id=str(state["location"]),
        )
        conditions = dict(action.conditions)
        conditions[CONDITION_KEY] = transition
        return Action(
            action.name,
            action.duration_minutes,
            action.target,
            action.reason,
            tuple(action.participants),
            tuple(action.resources),
            conditions,
            dict(action.modifiers),
        )


def autonomy_tick(
    conn: sqlite3.Connection,
    *,
    actor_id: str | None = None,
    provider: Any | None = None,
    now_wall: float | None = None,
) -> dict[str, Any]:
    """Run one normal autonomy tick with a bounded cross-action purpose bridge.

    Core scheduling/validation remains authoritative in ``autonomy.autonomy_tick``.
    This wrapper only carries a short active purpose across action boundaries; it
    never invents actions, targets, resources, or state consequences.
    """
    actor_id = resolve_actor_id(conn, actor_id)
    pending_before = pending_action(conn, actor_id)
    if pending_before is None:
        state = snapshot(conn, actor_id)
        expire_stale_intent(conn, actor_id, as_of_sim_time=str(state["sim_time"]))
        inner = provider or ModelDecisionProvider(conn, character_id=actor_id)
        provider = _IntentAwareProvider(conn, actor_id, inner)

    result = _core_autonomy_tick(
        conn,
        actor_id=actor_id,
        provider=provider,
        now_wall=now_wall,
    )

    if result.get("state") == "planned":
        pending = result.get("pending") or pending_action(conn, actor_id)
        transition = (pending or {}).get("conditions", {}).get(CONDITION_KEY)
        commit_planned_transition(conn, actor_id, transition)
    elif result.get("state") in {"completed", "recovered_completed"} and pending_before:
        transition = pending_before.get("conditions", {}).get(CONDITION_KEY)
        settle_completed_transition(conn, actor_id, transition)

    return result

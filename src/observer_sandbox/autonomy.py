from __future__ import annotations

import json
import sqlite3
import time
import uuid
from typing import Any

from .actor_runtime import actor_runtime, pending_action, set_actor_runtime, set_retry
from .event_log import record_event
from .model_decision import ModelDecisionProvider
from .simulation import ACTION_NAMES, Action, apply_action, ensure_action_instance, runtime_value, set_runtime_value, snapshot, validate_action
from .world import set_field

# Legacy names remain exported for downstream import compatibility only. Their
# state is no longer stored as universe-global runtime_state keys.
LEASE_KEY = "autonomy_lease"
PENDING_KEY = "autonomy_pending_action"
RETRY_KEY = "autonomy_retry"
MODE_KEY = "autonomy_mode"
MIND_STATS_KEY = "cognition_wake_stats"
MIND_WAKE_REASON_KEY = "cognition_wake_reason"
NORMAL_MODE = "normal"
CANARY_MODE = "canary_once"


def _wall_now() -> float:
    return time.time()


def _event(conn: sqlite3.Connection, actor_id: str, event_type: str, payload: dict[str, Any], *, action_id: str | None = None) -> None:
    state = snapshot(conn, actor_id)
    record_event(
        conn,
        sim_time=state["sim_time"],
        actor_id=actor_id,
        event_type=event_type,
        action_id=action_id,
        location_id=state["location"],
        payload=payload,
    )
    conn.commit()


def _acquire_lease(conn: sqlite3.Connection, actor_id: str, *, now: float, ttl_seconds: float = 30.0) -> str | None:
    actor_runtime(conn, actor_id)
    owner = str(uuid.uuid4())
    conn.execute("BEGIN IMMEDIATE")
    row = conn.execute("SELECT lease_owner,lease_expires_at FROM actor_runtime WHERE actor_id=?", (actor_id,)).fetchone()
    if row and row["lease_owner"] and float(row["lease_expires_at"] or 0) > now:
        conn.rollback()
        return None
    conn.execute(
        "UPDATE actor_runtime SET lease_owner=?,lease_expires_at=?,updated_at=CURRENT_TIMESTAMP WHERE actor_id=?",
        (owner, now + ttl_seconds, actor_id),
    )
    conn.commit()
    return owner


def _release_lease(conn: sqlite3.Connection, actor_id: str, owner: str) -> None:
    conn.execute(
        "UPDATE actor_runtime SET lease_owner=NULL,lease_expires_at=NULL,updated_at=CURRENT_TIMESTAMP WHERE actor_id=? AND lease_owner=?",
        (actor_id, owner),
    )
    conn.commit()


def _action_from_pending(pending: dict[str, Any]) -> Action:
    return Action(
        pending["action"], int(pending["duration_minutes"]), pending.get("target"), pending.get("reason"),
        tuple(pending.get("participants") or ()), tuple(pending.get("resources") or ()),
        dict(pending.get("conditions") or {}), dict(pending.get("modifiers") or {}),
    )


def _completion_already_recorded(conn: sqlite3.Connection, action_id: str) -> bool:
    row = conn.execute("SELECT status FROM action_instances WHERE id=?", (action_id,)).fetchone()
    return bool(row and row["status"] == "completed")


def _retry_blocked(conn: sqlite3.Connection, actor_id: str, now: float) -> bool:
    retry = actor_runtime(conn, actor_id)["retry"]
    return bool(retry and retry.get("retry_after") is not None and float(retry["retry_after"]) > now)


def _record_failure(conn: sqlite3.Connection, actor_id: str, *, stage: str, error: Exception, now: float, action_id: str | None = None) -> None:
    previous = actor_runtime(conn, actor_id)["retry"] or {}
    failures = min(int(previous.get("failures", 0)) + 1, 8)
    delay = min(300.0, float(2 ** failures))
    set_retry(conn, actor_id, {"failures": failures, "retry_after": now + delay, "last_error": type(error).__name__})
    if action_id:
        conn.execute(
            "UPDATE action_instances SET status='failed',outcome_json=?,updated_at=CURRENT_TIMESTAMP WHERE id=?",
            (json.dumps({"stage": stage, "error_type": type(error).__name__}), action_id),
        )
    conn.commit()
    _event(conn, actor_id, "autonomy_error", {"stage": stage, "error_type": type(error).__name__, "message": str(error)[:300], "retry_seconds": delay}, action_id=action_id)


def _clear_retry(conn: sqlite3.Connection, actor_id: str) -> None:
    if actor_runtime(conn, actor_id)["retry"] is not None:
        set_retry(conn, actor_id, None)
        conn.commit()


def _mode(conn: sqlite3.Connection, actor_id: str) -> str:
    return str(actor_runtime(conn, actor_id)["autonomy_mode"] or NORMAL_MODE)


def _record_cognition_wake(conn: sqlite3.Connection, actor_id: str, *, now: float, reason: str) -> None:
    stats = actor_runtime(conn, actor_id)["cognition_stats"] or {}
    stats = {
        "decision_calls": int(stats.get("decision_calls", 0)) + 1,
        "last_call_wall_time": now,
        "last_call_sim_time": snapshot(conn, actor_id)["sim_time"],
        "last_wake_reason": reason,
    }
    set_actor_runtime(conn, actor_id, cognition_stats=stats, wake_reason=None)
    conn.commit()


def _finish_canary(conn: sqlite3.Connection, actor_id: str, *, success: bool, action_id: str | None, detail: str | None = None) -> None:
    set_actor_runtime(conn, actor_id, autonomy_enabled=False, autonomy_mode=NORMAL_MODE, wake_reason=None)
    if not success:
        set_actor_runtime(conn, actor_id, pending_action_id=None)
        set_field(conn, actor_id, "runtime.current_action", "idle")
        if action_id:
            conn.execute("UPDATE action_instances SET status='failed',updated_at=CURRENT_TIMESTAMP WHERE id=? AND status!='completed'", (action_id,))
    conn.commit()
    _event(conn, actor_id, "autonomy_canary_completed" if success else "autonomy_canary_failed", {"success": success, "action_id": action_id, "detail": detail}, action_id=action_id)


def set_autonomy_enabled(conn: sqlite3.Connection, enabled: bool, *, actor_id: str = "char_darian") -> dict[str, Any]:
    current = actor_runtime(conn, actor_id)
    if not enabled:
        if current["pending_action_id"] is not None:
            raise ValueError("Cannot disable autonomy while an action is pending; pause it or wait for completion")
        set_actor_runtime(conn, actor_id, autonomy_enabled=False, autonomy_mode=NORMAL_MODE, wake_reason=None)
    else:
        if current["pending_action_id"] is not None:
            raise ValueError("Cannot enable autonomy with a pre-existing pending action")
        set_actor_runtime(conn, actor_id, autonomy_mode=NORMAL_MODE, wake_reason="autonomy_enabled", autonomy_enabled=True)
    conn.commit()
    _event(conn, actor_id, "autonomy_control", {"enabled": enabled, "mode": _mode(conn, actor_id)})
    return autonomy_status(conn, actor_id)


def set_autonomy_paused(conn: sqlite3.Connection, paused: bool, *, actor_id: str = "char_darian") -> dict[str, Any]:
    set_runtime_value(conn, "paused", bool(paused))
    current = actor_runtime(conn, actor_id)
    if not paused and current["autonomy_enabled"] and current["pending_action_id"] is None:
        set_actor_runtime(conn, actor_id, wake_reason="resume")
    conn.commit()
    _event(conn, actor_id, "autonomy_control", {"paused": bool(paused)})
    return autonomy_status(conn, actor_id)


def set_autonomy_speed(conn: sqlite3.Connection, speed: float, *, actor_id: str = "char_darian") -> dict[str, Any]:
    value = float(speed)
    if value <= 0 or value > 3600:
        raise ValueError("Autonomy speed must be greater than 0 and at most 3600")
    if conn.execute("SELECT 1 FROM actor_runtime WHERE pending_action_id IS NOT NULL LIMIT 1").fetchone() is not None:
        raise ValueError("Cannot change global speed while any actor action is pending")
    set_runtime_value(conn, "speed", value)
    conn.commit()
    _event(conn, actor_id, "autonomy_control", {"speed": value})
    return autonomy_status(conn, actor_id)


def arm_canary_once(conn: sqlite3.Connection, *, actor_id: str = "char_darian") -> dict[str, Any]:
    state = actor_runtime(conn, actor_id)
    if state["autonomy_enabled"]:
        raise ValueError("Canary requires autonomy to be disabled first")
    if bool(runtime_value(conn, "paused", False)):
        raise ValueError("Canary requires runtime to be resumed")
    if state["pending_action_id"] is not None:
        raise ValueError("Canary requires no pending action")
    _clear_retry(conn, actor_id)
    set_actor_runtime(conn, actor_id, autonomy_mode=CANARY_MODE, wake_reason="canary_armed", autonomy_enabled=True)
    conn.commit()
    _event(conn, actor_id, "autonomy_canary_armed", {"mode": CANARY_MODE})
    return autonomy_status(conn, actor_id)


def autonomy_tick(conn: sqlite3.Connection, *, actor_id: str = "char_darian", provider: Any | None = None, now_wall: float | None = None) -> dict[str, Any]:
    now = _wall_now() if now_wall is None else float(now_wall)
    state_rt = actor_runtime(conn, actor_id)
    if not state_rt["autonomy_enabled"]:
        return {"ok": True, "state": "disabled"}
    if bool(runtime_value(conn, "paused", False)):
        return {"ok": True, "state": "paused"}
    if _retry_blocked(conn, actor_id, now):
        return {"ok": True, "state": "backoff"}

    owner = _acquire_lease(conn, actor_id, now=now)
    if owner is None:
        return {"ok": True, "state": "leased_elsewhere"}
    try:
        pending = pending_action(conn, actor_id)
        if pending:
            action_id = pending["action_id"]
            if _completion_already_recorded(conn, action_id):
                set_actor_runtime(conn, actor_id, pending_action_id=None, wake_reason="recovered_action_boundary")
                set_field(conn, actor_id, "runtime.current_action", "idle")
                conn.commit()
                if _mode(conn, actor_id) == CANARY_MODE:
                    _finish_canary(conn, actor_id, success=True, action_id=action_id, detail="recovered completed action")
                return {"ok": True, "state": "recovered_completed", "action_id": action_id}
            if now < float(pending["due_wall_time"]):
                return {"ok": True, "state": "in_progress", "action_id": action_id, "due_wall_time": pending["due_wall_time"]}
            action = _action_from_pending(pending)
            try:
                after = apply_action(conn, action, actor_id, action_id=action_id)
            except Exception as exc:
                _record_failure(conn, actor_id, stage="complete", error=exc, now=now, action_id=action_id)
                if _mode(conn, actor_id) == CANARY_MODE:
                    _finish_canary(conn, actor_id, success=False, action_id=action_id, detail=f"completion:{type(exc).__name__}")
                return {"ok": False, "state": "completion_error", "error": type(exc).__name__}
            set_actor_runtime(conn, actor_id, pending_action_id=None, wake_reason="action_completed")
            _clear_retry(conn, actor_id)
            conn.commit()
            if _mode(conn, actor_id) == CANARY_MODE:
                _finish_canary(conn, actor_id, success=True, action_id=action_id)
            return {"ok": True, "state": "completed", "action_id": action_id, "after": after}

        state = snapshot(conn, actor_id)
        decider = provider or ModelDecisionProvider(conn, character_id=actor_id)
        wake_reason = str(actor_runtime(conn, actor_id)["wake_reason"] or "decision_boundary")
        try:
            _record_cognition_wake(conn, actor_id, now=now, reason=wake_reason)
            action = decider.choose(state, ACTION_NAMES)
            validate_action(conn, actor_id, action)
        except Exception as exc:
            _record_failure(conn, actor_id, stage="decide", error=exc, now=now)
            if _mode(conn, actor_id) == CANARY_MODE:
                _finish_canary(conn, actor_id, success=False, action_id=None, detail=f"decision:{type(exc).__name__}")
            return {"ok": False, "state": "decision_error", "error": type(exc).__name__}

        speed = float(runtime_value(conn, "speed", 1.0))
        if speed <= 0:
            error = ValueError("Runtime speed must be greater than zero")
            _record_failure(conn, actor_id, stage="schedule", error=error, now=now)
            if _mode(conn, actor_id) == CANARY_MODE:
                _finish_canary(conn, actor_id, success=False, action_id=None, detail="schedule:ValueError")
            return {"ok": False, "state": "schedule_error", "error": type(error).__name__}

        action_id = str(uuid.uuid4())
        due = now + (action.duration_minutes * 60.0 / speed)
        ensure_action_instance(conn, action, actor_id, action_id=action_id, status="in_progress", planned_wall_time=now, due_wall_time=due, speed_at_plan=speed)
        set_actor_runtime(conn, actor_id, pending_action_id=action_id)
        set_field(conn, actor_id, "runtime.current_action", action.name)
        _clear_retry(conn, actor_id)
        conn.commit()
        pending = pending_action(conn, actor_id)
        _event(conn, actor_id, "action_started", {
            "action_id": action_id, "action": action.name, "target": action.target,
            "duration_minutes": action.duration_minutes, "reason": action.reason,
            "due_wall_time": due, "autonomy_mode": _mode(conn, actor_id),
            "place_id": state["location"], "participants": list(action.participants),
            "resources": list(action.resources), "conditions": action.conditions, "modifiers": action.modifiers,
        }, action_id=action_id)
        return {"ok": True, "state": "planned", "pending": pending}
    finally:
        _release_lease(conn, actor_id, owner)


def run_canary_once(conn: sqlite3.Connection, *, actor_id: str = "char_darian", provider: Any | None = None, now_wall: float | None = None, lease_retries: int = 20) -> dict[str, Any]:
    start = _wall_now() if now_wall is None else float(now_wall)
    before = snapshot(conn, actor_id)
    arm_canary_once(conn, actor_id=actor_id)
    planned: dict[str, Any] | None = None
    for attempt in range(max(1, lease_retries)):
        pending = pending_action(conn, actor_id)
        if pending is not None:
            planned = {"ok": True, "state": "planned_elsewhere", "pending": pending}; break
        current = autonomy_status(conn, actor_id)
        if not current["autonomy_enabled"]:
            return {"ok": False, "state": "failed_closed", "before": before, "after": current, "plan": planned}
        result = autonomy_tick(conn, actor_id=actor_id, provider=provider, now_wall=start + attempt * 0.001)
        if result.get("state") == "planned": planned = result; break
        if result.get("state") in {"decision_error", "schedule_error", "completion_error"}:
            return {"ok": False, "state": result["state"], "before": before, "after": autonomy_status(conn, actor_id), "plan": result}
        if result.get("state") == "leased_elsewhere": time.sleep(0.05)
    pending = pending_action(conn, actor_id)
    if pending is None:
        current = autonomy_status(conn, actor_id)
        if current["autonomy_enabled"]: _finish_canary(conn, actor_id, success=False, action_id=None, detail="control:no_pending_action")
        return {"ok": False, "state": "no_pending_action", "before": before, "after": autonomy_status(conn, actor_id), "plan": planned}
    completion: dict[str, Any] | None = None
    due = float(pending["due_wall_time"]) + 0.001
    for _ in range(max(1, lease_retries)):
        completion = autonomy_tick(conn, actor_id=actor_id, provider=provider, now_wall=due)
        if completion.get("state") in {"completed", "recovered_completed", "completion_error", "disabled"}: break
        if completion.get("state") == "leased_elsewhere": time.sleep(0.05)
    after = autonomy_status(conn, actor_id)
    success = bool(completion and completion.get("state") in {"completed", "recovered_completed"} and not after["autonomy_enabled"] and after["mode"] == NORMAL_MODE and after["pending_action"] is None)
    if not success and after["autonomy_enabled"]:
        _finish_canary(conn, actor_id, success=False, action_id=pending.get("action_id"), detail="control:incomplete")
        after = autonomy_status(conn, actor_id)
    return {"ok": success, "state": "completed" if success else "failed_closed", "before": before, "plan": planned, "completion": completion, "after": after}


def autonomy_status(conn: sqlite3.Connection, actor_id: str = "char_darian") -> dict[str, Any]:
    state = actor_runtime(conn, actor_id)
    return {
        "autonomy_enabled": state["autonomy_enabled"],
        "mode": state["autonomy_mode"],
        "paused": bool(runtime_value(conn, "paused", False)),
        "speed": float(runtime_value(conn, "speed", 1.0)),
        "pending_action": pending_action(conn, actor_id),
        "retry": state["retry"],
        "cognition_wake_reason": state["wake_reason"],
        "cognition_stats": state["cognition_stats"] or {"decision_calls": 0},
        "character": snapshot(conn, actor_id),
    }

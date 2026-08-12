from __future__ import annotations

import json
import sqlite3
import time
import uuid
from typing import Any

from .model_decision import ModelDecisionProvider
from .simulation import ACTION_NAMES, Action, apply_action, runtime_value, set_runtime_value, snapshot, validate_action
from .world import set_field


LEASE_KEY = "autonomy_lease"
PENDING_KEY = "autonomy_pending_action"
RETRY_KEY = "autonomy_retry"
MODE_KEY = "autonomy_mode"
NORMAL_MODE = "normal"
CANARY_MODE = "canary_once"


def _wall_now() -> float:
    return time.time()


def _event(conn: sqlite3.Connection, actor_id: str, event_type: str, payload: dict[str, Any]) -> None:
    conn.execute(
        "INSERT INTO events(sim_time, actor_id, event_type, payload_json) VALUES (?, ?, ?, ?)",
        (snapshot(conn, actor_id)["sim_time"], actor_id, event_type, json.dumps(payload, ensure_ascii=False)),
    )
    conn.commit()


def _acquire_lease(conn: sqlite3.Connection, *, now: float, ttl_seconds: float = 30.0) -> str | None:
    owner = str(uuid.uuid4())
    conn.execute("BEGIN IMMEDIATE")
    lease = runtime_value(conn, LEASE_KEY, None)
    if lease and float(lease.get("expires_at", 0)) > now:
        conn.rollback()
        return None
    set_runtime_value(conn, LEASE_KEY, {"owner": owner, "expires_at": now + ttl_seconds})
    conn.commit()
    return owner


def _release_lease(conn: sqlite3.Connection, owner: str) -> None:
    lease = runtime_value(conn, LEASE_KEY, None)
    if lease and lease.get("owner") == owner:
        set_runtime_value(conn, LEASE_KEY, None)
        conn.commit()


def _action_from_pending(pending: dict[str, Any]) -> Action:
    return Action(pending["action"], int(pending["duration_minutes"]), pending.get("target"), pending.get("reason"))


def _completion_already_recorded(conn: sqlite3.Connection, action_id: str) -> bool:
    rows = conn.execute("SELECT payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 50").fetchall()
    return any(json.loads(row[0]).get("action_id") == action_id for row in rows)


def _retry_blocked(conn: sqlite3.Connection, now: float) -> bool:
    retry = runtime_value(conn, RETRY_KEY, None)
    return bool(retry and float(retry.get("retry_after", 0)) > now)


def _record_failure(conn: sqlite3.Connection, actor_id: str, *, stage: str, error: Exception, now: float) -> None:
    previous = runtime_value(conn, RETRY_KEY, {}) or {}
    failures = min(int(previous.get("failures", 0)) + 1, 8)
    delay = min(300.0, float(2 ** failures))
    set_runtime_value(conn, RETRY_KEY, {"failures": failures, "retry_after": now + delay, "last_error": type(error).__name__})
    conn.commit()
    _event(conn, actor_id, "autonomy_error", {"stage": stage, "error_type": type(error).__name__, "message": str(error)[:300], "retry_seconds": delay})


def _clear_retry(conn: sqlite3.Connection) -> None:
    if runtime_value(conn, RETRY_KEY, None) is not None:
        set_runtime_value(conn, RETRY_KEY, None)
        conn.commit()


def _mode(conn: sqlite3.Connection) -> str:
    return str(runtime_value(conn, MODE_KEY, NORMAL_MODE) or NORMAL_MODE)


def _finish_canary(conn: sqlite3.Connection, actor_id: str, *, success: bool, action_id: str | None, detail: str | None = None) -> None:
    set_runtime_value(conn, "autonomy_enabled", False)
    set_runtime_value(conn, MODE_KEY, NORMAL_MODE)
    if not success:
        set_runtime_value(conn, PENDING_KEY, None)
        set_field(conn, actor_id, "runtime.current_action", "idle")
    conn.commit()
    _event(
        conn,
        actor_id,
        "autonomy_canary_completed" if success else "autonomy_canary_failed",
        {"success": success, "action_id": action_id, "detail": detail},
    )


def set_autonomy_enabled(conn: sqlite3.Connection, enabled: bool, *, actor_id: str = "char_darian") -> dict[str, Any]:
    if not enabled:
        if runtime_value(conn, PENDING_KEY, None) is not None:
            raise ValueError("Cannot disable autonomy while an action is pending; pause it or wait for completion")
        set_runtime_value(conn, "autonomy_enabled", False)
        set_runtime_value(conn, MODE_KEY, NORMAL_MODE)
    else:
        if runtime_value(conn, PENDING_KEY, None) is not None:
            raise ValueError("Cannot enable autonomy with a pre-existing pending action")
        set_runtime_value(conn, MODE_KEY, NORMAL_MODE)
        set_runtime_value(conn, "autonomy_enabled", True)
    conn.commit()
    _event(conn, actor_id, "autonomy_control", {"enabled": enabled, "mode": _mode(conn)})
    return autonomy_status(conn, actor_id)


def set_autonomy_paused(conn: sqlite3.Connection, paused: bool, *, actor_id: str = "char_darian") -> dict[str, Any]:
    set_runtime_value(conn, "paused", bool(paused))
    conn.commit()
    _event(conn, actor_id, "autonomy_control", {"paused": bool(paused)})
    return autonomy_status(conn, actor_id)


def set_autonomy_speed(conn: sqlite3.Connection, speed: float, *, actor_id: str = "char_darian") -> dict[str, Any]:
    value = float(speed)
    if value <= 0 or value > 3600:
        raise ValueError("Autonomy speed must be greater than 0 and at most 3600")
    if runtime_value(conn, PENDING_KEY, None) is not None:
        raise ValueError("Cannot change speed while an action is pending")
    set_runtime_value(conn, "speed", value)
    conn.commit()
    _event(conn, actor_id, "autonomy_control", {"speed": value})
    return autonomy_status(conn, actor_id)


def arm_canary_once(conn: sqlite3.Connection, *, actor_id: str = "char_darian") -> dict[str, Any]:
    """Arm exactly one production-style autonomous action.

    Low-level primitive retained for tests/service coordination. User-facing control
    should normally call run_canary_once(), which bounds wall time as well as action count.
    """
    if bool(runtime_value(conn, "autonomy_enabled", False)):
        raise ValueError("Canary requires autonomy to be disabled first")
    if bool(runtime_value(conn, "paused", False)):
        raise ValueError("Canary requires runtime to be resumed")
    if runtime_value(conn, PENDING_KEY, None) is not None:
        raise ValueError("Canary requires no pending action")
    _clear_retry(conn)
    set_runtime_value(conn, MODE_KEY, CANARY_MODE)
    set_runtime_value(conn, "autonomy_enabled", True)
    conn.commit()
    _event(conn, actor_id, "autonomy_canary_armed", {"mode": CANARY_MODE})
    return autonomy_status(conn, actor_id)


def autonomy_tick(
    conn: sqlite3.Connection,
    *,
    actor_id: str = "char_darian",
    provider: Any | None = None,
    now_wall: float | None = None,
) -> dict[str, Any]:
    """Advance at most one scheduler transition: idle, plan, or complete."""
    now = _wall_now() if now_wall is None else float(now_wall)
    if not bool(runtime_value(conn, "autonomy_enabled", False)):
        return {"ok": True, "state": "disabled"}
    if bool(runtime_value(conn, "paused", False)):
        return {"ok": True, "state": "paused"}
    if _retry_blocked(conn, now):
        return {"ok": True, "state": "backoff"}

    owner = _acquire_lease(conn, now=now)
    if owner is None:
        return {"ok": True, "state": "leased_elsewhere"}

    try:
        pending = runtime_value(conn, PENDING_KEY, None)
        if pending:
            action_id = pending["action_id"]
            if _completion_already_recorded(conn, action_id):
                set_runtime_value(conn, PENDING_KEY, None)
                set_field(conn, actor_id, "runtime.current_action", "idle")
                conn.commit()
                if _mode(conn) == CANARY_MODE:
                    _finish_canary(conn, actor_id, success=True, action_id=action_id, detail="recovered completed action")
                return {"ok": True, "state": "recovered_completed", "action_id": action_id}
            if now < float(pending["due_wall_time"]):
                return {"ok": True, "state": "in_progress", "action_id": action_id, "due_wall_time": pending["due_wall_time"]}
            action = _action_from_pending(pending)
            try:
                after = apply_action(conn, action, actor_id, action_id=action_id)
            except Exception as exc:
                _record_failure(conn, actor_id, stage="complete", error=exc, now=now)
                if _mode(conn) == CANARY_MODE:
                    _finish_canary(conn, actor_id, success=False, action_id=action_id, detail=f"completion:{type(exc).__name__}")
                return {"ok": False, "state": "completion_error", "error": type(exc).__name__}
            set_runtime_value(conn, PENDING_KEY, None)
            _clear_retry(conn)
            conn.commit()
            if _mode(conn) == CANARY_MODE:
                _finish_canary(conn, actor_id, success=True, action_id=action_id)
            return {"ok": True, "state": "completed", "action_id": action_id, "after": after}

        state = snapshot(conn, actor_id)
        decider = provider or ModelDecisionProvider(conn, character_id=actor_id)
        try:
            action = decider.choose(state, ACTION_NAMES)
            validate_action(conn, actor_id, action)
        except Exception as exc:
            _record_failure(conn, actor_id, stage="decide", error=exc, now=now)
            if _mode(conn) == CANARY_MODE:
                _finish_canary(conn, actor_id, success=False, action_id=None, detail=f"decision:{type(exc).__name__}")
            return {"ok": False, "state": "decision_error", "error": type(exc).__name__}

        speed = float(runtime_value(conn, "speed", 1.0))
        if speed <= 0:
            error = ValueError("Runtime speed must be greater than zero")
            _record_failure(conn, actor_id, stage="schedule", error=error, now=now)
            if _mode(conn) == CANARY_MODE:
                _finish_canary(conn, actor_id, success=False, action_id=None, detail="schedule:ValueError")
            return {"ok": False, "state": "schedule_error", "error": type(error).__name__}

        action_id = str(uuid.uuid4())
        pending = {
            "action_id": action_id,
            "action": action.name,
            "duration_minutes": action.duration_minutes,
            "target": action.target,
            "reason": action.reason,
            "planned_sim_time": state["sim_time"],
            "planned_wall_time": now,
            "due_wall_time": now + (action.duration_minutes * 60.0 / speed),
            "speed_at_plan": speed,
            "autonomy_mode": _mode(conn),
        }
        set_runtime_value(conn, PENDING_KEY, pending)
        set_field(conn, actor_id, "runtime.current_action", action.name)
        _clear_retry(conn)
        conn.commit()
        _event(conn, actor_id, "action_started", {"action_id": action_id, "action": action.name, "target": action.target, "duration_minutes": action.duration_minutes, "reason": action.reason, "due_wall_time": pending["due_wall_time"], "autonomy_mode": pending["autonomy_mode"]})
        return {"ok": True, "state": "planned", "pending": pending}
    finally:
        _release_lease(conn, owner)


def run_canary_once(
    conn: sqlite3.Connection,
    *,
    actor_id: str = "char_darian",
    provider: Any | None = None,
    now_wall: float | None = None,
    lease_retries: int = 20,
) -> dict[str, Any]:
    """Run one production-style action synchronously, then auto-disable.

    The simulated action keeps its authored duration, but the control command advances
    the scheduler directly to that action's due point so a canary cannot remain armed
    for minutes or hours of wall time. Runtime validation, persistence, lease handling,
    idempotency, state mutation, and canary auto-disable all stay on the normal scheduler path.
    """
    start = _wall_now() if now_wall is None else float(now_wall)
    before = snapshot(conn, actor_id)
    arm_canary_once(conn, actor_id=actor_id)

    planned: dict[str, Any] | None = None
    for attempt in range(max(1, lease_retries)):
        pending = runtime_value(conn, PENDING_KEY, None)
        if pending is not None:
            planned = {"ok": True, "state": "planned_elsewhere", "pending": pending}
            break
        current = autonomy_status(conn, actor_id)
        if not current["autonomy_enabled"]:
            return {"ok": False, "state": "failed_closed", "before": before, "after": current, "plan": planned}
        result = autonomy_tick(conn, actor_id=actor_id, provider=provider, now_wall=start + attempt * 0.001)
        if result.get("state") == "planned":
            planned = result
            break
        if result.get("state") in {"decision_error", "schedule_error", "completion_error"}:
            return {"ok": False, "state": result["state"], "before": before, "after": autonomy_status(conn, actor_id), "plan": result}
        if result.get("state") == "leased_elsewhere":
            time.sleep(0.05)
            continue

    pending = runtime_value(conn, PENDING_KEY, None)
    if pending is None:
        current = autonomy_status(conn, actor_id)
        if current["autonomy_enabled"]:
            _finish_canary(conn, actor_id, success=False, action_id=None, detail="control:no_pending_action")
        return {"ok": False, "state": "no_pending_action", "before": before, "after": autonomy_status(conn, actor_id), "plan": planned}

    completion: dict[str, Any] | None = None
    due = float(pending["due_wall_time"]) + 0.001
    for _ in range(max(1, lease_retries)):
        completion = autonomy_tick(conn, actor_id=actor_id, provider=provider, now_wall=due)
        if completion.get("state") in {"completed", "recovered_completed", "completion_error"}:
            break
        if completion.get("state") == "leased_elsewhere":
            time.sleep(0.05)
            continue
        if completion.get("state") == "disabled":
            break

    after = autonomy_status(conn, actor_id)
    success = (
        completion is not None
        and completion.get("state") in {"completed", "recovered_completed"}
        and not after["autonomy_enabled"]
        and after["mode"] == NORMAL_MODE
        and after["pending_action"] is None
    )
    if not success and after["autonomy_enabled"]:
        _finish_canary(conn, actor_id, success=False, action_id=pending.get("action_id"), detail="control:incomplete")
        after = autonomy_status(conn, actor_id)
    return {
        "ok": success,
        "state": "completed" if success else "failed_closed",
        "before": before,
        "plan": planned,
        "completion": completion,
        "after": after,
    }


def autonomy_status(conn: sqlite3.Connection, actor_id: str = "char_darian") -> dict[str, Any]:
    return {
        "autonomy_enabled": bool(runtime_value(conn, "autonomy_enabled", False)),
        "mode": _mode(conn),
        "paused": bool(runtime_value(conn, "paused", False)),
        "speed": float(runtime_value(conn, "speed", 1.0)),
        "pending_action": runtime_value(conn, PENDING_KEY, None),
        "retry": runtime_value(conn, RETRY_KEY, None),
        "character": snapshot(conn, actor_id),
    }

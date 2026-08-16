from __future__ import annotations

import json
import os
import signal
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .actor_runtime import actor_runtime, set_actor_runtime, set_retry
from .autonomy import autonomy_tick as core_autonomy_tick
from .autonomy_intent import CONDITION_KEY, active_intent, transition_for_action
from .autonomy_livelock_watchdog import authoritative_recovery_action
from .db import connect
from .event_log import record_event
from .model_decision import ModelDecisionProvider
from .simulation import Action, snapshot


DB_PATH = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
CHECK_INTERVAL_SECONDS = 2.0
RESTART_DELAY_SECONDS = 5.0
DECISION_RECOVERY_THRESHOLD = 3
STALE_RUNTIME_SECONDS = 120.0
RUNNING = True
CHILD: subprocess.Popen[Any] | None = None


class _StaticProvider:
    def __init__(self, action: Action) -> None:
        self.action = action

    def choose(self, _state: dict[str, Any], _available_actions: list[str]) -> Action:
        return self.action


def _parse_sqlite_timestamp(value: str | None) -> float | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def _active_actor_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        """SELECT actor_id,autonomy_mode,pending_action_id,retry_failures,retry_after,retry_last_error,
                  lease_owner,lease_expires_at,updated_at
           FROM actor_runtime
           WHERE autonomy_enabled=1
           ORDER BY actor_id"""
    ).fetchall()


def _repeated_decision_validation_failure(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    sim_time: str,
    threshold: int = DECISION_RECOVERY_THRESHOLD,
) -> bool:
    rows = conn.execute(
        "SELECT sim_time,payload_json FROM events WHERE actor_id=? AND event_type='autonomy_error' ORDER BY id DESC LIMIT ?",
        (actor_id, int(threshold)),
    ).fetchall()
    if len(rows) < threshold:
        return False
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if str(row["sim_time"]) != str(sim_time):
            return False
        if payload.get("stage") != "decide" or payload.get("error_type") != "ValueError":
            return False
    return True


def _recovery_action(conn: sqlite3.Connection, actor_id: str, state: dict[str, Any]) -> Action | None:
    enriched = ModelDecisionProvider(
        conn,
        character_id=actor_id,
        capture_context=False,
    )._enrich_state(state)
    action = authoritative_recovery_action(enriched)
    if action is None:
        return None

    conditions = dict(action.conditions)
    conditions["autonomy_recovery"] = {
        "source": "service-supervisor-v1",
        "basis": "repeated_decision_validation_failure",
        "threshold": DECISION_RECOVERY_THRESHOLD,
    }
    current_intent = active_intent(conn, actor_id, as_of_sim_time=str(state["sim_time"]))
    conditions[CONDITION_KEY] = transition_for_action(
        current_intent,
        action,
        actor_id=actor_id,
        sim_time=str(state["sim_time"]),
        origin_location_id=str(state["location"]),
    )
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


def recover_decision_livelock(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    now_wall: float | None = None,
) -> dict[str, Any] | None:
    runtime = actor_runtime(conn, actor_id)
    if not runtime["autonomy_enabled"] or runtime["autonomy_mode"] != "normal":
        return None
    if runtime["pending_action_id"] is not None:
        return None
    retry = runtime["retry"] or {}
    if int(retry.get("failures", 0)) < DECISION_RECOVERY_THRESHOLD:
        return None
    if retry.get("last_error") != "ValueError":
        return None

    state = snapshot(conn, actor_id)
    if not _repeated_decision_validation_failure(
        conn,
        actor_id,
        sim_time=str(state["sim_time"]),
    ):
        return None

    action = _recovery_action(conn, actor_id, state)
    if action is None:
        return None

    set_retry(conn, actor_id, None)
    set_actor_runtime(conn, actor_id, wake_reason="supervisor_decision_recovery")
    conn.commit()
    result = core_autonomy_tick(
        conn,
        actor_id=actor_id,
        provider=_StaticProvider(action),
        now_wall=time.time() if now_wall is None else float(now_wall),
    )
    if result.get("state") != "planned":
        return None

    record_event(
        conn,
        sim_time=str(state["sim_time"]),
        actor_id=actor_id,
        event_type="autonomy_supervisor_recovery",
        location_id=str(state["location"]),
        payload={
            "source": "service-supervisor-v1",
            "basis": "repeated_decision_validation_failure",
            "prior_failures": int(retry.get("failures", 0)),
            "scheduled_action": action.name,
            "scheduled_target": action.target,
            "action_id": (result.get("pending") or {}).get("action_id"),
        },
    )
    conn.commit()
    return result


def stale_runtime_detected(conn: sqlite3.Connection, *, now_wall: float | None = None) -> bool:
    now = time.time() if now_wall is None else float(now_wall)
    paused_row = conn.execute("SELECT value_json FROM runtime_state WHERE key='paused'").fetchone()
    if paused_row is not None:
        try:
            if bool(json.loads(paused_row[0])):
                return False
        except Exception:
            pass

    for row in _active_actor_rows(conn):
        if row["pending_action_id"] is not None:
            continue
        if int(row["retry_failures"] or 0) > 0:
            continue
        updated_at = _parse_sqlite_timestamp(row["updated_at"])
        if updated_at is not None and now - updated_at > STALE_RUNTIME_SECONDS:
            return True
    return False


def _stop(_signum, _frame) -> None:
    global RUNNING
    RUNNING = False
    if CHILD is not None and CHILD.poll() is None:
        CHILD.terminate()


def _start_child() -> subprocess.Popen[Any]:
    return subprocess.Popen([sys.executable, "-m", "observer_sandbox.service"], env=os.environ.copy())


def _terminate_child(child: subprocess.Popen[Any]) -> None:
    if child.poll() is not None:
        return
    child.terminate()
    try:
        child.wait(timeout=10)
    except subprocess.TimeoutExpired:
        child.kill()
        child.wait(timeout=10)


def main() -> None:
    global CHILD
    signal.signal(signal.SIGTERM, _stop)
    signal.signal(signal.SIGINT, _stop)

    while RUNNING:
        CHILD = _start_child()
        restart_requested = False
        while RUNNING and CHILD.poll() is None:
            time.sleep(CHECK_INTERVAL_SECONDS)
            if not DB_PATH.exists():
                continue
            try:
                with connect(DB_PATH) as conn:
                    for row in _active_actor_rows(conn):
                        recover_decision_livelock(conn, str(row["actor_id"]))
                    if stale_runtime_detected(conn):
                        restart_requested = True
            except Exception:
                # The supervisor must not become a second failure source. A child
                # restart is safer than silently remaining wedged on repeated
                # supervisor inspection failures.
                restart_requested = True
            if restart_requested:
                _terminate_child(CHILD)
                break

        if not RUNNING:
            break
        if CHILD.poll() is None:
            _terminate_child(CHILD)
        time.sleep(RESTART_DELAY_SECONDS)

    if CHILD is not None:
        _terminate_child(CHILD)


if __name__ == "__main__":
    main()

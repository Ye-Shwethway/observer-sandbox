from __future__ import annotations

import json
import sqlite3
import time
from typing import Any

from .actor_runtime import actor_runtime, set_actor_runtime, set_retry
from .autonomy_intent import autonomy_tick
from .autonomy_livelock_watchdog import authoritative_recovery_action
from .event_log import record_event
from .model_decision import ModelDecisionProvider
from .simulation import Action, snapshot


DECISION_RECOVERY_THRESHOLD = 3


class _StaticProvider:
    def __init__(self, action: Action) -> None:
        self.action = action

    def choose(self, _state: dict[str, Any], _available_actions: list[str]) -> Action:
        return self.action


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


def recover_decision_livelock(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    now_wall: float | None = None,
) -> dict[str, Any] | None:
    """Recover a repeated deterministic decision-validation livelock.

    Recovery is deliberately narrow: only repeated decision-stage ``ValueError``
    failures at one simulation boundary are eligible. Provider/API/configuration
    failures remain visible and retain normal retry/backoff semantics.
    """
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

    enriched = ModelDecisionProvider(
        conn,
        character_id=actor_id,
        capture_context=False,
    )._enrich_state(state)
    base_action = authoritative_recovery_action(enriched)
    if base_action is None:
        return None

    conditions = dict(base_action.conditions)
    conditions["autonomy_recovery"] = {
        "source": "autonomy-recovery-v1",
        "basis": "repeated_decision_validation_failure",
        "threshold": DECISION_RECOVERY_THRESHOLD,
    }
    action = Action(
        base_action.name,
        base_action.duration_minutes,
        base_action.target,
        base_action.reason,
        tuple(base_action.participants),
        tuple(base_action.resources),
        conditions,
        dict(base_action.modifiers),
    )

    set_retry(conn, actor_id, None)
    set_actor_runtime(conn, actor_id, wake_reason="decision_livelock_recovery")
    conn.commit()

    result = autonomy_tick(
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
        event_type="autonomy_recovery",
        location_id=str(state["location"]),
        payload={
            "source": "autonomy-recovery-v1",
            "basis": "repeated_decision_validation_failure",
            "prior_failures": int(retry.get("failures", 0)),
            "scheduled_action": action.name,
            "scheduled_target": action.target,
            "action_id": (result.get("pending") or {}).get("action_id"),
        },
    )
    conn.commit()
    return result

from __future__ import annotations

import json
import sqlite3
from typing import Any

from .actor_runtime import actor_runtime
from .simulation import Action


PAIR_VALIDATION_MARKER = "outside authoritative action_options"
RECOVERY_THRESHOLD = 3


def repeated_pair_validation_livelock(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    sim_time: str,
    prior_failures_required: int = RECOVERY_THRESHOLD - 1,
) -> bool:
    """Recognize only repeated decision-pair validation failures at one sim boundary.

    Provider/API failures, schedule/completion failures, unrelated ValueErrors and
    canary runs intentionally remain outside this watchdog.
    """
    runtime = actor_runtime(conn, actor_id)
    if runtime["autonomy_mode"] != "normal" or runtime["pending_action_id"] is not None:
        return False
    retry = runtime["retry"] or {}
    if int(retry.get("failures", 0)) < prior_failures_required:
        return False

    rows = conn.execute(
        "SELECT sim_time,payload_json FROM events WHERE actor_id=? AND event_type='autonomy_error' ORDER BY id DESC LIMIT ?",
        (actor_id, int(prior_failures_required)),
    ).fetchall()
    if len(rows) < prior_failures_required:
        return False
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if str(row["sim_time"]) != str(sim_time):
            return False
        if payload.get("stage") != "decide" or payload.get("error_type") != "ValueError":
            return False
        if PAIR_VALIDATION_MARKER not in str(payload.get("message", "")):
            return False
    return True


def _meal_resources_for_option(option: dict[str, Any]) -> tuple[dict[str, Any], ...]:
    if option.get("action") != "eat":
        return ()
    choices = option.get("meal_resources") or []
    if not choices:
        return ()
    choice = choices[0]
    return ({
        "stack_id": str(choice["stack_id"]),
        "quantity": float(choice["default_quantity"]),
    },)


def authoritative_recovery_action(enriched: dict[str, Any]) -> Action | None:
    """Build a lowest-risk continuity action from the already-shaped legal surface."""
    options = [option for option in (enriched.get("action_options") or []) if isinstance(option, dict)]
    if not options:
        return None

    highest = (enriched.get("decision_signals") or {}).get("highest_priority")
    if highest:
        # Need shaping already reduced this surface to resolver actions/first hops.
        candidates = options
    else:
        idle = [option for option in options if option.get("action") == "idle" and not option.get("target")]
        candidates = idle or [option for option in options if option.get("action") == "rest" and not option.get("target")]
        if not candidates:
            candidates = options

    option = sorted(
        candidates,
        key=lambda item: (str(item.get("action", "")), str(item.get("target") or "")),
    )[0]
    duration = option.get("duration") or (1, 1)
    minimum = int(duration[0])
    recommended = (enriched.get("decision_signals") or {}).get("recommended_duration") or {}
    if recommended.get("action") == option.get("action"):
        minimum = max(minimum, int(recommended.get("min_minutes", minimum)))

    return Action(
        str(option["action"]),
        minimum,
        option.get("target") if isinstance(option.get("target"), str) else None,
        "autonomy livelock recovery from authoritative action options",
        resources=_meal_resources_for_option(option),
        conditions={
            "autonomy_recovery": {
                "source": "autonomy-livelock-watchdog-v1",
                "basis": "repeated_pair_validation_failure",
                "threshold": RECOVERY_THRESHOLD,
            }
        },
    )

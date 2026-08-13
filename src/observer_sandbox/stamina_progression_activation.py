from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .recovery_realization import FATIGUE_HARD_BLOCK, recovery_state_quality
from .stamina_progression import (
    FULL_RECOVERY_HOURS,
    SETTLEMENT_EVENT_TYPE,
    latest_stamina_settlement_time,
    settle_stamina_progression,
    stamina_stimulus_events,
)


ACTIVATION_POLICY_ID = "stamina-progression-auto-activation-v1"
DETRAINING_CHECKPOINT_HOURS = 24.0


@dataclass(frozen=True)
class StaminaProgressionDue:
    due: bool
    reason: str
    last_settled_sim_time: str | None
    eligible_stimulus_event_ids: tuple[int, ...]
    hours_since_settlement: float | None


def _dt(raw: str) -> datetime:
    return datetime.fromisoformat(raw)


def _consumed_stimulus_ids(conn: sqlite3.Connection, actor_id: str) -> set[int]:
    rows = conn.execute(
        "SELECT payload_json FROM events WHERE actor_id=? AND event_type=?",
        (actor_id, SETTLEMENT_EVENT_TYPE),
    ).fetchall()
    consumed: set[int] = set()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        for event_id in payload.get("consumed_stimulus_event_ids") or []:
            if isinstance(event_id, int):
                consumed.add(event_id)
    return consumed


def stamina_progression_due(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
    detraining_checkpoint_hours: float = DETRAINING_CHECKPOINT_HOURS,
) -> StaminaProgressionDue:
    checkpoint_hours = float(detraining_checkpoint_hours)
    if checkpoint_hours <= 0.0:
        raise ValueError("detraining_checkpoint_hours must be positive")

    as_of = _dt(as_of_sim_time)
    last_settled = latest_stamina_settlement_time(conn, actor_id)
    stimuli = stamina_stimulus_events(conn, actor_id, as_of_sim_time=as_of_sim_time)

    if last_settled is None:
        return StaminaProgressionDue(True, "bootstrap", None, (), None)

    last_dt = _dt(last_settled)
    if as_of <= last_dt:
        return StaminaProgressionDue(False, "same_or_older_boundary", last_settled, (), 0.0)

    consumed = _consumed_stimulus_ids(conn, actor_id)
    state_quality, _ = recovery_state_quality(state)
    recovery_allowed = float(state["fatigue"]) < FATIGUE_HARD_BLOCK and state_quality > 0.0
    eligible: list[int] = []
    if recovery_allowed:
        for event in stimuli:
            if event.event_id in consumed:
                continue
            age_hours = max(0.0, (as_of - _dt(event.sim_time)).total_seconds() / 3600.0)
            if age_hours >= FULL_RECOVERY_HOURS:
                eligible.append(event.event_id)

    elapsed_hours = max(0.0, (as_of - last_dt).total_seconds() / 3600.0)
    if eligible:
        return StaminaProgressionDue(
            True,
            "eligible_stimulus",
            last_settled,
            tuple(eligible),
            round(elapsed_hours, 6),
        )

    if stimuli and elapsed_hours >= checkpoint_hours:
        return StaminaProgressionDue(
            True,
            "detraining_checkpoint",
            last_settled,
            (),
            round(elapsed_hours, 6),
        )

    return StaminaProgressionDue(
        False,
        "not_due",
        last_settled,
        (),
        round(elapsed_hours, 6),
    )


def maybe_settle_stamina_progression(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    due = stamina_progression_due(
        conn,
        actor_id,
        as_of_sim_time=as_of_sim_time,
        state=state,
    )
    if not due.due:
        return {
            "state": "skipped",
            "reason": due.reason,
            "policy_id": ACTIVATION_POLICY_ID,
            "settlement": None,
        }

    settlement = settle_stamina_progression(
        conn,
        actor_id,
        as_of_sim_time=as_of_sim_time,
        state=state,
    )
    return {
        "state": "settled",
        "reason": due.reason,
        "policy_id": ACTIVATION_POLICY_ID,
        "settlement": settlement,
    }

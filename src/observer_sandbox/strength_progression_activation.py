from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .recovery_realization import FATIGUE_HARD_BLOCK, FULL_RECOVERY_HOURS, recovery_state_quality
from .strength_progression import SETTLEMENT_EVENT_TYPE, settle_strength_progression


ACTIVATION_POLICY_ID = "strength-progression-auto-activation-v1"
DETRAINING_CHECKPOINT_HOURS = 24.0


@dataclass(frozen=True)
class StrengthProgressionDue:
    due: bool
    reason: str
    last_settled_sim_time: str | None
    eligible_stimulus_event_ids: tuple[int, ...]
    hours_since_settlement: float | None


def _dt(raw: str) -> datetime:
    return datetime.fromisoformat(raw)


def _settlement_state(conn: sqlite3.Connection, actor_id: str) -> tuple[str | None, set[int]]:
    rows = conn.execute(
        "SELECT sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (actor_id, SETTLEMENT_EVENT_TYPE),
    ).fetchall()
    latest: tuple[datetime, str] | None = None
    consumed: set[int] = set()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        raw = payload.get("settled_through_sim_time") or row["sim_time"]
        if isinstance(raw, str):
            parsed = _dt(raw)
            if latest is None or parsed > latest[0]:
                latest = (parsed, raw)
        for event_id in payload.get("consumed_stimulus_event_ids") or []:
            if isinstance(event_id, int):
                consumed.add(event_id)
    return (None if latest is None else latest[1], consumed)


def _strength_stimulus_events(conn: sqlite3.Connection, actor_id: str, as_of_sim_time: str) -> list[tuple[int, str]]:
    as_of = _dt(as_of_sim_time)
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed'",
        (actor_id,),
    ).fetchall()
    found: list[tuple[int, str]] = []
    for row in rows:
        if _dt(row["sim_time"]) > as_of:
            continue
        payload = json.loads(row["payload_json"] or "{}")
        evidence = payload.get("training_stimulus")
        if not isinstance(evidence, dict) or evidence.get("domain") != "strength":
            continue
        units = evidence.get("stimulus_units")
        if isinstance(units, (int, float)) and float(units) > 0.0:
            found.append((int(row["id"]), row["sim_time"]))
    found.sort(key=lambda item: (_dt(item[1]), item[0]))
    return found


def strength_progression_due(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
    recovery_multiplier: float = 1.0,
    detraining_checkpoint_hours: float = DETRAINING_CHECKPOINT_HOURS,
) -> StrengthProgressionDue:
    """Decide whether automatic Strength settlement should run at this boundary.

    The service may call this at every completed-action boundary. The policy keeps
    actual settlements sparse: bootstrap once, immediately settle newly eligible
    recovered stimulus, otherwise checkpoint pure detraining at most once per
    configured simulated-time interval and only when Strength-training history exists.
    """
    checkpoint_hours = float(detraining_checkpoint_hours)
    if checkpoint_hours <= 0.0:
        raise ValueError("detraining_checkpoint_hours must be positive")
    multiplier = float(recovery_multiplier)
    if multiplier < 0.0:
        raise ValueError("recovery_multiplier must be non-negative")

    as_of = _dt(as_of_sim_time)
    last_settled, consumed = _settlement_state(conn, actor_id)
    stimulus = _strength_stimulus_events(conn, actor_id, as_of_sim_time)

    if last_settled is None:
        return StrengthProgressionDue(True, "bootstrap", None, (), None)

    last_dt = _dt(last_settled)
    if as_of <= last_dt:
        return StrengthProgressionDue(False, "same_or_older_boundary", last_settled, (), 0.0)

    state_quality, _ = recovery_state_quality(state)
    recovery_allowed = float(state["fatigue"]) < FATIGUE_HARD_BLOCK and state_quality * multiplier > 0.0
    eligible: list[int] = []
    if recovery_allowed:
        for event_id, sim_time in stimulus:
            if event_id in consumed:
                continue
            age_hours = max(0.0, (as_of - _dt(sim_time)).total_seconds() / 3600.0)
            if age_hours >= FULL_RECOVERY_HOURS:
                eligible.append(event_id)
    if eligible:
        return StrengthProgressionDue(
            True,
            "eligible_stimulus",
            last_settled,
            tuple(eligible),
            round((as_of - last_dt).total_seconds() / 3600.0, 6),
        )

    elapsed_hours = max(0.0, (as_of - last_dt).total_seconds() / 3600.0)
    if stimulus and elapsed_hours >= checkpoint_hours:
        return StrengthProgressionDue(
            True,
            "detraining_checkpoint",
            last_settled,
            (),
            round(elapsed_hours, 6),
        )

    return StrengthProgressionDue(
        False,
        "not_due",
        last_settled,
        (),
        round(elapsed_hours, 6),
    )


def maybe_settle_strength_progression(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    due = strength_progression_due(
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
    settlement = settle_strength_progression(
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

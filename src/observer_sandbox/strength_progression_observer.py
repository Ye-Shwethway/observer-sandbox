from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Any

from .adaptation_curve import strength_level_factor
from .detraining_decay import strength_detraining_decay_evidence
from .recovery_realization import FULL_RECOVERY_HOURS, strength_recovery_realization_evidence
from .stimulus_saturation import strength_stimulus_saturation_evidence
from .strength_progression import SETTLEMENT_EVENT_TYPE
from .strength_progression_activation import DETRAINING_CHECKPOINT_HOURS, strength_progression_due


def _dt(raw: str) -> datetime:
    return datetime.fromisoformat(raw)


def _fmt_time(raw: str | None) -> str:
    if not raw:
        return "—"
    return _dt(raw).strftime("%d-%m-%Y %H:%M")


def _strength_value(conn: sqlite3.Connection, actor_id: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key='raps_pa.strength'",
        (actor_id,),
    ).fetchone()
    if row is None:
        raise KeyError(f"Missing Strength for {actor_id}")
    return float(json.loads(row["value_json"]))


def _settlements(conn: sqlite3.Connection, actor_id: str) -> tuple[dict[str, Any] | None, set[int]]:
    latest: tuple[datetime, dict[str, Any]] | None = None
    consumed: set[int] = set()
    rows = conn.execute(
        "SELECT sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (actor_id, SETTLEMENT_EVENT_TYPE),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        raw = payload.get("settled_through_sim_time") or row["sim_time"]
        if isinstance(raw, str):
            parsed = _dt(raw)
            view = {"sim_time": raw, **payload}
            if latest is None or parsed > latest[0]:
                latest = (parsed, view)
        for event_id in payload.get("consumed_stimulus_event_ids") or []:
            if isinstance(event_id, int):
                consumed.add(event_id)
    return (None if latest is None else latest[1], consumed)


def _stimulus_events(conn: sqlite3.Connection, actor_id: str, as_of_sim_time: str) -> list[dict[str, Any]]:
    as_of = _dt(as_of_sim_time)
    found: list[dict[str, Any]] = []
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed'",
        (actor_id,),
    ).fetchall()
    for row in rows:
        when = _dt(row["sim_time"])
        if when > as_of:
            continue
        payload = json.loads(row["payload_json"] or "{}")
        evidence = payload.get("training_stimulus")
        if not isinstance(evidence, dict) or evidence.get("domain") != "strength":
            continue
        units = evidence.get("stimulus_units")
        if isinstance(units, (int, float)) and float(units) > 0:
            found.append({"id": int(row["id"]), "sim_time": row["sim_time"], "units": float(units)})
    found.sort(key=lambda item: (_dt(item["sim_time"]), item["id"]))
    return found


def strength_progression_observation(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    state: dict[str, Any],
) -> dict[str, Any]:
    as_of_sim_time = str(state["sim_time"])
    as_of = _dt(as_of_sim_time)
    strength = _strength_value(conn, actor_id)
    level = strength_level_factor(strength)
    saturation = strength_stimulus_saturation_evidence(conn, actor_id, as_of_sim_time=as_of_sim_time)
    recovery = strength_recovery_realization_evidence(
        conn, actor_id, as_of_sim_time=as_of_sim_time, state=state
    )
    detraining = strength_detraining_decay_evidence(
        conn, actor_id, as_of_sim_time=as_of_sim_time, current_strength=strength
    )
    due = strength_progression_due(
        conn, actor_id, as_of_sim_time=as_of_sim_time, state=state
    )
    latest_settlement, consumed = _settlements(conn, actor_id)
    stimulus = _stimulus_events(conn, actor_id, as_of_sim_time)
    unconsumed = [item for item in stimulus if item["id"] not in consumed]

    if recovery.latest_stimulus_sim_time is None:
        adaptation_status = "No Strength stimulus yet"
    elif recovery.blocked:
        adaptation_status = "Blocked by systemic fatigue"
    elif recovery.elapsed_hours < FULL_RECOVERY_HOURS:
        adaptation_status = f"Recovering · {recovery.elapsed_hours:.1f}/{FULL_RECOVERY_HOURS:.0f} h"
    elif unconsumed:
        adaptation_status = "Eligible at next action boundary"
    else:
        adaptation_status = "No unconsumed eligible stimulus"

    latest_delta = 0.0
    latest_settlement_time = None
    if latest_settlement:
        latest_delta = float(latest_settlement.get("net_delta") or 0.0)
        latest_settlement_time = str(latest_settlement.get("settled_through_sim_time") or latest_settlement.get("sim_time"))

    if detraining.last_strength_stimulus_sim_time is None:
        detraining_status = "No Strength-training history"
    elif detraining.eligible:
        detraining_status = f"Active · pressure {detraining.decay_pressure * 100:.2f}%"
    else:
        remaining = max(0.0, detraining.grace_days - detraining.untrained_days)
        detraining_status = f"Grace · {remaining:.1f} d remaining"

    boundaries: list[datetime] = []
    for item in unconsumed:
        boundary = _dt(item["sim_time"]) + timedelta(hours=FULL_RECOVERY_HOURS)
        if boundary > as_of:
            boundaries.append(boundary)
    if latest_settlement_time and stimulus:
        checkpoint = _dt(latest_settlement_time) + timedelta(hours=DETRAINING_CHECKPOINT_HOURS)
        if checkpoint > as_of:
            boundaries.append(checkpoint)

    if due.due:
        next_boundary = f"Next action boundary · {due.reason.replace('_', ' ')}"
    elif boundaries:
        next_boundary = min(boundaries).strftime("%d-%m-%Y %H:%M")
    elif stimulus:
        next_boundary = "Next 24 h detraining checkpoint"
    else:
        next_boundary = "After first Strength stimulus"

    return {
        "strength": round(strength, 6),
        "recent_stimulus_units": saturation.recent_stimulus_units,
        "level_factor": level.level_factor,
        "saturation_factor": saturation.saturation_factor,
        "recovery_factor": recovery.recovery_factor,
        "recovery_elapsed_hours": recovery.elapsed_hours,
        "latest_stimulus_time": recovery.latest_stimulus_sim_time,
        "adaptation_status": adaptation_status,
        "latest_settlement_delta": round(latest_delta, 9),
        "latest_settlement_time": latest_settlement_time,
        "detraining_status": detraining_status,
        "next_boundary": next_boundary,
        "due_reason": due.reason,
    }


def strength_progression_profile_items(conn: sqlite3.Connection, actor_id: str, *, state: dict[str, Any]) -> list[dict[str, Any]]:
    obs = strength_progression_observation(conn, actor_id, state=state)
    latest_settlement = (
        f"{obs['latest_settlement_delta']:+.6f} · {_fmt_time(obs['latest_settlement_time'])}"
        if obs["latest_settlement_time"] else "No settlement yet"
    )
    return [
        {"kind": "derived", "field_key": "strength.progression.raw", "domain": "progression", "label": "Strength raw", "value": f"{obs['strength']:.6f}", "mode": "derived"},
        {"kind": "derived", "field_key": "strength.progression.stimulus", "domain": "progression", "label": "Recent Strength stimulus", "value": f"{obs['recent_stimulus_units']:.3f} units / 72 h", "mode": "derived"},
        {"kind": "derived", "field_key": "strength.progression.level_factor", "domain": "progression", "label": "Level gain factor", "value": f"{obs['level_factor'] * 100:.3f}%", "mode": "derived"},
        {"kind": "derived", "field_key": "strength.progression.saturation", "domain": "progression", "label": "Saturation yield", "value": f"{obs['saturation_factor'] * 100:.1f}%", "mode": "derived"},
        {"kind": "derived", "field_key": "strength.progression.recovery", "domain": "progression", "label": "Recovery realization", "value": f"{obs['recovery_factor'] * 100:.1f}%", "mode": "derived"},
        {"kind": "derived", "field_key": "strength.progression.status", "domain": "progression", "label": "Adaptation status", "value": obs["adaptation_status"], "mode": "derived"},
        {"kind": "derived", "field_key": "strength.progression.settlement", "domain": "progression", "label": "Latest settlement", "value": latest_settlement, "mode": "derived"},
        {"kind": "derived", "field_key": "strength.progression.detraining", "domain": "progression", "label": "Detraining", "value": obs["detraining_status"], "mode": "derived"},
        {"kind": "derived", "field_key": "strength.progression.next", "domain": "progression", "label": "Next progression boundary", "value": obs["next_boundary"], "mode": "derived"},
    ]

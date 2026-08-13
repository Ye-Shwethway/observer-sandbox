from __future__ import annotations

import json
import math
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .adaptation_curve import strength_level_factor
from .detraining_decay import (
    DEFAULT_GRACE_DAYS,
    DEFAULT_TIME_CONSTANT_DAYS,
    detraining_level_exposure,
)
from .event_log import record_event
from .recovery_realization import FATIGUE_HARD_BLOCK, FULL_RECOVERY_HOURS, recovery_state_quality
from .stimulus_saturation import recent_strength_stimulus_units, saturation_factor


SETTLEMENT_EVENT_TYPE = "strength_progression_settled"
SETTLEMENT_SOURCE = "strength-progression-settlement-v1"
STRENGTH_FIELD_KEY = "raps_pa.strength"
BASE_POSITIVE_SCALE = 0.25
BASE_DETRAINING_POINTS_PER_DAY = 0.02
MAX_RAW_STRENGTH = 100.0


@dataclass(frozen=True)
class StrengthStimulusEvent:
    event_id: int
    sim_time: str
    stimulus_units: float


def _dt(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _strength_events(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
) -> list[StrengthStimulusEvent]:
    as_of = _dt(as_of_sim_time)
    rows = conn.execute(
        """
        SELECT id,sim_time,payload_json
        FROM events
        WHERE actor_id=? AND event_type='action_completed'
        """,
        (actor_id,),
    ).fetchall()
    events: list[StrengthStimulusEvent] = []
    for row in rows:
        event_time = _dt(row["sim_time"])
        if event_time > as_of:
            continue
        payload = json.loads(row["payload_json"] or "{}")
        evidence = payload.get("training_stimulus")
        if not isinstance(evidence, dict) or evidence.get("domain") != "strength":
            continue
        units = evidence.get("stimulus_units")
        if not isinstance(units, (int, float)) or float(units) <= 0.0:
            continue
        events.append(StrengthStimulusEvent(int(row["id"]), row["sim_time"], float(units)))
    events.sort(key=lambda item: (_dt(item.sim_time), item.event_id))
    return events


def _settlement_rows(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (actor_id, SETTLEMENT_EVENT_TYPE),
    ).fetchall()


def _consumed_stimulus_ids(conn: sqlite3.Connection, actor_id: str) -> set[int]:
    consumed: set[int] = set()
    for row in _settlement_rows(conn, actor_id):
        payload = json.loads(row["payload_json"] or "{}")
        for value in payload.get("consumed_stimulus_event_ids") or []:
            if isinstance(value, int):
                consumed.add(value)
    return consumed


def _latest_settled_through(conn: sqlite3.Connection, actor_id: str) -> str | None:
    latest: tuple[datetime, str] | None = None
    for row in _settlement_rows(conn, actor_id):
        payload = json.loads(row["payload_json"] or "{}")
        raw = payload.get("settled_through_sim_time") or row["sim_time"]
        if not isinstance(raw, str):
            continue
        parsed = _dt(raw)
        if latest is None or parsed > latest[0]:
            latest = (parsed, raw)
    return None if latest is None else latest[1]


def _read_strength_row(conn: sqlite3.Connection, actor_id: str) -> sqlite3.Row:
    row = conn.execute(
        "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, STRENGTH_FIELD_KEY),
    ).fetchone()
    if row is None:
        raise KeyError(f"Missing Strength profile value for {actor_id}")
    return row


def _integral_time_factor_days(
    start_age_days: float,
    end_age_days: float,
    *,
    grace_days: float = DEFAULT_GRACE_DAYS,
    time_constant_days: float = DEFAULT_TIME_CONSTANT_DAYS,
) -> float:
    if end_age_days <= start_age_days:
        return 0.0
    u1 = max(0.0, float(start_age_days) - float(grace_days))
    u2 = max(0.0, float(end_age_days) - float(grace_days))
    if u2 <= u1:
        return 0.0
    tau = float(time_constant_days)
    return max(0.0, (u2 - u1) + tau * (math.exp(-u2 / tau) - math.exp(-u1 / tau)))


def integrated_detraining_time_factor_days(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    start_sim_time: str,
    end_sim_time: str,
) -> float:
    """Integrate detraining time pressure exactly across one settlement interval.

    Strength stimulus events inside the interval reset the untrained clock. If no
    prior Strength stimulus exists, no detraining interval is invented.
    """
    start = _dt(start_sim_time)
    end = _dt(end_sim_time)
    if end <= start:
        return 0.0
    events = _strength_events(conn, actor_id, as_of_sim_time=end_sim_time)
    previous = [event for event in events if _dt(event.sim_time) <= start]
    last_training = _dt(previous[-1].sim_time) if previous else None
    interval_events = [event for event in events if start < _dt(event.sim_time) <= end]

    total = 0.0
    segment_start = start
    for event in interval_events:
        event_time = _dt(event.sim_time)
        if last_training is not None and event_time > segment_start:
            age_start = max(0.0, (segment_start - last_training).total_seconds() / 86400.0)
            age_end = max(0.0, (event_time - last_training).total_seconds() / 86400.0)
            total += _integral_time_factor_days(age_start, age_end)
        last_training = event_time
        segment_start = event_time

    if last_training is not None and end > segment_start:
        age_start = max(0.0, (segment_start - last_training).total_seconds() / 86400.0)
        age_end = max(0.0, (end - last_training).total_seconds() / 86400.0)
        total += _integral_time_factor_days(age_start, age_end)
    return round(total, 9)


def _write_strength(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    old_value: float,
    new_value: float,
    sim_time: str,
    reason: str,
) -> None:
    value_json = json.dumps(round(float(new_value), 6))
    conn.execute(
        """
        UPDATE character_profile_values
        SET value_json=?, mode='simulated', authority=?, source=?, observed_at=?, updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND field_key=?
        """,
        (value_json, SETTLEMENT_SOURCE, SETTLEMENT_SOURCE, sim_time, actor_id, STRENGTH_FIELD_KEY),
    )
    conn.execute(
        """
        INSERT INTO character_profile_history(
            entity_id,field_key,old_value_json,new_value_json,mode,authority,reason,sim_time
        ) VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            actor_id,
            STRENGTH_FIELD_KEY,
            json.dumps(round(float(old_value), 6)),
            value_json,
            "simulated",
            SETTLEMENT_SOURCE,
            reason,
            sim_time,
        ),
    )


def settle_strength_progression(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
    adaptation_rate_multiplier: float = 1.0,
    recovery_multiplier: float = 1.0,
    detraining_multiplier: float = 1.0,
    decay_rate_multiplier: float = 1.0,
) -> dict[str, Any]:
    """Settle Strength progression exactly once per evidence/time boundary.

    First invocation is a non-mutating bootstrap. It marks existing historical
    Strength stimulus evidence consumed and establishes the settlement cursor so
    deployment cannot retroactively alter the character.

    Subsequent invocations:
    * consume only previously-unconsumed Strength stimulus events at least 48 sim
      hours old and only when systemic fatigue is below the hard block;
    * integrate detraining across the unsettled interval with training resets;
    * write at most one tiny decimal Strength update plus one audit settlement event.
    """
    adaptation_rate_multiplier = float(adaptation_rate_multiplier)
    recovery_multiplier = float(recovery_multiplier)
    detraining_multiplier = float(detraining_multiplier)
    decay_rate_multiplier = float(decay_rate_multiplier)
    if min(adaptation_rate_multiplier, recovery_multiplier, detraining_multiplier, decay_rate_multiplier) < 0.0:
        raise ValueError("progression multipliers must be non-negative")

    as_of = _dt(as_of_sim_time)
    strength_row = _read_strength_row(conn, actor_id)
    old_strength = float(json.loads(strength_row["value_json"]))
    all_stimulus = _strength_events(conn, actor_id, as_of_sim_time=as_of_sim_time)
    last_settled = _latest_settled_through(conn, actor_id)

    if last_settled is None:
        consumed = [event.event_id for event in all_stimulus]
        event_id = record_event(
            conn,
            sim_time=as_of_sim_time,
            actor_id=actor_id,
            event_type=SETTLEMENT_EVENT_TYPE,
            payload={
                "source": SETTLEMENT_SOURCE,
                "bootstrap": True,
                "settled_through_sim_time": as_of_sim_time,
                "consumed_stimulus_event_ids": consumed,
                "old_strength": round(old_strength, 6),
                "new_strength": round(old_strength, 6),
                "positive_delta": 0.0,
                "negative_delta": 0.0,
                "net_delta": 0.0,
            },
        )
        conn.commit()
        return {
            "status": "bootstrapped",
            "event_id": event_id,
            "old_strength": round(old_strength, 6),
            "new_strength": round(old_strength, 6),
            "positive_delta": 0.0,
            "negative_delta": 0.0,
            "net_delta": 0.0,
            "consumed_stimulus_event_ids": consumed,
            "settled_through_sim_time": as_of_sim_time,
        }

    last_dt = _dt(last_settled)
    if as_of < last_dt:
        raise ValueError("cannot settle Strength progression before the latest settlement cursor")
    if as_of == last_dt:
        return {
            "status": "no_change",
            "old_strength": round(old_strength, 6),
            "new_strength": round(old_strength, 6),
            "positive_delta": 0.0,
            "negative_delta": 0.0,
            "net_delta": 0.0,
            "consumed_stimulus_event_ids": [],
            "settled_through_sim_time": last_settled,
        }

    consumed_ids = _consumed_stimulus_ids(conn, actor_id)
    state_quality, recovery_components = recovery_state_quality(state)
    fatigue_blocked = float(state["fatigue"]) >= FATIGUE_HARD_BLOCK
    current_strength = old_strength
    positive_delta = 0.0
    newly_consumed: list[int] = []
    positive_evidence: list[dict[str, Any]] = []

    for event in all_stimulus:
        if event.event_id in consumed_ids:
            continue
        age_hours = max(0.0, (as_of - _dt(event.sim_time)).total_seconds() / 3600.0)
        if age_hours < FULL_RECOVERY_HOURS or fatigue_blocked:
            continue
        recovery_factor = max(0.0, min(1.0, state_quality * recovery_multiplier))
        if recovery_factor <= 0.0:
            continue
        level = strength_level_factor(current_strength)
        recent_at_event = recent_strength_stimulus_units(
            conn,
            actor_id,
            as_of_sim_time=event.sim_time,
        )
        saturation = saturation_factor(recent_at_event)
        gain = (
            BASE_POSITIVE_SCALE
            * event.stimulus_units
            * level.level_factor
            * saturation
            * recovery_factor
            * adaptation_rate_multiplier
        )
        gain = max(0.0, gain)
        next_strength = min(MAX_RAW_STRENGTH, current_strength + gain)
        realized = max(0.0, next_strength - current_strength)
        positive_delta += realized
        current_strength = next_strength
        newly_consumed.append(event.event_id)
        positive_evidence.append(
            {
                "stimulus_event_id": event.event_id,
                "stimulus_sim_time": event.sim_time,
                "stimulus_units": round(event.stimulus_units, 6),
                "age_hours": round(age_hours, 6),
                "recent_stimulus_at_event": round(recent_at_event, 6),
                "level_factor": level.level_factor,
                "saturation_factor": round(saturation, 9),
                "recovery_factor": round(recovery_factor, 9),
                "realized_delta": round(realized, 9),
            }
        )

    integrated_days = integrated_detraining_time_factor_days(
        conn,
        actor_id,
        start_sim_time=last_settled,
        end_sim_time=as_of_sim_time,
    )
    level_exposure = detraining_level_exposure(current_strength, effective_ceiling=MAX_RAW_STRENGTH)
    negative_delta = (
        BASE_DETRAINING_POINTS_PER_DAY
        * integrated_days
        * level_exposure
        * detraining_multiplier
        * decay_rate_multiplier
    )
    negative_delta = max(0.0, negative_delta)
    new_strength = max(0.0, min(MAX_RAW_STRENGTH, current_strength - negative_delta))
    realized_negative = max(0.0, current_strength - new_strength)
    net_delta = new_strength - old_strength

    changed = abs(net_delta) >= 0.0000005
    if changed:
        _write_strength(
            conn,
            actor_id,
            old_value=old_strength,
            new_value=new_strength,
            sim_time=as_of_sim_time,
            reason="Strength progression settlement v1",
        )

    event_id = record_event(
        conn,
        sim_time=as_of_sim_time,
        actor_id=actor_id,
        event_type=SETTLEMENT_EVENT_TYPE,
        state_changes={
            STRENGTH_FIELD_KEY: {
                "before": round(old_strength, 6),
                "after": round(new_strength, 6),
                "delta": round(net_delta, 9),
            }
        } if changed else {},
        payload={
            "source": SETTLEMENT_SOURCE,
            "bootstrap": False,
            "settled_from_sim_time": last_settled,
            "settled_through_sim_time": as_of_sim_time,
            "consumed_stimulus_event_ids": newly_consumed,
            "positive_evidence": positive_evidence,
            "recovery_components": recovery_components,
            "fatigue_blocked": fatigue_blocked,
            "integrated_detraining_time_factor_days": round(integrated_days, 9),
            "detraining_level_exposure": round(level_exposure, 9),
            "old_strength": round(old_strength, 6),
            "new_strength": round(new_strength, 6),
            "positive_delta": round(positive_delta, 9),
            "negative_delta": round(realized_negative, 9),
            "net_delta": round(net_delta, 9),
            "stat_mutated": changed,
        },
    )
    conn.commit()
    return {
        "status": "applied" if changed else "advanced",
        "event_id": event_id,
        "old_strength": round(old_strength, 6),
        "new_strength": round(new_strength, 6),
        "positive_delta": round(positive_delta, 9),
        "negative_delta": round(realized_negative, 9),
        "net_delta": round(net_delta, 9),
        "consumed_stimulus_event_ids": newly_consumed,
        "integrated_detraining_time_factor_days": round(integrated_days, 9),
        "settled_through_sim_time": as_of_sim_time,
    }

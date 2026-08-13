from __future__ import annotations

import json
import math
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

from .event_log import record_event
from .recovery_realization import FATIGUE_HARD_BLOCK, recovery_state_quality


STAMINA_FIELD_KEY = "raps_pa.stamina"
STAMINA_METHOD_ID = "steady_state_cardio"
STAMINA_METHOD_IDS = frozenset({"steady_state_cardio", "rowing_conditioning", "altitude_conditioning"})
SETTLEMENT_EVENT_TYPE = "stamina_progression_settled"
SETTLEMENT_SOURCE = "stamina-progression-settlement-v1"
STIMULUS_SOURCE = "stamina-stimulus-conditioning-v1"

STIMULUS_MINUTES_PER_UNIT = 45.0
NATURAL_CEILING = 100.0
LEVEL_EXPONENT = 1.5
BASE_POSITIVE_SCALE = 0.18
SATURATION_WINDOW_HOURS = 96.0
SATURATION_COEFFICIENT = 0.20
FULL_RECOVERY_HOURS = 30.0
DETRAINING_GRACE_DAYS = 10.0
DETRAINING_TIME_CONSTANT_DAYS = 45.0
DETRAINING_LEVEL_EXPONENT = 1.5
BASE_DETRAINING_POINTS_PER_DAY = 0.015
MAX_RAW_STAMINA = 100.0


@dataclass(frozen=True)
class StaminaStimulusEvent:
    event_id: int
    sim_time: str
    stimulus_units: float
    effective_minutes: float


def _dt(raw: str) -> datetime:
    return datetime.fromisoformat(raw)


def stamina_level_factor(current_value: float | int) -> float:
    current = max(0.0, float(current_value))
    remaining = max(0.0, min(1.0, (NATURAL_CEILING - current) / NATURAL_CEILING))
    return round(remaining**LEVEL_EXPONENT, 9)


def stamina_saturation_factor(recent_units: float | int) -> float:
    units = max(0.0, float(recent_units))
    return round(1.0 / (1.0 + SATURATION_COEFFICIENT * units), 9)


def _stimulus_from_payload(payload: dict[str, Any]) -> tuple[float, float] | None:
    method = payload.get("training_method")
    if not isinstance(method, dict) or method.get("method_id") not in STAMINA_METHOD_IDS:
        return None
    if method.get("source") != "training-method-semantics-v1":
        return None
    if method.get("workload_channels") != ["conditioning"]:
        return None
    effective_load = method.get("effective_load")
    if not isinstance(effective_load, dict):
        return None
    effective_minutes = effective_load.get("effective_minutes")
    if not isinstance(effective_minutes, (int, float)) or float(effective_minutes) <= 0.0:
        return None
    minutes = float(effective_minutes)
    return round(minutes / STIMULUS_MINUTES_PER_UNIT, 6), round(minutes, 6)


def stamina_stimulus_events(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
) -> list[StaminaStimulusEvent]:
    as_of = _dt(as_of_sim_time)
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed'",
        (actor_id,),
    ).fetchall()
    found: list[StaminaStimulusEvent] = []
    for row in rows:
        if _dt(row["sim_time"]) > as_of:
            continue
        payload = json.loads(row["payload_json"] or "{}")
        derived = _stimulus_from_payload(payload)
        if derived is None:
            continue
        units, minutes = derived
        if units > 0.0:
            found.append(StaminaStimulusEvent(int(row["id"]), row["sim_time"], units, minutes))
    found.sort(key=lambda item: (_dt(item.sim_time), item.event_id))
    return found


def recent_stamina_stimulus_units(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    window_hours: float = SATURATION_WINDOW_HOURS,
) -> float:
    as_of = _dt(as_of_sim_time)
    lower = as_of - timedelta(hours=float(window_hours))
    total = 0.0
    for event in stamina_stimulus_events(conn, actor_id, as_of_sim_time=as_of_sim_time):
        when = _dt(event.sim_time)
        if lower <= when <= as_of:
            total += event.stimulus_units
    return round(total, 6)


def _settlement_rows(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (actor_id, SETTLEMENT_EVENT_TYPE),
    ).fetchall()


def _consumed_ids(conn: sqlite3.Connection, actor_id: str) -> set[int]:
    consumed: set[int] = set()
    for row in _settlement_rows(conn, actor_id):
        payload = json.loads(row["payload_json"] or "{}")
        for event_id in payload.get("consumed_stimulus_event_ids") or []:
            if isinstance(event_id, int):
                consumed.add(event_id)
    return consumed


def latest_stamina_settlement_time(conn: sqlite3.Connection, actor_id: str) -> str | None:
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


def _read_stamina(conn: sqlite3.Connection, actor_id: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, STAMINA_FIELD_KEY),
    ).fetchone()
    if row is None:
        raise KeyError(f"Missing Stamina profile value for {actor_id}")
    return float(json.loads(row["value_json"]))


def _write_stamina(
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
        """UPDATE character_profile_values
        SET value_json=?,mode='simulated',authority=?,source=?,observed_at=?,updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND field_key=?""",
        (value_json, SETTLEMENT_SOURCE, SETTLEMENT_SOURCE, sim_time, actor_id, STAMINA_FIELD_KEY),
    )
    conn.execute(
        """INSERT INTO character_profile_history(
        entity_id,field_key,old_value_json,new_value_json,mode,authority,reason,sim_time
        ) VALUES(?,?,?,?,?,?,?,?)""",
        (
            actor_id,
            STAMINA_FIELD_KEY,
            json.dumps(round(float(old_value), 6)),
            value_json,
            "simulated",
            SETTLEMENT_SOURCE,
            reason,
            sim_time,
        ),
    )


def _integral_detraining_time_days(start_age_days: float, end_age_days: float) -> float:
    if end_age_days <= start_age_days:
        return 0.0
    u1 = max(0.0, float(start_age_days) - DETRAINING_GRACE_DAYS)
    u2 = max(0.0, float(end_age_days) - DETRAINING_GRACE_DAYS)
    if u2 <= u1:
        return 0.0
    tau = DETRAINING_TIME_CONSTANT_DAYS
    return max(0.0, (u2 - u1) + tau * (math.exp(-u2 / tau) - math.exp(-u1 / tau)))


def integrated_stamina_detraining_days(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    start_sim_time: str,
    end_sim_time: str,
) -> float:
    start = _dt(start_sim_time)
    end = _dt(end_sim_time)
    if end <= start:
        return 0.0
    events = stamina_stimulus_events(conn, actor_id, as_of_sim_time=end_sim_time)
    previous = [event for event in events if _dt(event.sim_time) <= start]
    last_training = _dt(previous[-1].sim_time) if previous else None
    interval_events = [event for event in events if start < _dt(event.sim_time) <= end]

    total = 0.0
    segment_start = start
    for event in interval_events:
        event_time = _dt(event.sim_time)
        if last_training is not None and event_time > segment_start:
            total += _integral_detraining_time_days(
                max(0.0, (segment_start - last_training).total_seconds() / 86400.0),
                max(0.0, (event_time - last_training).total_seconds() / 86400.0),
            )
        last_training = event_time
        segment_start = event_time
    if last_training is not None and end > segment_start:
        total += _integral_detraining_time_days(
            max(0.0, (segment_start - last_training).total_seconds() / 86400.0),
            max(0.0, (end - last_training).total_seconds() / 86400.0),
        )
    return round(total, 9)


def settle_stamina_progression(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    as_of = _dt(as_of_sim_time)
    old_stamina = _read_stamina(conn, actor_id)
    stimuli = stamina_stimulus_events(conn, actor_id, as_of_sim_time=as_of_sim_time)
    last_settled = latest_stamina_settlement_time(conn, actor_id)

    if last_settled is None:
        consumed = [event.event_id for event in stimuli]
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
                "old_stamina": round(old_stamina, 6),
                "new_stamina": round(old_stamina, 6),
                "positive_delta": 0.0,
                "negative_delta": 0.0,
                "net_delta": 0.0,
            },
        )
        conn.commit()
        return {"status": "bootstrapped", "event_id": event_id, "old_stamina": round(old_stamina, 6), "new_stamina": round(old_stamina, 6), "net_delta": 0.0, "consumed_stimulus_event_ids": consumed, "settled_through_sim_time": as_of_sim_time}

    last_dt = _dt(last_settled)
    if as_of < last_dt:
        raise ValueError("cannot settle Stamina progression before the latest settlement cursor")
    if as_of == last_dt:
        return {"status": "no_change", "old_stamina": round(old_stamina, 6), "new_stamina": round(old_stamina, 6), "net_delta": 0.0, "consumed_stimulus_event_ids": [], "settled_through_sim_time": last_settled}

    consumed = _consumed_ids(conn, actor_id)
    state_quality, recovery_components = recovery_state_quality(state)
    fatigue_blocked = float(state["fatigue"]) >= FATIGUE_HARD_BLOCK
    current = old_stamina
    positive_delta = 0.0
    newly_consumed: list[int] = []
    positive_evidence: list[dict[str, Any]] = []

    for event in stimuli:
        if event.event_id in consumed:
            continue
        age_hours = max(0.0, (as_of - _dt(event.sim_time)).total_seconds() / 3600.0)
        if age_hours < FULL_RECOVERY_HOURS or fatigue_blocked or state_quality <= 0.0:
            continue
        level = stamina_level_factor(current)
        recent_units = recent_stamina_stimulus_units(conn, actor_id, as_of_sim_time=event.sim_time)
        saturation = stamina_saturation_factor(recent_units)
        gain = max(0.0, BASE_POSITIVE_SCALE * event.stimulus_units * level * saturation * state_quality)
        current = min(MAX_RAW_STAMINA, current + gain)
        positive_delta += gain
        newly_consumed.append(event.event_id)
        positive_evidence.append({
            "event_id": event.event_id,
            "stimulus_source": STIMULUS_SOURCE,
            "stimulus_units": event.stimulus_units,
            "effective_minutes": event.effective_minutes,
            "age_hours": round(age_hours, 6),
            "level_factor": level,
            "recent_stimulus_units": recent_units,
            "saturation_factor": saturation,
            "recovery_state_quality": state_quality,
            "gain": round(gain, 9),
        })

    integrated_days = integrated_stamina_detraining_days(
        conn,
        actor_id,
        start_sim_time=last_settled,
        end_sim_time=as_of_sim_time,
    )
    level_exposure = max(0.0, min(1.0, current / NATURAL_CEILING)) ** DETRAINING_LEVEL_EXPONENT
    negative_delta = max(0.0, BASE_DETRAINING_POINTS_PER_DAY * integrated_days * level_exposure)
    current = max(0.0, current - negative_delta)
    net_delta = current - old_stamina

    if abs(net_delta) >= 0.0000005:
        _write_stamina(
            conn,
            actor_id,
            old_value=old_stamina,
            new_value=current,
            sim_time=as_of_sim_time,
            reason="Stamina progression settlement from authored conditioning evidence",
        )

    event_id = record_event(
        conn,
        sim_time=as_of_sim_time,
        actor_id=actor_id,
        event_type=SETTLEMENT_EVENT_TYPE,
        payload={
            "source": SETTLEMENT_SOURCE,
            "bootstrap": False,
            "settled_through_sim_time": as_of_sim_time,
            "consumed_stimulus_event_ids": newly_consumed,
            "old_stamina": round(old_stamina, 6),
            "new_stamina": round(current, 6),
            "positive_delta": round(positive_delta, 9),
            "negative_delta": round(negative_delta, 9),
            "net_delta": round(net_delta, 9),
            "full_recovery_hours": FULL_RECOVERY_HOURS,
            "fatigue_blocked": fatigue_blocked,
            "recovery_components": recovery_components,
            "integrated_detraining_days": integrated_days,
            "positive_evidence": positive_evidence,
        },
    )
    conn.commit()
    return {
        "status": "settled",
        "event_id": event_id,
        "old_stamina": round(old_stamina, 6),
        "new_stamina": round(current, 6),
        "positive_delta": round(positive_delta, 9),
        "negative_delta": round(negative_delta, 9),
        "net_delta": round(net_delta, 9),
        "consumed_stimulus_event_ids": newly_consumed,
        "settled_through_sim_time": as_of_sim_time,
    }

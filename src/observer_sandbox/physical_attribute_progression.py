from __future__ import annotations

import json
import math
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any

from .event_log import record_event
from .recovery_realization import FATIGUE_HARD_BLOCK, recovery_state_quality


REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "config" / "physical_attribute_progression.v1.json"


@dataclass(frozen=True)
class PhysicalAttributePolicy:
    attribute_key: str
    field_key: str
    method_weights: dict[str, float]
    stimulus_minutes_per_unit: float
    natural_ceiling: float
    level_exponent: float
    base_positive_scale: float
    saturation_window_hours: float
    saturation_coefficient: float
    full_recovery_hours: float
    detraining_grace_days: float
    detraining_time_constant_days: float
    detraining_level_exponent: float
    base_detraining_points_per_day: float
    settlement_event_type: str
    framework_source: str
    detraining_checkpoint_hours: float


@dataclass(frozen=True)
class PhysicalAttributeStimulusEvent:
    event_id: int
    sim_time: str
    method_id: str
    effective_minutes: float
    stimulus_units: float


@dataclass(frozen=True)
class PhysicalAttributeProgressionDue:
    due: bool
    reason: str
    last_settled_sim_time: str | None
    eligible_stimulus_event_ids: tuple[int, ...]
    hours_since_settlement: float | None


def _dt(raw: str) -> datetime:
    return datetime.fromisoformat(raw)


@lru_cache(maxsize=1)
def load_physical_attribute_policy_catalog(path: str | Path = POLICY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def physical_attribute_keys() -> tuple[str, ...]:
    source = load_physical_attribute_policy_catalog()
    attributes = source.get("attributes", {})
    if not isinstance(attributes, dict):
        return ()
    return tuple(str(key) for key in attributes)


def physical_attribute_policy(attribute_key: str) -> PhysicalAttributePolicy:
    source = load_physical_attribute_policy_catalog()
    raw = source.get("attributes", {}).get(attribute_key)
    if not isinstance(raw, dict):
        raise KeyError(f"Unknown physical attribute progression policy: {attribute_key}")
    weights = raw.get("method_weights")
    if not isinstance(weights, dict) or not weights:
        raise ValueError(f"Physical attribute policy {attribute_key} has no eligible methods")
    method_weights = {str(key): float(value) for key, value in weights.items()}
    if any(value <= 0.0 for value in method_weights.values()):
        raise ValueError(f"Physical attribute policy {attribute_key} has a non-positive method weight")
    policy = PhysicalAttributePolicy(
        attribute_key=str(attribute_key),
        field_key=str(raw["field_key"]),
        method_weights=method_weights,
        stimulus_minutes_per_unit=float(raw["stimulus_minutes_per_unit"]),
        natural_ceiling=float(raw.get("natural_ceiling", 100.0)),
        level_exponent=float(raw["level_exponent"]),
        base_positive_scale=float(raw["base_positive_scale"]),
        saturation_window_hours=float(raw["saturation_window_hours"]),
        saturation_coefficient=float(raw["saturation_coefficient"]),
        full_recovery_hours=float(raw["full_recovery_hours"]),
        detraining_grace_days=float(raw["detraining_grace_days"]),
        detraining_time_constant_days=float(raw["detraining_time_constant_days"]),
        detraining_level_exponent=float(raw["detraining_level_exponent"]),
        base_detraining_points_per_day=float(raw["base_detraining_points_per_day"]),
        settlement_event_type=str(source.get("settlement_event_type", "physical_attribute_progression_settled")),
        framework_source=str(source.get("framework_source", "physical-attribute-progression-framework-v1")),
        detraining_checkpoint_hours=float(source.get("detraining_checkpoint_hours", 24.0)),
    )
    numeric = (
        policy.stimulus_minutes_per_unit,
        policy.natural_ceiling,
        policy.level_exponent,
        policy.base_positive_scale,
        policy.saturation_window_hours,
        policy.saturation_coefficient,
        policy.full_recovery_hours,
        policy.detraining_grace_days,
        policy.detraining_time_constant_days,
        policy.detraining_level_exponent,
        policy.base_detraining_points_per_day,
        policy.detraining_checkpoint_hours,
    )
    if any(value <= 0.0 for value in numeric):
        raise ValueError(f"Physical attribute policy {attribute_key} contains a non-positive parameter")
    return policy


def _stimulus_from_payload(payload: dict[str, Any], policy: PhysicalAttributePolicy) -> tuple[str, float, float] | None:
    method = payload.get("training_method")
    if not isinstance(method, dict) or method.get("source") != "training-method-semantics-v1":
        return None
    method_id = method.get("method_id")
    if not isinstance(method_id, str) or method_id not in policy.method_weights:
        return None
    effective_load = method.get("effective_load")
    if not isinstance(effective_load, dict):
        return None
    effective_minutes = effective_load.get("effective_minutes")
    if not isinstance(effective_minutes, (int, float)) or float(effective_minutes) <= 0.0:
        return None
    minutes = float(effective_minutes)
    units = minutes / policy.stimulus_minutes_per_unit * policy.method_weights[method_id]
    if units <= 0.0:
        return None
    return method_id, round(minutes, 6), round(units, 6)


def physical_attribute_stimulus_events(
    conn: sqlite3.Connection,
    actor_id: str,
    attribute_key: str,
    *,
    as_of_sim_time: str,
) -> list[PhysicalAttributeStimulusEvent]:
    policy = physical_attribute_policy(attribute_key)
    as_of = _dt(as_of_sim_time)
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed'",
        (actor_id,),
    ).fetchall()
    found: list[PhysicalAttributeStimulusEvent] = []
    for row in rows:
        if _dt(row["sim_time"]) > as_of:
            continue
        payload = json.loads(row["payload_json"] or "{}")
        derived = _stimulus_from_payload(payload, policy)
        if derived is None:
            continue
        method_id, effective_minutes, units = derived
        found.append(
            PhysicalAttributeStimulusEvent(
                event_id=int(row["id"]),
                sim_time=str(row["sim_time"]),
                method_id=method_id,
                effective_minutes=effective_minutes,
                stimulus_units=units,
            )
        )
    found.sort(key=lambda item: (_dt(item.sim_time), item.event_id))
    return found


def recent_physical_attribute_stimulus_units(
    conn: sqlite3.Connection,
    actor_id: str,
    attribute_key: str,
    *,
    as_of_sim_time: str,
) -> float:
    policy = physical_attribute_policy(attribute_key)
    as_of = _dt(as_of_sim_time)
    lower = as_of - timedelta(hours=policy.saturation_window_hours)
    total = 0.0
    for event in physical_attribute_stimulus_events(
        conn,
        actor_id,
        attribute_key,
        as_of_sim_time=as_of_sim_time,
    ):
        when = _dt(event.sim_time)
        if lower <= when <= as_of:
            total += event.stimulus_units
    return round(total, 6)


def physical_attribute_level_factor(current_value: float | int, policy: PhysicalAttributePolicy) -> float:
    current = max(0.0, float(current_value))
    remaining = max(0.0, min(1.0, (policy.natural_ceiling - current) / policy.natural_ceiling))
    return round(remaining**policy.level_exponent, 9)


def physical_attribute_saturation_factor(recent_units: float | int, policy: PhysicalAttributePolicy) -> float:
    units = max(0.0, float(recent_units))
    return round(1.0 / (1.0 + policy.saturation_coefficient * units), 9)


def _settlement_rows(conn: sqlite3.Connection, actor_id: str, policy: PhysicalAttributePolicy) -> list[sqlite3.Row]:
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (actor_id, policy.settlement_event_type),
    ).fetchall()
    return [
        row
        for row in rows
        if json.loads(row["payload_json"] or "{}").get("attribute_key") == policy.attribute_key
    ]


def _consumed_ids(conn: sqlite3.Connection, actor_id: str, policy: PhysicalAttributePolicy) -> set[int]:
    consumed: set[int] = set()
    for row in _settlement_rows(conn, actor_id, policy):
        payload = json.loads(row["payload_json"] or "{}")
        for event_id in payload.get("consumed_stimulus_event_ids") or []:
            if isinstance(event_id, int):
                consumed.add(event_id)
    return consumed


def latest_physical_attribute_settlement_time(
    conn: sqlite3.Connection,
    actor_id: str,
    attribute_key: str,
) -> str | None:
    policy = physical_attribute_policy(attribute_key)
    latest: tuple[datetime, str] | None = None
    for row in _settlement_rows(conn, actor_id, policy):
        payload = json.loads(row["payload_json"] or "{}")
        raw = payload.get("settled_through_sim_time") or row["sim_time"]
        if not isinstance(raw, str):
            continue
        parsed = _dt(raw)
        if latest is None or parsed > latest[0]:
            latest = (parsed, raw)
    return None if latest is None else latest[1]


def _read_profile_value(conn: sqlite3.Connection, actor_id: str, field_key: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    if row is None:
        raise KeyError(f"Missing profile value {field_key} for {actor_id}")
    return float(json.loads(row["value_json"]))


def _write_profile_value(
    conn: sqlite3.Connection,
    actor_id: str,
    policy: PhysicalAttributePolicy,
    *,
    old_value: float,
    new_value: float,
    sim_time: str,
) -> None:
    value_json = json.dumps(round(float(new_value), 6))
    conn.execute(
        """UPDATE character_profile_values
        SET value_json=?,mode='simulated',authority=?,source=?,observed_at=?,updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND field_key=?""",
        (value_json, policy.framework_source, policy.framework_source, sim_time, actor_id, policy.field_key),
    )
    conn.execute(
        """INSERT INTO character_profile_history(
        entity_id,field_key,old_value_json,new_value_json,mode,authority,reason,sim_time
        ) VALUES(?,?,?,?,?,?,?,?)""",
        (
            actor_id,
            policy.field_key,
            json.dumps(round(float(old_value), 6)),
            value_json,
            "simulated",
            policy.framework_source,
            f"{policy.attribute_key} progression settlement via Physical Attribute Progression Framework v1",
            sim_time,
        ),
    )


def _integral_detraining_time_days(start_age_days: float, end_age_days: float, policy: PhysicalAttributePolicy) -> float:
    if end_age_days <= start_age_days:
        return 0.0
    u1 = max(0.0, float(start_age_days) - policy.detraining_grace_days)
    u2 = max(0.0, float(end_age_days) - policy.detraining_grace_days)
    if u2 <= u1:
        return 0.0
    tau = policy.detraining_time_constant_days
    return max(0.0, (u2 - u1) + tau * (math.exp(-u2 / tau) - math.exp(-u1 / tau)))


def integrated_physical_attribute_detraining_days(
    conn: sqlite3.Connection,
    actor_id: str,
    attribute_key: str,
    *,
    start_sim_time: str,
    end_sim_time: str,
) -> float:
    policy = physical_attribute_policy(attribute_key)
    start = _dt(start_sim_time)
    end = _dt(end_sim_time)
    if end <= start:
        return 0.0
    events = physical_attribute_stimulus_events(
        conn,
        actor_id,
        attribute_key,
        as_of_sim_time=end_sim_time,
    )
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
                policy,
            )
        last_training = event_time
        segment_start = event_time
    if last_training is not None and end > segment_start:
        total += _integral_detraining_time_days(
            max(0.0, (segment_start - last_training).total_seconds() / 86400.0),
            max(0.0, (end - last_training).total_seconds() / 86400.0),
            policy,
        )
    return round(total, 9)


def physical_attribute_progression_due(
    conn: sqlite3.Connection,
    actor_id: str,
    attribute_key: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
) -> PhysicalAttributeProgressionDue:
    policy = physical_attribute_policy(attribute_key)
    as_of = _dt(as_of_sim_time)
    last_settled = latest_physical_attribute_settlement_time(conn, actor_id, attribute_key)
    stimuli = physical_attribute_stimulus_events(
        conn,
        actor_id,
        attribute_key,
        as_of_sim_time=as_of_sim_time,
    )
    if last_settled is None:
        return PhysicalAttributeProgressionDue(True, "bootstrap", None, (), None)
    last_dt = _dt(last_settled)
    if as_of <= last_dt:
        return PhysicalAttributeProgressionDue(False, "same_or_older_boundary", last_settled, (), 0.0)

    consumed = _consumed_ids(conn, actor_id, policy)
    state_quality, _ = recovery_state_quality(state)
    recovery_allowed = float(state["fatigue"]) < FATIGUE_HARD_BLOCK and state_quality > 0.0
    eligible: list[int] = []
    if recovery_allowed:
        for event in stimuli:
            if event.event_id in consumed:
                continue
            age_hours = max(0.0, (as_of - _dt(event.sim_time)).total_seconds() / 3600.0)
            if age_hours >= policy.full_recovery_hours:
                eligible.append(event.event_id)

    elapsed_hours = max(0.0, (as_of - last_dt).total_seconds() / 3600.0)
    if eligible:
        return PhysicalAttributeProgressionDue(
            True,
            "eligible_stimulus",
            last_settled,
            tuple(eligible),
            round(elapsed_hours, 6),
        )
    if stimuli and elapsed_hours >= policy.detraining_checkpoint_hours:
        return PhysicalAttributeProgressionDue(
            True,
            "detraining_checkpoint",
            last_settled,
            (),
            round(elapsed_hours, 6),
        )
    return PhysicalAttributeProgressionDue(
        False,
        "not_due",
        last_settled,
        (),
        round(elapsed_hours, 6),
    )


def settle_physical_attribute_progression(
    conn: sqlite3.Connection,
    actor_id: str,
    attribute_key: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    policy = physical_attribute_policy(attribute_key)
    as_of = _dt(as_of_sim_time)
    old_value = _read_profile_value(conn, actor_id, policy.field_key)
    stimuli = physical_attribute_stimulus_events(
        conn,
        actor_id,
        attribute_key,
        as_of_sim_time=as_of_sim_time,
    )
    last_settled = latest_physical_attribute_settlement_time(conn, actor_id, attribute_key)

    if last_settled is None:
        consumed = [event.event_id for event in stimuli]
        event_id = record_event(
            conn,
            sim_time=as_of_sim_time,
            actor_id=actor_id,
            event_type=policy.settlement_event_type,
            payload={
                "source": policy.framework_source,
                "attribute_key": attribute_key,
                "field_key": policy.field_key,
                "bootstrap": True,
                "settled_through_sim_time": as_of_sim_time,
                "consumed_stimulus_event_ids": consumed,
                "old_value": round(old_value, 6),
                "new_value": round(old_value, 6),
                "positive_delta": 0.0,
                "negative_delta": 0.0,
                "net_delta": 0.0,
            },
        )
        conn.commit()
        return {
            "status": "bootstrapped",
            "event_id": event_id,
            "attribute_key": attribute_key,
            "field_key": policy.field_key,
            "old_value": round(old_value, 6),
            "new_value": round(old_value, 6),
            "positive_delta": 0.0,
            "negative_delta": 0.0,
            "net_delta": 0.0,
            "consumed_stimulus_event_ids": consumed,
            "settled_through_sim_time": as_of_sim_time,
        }

    last_dt = _dt(last_settled)
    if as_of < last_dt:
        raise ValueError(f"cannot settle {attribute_key} progression before the latest settlement cursor")
    if as_of == last_dt:
        return {
            "status": "no_change",
            "attribute_key": attribute_key,
            "field_key": policy.field_key,
            "old_value": round(old_value, 6),
            "new_value": round(old_value, 6),
            "positive_delta": 0.0,
            "negative_delta": 0.0,
            "net_delta": 0.0,
            "consumed_stimulus_event_ids": [],
            "settled_through_sim_time": last_settled,
        }

    consumed = _consumed_ids(conn, actor_id, policy)
    state_quality, recovery_components = recovery_state_quality(state)
    fatigue_blocked = float(state["fatigue"]) >= FATIGUE_HARD_BLOCK
    current = old_value
    positive_delta = 0.0
    newly_consumed: list[int] = []
    positive_evidence: list[dict[str, Any]] = []

    for event in stimuli:
        if event.event_id in consumed:
            continue
        age_hours = max(0.0, (as_of - _dt(event.sim_time)).total_seconds() / 3600.0)
        if age_hours < policy.full_recovery_hours or fatigue_blocked or state_quality <= 0.0:
            continue
        level = physical_attribute_level_factor(current, policy)
        recent_units = recent_physical_attribute_stimulus_units(
            conn,
            actor_id,
            attribute_key,
            as_of_sim_time=event.sim_time,
        )
        saturation = physical_attribute_saturation_factor(recent_units, policy)
        gain = max(
            0.0,
            policy.base_positive_scale
            * event.stimulus_units
            * level
            * saturation
            * state_quality,
        )
        next_value = min(policy.natural_ceiling, current + gain)
        realized = max(0.0, next_value - current)
        current = next_value
        positive_delta += realized
        newly_consumed.append(event.event_id)
        positive_evidence.append(
            {
                "event_id": event.event_id,
                "method_id": event.method_id,
                "stimulus_units": event.stimulus_units,
                "effective_minutes": event.effective_minutes,
                "age_hours": round(age_hours, 6),
                "level_factor": level,
                "recent_stimulus_units": recent_units,
                "saturation_factor": saturation,
                "recovery_state_quality": round(state_quality, 9),
                "realized_delta": round(realized, 9),
            }
        )

    integrated_days = integrated_physical_attribute_detraining_days(
        conn,
        actor_id,
        attribute_key,
        start_sim_time=last_settled,
        end_sim_time=as_of_sim_time,
    )
    level_exposure = max(0.0, min(1.0, current / policy.natural_ceiling)) ** policy.detraining_level_exponent
    negative_delta = max(
        0.0,
        policy.base_detraining_points_per_day * integrated_days * level_exposure,
    )
    new_value = max(0.0, min(policy.natural_ceiling, current - negative_delta))
    realized_negative = max(0.0, current - new_value)
    net_delta = new_value - old_value
    changed = abs(net_delta) >= 0.0000005
    if changed:
        _write_profile_value(
            conn,
            actor_id,
            policy,
            old_value=old_value,
            new_value=new_value,
            sim_time=as_of_sim_time,
        )

    event_id = record_event(
        conn,
        sim_time=as_of_sim_time,
        actor_id=actor_id,
        event_type=policy.settlement_event_type,
        state_changes={
            policy.field_key: {
                "before": round(old_value, 6),
                "after": round(new_value, 6),
                "delta": round(net_delta, 9),
            }
        } if changed else {},
        payload={
            "source": policy.framework_source,
            "attribute_key": attribute_key,
            "field_key": policy.field_key,
            "bootstrap": False,
            "settled_from_sim_time": last_settled,
            "settled_through_sim_time": as_of_sim_time,
            "consumed_stimulus_event_ids": newly_consumed,
            "positive_evidence": positive_evidence,
            "recovery_components": recovery_components,
            "fatigue_blocked": fatigue_blocked,
            "integrated_detraining_days": integrated_days,
            "detraining_level_exposure": round(level_exposure, 9),
            "old_value": round(old_value, 6),
            "new_value": round(new_value, 6),
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
        "attribute_key": attribute_key,
        "field_key": policy.field_key,
        "old_value": round(old_value, 6),
        "new_value": round(new_value, 6),
        "positive_delta": round(positive_delta, 9),
        "negative_delta": round(realized_negative, 9),
        "net_delta": round(net_delta, 9),
        "consumed_stimulus_event_ids": newly_consumed,
        "settled_through_sim_time": as_of_sim_time,
    }


def maybe_settle_physical_attribute_progression(
    conn: sqlite3.Connection,
    actor_id: str,
    attribute_key: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    due = physical_attribute_progression_due(
        conn,
        actor_id,
        attribute_key,
        as_of_sim_time=as_of_sim_time,
        state=state,
    )
    if not due.due:
        return {
            "state": "skipped",
            "reason": due.reason,
            "attribute_key": attribute_key,
            "settlement": None,
        }
    settlement = settle_physical_attribute_progression(
        conn,
        actor_id,
        attribute_key,
        as_of_sim_time=as_of_sim_time,
        state=state,
    )
    return {
        "state": "settled",
        "reason": due.reason,
        "attribute_key": attribute_key,
        "settlement": settlement,
    }


def maybe_settle_physical_attribute_batch(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    results: dict[str, dict[str, Any]] = {}
    current_state = state
    for attribute_key in physical_attribute_keys():
        results[attribute_key] = maybe_settle_physical_attribute_progression(
            conn,
            actor_id,
            attribute_key,
            as_of_sim_time=as_of_sim_time,
            state=current_state,
        )
    return results

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta


SATURATION_CURVE_ID = "strength-stimulus-saturation-v1"
DEFAULT_WINDOW_HOURS = 72.0
DEFAULT_ALPHA = 0.3


@dataclass(frozen=True)
class StrengthStimulusSaturationEvidence:
    curve_id: str
    recent_stimulus_units: float
    window_hours: float
    alpha: float
    saturation_factor: float


def saturation_factor(
    recent_stimulus_units: float | int,
    *,
    alpha: float = DEFAULT_ALPHA,
) -> float:
    """Return marginal adaptation yield from recent same-domain stimulus.

    v1 proof curve:
        factor = 1 / (1 + alpha * recent_stimulus_units)

    This is read-only and does not consume or mutate stimulus history.
    """
    stimulus = float(recent_stimulus_units)
    coefficient = float(alpha)
    if stimulus < 0.0:
        raise ValueError("recent_stimulus_units must be non-negative")
    if coefficient < 0.0:
        raise ValueError("alpha must be non-negative")
    return round(1.0 / (1.0 + coefficient * stimulus), 9)


def recent_strength_stimulus_units(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    window_hours: float = DEFAULT_WINDOW_HOURS,
) -> float:
    """Aggregate eligible Strength stimulus from existing completion events.

    No new persistence is introduced. Only completed-event payload evidence with
    `training_stimulus.domain == strength` is counted.
    """
    hours = float(window_hours)
    if hours <= 0.0:
        raise ValueError("window_hours must be positive")
    as_of = datetime.fromisoformat(as_of_sim_time)
    cutoff = as_of - timedelta(hours=hours)

    rows = conn.execute(
        """
        SELECT sim_time,payload_json
        FROM events
        WHERE actor_id=? AND event_type='action_completed'
        ORDER BY id DESC
        """,
        (actor_id,),
    ).fetchall()

    total = 0.0
    for row in rows:
        event_time = datetime.fromisoformat(row["sim_time"])
        if event_time > as_of:
            continue
        if event_time < cutoff:
            break
        payload = json.loads(row["payload_json"] or "{}")
        evidence = payload.get("training_stimulus")
        if not isinstance(evidence, dict) or evidence.get("domain") != "strength":
            continue
        units = evidence.get("stimulus_units")
        if isinstance(units, (int, float)) and float(units) > 0.0:
            total += float(units)
    return round(total, 6)


def strength_stimulus_saturation_evidence(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    window_hours: float = DEFAULT_WINDOW_HOURS,
    alpha: float = DEFAULT_ALPHA,
) -> StrengthStimulusSaturationEvidence:
    recent = recent_strength_stimulus_units(
        conn,
        actor_id,
        as_of_sim_time=as_of_sim_time,
        window_hours=window_hours,
    )
    return StrengthStimulusSaturationEvidence(
        curve_id=SATURATION_CURVE_ID,
        recent_stimulus_units=recent,
        window_hours=round(float(window_hours), 6),
        alpha=round(float(alpha), 6),
        saturation_factor=saturation_factor(recent, alpha=alpha),
    )

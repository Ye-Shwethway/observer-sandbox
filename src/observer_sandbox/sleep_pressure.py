from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any


RESTORATIVE_SLEEP_MINUTES = 180
CRITICAL_HOURS_AWAKE = 20.0
NIGHT_STRONG_HOURS_AWAKE = 14.0
DEEP_NIGHT_CRITICAL_HOURS_AWAKE = 17.0
NIGHT_START_HOUR = 22
DAY_START_HOUR = 7


def _completed_sleep_rows(conn: sqlite3.Connection, actor_id: str):
    return conn.execute(
        """
        SELECT sim_time,payload_json
        FROM events
        WHERE actor_id=? AND event_type='action_completed'
        ORDER BY id DESC
        """,
        (actor_id,),
    ).fetchall()


def last_restorative_sleep_end(conn: sqlite3.Connection, actor_id: str) -> datetime | None:
    for row in _completed_sleep_rows(conn, actor_id):
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") != "sleep":
            continue
        duration = payload.get("duration_minutes")
        if not isinstance(duration, (int, float)) or float(duration) < RESTORATIVE_SLEEP_MINUTES:
            continue
        ended = payload.get("action_ended_sim_time") or row["sim_time"]
        if ended:
            return datetime.fromisoformat(str(ended))
    return None


def _earliest_observed_time(conn: sqlite3.Connection, actor_id: str) -> datetime | None:
    row = conn.execute(
        "SELECT sim_time FROM events WHERE actor_id=? ORDER BY id ASC LIMIT 1",
        (actor_id,),
    ).fetchone()
    return None if row is None or not row["sim_time"] else datetime.fromisoformat(str(row["sim_time"]))


def sleep_pressure_signal(
    conn: sqlite3.Connection,
    *,
    state: dict[str, Any],
    actor_id: str,
) -> dict[str, Any]:
    now = datetime.fromisoformat(str(state["sim_time"]))
    last_sleep = last_restorative_sleep_end(conn, actor_id)
    anchor = last_sleep or _earliest_observed_time(conn, actor_id)
    hours_awake = None if anchor is None else max(0.0, (now - anchor).total_seconds() / 3600.0)
    raw_sleepiness = float(state["sleepiness"])
    hour = now.hour
    night = hour >= NIGHT_START_HOUR or hour < DAY_START_HOUR
    deep_night = 0 <= hour < 5

    critical_reasons: list[str] = []
    strong_reasons: list[str] = []
    if raw_sleepiness >= 80.0:
        critical_reasons.append("raw_sleepiness")
    elif raw_sleepiness >= 65.0:
        strong_reasons.append("raw_sleepiness")

    if hours_awake is not None:
        # Severe sleep deprivation remains an all-day safety override. Ordinary
        # 16-hour wakefulness is not itself a bedtime trigger because doing so
        # phase-locks the actor to whatever wake time the previous sleep created.
        if hours_awake >= CRITICAL_HOURS_AWAKE:
            critical_reasons.append("extended_wakefulness")

        # Normal accumulated wakefulness becomes a strong sleep signal only in
        # the authored circadian night window. This lets an early wake time drift
        # back toward a conventional night sleep instead of causing progressively
        # earlier evening bedtimes.
        if deep_night and hours_awake >= DEEP_NIGHT_CRITICAL_HOURS_AWAKE:
            critical_reasons.append("deep_night_circadian_pressure")
        elif night and hours_awake >= NIGHT_STRONG_HOURS_AWAKE:
            strong_reasons.append("night_circadian_pressure")

    level = "critical" if critical_reasons else "strong" if strong_reasons else "comfortable"
    reasons = critical_reasons if critical_reasons else strong_reasons
    return {
        "level": level,
        "raw_sleepiness": round(raw_sleepiness, 3),
        "hours_awake": None if hours_awake is None else round(hours_awake, 3),
        "night_window": night,
        "deep_night": deep_night,
        "circadian_phase": "sleep_window" if night else "wake_window",
        "last_restorative_sleep_end": None if last_sleep is None else last_sleep.isoformat(),
        "restorative_sleep_min_minutes": RESTORATIVE_SLEEP_MINUTES,
        "reasons": reasons,
        "source": "sleep-pressure-circadian-v1.1",
    }

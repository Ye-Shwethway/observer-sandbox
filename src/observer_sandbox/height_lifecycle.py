from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

from .event_log import record_event

REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "config" / "height_lifecycle.v1.json"
DAYS_PER_YEAR = 365.2425


@lru_cache(maxsize=1)
def load_height_lifecycle_policy(path: str | Path = POLICY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _profile_record(conn: sqlite3.Connection, actor_id: str, field_key: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT value_json,mode,authority,source,observed_at FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()


def _profile_value(conn: sqlite3.Connection, actor_id: str, field_key: str) -> Any:
    row = _profile_record(conn, actor_id, field_key)
    return None if row is None else json.loads(row["value_json"])


def age_years_on(date_of_birth: str, sim_time: str) -> float:
    born = date.fromisoformat(date_of_birth)
    current = datetime.fromisoformat(sim_time).date()
    return max(0.0, (current - born).days / DAYS_PER_YEAR)


def _sex_key(value: Any) -> str:
    raw = str(value or "").strip().lower()
    return raw if raw in {"male", "female"} else "default"


def height_lifecycle_phase(*, age_years: float, sex: str, policy: dict[str, Any] | None = None) -> str:
    source = policy if policy is not None else load_height_lifecycle_policy()
    maturity = source["development"]["maturity_age_years"]
    maturity_age = float(maturity.get(_sex_key(sex), maturity["default"]))
    decline_age = float(source["adult_decline"]["start_age_years"])
    if age_years < maturity_age:
        return "developmental_growth"
    if age_years < decline_age:
        return "adult_stable"
    return "age_related_decline"


def _height_events(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    event_type = str(load_height_lifecycle_policy()["settlement_event_type"])
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
        (actor_id, event_type),
    ).fetchall()


def _latest_height_cursor(conn: sqlite3.Connection, actor_id: str) -> tuple[str | None, float | None]:
    cursor: str | None = None
    activation_height: float | None = None
    for row in _height_events(conn, actor_id):
        payload = json.loads(row["payload_json"] or "{}")
        raw_cursor = payload.get("settled_through_sim_time") or row["sim_time"]
        if isinstance(raw_cursor, str):
            cursor = raw_cursor
        if payload.get("activation_boundary") and isinstance(payload.get("activation_height_in"), (int, float)):
            activation_height = float(payload["activation_height_in"])
    return cursor, activation_height


def _required_inputs(conn: sqlite3.Connection, actor_id: str) -> dict[str, Any] | None:
    policy = load_height_lifecycle_policy()
    height = _profile_value(conn, actor_id, str(policy["field_key"]))
    maximum = _profile_value(conn, actor_id, str(policy["genetic_max_field"]))
    dob = _profile_value(conn, actor_id, str(policy["date_of_birth_field"]))
    sex = _profile_value(conn, actor_id, str(policy["sex_field"]))
    if not isinstance(height, (int, float)) or float(height) <= 0.0:
        return None
    if not isinstance(maximum, (int, float)) or float(maximum) <= 0.0:
        return None
    if not isinstance(dob, str):
        return None
    try:
        date.fromisoformat(dob)
    except ValueError:
        return None
    return {"height_in": float(height), "genetic_max_in": float(maximum), "date_of_birth": dob, "sex": _sex_key(sex)}


def _write_height(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    old_value: float,
    new_value: float,
    sim_time: str,
    reason: str,
) -> None:
    policy = load_height_lifecycle_policy()
    field_key = str(policy["field_key"])
    value_json = json.dumps(round(float(new_value), 6))
    cur = conn.execute(
        """UPDATE character_profile_values
        SET value_json=?,mode='simulated',authority='height_lifecycle_engine',source=?,observed_at=?,updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND field_key=?""",
        (value_json, str(policy["revision"]), sim_time, actor_id, field_key),
    )
    if cur.rowcount != 1:
        raise KeyError(f"Missing profile value {field_key} for {actor_id}")
    conn.execute(
        """INSERT INTO character_profile_history(
        entity_id,field_key,old_value_json,new_value_json,mode,authority,reason,sim_time
        ) VALUES(?,?,?,?,?,?,?,?)""",
        (
            actor_id,
            field_key,
            json.dumps(round(float(old_value), 6)),
            value_json,
            "simulated",
            "height_lifecycle_engine",
            reason,
            sim_time,
        ),
    )


def _activate(conn: sqlite3.Connection, actor_id: str, *, as_of_sim_time: str, inputs: dict[str, Any]) -> dict[str, Any]:
    policy = load_height_lifecycle_policy()
    current = float(inputs["height_in"])
    age = age_years_on(str(inputs["date_of_birth"]), as_of_sim_time)
    phase = height_lifecycle_phase(age_years=age, sex=str(inputs["sex"]), policy=policy)
    conn.execute("SAVEPOINT height_lifecycle_activation")
    try:
        _write_height(
            conn,
            actor_id,
            old_value=current,
            new_value=current,
            sim_time=as_of_sim_time,
            reason="Height Lifecycle v1 activation; structural stature preserved",
        )
        event_id = record_event(
            conn,
            sim_time=as_of_sim_time,
            actor_id=actor_id,
            event_type=str(policy["settlement_event_type"]),
            payload={
                "source": policy["revision"],
                "status": "bootstrapped",
                "activation_boundary": True,
                "activation_height_in": round(current, 6),
                "settled_through_sim_time": as_of_sim_time,
                "age_years": round(age, 6),
                "phase": phase,
                "genetic_max_in": round(float(inputs["genetic_max_in"]), 6),
                "stat_mutated": False,
            },
        )
        conn.execute("RELEASE SAVEPOINT height_lifecycle_activation")
        conn.commit()
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT height_lifecycle_activation")
        conn.execute("RELEASE SAVEPOINT height_lifecycle_activation")
        conn.rollback()
        raise
    return {
        "status": "bootstrapped",
        "event_id": event_id,
        "settled_through_sim_time": as_of_sim_time,
        "height_in": round(current, 6),
        "phase": phase,
        "stat_mutated": False,
    }


def _project_height(
    *,
    current_height_in: float,
    genetic_max_in: float,
    activation_height_in: float,
    age_years: float,
    sex: str,
    elapsed_days: float,
    policy: dict[str, Any] | None = None,
) -> tuple[float, dict[str, Any]]:
    source = policy if policy is not None else load_height_lifecycle_policy()
    years = max(0.0, elapsed_days / DAYS_PER_YEAR)
    phase = height_lifecycle_phase(age_years=age_years, sex=sex, policy=source)
    delta = 0.0

    if phase == "developmental_growth":
        headroom = max(0.0, genetic_max_in - current_height_in)
        dev = source["development"]
        max_growth = float(dev["max_growth_in_per_year"]) * years
        headroom_realization = headroom * min(1.0, float(dev["headroom_realization_fraction_per_year"]) * years)
        delta = min(headroom, max_growth, headroom_realization)
    elif phase == "age_related_decline":
        decline = source["adult_decline"]
        rates = decline["annual_height_fraction"]
        rate = float(rates.get(_sex_key(sex), rates["default"]))
        if age_years >= float(decline["acceleration_age_years"]):
            rate *= float(decline["acceleration_multiplier"])
        proportional_loss = current_height_in * rate * years
        absolute_cap = float(decline["maximum_loss_in_per_year"]) * years
        lifetime_floor = activation_height_in * (1.0 - float(decline["maximum_lifetime_decline_fraction_from_activation"]))
        available = max(0.0, current_height_in - lifetime_floor)
        delta = -min(proportional_loss, absolute_cap, available)

    max_abs = float(source["maximum_abs_change_in_per_settlement"])
    delta = max(-max_abs, min(max_abs, delta))
    projected = current_height_in + delta
    if phase == "developmental_growth":
        projected = min(projected, genetic_max_in)
    return round(projected, 6), {
        "phase": phase,
        "age_years": round(age_years, 6),
        "elapsed_days": round(elapsed_days, 6),
        "raw_delta_in": round(delta, 9),
        "genetic_max_in": round(genetic_max_in, 6),
        "activation_height_in": round(activation_height_in, 6),
    }


def maybe_settle_height_lifecycle(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del state
    policy = load_height_lifecycle_policy()
    inputs = _required_inputs(conn, actor_id)
    if inputs is None:
        return {"status": "deferred_missing_inputs", "stat_mutated": False}

    cursor, activation_height = _latest_height_cursor(conn, actor_id)
    if cursor is None or activation_height is None:
        return _activate(conn, actor_id, as_of_sim_time=as_of_sim_time, inputs=inputs)

    start = datetime.fromisoformat(cursor)
    end = datetime.fromisoformat(as_of_sim_time)
    elapsed_days = (end - start).total_seconds() / 86400.0
    if elapsed_days < float(policy["minimum_settlement_days"]):
        return {"status": "not_due", "settled_through_sim_time": cursor, "stat_mutated": False}

    current = float(inputs["height_in"])
    age = age_years_on(str(inputs["date_of_birth"]), as_of_sim_time)
    projected, detail = _project_height(
        current_height_in=current,
        genetic_max_in=float(inputs["genetic_max_in"]),
        activation_height_in=float(activation_height),
        age_years=age,
        sex=str(inputs["sex"]),
        elapsed_days=elapsed_days,
        policy=policy,
    )
    changed = abs(projected - current) >= 0.0000005
    conn.execute("SAVEPOINT height_lifecycle_settlement")
    try:
        if changed:
            _write_height(
                conn,
                actor_id,
                old_value=current,
                new_value=projected,
                sim_time=as_of_sim_time,
                reason=f"Height Lifecycle v1 {detail['phase']} settlement",
            )
        event_id = record_event(
            conn,
            sim_time=as_of_sim_time,
            actor_id=actor_id,
            event_type=str(policy["settlement_event_type"]),
            state_changes=(
                {str(policy["field_key"]): {"before": round(current, 6), "after": projected, "delta": round(projected - current, 9)}}
                if changed else {}
            ),
            payload={
                "source": policy["revision"],
                "status": "applied" if changed else "stable",
                "settled_from_sim_time": cursor,
                "settled_through_sim_time": as_of_sim_time,
                "old_height_in": round(current, 6),
                "new_height_in": projected,
                "projection": detail,
                "stat_mutated": changed,
            },
        )
        conn.execute("RELEASE SAVEPOINT height_lifecycle_settlement")
        conn.commit()
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT height_lifecycle_settlement")
        conn.execute("RELEASE SAVEPOINT height_lifecycle_settlement")
        conn.rollback()
        raise
    return {
        "status": "applied" if changed else "stable",
        "event_id": event_id,
        "settled_through_sim_time": as_of_sim_time,
        "height_in": projected,
        "phase": detail["phase"],
        "stat_mutated": changed,
    }

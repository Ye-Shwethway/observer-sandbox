from __future__ import annotations

import json
import sqlite3
from datetime import date, datetime
from functools import lru_cache
from pathlib import Path
from typing import Any

from .event_log import record_event

REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "config" / "sexual_anatomy_physiology_lifecycle.v1.json"
DAYS_PER_YEAR = 365.2425


@lru_cache(maxsize=1)
def load_sexual_lifecycle_policy(path: str | Path = POLICY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _record(conn: sqlite3.Connection, actor_id: str, field_key: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT value_json,mode,authority,source,observed_at FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()


def _value(conn: sqlite3.Connection, actor_id: str, field_key: str) -> Any:
    row = _record(conn, actor_id, field_key)
    return None if row is None else json.loads(row["value_json"])


def _age_years(date_of_birth: str, sim_time: str) -> float:
    born = date.fromisoformat(date_of_birth)
    current = datetime.fromisoformat(sim_time).date()
    return max(0.0, (current - born).days / DAYS_PER_YEAR)


def _sex_key(value: Any) -> str:
    raw = str(value or "").strip().lower()
    return raw if raw == "male" else "default"


def _events(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    event_type = str(load_sexual_lifecycle_policy()["settlement_event_type"])
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
        (actor_id, event_type),
    ).fetchall()


def _latest_cursor(conn: sqlite3.Connection, actor_id: str) -> tuple[str | None, dict[str, float]]:
    cursor: str | None = None
    activation: dict[str, float] = {}
    for row in _events(conn, actor_id):
        payload = json.loads(row["payload_json"] or "{}")
        raw = payload.get("settled_through_sim_time") or row["sim_time"]
        if isinstance(raw, str):
            cursor = raw
        if payload.get("activation_boundary"):
            values = payload.get("activation_structural_values")
            if isinstance(values, dict):
                activation = {
                    str(key): float(value)
                    for key, value in values.items()
                    if isinstance(value, (int, float))
                }
    return cursor, activation


def _write_value(
    conn: sqlite3.Connection,
    actor_id: str,
    field_key: str,
    *,
    old_value: float,
    new_value: float,
    sim_time: str,
    authority: str,
    reason: str,
) -> None:
    policy = load_sexual_lifecycle_policy()
    value_json = json.dumps(round(float(new_value), 6))
    cur = conn.execute(
        """UPDATE character_profile_values
        SET value_json=?,mode='simulated',authority=?,source=?,observed_at=?,updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND field_key=?""",
        (value_json, authority, str(policy["revision"]), sim_time, actor_id, field_key),
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
            authority,
            reason,
            sim_time,
        ),
    )


def _required_structural_inputs(conn: sqlite3.Connection, actor_id: str) -> dict[str, Any] | None:
    policy = load_sexual_lifecycle_policy()
    dob = _value(conn, actor_id, str(policy["date_of_birth_field"]))
    sex = _value(conn, actor_id, str(policy["sex_field"]))
    if not isinstance(dob, str) or _sex_key(sex) != "male":
        return None
    try:
        date.fromisoformat(dob)
    except ValueError:
        return None
    fields: dict[str, tuple[float, float]] = {}
    for field_key, genetic_key in policy["structural"]["fields"].items():
        current = _value(conn, actor_id, field_key)
        target = _value(conn, actor_id, str(genetic_key))
        if not isinstance(current, (int, float)) or not isinstance(target, (int, float)):
            return None
        if float(current) <= 0.0 or float(target) <= 0.0:
            return None
        fields[str(field_key)] = (float(current), float(target))
    return {"date_of_birth": dob, "sex": "male", "fields": fields}


def _structural_phase(age_years: float, sex: str, policy: dict[str, Any]) -> str:
    maturity_map = policy["structural"]["maturity_age_years"]
    maturity = float(maturity_map.get(_sex_key(sex), maturity_map["default"]))
    return "developmental_growth" if age_years < maturity else "adult_stable"


def _project_structural_field(
    *,
    field_key: str,
    current: float,
    target: float,
    age_years: float,
    sex: str,
    elapsed_days: float,
    policy: dict[str, Any],
) -> tuple[float, dict[str, Any]]:
    phase = _structural_phase(age_years, sex, policy)
    delta = 0.0
    if phase == "developmental_growth":
        years = max(0.0, elapsed_days / DAYS_PER_YEAR)
        headroom = max(0.0, target - current)
        realization = headroom * min(1.0, float(policy["structural"]["headroom_realization_fraction_per_year"]) * years)
        proportional_cap = current * float(policy["structural"]["maximum_fractional_growth_per_year"]) * years
        delta = min(headroom, realization, proportional_cap)
    max_abs = float(policy["structural"]["maximum_abs_change_in_per_settlement"][field_key])
    delta = max(-max_abs, min(max_abs, delta))
    projected = min(target, current + delta) if phase == "developmental_growth" else current
    return round(projected, 6), {
        "phase": phase,
        "age_years": round(age_years, 6),
        "adult_target": round(target, 6),
        "raw_delta": round(delta, 9),
    }


def _project_functional_capacity(
    *,
    current: float,
    cap: float,
    age_years: float,
    elapsed_days: float,
    policy: dict[str, Any],
) -> tuple[float, dict[str, Any]]:
    functional = policy["functional"]
    years = max(0.0, elapsed_days / DAYS_PER_YEAR)
    phase = "adult_stable"
    delta = 0.0
    if age_years >= float(functional["decline_start_age_years"]):
        phase = "age_related_functional_decline"
        rate = float(functional["annual_points_after_start"])
        if age_years >= float(functional["acceleration_age_years"]):
            rate *= float(functional["acceleration_multiplier"])
        delta = -rate * years
    max_abs = float(functional["maximum_abs_change_per_settlement"])
    delta = max(-max_abs, min(max_abs, delta))
    projected = max(float(functional["minimum_score"]), min(cap, current + delta))
    return round(projected, 6), {
        "phase": phase,
        "age_years": round(age_years, 6),
        "cap": round(cap, 6),
        "raw_delta": round(delta, 9),
    }


def _activate(conn: sqlite3.Connection, actor_id: str, *, sim_time: str, inputs: dict[str, Any]) -> dict[str, Any]:
    policy = load_sexual_lifecycle_policy()
    age = _age_years(str(inputs["date_of_birth"]), sim_time)
    phase = _structural_phase(age, str(inputs["sex"]), policy)
    activated: dict[str, float] = {}
    conn.execute("SAVEPOINT sexual_lifecycle_activation")
    try:
        for field_key, (current, _target) in inputs["fields"].items():
            _write_value(
                conn,
                actor_id,
                field_key,
                old_value=current,
                new_value=current,
                sim_time=sim_time,
                authority="sexual_anatomy_lifecycle_engine",
                reason="Sexual Anatomy Lifecycle v1 activation; structural value preserved",
            )
            activated[field_key] = current
        event_id = record_event(
            conn,
            sim_time=sim_time,
            actor_id=actor_id,
            event_type=str(policy["settlement_event_type"]),
            payload={
                "source": policy["revision"],
                "status": "bootstrapped",
                "activation_boundary": True,
                "activation_structural_values": activated,
                "settled_through_sim_time": sim_time,
                "age_years": round(age, 6),
                "structural_phase": phase,
                "functional_status": "deferred_missing_baseline_or_cap",
                "stat_mutated": False,
            },
        )
        conn.execute("RELEASE SAVEPOINT sexual_lifecycle_activation")
        conn.commit()
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT sexual_lifecycle_activation")
        conn.execute("RELEASE SAVEPOINT sexual_lifecycle_activation")
        conn.rollback()
        raise
    return {
        "status": "bootstrapped",
        "event_id": event_id,
        "structural_phase": phase,
        "structural_values": activated,
        "stat_mutated": False,
    }


def maybe_settle_sexual_anatomy_physiology_lifecycle(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del state
    policy = load_sexual_lifecycle_policy()
    inputs = _required_structural_inputs(conn, actor_id)
    if inputs is None:
        return {"status": "deferred_missing_or_inapplicable_structural_inputs", "stat_mutated": False}

    cursor, activation_values = _latest_cursor(conn, actor_id)
    if cursor is None or not activation_values:
        return _activate(conn, actor_id, sim_time=as_of_sim_time, inputs=inputs)

    start = datetime.fromisoformat(cursor)
    end = datetime.fromisoformat(as_of_sim_time)
    elapsed_days = (end - start).total_seconds() / 86400.0
    if elapsed_days < float(policy["minimum_settlement_days"]):
        return {"status": "not_due", "settled_through_sim_time": cursor, "stat_mutated": False}

    age = _age_years(str(inputs["date_of_birth"]), as_of_sim_time)
    structural_new: dict[str, float] = {}
    structural_detail: dict[str, Any] = {}
    changes: dict[str, Any] = {}
    for field_key, (current, target) in inputs["fields"].items():
        projected, detail = _project_structural_field(
            field_key=field_key,
            current=current,
            target=target,
            age_years=age,
            sex=str(inputs["sex"]),
            elapsed_days=elapsed_days,
            policy=policy,
        )
        structural_new[field_key] = projected
        structural_detail[field_key] = detail
        if abs(projected - current) >= 0.0000005:
            changes[field_key] = {"before": current, "after": projected, "delta": round(projected - current, 9)}

    functional = policy["functional"]
    baseline_field = str(functional["baseline_field"])
    cap_field = str(functional["cap_field"])
    baseline = _value(conn, actor_id, baseline_field)
    cap = _value(conn, actor_id, cap_field)
    functional_detail: dict[str, Any] = {"status": "deferred_missing_baseline_or_cap"}
    functional_new: float | None = None
    if isinstance(baseline, (int, float)) and isinstance(cap, (int, float)):
        functional_new, projection = _project_functional_capacity(
            current=float(baseline),
            cap=float(cap),
            age_years=age,
            elapsed_days=elapsed_days,
            policy=policy,
        )
        functional_detail = {"status": "available", **projection}
        if abs(functional_new - float(baseline)) >= 0.0000005:
            changes[baseline_field] = {
                "before": float(baseline),
                "after": functional_new,
                "delta": round(functional_new - float(baseline), 9),
            }

    conn.execute("SAVEPOINT sexual_lifecycle_settlement")
    try:
        for field_key, change in changes.items():
            authority = "sexual_physiology_engine" if field_key == baseline_field else "sexual_anatomy_lifecycle_engine"
            _write_value(
                conn,
                actor_id,
                field_key,
                old_value=float(change["before"]),
                new_value=float(change["after"]),
                sim_time=as_of_sim_time,
                authority=authority,
                reason="Sexual Anatomy & Physiology Lifecycle v1 settlement",
            )
        event_id = record_event(
            conn,
            sim_time=as_of_sim_time,
            actor_id=actor_id,
            event_type=str(policy["settlement_event_type"]),
            state_changes=changes,
            payload={
                "source": policy["revision"],
                "status": "applied" if changes else "stable",
                "settled_from_sim_time": cursor,
                "settled_through_sim_time": as_of_sim_time,
                "age_years": round(age, 6),
                "structural_values": structural_new,
                "structural_projection": structural_detail,
                "functional_projection": functional_detail,
                "stat_mutated": bool(changes),
            },
        )
        conn.execute("RELEASE SAVEPOINT sexual_lifecycle_settlement")
        conn.commit()
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT sexual_lifecycle_settlement")
        conn.execute("RELEASE SAVEPOINT sexual_lifecycle_settlement")
        conn.rollback()
        raise
    return {
        "status": "applied" if changes else "stable",
        "event_id": event_id,
        "structural_values": structural_new,
        "functional_value": functional_new,
        "stat_mutated": bool(changes),
    }

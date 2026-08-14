from __future__ import annotations

import json
import math
import sqlite3
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path
from typing import Any

from .event_log import record_event
from .nutrition_energy import energy_balance_window
from .recovery_realization import recovery_state_quality


REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "config" / "body_composition_progression.v1.json"
LB_PER_KG = 2.2046226218


@lru_cache(maxsize=1)
def load_body_composition_policy(path: str | Path = POLICY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dt(raw: str) -> datetime:
    return datetime.fromisoformat(raw)


def _profile_value(conn: sqlite3.Connection, actor_id: str, field_key: str) -> float | None:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    return None if row is None else float(json.loads(row[0]))


def body_composition_snapshot(conn: sqlite3.Connection, actor_id: str) -> dict[str, float]:
    weight_lb = _profile_value(conn, actor_id, "body.weight_lb")
    body_fat_pct = _profile_value(conn, actor_id, "body.body_fat_pct")
    height_in = _profile_value(conn, actor_id, "body.height_in")
    if weight_lb is None or body_fat_pct is None or height_in is None:
        raise KeyError(f"Missing body composition inputs for {actor_id}")
    if weight_lb <= 0.0 or height_in <= 0.0 or not (0.0 <= body_fat_pct < 100.0):
        raise ValueError(f"Invalid body composition state for {actor_id}")
    fat_mass_lb = weight_lb * body_fat_pct / 100.0
    lean_mass_lb = weight_lb - fat_mass_lb
    bmi = 703.0 * weight_lb / (height_in * height_in)
    return {
        "weight_lb": round(weight_lb, 6),
        "body_fat_pct": round(body_fat_pct, 6),
        "fat_mass_lb": round(fat_mass_lb, 6),
        "lean_mass_lb": round(lean_mass_lb, 6),
        "bmi": round(bmi, 6),
    }


def _settlement_rows(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    policy = load_body_composition_policy()
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
        (actor_id, str(policy["settlement_event_type"])),
    ).fetchall()


def latest_body_composition_settlement_time(conn: sqlite3.Connection, actor_id: str) -> str | None:
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


def _write_profile_value(
    conn: sqlite3.Connection,
    actor_id: str,
    field_key: str,
    *,
    old_value: float,
    new_value: float,
    sim_time: str,
    reason: str,
) -> None:
    policy = load_body_composition_policy()
    source = str(policy["revision"])
    value_json = json.dumps(round(float(new_value), 6))
    conn.execute(
        """UPDATE character_profile_values
        SET value_json=?,mode='simulated',authority='physiology_engine',source=?,observed_at=?,updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND field_key=?""",
        (value_json, source, sim_time, actor_id, field_key),
    )
    if conn.total_changes <= 0:
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
            "physiology_engine",
            reason,
            sim_time,
        ),
    )


def _activate_fields(conn: sqlite3.Connection, actor_id: str, *, sim_time: str) -> dict[str, float]:
    before = body_composition_snapshot(conn, actor_id)
    reason = "BC-2 activation boundary; numerical value preserved"
    _write_profile_value(
        conn, actor_id, "body.weight_lb", old_value=before["weight_lb"], new_value=before["weight_lb"], sim_time=sim_time, reason=reason
    )
    _write_profile_value(
        conn, actor_id, "body.body_fat_pct", old_value=before["body_fat_pct"], new_value=before["body_fat_pct"], sim_time=sim_time, reason=reason
    )
    return before


def _training_effective_minutes(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    start_sim_time: str,
    end_sim_time: str,
) -> float:
    start = _dt(start_sim_time)
    end = _dt(end_sim_time)
    total = 0.0
    rows = conn.execute(
        "SELECT sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id",
        (actor_id,),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") != "train":
            continue
        ended_raw = payload.get("action_ended_sim_time") or row["sim_time"]
        if not isinstance(ended_raw, str):
            continue
        ended = _dt(ended_raw)
        if not (start < ended <= end):
            continue
        method = payload.get("training_method")
        effective = method.get("effective_load") if isinstance(method, dict) else None
        minutes = effective.get("effective_minutes") if isinstance(effective, dict) else None
        if isinstance(minutes, (int, float)) and float(minutes) > 0.0:
            total += float(minutes)
    return round(total, 6)


def _genetic_ffm_ceiling_lb(conn: sqlite3.Connection, actor_id: str) -> float | None:
    lean_condition_max = _profile_value(conn, actor_id, "genetics.weight_lean_max_lb")
    fat_floor = _profile_value(conn, actor_id, "genetics.body_fat_floor_pct")
    if lean_condition_max is None or fat_floor is None:
        return None
    if lean_condition_max <= 0.0 or not (0.0 <= fat_floor < 100.0):
        return None
    return round(lean_condition_max * (1.0 - fat_floor / 100.0), 6)


def _forbes_partition(net_energy_kcal: float, current_fm_lb: float) -> dict[str, float]:
    policy = load_body_composition_policy()["partition"]
    fm_kg = max(0.001, current_fm_lb / LB_PER_KG)
    ffm_share = float(policy["forbes_constant_kg"]) / (float(policy["forbes_constant_kg"]) + fm_kg)
    fat_share = 1.0 - ffm_share
    lean_density = float(policy["lean_change_energy_density_mj_per_kg"]) * float(policy["kcal_per_mj"])
    fat_density = float(policy["fat_change_energy_density_mj_per_kg"]) * float(policy["kcal_per_mj"])
    mixed_density = ffm_share * lean_density + fat_share * fat_density
    delta_bw_kg = 0.0 if mixed_density <= 0.0 else float(net_energy_kcal) / mixed_density
    delta_ffm_lb = delta_bw_kg * ffm_share * LB_PER_KG
    delta_fm_lb = delta_bw_kg * fat_share * LB_PER_KG
    max_abs = float(policy["max_abs_partition_weight_change_lb_per_window"])
    total_lb = delta_ffm_lb + delta_fm_lb
    scale = 1.0
    if abs(total_lb) > max_abs and abs(total_lb) > 1e-12:
        scale = max_abs / abs(total_lb)
        delta_ffm_lb *= scale
        delta_fm_lb *= scale
    return {
        "forbes_ffm_share": round(ffm_share, 9),
        "mixed_energy_density_kcal_per_kg": round(mixed_density, 6),
        "partition_delta_ffm_lb": round(delta_ffm_lb, 9),
        "partition_delta_fm_lb": round(delta_fm_lb, 9),
        "partition_clamp_scale": round(scale, 9),
    }


def _rt_recomposition(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    current: dict[str, float],
    balance: dict[str, Any],
    training_minutes: float,
    state: dict[str, Any],
) -> dict[str, float]:
    raw = load_body_composition_policy()["resistance_training_recomposition"]
    weight_kg = current["weight_lb"] / LB_PER_KG
    protein_reference = max(1e-6, float(raw["protein_reference_g_per_kg_day"]) * weight_kg)
    protein_factor = max(0.0, min(1.0, float(balance["protein_g"]) / protein_reference))
    training_factor = max(0.0, min(1.0, training_minutes / float(raw["effective_training_minutes_for_full_signal"])))
    deficit_zero = float(raw["energy_deficit_zero_gain_kcal_day"])
    net = float(balance["net_energy_kcal"])
    energy_factor = 1.0 if net >= 0.0 else max(0.0, min(1.0, (net + deficit_zero) / deficit_zero))
    recovery_factor, _ = recovery_state_quality(state)
    recovery_factor = max(0.0, min(1.0, float(recovery_factor)))

    ceiling = _genetic_ffm_ceiling_lb(conn, actor_id)
    if ceiling is None or ceiling <= 0.0:
        headroom_factor = 0.25
        headroom_lb = None
    else:
        headroom_lb = max(0.0, ceiling - current["lean_mass_lb"])
        headroom_fraction = max(0.0, min(1.0, headroom_lb / ceiling))
        headroom_factor = headroom_fraction ** float(raw["genetic_headroom_exponent"])

    desired_ffm_gain = (
        float(raw["max_ffm_gain_lb_per_day_before_modifiers"])
        * protein_factor
        * training_factor
        * energy_factor
        * recovery_factor
        * headroom_factor
    )
    if headroom_lb is not None:
        desired_ffm_gain = min(desired_ffm_gain, headroom_lb)

    fat_floor = _profile_value(conn, actor_id, "genetics.body_fat_floor_pct")
    sustainable_floor = max(0.0, float(fat_floor or 0.0))
    minimum_fm_lb = current["lean_mass_lb"] * sustainable_floor / max(1e-6, 100.0 - sustainable_floor)
    available_fm_lb = max(0.0, current["fat_mass_lb"] - minimum_fm_lb)
    fat_cost_ratio = float(raw["fat_energy_cost_ratio_mj_per_kg_lean_to_mj_per_kg_fat"])
    fat_cost_lb = desired_ffm_gain * fat_cost_ratio
    if fat_cost_lb > available_fm_lb and fat_cost_lb > 0.0:
        scale = available_fm_lb / fat_cost_lb
        desired_ffm_gain *= scale
        fat_cost_lb = available_fm_lb

    return {
        "protein_factor": round(protein_factor, 9),
        "training_factor": round(training_factor, 9),
        "energy_factor": round(energy_factor, 9),
        "recovery_factor": round(recovery_factor, 9),
        "genetic_headroom_factor": round(headroom_factor, 9),
        "genetic_ffm_ceiling_lb": None if ceiling is None else round(ceiling, 6),
        "rt_ffm_gain_lb": round(max(0.0, desired_ffm_gain), 9),
        "rt_fm_energy_cost_lb": round(max(0.0, fat_cost_lb), 9),
    }


def _guard_final_composition(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    ffm_lb: float,
    fm_lb: float,
) -> tuple[float, float, dict[str, Any]]:
    guards = load_body_composition_policy()["guards"]
    ffm = max(1.0, float(ffm_lb))
    fm = max(0.0, float(fm_lb))
    floor = _profile_value(conn, actor_id, "genetics.body_fat_floor_pct")
    sustainable_floor = max(float(guards["min_body_fat_pct"]), float(floor or 0.0))
    min_fm = ffm * sustainable_floor / max(1e-6, 100.0 - sustainable_floor)
    floor_clamped = fm < min_fm
    if floor_clamped:
        fm = min_fm
    weight = ffm + fm
    min_weight = float(guards["min_weight_lb"])
    max_weight = float(guards["max_weight_lb"])
    if not (min_weight <= weight <= max_weight):
        raise ValueError(f"BC-2 produced implausible weight {weight:.3f} lb")
    body_fat = 100.0 * fm / weight
    if not (float(guards["min_body_fat_pct"]) <= body_fat <= float(guards["max_body_fat_pct"])):
        raise ValueError(f"BC-2 produced implausible body fat {body_fat:.3f}%")
    return ffm, fm, {"fat_floor_pct": sustainable_floor, "fat_floor_clamped": floor_clamped}


def maybe_settle_body_composition(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any],
) -> dict[str, Any]:
    policy = load_body_composition_policy()
    source = str(policy["revision"])
    event_type = str(policy["settlement_event_type"])
    as_of = _dt(as_of_sim_time)
    current = body_composition_snapshot(conn, actor_id)
    last = latest_body_composition_settlement_time(conn, actor_id)

    if last is None:
        before = _activate_fields(conn, actor_id, sim_time=as_of_sim_time)
        event_id = record_event(
            conn,
            sim_time=as_of_sim_time,
            actor_id=actor_id,
            event_type=event_type,
            payload={
                "source": source,
                "status": "bootstrapped",
                "activation_boundary": True,
                "settled_through_sim_time": as_of_sim_time,
                "old": before,
                "new": before,
                "stat_mutated": False,
            },
        )
        conn.commit()
        return {"status": "bootstrapped", "event_id": event_id, "settled_through_sim_time": as_of_sim_time, "composition": before}

    start = _dt(last)
    window_hours = float(policy["settlement_window_hours"])
    end = start + timedelta(hours=window_hours)
    if as_of < end:
        return {"status": "not_due", "settled_through_sim_time": last, "hours_remaining": round((end - as_of).total_seconds() / 3600.0, 6)}

    end_raw = end.isoformat()
    balance = energy_balance_window(conn, actor_id, start_sim_time=last, end_sim_time=end_raw)
    minimum_coverage = float(policy["guards"]["minimum_evidence_coverage_ratio"])
    if not bool(balance["complete"]) or float(balance["coverage_ratio"]) < minimum_coverage:
        event_id = record_event(
            conn,
            sim_time=end_raw,
            actor_id=actor_id,
            event_type=event_type,
            payload={
                "source": source,
                "status": "deferred_incomplete_evidence",
                "settled_from_sim_time": last,
                "settled_through_sim_time": end_raw,
                "energy_balance": balance,
                "old": current,
                "new": current,
                "stat_mutated": False,
            },
        )
        conn.commit()
        return {"status": "deferred_incomplete_evidence", "event_id": event_id, "settled_through_sim_time": end_raw, "composition": current}

    training_minutes = _training_effective_minutes(conn, actor_id, start_sim_time=last, end_sim_time=end_raw)
    partition = _forbes_partition(float(balance["net_energy_kcal"]), current["fat_mass_lb"])
    recomposition = _rt_recomposition(
        conn,
        actor_id,
        current=current,
        balance=balance,
        training_minutes=training_minutes,
        state=state,
    )

    ffm = current["lean_mass_lb"] + float(partition["partition_delta_ffm_lb"]) + float(recomposition["rt_ffm_gain_lb"])
    fm = current["fat_mass_lb"] + float(partition["partition_delta_fm_lb"]) - float(recomposition["rt_fm_energy_cost_lb"])
    ffm, fm, guard_detail = _guard_final_composition(conn, actor_id, ffm_lb=ffm, fm_lb=fm)
    new_weight = ffm + fm
    new_bf = 100.0 * fm / new_weight
    new_bmi = 703.0 * new_weight / (_profile_value(conn, actor_id, "body.height_in") ** 2)
    new = {
        "weight_lb": round(new_weight, 6),
        "body_fat_pct": round(new_bf, 6),
        "fat_mass_lb": round(fm, 6),
        "lean_mass_lb": round(ffm, 6),
        "bmi": round(new_bmi, 6),
    }
    weight_delta = new["weight_lb"] - current["weight_lb"]
    bf_delta = new["body_fat_pct"] - current["body_fat_pct"]
    changed = abs(weight_delta) >= 0.0000005 or abs(bf_delta) >= 0.0000005

    conn.execute("SAVEPOINT bc2_body_composition")
    try:
        if changed:
            _write_profile_value(
                conn,
                actor_id,
                "body.weight_lb",
                old_value=current["weight_lb"],
                new_value=new["weight_lb"],
                sim_time=end_raw,
                reason="BC-2 coupled daily body-composition settlement",
            )
            _write_profile_value(
                conn,
                actor_id,
                "body.body_fat_pct",
                old_value=current["body_fat_pct"],
                new_value=new["body_fat_pct"],
                sim_time=end_raw,
                reason="BC-2 coupled daily body-composition settlement",
            )
        event_id = record_event(
            conn,
            sim_time=end_raw,
            actor_id=actor_id,
            event_type=event_type,
            state_changes={
                "body.weight_lb": {"before": current["weight_lb"], "after": new["weight_lb"], "delta": round(weight_delta, 9)},
                "body.body_fat_pct": {"before": current["body_fat_pct"], "after": new["body_fat_pct"], "delta": round(bf_delta, 9)},
            } if changed else {},
            payload={
                "source": source,
                "status": "applied" if changed else "advanced",
                "settled_from_sim_time": last,
                "settled_through_sim_time": end_raw,
                "window_hours": window_hours,
                "energy_balance": balance,
                "training_effective_minutes": training_minutes,
                "partition": partition,
                "rt_recomposition": recomposition,
                "guards": guard_detail,
                "old": current,
                "new": new,
                "stat_mutated": changed,
            },
        )
        conn.execute("RELEASE SAVEPOINT bc2_body_composition")
        conn.commit()
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT bc2_body_composition")
        conn.execute("RELEASE SAVEPOINT bc2_body_composition")
        conn.rollback()
        raise

    return {
        "status": "applied" if changed else "advanced",
        "event_id": event_id,
        "settled_through_sim_time": end_raw,
        "old": current,
        "new": new,
        "weight_delta_lb": round(weight_delta, 9),
        "body_fat_delta_pct": round(bf_delta, 9),
    }

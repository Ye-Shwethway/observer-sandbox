from __future__ import annotations

import json
import sqlite3
from functools import lru_cache
from pathlib import Path
from typing import Any

from .event_log import record_event

REPO_ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = REPO_ROOT / "config" / "body_measurement_progression.v1.json"
LB_PER_KG = 2.2046226218


@lru_cache(maxsize=1)
def load_body_measurement_policy(path: str | Path = POLICY_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _profile_value(conn: sqlite3.Connection, actor_id: str, field_key: str) -> float | None:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (actor_id, field_key),
    ).fetchone()
    return None if row is None else float(json.loads(row[0]))


def body_measurement_snapshot(conn: sqlite3.Connection, actor_id: str) -> dict[str, float]:
    values: dict[str, float] = {}
    for field_key in load_body_measurement_policy()["fields"]:
        value = _profile_value(conn, actor_id, field_key)
        if value is not None:
            values[field_key] = round(value, 6)
    return values


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
    source = str(load_body_measurement_policy()["revision"])
    value_json = json.dumps(round(float(new_value), 6))
    cur = conn.execute(
        """UPDATE character_profile_values
        SET value_json=?,mode='simulated',authority='body_progression_engine',source=?,observed_at=?,updated_at=CURRENT_TIMESTAMP
        WHERE entity_id=? AND field_key=?""",
        (value_json, source, sim_time, actor_id, field_key),
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
            "body_progression_engine",
            reason,
            sim_time,
        ),
    )


def _measurement_events(conn: sqlite3.Connection, actor_id: str) -> list[sqlite3.Row]:
    event_type = str(load_body_measurement_policy()["settlement_event_type"])
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
        (actor_id, event_type),
    ).fetchall()


def _latest_measurement_cursor(conn: sqlite3.Connection, actor_id: str) -> tuple[str | None, str | None]:
    cursor: str | None = None
    activation: str | None = None
    for row in _measurement_events(conn, actor_id):
        payload = json.loads(row["payload_json"] or "{}")
        raw = payload.get("settled_through_sim_time") or row["sim_time"]
        if isinstance(raw, str):
            cursor = raw
        if payload.get("activation_boundary") and isinstance(payload.get("activation_sim_time"), str):
            activation = str(payload["activation_sim_time"])
        elif payload.get("activation_boundary") and isinstance(row["sim_time"], str):
            activation = str(row["sim_time"])
    return cursor, activation


def _next_bc2_event(conn: sqlite3.Connection, actor_id: str, cursor: str) -> sqlite3.Row | None:
    event_type = str(load_body_measurement_policy()["body_composition_event_type"])
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
        (actor_id, event_type),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        through = payload.get("settled_through_sim_time") or row["sim_time"]
        if not isinstance(through, str) or through <= cursor:
            continue
        if payload.get("status") == "bootstrapped":
            continue
        return row
    return None


def _genetic_ffm_ceiling_lb(conn: sqlite3.Connection, actor_id: str) -> float | None:
    lean_condition_max = _profile_value(conn, actor_id, "genetics.weight_lean_max_lb")
    fat_floor = _profile_value(conn, actor_id, "genetics.body_fat_floor_pct")
    if lean_condition_max is None or fat_floor is None or lean_condition_max <= 0.0 or not (0.0 <= fat_floor < 100.0):
        return None
    return round(lean_condition_max * (1.0 - fat_floor / 100.0), 6)


def _regional_training_exposure(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    start_sim_time: str,
    end_sim_time: str,
) -> dict[str, float]:
    policy = load_body_measurement_policy()
    method_weights = policy["method_region_weights"]
    weighted: dict[str, float] = {}
    total_resistance_minutes = 0.0
    rows = conn.execute(
        "SELECT sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id",
        (actor_id,),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") != "train":
            continue
        ended = payload.get("action_ended_sim_time") or row["sim_time"]
        if not isinstance(ended, str) or not (start_sim_time < ended <= end_sim_time):
            continue
        method = payload.get("training_method")
        if not isinstance(method, dict):
            continue
        channels = method.get("workload_channels")
        if not isinstance(channels, list) or "resistance" not in channels:
            continue
        effective = method.get("effective_load")
        minutes = effective.get("effective_minutes") if isinstance(effective, dict) else None
        if not isinstance(minutes, (int, float)) or float(minutes) <= 0.0:
            continue
        total_resistance_minutes += float(minutes)
        weights = method_weights.get(str(method.get("method_id") or ""), {})
        for region, weight in weights.items():
            weighted[region] = weighted.get(region, 0.0) + float(minutes) * max(0.0, min(1.0, float(weight)))
    if total_resistance_minutes <= 0.0:
        return {region: 0.0 for region in {cfg["region"] for cfg in policy["fields"].values()}}
    return {
        region: round(max(0.0, min(1.0, value / total_resistance_minutes)), 6)
        for region, value in weighted.items()
    }


def _activate(conn: sqlite3.Connection, actor_id: str, sim_time: str) -> dict[str, Any]:
    policy = load_body_measurement_policy()
    available = body_measurement_snapshot(conn, actor_id)
    activated: dict[str, float] = {}
    deferred: list[str] = []
    conn.execute("SAVEPOINT bc3_measurement_activation")
    try:
        for field_key, cfg in policy["fields"].items():
            value = available.get(field_key)
            if value is None:
                deferred.append(field_key)
                continue
            max_field = cfg.get("max_field")
            target_field = cfg.get("target_field")
            if isinstance(max_field, str) and _profile_value(conn, actor_id, max_field) is None:
                deferred.append(field_key)
                continue
            if isinstance(target_field, str) and _profile_value(conn, actor_id, target_field) is None:
                deferred.append(field_key)
                continue
            _write_profile_value(
                conn,
                actor_id,
                field_key,
                old_value=value,
                new_value=value,
                sim_time=sim_time,
                reason=str(policy["activation_reason"]),
            )
            activated[field_key] = value
        event_id = record_event(
            conn,
            sim_time=sim_time,
            actor_id=actor_id,
            event_type=str(policy["settlement_event_type"]),
            payload={
                "source": policy["revision"],
                "status": "bootstrapped",
                "activation_boundary": True,
                "activation_sim_time": sim_time,
                "settled_through_sim_time": sim_time,
                "activated_measurements": activated,
                "deferred_fields": deferred,
                "stat_mutated": False,
            },
        )
        conn.execute("RELEASE SAVEPOINT bc3_measurement_activation")
        conn.commit()
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT bc3_measurement_activation")
        conn.execute("RELEASE SAVEPOINT bc3_measurement_activation")
        conn.rollback()
        raise
    return {
        "status": "bootstrapped",
        "event_id": event_id,
        "settled_through_sim_time": sim_time,
        "activated_measurements": activated,
        "deferred_fields": deferred,
    }


def _project_field(
    *,
    current: float,
    cfg: dict[str, Any],
    global_ffm_headroom_lb: float,
    partition_ffm_delta_lb: float,
    rt_ffm_gain_lb: float,
    fm_delta_lb: float,
    old_fm_lb: float,
    region_exposure: float,
    genetic_max: float | None,
    waist_target: float | None,
    activation_value: float,
) -> tuple[float, dict[str, float]]:
    policy = load_body_measurement_policy()
    partition_delta = 0.0
    rt_delta = 0.0
    lean_loss_delta = 0.0
    fat_delta = 0.0

    if partition_ffm_delta_lb > 0.0:
        headroom_fraction = partition_ffm_delta_lb / max(1e-6, global_ffm_headroom_lb)
        if genetic_max is not None:
            muscular_headroom = max(0.0, genetic_max - current)
            partition_delta = muscular_headroom * headroom_fraction * float(policy["general_lean_headroom_share"])
        else:
            partition_delta = current * headroom_fraction * float(cfg.get("lean_elasticity", 0.10))
    elif partition_ffm_delta_lb < 0.0:
        fraction = abs(partition_ffm_delta_lb) / max(1e-6, global_ffm_headroom_lb)
        lean_loss_delta = -current * fraction * float(cfg.get("lean_loss_elasticity", 0.8))

    if rt_ffm_gain_lb > 0.0 and region_exposure > 0.0:
        headroom_fraction = rt_ffm_gain_lb / max(1e-6, global_ffm_headroom_lb)
        if genetic_max is not None:
            muscular_headroom = max(0.0, genetic_max - (current + partition_delta))
            rt_delta = muscular_headroom * headroom_fraction * region_exposure * float(policy["regional_rt_headroom_share"])
        else:
            rt_delta = current * headroom_fraction * region_exposure * float(cfg.get("lean_elasticity", 0.10))

    if abs(fm_delta_lb) > 1e-12 and old_fm_lb > 1e-6:
        fat_delta = current * (fm_delta_lb / old_fm_lb) * float(cfg.get("fat_elasticity", 0.0))

    lean_projected = current + partition_delta + rt_delta + lean_loss_delta
    if genetic_max is not None:
        lean_projected = min(lean_projected, genetic_max)
    projected = lean_projected + fat_delta
    if waist_target is not None and fm_delta_lb <= 0.0:
        projected = max(projected, waist_target)

    lower = activation_value * float(policy["minimum_activation_fraction"])
    upper = activation_value * float(policy["maximum_activation_fraction"])
    projected = max(lower, min(upper, projected))
    max_abs = float(cfg["max_abs_change_in_per_window"])
    delta = max(-max_abs, min(max_abs, projected - current))
    final = current + delta
    return round(final, 6), {
        "partition_lean_delta_in": round(partition_delta, 9),
        "regional_rt_delta_in": round(rt_delta, 9),
        "lean_loss_delta_in": round(lean_loss_delta, 9),
        "fat_delta_in": round(fat_delta, 9),
        "clamped_delta_in": round(delta, 9),
    }


def maybe_settle_body_measurements(
    conn: sqlite3.Connection,
    actor_id: str,
    *,
    as_of_sim_time: str,
    state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    del state
    policy = load_body_measurement_policy()
    cursor, activation = _latest_measurement_cursor(conn, actor_id)
    if cursor is None or activation is None:
        return _activate(conn, actor_id, as_of_sim_time)

    bc2_row = _next_bc2_event(conn, actor_id, cursor)
    if bc2_row is None:
        return {"status": "not_due", "settled_through_sim_time": cursor}
    bc2 = json.loads(bc2_row["payload_json"] or "{}")
    start = bc2.get("settled_from_sim_time")
    end = bc2.get("settled_through_sim_time") or bc2_row["sim_time"]
    if not isinstance(start, str) or not isinstance(end, str):
        raise ValueError("BC-3 requires bounded BC-2 settlement timestamps")

    if start < activation:
        event_id = record_event(
            conn,
            sim_time=end,
            actor_id=actor_id,
            event_type=str(policy["settlement_event_type"]),
            caused_by_event_id=int(bc2_row["id"]),
            payload={
                "source": policy["revision"],
                "status": "deferred_partial_pre_activation_window",
                "activation_sim_time": activation,
                "settled_from_sim_time": start,
                "settled_through_sim_time": end,
                "stat_mutated": False,
            },
        )
        conn.commit()
        return {"status": "deferred_partial_pre_activation_window", "event_id": event_id, "settled_through_sim_time": end}

    old_comp = bc2.get("old")
    new_comp = bc2.get("new")
    partition = bc2.get("partition")
    recomposition = bc2.get("rt_recomposition")
    if not all(isinstance(value, dict) for value in (old_comp, new_comp, partition, recomposition)):
        event_id = record_event(
            conn,
            sim_time=end,
            actor_id=actor_id,
            event_type=str(policy["settlement_event_type"]),
            caused_by_event_id=int(bc2_row["id"]),
            payload={
                "source": policy["revision"],
                "status": "deferred_incomplete_body_composition_evidence",
                "settled_from_sim_time": start,
                "settled_through_sim_time": end,
                "stat_mutated": False,
            },
        )
        conn.commit()
        return {"status": "deferred_incomplete_body_composition_evidence", "event_id": event_id, "settled_through_sim_time": end}

    partition_ffm = float(partition.get("partition_delta_ffm_lb") or 0.0)
    rt_ffm = float(recomposition.get("rt_ffm_gain_lb") or 0.0)
    old_fm = float(old_comp.get("fat_mass_lb") or 0.0)
    new_fm = float(new_comp.get("fat_mass_lb") or old_fm)
    fm_delta = new_fm - old_fm
    current_ffm = float(old_comp.get("lean_mass_lb") or 0.0)
    ceiling = _genetic_ffm_ceiling_lb(conn, actor_id)
    if ceiling is None or ceiling <= current_ffm:
        global_headroom = max(1.0, current_ffm * float(policy["fallback_global_ffm_headroom_fraction"]))
    else:
        global_headroom = max(1.0, ceiling - current_ffm)
    regional = _regional_training_exposure(conn, actor_id, start_sim_time=start, end_sim_time=end)

    current = body_measurement_snapshot(conn, actor_id)
    activation_values: dict[str, float] = {}
    for row in _measurement_events(conn, actor_id):
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("activation_boundary"):
            raw = payload.get("activated_measurements")
            if isinstance(raw, dict):
                activation_values = {str(k): float(v) for k, v in raw.items() if isinstance(v, (int, float))}
            break

    new_values: dict[str, float] = {}
    details: dict[str, Any] = {}
    deferred_fields: list[str] = []
    for field_key, cfg in policy["fields"].items():
        value = current.get(field_key)
        activation_value = activation_values.get(field_key)
        if value is None or activation_value is None:
            deferred_fields.append(field_key)
            continue
        genetic_max = _profile_value(conn, actor_id, str(cfg["max_field"])) if cfg.get("max_field") else None
        waist_target = _profile_value(conn, actor_id, str(cfg["target_field"])) if cfg.get("target_field") else None
        if cfg.get("max_field") and genetic_max is None:
            deferred_fields.append(field_key)
            continue
        projected, detail = _project_field(
            current=value,
            cfg=cfg,
            global_ffm_headroom_lb=global_headroom,
            partition_ffm_delta_lb=partition_ffm,
            rt_ffm_gain_lb=rt_ffm,
            fm_delta_lb=fm_delta,
            old_fm_lb=old_fm,
            region_exposure=float(regional.get(str(cfg["region"]), 0.0)),
            genetic_max=genetic_max,
            waist_target=waist_target,
            activation_value=activation_value,
        )
        new_values[field_key] = projected
        details[field_key] = {
            **detail,
            "region": cfg["region"],
            "regional_exposure": round(float(regional.get(str(cfg["region"]), 0.0)), 6),
            "genetic_max_in": None if genetic_max is None else round(genetic_max, 6),
            "waist_target_in": None if waist_target is None else round(waist_target, 6),
        }

    changes = {
        key: {"before": current[key], "after": value, "delta": round(value - current[key], 9)}
        for key, value in new_values.items()
        if abs(value - current[key]) >= 0.0000005
    }
    conn.execute("SAVEPOINT bc3_body_measurements")
    try:
        for field_key, change in changes.items():
            _write_profile_value(
                conn,
                actor_id,
                field_key,
                old_value=float(change["before"]),
                new_value=float(change["after"]),
                sim_time=end,
                reason="BC-3 regional body-measurement settlement",
            )
        event_id = record_event(
            conn,
            sim_time=end,
            actor_id=actor_id,
            event_type=str(policy["settlement_event_type"]),
            caused_by_event_id=int(bc2_row["id"]),
            state_changes=changes,
            payload={
                "source": policy["revision"],
                "status": "applied" if changes else "advanced",
                "settled_from_sim_time": start,
                "settled_through_sim_time": end,
                "body_composition_event_id": int(bc2_row["id"]),
                "body_composition_signal": {
                    "partition_delta_ffm_lb": round(partition_ffm, 9),
                    "rt_ffm_gain_lb": round(rt_ffm, 9),
                    "fat_mass_delta_lb": round(fm_delta, 9),
                    "global_ffm_headroom_lb": round(global_headroom, 6),
                },
                "regional_training_exposure": regional,
                "projection_detail": details,
                "deferred_fields": deferred_fields,
                "stat_mutated": bool(changes),
            },
        )
        conn.execute("RELEASE SAVEPOINT bc3_body_measurements")
        conn.commit()
    except Exception:
        conn.execute("ROLLBACK TO SAVEPOINT bc3_body_measurements")
        conn.execute("RELEASE SAVEPOINT bc3_body_measurements")
        conn.rollback()
        raise
    return {
        "status": "applied" if changes else "advanced",
        "event_id": event_id,
        "settled_through_sim_time": end,
        "changes": changes,
        "deferred_fields": deferred_fields,
    }

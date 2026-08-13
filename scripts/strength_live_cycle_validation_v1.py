from __future__ import annotations

import argparse
import json
import math
import os
import sqlite3
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from observer_sandbox.adaptation_curve import strength_level_factor
from observer_sandbox.db import connect
from observer_sandbox.recovery_realization import recovery_time_factor, strength_recovery_realization_evidence
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.stimulus_saturation import recent_strength_stimulus_units, saturation_factor
from observer_sandbox.strength_progression import BASE_POSITIVE_SCALE, SETTLEMENT_EVENT_TYPE
from observer_sandbox.strength_progression_activation import maybe_settle_strength_progression

ACTOR = "char_darian"
STRENGTH_KEY = "raps_pa.strength"


def _ro_connect(path: str | Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{Path(path)}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def _runtime_json(conn: sqlite3.Connection, key: str, default: Any = None) -> Any:
    row = conn.execute("SELECT value_json FROM runtime_state WHERE key=?", (key,)).fetchone()
    return default if row is None else json.loads(row["value_json"])


def _strength_row(conn: sqlite3.Connection) -> sqlite3.Row:
    row = conn.execute(
        "SELECT value_json,mode,authority,source,observed_at FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, STRENGTH_KEY),
    ).fetchone()
    if row is None:
        raise AssertionError("Strength profile row is missing")
    return row


def _strength_value(conn: sqlite3.Connection) -> float:
    return float(json.loads(_strength_row(conn)["value_json"]))


def _stimulus_rows(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    rows = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (ACTOR, "action_completed"),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        evidence = payload.get("training_stimulus")
        if not isinstance(evidence, dict) or evidence.get("domain") != "strength":
            continue
        units = evidence.get("stimulus_units")
        if not isinstance(units, (int, float)) or float(units) <= 0.0:
            continue
        found.append({
            "event_id": int(row["id"]), "sim_time": row["sim_time"],
            "stimulus_units": float(units), "effective_minutes": evidence.get("effective_minutes"),
            "payload": payload,
        })
    found.sort(key=lambda item: (datetime.fromisoformat(item["sim_time"]), item["event_id"]))
    return found


def _settlement_rows(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (ACTOR, SETTLEMENT_EVENT_TYPE),
    ).fetchall()


def _consumed_ids(conn: sqlite3.Connection) -> set[int]:
    consumed: set[int] = set()
    for row in _settlement_rows(conn):
        payload = json.loads(row["payload_json"] or "{}")
        for event_id in payload.get("consumed_stimulus_event_ids") or []:
            if isinstance(event_id, int): consumed.add(event_id)
    return consumed


def _live_baseline(conn: sqlite3.Connection) -> dict[str, Any]:
    strength = _strength_row(conn)
    fatigue_row = conn.execute(
        "SELECT value_json FROM fields WHERE entity_id=? AND field_key=?", (ACTOR, "physiology.fatigue")
    ).fetchone()
    pending = conn.execute(
        """SELECT ai.id,ai.action_type,ai.target_id,ai.duration_minutes,ai.status,ai.planned_sim_time,ai.ended_sim_time
        FROM actor_runtime ar LEFT JOIN action_instances ai ON ai.id=ar.pending_action_id WHERE ar.actor_id=?""",
        (ACTOR,),
    ).fetchone()
    stimulus = _stimulus_rows(conn); consumed = _consumed_ids(conn)
    return {
        "live_read_only": True, "sim_time": _runtime_json(conn, "sim_time"), "speed": _runtime_json(conn, "speed", 1.0),
        "strength": {"value": json.loads(strength["value_json"]), "mode": strength["mode"], "authority": strength["authority"], "source": strength["source"], "observed_at": strength["observed_at"]},
        "fatigue": None if fatigue_row is None else json.loads(fatigue_row["value_json"]),
        "pending_action": dict(pending) if pending is not None and pending["id"] else None,
        "strength_stimulus_count": len(stimulus),
        "unconsumed_strength_stimulus": [{k:v for k,v in item.items() if k != "payload"} for item in stimulus if item["event_id"] not in consumed],
        "settlement_count": len(_settlement_rows(conn)),
    }


def _backup_live_to_copy(live_db: str | Path, copy_db: str | Path) -> None:
    with _ro_connect(live_db) as source:
        destination = sqlite3.connect(copy_db)
        try: source.backup(destination)
        finally: destination.close()


def _check(condition: bool, name: str, evidence: Any = None) -> None:
    print(json.dumps({"checkpoint": name, "ok": bool(condition), "evidence": evidence}, default=str, sort_keys=True))
    if not condition: raise AssertionError(name)


def validate_copy(copy_db: str | Path) -> dict[str, Any]:
    os.environ["OBSERVER_SANDBOX_DB"] = str(copy_db)
    with connect(copy_db) as conn:
        copied_baseline = snapshot(conn, ACTOR); strength_before = _strength_value(conn)
        stimulus = _stimulus_rows(conn); consumed_before = _consumed_ids(conn)
        unconsumed = [item for item in stimulus if item["event_id"] not in consumed_before]
        _check(bool(unconsumed), "real_unconsumed_strength_stimulus_exists", [{k:v for k,v in item.items() if k != "payload"} for item in unconsumed])
        selected = unconsumed[-1]; selected_time = datetime.fromisoformat(selected["sim_time"])
        selected_after = selected["payload"].get("after") or copied_baseline

        _check(recovery_time_factor(0.0) == 0.0, "recovery_curve_at_0h")
        _check(recovery_time_factor(6.0) == 0.0, "recovery_curve_at_6h")
        _check(0.0 < recovery_time_factor(24.0) < 1.0, "recovery_curve_midpoint", recovery_time_factor(24.0))
        _check(recovery_time_factor(48.0) == 1.0, "recovery_curve_at_48h")
        immediate = strength_recovery_realization_evidence(conn, ACTOR, as_of_sim_time=selected_time.isoformat(), state=selected_after)
        six_hour = strength_recovery_realization_evidence(conn, ACTOR, as_of_sim_time=(selected_time+timedelta(hours=6)).isoformat(), state=selected_after)
        mid = strength_recovery_realization_evidence(conn, ACTOR, as_of_sim_time=(selected_time+timedelta(hours=24)).isoformat(), state=selected_after)
        _check(immediate.time_factor == 0.0, "real_stimulus_immediate_time_factor", immediate.__dict__)
        _check(six_hour.time_factor == 0.0, "real_stimulus_6h_time_factor", six_hour.__dict__)
        _check(0.0 < mid.time_factor < 1.0, "real_stimulus_24h_time_factor", mid.__dict__)

        settlement_count_before = len(_settlement_rows(conn)); boundary_trace=[]; positive_result=None
        for index in range(40):
            if selected["event_id"] in _consumed_ids(conn): break
            after = apply_action(conn, Action("rest",240,None,"disposable Strength recovery validation"), ACTOR)
            result = maybe_settle_strength_progression(conn, ACTOR, as_of_sim_time=str(after["sim_time"]), state=after)
            settlement = result.get("settlement") or {}
            trace = {"boundary":index+1,"sim_time":after["sim_time"],"fatigue":after["fatigue"],"energy":after["energy"],"sleepiness":after["sleepiness"],"activation_state":result["state"],"activation_reason":result["reason"],"settlement_status":settlement.get("status"),"consumed_stimulus_event_ids":settlement.get("consumed_stimulus_event_ids") or [],"positive_delta":settlement.get("positive_delta"),"negative_delta":settlement.get("negative_delta"),"net_delta":settlement.get("net_delta")}
            boundary_trace.append(trace); print(json.dumps({"checkpoint":"action_boundary","ok":True,"evidence":trace},sort_keys=True))
            if selected["event_id"] in trace["consumed_stimulus_event_ids"]: positive_result=result; break

        _check(positive_result is not None, "real_stimulus_settled_within_bounded_rest", boundary_trace)
        settlement = positive_result["settlement"]
        _check(positive_result["reason"] == "eligible_stimulus", "eligible_stimulus_reason", positive_result["reason"])
        _check(selected["event_id"] in settlement["consumed_stimulus_event_ids"], "selected_stimulus_consumed", settlement)
        _check(float(settlement["positive_delta"]) > 0.0, "positive_delta_realized", settlement)

        expected_positive=0.0; formula_evidence=[]
        for evidence in settlement.get("positive_evidence") or []:
            expected=BASE_POSITIVE_SCALE*float(evidence["stimulus_units"])*float(evidence["level_factor"])*float(evidence["saturation_factor"])*float(evidence["recovery_factor"])
            record={"expected":expected,"recorded":evidence["realized_delta"],**evidence}; formula_evidence.append(record)
            _check(math.isclose(expected,float(evidence["realized_delta"]),rel_tol=0.0,abs_tol=2e-9),"per_stimulus_formula_matches",record)
            expected_positive += float(evidence["realized_delta"])
        _check(math.isclose(expected_positive,float(settlement["positive_delta"]),rel_tol=0.0,abs_tol=2e-9),"positive_delta_sum_matches",{"expected":expected_positive,"recorded":settlement["positive_delta"]})

        strength_after=_strength_value(conn); expected_after=strength_before+float(settlement["net_delta"])
        _check(math.isclose(strength_after,expected_after,rel_tol=0.0,abs_tol=1e-6),"raw_strength_matches_net_delta",{"before":strength_before,"expected_after":expected_after,"actual_after":strength_after})
        history=conn.execute("""SELECT old_value_json,new_value_json,mode,authority,reason,sim_time FROM character_profile_history WHERE entity_id=? AND field_key=? ORDER BY id DESC LIMIT 1""",(ACTOR,STRENGTH_KEY)).fetchone()
        _check(history is not None,"strength_history_written"); history_dict=dict(history)
        _check(history["mode"]=="simulated","strength_history_mode",history_dict)
        _check(history["authority"]=="strength-progression-settlement-v1","strength_history_authority",history_dict)

        consumed_after=_consumed_ids(conn); _check(selected["event_id"] in consumed_after,"consumed_id_persisted",sorted(consumed_after))
        settlement_count_after=len(_settlement_rows(conn)); same_state=snapshot(conn,ACTOR)
        same_boundary=maybe_settle_strength_progression(conn,ACTOR,as_of_sim_time=str(same_state["sim_time"]),state=same_state)
        _check(same_boundary["state"]=="skipped","same_boundary_skipped",same_boundary)
        _check(same_boundary["reason"]=="same_or_older_boundary","same_boundary_reason",same_boundary)
        _check(len(_settlement_rows(conn))==settlement_count_after,"same_boundary_emits_no_extra_settlement",{"before":settlement_count_after,"after":len(_settlement_rows(conn))})

        recent_at_event=recent_strength_stimulus_units(conn,ACTOR,as_of_sim_time=selected["sim_time"]); selected_level=strength_level_factor(strength_before); selected_saturation=saturation_factor(recent_at_event)
        return {"ok":True,"disposable_production_copy":True,"validation_writes_to_live":False,"model_calls":0,"telegram_calls":0,"copied_baseline":copied_baseline,"real_stimulus":{"event_id":selected["event_id"],"sim_time":selected["sim_time"],"stimulus_units":selected["stimulus_units"],"effective_minutes":selected["effective_minutes"],"recent_stimulus_at_event":recent_at_event,"level_factor_at_copy_start":selected_level.level_factor,"saturation_factor_at_event":selected_saturation},"recovery_curve":{"immediate":immediate.__dict__,"six_hour":six_hour.__dict__,"twenty_four_hour":mid.__dict__},"boundary_trace":boundary_trace,"formula_evidence":formula_evidence,"settlement":settlement,"strength_before":strength_before,"strength_after":strength_after,"settlement_events_before":settlement_count_before,"settlement_events_after":settlement_count_after,"same_boundary_replay":same_boundary,"consumed_once":selected["event_id"] in consumed_after}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument("--live-db",required=True); args=parser.parse_args(); live_db=Path(args.live_db)
    with _ro_connect(live_db) as live: baseline=_live_baseline(live)
    print("--- LIVE READ-ONLY BASELINE ---"); print(json.dumps(baseline,indent=2,sort_keys=True,default=str))
    with tempfile.TemporaryDirectory(prefix="observer-strength-live-cycle-v1-") as tmp:
        copy_db=Path(tmp)/"observer.sqlite3"; _backup_live_to_copy(live_db,copy_db)
        print("--- DISPOSABLE PRODUCTION-COPY VALIDATION ---"); result=validate_copy(copy_db); print(json.dumps(result,indent=2,sort_keys=True,default=str))
    with _ro_connect(live_db) as live: after=_live_baseline(live)
    _check(baseline==after,"live_baseline_unchanged_across_validation",{"before":baseline,"after":after})
    print(json.dumps({"ok":True,"production_mutated":False},sort_keys=True))


if __name__ == "__main__": main()

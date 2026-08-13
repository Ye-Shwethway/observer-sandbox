from __future__ import annotations

import argparse
import json
import math
import sqlite3
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.recovery_realization import recovery_time_factor, strength_recovery_realization_evidence
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.strength_progression import BASE_POSITIVE_SCALE, SETTLEMENT_EVENT_TYPE
from observer_sandbox.strength_progression_activation import maybe_settle_strength_progression

ACTOR = "char_darian"
STRENGTH_KEY = "raps_pa.strength"


def ro(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def strength(conn: sqlite3.Connection) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, STRENGTH_KEY),
    ).fetchone()
    assert row is not None
    return float(json.loads(row["value_json"]))


def stimuli(conn: sqlite3.Connection) -> list[dict]:
    result = []
    for row in conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (ACTOR, "action_completed"),
    ).fetchall():
        payload = json.loads(row["payload_json"] or "{}")
        ev = payload.get("training_stimulus")
        if isinstance(ev, dict) and ev.get("domain") == "strength" and float(ev.get("stimulus_units") or 0) > 0:
            result.append({"id": int(row["id"]), "sim_time": row["sim_time"], "units": float(ev["stimulus_units"]), "effective_minutes": ev.get("effective_minutes"), "payload": payload})
    result.sort(key=lambda x: (datetime.fromisoformat(x["sim_time"]), x["id"]))
    return result


def settlements(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type=?",
        (ACTOR, SETTLEMENT_EVENT_TYPE),
    ).fetchall()


def consumed(conn: sqlite3.Connection) -> set[int]:
    out: set[int] = set()
    for row in settlements(conn):
        for event_id in json.loads(row["payload_json"] or "{}").get("consumed_stimulus_event_ids") or []:
            if isinstance(event_id, int):
                out.add(event_id)
    return out


def baseline(conn: sqlite3.Connection) -> dict:
    runtime = {row["key"]: json.loads(row["value_json"]) for row in conn.execute("SELECT key,value_json FROM runtime_state WHERE key IN (?,?)", ("sim_time", "speed")).fetchall()}
    fatigue = conn.execute("SELECT value_json FROM fields WHERE entity_id=? AND field_key=?", (ACTOR, "physiology.fatigue")).fetchone()
    pending = conn.execute(
        """SELECT ai.id,ai.action_type,ai.target_id,ai.duration_minutes,ai.status,ai.planned_sim_time
        FROM actor_runtime ar LEFT JOIN action_instances ai ON ai.id=ar.pending_action_id WHERE ar.actor_id=?""",
        (ACTOR,),
    ).fetchone()
    unconsumed = [x for x in stimuli(conn) if x["id"] not in consumed(conn)]
    return {
        "sim_time": runtime.get("sim_time"),
        "speed": runtime.get("speed", 1.0),
        "strength": strength(conn),
        "fatigue": None if fatigue is None else json.loads(fatigue["value_json"]),
        "pending_action": dict(pending) if pending is not None and pending["id"] else None,
        "settlement_count": len(settlements(conn)),
        "unconsumed_strength_stimulus": [{"id": x["id"], "sim_time": x["sim_time"], "units": x["units"], "effective_minutes": x["effective_minutes"]} for x in unconsumed],
    }


def backup(live_db: Path, copy_db: Path) -> None:
    with ro(live_db) as source:
        dest = sqlite3.connect(copy_db)
        try:
            source.backup(dest)
        finally:
            dest.close()


def validate(copy_db: Path) -> dict:
    with connect(copy_db) as conn:
        before_state = snapshot(conn, ACTOR)
        before_strength = strength(conn)
        available = [x for x in stimuli(conn) if x["id"] not in consumed(conn)]
        assert available, "no real unconsumed Strength stimulus in copied production DB"
        selected = available[-1]
        t = datetime.fromisoformat(selected["sim_time"])
        post_training = selected["payload"].get("after") or before_state

        assert recovery_time_factor(0) == 0
        assert recovery_time_factor(6) == 0
        assert 0 < recovery_time_factor(24) < 1
        assert recovery_time_factor(48) == 1
        immediate = strength_recovery_realization_evidence(conn, ACTOR, as_of_sim_time=t.isoformat(), state=post_training)
        six = strength_recovery_realization_evidence(conn, ACTOR, as_of_sim_time=(t + timedelta(hours=6)).isoformat(), state=post_training)
        assert immediate.time_factor == 0 and six.time_factor == 0

        trace = []
        settled = None
        for _ in range(40):
            after = apply_action(conn, Action("rest", 240, None, "disposable Strength recovery validation"), ACTOR)
            result = maybe_settle_strength_progression(conn, ACTOR, as_of_sim_time=after["sim_time"], state=after)
            compact = result.get("settlement") or {}
            trace.append({"sim_time": after["sim_time"], "fatigue": after["fatigue"], "reason": result["reason"], "consumed": compact.get("consumed_stimulus_event_ids") or []})
            if selected["id"] in (compact.get("consumed_stimulus_event_ids") or []):
                settled = result
                break
        assert settled is not None, "real Strength stimulus never reached eligible settlement"
        compact = settled["settlement"]
        assert settled["reason"] == "eligible_stimulus"
        assert compact["positive_delta"] > 0
        audit_row = conn.execute("SELECT payload_json FROM events WHERE id=?", (compact["event_id"],)).fetchone()
        assert audit_row is not None
        audit = json.loads(audit_row["payload_json"] or "{}")
        evidence = audit.get("positive_evidence") or []
        assert evidence
        expected_sum = 0.0
        for item in evidence:
            expected = BASE_POSITIVE_SCALE * float(item["stimulus_units"]) * float(item["level_factor"]) * float(item["saturation_factor"]) * float(item["recovery_factor"])
            assert math.isclose(expected, float(item["realized_delta"]), rel_tol=0, abs_tol=2e-9)
            expected_sum += float(item["realized_delta"])
        assert math.isclose(expected_sum, float(compact["positive_delta"]), rel_tol=0, abs_tol=2e-9)
        after_strength = strength(conn)
        assert math.isclose(after_strength, before_strength + float(compact["net_delta"]), rel_tol=0, abs_tol=1e-6)
        history = conn.execute("SELECT mode,authority FROM character_profile_history WHERE entity_id=? AND field_key=? ORDER BY id DESC LIMIT 1", (ACTOR, STRENGTH_KEY)).fetchone()
        assert history is not None and history["mode"] == "simulated" and history["authority"] == "strength-progression-settlement-v1"
        assert selected["id"] in consumed(conn)
        count = len(settlements(conn))
        same = maybe_settle_strength_progression(conn, ACTOR, as_of_sim_time=snapshot(conn, ACTOR)["sim_time"], state=snapshot(conn, ACTOR))
        assert same["state"] == "skipped" and same["reason"] == "same_or_older_boundary"
        assert len(settlements(conn)) == count
        return {
            "ok": True,
            "real_stimulus": {"event_id": selected["id"], "sim_time": selected["sim_time"], "stimulus_units": selected["units"], "effective_minutes": selected["effective_minutes"]},
            "settlement": compact,
            "positive_evidence": evidence,
            "strength_before": before_strength,
            "strength_after": after_strength,
            "boundary_trace": trace,
            "model_calls": 0,
            "telegram_calls": 0,
            "disposable_production_copy": True,
        }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live-db", required=True)
    args = parser.parse_args()
    live_db = Path(args.live_db)
    with ro(live_db) as conn:
        before = baseline(conn)
    print(json.dumps({"live_read_only_baseline": before}, indent=2, sort_keys=True))
    with tempfile.TemporaryDirectory(prefix="observer-strength-live-cycle-") as tmp:
        copy_db = Path(tmp) / "observer.sqlite3"
        backup(live_db, copy_db)
        result = validate(copy_db)
        print(json.dumps(result, indent=2, sort_keys=True))
    with ro(live_db) as conn:
        after = baseline(conn)
    assert before == after, "live production baseline changed during validation"
    print(json.dumps({"ok": True, "production_mutated": False, "live_baseline_unchanged": True}, sort_keys=True))


if __name__ == "__main__":
    main()

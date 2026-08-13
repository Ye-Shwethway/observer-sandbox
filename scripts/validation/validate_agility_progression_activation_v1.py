from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from observer_sandbox.agility_progression import AGILITY_FIELD_KEY, latest_agility_settlement_time
from observer_sandbox.agility_progression_activation import agility_progression_due, maybe_settle_agility_progression
from observer_sandbox.db import connect
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field

ACTOR = "char_darian"
HOME_GYM = "loc_thorne_estate_home_gym"
TARGET = "obj_thorne_estate_gym_speed_agility_station"


def profile_value(conn, key: str) -> float:
    row = conn.execute("SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?", (ACTOR, key)).fetchone()
    assert row is not None
    return float(json.loads(row["value_json"]))


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("temporary database required")

    conn = connect(db_path)
    agility_before = profile_value(conn, AGILITY_FIELD_KEY)
    strength_before = profile_value(conn, "raps_pa.strength")
    stamina_before = profile_value(conn, "raps_pa.stamina")
    set_field(conn, ACTOR, "runtime.location", HOME_GYM)
    set_field(conn, ACTOR, "runtime.current_action", "idle")
    set_field(conn, ACTOR, "needs.energy", 90.0)
    set_field(conn, ACTOR, "needs.sleepiness", 10.0)
    set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="physiology_engine", source="agility-activation-acceptance")
    conn.commit()

    state0 = snapshot(conn, ACTOR)
    boundary0 = str(state0["sim_time"])
    if latest_agility_settlement_time(conn, ACTOR) is None:
        boot = maybe_settle_agility_progression(conn, ACTOR, as_of_sim_time=boundary0, state=state0)
        assert boot["reason"] == "bootstrap"
        assert boot["settlement"]["net_delta"] == 0.0
        assert profile_value(conn, AGILITY_FIELD_KEY) == agility_before

    apply_action(conn, Action("train", 30, TARGET, "agility activation acceptance"), ACTOR)
    row = conn.execute("SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1", (ACTOR,)).fetchone()
    assert row is not None
    event_id = int(row["id"])
    method = json.loads(row["payload_json"])["training_method"]
    assert method["method_id"] == "speed_agility_drills"
    assert method["workload_channels"] == ["conditioning", "movement"]

    event_time = datetime.fromisoformat(row["sim_time"])
    state = {"energy": 90.0, "sleepiness": 10.0, "fatigue": 10.0}
    early_time = (event_time + timedelta(hours=19)).isoformat()
    early = agility_progression_due(conn, ACTOR, as_of_sim_time=early_time, state=state)
    assert event_id not in early.eligible_stimulus_event_ids

    eligible_time = (event_time + timedelta(hours=21)).isoformat()
    due = agility_progression_due(conn, ACTOR, as_of_sim_time=eligible_time, state=state)
    assert due.reason == "eligible_stimulus"
    assert event_id in due.eligible_stimulus_event_ids

    settled = maybe_settle_agility_progression(conn, ACTOR, as_of_sim_time=eligible_time, state=state)
    assert settled["state"] == "settled"
    assert settled["settlement"]["positive_delta"] > 0.0
    assert event_id in settled["settlement"]["consumed_stimulus_event_ids"]
    assert profile_value(conn, AGILITY_FIELD_KEY) > agility_before
    assert profile_value(conn, "raps_pa.strength") == strength_before
    assert profile_value(conn, "raps_pa.stamina") == stamina_before

    replay = maybe_settle_agility_progression(conn, ACTOR, as_of_sim_time=eligible_time, state=state)
    assert replay["state"] == "skipped"
    assert replay["reason"] == "same_or_older_boundary"

    print(json.dumps({"ok": True, "baseline_agility": agility_before, "new_event_id": event_id, "early_19h_eligible": False, "eligible_21h_reason": due.reason, "settlement": settled["settlement"], "strength_unchanged": True, "stamina_unchanged": True, "replay_skipped": True, "model_calls": 0, "telegram_calls": 0, "production_mutated_by_validation": False}, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

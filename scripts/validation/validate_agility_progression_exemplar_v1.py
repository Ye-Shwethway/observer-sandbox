from __future__ import annotations

import json
import math
import os
from datetime import datetime, timedelta
from pathlib import Path

from observer_sandbox.agility_progression import (
    AGILITY_FIELD_KEY,
    BASE_POSITIVE_SCALE,
    LEVEL_EXPONENT,
    NATURAL_CEILING,
    SATURATION_COEFFICIENT,
    SETTLEMENT_SOURCE,
    STIMULUS_MINUTES_PER_UNIT,
    settle_agility_progression,
)
from observer_sandbox.db import connect
from observer_sandbox.recovery_realization import recovery_state_quality
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field


ACTOR = "char_darian"
HOME_GYM = "loc_thorne_estate_home_gym"
SPEED_AGILITY_STATION = "obj_thorne_estate_gym_speed_agility_station"


def profile_value(conn, key: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return float(json.loads(row["value_json"]))


def latest_action(conn):
    row = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
        (ACTOR,),
    ).fetchone()
    assert row is not None
    return row, json.loads(row["payload_json"])


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    conn = connect(db_path)
    agility_before = profile_value(conn, AGILITY_FIELD_KEY)
    strength_before = profile_value(conn, "raps_pa.strength")
    stamina_before = profile_value(conn, "raps_pa.stamina")

    set_field(conn, ACTOR, "runtime.location", HOME_GYM)
    set_field(conn, ACTOR, "runtime.current_action", "idle")
    set_field(conn, ACTOR, "needs.energy", 90.0)
    set_field(conn, ACTOR, "needs.sleepiness", 10.0)
    set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="physiology_engine", source="agility-acceptance")
    conn.commit()

    state0 = snapshot(conn, ACTOR)
    boot_time = str(state0["sim_time"])
    bootstrap = settle_agility_progression(conn, ACTOR, as_of_sim_time=boot_time, state=state0)
    assert bootstrap["status"] == "bootstrapped"
    assert bootstrap["net_delta"] == 0.0
    assert profile_value(conn, AGILITY_FIELD_KEY) == agility_before

    apply_action(conn, Action("train", 30, SPEED_AGILITY_STATION, "agility progression acceptance"), ACTOR)
    row, payload = latest_action(conn)
    method = payload.get("training_method")
    assert isinstance(method, dict)
    assert method["method_id"] == "speed_agility_drills"
    assert method["workload_channels"] == ["conditioning", "movement"]
    assert "speed_agility" in method["tags"]
    assert "training_stimulus" not in payload

    effective_minutes = float(method["effective_load"]["effective_minutes"])
    stimulus_units = round(effective_minutes / STIMULUS_MINUTES_PER_UNIT, 6)
    event_id = int(row["id"])
    event_time = datetime.fromisoformat(row["sim_time"])

    early_state = {"energy": 90.0, "sleepiness": 10.0, "fatigue": 10.0}
    early = settle_agility_progression(
        conn,
        ACTOR,
        as_of_sim_time=(event_time + timedelta(hours=19)).isoformat(),
        state=early_state,
    )
    assert early["positive_delta"] == 0.0
    assert event_id not in early["consumed_stimulus_event_ids"]
    assert profile_value(conn, AGILITY_FIELD_KEY) == agility_before

    eligible_time = (event_time + timedelta(hours=21)).isoformat()
    eligible_state = {"energy": 90.0, "sleepiness": 10.0, "fatigue": 10.0}
    quality, _ = recovery_state_quality(eligible_state)
    level_factor = round(((NATURAL_CEILING - agility_before) / NATURAL_CEILING) ** LEVEL_EXPONENT, 9)
    saturation_factor = round(1.0 / (1.0 + SATURATION_COEFFICIENT * stimulus_units), 9)
    expected_gain = BASE_POSITIVE_SCALE * stimulus_units * level_factor * saturation_factor * quality

    settled = settle_agility_progression(
        conn,
        ACTOR,
        as_of_sim_time=eligible_time,
        state=eligible_state,
    )
    assert settled["status"] == "settled"
    assert settled["consumed_stimulus_event_ids"] == [event_id]
    assert math.isclose(settled["positive_delta"], expected_gain, rel_tol=0.0, abs_tol=1e-8)
    assert math.isclose(profile_value(conn, AGILITY_FIELD_KEY), agility_before + expected_gain, rel_tol=0.0, abs_tol=1e-6)
    assert profile_value(conn, "raps_pa.strength") == strength_before
    assert profile_value(conn, "raps_pa.stamina") == stamina_before

    history = conn.execute(
        "SELECT authority,mode FROM character_profile_history WHERE entity_id=? AND field_key=? ORDER BY id DESC LIMIT 1",
        (ACTOR, AGILITY_FIELD_KEY),
    ).fetchone()
    assert history is not None
    assert history["authority"] == SETTLEMENT_SOURCE
    assert history["mode"] == "simulated"

    replay = settle_agility_progression(conn, ACTOR, as_of_sim_time=eligible_time, state=eligible_state)
    assert replay["status"] == "no_change"
    assert replay["net_delta"] == 0.0

    print(json.dumps({
        "ok": True,
        "validation_db": str(db_path),
        "baseline_agility": agility_before,
        "effective_minutes": effective_minutes,
        "stimulus_units": stimulus_units,
        "level_factor": level_factor,
        "saturation_factor": saturation_factor,
        "recovery_state_quality": quality,
        "expected_gain": round(expected_gain, 9),
        "settlement": settled,
        "strength_unchanged": True,
        "stamina_unchanged": True,
        "replay_noop": True,
        "model_calls": 0,
        "telegram_calls": 0,
        "production_mutated_by_validation": False,
    }, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

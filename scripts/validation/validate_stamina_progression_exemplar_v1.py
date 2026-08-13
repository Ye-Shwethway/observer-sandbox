from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.stamina_progression import STAMINA_FIELD_KEY, STIMULUS_MINUTES_PER_UNIT, stamina_stimulus_events
from observer_sandbox.world import set_field


ACTOR = "char_darian"
HOME_GYM = "loc_thorne_estate_home_gym"
TREADMILL = "obj_thorne_estate_gym_high_speed_treadmill"


def profile_value(conn, key: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return float(json.loads(row["value_json"]))


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("disposable validation required")
    path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(path):
        raise RuntimeError("temporary database required")

    conn = connect(path)
    stamina_before = profile_value(conn, STAMINA_FIELD_KEY)
    strength_before = profile_value(conn, "raps_pa.strength")
    set_field(conn, ACTOR, "runtime.location", HOME_GYM)
    set_field(conn, ACTOR, "runtime.current_action", "idle")
    set_field(conn, ACTOR, "needs.energy", 90.0)
    set_field(conn, ACTOR, "needs.sleepiness", 10.0)
    set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="physiology_engine", source="stamina-exemplar-compatibility")
    conn.commit()

    apply_action(conn, Action("train", 45, TREADMILL, "Stamina exemplar compatibility"), ACTOR)
    row = conn.execute(
        "SELECT id,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
        (ACTOR,),
    ).fetchone()
    assert row is not None
    event_id = int(row["id"])
    payload = json.loads(row["payload_json"])
    method = payload["training_method"]
    assert method["method_id"] == "steady_state_cardio"
    assert method["source"] == "training-method-semantics-v1"
    assert method["workload_channels"] == ["conditioning"]
    assert "training_stimulus" not in payload

    now = str(snapshot(conn, ACTOR)["sim_time"])
    stimuli = {item.event_id: item for item in stamina_stimulus_events(conn, ACTOR, as_of_sim_time=now)}
    assert event_id in stimuli
    item = stimuli[event_id]
    effective_minutes = float(method["effective_load"]["effective_minutes"])
    expected_units = round(effective_minutes / STIMULUS_MINUTES_PER_UNIT, 6)
    assert item.effective_minutes == round(effective_minutes, 6)
    assert item.stimulus_units == expected_units

    assert profile_value(conn, STAMINA_FIELD_KEY) == stamina_before
    assert profile_value(conn, "raps_pa.strength") == strength_before
    print(json.dumps({
        "ok": True,
        "validation_db": str(path),
        "treadmill_method_preserved": True,
        "effective_minutes": effective_minutes,
        "stimulus_units": item.stimulus_units,
        "stamina_unchanged": True,
        "strength_unchanged": True,
        "model_calls": 0,
        "telegram_calls": 0,
        "production_mutated_by_validation": False,
    }, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

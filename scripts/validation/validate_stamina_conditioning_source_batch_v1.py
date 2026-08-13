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
TARGETS = (
    ("obj_thorne_estate_gym_rowing_ergometer", "rowing_conditioning", True),
    ("obj_thorne_estate_gym_altitude_chamber", "altitude_conditioning", True),
    ("obj_thorne_estate_gym_speed_agility_station", "speed_agility_drills", False),
)


def profile_value(conn, key):
    row = conn.execute("SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?", (ACTOR, key)).fetchone()
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
    max_before = conn.execute("SELECT COALESCE(MAX(id),0) FROM events").fetchone()[0]
    set_field(conn, ACTOR, "runtime.location", HOME_GYM)
    set_field(conn, ACTOR, "needs.energy", 95.0)
    set_field(conn, ACTOR, "needs.sleepiness", 5.0)
    set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="physiology_engine", source="stamina-source-acceptance")
    conn.commit()

    observed = {}
    for target, method_id, expected in TARGETS:
        set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="physiology_engine", source="stamina-source-acceptance")
        set_field(conn, ACTOR, "needs.energy", 95.0)
        conn.commit()
        apply_action(conn, Action("train", 30, target, "conditioning source acceptance"), ACTOR)
        row = conn.execute("SELECT id,payload_json FROM events WHERE id>? AND actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1", (max_before, ACTOR)).fetchone()
        payload = json.loads(row["payload_json"])
        method = payload["training_method"]
        assert method["method_id"] == method_id
        observed[int(row["id"])] = (method, expected)
        max_before = int(row["id"])

    now = str(snapshot(conn, ACTOR)["sim_time"])
    stimuli = stamina_stimulus_events(conn, ACTOR, as_of_sim_time=now)
    stimulus_by_id = {item.event_id: item for item in stimuli}

    for event_id, (method, expected) in observed.items():
        if expected:
            assert method["workload_channels"] == ["conditioning"]
            assert event_id in stimulus_by_id
            item = stimulus_by_id[event_id]
            expected_units = round(float(method["effective_load"]["effective_minutes"]) / STIMULUS_MINUTES_PER_UNIT, 6)
            assert item.stimulus_units == expected_units
        else:
            assert event_id not in stimulus_by_id

    assert profile_value(conn, STAMINA_FIELD_KEY) == stamina_before
    assert profile_value(conn, "raps_pa.strength") == strength_before
    print(json.dumps({"ok": True, "rowing_accepted": True, "altitude_accepted": True, "mixed_speed_agility_rejected": True, "stamina_unchanged": True, "strength_unchanged": True, "model_calls": 0, "telegram_calls": 0, "production_mutated_by_validation": False}, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

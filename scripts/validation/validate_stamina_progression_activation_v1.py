from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.simulation import Action, apply_action, set_runtime_value, snapshot
from observer_sandbox.stamina_progression import STAMINA_FIELD_KEY, latest_stamina_settlement_time
from observer_sandbox.stamina_progression_activation import maybe_settle_stamina_progression, stamina_progression_due
from observer_sandbox.world import set_field


ACTOR = "char_darian"
HOME_GYM = "loc_thorne_estate_home_gym"
TREADMILL = "obj_thorne_estate_gym_high_speed_treadmill"
STRENGTH_FIELD = "raps_pa.strength"


def profile_value(conn, key: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return float(json.loads(row["value_json"]))


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    conn = connect(db_path)
    baseline_stamina = profile_value(conn, STAMINA_FIELD_KEY)
    baseline_strength = profile_value(conn, STRENGTH_FIELD)
    set_dynamic_location(conn, ACTOR, HOME_GYM)
    set_field(conn, ACTOR, "runtime.current_action", "idle")
    set_field(conn, ACTOR, "needs.energy", 90.0)
    set_field(conn, ACTOR, "needs.sleepiness", 10.0)
    set_field(
        conn,
        ACTOR,
        "physiology.fatigue",
        0.0,
        authority="physiology_engine",
        source="stamina-activation-acceptance",
    )
    conn.commit()

    state0 = snapshot(conn, ACTOR)
    cursor_before = latest_stamina_settlement_time(conn, ACTOR)
    baseline_mode = "existing_cursor"
    if cursor_before is None:
        bootstrap = maybe_settle_stamina_progression(
            conn,
            ACTOR,
            as_of_sim_time=str(state0["sim_time"]),
            state=state0,
        )
        assert bootstrap["reason"] == "bootstrap"
        assert bootstrap["settlement"]["net_delta"] == 0.0
        baseline_mode = "bootstrap"
    else:
        assert datetime.fromisoformat(cursor_before) <= datetime.fromisoformat(str(state0["sim_time"]))
    assert profile_value(conn, STAMINA_FIELD_KEY) == baseline_stamina
    assert profile_value(conn, STRENGTH_FIELD) == baseline_strength

    apply_action(conn, Action("train", 45, TREADMILL, "activation acceptance treadmill"), ACTOR)
    row = conn.execute(
        "SELECT id,sim_time,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
        (ACTOR,),
    ).fetchone()
    assert row is not None
    event_id = int(row["id"])
    payload = json.loads(row["payload_json"])
    assert payload["training_method"]["method_id"] == "steady_state_cardio"
    assert payload["training_method"]["workload_channels"] == ["conditioning"]

    event_time = datetime.fromisoformat(row["sim_time"])
    early_time = (event_time + timedelta(hours=29)).isoformat()
    early = stamina_progression_due(
        conn,
        ACTOR,
        as_of_sim_time=early_time,
        state=snapshot(conn, ACTOR),
    )
    assert event_id not in early.eligible_stimulus_event_ids

    eligible_time = (event_time + timedelta(hours=31)).isoformat()
    set_runtime_value(conn, "sim_time", eligible_time)
    conn.commit()
    eligible_state = snapshot(conn, ACTOR)
    due = stamina_progression_due(
        conn,
        ACTOR,
        as_of_sim_time=eligible_time,
        state=eligible_state,
    )
    assert due.reason == "eligible_stimulus"
    assert event_id in due.eligible_stimulus_event_ids

    activated = maybe_settle_stamina_progression(
        conn,
        ACTOR,
        as_of_sim_time=eligible_time,
        state=eligible_state,
    )
    settlement = activated["settlement"]
    assert activated["reason"] == "eligible_stimulus"
    assert event_id in settlement["consumed_stimulus_event_ids"]
    assert settlement["positive_delta"] > 0.0
    assert settlement["net_delta"] > 0.0
    assert profile_value(conn, STAMINA_FIELD_KEY) > baseline_stamina
    assert profile_value(conn, STRENGTH_FIELD) == baseline_strength

    repeated = maybe_settle_stamina_progression(
        conn,
        ACTOR,
        as_of_sim_time=eligible_time,
        state=eligible_state,
    )
    assert repeated["reason"] != "eligible_stimulus"
    assert repeated["settlement"] is None or event_id not in repeated["settlement"].get("consumed_stimulus_event_ids", [])

    history = conn.execute(
        "SELECT field_key,old_value_json,new_value_json,mode,authority,reason FROM character_profile_history WHERE entity_id=? AND field_key=? ORDER BY id DESC LIMIT 2",
        (ACTOR, STAMINA_FIELD_KEY),
    ).fetchall()
    assert history
    assert history[0]["mode"] == "simulated"
    assert history[0]["authority"] == "physical_attribute_progression_engine"

    print(json.dumps({
        "ok": True,
        "disposable_production_copy": True,
        "actor_id": ACTOR,
        "baseline_mode": baseline_mode,
        "stamina_before": baseline_stamina,
        "stamina_after": profile_value(conn, STAMINA_FIELD_KEY),
        "strength_unchanged": profile_value(conn, STRENGTH_FIELD) == baseline_strength,
        "stimulus_event_id": event_id,
        "model_calls": 0,
        "telegram_calls": 0,
        "production_mutated_by_validation": False,
    }, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

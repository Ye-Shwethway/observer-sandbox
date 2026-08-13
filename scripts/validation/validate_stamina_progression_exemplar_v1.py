from __future__ import annotations

import json
import math
import os
from datetime import datetime, timedelta
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.recovery_realization import recovery_state_quality
from observer_sandbox.simulation import Action, apply_action, set_runtime_value, snapshot
from observer_sandbox.stamina_progression import (
    BASE_POSITIVE_SCALE,
    LEVEL_EXPONENT,
    NATURAL_CEILING,
    SETTLEMENT_EVENT_TYPE,
    SETTLEMENT_SOURCE,
    STAMINA_FIELD_KEY,
    STIMULUS_MINUTES_PER_UNIT,
    settle_stamina_progression,
)
from observer_sandbox.world import get_field, set_field


ACTOR = "char_darian"
HOME_GYM = "loc_thorne_estate_home_gym"
TREADMILL = "obj_thorne_estate_gym_high_speed_treadmill"
STRENGTH_FIELD = "raps_pa.strength"


def _profile_value(conn, key: str) -> float:
    row = conn.execute(
        "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (ACTOR, key),
    ).fetchone()
    assert row is not None
    return float(json.loads(row["value_json"]))


def _latest_action_payload(conn) -> tuple[int, dict[str, object]]:
    row = conn.execute(
        "SELECT id,payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
        (ACTOR,),
    ).fetchone()
    assert row is not None
    return int(row["id"]), json.loads(row["payload_json"])


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires OBSERVER_VALIDATION_DISPOSABLE=1")

    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError(f"refusing non-temporary validation DB: {db_path}")

    conn = connect(db_path)
    baseline_stamina = _profile_value(conn, STAMINA_FIELD_KEY)
    baseline_strength = _profile_value(conn, STRENGTH_FIELD)
    start = str(get_field(conn, "world_observer_sandbox", "runtime.sim_time", "2025-05-02T00:00:00+00:00"))

    set_field(conn, ACTOR, "runtime.location", HOME_GYM)
    set_field(conn, ACTOR, "runtime.current_action", "idle")
    set_field(conn, ACTOR, "needs.energy", 90.0)
    set_field(conn, ACTOR, "needs.sleepiness", 10.0)
    set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="physiology_engine", source="stamina-acceptance")
    conn.commit()

    boot_state = snapshot(conn, ACTOR)
    start = str(boot_state["sim_time"])
    bootstrap = settle_stamina_progression(conn, ACTOR, as_of_sim_time=start, state=boot_state)
    assert bootstrap["status"] == "bootstrapped"
    assert _profile_value(conn, STAMINA_FIELD_KEY) == baseline_stamina

    apply_action(conn, Action("train", 45, TREADMILL, "conditioning acceptance exemplar"), ACTOR)
    action_event_id, payload = _latest_action_payload(conn)
    method = payload.get("training_method")
    assert isinstance(method, dict)
    assert method["method_id"] == "steady_state_cardio"
    assert method["source"] == "training-method-semantics-v1"
    assert "training_stimulus" not in payload

    effective_minutes = float(method["effective_load"]["effective_minutes"])
    stimulus_units = round(effective_minutes / STIMULUS_MINUTES_PER_UNIT, 6)
    event_time = datetime.fromisoformat(str(payload["action_ended_sim_time"]))
    eligible_time = (event_time + timedelta(hours=31)).isoformat()
    set_runtime_value(conn, "sim_time", eligible_time)
    conn.commit()

    eligible_state = snapshot(conn, ACTOR)
    quality, _ = recovery_state_quality(eligible_state)
    level_factor = round(((NATURAL_CEILING - baseline_stamina) / NATURAL_CEILING) ** LEVEL_EXPONENT, 9)
    saturation_factor = round(1.0 / (1.0 + 0.20 * stimulus_units), 9)
    expected_gain = BASE_POSITIVE_SCALE * stimulus_units * level_factor * saturation_factor * quality

    settlement = settle_stamina_progression(conn, ACTOR, as_of_sim_time=eligible_time, state=eligible_state)
    assert settlement["status"] == "settled"
    assert settlement["consumed_stimulus_event_ids"] == [action_event_id]
    assert math.isclose(settlement["positive_delta"], expected_gain, rel_tol=0.0, abs_tol=1e-8)
    assert math.isclose(settlement["negative_delta"], 0.0, rel_tol=0.0, abs_tol=1e-12)
    assert math.isclose(_profile_value(conn, STAMINA_FIELD_KEY), baseline_stamina + expected_gain, rel_tol=0.0, abs_tol=1e-6)
    assert _profile_value(conn, STRENGTH_FIELD) == baseline_strength

    history = conn.execute(
        "SELECT authority,mode FROM character_profile_history WHERE entity_id=? AND field_key=? ORDER BY id DESC LIMIT 1",
        (ACTOR, STAMINA_FIELD_KEY),
    ).fetchone()
    assert history is not None
    assert history["authority"] == SETTLEMENT_SOURCE
    assert history["mode"] == "simulated"

    replay = settle_stamina_progression(conn, ACTOR, as_of_sim_time=eligible_time, state=eligible_state)
    assert replay["status"] == "no_change"
    assert replay["net_delta"] == 0.0

    settlement_count = conn.execute(
        "SELECT COUNT(*) AS n FROM events WHERE actor_id=? AND event_type=?",
        (ACTOR, SETTLEMENT_EVENT_TYPE),
    ).fetchone()["n"]
    assert int(settlement_count) == 2

    print(json.dumps({
        "ok": True,
        "validation_db": str(db_path),
        "baseline_stamina": baseline_stamina,
        "effective_minutes": effective_minutes,
        "stimulus_units": stimulus_units,
        "recovery_state_quality": quality,
        "level_factor": level_factor,
        "saturation_factor": saturation_factor,
        "expected_gain": round(expected_gain, 9),
        "settlement": settlement,
        "strength_unchanged": True,
        "replay_noop": True,
        "model_calls": 0,
        "telegram_calls": 0,
        "production_mutated_by_validation": False,
    }, sort_keys=True))
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

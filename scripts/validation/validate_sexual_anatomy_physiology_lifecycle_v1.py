from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sexual_anatomy_physiology_lifecycle import maybe_settle_sexual_anatomy_physiology_lifecycle
from observer_sandbox.simulation import snapshot

ACTOR = "char_darian"
FIELDS = ("sexual_anatomy.penis_length_in", "sexual_anatomy.penis_girth_in")
BASELINE_FIELD = "sexual_anatomy.baseline_erectile_function"
CAP_FIELD = "sexual_anatomy.erection_firmness_cap"


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    initialize(db_path)
    with connect(db_path) as conn:
        state = snapshot(conn, ACTOR)
        before = {
            row["field_key"]: row
            for row in conn.execute(
                "SELECT field_key,value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key IN (?,?)",
                (ACTOR, *FIELDS),
            ).fetchall()
        }
        assert float(json.loads(before[FIELDS[0]]["value_json"])) == 10.0
        assert float(json.loads(before[FIELDS[1]]["value_json"])) == 5.0

        functional = {
            row["field_key"]: row
            for row in conn.execute(
                "SELECT field_key,value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key IN (?,?)",
                (ACTOR, BASELINE_FIELD, CAP_FIELD),
            ).fetchall()
        }
        assert float(json.loads(functional[BASELINE_FIELD]["value_json"])) == 95.0
        assert functional[BASELINE_FIELD]["authority"] == "sexual_physiology_engine"
        assert float(json.loads(functional[CAP_FIELD]["value_json"])) == 98.0
        assert functional[CAP_FIELD]["authority"] == "profile_core"

        existing = conn.execute(
            "SELECT id FROM events WHERE actor_id=? AND event_type='sexual_anatomy_physiology_lifecycle_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        result = maybe_settle_sexual_anatomy_physiology_lifecycle(
            conn,
            ACTOR,
            as_of_sim_time=str(state["sim_time"]),
            state=state,
        )
        after = {
            row["field_key"]: row
            for row in conn.execute(
                "SELECT field_key,value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key IN (?,?)",
                (ACTOR, *FIELDS),
            ).fetchall()
        }

        if existing is None:
            assert result["status"] == "bootstrapped"
            assert result["structural_phase"] == "adult_stable"
        else:
            assert result["status"] in {"not_due", "stable"}
        assert float(json.loads(after[FIELDS[0]]["value_json"])) == 10.0
        assert float(json.loads(after[FIELDS[1]]["value_json"])) == 5.0
        assert all(after[key]["mode"] == "simulated" for key in FIELDS)
        assert all(after[key]["authority"] == "sexual_anatomy_lifecycle_engine" for key in FIELDS)
        assert all(after[key]["source"] == "sexual-anatomy-physiology-lifecycle-v1" for key in FIELDS)

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "actor_id": ACTOR,
            "activation_state_at_start": "fresh" if existing is None else "already_active",
            "length_in": 10.0,
            "girth_in": 5.0,
            "baseline_erectile_function": 95.0,
            "erection_firmness_cap": 98.0,
            "functional_values_authored": True,
            "model_calls": 0,
            "telegram_calls": 0,
            "production_mutated_by_validation": False,
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

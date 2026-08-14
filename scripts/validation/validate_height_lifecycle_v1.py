from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.height_lifecycle import maybe_settle_height_lifecycle
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot

ACTOR = "char_darian"
FIELD = "body.height_in"


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    initialize(db_path)
    with connect(db_path) as conn:
        state = snapshot(conn, ACTOR)
        row_before = conn.execute(
            "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key=?",
            (ACTOR, FIELD),
        ).fetchone()
        assert row_before is not None
        height_before = float(json.loads(row_before["value_json"]))
        assert height_before == 76.0

        existing = conn.execute(
            "SELECT id FROM events WHERE actor_id=? AND event_type='height_lifecycle_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        result = maybe_settle_height_lifecycle(
            conn,
            ACTOR,
            as_of_sim_time=str(state["sim_time"]),
            state=state,
        )
        row_after = conn.execute(
            "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key=?",
            (ACTOR, FIELD),
        ).fetchone()
        height_after = float(json.loads(row_after["value_json"]))

        if existing is None:
            assert result["status"] == "bootstrapped"
            assert result["phase"] == "adult_stable"
        else:
            assert result["status"] in {"not_due", "stable"}
        assert height_after == height_before == 76.0
        assert row_after["mode"] == "simulated"
        assert row_after["authority"] == "height_lifecycle_engine"
        assert row_after["source"] == "height-lifecycle-v1"

        latest = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id=? AND event_type='height_lifecycle_settled' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        assert latest is not None
        payload = json.loads(latest["payload_json"] or "{}")
        assert payload["source"] == "height-lifecycle-v1"
        if payload.get("activation_boundary"):
            assert payload["activation_height_in"] == 76.0
            assert payload["phase"] == "adult_stable"
            assert payload["stat_mutated"] is False

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "actor_id": ACTOR,
            "height_before_in": height_before,
            "height_after_in": height_after,
            "activation_state_at_start": "fresh" if existing is None else "already_active",
            "result_status": result["status"],
            "mode": row_after["mode"],
            "authority": row_after["authority"],
            "model_calls": 0,
            "telegram_calls": 0,
            "production_mutated_by_validation": False,
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

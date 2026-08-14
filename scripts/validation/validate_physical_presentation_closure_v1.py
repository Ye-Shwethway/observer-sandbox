from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.physical_presentation import refresh_physical_presentation
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot

ACTOR = "char_darian"


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    initialize(db_path)
    with connect(db_path) as conn:
        state = snapshot(conn, ACTOR)
        structure = conn.execute(
            "SELECT value_json,mode,authority FROM character_profile_values WHERE entity_id=? AND field_key='body.abdominal_structure'",
            (ACTOR,),
        ).fetchone()
        assert structure is not None
        assert json.loads(structure["value_json"]) == "rare 8-pack configuration"
        assert structure["mode"] == "canonical"
        assert structure["authority"] == "profile_core"

        result = refresh_physical_presentation(
            conn,
            ACTOR,
            as_of_sim_time=str(state["sim_time"]),
        )
        definition = conn.execute(
            "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key='body.abdominal_definition'",
            (ACTOR,),
        ).fetchone()
        assert definition is not None
        assert json.loads(definition["value_json"]) == "peak definition"
        assert definition["mode"] == "derived"
        assert definition["authority"] == "appearance_engine"
        assert definition["source"] == "physical-presentation-v1"

        schema = {
            row["field_key"]: row
            for row in conn.execute(
                "SELECT field_key,default_mode,default_authority,sensitivity FROM profile_field_definitions WHERE field_key IN ('appearance.skin_quality','appearance.pars','sexual_anatomy.sensitivity')"
            ).fetchall()
        }
        assert schema["appearance.skin_quality"]["default_mode"] == "canonical"
        assert schema["appearance.skin_quality"]["default_authority"] == "profile_core"
        assert schema["appearance.pars"]["default_mode"] == "canonical"
        assert schema["appearance.pars"]["default_authority"] == "profile_core"
        assert schema["sexual_anatomy.sensitivity"]["default_authority"] == "sexual_physiology_engine"
        assert schema["sexual_anatomy.sensitivity"]["sensitivity"] == "intimate"

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "actor_id": ACTOR,
            "abdominal_structure": json.loads(structure["value_json"]),
            "abdominal_definition": json.loads(definition["value_json"]),
            "physical_profile_completion": True,
            "model_calls": 0,
            "telegram_calls": 0,
            "production_mutated_by_validation": False
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

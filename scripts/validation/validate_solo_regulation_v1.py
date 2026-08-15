from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.observer_query import recent_history
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, set_runtime_value, snapshot
from observer_sandbox.solo_sexual_regulation import solo_sexual_regulation_context
from observer_sandbox.world import set_field

ACTOR = "char_darian"
PRIVATE_ROOM = "loc_thorne_estate_master_suite"
SECLUDED_ROOM = "loc_thorne_estate_training_hall"
OTHER_PERSONAL_ROOM = "loc_thorne_estate_quasi_room"


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    initialize(db_path)
    with connect(db_path) as conn:
        before_events = int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])

        # Establish deterministic eligibility only on the disposable copy.
        conn.execute(
            "DELETE FROM action_instances WHERE actor_id=? AND action_type='self_satisfaction'",
            (ACTOR,),
        )
        # Reset the derived rolling metric so this validation proves that the
        # candidate completion path rewrites it under the current authority.
        conn.execute(
            "UPDATE character_profile_values SET value_json='0' WHERE entity_id=? AND field_key='raps_sa.self_satisfaction_weekly'",
            (ACTOR,),
        )
        set_dynamic_location(conn, ACTOR, PRIVATE_ROOM)
        set_field(conn, ACTOR, "needs.energy", 100.0, authority="validation_fixture", source="solo-regulation-acceptance")
        set_field(conn, ACTOR, "needs.sleepiness", 0.0, authority="validation_fixture", source="solo-regulation-acceptance")
        set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="validation_fixture", source="solo-regulation-acceptance")
        conn.commit()

        state = snapshot(conn, ACTOR)
        context = solo_sexual_regulation_context(conn, ACTOR, state=state)
        assert context["adult"] is True
        assert context["private_environment"]["safe_private"] is True
        assert context["cooldown_remaining_hours"] == 0.0
        assert context["available_now"] is True
        assert context["drive_components"]["age_bonus"] > 0.0
        assert context["drive_components"]["recovery_bonus"] > 0.0
        assert context["drive_components"]["solitude_bonus"] >= 0.0
        assert any(option["action"] == "self_satisfaction" for option in action_options(conn, ACTOR))

        # Privacy suitability is authored independently of generic access class.
        set_dynamic_location(conn, ACTOR, SECLUDED_ROOM)
        conn.commit()
        secluded = solo_sexual_regulation_context(conn, ACTOR, state=snapshot(conn, ACTOR))
        assert secluded["private_environment"]["access"] == "restricted"
        assert secluded["private_environment"]["safe_private"] is True

        set_dynamic_location(conn, ACTOR, OTHER_PERSONAL_ROOM)
        conn.commit()
        other_personal = solo_sexual_regulation_context(conn, ACTOR, state=snapshot(conn, ACTOR))
        assert other_personal["private_environment"]["access"] == "private"
        assert other_personal["private_environment"]["privacy_policy"] == "personal_other"
        assert other_personal["private_environment"]["safe_private"] is False

        set_dynamic_location(conn, ACTOR, PRIVATE_ROOM)
        conn.commit()
        structural_before = conn.execute(
            """
            SELECT field_key,value_json FROM character_profile_values
            WHERE entity_id=? AND field_key IN (
                'sexual_anatomy.penis_length_in','sexual_anatomy.penis_girth_in',
                'sexual_anatomy.baseline_erectile_function','sexual_anatomy.erection_firmness_cap'
            ) ORDER BY field_key
            """,
            (ACTOR,),
        ).fetchall()
        structural_before = [(row["field_key"], row["value_json"]) for row in structural_before]

        action = Action("self_satisfaction", 15, None, "private self-regulation")
        apply_action(conn, action, ACTOR)
        weekly = conn.execute(
            "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id=? AND field_key='raps_sa.self_satisfaction_weekly'",
            (ACTOR,),
        ).fetchone()
        assert weekly is not None
        assert int(json.loads(weekly["value_json"])) >= 1
        assert weekly["mode"] == "simulated"
        assert weekly["authority"] == "sexual_behavior_engine"
        assert weekly["source"] == "solo-sexual-regulation-v2-naturalism"

        release_time = datetime.fromisoformat(snapshot(conn, ACTOR)["sim_time"])
        set_runtime_value(conn, "sim_time", (release_time + timedelta(hours=2)).isoformat())
        conn.commit()
        same_day = solo_sexual_regulation_context(conn, ACTOR, state=snapshot(conn, ACTOR))
        assert same_day["recent_24h_count"] == 1
        assert same_day["cooldown_remaining_hours"] == 0.0
        assert same_day["available_now"] is True

        owner_history = recent_history(conn, character_id=ACTOR, limit=12, role="owner")
        allowed_history = recent_history(conn, character_id=ACTOR, limit=12, role="allowed")
        assert any(row.get("action") == "self_satisfaction" for row in owner_history)
        assert all(row.get("action") != "self_satisfaction" for row in allowed_history)

        sexual = profile_section(conn, ACTOR, "sexual", role="owner")
        keys = {item["field_key"] for item in sexual["content"]}
        assert "raps_sa.self_satisfaction_weekly" in keys
        assert "sexual_state.solo_regulation_drive" in keys

        structural_after = conn.execute(
            """
            SELECT field_key,value_json FROM character_profile_values
            WHERE entity_id=? AND field_key IN (
                'sexual_anatomy.penis_length_in','sexual_anatomy.penis_girth_in',
                'sexual_anatomy.baseline_erectile_function','sexual_anatomy.erection_firmness_cap'
            ) ORDER BY field_key
            """,
            (ACTOR,),
        ).fetchall()
        structural_after = [(row["field_key"], row["value_json"]) for row in structural_after]
        assert structural_after == structural_before
        assert int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]) > before_events

        print(json.dumps({
            "ok": True,
            "disposable_production_copy": True,
            "deterministic_disposable_preconditions": True,
            "adult_gate": True,
            "private_activity_policy": True,
            "secluded_non_bathroom_location": True,
            "other_personal_room_excluded": True,
            "young_recovery_positive_modifiers": True,
            "same_day_repeat_can_be_legal": True,
            "rolling_metric_updated": True,
            "owner_observer_visible": True,
            "allowed_observer_hidden": True,
            "structural_anatomy_unchanged": True,
            "model_calls": 0,
            "production_mutated_by_validation": False
        }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

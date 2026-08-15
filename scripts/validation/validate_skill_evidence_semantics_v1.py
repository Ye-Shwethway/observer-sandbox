from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import settle_skill_progression
from observer_sandbox.world import set_field

ACTOR = "char_darian"
SKILL = "technology"
COMMS = "loc_thorne_estate_comms"
PRACTICE_CONSOLE = "obj_thorne_estate_comms_diagnostic_practice_console"
ORDINARY_TERMINAL = "obj_thorne_estate_comms_secure_terminal"


def _skill(conn):
    row = conn.execute(
        "SELECT score,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, SKILL),
    ).fetchone()
    if row is None:
        raise AssertionError("Technology skill is not represented")
    return row


def _last_action_payload(conn, action_name: str) -> dict:
    rows = conn.execute(
        "SELECT payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC",
        (ACTOR,),
    ).fetchall()
    for row in rows:
        payload = json.loads(row["payload_json"] or "{}")
        if payload.get("action") == action_name:
            return payload
    raise AssertionError(f"No {action_name} event found")


def main() -> int:
    if os.environ.get("OBSERVER_VALIDATION_DISPOSABLE") != "1":
        raise RuntimeError("validator requires disposable mode")
    db_path = Path(os.environ["OBSERVER_SANDBOX_DB"]).resolve()
    if "/tmp/" not in str(db_path):
        raise RuntimeError("refusing non-temporary validation DB")

    with connect(db_path) as conn:
        before = _skill(conn)
        before_score = float(before["score"])
        before_experience = before["experience"]

    initialize(db_path)
    with connect(db_path) as conn:
        activated = _skill(conn)
        assert float(activated["score"]) == before_score
        assert activated["experience"] == before_experience
        metadata = json.loads(activated["metadata_json"] or "{}")
        assert metadata.get("progression_active") is True

        target = conn.execute(
            "SELECT capabilities_json,definition_id FROM entities WHERE id=?",
            (PRACTICE_CONSOLE,),
        ).fetchone()
        assert target is not None
        assert "practice" in json.loads(target["capabilities_json"])
        assert target["definition_id"] == "skill_practice:systems_diagnostic_practice"

        set_dynamic_location(conn, ACTOR, COMMS)
        set_field(conn, ACTOR, "needs.energy", 100.0, authority="validation_fixture", source="skill-evidence-semantics-v1-acceptance")
        set_field(conn, ACTOR, "needs.sleepiness", 0.0, authority="validation_fixture", source="skill-evidence-semantics-v1-acceptance")
        set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="validation_fixture", source="skill-evidence-semantics-v1-acceptance")
        conn.commit()

        options = action_options(conn, ACTOR)
        practice_targets = {row.get("target") for row in options if row.get("action") == "practice"}
        assert PRACTICE_CONSOLE in practice_targets
        assert ORDINARY_TERMINAL not in practice_targets

        # Generic object use is deliberately not learning evidence.
        apply_action(conn, Action("use", 20, ORDINARY_TERMINAL, "disposable ordinary-use negative control"), ACTOR)
        use_payload = _last_action_payload(conn, "use")
        assert "skill_practice" not in use_payload
        use_as_of = str(snapshot(conn, ACTOR)["sim_time"])
        negative = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=use_as_of)
        assert negative["settled"] is False
        assert negative["reason"] == "no_new_learning_evidence"
        assert float(_skill(conn)["score"]) == before_score

        # Purpose-built practice emits typed evidence and progresses Technology.
        apply_action(conn, Action("practice", 30, PRACTICE_CONSOLE, "disposable systems diagnostic practice"), ACTOR)
        practice_payload = _last_action_payload(conn, "practice")
        evidence = practice_payload.get("skill_practice")
        assert isinstance(evidence, dict)
        assert evidence["source"] == "skill-evidence-semantics-v1"
        assert evidence["method_id"] == "systems_diagnostic_practice"
        assert evidence["skill_relevance"] == {"technology": 1.0}
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert result["evidence"][0]["evidence_kind"] == "skill_practice"
        progressed = _skill(conn)
        progressed_score = float(progressed["score"])
        progressed_experience = float(progressed["experience"])
        assert progressed_score > before_score
        assert progressed_experience > float(before_experience or 0.0)

        duplicate = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert duplicate["settled"] is False
        assert duplicate["reason"] == "no_new_learning_evidence"

    initialize(db_path)
    with connect(db_path) as conn:
        persisted = _skill(conn)
        assert float(persisted["score"]) == progressed_score
        assert float(persisted["experience"]) == progressed_experience

    print(json.dumps({
        "ok": True,
        "disposable_production_copy": True,
        "technology_activation_zero_gain": True,
        "purpose_built_practice_target_seeded": True,
        "generic_use_not_learning_evidence": True,
        "structured_practice_evidence_emitted": True,
        "future_practice_progressed_technology": True,
        "double_count_blocked": True,
        "reinitialize_preserved_progression": True,
        "production_mutated_by_validation": False,
        "model_calls": 0
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

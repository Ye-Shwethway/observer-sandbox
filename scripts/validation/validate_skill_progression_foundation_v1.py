from __future__ import annotations

import json
import os
from pathlib import Path

from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.skill_progression import SETTLEMENT_EVENT_TYPE, settle_skill_progression
from observer_sandbox.world import set_field

ACTOR = "char_darian"
SKILL = "hand_to_hand_combat"
HOME_GYM = "loc_thorne_estate_home_gym"
HEAVY_BAG = "obj_thorne_estate_gym_heavy_bag"


def _skill(conn):
    row = conn.execute(
        "SELECT score,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, SKILL),
    ).fetchone()
    if row is None:
        raise AssertionError("Hand-to-Hand Combat skill is not represented")
    return row


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

    # Candidate initialization is the migration/activation boundary. It must
    # preserve represented proficiency and existing experience while recording
    # one zero-gain bootstrap cursor over historical eligible evidence.
    initialize(db_path)
    with connect(db_path) as conn:
        activated = _skill(conn)
        assert float(activated["score"]) == before_score
        assert activated["experience"] == before_experience
        metadata = json.loads(activated["metadata_json"] or "{}")
        assert metadata.get("progression_active") is True
        bootstrap_rows = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
            (ACTOR, SETTLEMENT_EVENT_TYPE),
        ).fetchall()
        matching = [
            json.loads(row["payload_json"] or "{}")
            for row in bootstrap_rows
            if json.loads(row["payload_json"] or "{}").get("skill_key") == SKILL
        ]
        assert matching
        assert matching[-1]["bootstrap"] is True
        assert matching[-1]["score_delta"] == 0.0
        assert matching[-1]["experience_gain"] == 0.0

        # Establish deterministic training preconditions only on the disposable
        # copy. Production itself is never moved, trained, accelerated or edited.
        set_dynamic_location(conn, ACTOR, HOME_GYM)
        set_field(conn, ACTOR, "needs.energy", 100.0, authority="validation_fixture", source="skill-progression-acceptance")
        set_field(conn, ACTOR, "needs.sleepiness", 0.0, authority="validation_fixture", source="skill-progression-acceptance")
        set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="validation_fixture", source="skill-progression-acceptance")
        conn.commit()

        apply_action(conn, Action("train", 30, HEAVY_BAG, "disposable skill progression acceptance"), ACTOR)
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert result["evidence"]
        assert result["evidence"][0]["method_id"] == "heavy_bag_rounds"
        progressed = _skill(conn)
        progressed_score = float(progressed["score"])
        progressed_experience = float(progressed["experience"])
        assert progressed_score > before_score
        assert progressed_experience > float(before_experience or 0.0)

        duplicate = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert duplicate["settled"] is False
        assert duplicate["reason"] == "no_new_learning_evidence"

    # Ordinary re-initialization/deployment must not reset earned skill state.
    initialize(db_path)
    with connect(db_path) as conn:
        persisted = _skill(conn)
        assert float(persisted["score"]) == progressed_score
        assert float(persisted["experience"]) == progressed_experience

    print(json.dumps({
        "ok": True,
        "disposable_production_copy": True,
        "bootstrap_zero_gain": True,
        "historical_evidence_not_retroactive": True,
        "future_combat_training_progressed": True,
        "method_semantics_used": True,
        "double_count_blocked": True,
        "reinitialize_preserved_progression": True,
        "production_mutated_by_validation": False,
        "model_calls": 0
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

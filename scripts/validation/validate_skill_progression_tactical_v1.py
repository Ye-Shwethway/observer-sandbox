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
SKILL = "tactical_planning"
TRAINING_HALL = "loc_thorne_estate_training_hall"
VR_TACTICAL = "obj_thorne_estate_training_vr_tactical_sim"
COMBAT_MAT = "obj_thorne_estate_training_combat_mat"


def _skill(conn):
    row = conn.execute(
        "SELECT score,experience,metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
        (ACTOR, SKILL),
    ).fetchone()
    if row is None:
        raise AssertionError("Tactical Planning skill is not represented")
    return row


def _matching_settlements(conn):
    rows = conn.execute(
        "SELECT payload_json FROM events WHERE actor_id=? AND event_type=? ORDER BY id",
        (ACTOR, SETTLEMENT_EVENT_TYPE),
    ).fetchall()
    return [
        json.loads(row["payload_json"] or "{}")
        for row in rows
        if json.loads(row["payload_json"] or "{}").get("skill_key") == SKILL
    ]


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

    # Candidate initialize is idempotent. On a mature production copy the
    # activation/bootstrap settlement may no longer be the latest settlement,
    # so acceptance proves that the zero-gain bootstrap exists rather than
    # incorrectly requiring it to be last forever.
    initialize(db_path)
    with connect(db_path) as conn:
        activated = _skill(conn)
        assert float(activated["score"]) == before_score
        assert activated["experience"] == before_experience
        metadata = json.loads(activated["metadata_json"] or "{}")
        assert metadata.get("progression_active") is True
        matching = _matching_settlements(conn)
        assert matching
        bootstrap = next((item for item in matching if item.get("bootstrap") is True), None)
        assert bootstrap is not None
        assert bootstrap["score_delta"] == 0.0
        assert bootstrap["experience_gain"] == 0.0

        # Deterministic fixture state exists only on the disposable copy.
        set_dynamic_location(conn, ACTOR, TRAINING_HALL)
        set_field(conn, ACTOR, "needs.energy", 100.0, authority="validation_fixture", source="tactical-skill-progression-acceptance")
        set_field(conn, ACTOR, "needs.sleepiness", 0.0, authority="validation_fixture", source="tactical-skill-progression-acceptance")
        set_field(conn, ACTOR, "physiology.fatigue", 0.0, authority="validation_fixture", source="tactical-skill-progression-acceptance")
        conn.commit()

        # A non-tactical combat method must not count.
        apply_action(conn, Action("train", 30, COMBAT_MAT, "disposable negative-control fixture"), ACTOR)
        non_tactical_as_of = str(snapshot(conn, ACTOR)["sim_time"])
        negative = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=non_tactical_as_of)
        assert negative["settled"] is False
        assert negative["reason"] == "no_new_learning_evidence"
        assert float(_skill(conn)["score"]) == before_score

        # A future direct Tactical method must progress score and experience.
        apply_action(conn, Action("train", 30, VR_TACTICAL, "disposable tactical progression acceptance"), ACTOR)
        as_of = str(snapshot(conn, ACTOR)["sim_time"])
        result = settle_skill_progression(conn, ACTOR, SKILL, as_of_sim_time=as_of)
        assert result["settled"] is True
        assert result["bootstrap"] is False
        assert result["score_delta"] > 0.0
        assert result["experience_gain"] > 0.0
        assert result["evidence"]
        assert result["evidence"][0]["method_id"] == "vr_tactical_drills"
        assert float(result["evidence"][0]["method_weight"]) == 1.0
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
        "tactical_bootstrap_zero_gain": True,
        "historical_evidence_not_retroactive": True,
        "non_tactical_combat_rejected": True,
        "future_vr_tactical_training_progressed": True,
        "method_semantics_used": True,
        "double_count_blocked": True,
        "reinitialize_preserved_progression": True,
        "production_mutated_by_validation": False,
        "model_calls": 0
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

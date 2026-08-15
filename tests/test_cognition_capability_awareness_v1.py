from __future__ import annotations

import json

import pytest

from observer_sandbox.cognition_capability_awareness import cognition_capability_awareness
from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot


ACTOR = "char_cognition_capability_fixture"


def _seed_actor(conn) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
        (ACTOR, "character", "Cognition Capability Fixture", "{}", "[]"),
    )
    conn.execute(
        "INSERT INTO character_profiles(entity_id,profile_schema_version,canonical_revision,status) VALUES(?,?,?,?)",
        (ACTOR, 1, "cognition-capability-awareness-test", "active"),
    )
    conn.execute(
        "INSERT INTO character_skills(entity_id,skill_key,category,score,experience,metadata_json) VALUES(?,?,?,?,?,?)",
        (ACTOR, "technology", "technical", 82.0, None, "{}"),
    )
    values = {
        "raps_ia.iq": 140.0,
        "raps_ia.problem_solving": 88.0,
        "raps_ma.focus": 92.0,
        "raps_ma.adaptability": 85.0,
        "raps_ia.creativity": 85.0,
        "raps_ma.emotional_stability": 85.0,
        "raps_ma.stress_management": 85.0,
        "raps_ia.tactical_thinking": 92.0,
        # Explicit legacy compatibility value: not authoritative Skill proficiency.
        "raps_ia.technological_aptitude": 5.0,
    }
    for field_key, value in values.items():
        conn.execute(
            """
            INSERT INTO character_profile_values(
                entity_id,field_key,value_json,mode,authority,source
            ) VALUES(?,?,?,?,?,?)
            """,
            (ACTOR, field_key, json.dumps(value), "static", "test", "test"),
        )
    conn.commit()


def _technology(awareness):
    return next(item for item in awareness["skills"] if item["skill_id"] == "technology")


def test_awareness_exposes_skill_semantics_not_only_score(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        awareness = cognition_capability_awareness(conn, ACTOR)

        technology = _technology(awareness)
        assert technology["proficiency"]["score"] == pytest.approx(82.0)
        assert technology["proficiency"]["grade"] == "A"
        assert technology["proficiency"]["label"] == "Advanced"
        assert "advanced" in technology["proficiency"]["behavioral_anchor"]["supported_challenges"]
        assert technology["definition"]
        assert technology["scope_excludes"]
        assert any(
            app["application_id"] == "diagnose_known_system_fault"
            for app in technology["applications"]
        )
        diagnostic = next(
            app
            for app in technology["applications"]
            if app["application_id"] == "diagnose_known_system_fault"
        )
        assert "technical_system_represented" in diagnostic["required_context_tags"]
        assert diagnostic["required_resource_mode"] == "any"
        assert "diagnostic_interface" in diagnostic["required_resource_capabilities_any"]


def test_reasoning_profile_exposes_iq_and_supporting_factors_without_skill_substitution(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        awareness = cognition_capability_awareness(conn, ACTOR)

        factors = awareness["reasoning_profile"]["factors"]
        assert factors["general_reasoning_capacity"] == {
            "field_key": "raps_ia.iq",
            "value": 140.0,
        }
        assert factors["problem_solving"]["value"] == pytest.approx(88.0)
        assert factors["focus"]["value"] == pytest.approx(92.0)

        technology = _technology(awareness)
        assert technology["proficiency"]["score"] == pytest.approx(82.0)
        assert all(
            item["field_key"] != "raps_ia.technological_aptitude"
            for item in technology["supporting_attributes"]
        )
        principles = " ".join(awareness["reasoning_profile"]["principles"])
        assert "does not create missing knowledge or learned Skill proficiency" in principles
        assert "deterministic engine authority" in principles


def test_iq_change_does_not_rewrite_skill_proficiency_or_anchor(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        before = cognition_capability_awareness(conn, ACTOR)
        conn.execute(
            "UPDATE character_profile_values SET value_json=? WHERE entity_id=? AND field_key='raps_ia.iq'",
            (json.dumps(90.0), ACTOR),
        )
        after = cognition_capability_awareness(conn, ACTOR)

        before_technology = _technology(before)
        after_technology = _technology(after)
        assert before_technology["proficiency"] == after_technology["proficiency"]
        assert before["reasoning_profile"]["factors"]["general_reasoning_capacity"]["value"] == 140.0
        assert after["reasoning_profile"]["factors"]["general_reasoning_capacity"]["value"] == 90.0


def test_undefined_skill_is_reported_not_invented(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        conn.execute(
            "INSERT INTO character_skills(entity_id,skill_key,category,score,experience,metadata_json) VALUES(?,?,?,?,?,?)",
            (ACTOR, "future_skill_without_definition", "test", 55.0, None, "{}"),
        )
        awareness = cognition_capability_awareness(conn, ACTOR)

        assert "future_skill_without_definition" in awareness["unresolved_skills"]
        assert all(
            item["skill_id"] != "future_skill_without_definition"
            for item in awareness["skills"]
        )


def test_awareness_is_read_only(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        before = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "history": conn.execute("SELECT COUNT(*) FROM character_profile_history").fetchone()[0],
            "skill": tuple(
                conn.execute(
                    "SELECT score,experience FROM character_skills WHERE entity_id=? AND skill_key='technology'",
                    (ACTOR,),
                ).fetchone()
            ),
        }
        cognition_capability_awareness(conn, ACTOR)
        after = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "history": conn.execute("SELECT COUNT(*) FROM character_profile_history").fetchone()[0],
            "skill": tuple(
                conn.execute(
                    "SELECT score,experience FROM character_skills WHERE entity_id=? AND skill_key='technology'",
                    (ACTOR,),
                ).fetchone()
            ),
        }
        assert before == after


def test_model_decision_enrichment_includes_semantic_capability_awareness(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        enriched = ModelDecisionProvider(conn, character_id="char_darian")._enrich_state(state)

        awareness = enriched["capability_awareness"]
        assert awareness["revision"] == "cognition-capability-awareness-v1"
        assert awareness["actor_id"] == "char_darian"
        assert len(awareness["skills"]) >= 6
        assert _technology(awareness)["applications"]
        assert awareness["reasoning_profile"]["factors"]["general_reasoning_capacity"]["value"] is not None

from __future__ import annotations

import json

import pytest

from observer_sandbox.actor_skill_capability import (
    ActorSkillCapabilityError,
    assess_actor_skill_application,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


ACTOR = "char_capability_fixture"
SKILL = "technology"
APPLICATION = "diagnose_known_system_fault"
CONTEXT = {"technical_system_represented", "diagnostic_evidence_available"}
RESOURCES = {"diagnostic_interface", "technical_documentation"}


def _seed_actor(conn) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
        (ACTOR, "character", "Capability Fixture", "{}", "[]"),
    )
    conn.execute(
        "INSERT INTO character_profiles(entity_id,profile_schema_version,canonical_revision,status) VALUES(?,?,?,?)",
        (ACTOR, 1, "capability-adapter-test", "active"),
    )
    conn.execute(
        "INSERT INTO character_skills(entity_id,skill_key,category,score,experience,metadata_json) VALUES(?,?,?,?,?,?)",
        (ACTOR, SKILL, "technical", 82.0, None, "{}"),
    )
    for field_key, value in (
        ("raps_ia.problem_solving", 88.0),
        ("raps_ma.focus", 92.0),
        ("raps_ia.creativity", 1.0),
    ):
        conn.execute(
            """
            INSERT INTO character_profile_values(
                entity_id,field_key,value_json,mode,authority,source
            ) VALUES(?,?,?,?,?,?)
            """,
            (ACTOR, field_key, json.dumps(value), "static", "test", "test"),
        )
    conn.commit()


def _assess(conn, **kwargs):
    return assess_actor_skill_application(
        conn,
        ACTOR,
        SKILL,
        APPLICATION,
        challenge_class=kwargs.pop("challenge_class", "advanced"),
        context_tags=kwargs.pop("context_tags", CONTEXT),
        resource_capabilities=kwargs.pop("resource_capabilities", RESOURCES),
        **kwargs,
    )


def test_adapter_reads_authoritative_skill_and_declared_attributes(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        result = _assess(conn)

        assert result.status == "supported"
        assert result.skill_score == pytest.approx(82.0)
        assert result.proficiency_grade == "A"
        assert dict(result.attribute_inputs) == {
            "raps_ia.problem_solving": 88.0,
            "raps_ma.focus": 92.0,
        }


def test_adapter_ignores_undeclared_profile_fields(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        before = _assess(conn)
        conn.execute(
            "UPDATE character_profile_values SET value_json=? WHERE entity_id=? AND field_key='raps_ia.creativity'",
            (json.dumps(99.0), ACTOR),
        )
        after = _assess(conn)

        assert before.status == after.status == "supported"
        assert dict(before.attribute_inputs) == dict(after.attribute_inputs)
        assert "raps_ia.creativity" not in dict(after.attribute_inputs)


def test_missing_declared_attribute_is_transparent_non_gating_none(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        conn.execute(
            "DELETE FROM character_profile_values WHERE entity_id=? AND field_key='raps_ma.focus'",
            (ACTOR,),
        )
        result = _assess(conn)

        assert result.status == "supported"
        assert dict(result.attribute_inputs) == {
            "raps_ia.problem_solving": 88.0,
            "raps_ma.focus": None,
        }


def test_missing_authoritative_skill_state_fails_closed_without_fabrication(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        conn.execute(
            "DELETE FROM character_skills WHERE entity_id=? AND skill_key=?",
            (ACTOR, SKILL),
        )
        with pytest.raises(ActorSkillCapabilityError, match="no authoritative Skill state"):
            _assess(conn)


def test_adapter_does_not_guess_context_or_resources_from_world_state(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        result = _assess(conn, context_tags=set(), resource_capabilities=set())

        assert result.status == "unsupported"
        assert set(result.missing_context_tags) == CONTEXT
        assert "required_resource_capability_missing" in result.reasons


def test_assessment_is_read_only_and_emits_no_evidence(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        before = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "history": conn.execute("SELECT COUNT(*) FROM character_profile_history").fetchone()[0],
            "score": conn.execute(
                "SELECT score FROM character_skills WHERE entity_id=? AND skill_key=?",
                (ACTOR, SKILL),
            ).fetchone()[0],
            "values": conn.execute(
                "SELECT field_key,value_json FROM character_profile_values WHERE entity_id=? ORDER BY field_key",
                (ACTOR,),
            ).fetchall(),
        }

        result = _assess(conn)

        after = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "history": conn.execute("SELECT COUNT(*) FROM character_profile_history").fetchone()[0],
            "score": conn.execute(
                "SELECT score FROM character_skills WHERE entity_id=? AND skill_key=?",
                (ACTOR, SKILL),
            ).fetchone()[0],
            "values": conn.execute(
                "SELECT field_key,value_json FROM character_profile_values WHERE entity_id=? ORDER BY field_key",
                (ACTOR,),
            ).fetchall(),
        }

        assert result.status == "supported"
        assert before["events"] == after["events"]
        assert before["history"] == after["history"]
        assert before["score"] == after["score"]
        assert [tuple(row) for row in before["values"]] == [tuple(row) for row in after["values"]]


def test_non_numeric_declared_attribute_fails_clearly(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        conn.execute(
            "UPDATE character_profile_values SET value_json=? WHERE entity_id=? AND field_key='raps_ma.focus'",
            (json.dumps("high"), ACTOR),
        )
        with pytest.raises(ActorSkillCapabilityError, match="must be numeric"):
            _assess(conn)

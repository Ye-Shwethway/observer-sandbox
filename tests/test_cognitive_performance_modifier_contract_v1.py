from __future__ import annotations

import copy
import json

import pytest

from observer_sandbox.actor_skill_capability import assess_actor_skill_application
from observer_sandbox.cognitive_performance import (
    CognitivePerformanceValidationError,
    assess_actor_cognitive_performance,
    assess_cognitive_performance,
    load_cognitive_performance_config,
    validate_cognitive_performance_config,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


ACTOR = "char_cognitive_performance_fixture"
SKILL = "technology"
APPLICATION = "diagnose_known_system_fault"
CONTEXT = {"technical_system_represented", "diagnostic_evidence_available"}
RESOURCES = {"diagnostic_interface", "technical_documentation"}


def _seed_actor(conn) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
        (ACTOR, "character", "Cognitive Performance Fixture", "{}", "[]"),
    )
    conn.execute(
        "INSERT INTO character_profiles(entity_id,profile_schema_version,canonical_revision,status) VALUES(?,?,?,?)",
        (ACTOR, 1, "cognitive-performance-test", "active"),
    )
    conn.execute(
        "INSERT INTO character_skills(entity_id,skill_key,category,score,experience,metadata_json) VALUES(?,?,?,?,?,?)",
        (ACTOR, SKILL, "technical", 82.0, None, "{}"),
    )
    for field_key, value in {
        "raps_ia.iq": 140.0,
        "raps_ia.problem_solving": 88.0,
        "raps_ma.focus": 92.0,
        "raps_ma.adaptability": 85.0,
    }.items():
        conn.execute(
            """
            INSERT INTO character_profile_values(
                entity_id,field_key,value_json,mode,authority,source
            ) VALUES(?,?,?,?,?,?)
            """,
            (ACTOR, field_key, json.dumps(value), "static", "test", "test"),
        )
    conn.commit()


def _dimension(result, name):
    return next(item for item in result.dimensions if item.dimension == name)


def test_canonical_modifier_contract_validates() -> None:
    config = validate_cognitive_performance_config()
    contract = config["contracts"][f"{SKILL}.{APPLICATION}"]
    assert contract["feasibility_policy"] == "never_modify"
    assert contract["knowledge_policy"] == "do_not_infer_or_create_knowledge"
    assert set(contract["dimensions"]) == {"reasoning_quality", "precision", "adaptation"}


def test_high_reasoning_factors_produce_bounded_positive_modifiers() -> None:
    result = assess_cognitive_performance(
        SKILL,
        APPLICATION,
        factor_values={
            "raps_ia.iq": 140.0,
            "raps_ia.problem_solving": 88.0,
            "raps_ma.focus": 92.0,
            "raps_ma.adaptability": 85.0,
        },
    )

    reasoning = _dimension(result, "reasoning_quality")
    precision = _dimension(result, "precision")
    adaptation = _dimension(result, "adaptation")
    assert reasoning.multiplier == pytest.approx(1.10464)
    assert precision.multiplier == pytest.approx(1.0836)
    assert adaptation.multiplier == pytest.approx(1.0778)
    assert reasoning.multiplier <= 1.12
    assert precision.multiplier <= 1.10
    assert adaptation.multiplier <= 1.10
    assert "feasibility" not in reasoning.outcome_effects


def test_low_factors_can_reduce_performance_but_never_change_feasibility() -> None:
    result = assess_cognitive_performance(
        SKILL,
        APPLICATION,
        factor_values={
            "raps_ia.iq": 70.0,
            "raps_ia.problem_solving": 20.0,
            "raps_ma.focus": 20.0,
            "raps_ma.adaptability": 20.0,
        },
    )
    assert _dimension(result, "reasoning_quality").multiplier < 1.0
    assert _dimension(result, "precision").multiplier < 1.0
    assert _dimension(result, "adaptation").multiplier < 1.0
    assert all(
        "feasibility" not in dimension.outcome_effects
        for dimension in result.dimensions
    )


def test_missing_input_is_neutral_without_weight_renormalization() -> None:
    result = assess_cognitive_performance(
        SKILL,
        APPLICATION,
        factor_values={
            "raps_ia.iq": None,
            "raps_ia.problem_solving": 50.0,
            "raps_ma.focus": 50.0,
            "raps_ma.adaptability": 50.0,
        },
    )
    reasoning = _dimension(result, "reasoning_quality")
    assert reasoning.multiplier == pytest.approx(1.0)
    assert reasoning.missing_inputs == ("raps_ia.iq",)
    iq = next(
        item for item in reasoning.factor_contributions if item["field_key"] == "raps_ia.iq"
    )
    assert iq["normalized"] == 0.0
    assert iq["weighted_contribution"] == 0.0


def test_actor_adapter_is_read_only_and_does_not_rewrite_skill_authority(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        capability_before = assess_actor_skill_application(
            conn,
            ACTOR,
            SKILL,
            APPLICATION,
            challenge_class="advanced",
            context_tags=CONTEXT,
            resource_capabilities=RESOURCES,
        )
        before = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "history": conn.execute("SELECT COUNT(*) FROM character_profile_history").fetchone()[0],
            "skill": tuple(
                conn.execute(
                    "SELECT score,experience FROM character_skills WHERE entity_id=? AND skill_key=?",
                    (ACTOR, SKILL),
                ).fetchone()
            ),
        }

        performance = assess_actor_cognitive_performance(conn, ACTOR, SKILL, APPLICATION)

        after = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "history": conn.execute("SELECT COUNT(*) FROM character_profile_history").fetchone()[0],
            "skill": tuple(
                conn.execute(
                    "SELECT score,experience FROM character_skills WHERE entity_id=? AND skill_key=?",
                    (ACTOR, SKILL),
                ).fetchone()
            ),
        }
        capability_after = assess_actor_skill_application(
            conn,
            ACTOR,
            SKILL,
            APPLICATION,
            challenge_class="advanced",
            context_tags=CONTEXT,
            resource_capabilities=RESOURCES,
        )

        assert capability_before.status == capability_after.status == "supported"
        assert capability_before.skill_score == capability_after.skill_score == pytest.approx(82.0)
        assert _dimension(performance, "reasoning_quality").multiplier > 1.0
        assert before == after


def test_iq_changes_performance_context_not_skill_capability(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        performance_before = assess_actor_cognitive_performance(conn, ACTOR, SKILL, APPLICATION)
        capability_before = assess_actor_skill_application(
            conn,
            ACTOR,
            SKILL,
            APPLICATION,
            challenge_class="advanced",
            context_tags=CONTEXT,
            resource_capabilities=RESOURCES,
        )
        conn.execute(
            "UPDATE character_profile_values SET value_json=? WHERE entity_id=? AND field_key='raps_ia.iq'",
            (json.dumps(85.0), ACTOR),
        )
        performance_after = assess_actor_cognitive_performance(conn, ACTOR, SKILL, APPLICATION)
        capability_after = assess_actor_skill_application(
            conn,
            ACTOR,
            SKILL,
            APPLICATION,
            challenge_class="advanced",
            context_tags=CONTEXT,
            resource_capabilities=RESOURCES,
        )

        assert _dimension(performance_before, "reasoning_quality").multiplier > _dimension(
            performance_after, "reasoning_quality"
        ).multiplier
        assert capability_before.status == capability_after.status == "supported"
        assert capability_before.proficiency_grade == capability_after.proficiency_grade == "A"
        assert capability_before.skill_score == capability_after.skill_score == pytest.approx(82.0)


def test_validator_rejects_feasibility_modification() -> None:
    config = copy.deepcopy(load_cognitive_performance_config())
    contract = config["contracts"][f"{SKILL}.{APPLICATION}"]
    contract["dimensions"]["reasoning_quality"]["outcome_effects"].append("feasibility")
    with pytest.raises(CognitivePerformanceValidationError, match="cannot modify feasibility"):
        validate_cognitive_performance_config(config)


def test_validator_rejects_excessive_modifier_cap() -> None:
    config = copy.deepcopy(load_cognitive_performance_config())
    config["contracts"][f"{SKILL}.{APPLICATION}"]["dimensions"]["reasoning_quality"][
        "max_abs_effect"
    ] = 0.50
    with pytest.raises(CognitivePerformanceValidationError, match="0,0.15"):
        validate_cognitive_performance_config(config)


def test_validator_rejects_weight_overflow() -> None:
    config = copy.deepcopy(load_cognitive_performance_config())
    factors = config["contracts"][f"{SKILL}.{APPLICATION}"]["dimensions"]["precision"]["factors"]
    factors[0]["weight"] = 0.80
    with pytest.raises(CognitivePerformanceValidationError, match="total weight"):
        validate_cognitive_performance_config(config)

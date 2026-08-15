from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.represented_skill_task_instance import (
    RepresentedSkillTaskInstanceError,
    assess_represented_skill_task_instance,
)
from observer_sandbox.runtime import initialize


ACTOR = "char_task_instance_fixture"
TASK = "technology_known_system_fault_diagnostic_sim_v1"
TARGET = "obj_task_instance_fixture"
TARGET_DEFINITION = "represented_task:technology_known_fault_diagnostic_simulator_v1"


def _seed_actor(conn) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
        (ACTOR, "character", "Task Instance Actor", "{}", "[]"),
    )
    conn.execute(
        "INSERT INTO character_profiles(entity_id,profile_schema_version,canonical_revision,status) VALUES(?,?,?,?)",
        (ACTOR, 1, "task-instance-test", "active"),
    )
    conn.execute(
        "INSERT INTO character_skills(entity_id,skill_key,category,score,experience,metadata_json) VALUES(?,?,?,?,?,?)",
        (ACTOR, "technology", "technical", 82.0, None, "{}"),
    )
    for field_key, value in (
        ("raps_ia.problem_solving", 88.0),
        ("raps_ma.focus", 92.0),
    ):
        conn.execute(
            """INSERT INTO character_profile_values(
                entity_id,field_key,value_json,mode,authority,source
            ) VALUES(?,?,?,?,?,?)""",
            (ACTOR, field_key, json.dumps(value), "static", "test", "test"),
        )


def _seed_target(
    conn,
    *,
    entity_type: str = "object",
    definition_id: str = TARGET_DEFINITION,
    capabilities: tuple[str, ...] = ("inspect",),
) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json,definition_id) VALUES(?,?,?,?,?,?)",
        (TARGET, entity_type, "Synthetic Diagnostic Target", "{}", json.dumps(capabilities), definition_id),
    )
    conn.commit()


def _assess(conn, resources=()):
    return assess_represented_skill_task_instance(
        conn,
        ACTOR,
        TASK,
        TARGET,
        resource_capabilities=resources,
    )


def test_exact_bound_target_with_required_and_supporting_resources_is_supported(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn)
        result = _assess(conn, ("diagnostic_interface", "technical_documentation"))

        assert result.status == "supported"
        assert result.target_definition_id == TARGET_DEFINITION
        assert result.target_entity_type == "object"
        assert result.target_capabilities == ("inspect",)
        assert result.capability.skill_score == pytest.approx(82.0)
        assert result.capability.proficiency_grade == "A"


def test_missing_required_task_resource_is_unsupported(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn)
        result = _assess(conn, ("technical_documentation",))

        assert result.status == "unsupported"
        assert "required_resource_capability_missing" in result.reasons


def test_missing_supporting_documentation_is_constrained(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn)
        result = _assess(conn, ("diagnostic_interface",))

        assert result.status == "constrained"
        assert result.capability.missing_supporting_resource_capabilities == (
            "technical_documentation",
        )


def test_task_resource_envelope_cannot_be_bypassed_by_broader_application_resource(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn)
        result = _assess(
            conn,
            ("diagnostic_instrumentation", "technical_documentation"),
        )

        assert result.status == "unsupported"
        assert result.supplied_resource_capabilities == (
            "diagnostic_instrumentation",
            "technical_documentation",
        )
        assert result.recognized_resource_capabilities == ("technical_documentation",)
        assert "required_resource_capability_missing" in result.reasons


def test_wrong_target_definition_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn, definition_id="represented_task:wrong_definition")
        with pytest.raises(RepresentedSkillTaskInstanceError, match="expected"):
            _assess(conn, ("diagnostic_interface", "technical_documentation"))


def test_practice_console_definition_cannot_bind_as_application_target(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn, definition_id="skill_practice:systems_diagnostic_practice")
        with pytest.raises(RepresentedSkillTaskInstanceError, match="expected"):
            _assess(conn, ("diagnostic_interface", "technical_documentation"))


def test_wrong_target_entity_type_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn, entity_type="location")
        with pytest.raises(RepresentedSkillTaskInstanceError, match="entity type"):
            _assess(conn, ("diagnostic_interface", "technical_documentation"))


def test_missing_required_target_capability_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn, capabilities=("use",))
        with pytest.raises(RepresentedSkillTaskInstanceError, match="missing required task capabilities"):
            _assess(conn, ("diagnostic_interface", "technical_documentation"))


def test_missing_target_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        conn.commit()
        with pytest.raises(RepresentedSkillTaskInstanceError, match="does not exist"):
            _assess(conn, ("diagnostic_interface", "technical_documentation"))


def test_instance_assessment_is_read_only_and_emits_no_evidence(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_actor(conn)
        _seed_target(conn)
        before = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "history": conn.execute("SELECT COUNT(*) FROM character_profile_history").fetchone()[0],
            "score": conn.execute(
                "SELECT score FROM character_skills WHERE entity_id=? AND skill_key='technology'",
                (ACTOR,),
            ).fetchone()[0],
            "target": tuple(
                conn.execute(
                    "SELECT entity_type,definition_id,capabilities_json FROM entities WHERE id=?",
                    (TARGET,),
                ).fetchone()
            ),
        }

        result = _assess(conn, ("diagnostic_interface", "technical_documentation"))

        after = {
            "events": conn.execute("SELECT COUNT(*) FROM events").fetchone()[0],
            "history": conn.execute("SELECT COUNT(*) FROM character_profile_history").fetchone()[0],
            "score": conn.execute(
                "SELECT score FROM character_skills WHERE entity_id=? AND skill_key='technology'",
                (ACTOR,),
            ).fetchone()[0],
            "target": tuple(
                conn.execute(
                    "SELECT entity_type,definition_id,capabilities_json FROM entities WHERE id=?",
                    (TARGET,),
                ).fetchone()
            ),
        }

        assert result.status == "supported"
        assert before == after

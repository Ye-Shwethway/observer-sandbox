from __future__ import annotations

import json
from pathlib import Path

import pytest

from observer_sandbox.cognition_capability_awareness import cognition_capability_awareness
from observer_sandbox.db import connect
from observer_sandbox.represented_skill_runtime_batch import (
    assess_batch_action,
    represented_skill_batch_outcome,
    spec_for_action,
)
from observer_sandbox.represented_skill_tasks import validate_represented_skill_tasks
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_application_requirements import get_executable_skill_application
from observer_sandbox.skill_hierarchy import load_skill_hierarchy_config
from observer_sandbox.skill_progression import maybe_settle_skill_progression
from observer_sandbox.world import set_field


ACTOR = "char_darian"
PARENT = "weapon_mastery"
BLADED = "bladed_weapons"
FIREARMS = "firearms"
LEGACY = "weapons"
ACTION = "blade_drill"
TASK_CONFIG = Path(__file__).resolve().parents[1] / "config" / "bladed_weapons_simulation_safe_runtime.v1.json"


def _move_actor(conn, room_id: str) -> None:
    set_field(conn, ACTOR, "runtime.location", room_id)
    set_field(conn, ACTOR, "runtime.current_action", "idle")
    conn.commit()


def _weapon_state(conn) -> dict[str, tuple[float, float | None]]:
    return {
        row["skill_key"]: (
            float(row["score"]),
            None if row["experience"] is None else float(row["experience"]),
        )
        for row in conn.execute(
            """SELECT skill_key,score,experience FROM character_skills
            WHERE entity_id=? AND skill_key IN (?,?,?,?) ORDER BY skill_key""",
            (ACTOR, PARENT, BLADED, FIREARMS, LEGACY),
        ).fetchall()
    }


def test_component_owns_melee_application_and_legacy_projection_no_longer_does() -> None:
    hierarchy = load_skill_hierarchy_config()
    bladed = hierarchy["hierarchies"][PARENT]["components"][BLADED]
    authority = bladed["application_authority"]["employ_familiar_melee_weapon"]
    assert authority["status"] == "active"
    assert authority["source_skill_id"] == LEGACY
    assert authority["requirements_override"]["resource_capabilities_any"] == [
        "usable_bladed_training_weapon"
    ]

    definition, application = get_executable_skill_application(
        BLADED,
        "employ_familiar_melee_weapon",
    )
    assert definition["skill_id"] == BLADED
    assert application["requirements"]["context_tags_all"] == [
        "weapon_employment_context",
        "represented_melee_weapon",
        "simulation_safe_training_context",
    ]
    assert application["requirements"]["resource_capabilities_any"] == [
        "usable_bladed_training_weapon"
    ]
    with pytest.raises(KeyError, match="authority moved to component Skill"):
        get_executable_skill_application(LEGACY, "employ_familiar_melee_weapon")


def test_safe_task_contract_is_exact_low_risk_and_non_learning() -> None:
    source = json.loads(TASK_CONFIG.read_text(encoding="utf-8"))
    validate_represented_skill_tasks(source)
    task = source["tasks"]["bladed_weapons_safe_handling_sim_v1"]
    assert task["skill_id"] == BLADED
    assert task["application_id"] == "employ_familiar_melee_weapon"
    assert task["task_mode"] == "simulation_safe"
    assert task["risk_class"] == "low"
    assert task["target_contract"]["definition_id"] == (
        "represented_task:bladed_weapons_safe_handling_simulator_v1"
    )
    assert task["resource_contract"]["required_capabilities_any"] == [
        "usable_bladed_training_weapon"
    ]
    assert task["outcome_dimensions"] == [
        "quality_precision",
        "partial_failure_recovery",
    ]
    assert task["evidence_policy"]["learning_evidence"] is False


def test_initialize_seeds_solo_safe_blade_drill_and_cognition_uses_component_authority(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    spec = spec_for_action(ACTION)
    assert spec is not None
    with connect(db) as conn:
        action = conn.execute(
            "SELECT target_mode,required_capability,requires_colocation FROM action_definitions WHERE action_type=?",
            (ACTION,),
        ).fetchone()
        assert action is not None
        assert action["target_mode"] == "object"
        assert action["required_capability"] == ACTION
        assert action["requires_colocation"] == 1

        target = conn.execute(
            "SELECT entity_type,definition_id,capabilities_json FROM entities WHERE id=?",
            (spec.simulator_id,),
        ).fetchone()
        assert target is not None
        assert target["entity_type"] == "object"
        assert target["definition_id"] == spec.simulator_definition_id
        assert set(json.loads(target["capabilities_json"])) == {
            "inspect",
            ACTION,
            "usable_bladed_training_weapon",
        }

        _move_actor(conn, spec.room_id)
        assert any(
            option["action"] == ACTION and option.get("target") == spec.simulator_id
            for option in action_options(conn, ACTOR)
        )

        awareness = cognition_capability_awareness(conn, ACTOR)
        by_id = {item["skill_id"]: item for item in awareness["skills"]}
        assert LEGACY not in by_id
        assert by_id[PARENT]["applications"] == []
        bladed_apps = {
            item["application_id"]: item for item in by_id[BLADED]["applications"]
        }
        assert "employ_familiar_melee_weapon" in bladed_apps
        assert bladed_apps["employ_familiar_melee_weapon"][
            "required_resource_capabilities_any"
        ] == ["usable_bladed_training_weapon"]


def test_blade_drill_uses_bladed_score_and_emits_application_evidence_without_learning(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    spec = spec_for_action(ACTION)
    assert spec is not None
    with connect(db) as conn:
        _move_actor(conn, spec.room_id)
        before = _weapon_state(conn)
        assessment = assess_batch_action(conn, ACTOR, ACTION, spec.simulator_id)
        assert assessment.status == "supported"
        assert assessment.capability.skill_id == BLADED
        assert assessment.capability.skill_score == pytest.approx(87.0)
        assert assessment.recognized_resource_capabilities == (
            "usable_bladed_training_weapon",
        )

        deterministic = represented_skill_batch_outcome(
            conn,
            ACTOR,
            ACTION,
            spec.simulator_id,
        )
        assert deterministic["outcome_class"] == "strong"
        assert deterministic["indices"] == {
            "quality_precision": pytest.approx(0.87),
            "partial_failure_recovery": pytest.approx(0.87),
        }
        assert deterministic["cognitive_performance"]["contract_id"] is None
        assert deterministic["world_mutation_policy"] == "simulation_evidence_only"
        assert deterministic["learning_evidence"] is False

        action_id = "bladed-safe-runtime-action"
        apply_action(
            conn,
            Action(ACTION, 20, spec.simulator_id, "bounded safe handling simulation"),
            ACTOR,
            action_id=action_id,
        )
        instance = conn.execute(
            "SELECT status,outcome_json FROM action_instances WHERE id=?",
            (action_id,),
        ).fetchone()
        assert instance["status"] == "completed"
        outcome = json.loads(instance["outcome_json"])
        evidence = outcome["skill_application"]
        assert evidence["skill_id"] == BLADED
        assert evidence["application_id"] == "employ_familiar_melee_weapon"
        assert evidence["learning_evidence"] is False
        assert outcome["represented_skill_task"]["world_mutation_policy"] == (
            "simulation_evidence_only"
        )

        events = conn.execute(
            "SELECT event_type,payload_json FROM events WHERE action_id=? ORDER BY id",
            (action_id,),
        ).fetchall()
        assert [row["event_type"] for row in events] == [
            "action_completed",
            "skill_application_evidence",
        ]
        assert json.loads(events[1]["payload_json"])["learning_evidence"] is False

        maybe_settle_skill_progression(
            conn,
            ACTOR,
            as_of_sim_time=snapshot(conn, ACTOR)["sim_time"],
        )
        assert _weapon_state(conn) == before

        event_count = conn.execute(
            "SELECT COUNT(*) FROM events WHERE action_id=?",
            (action_id,),
        ).fetchone()[0]
        apply_action(
            conn,
            Action(ACTION, 20, spec.simulator_id, "duplicate must be idempotent"),
            ACTOR,
            action_id=action_id,
        )
        assert conn.execute(
            "SELECT COUNT(*) FROM events WHERE action_id=?",
            (action_id,),
        ).fetchone()[0] == event_count
        assert _weapon_state(conn) == before


def test_blade_drill_fails_closed_on_wrong_target_missing_resource_or_missing_skill(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    spec = spec_for_action(ACTION)
    assert spec is not None
    with connect(db) as conn:
        _move_actor(conn, spec.room_id)

        wrong_definition = "obj_wrong_blade_definition"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            (
                wrong_definition,
                "object",
                "Wrong Blade Simulator",
                json.dumps(list(spec.capabilities)),
                "represented_task:not_the_authorized_blade_simulator",
            ),
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
            (spec.room_id, "contains", wrong_definition),
        )
        conn.commit()
        before = snapshot(conn, ACTOR)
        with pytest.raises(Exception, match="expected"):
            apply_action(
                conn,
                Action(ACTION, 20, wrong_definition, "wrong target"),
                ACTOR,
                action_id="wrong-blade-definition",
            )
        assert snapshot(conn, ACTOR) == before
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='wrong-blade-definition'"
        ).fetchone() is None

        missing_resource = "obj_blade_without_training_resource"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            (
                missing_resource,
                "object",
                "Blade Simulator Without Training Resource",
                json.dumps(["inspect", ACTION]),
                spec.simulator_definition_id,
            ),
        )
        with pytest.raises(Exception, match="missing required task capabilities"):
            assess_batch_action(conn, ACTOR, ACTION, missing_resource)

        conn.execute(
            "DELETE FROM character_skills WHERE entity_id=? AND skill_key=?",
            (ACTOR, BLADED),
        )
        conn.commit()
        with pytest.raises(Exception, match="no authoritative Skill state"):
            assess_batch_action(conn, ACTOR, ACTION, spec.simulator_id)

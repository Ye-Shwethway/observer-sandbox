from __future__ import annotations

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.represented_skill_runtime_batch import (
    TASK_SPECS,
    assess_batch_action,
    represented_skill_batch_outcome,
)
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.skill_progression import maybe_settle_skill_progression
from observer_sandbox.world import set_field


def _move_actor(conn, actor_id: str, room_id: str) -> None:
    set_field(conn, actor_id, "runtime.location", room_id)
    set_field(conn, actor_id, "runtime.current_action", "idle")
    conn.commit()


def test_batch_seed_registers_distinct_simulation_only_targets(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        for spec in TASK_SPECS:
            action = conn.execute(
                "SELECT target_mode,required_capability,requires_colocation FROM action_definitions WHERE action_type=?",
                (spec.action,),
            ).fetchone()
            assert action is not None
            assert action["target_mode"] == "object"
            assert action["required_capability"] == spec.action
            assert action["requires_colocation"] == 1
            simulator = conn.execute(
                "SELECT entity_type,definition_id,capabilities_json FROM entities WHERE id=?",
                (spec.simulator_id,),
            ).fetchone()
            assert simulator is not None
            assert simulator["entity_type"] == "object"
            assert simulator["definition_id"] == spec.simulator_definition_id
            assert simulator["definition_id"].startswith("represented_task:")
            assert not simulator["definition_id"].startswith("skill_practice:")
            assert set(spec.capabilities).issubset(set(json.loads(simulator["capabilities_json"])))
            assert conn.execute(
                "SELECT 1 FROM relations WHERE source_id=? AND relation_type='contains' AND target_id=?",
                (spec.room_id, spec.simulator_id),
            ).fetchone() is not None


@pytest.mark.parametrize("spec", TASK_SPECS, ids=lambda spec: spec.task_id)
def test_batch_actions_are_cognition_visible_only_when_colocated(tmp_path, spec) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert not any(
            item["action"] == spec.action and item.get("target") == spec.simulator_id
            for item in action_options(conn, "char_darian")
        )
        _move_actor(conn, "char_darian", spec.room_id)
        option = next(
            item
            for item in action_options(conn, "char_darian")
            if item["action"] == spec.action and item["target"] == spec.simulator_id
        )
        assert option["target_name"] == spec.simulator_name
        enriched = ModelDecisionProvider(conn, character_id="char_darian")._enrich_state(
            snapshot(conn, "char_darian")
        )
        assert any(
            item["action"] == spec.action and item["target"] == spec.simulator_id
            for item in enriched["action_options"]
        )
        skill = next(
            item
            for item in enriched["capability_awareness"]["skills"]
            if item["skill_id"] == spec.skill_id
        )
        assert any(app["application_id"] == spec.application_id for app in skill["applications"])


@pytest.mark.parametrize("spec", TASK_SPECS, ids=lambda spec: spec.task_id)
def test_batch_outcomes_use_authoritative_skill_and_only_declared_modifiers(tmp_path, spec) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    expected_scores = {
        "tactical_planning": 92.0,
        "survival": 85.0,
        "bladed_weapons": 87.0,
        "firearms": 87.0,
    }
    with connect(db) as conn:
        assessment = assess_batch_action(conn, "char_darian", spec.action, spec.simulator_id)
        assert assessment.status == "supported"
        assert assessment.capability.skill_score == pytest.approx(expected_scores[spec.skill_id])
        first = represented_skill_batch_outcome(conn, "char_darian", spec.action, spec.simulator_id)
        second = represented_skill_batch_outcome(conn, "char_darian", spec.action, spec.simulator_id)
        assert first == second
        assert first["outcome_class"] == "strong"
        assert first["learning_evidence"] is False
        assert first["world_mutation_policy"] == "simulation_evidence_only"
        assert set(first["indices"]) == set(spec.outcome_dimensions)

        if spec.uses_cognitive_performance:
            assert first["cognitive_performance"]["contract_id"] is not None
            factor_keys = {
                contribution["field_key"]
                for dimension in first["cognitive_performance"]["dimensions"]
                for contribution in dimension["factor_contributions"]
            }
            if spec.skill_id == "tactical_planning":
                assert "raps_ia.iq" in factor_keys
                assert "raps_ia.tactical_thinking" not in factor_keys
            else:
                assert "raps_ia.iq" not in factor_keys
                assert "raps_pa.survival_skill" not in factor_keys
                assert {"raps_ia.problem_solving", "raps_ma.adaptability"}.issubset(factor_keys)
        else:
            assert first["cognitive_performance"]["contract_id"] is None
            assert first["cognitive_performance"]["dimensions"] == []
            assert first["indices"]["quality_precision"] == pytest.approx(
                expected_scores[spec.skill_id] / 100.0
            )


def test_batch_completion_writes_application_evidence_without_xp_or_domain_state_mutation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    tracked_skills = (
        "tactical_planning",
        "survival",
        "bladed_weapons",
        "firearms",
        "weapon_mastery",
        "weapons",
    )
    placeholders = ",".join("?" for _ in tracked_skills)
    with connect(db) as conn:
        before_skills = {
            row["skill_key"]: (row["score"], row["experience"])
            for row in conn.execute(
                f"""
                SELECT skill_key,score,experience FROM character_skills
                WHERE entity_id='char_darian'
                  AND skill_key IN ({placeholders})
                ORDER BY skill_key
                """,
                tracked_skills,
            ).fetchall()
        }
        for index, spec in enumerate(TASK_SPECS, start=1):
            _move_actor(conn, "char_darian", spec.room_id)
            action_id = f"represented-batch-action-{index}"
            apply_action(
                conn,
                Action(spec.action, 20, spec.simulator_id, "bounded represented Skill batch simulation"),
                "char_darian",
                action_id=action_id,
            )
            instance = conn.execute(
                "SELECT status,outcome_json FROM action_instances WHERE id=?",
                (action_id,),
            ).fetchone()
            assert instance["status"] == "completed"
            outcome = json.loads(instance["outcome_json"])
            assert outcome["represented_skill_task"]["world_mutation_policy"] == "simulation_evidence_only"
            assert outcome["skill_application"]["skill_id"] == spec.skill_id
            assert outcome["skill_application"]["application_id"] == spec.application_id
            assert outcome["skill_application"]["learning_evidence"] is False
            events = conn.execute(
                "SELECT event_type,payload_json,caused_by_event_id FROM events WHERE action_id=? ORDER BY id",
                (action_id,),
            ).fetchall()
            assert [row["event_type"] for row in events] == ["action_completed", "skill_application_evidence"]
            evidence = json.loads(events[1]["payload_json"])
            assert evidence["learning_evidence"] is False
            assert events[1]["caused_by_event_id"] is not None
        maybe_settle_skill_progression(
            conn,
            "char_darian",
            as_of_sim_time=snapshot(conn, "char_darian")["sim_time"],
        )
        after_skills = {
            row["skill_key"]: (row["score"], row["experience"])
            for row in conn.execute(
                f"""
                SELECT skill_key,score,experience FROM character_skills
                WHERE entity_id='char_darian'
                  AND skill_key IN ({placeholders})
                ORDER BY skill_key
                """,
                tracked_skills,
            ).fetchall()
        }
        assert after_skills == before_skills


def test_batch_exact_definition_binding_fails_closed_before_completion(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    spec = TASK_SPECS[1]
    with connect(db) as conn:
        _move_actor(conn, "char_darian", spec.room_id)
        wrong = "obj_wrong_field_navigation_target"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            (wrong, "object", "Wrong Field Navigation Target", json.dumps(list(spec.capabilities)), "represented_task:not_the_authorized_field_navigation_simulator"),
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?,?,?)",
            (spec.room_id, "contains", wrong),
        )
        conn.commit()
        before = snapshot(conn, "char_darian")
        with pytest.raises(Exception, match="expected"):
            apply_action(
                conn,
                Action(spec.action, 20, wrong, "wrong target must fail exact binding"),
                "char_darian",
                action_id="wrong-represented-batch-target",
            )
        assert snapshot(conn, "char_darian") == before
        assert conn.execute(
            "SELECT 1 FROM action_instances WHERE id='wrong-represented-batch-target'"
        ).fetchone() is None


def test_batch_missing_required_resource_fails_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    spec = TASK_SPECS[2]
    with connect(db) as conn:
        target = "obj_sustainment_without_materials"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json,definition_id) VALUES(?,?,?,?,?)",
            (target, "object", "Sustainment Simulator Without Materials", json.dumps(["inspect", "sustain", "field_toolkit"]), spec.simulator_definition_id),
        )
        assessment = assess_batch_action(conn, "char_darian", spec.action, target)
        assert assessment.status == "unsupported"
        assert "field_sustainment_materials" not in assessment.recognized_resource_capabilities
        assert "required_resource_capability_missing" in assessment.reasons

from __future__ import annotations

import json

import pytest

from observer_sandbox.action_conditions import ActionConditionError, evaluate_action_conditions
from observer_sandbox.composition_schema import TRAINING_FATIGUE_LIMIT
from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_definition, action_options, set_runtime_value, validate_action
from observer_sandbox.world import set_field


ACTOR = "char_darian"
HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"


def test_empty_conditions_are_satisfied_and_all_clauses_are_required():
    assert evaluate_action_conditions({}, {"x": 1})["satisfied"] is True
    result = evaluate_action_conditions(
        {
            "all": [
                {"field_key": "x", "operator": "gte", "value": 5},
                {"field_key": "y", "operator": "lt", "value": 10},
            ]
        },
        {"x": 6, "y": 12},
    )
    assert result["satisfied"] is False
    assert len(result["failures"]) == 1
    assert result["failures"][0]["field_key"] == "y"


def test_malformed_or_unavailable_condition_contract_fails_closed():
    with pytest.raises(ActionConditionError, match="exactly an 'all'"):
        evaluate_action_conditions({"any": []}, {"x": 1})
    with pytest.raises(ActionConditionError, match="field is unavailable"):
        evaluate_action_conditions(
            {"all": [{"field_key": "missing", "operator": "eq", "value": 1}]},
            {"x": 1},
        )
    with pytest.raises(ActionConditionError, match="Unsupported action condition operator"):
        evaluate_action_conditions(
            {"all": [{"field_key": "x", "operator": "contains", "value": 1}]},
            {"x": 1},
        )


def test_train_definition_owns_the_systemic_fatigue_prerequisite(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        condition = action_definition(conn, "train")["conditions"]
        assert condition == {
            "all": [
                {
                    "field_key": "physiology.fatigue",
                    "operator": "lt",
                    "value": TRAINING_FATIGUE_LIMIT,
                }
            ]
        }


def test_train_option_and_validation_use_definition_condition_boundary(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, HOME_GYM)
        set_field(conn, ACTOR, "physiology.fatigue", TRAINING_FATIGUE_LIMIT - 0.1, authority="physiology_engine")
        conn.commit()
        assert any(option["action"] == "train" for option in action_options(conn, ACTOR))
        validate_action(conn, ACTOR, Action("train", 30, FREE_WEIGHTS, "condition boundary allowed"))

        set_field(conn, ACTOR, "physiology.fatigue", TRAINING_FATIGUE_LIMIT, authority="physiology_engine")
        conn.commit()
        assert not any(option["action"] == "train" for option in action_options(conn, ACTOR))
        with pytest.raises(ValueError, match="Action train conditions are not satisfied"):
            validate_action(conn, ACTOR, Action("train", 30, FREE_WEIGHTS, "condition boundary blocked"))


def test_active_modifier_effective_value_composes_with_action_condition(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, HOME_GYM)
        set_field(conn, ACTOR, "physiology.fatigue", 20.0, authority="physiology_engine")
        set_runtime_value(conn, "sim_time", "2025-05-01T08:00:00+00:00")
        conn.execute(
            """
            INSERT INTO active_modifiers(
                id,subject_id,field_key,operation,value_json,starts_sim_time,ends_sim_time,
                stack_key,stack_policy,conditions_json
            ) VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                "mod_condition_bridge",
                ACTOR,
                "physiology.fatigue",
                "add",
                json.dumps(55.0),
                "2025-05-01T07:00:00+00:00",
                "2025-05-01T09:00:00+00:00",
                "condition_bridge",
                "replace",
                "{}",
            ),
        )
        conn.commit()

        assert not any(option["action"] == "train" for option in action_options(conn, ACTOR))
        with pytest.raises(ValueError, match="actual 75.0"):
            validate_action(conn, ACTOR, Action("train", 30, FREE_WEIGHTS, "temporary fatigue blocks"))

        set_runtime_value(conn, "sim_time", "2025-05-01T09:00:00+00:00")
        conn.commit()
        assert any(option["action"] == "train" for option in action_options(conn, ACTOR))
        validate_action(conn, ACTOR, Action("train", 30, FREE_WEIGHTS, "temporary fatigue expired"))


def test_reinitialize_restores_canonical_train_condition_without_schema_change(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute("UPDATE action_definitions SET conditions_json='{}' WHERE action_type='train'")
        conn.commit()
    initialize(db)
    with connect(db) as conn:
        condition = json.loads(
            conn.execute("SELECT conditions_json FROM action_definitions WHERE action_type='train'").fetchone()[0]
        )
        assert condition["all"][0]["field_key"] == "physiology.fatigue"
        assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "5"

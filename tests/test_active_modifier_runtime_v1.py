from __future__ import annotations

import json

import pytest

from observer_sandbox.active_modifiers import (
    ActiveModifierError,
    active_modifier_rows,
    resolve_active_modifier_value,
)
from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, set_runtime_value, snapshot, validate_action
from observer_sandbox.world import get_field, set_field


ACTOR = "char_darian"
HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"


def _modifier(
    conn,
    modifier_id: str,
    *,
    field_key: str,
    operation: str,
    value: float,
    starts: str = "2025-05-01T07:00:00+00:00",
    ends: str | None = "2025-05-01T09:00:00+00:00",
    stack_key: str | None = None,
    stack_policy: str = "replace",
    conditions: dict | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO active_modifiers(
            id,subject_id,field_key,operation,value_json,starts_sim_time,ends_sim_time,
            stack_key,stack_policy,conditions_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?)
        """,
        (
            modifier_id,
            ACTOR,
            field_key,
            operation,
            json.dumps(value),
            starts,
            ends,
            stack_key,
            stack_policy,
            json.dumps(conditions or {}),
        ),
    )
    conn.commit()


def test_time_bounds_are_half_open_and_do_not_delete_expired_rows(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _modifier(conn, "mod_energy", field_key="needs.energy", operation="add", value=10)
        assert len(active_modifier_rows(conn, ACTOR, "needs.energy", as_of_sim_time="2025-05-01T08:00:00+00:00")) == 1
        assert active_modifier_rows(conn, ACTOR, "needs.energy", as_of_sim_time="2025-05-01T09:00:00+00:00") == []
        assert conn.execute("SELECT COUNT(*) FROM active_modifiers WHERE id='mod_energy'").fetchone()[0] == 1


def test_stack_and_replace_policies_resolve_deterministically(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _modifier(conn, "stack_a", field_key="needs.energy", operation="add", value=5, stack_key="boost", stack_policy="stack")
        _modifier(conn, "stack_b", field_key="needs.energy", operation="add", value=7, stack_key="boost", stack_policy="stack", starts="2025-05-01T07:10:00+00:00")
        _modifier(conn, "replace_old", field_key="needs.energy", operation="multiply", value=0.5, stack_key="factor", stack_policy="replace")
        _modifier(conn, "replace_new", field_key="needs.energy", operation="multiply", value=0.8, stack_key="factor", stack_policy="replace", starts="2025-05-01T07:20:00+00:00")
        resolved = resolve_active_modifier_value(
            conn,
            ACTOR,
            "needs.energy",
            50,
            as_of_sim_time="2025-05-01T08:00:00+00:00",
        )
        # +5, +7, then newest replacement multiplier 0.8.
        assert resolved["effective_value"] == pytest.approx(49.6)
        assert [item["id"] for item in resolved["applied"]] == ["stack_a", "stack_b", "replace_new"]


def test_max_and_min_stack_policies_select_one_row_each(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _modifier(conn, "max_low", field_key="needs.energy", operation="add", value=2, stack_key="max_group", stack_policy="max")
        _modifier(conn, "max_high", field_key="needs.energy", operation="add", value=8, stack_key="max_group", stack_policy="max", starts="2025-05-01T07:05:00+00:00")
        _modifier(conn, "min_high", field_key="needs.energy", operation="add", value=-2, stack_key="min_group", stack_policy="min")
        _modifier(conn, "min_low", field_key="needs.energy", operation="add", value=-6, stack_key="min_group", stack_policy="min", starts="2025-05-01T07:06:00+00:00")
        resolved = resolve_active_modifier_value(conn, ACTOR, "needs.energy", 50, as_of_sim_time="2025-05-01T08:00:00+00:00")
        assert resolved["effective_value"] == pytest.approx(52.0)
        assert {item["id"] for item in resolved["applied"]} == {"max_high", "min_low"}


def test_conditions_require_exact_caller_context(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _modifier(
            conn,
            "conditional",
            field_key="needs.energy",
            operation="add",
            value=12,
            conditions={"environment": "cold"},
        )
        without_context = resolve_active_modifier_value(conn, ACTOR, "needs.energy", 50, as_of_sim_time="2025-05-01T08:00:00+00:00")
        wrong_context = resolve_active_modifier_value(conn, ACTOR, "needs.energy", 50, as_of_sim_time="2025-05-01T08:00:00+00:00", context={"environment": "warm"})
        matching = resolve_active_modifier_value(conn, ACTOR, "needs.energy", 50, as_of_sim_time="2025-05-01T08:00:00+00:00", context={"environment": "cold"})
        assert without_context["effective_value"] == 50
        assert wrong_context["effective_value"] == 50
        assert matching["effective_value"] == 62


def test_runtime_snapshot_uses_effective_need_without_overwriting_base_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, ACTOR, "needs.energy", 50.0)
        _modifier(conn, "temporary_energy", field_key="needs.energy", operation="add", value=20)
        set_runtime_value(conn, "sim_time", "2025-05-01T08:00:00+00:00")
        conn.commit()
        assert snapshot(conn, ACTOR)["energy"] == 70.0
        assert get_field(conn, ACTOR, "needs.energy") == 50.0

        set_runtime_value(conn, "sim_time", "2025-05-01T09:00:00+00:00")
        conn.commit()
        assert snapshot(conn, ACTOR)["energy"] == 50.0
        assert get_field(conn, ACTOR, "needs.energy") == 50.0


def test_active_fatigue_modifier_changes_training_legality_then_expires(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, ACTOR, HOME_GYM)
        set_field(conn, ACTOR, "physiology.fatigue", 20.0, authority="physiology_engine")
        _modifier(conn, "temporary_fatigue", field_key="physiology.fatigue", operation="add", value=60)
        set_runtime_value(conn, "sim_time", "2025-05-01T08:00:00+00:00")
        conn.commit()

        assert snapshot(conn, ACTOR)["fatigue"] == 80.0
        assert not any(option["action"] == "train" for option in action_options(conn, ACTOR))
        with pytest.raises(ValueError, match="Action train conditions are not satisfied"):
            validate_action(conn, ACTOR, Action("train", 30, FREE_WEIGHTS, "training while temporarily impaired"))
        assert get_field(conn, ACTOR, "physiology.fatigue") == 20.0

        set_runtime_value(conn, "sim_time", "2025-05-01T09:00:00+00:00")
        conn.commit()
        assert snapshot(conn, ACTOR)["fatigue"] == 20.0
        assert any(option["action"] == "train" for option in action_options(conn, ACTOR))


def test_mixed_policy_same_stack_is_rejected(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _modifier(conn, "mixed_a", field_key="needs.energy", operation="add", value=1, stack_key="mixed", stack_policy="stack")
        _modifier(conn, "mixed_b", field_key="needs.energy", operation="add", value=2, stack_key="mixed", stack_policy="replace", starts="2025-05-01T07:05:00+00:00")
        with pytest.raises(ActiveModifierError, match="mixes stack policies"):
            resolve_active_modifier_value(conn, ACTOR, "needs.energy", 50, as_of_sim_time="2025-05-01T08:00:00+00:00")

from __future__ import annotations

import json
from datetime import timedelta

import pytest

from observer_sandbox.body_measurement_progression import _regional_training_exposure
from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, ensure_sim_clock, snapshot
from observer_sandbox.training_anatomy import load_training_movement_catalog, movement_anatomy_evidence
from observer_sandbox.training_methods import (
    training_profile_for_target,
    validate_training_movements_for_target,
)
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"
BENCH = "obj_thorne_estate_gym_adjustable_bench"
TREADMILL = "obj_thorne_estate_gym_high_speed_treadmill"


def _prepare(conn) -> None:
    set_dynamic_location(conn, "char_darian", HOME_GYM)
    set_field(conn, "char_darian", "runtime.current_action", "idle")
    set_field(conn, "char_darian", "needs.energy", 95.0)
    set_field(conn, "char_darian", "physiology.fatigue", 0.0, authority="physiology_engine", source="training-anatomy-test")
    conn.commit()


def test_movement_catalog_is_actor_and_target_independent() -> None:
    catalog = load_training_movement_catalog()
    assert catalog["revision"] == "training-anatomy-v1"
    assert {"squat", "hinge", "horizontal_press", "vertical_press", "row", "curl", "extension", "calf_raise"} <= set(catalog["movements"])
    for movement in catalog["movements"].values():
        assert movement["name"]
        assert movement["region_weights"]
        assert "char_darian" not in json.dumps(movement)
        assert "obj_thorne_estate" not in json.dumps(movement)


def test_resistance_method_exposes_allowed_movement_options_but_conditioning_does_not() -> None:
    free_weights = training_profile_for_target(FREE_WEIGHTS)
    treadmill = training_profile_for_target(TREADMILL)
    assert free_weights is not None and treadmill is not None
    ids = {row["movement_id"] for row in free_weights["movement_options"]}
    assert {"squat", "hinge", "horizontal_press", "row", "curl", "extension", "calf_raise"} <= ids
    assert "movement_options" not in treadmill


def test_selected_movement_must_belong_to_selected_method() -> None:
    assert validate_training_movements_for_target(BENCH, ["horizontal_press", "extension"]) == (
        "horizontal_press",
        "extension",
    )
    with pytest.raises(ValueError, match="not allowed"):
        validate_training_movements_for_target(BENCH, ["squat"])


def test_movement_anatomy_distinguishes_curl_from_squat() -> None:
    curl = movement_anatomy_evidence(["curl"])
    squat = movement_anatomy_evidence(["squat"])
    assert curl is not None and squat is not None
    assert curl["regional_load"]["biceps"] == 1.0
    assert curl["regional_load"].get("thighs", 0.0) == 0.0
    assert squat["regional_load"]["thighs"] == 1.0
    assert squat["regional_load"].get("biceps", 0.0) == 0.0


def test_completed_training_event_persists_selected_movement_anatomy(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        apply_action(
            conn,
            Action(
                "train",
                45,
                FREE_WEIGHTS,
                "arm-focused accessory work",
                conditions={"training_movements": ["curl"]},
            ),
        )
        row = conn.execute(
            "SELECT payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        payload = json.loads(row["payload_json"])
        anatomy = payload["training_method"]["movement_anatomy"]
        assert anatomy["movement_ids"] == ["curl"]
        assert anatomy["regional_load"]["biceps"] == 1.0
        assert anatomy["regional_load"].get("thighs", 0.0) == 0.0


def test_bc3_prefers_movement_anatomy_and_keeps_method_fallback(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        start = ensure_sim_clock(conn)
        apply_action(
            conn,
            Action("train", 45, FREE_WEIGHTS, "curl emphasis", conditions={"training_movements": ["curl"]}),
        )
        end = start + timedelta(hours=1)
        movement_exposure = _regional_training_exposure(
            conn,
            "char_darian",
            start_sim_time=(start - timedelta(seconds=1)).isoformat(),
            end_sim_time=end.isoformat(),
        )
        assert movement_exposure["biceps"] == 1.0
        assert movement_exposure.get("thighs", 0.0) == 0.0

    db2 = tmp_path / "observer-fallback.sqlite3"
    initialize(db2)
    with connect(db2) as conn:
        _prepare(conn)
        start = ensure_sim_clock(conn)
        apply_action(conn, Action("train", 45, FREE_WEIGHTS, "legacy broad strength session"))
        end = start + timedelta(hours=1)
        fallback = _regional_training_exposure(
            conn,
            "char_darian",
            start_sim_time=(start - timedelta(seconds=1)).isoformat(),
            end_sim_time=end.isoformat(),
        )
        assert fallback["biceps"] == 0.65
        assert fallback["thighs"] == 0.8


def test_model_training_movements_become_action_conditions(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)

        def fake_decision(*args, **kwargs):
            return {
                "action": "train",
                "duration_minutes": 45,
                "target": FREE_WEIGHTS,
                "reason": "focused upper-body accessory work",
                "resources": [],
                "training_movements": ["curl", "extension"],
            }

        monkeypatch.setattr("observer_sandbox.model_decision.generate_character_decision", fake_decision)
        action = ModelDecisionProvider(conn).choose(snapshot(conn), ["train"])
        assert action.conditions == {"training_movements": ["curl", "extension"]}

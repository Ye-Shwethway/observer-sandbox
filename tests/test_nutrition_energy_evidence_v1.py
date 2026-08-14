from __future__ import annotations

import json
from datetime import datetime, timedelta

from observer_sandbox.db import connect
from observer_sandbox.nutrition_energy import (
    energy_balance_window,
    load_nutrition_catalog,
    resting_energy_reference,
)
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field


ACTOR = "char_darian"
KITCHEN = "loc_thorne_estate_kitchen"
MEAL = "obj_thorne_estate_kitchen_meal_ingredients"


def _latest_action_payload(conn):
    row = conn.execute(
        "SELECT payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
        (ACTOR,),
    ).fetchone()
    assert row is not None
    return json.loads(row["payload_json"])


def _prepare_kitchen(conn) -> None:
    set_field(conn, ACTOR, "runtime.location", KITCHEN)
    set_field(conn, ACTOR, "runtime.current_action", "idle")
    set_field(conn, ACTOR, "needs.hunger", 70.0)
    set_field(conn, ACTOR, "needs.energy", 80.0)
    conn.commit()


def test_authored_nutrition_profiles_have_coherent_macros() -> None:
    catalog = load_nutrition_catalog()
    assert catalog["revision"] == "nutrition-evidence-v1"
    assert set(catalog["profiles"]) == {
        "obj_thorne_estate_kitchen_pantry",
        "obj_thorne_estate_food_storage_provisions",
        "obj_thorne_estate_kitchen_meal_ingredients",
    }
    for profile in catalog["profiles"].values():
        kcal = float(profile["energy_kcal"])
        macro_kcal = 4.0 * (float(profile["protein_g"]) + float(profile["carbohydrate_g"])) + 9.0 * float(profile["fat_g"])
        assert kcal > 0.0
        assert float(profile["protein_g"]) > 0.0
        assert abs(macro_kcal - kcal) / kcal < 0.05


def test_completed_eat_action_persists_nutrition_and_energy_evidence(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_kitchen(conn)
        before_weight = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key='body.weight_lb'",
            (ACTOR,),
        ).fetchone()[0]
        before_bf = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key='body.body_fat_pct'",
            (ACTOR,),
        ).fetchone()[0]

        apply_action(conn, Action("eat", 25, MEAL, "nutrition evidence test"), ACTOR)
        payload = _latest_action_payload(conn)
        nutrition = payload["nutrition_intake"]
        energy = payload["energy_expenditure"]

        assert nutrition["source"] == "nutrition-evidence-v1"
        assert nutrition["energy_kcal"] == 800.0
        assert nutrition["protein_g"] == 50.0
        assert nutrition["target"] == MEAL
        assert energy["source"] == "energy-expenditure-evidence-v1"
        assert energy["resting_reference"]["formula"] == "mifflin-st-jeor-1990"
        assert energy["activity_multiplier"] == 1.5
        assert energy["estimated_kcal"] > 0.0

        after_weight = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key='body.weight_lb'",
            (ACTOR,),
        ).fetchone()[0]
        after_bf = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key='body.body_fat_pct'",
            (ACTOR,),
        ).fetchone()[0]
        assert before_weight == after_weight
        assert before_bf == after_bf


def test_resting_reference_uses_age_sex_height_and_weight_without_identity_hardcode(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        now = snapshot(conn, ACTOR)["sim_time"]
        male = resting_energy_reference(conn, ACTOR, as_of_sim_time=now)
        assert male is not None and male["sex"] == "male"

        conn.execute(
            "UPDATE character_profile_values SET value_json=? WHERE entity_id=? AND field_key='identity.sex'",
            (json.dumps("female"), ACTOR),
        )
        conn.commit()
        female = resting_energy_reference(conn, ACTOR, as_of_sim_time=now)
        assert female is not None and female["ree_kcal_day"] < male["ree_kcal_day"]

        older_time = (datetime.fromisoformat(now) + timedelta(days=3652)).isoformat()
        older = resting_energy_reference(conn, ACTOR, as_of_sim_time=older_time)
        assert older is not None and older["ree_kcal_day"] < female["ree_kcal_day"]


def test_full_action_coverage_aggregates_window_without_body_mutation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare_kitchen(conn)
        start = snapshot(conn, ACTOR)["sim_time"]

        # 11 x 120 idle + 25 eat + 95 idle = exactly 24 simulated hours.
        for _ in range(11):
            apply_action(conn, Action("idle", 120, None, "coverage test"), ACTOR)
        apply_action(conn, Action("eat", 25, MEAL, "coverage meal"), ACTOR)
        apply_action(conn, Action("idle", 95, None, "coverage test"), ACTOR)

        end = snapshot(conn, ACTOR)["sim_time"]
        evidence = energy_balance_window(conn, ACTOR, start_sim_time=start, end_sim_time=end)
        assert evidence["window_minutes"] == 1440.0
        assert evidence["covered_action_minutes"] == 1440.0
        assert evidence["coverage_ratio"] == 1.0
        assert evidence["complete"] is True
        assert evidence["intake_event_count"] == 1
        assert evidence["intake_kcal"] == 800.0
        assert evidence["protein_g"] == 50.0
        assert evidence["expenditure_kcal"] > 0.0
        assert evidence["missing_energy_event_ids"] == []
        assert evidence["missing_nutrition_event_ids"] == []


def test_pre_evidence_history_is_not_recomputed_and_makes_window_incomplete(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        start = snapshot(conn, ACTOR)["sim_time"]
        end = (datetime.fromisoformat(start) + timedelta(hours=1)).isoformat()
        conn.execute(
            """INSERT INTO events(sim_time,actor_id,event_type,payload_json,event_uuid,state_changes_json)
            VALUES(?,?,?,?,?,?)""",
            (
                end,
                ACTOR,
                "action_completed",
                json.dumps({
                    "action": "idle",
                    "target": None,
                    "duration_minutes": 60,
                    "action_started_sim_time": start,
                    "action_ended_sim_time": end,
                }),
                "legacy-no-energy-evidence",
                "{}",
            ),
        )
        conn.commit()
        evidence = energy_balance_window(conn, ACTOR, start_sim_time=start, end_sim_time=end)
        assert evidence["complete"] is False
        assert evidence["coverage_ratio"] == 0.0
        assert evidence["missing_energy_event_ids"]
        assert evidence["expenditure_kcal"] == 0.0

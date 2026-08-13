from __future__ import annotations

from datetime import timedelta

import pytest

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import (
    Action,
    action_options,
    apply_action,
    ensure_sim_clock,
    run_one_simulated_day,
    snapshot,
    validate_action,
)
from observer_sandbox.world import set_field


MASTER_SUITE = "loc_thorne_estate_master_suite"
MASTER_BATHROOM = "loc_thorne_estate_master_bathroom"
KITCHEN = "loc_thorne_estate_kitchen"
HOME_GYM = "loc_thorne_estate_home_gym"
FOYER = "loc_thorne_estate_foyer"
ARMORY = "loc_thorne_estate_armory"
EXTERIOR = "loc_thorne_estate_exterior_boundary"
MASTER_BED = "obj_thorne_estate_master_bed"
MASTER_SHOWER = "obj_thorne_estate_master_shower"
DRINKING_WATER = "obj_thorne_estate_kitchen_drinking_water"
MEAL_INGREDIENTS = "obj_thorne_estate_kitchen_meal_ingredients"
DINING_TABLE = "obj_thorne_estate_dining_table"


def test_p1_home_seed_and_darian_instantiation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM entities WHERE entity_type='location'").fetchone()[0] >= 20
        assert conn.execute("SELECT COUNT(*) FROM entities WHERE entity_type='object'").fetchone()[0] >= 40
        assert conn.execute("SELECT name FROM entities WHERE id='loc_thorne_estate'").fetchone()[0] == "Thorne Estate"
        assert conn.execute("SELECT name FROM entities WHERE id=?", (MASTER_SUITE,)).fetchone()[0] == "Darian's Master Suite"
        assert conn.execute("SELECT name FROM entities WHERE id=?", (HOME_GYM,)).fetchone()[0] == "Top-Class Home Gym"
        assert conn.execute("SELECT name FROM entities WHERE id='char_darian'").fetchone()[0] == "Darian Thorne"
        state = snapshot(conn)
        assert state["location"] == MASTER_SUITE
        assert state["current_action"] == "idle"
        assert 0 <= state["energy"] <= 100
        assert 0 <= state["hunger"] <= 100
        assert 0 <= state["thirst"] <= 100
        assert 0 <= state["sleepiness"] <= 100


def test_estate_is_hierarchical_and_exterior_is_not_traversable(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert conn.execute(
            "SELECT 1 FROM relations WHERE source_id='loc_thorne_estate' AND relation_type='contains' AND target_id='loc_thorne_estate_underground'"
        ).fetchone() is not None
        assert conn.execute(
            "SELECT 1 FROM relations WHERE source_id='loc_thorne_estate_underground' AND relation_type='contains' AND target_id=?",
            (HOME_GYM,),
        ).fetchone() is not None
        assert conn.execute(
            "SELECT 1 FROM relations WHERE relation_type='connected_to' AND (source_id=? OR target_id=?)",
            (EXTERIOR, EXTERIOR),
        ).fetchone() is None
        set_field(conn, "char_darian", "runtime.location", FOYER)
        conn.commit()
        with pytest.raises(ValueError):
            validate_action(conn, "char_darian", Action("move", 5, EXTERIOR))


def test_p1_runtime_rejects_non_adjacent_move(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        with pytest.raises(ValueError):
            validate_action(conn, "char_darian", Action("move", 5, ARMORY))


def test_recovery_actions_increase_energy_and_rest_is_available_anywhere(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        set_field(conn, "char_darian", "needs.energy", 20.0)
        set_field(conn, "char_darian", "needs.sleepiness", 65.0)
        conn.commit()
        options = action_options(conn)
        rest = next(option for option in options if option["action"] == "rest" and option["target"] is None)
        assert rest["effects_per_hour"]["energy"] > 0
        assert "sleepiness" not in rest["effects_per_hour"]
        before = snapshot(conn)
        after_idle = apply_action(conn, Action("idle", 60, None, "brief pause"))
        assert after_idle["energy"] > before["energy"]
        after_rest = apply_action(conn, Action("rest", 60, None, "recover low energy"))
        assert after_rest["energy"] >= after_idle["energy"] + 7.9
        assert after_rest["sleepiness"] > after_idle["sleepiness"]


def test_sleep_is_strong_recovery_and_can_escape_critical_energy(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", MASTER_SUITE)
        set_field(conn, "char_darian", "needs.energy", 18.0)
        set_field(conn, "char_darian", "needs.sleepiness", 88.0)
        conn.commit()
        after = apply_action(conn, Action("sleep", 480, MASTER_BED, "overnight recovery"))
        assert after["energy"] >= 89.0
        assert after["sleepiness"] <= 5.0
        assert after["hunger"] < 50.0
        assert after["thirst"] < 50.0


def test_food_water_and_shower_restore_authored_basic_stats(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", KITCHEN)
        set_field(conn, "char_darian", "needs.energy", 25.0)
        set_field(conn, "char_darian", "needs.hunger", 80.0)
        set_field(conn, "char_darian", "needs.thirst", 80.0)
        conn.commit()
        options = action_options(conn)
        water = next(option for option in options if option["action"] == "drink" and option["target"] == DRINKING_WATER)
        meal = next(option for option in options if option["action"] == "eat" and option["target"] == MEAL_INGREDIENTS)
        assert water["effects"]["needs.thirst"] == -55.0
        assert meal["effects"]["needs.hunger"] == -50.0
        assert meal["effects"]["needs.energy"] == 8.0
        after_water = apply_action(conn, Action("drink", 5, DRINKING_WATER, "rehydrate"))
        assert after_water["thirst"] < 30.0
        after_meal = apply_action(conn, Action("eat", 25, MEAL_INGREDIENTS, "eat a meal"))
        assert after_meal["hunger"] < 35.0
        assert after_meal["energy"] > after_water["energy"]
        set_field(conn, "char_darian", "runtime.location", MASTER_BATHROOM)
        set_field(conn, "char_darian", "physiology.cleanliness", 35.0)
        conn.commit()
        after_shower = apply_action(conn, Action("shower", 15, MASTER_SHOWER, "restore cleanliness"))
        assert after_shower["cleanliness"] == 100.0


def test_restorative_item_action_requires_authored_effect(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", "loc_thorne_estate_dining_area")
        conn.execute("UPDATE entities SET capabilities_json='[\"eat\"]' WHERE id=?", (DINING_TABLE,))
        conn.commit()
        with pytest.raises(ValueError, match="no authored eat physiological effect"):
            validate_action(conn, "char_darian", Action("eat", 20, DINING_TABLE))


def test_p1_darian_completes_one_simulated_day_autonomously(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        start = ensure_sim_clock(conn)
        trace = run_one_simulated_day(conn)
        end = ensure_sim_clock(conn)
        assert end == start + timedelta(hours=24)
        assert 1 <= len(trace) <= 200
        events = conn.execute("SELECT payload_json FROM events WHERE actor_id='char_darian' AND event_type='action_completed'").fetchall()
        assert len(events) == len(trace)
        action_names = {__import__("json").loads(row[0])["action"] for row in events}
        assert "move" in action_names
        assert action_names & {"train", "eat", "drink", "sleep", "read", "rest"}
        final = snapshot(conn)
        for key in ("energy", "hunger", "thirst", "sleepiness", "cleanliness"):
            assert 0 <= final[key] <= 100
        assert final["current_action"] == "idle"

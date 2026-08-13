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


def test_p1_home_seed_and_darian_instantiation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert conn.execute("SELECT COUNT(*) FROM entities WHERE entity_type='location'").fetchone()[0] >= 20
        assert conn.execute("SELECT COUNT(*) FROM entities WHERE entity_type='object'").fetchone()[0] == 15
        assert conn.execute("SELECT name FROM entities WHERE id='home'").fetchone()[0] == "Thorne Estate"
        assert conn.execute("SELECT name FROM entities WHERE id='room_bedroom'").fetchone()[0] == "Darian's Master Suite"
        assert conn.execute("SELECT name FROM entities WHERE id='room_gym'").fetchone()[0] == "Top-Class Home Gym"
        assert conn.execute("SELECT name FROM entities WHERE id='char_darian'").fetchone()[0] == "Darian Thorne"
        state = snapshot(conn)
        assert state["location"] == "room_bedroom"
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
            "SELECT 1 FROM relations WHERE source_id='home' AND relation_type='contains' AND target_id='zone_underground'"
        ).fetchone() is not None
        assert conn.execute(
            "SELECT 1 FROM relations WHERE source_id='zone_underground' AND relation_type='contains' AND target_id='room_gym'"
        ).fetchone() is not None
        assert conn.execute(
            "SELECT 1 FROM relations WHERE relation_type='connected_to' AND (source_id='boundary_exterior' OR target_id='boundary_exterior')"
        ).fetchone() is None
        set_field(conn, "char_darian", "runtime.location", "room_foyer")
        conn.commit()
        with pytest.raises(ValueError):
            validate_action(conn, "char_darian", Action("move", 5, "boundary_exterior"))


def test_p1_runtime_rejects_non_adjacent_move(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        with pytest.raises(ValueError):
            validate_action(conn, "char_darian", Action("move", 5, "room_armory"))


def test_recovery_actions_increase_energy_and_rest_is_available_anywhere(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", "room_gym")
        set_field(conn, "char_darian", "needs.energy", 20.0)
        set_field(conn, "char_darian", "needs.sleepiness", 65.0)
        conn.commit()

        options = action_options(conn)
        rest = next(option for option in options if option["action"] == "rest" and option["target"] is None)
        assert rest["effects_per_hour"]["energy"] > 0

        before = snapshot(conn)
        after_idle = apply_action(conn, Action("idle", 60, None, "brief pause"))
        assert after_idle["energy"] > before["energy"]

        after_rest = apply_action(conn, Action("rest", 60, None, "recover low energy"))
        assert after_rest["energy"] >= after_idle["energy"] + 7.9
        assert after_rest["sleepiness"] < after_idle["sleepiness"]


def test_sleep_is_strong_recovery_and_can_escape_critical_energy(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", "room_bedroom")
        set_field(conn, "char_darian", "needs.energy", 18.0)
        set_field(conn, "char_darian", "needs.sleepiness", 88.0)
        conn.commit()

        after = apply_action(conn, Action("sleep", 480, "obj_bed", "overnight recovery"))
        assert after["energy"] >= 89.0
        assert after["sleepiness"] <= 5.0
        assert after["hunger"] < 50.0
        assert after["thirst"] < 50.0


def test_food_water_and_shower_restore_authored_basic_stats(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", "room_kitchen")
        set_field(conn, "char_darian", "needs.energy", 25.0)
        set_field(conn, "char_darian", "needs.hunger", 80.0)
        set_field(conn, "char_darian", "needs.thirst", 80.0)
        conn.commit()

        options = action_options(conn)
        water = next(option for option in options if option["action"] == "drink" and option["target"] == "obj_water")
        meal = next(option for option in options if option["action"] == "eat" and option["target"] == "obj_meal_stock")
        assert water["effects"]["needs.thirst"] == -55.0
        assert meal["effects"]["needs.hunger"] == -50.0
        assert meal["effects"]["needs.energy"] == 8.0

        after_water = apply_action(conn, Action("drink", 5, "obj_water", "rehydrate"))
        assert after_water["thirst"] < 30.0

        after_meal = apply_action(conn, Action("eat", 25, "obj_meal_stock", "eat a meal"))
        assert after_meal["hunger"] < 35.0
        assert after_meal["energy"] > after_water["energy"]

        set_field(conn, "char_darian", "runtime.location", "room_bathroom")
        set_field(conn, "char_darian", "physiology.cleanliness", 35.0)
        conn.commit()
        after_shower = apply_action(conn, Action("shower", 15, "obj_shower", "restore cleanliness"))
        assert after_shower["cleanliness"] == 100.0


def test_restorative_item_action_requires_authored_effect(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", "room_kitchen")
        conn.execute("UPDATE entities SET capabilities_json='[\"eat\"]' WHERE id='obj_table'")
        conn.execute("DELETE FROM relations WHERE target_id='obj_table' AND relation_type='contains'")
        conn.execute("INSERT OR IGNORE INTO relations(source_id, relation_type, target_id) VALUES('room_kitchen','contains','obj_table')")
        conn.commit()
        with pytest.raises(ValueError, match="no authored eat physiological effect"):
            validate_action(conn, "char_darian", Action("eat", 20, "obj_table"))


def test_p1_darian_completes_one_simulated_day_autonomously(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        start = ensure_sim_clock(conn)
        trace = run_one_simulated_day(conn)
        end = ensure_sim_clock(conn)
        assert end == start + timedelta(hours=24)
        assert 1 <= len(trace) <= 200

        events = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id='char_darian' AND event_type='action_completed'"
        ).fetchall()
        assert len(events) == len(trace)

        action_names = {__import__("json").loads(row[0])["action"] for row in events}
        assert "move" in action_names
        assert action_names & {"train", "eat", "drink", "sleep", "read", "rest"}

        final = snapshot(conn)
        for key in ("energy", "hunger", "thirst", "sleepiness", "cleanliness"):
            assert 0 <= final[key] <= 100
        assert final["current_action"] == "idle"

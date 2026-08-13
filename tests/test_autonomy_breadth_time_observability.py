from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import action_options
from observer_sandbox.telegram_notifications import format_action_completion
from observer_sandbox.world import set_field


def test_estate_breadth_exposes_purposeful_non_kitchen_targets(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        targets = {
            "loc_thorne_estate_garage": "obj_thorne_estate_garage_workbench",
            "loc_thorne_estate_intelligence_hub": "obj_thorne_estate_intel_surveillance_console",
            "loc_thorne_estate_comms": "obj_thorne_estate_comms_secure_terminal",
            "loc_thorne_estate_training_hall": "obj_thorne_estate_training_practice_dummy",
            "loc_thorne_estate_medical_bay": "obj_thorne_estate_medical_diagnostic_station",
            "loc_thorne_estate_armory": "obj_thorne_estate_armory_equipment_bench",
            "loc_thorne_estate_bunker": "obj_thorne_estate_bunker_emergency_console",
        }
        for room_id, target_id in targets.items():
            set_field(conn, "char_darian", "runtime.location", room_id)
            conn.commit()
            options = action_options(conn)
            assert any(option["target"] == target_id for option in options)


def test_generic_inspection_duration_is_bounded_for_cognition(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        row = conn.execute(
            "SELECT min_duration_minutes,max_duration_minutes FROM action_definitions WHERE action_type='inspect'"
        ).fetchone()
        assert tuple(row) == (1, 10)
        set_field(conn, "char_darian", "runtime.location", "loc_thorne_estate_kitchen")
        conn.commit()
        pantry = next(
            option
            for option in action_options(conn)
            if option["action"] == "inspect" and option["target"] == "obj_thorne_estate_kitchen_pantry"
        )
        assert pantry["duration"] == (1, 10)


def test_completion_notification_shows_elapsed_and_next_eta():
    before = {
        "sim_time": "2025-05-01T15:20:00+00:00",
        "location_name": "Kitchen",
        "energy": 74.5,
        "hunger": 20.0,
        "thirst": 15.0,
        "sleepiness": 15.0,
        "cleanliness": 80.0,
    }
    after = {
        "sim_time": "2025-05-01T15:25:00+00:00",
        "location_name": "Kitchen",
        "energy": 74.3,
        "hunger": 20.2,
        "thirst": 15.2,
        "sleepiness": 15.2,
        "cleanliness": 79.9,
    }
    completed = {
        "action": "inspect",
        "target_name": "Pantry",
        "duration_minutes": 5,
        "speed_at_plan": 1.0,
        "reason": "Check supplies briefly.",
    }
    next_action = {
        "action": "move",
        "target_name": "Living Room",
        "duration_minutes": 5,
        "speed_at_plan": 1.0,
        "planned_sim_time": "2025-05-01T15:25:00+00:00",
    }
    text = format_action_completion(
        completed,
        before,
        after,
        actor_name="Darian Thorne",
        next_action=next_action,
    )
    assert "Took 5 sim min" in text
    assert "~5 min real @ 1x" in text
    assert "Next: Move → Living Room" in text
    assert "Expected update: 01-05-2025 (Thursday) 03:30 PM" in text

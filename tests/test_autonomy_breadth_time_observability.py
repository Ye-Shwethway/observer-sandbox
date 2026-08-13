from observer_sandbox.db import connect
from observer_sandbox.model_decision import load_autonomy_policy
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import action_options
from observer_sandbox.telegram_bot import _fmt_character, _fmt_status
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


def test_quick_duration_guidance_preserves_runtime_compatibility_bounds(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    policy = load_autonomy_policy()
    assert policy["duration_guidance"]["quick_discretionary"]["inspect_minutes"] == [2, 6]
    assert policy["duration_guidance"]["quick_discretionary"]["simple_use_minutes"] == [2, 10]
    with connect(db) as conn:
        inspect_row = conn.execute(
            "SELECT min_duration_minutes,max_duration_minutes FROM action_definitions WHERE action_type='inspect'"
        ).fetchone()
        use_row = conn.execute(
            "SELECT min_duration_minutes,max_duration_minutes FROM action_definitions WHERE action_type='use'"
        ).fetchone()
        assert tuple(inspect_row) == (1, 60)
        assert tuple(use_row) == (1, 120)


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


def test_current_character_and_runtime_cards_show_pending_eta():
    character = {
        "character": {"name": "Darian Thorne"},
        "state": {
            "location_name": "Living Room",
            "current_action": "read",
            "sim_time": "2025-05-01T16:20:00+00:00",
            "energy": 80.0,
            "hunger": 0.2,
            "thirst": 21.5,
            "sleepiness": 19.5,
            "cleanliness": 78.8,
        },
    }
    status = {
        "character": character["state"],
        "autonomy_enabled": True,
        "mode": "normal",
        "paused": False,
        "speed": 1.0,
        "cognition_stats": {"decision_calls": 30},
        "pending_target_name": "Field Manual",
        "pending_action": {
            "action": "read",
            "target": "obj_field_manual",
            "duration_minutes": 10,
            "speed_at_plan": 1.0,
            "planned_sim_time": "2025-05-01T16:20:00+00:00",
            "due_wall_time": 1300.0,
        },
    }

    text = _fmt_character(character, status, now_wall=1000.0)
    assert "Action     Read → Field Manual" in text
    assert "Duration   10 sim min • ~10 min real @ 1x" in text
    assert "Expected   01-05-2025 (Thursday) 04:30 PM" in text
    assert "Remaining  ~5 min real" in text

    runtime_text = _fmt_status(status, now_wall=1000.0)
    assert "Pending    Read → Field Manual" in runtime_text
    assert "Duration   10 sim min • ~10 min real @ 1x" in runtime_text
    assert "Expected   01-05-2025 (Thursday) 04:30 PM" in runtime_text
    assert "Remaining  ~5 min real" in runtime_text

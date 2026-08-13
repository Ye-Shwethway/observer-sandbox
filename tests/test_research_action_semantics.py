import pytest

from observer_sandbox.db import connect
from observer_sandbox.duration_planning import duration_profile, normalize_duration
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_definition, action_options, apply_action, snapshot, validate_action
from observer_sandbox.world import set_field

LIBRARY = "loc_thorne_estate_library"
RESEARCH_DESK = "obj_thorne_estate_library_research_desk"
BOOKSHELF = "obj_thorne_estate_library_bookshelf"


def test_research_action_is_registered_and_only_exposed_by_research_capability(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        definition = action_definition(conn, "research")
        assert definition["target_mode"] == "object"
        assert definition["required_capability"] == "research"
        assert (definition["min_duration_minutes"], definition["max_duration_minutes"]) == (10, 180)

        set_field(conn, "char_darian", "runtime.location", LIBRARY)
        conn.commit()
        options = action_options(conn, "char_darian")
        research = [option for option in options if option["action"] == "research"]
        assert [(option["target"], option["target_name"]) for option in research] == [(RESEARCH_DESK, "Research Desk")]

        validate_action(conn, "char_darian", Action("research", 45, RESEARCH_DESK, "review estate records"))
        with pytest.raises(ValueError):
            validate_action(conn, "char_darian", Action("research", 45, BOOKSHELF, "unsupported research target"))


def test_research_has_deterministic_planning_profile_and_first_class_completion(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", LIBRARY)
        conn.commit()

        profile = duration_profile("research", RESEARCH_DESK)
        assert profile is not None
        assert (profile.min_minutes, profile.max_minutes) == (30, 90)
        assert normalize_duration("research", RESEARCH_DESK, 5) == 30
        assert normalize_duration("research", RESEARCH_DESK, 200) == 90

        before = snapshot(conn)
        after = apply_action(conn, Action("research", 45, RESEARCH_DESK, "review estate records"))
        assert after["sim_time"] != before["sim_time"]
        row = conn.execute(
            "SELECT action_type,target_id,status,duration_minutes FROM action_instances ORDER BY created_at DESC, rowid DESC LIMIT 1"
        ).fetchone()
        assert tuple(row) == ("research", RESEARCH_DESK, "completed", 45)
        event = conn.execute(
            "SELECT payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert '"action": "research"' in event["payload_json"]
        assert RESEARCH_DESK in event["payload_json"]

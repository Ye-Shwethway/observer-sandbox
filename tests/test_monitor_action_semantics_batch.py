import pytest

from observer_sandbox.db import connect
from observer_sandbox.duration_planning import normalize_duration
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_definition, action_options, apply_action, validate_action
from observer_sandbox.world import set_field

CASES = (
    ("loc_thorne_estate_intelligence_hub", "obj_thorne_estate_intel_surveillance_console", "Surveillance Console"),
    ("loc_thorne_estate_comms", "obj_thorne_estate_comms_secure_terminal", "Secure Communications Terminal"),
    ("loc_thorne_estate_bunker", "obj_thorne_estate_bunker_emergency_console", "Emergency Console"),
)


def test_monitor_batch_exposes_only_authored_local_console_targets(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        definition = action_definition(conn, "monitor")
        assert tuple(definition[key] for key in ("min_duration_minutes", "max_duration_minutes")) == (5, 120)
        assert definition["target_mode"] == "object"
        assert definition["required_capability"] == "monitor"

        for room, target, name in CASES:
            set_field(conn, "char_darian", "runtime.location", room)
            conn.commit()
            options = [option for option in action_options(conn) if option["action"] == "monitor"]
            assert [(option["target"], option["target_name"]) for option in options] == [(target, name)]
            validate_action(conn, "char_darian", Action("monitor", 30, target, "check current systems"))

        set_field(conn, "char_darian", "runtime.location", "loc_thorne_estate_living_room")
        conn.commit()
        with pytest.raises(ValueError):
            validate_action(
                conn,
                "char_darian",
                Action("monitor", 30, "obj_thorne_estate_living_media_console", "unsupported monitor target"),
            )


def test_monitor_batch_uses_one_preferred_profile_and_persists_each_target(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert normalize_duration("monitor", CASES[0][1], 5) == 15
        assert normalize_duration("monitor", CASES[0][1], 90) == 45

        completed = []
        for room, target, _ in CASES:
            set_field(conn, "char_darian", "runtime.location", room)
            conn.commit()
            apply_action(conn, Action("monitor", 30, target, "check current systems"))
            row = conn.execute(
                "SELECT action_type,target_id,status,duration_minutes FROM action_instances ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
            completed.append(tuple(row))

        assert completed == [
            ("monitor", CASES[0][1], "completed", 30),
            ("monitor", CASES[1][1], "completed", 30),
            ("monitor", CASES[2][1], "completed", 30),
        ]
        payloads = [
            row[0]
            for row in conn.execute(
                "SELECT payload_json FROM events WHERE event_type='action_completed' ORDER BY id DESC LIMIT 3"
            ).fetchall()
        ]
        for _, target, _ in CASES:
            assert any('"action": "monitor"' in payload and target in payload for payload in payloads)

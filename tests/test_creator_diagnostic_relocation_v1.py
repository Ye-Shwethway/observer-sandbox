from datetime import datetime, timedelta

import pytest

from observer_sandbox.actor_runtime import actor_runtime
from observer_sandbox.creator_diagnostics import relocate_character_for_diagnostic
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import runtime_value, snapshot
from observer_sandbox.telegram_ai_control import callback_view as creator_settings_callback
from observer_sandbox.telegram_creator_diagnostics import _locations


CORE_GROUNDS = "loc_thorne_estate_core_grounds"
DARIAN = "char_darian"


def _callbacks(keyboard):
    return [button["callback_data"] for row in keyboard or [] for button in row]


def test_creator_diagnostic_relocation_preserves_time_and_audits(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = snapshot(conn, DARIAN)
        result = relocate_character_for_diagnostic(
            conn,
            DARIAN,
            CORE_GROUNDS,
            authority="creator",
            requested_by="test",
        )
        after = snapshot(conn, DARIAN)

        assert result["time_mode"] == "preserve"
        assert after["sim_time"] == before["sim_time"]
        assert after["location"] == CORE_GROUNDS
        assert after["current_action"] == "idle"
        assert actor_runtime(conn, DARIAN)["wake_reason"] == "creator_diagnostic_relocation"

        event = conn.execute(
            "SELECT event_type,payload_json FROM events WHERE actor_id=? ORDER BY id DESC LIMIT 1",
            (DARIAN,),
        ).fetchone()
        assert event["event_type"] == "creator_diagnostic_relocation"
        assert '"diagnostic_only": true' in event["payload_json"]
        assert '"time_mode": "preserve"' in event["payload_json"]


def test_creator_diagnostic_relocation_allows_explicit_forward_raw_time_jump(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before_time = datetime.fromisoformat(str(runtime_value(conn, "sim_time", None)))
        target = before_time + timedelta(hours=6)
        result = relocate_character_for_diagnostic(
            conn,
            DARIAN,
            CORE_GROUNDS,
            sim_time=target.isoformat(),
            requested_by="test",
        )

        assert snapshot(conn, DARIAN)["sim_time"] == target.isoformat()
        assert result["time_mode"] == "raw_forward_jump"
        assert result["elapsed_minutes_without_simulation"] == 360.0


def test_creator_diagnostic_relocation_rejects_backward_time(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        current = datetime.fromisoformat(str(runtime_value(conn, "sim_time", None)))
        with pytest.raises(ValueError, match="cannot move simulation time backward"):
            relocate_character_for_diagnostic(
                conn,
                DARIAN,
                CORE_GROUNDS,
                sim_time=(current - timedelta(minutes=1)).isoformat(),
                requested_by="test",
            )


def test_creator_settings_exposes_owner_diagnostics_and_flow_uses_routed_callbacks(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        text, keyboard = creator_settings_callback(conn, 42, "ai:home")
        assert "CREATOR SETTINGS" in text
        assert "ai:diag:home" in _callbacks(keyboard)

        text, keyboard = creator_settings_callback(conn, 42, "ai:diag:home")
        assert "CREATOR DIAGNOSTICS" in text
        assert "ai:diag:move" in _callbacks(keyboard)
        assert not any(value.startswith("diag:") for value in _callbacks(keyboard))

        text, keyboard = creator_settings_callback(conn, 42, "ai:diag:move")
        assert "DIAGNOSTIC RELOCATION" in text
        character_callbacks = [value for value in _callbacks(keyboard) if value.startswith("ai:diag:c:")]
        assert character_callbacks

        text, keyboard = creator_settings_callback(conn, 42, character_callbacks[0])
        assert "SELECT TARGET LOCATION" in text
        locations = _locations(conn)
        core_index = next(index for index, row in enumerate(locations) if row["id"] == CORE_GROUNDS)
        location_callback = f"ai:diag:l:{core_index}"
        # Location pagination may not currently display this row, but callback
        # identity is stable against the same sorted represented-location list.
        text, keyboard = creator_settings_callback(conn, 42, location_callback)
        assert "DIAGNOSTIC TIME" in text
        assert "Keep Current Time" in " ".join(button["text"] for row in keyboard for button in row)

        text, keyboard = creator_settings_callback(conn, 42, "ai:diag:t:keep")
        assert "REVIEW CREATOR RELOCATION" in text
        assert "ai:diag:confirm" in _callbacks(keyboard)

        before_time = snapshot(conn, DARIAN)["sim_time"]
        text, keyboard = creator_settings_callback(conn, 42, "ai:diag:confirm")
        assert "CREATOR RELOCATION APPLIED" in text
        after = snapshot(conn, DARIAN)
        assert after["location"] == CORE_GROUNDS
        assert after["sim_time"] == before_time

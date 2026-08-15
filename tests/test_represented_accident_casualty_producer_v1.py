from __future__ import annotations

import json

import pytest

from observer_sandbox.casualty_state_lifecycle import AUTHORITY, INITIALIZED_EVENT, SOURCE as LIFECYCLE_SOURCE
from observer_sandbox.db import connect
from observer_sandbox.field_medicine_stabilization import DETERIORATION_FIELD
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.represented_accident_casualty import (
    EVENT_TYPE,
    SOURCE,
    RepresentedAccidentCasualtyError,
    record_represented_accident_casualty,
)
from observer_sandbox.runtime import initialize
from observer_sandbox.world import get_field, set_field


CASUALTY = "char_test_represented_accident_casualty"
ROOM = "loc_thorne_estate_living_room"
OTHER_ROOM = "loc_thorne_estate_library"


def _prepare(conn) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json,definition_id) VALUES(?,?,?,?,?,?)",
        (CASUALTY, "character", "Represented Accident Casualty", "{}", "[]", "test:accident-casualty-v1"),
    )
    set_dynamic_location(conn, CASUALTY, ROOM)
    conn.commit()


def test_represented_fall_emits_source_event_then_initializes_casualty_state(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        result = record_represented_accident_casualty(
            conn,
            incident_id="accident-v1-001",
            casualty_id=CASUALTY,
            location_id=ROOM,
            sim_time="2025-05-06T10:00:00+00:00",
            accident_kind="represented_fall",
            risk_class="moderate",
        )

        assert result["already_applied"] is False
        assert result["deterioration_risk"] == pytest.approx(50.0)
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(50.0)

        field = conn.execute(
            "SELECT mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
            (CASUALTY, DETERIORATION_FIELD),
        ).fetchone()
        assert tuple(field) == ("simulated", AUTHORITY, LIFECYCLE_SOURCE)

        events = conn.execute(
            "SELECT id,event_type,actor_id,location_id,caused_by_event_id,payload_json,state_changes_json FROM events WHERE id IN (?,?) ORDER BY id",
            (result["source_event_id"], result["lifecycle_event_id"]),
        ).fetchall()
        assert [row["event_type"] for row in events] == [EVENT_TYPE, INITIALIZED_EVENT]
        source_event, lifecycle_event = events
        assert source_event["actor_id"] == CASUALTY
        assert source_event["location_id"] == ROOM
        assert source_event["caused_by_event_id"] is None
        assert lifecycle_event["caused_by_event_id"] == source_event["id"]

        source_payload = json.loads(source_event["payload_json"])
        assert source_payload["source"] == SOURCE
        assert source_payload["incident_id"] == "accident-v1-001"
        assert source_payload["accident_kind"] == "represented_fall"
        assert source_payload["risk_class"] == "moderate"
        assert source_payload["deterioration_risk"] == pytest.approx(50.0)
        assert source_payload["injury_created"] is False
        assert source_payload["diagnosis_created"] is False
        assert source_payload["incapacity_created"] is False
        assert source_payload["learning_evidence"] is False
        assert json.loads(source_event["state_changes_json"]) == {}

        participant = conn.execute(
            "SELECT role FROM event_participants WHERE event_id=? AND entity_id=?",
            (source_event["id"], CASUALTY),
        ).fetchone()
        assert participant["role"] == "casualty"

        lifecycle_changes = json.loads(lifecycle_event["state_changes_json"])
        change = lifecycle_changes["fields"][DETERIORATION_FIELD]
        assert change == {"before": None, "after": 50.0, "operation": "create"}


def test_retry_same_incident_is_idempotent(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        kwargs = dict(
            incident_id="accident-v1-retry",
            casualty_id=CASUALTY,
            location_id=ROOM,
            sim_time="2025-05-06T10:05:00+00:00",
            accident_kind="represented_fall",
            risk_class="low",
        )
        first = record_represented_accident_casualty(conn, **kwargs)
        second = record_represented_accident_casualty(conn, **kwargs)
        assert first["already_applied"] is False
        assert second["already_applied"] is True
        assert second["source_event_id"] == first["source_event_id"]
        assert second["lifecycle_event_id"] == first["lifecycle_event_id"]
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(25.0)
        assert conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type=?",
            (EVENT_TYPE,),
        ).fetchone()[0] == 1
        assert conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type=?",
            (INITIALIZED_EVENT,),
        ).fetchone()[0] == 1


def test_incident_id_cannot_be_reused_with_different_semantics(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        record_represented_accident_casualty(
            conn,
            incident_id="accident-v1-conflict",
            casualty_id=CASUALTY,
            location_id=ROOM,
            sim_time="2025-05-06T10:10:00+00:00",
            accident_kind="represented_fall",
            risk_class="low",
        )
        with pytest.raises(RepresentedAccidentCasualtyError, match="different semantics"):
            record_represented_accident_casualty(
                conn,
                incident_id="accident-v1-conflict",
                casualty_id=CASUALTY,
                location_id=ROOM,
                sim_time="2025-05-06T10:11:00+00:00",
                accident_kind="represented_fall",
                risk_class="high",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(25.0)


def test_wrong_location_fails_before_event_or_state_creation(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        before_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        with pytest.raises(RepresentedAccidentCasualtyError, match="declared accident location"):
            record_represented_accident_casualty(
                conn,
                incident_id="accident-v1-wrong-location",
                casualty_id=CASUALTY,
                location_id=OTHER_ROOM,
                sim_time="2025-05-06T10:15:00+00:00",
                accident_kind="represented_fall",
                risk_class="moderate",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) is None
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == before_events


def test_existing_casualty_state_rolls_back_accident_source_event(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        set_field(
            conn,
            CASUALTY,
            DETERIORATION_FIELD,
            40.0,
            mode="simulated",
            authority="other_domain",
            source="other-source",
        )
        conn.commit()
        before_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        with pytest.raises(ValueError, match="already exists"):
            record_represented_accident_casualty(
                conn,
                incident_id="accident-v1-existing-state",
                casualty_id=CASUALTY,
                location_id=ROOM,
                sim_time="2025-05-06T10:20:00+00:00",
                accident_kind="represented_fall",
                risk_class="high",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(40.0)
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == before_events
        assert conn.execute(
            "SELECT 1 FROM events WHERE event_type=? AND payload_json LIKE '%accident-v1-existing-state%'",
            (EVENT_TYPE,),
        ).fetchone() is None


def test_free_form_or_unsupported_accident_semantics_fail_closed(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _prepare(conn)
        with pytest.raises(RepresentedAccidentCasualtyError, match="Unsupported represented accident kind"):
            record_represented_accident_casualty(
                conn,
                incident_id="accident-v1-freeform",
                casualty_id=CASUALTY,
                location_id=ROOM,
                sim_time="2025-05-06T10:25:00+00:00",
                accident_kind="fell badly and probably broke an arm",
                risk_class="moderate",
            )
        with pytest.raises(RepresentedAccidentCasualtyError, match="risk class"):
            record_represented_accident_casualty(
                conn,
                incident_id="accident-v1-unsupported-risk",
                casualty_id=CASUALTY,
                location_id=ROOM,
                sim_time="2025-05-06T10:26:00+00:00",
                accident_kind="represented_fall",
                risk_class="critical",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) is None

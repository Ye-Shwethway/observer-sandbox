from __future__ import annotations

import json

import pytest

from observer_sandbox.casualty_state_lifecycle import (
    AUTHORITY,
    CLEARED_EVENT,
    INITIALIZED_EVENT,
    SOURCE,
    CasualtyStateLifecycleError,
    clear_casualty_state,
    initialize_casualty_state,
)
from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.field_medicine_stabilization import DETERIORATION_FIELD
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot
from observer_sandbox.world import get_field, set_field


CASUALTY = "char_test_casualty_lifecycle"
ROOM = "loc_thorne_estate_medical_bay"


def _add_casualty(conn) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json,definition_id) VALUES(?,?,?,?,?,?)",
        (CASUALTY, "character", "Lifecycle Test Casualty", "{}", "[]", "test:casualty_lifecycle_v1"),
    )
    conn.commit()


def _source_event(conn, *, role: str = "casualty", event_type: str = "represented_hazard_resolved") -> int:
    sim_time = snapshot(conn, "char_darian")["sim_time"]
    return record_event(
        conn,
        sim_time=sim_time,
        event_type=event_type,
        actor_id="char_darian",
        location_id=ROOM,
        participants=[{"entity_id": CASUALTY, "role": role}],
        payload={"source": "test", "represented": True},
    )


def test_explicit_casualty_source_event_creates_one_owned_simulated_state(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_casualty(conn)
        source_event_id = _source_event(conn, event_type="represented_accident_occurred")

        result = initialize_casualty_state(
            conn,
            casualty_id=CASUALTY,
            deterioration_risk=60.0,
            source_event_id=source_event_id,
            origin_kind="represented_accident",
        )

        assert result["already_applied"] is False
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(60.0)
        row = conn.execute(
            "SELECT mode,authority,source FROM fields WHERE entity_id=? AND field_key=?",
            (CASUALTY, DETERIORATION_FIELD),
        ).fetchone()
        assert tuple(row) == ("simulated", AUTHORITY, SOURCE)

        event = conn.execute(
            "SELECT event_type,caused_by_event_id,payload_json,state_changes_json FROM events WHERE id=?",
            (result["event_id"],),
        ).fetchone()
        assert event["event_type"] == INITIALIZED_EVENT
        assert event["caused_by_event_id"] == source_event_id
        payload = json.loads(event["payload_json"])
        changes = json.loads(event["state_changes_json"])
        assert payload["casualty_id"] == CASUALTY
        assert payload["origin_kind"] == "represented_accident"
        assert payload["diagnosis_created"] is False
        assert payload["definitive_treatment_created"] is False
        assert payload["learning_evidence"] is False
        assert changes["fields"][DETERIORATION_FIELD] == {
            "before": None,
            "after": 60.0,
            "operation": "create",
        }


def test_origin_requires_explicit_casualty_role_and_never_infers_from_event_text(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_casualty(conn)
        source_event_id = _source_event(conn, role="participant", event_type="injury sounding prose event")
        with pytest.raises(CasualtyStateLifecycleError, match="role 'casualty'"):
            initialize_casualty_state(
                conn,
                casualty_id=CASUALTY,
                deterioration_risk=40.0,
                source_event_id=source_event_id,
                origin_kind="represented_domain_consequence",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD, None) is None


def test_origin_cannot_overwrite_preexisting_state_from_another_authority(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_casualty(conn)
        set_field(
            conn,
            CASUALTY,
            DETERIORATION_FIELD,
            35.0,
            mode="simulated",
            authority="other_domain",
            source="other-source",
        )
        source_event_id = _source_event(conn)
        with pytest.raises(CasualtyStateLifecycleError, match="already exists"):
            initialize_casualty_state(
                conn,
                casualty_id=CASUALTY,
                deterioration_risk=80.0,
                source_event_id=source_event_id,
                origin_kind="represented_environmental_hazard",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(35.0)


def test_origin_retry_is_idempotent_for_same_source_event(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_casualty(conn)
        source_event_id = _source_event(conn)
        first = initialize_casualty_state(
            conn,
            casualty_id=CASUALTY,
            deterioration_risk=50.0,
            source_event_id=source_event_id,
            origin_kind="represented_domain_consequence",
        )
        second = initialize_casualty_state(
            conn,
            casualty_id=CASUALTY,
            deterioration_risk=50.0,
            source_event_id=source_event_id,
            origin_kind="represented_domain_consequence",
        )
        assert second["already_applied"] is True
        assert second["event_id"] == first["event_id"]
        assert conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type=? AND caused_by_event_id=?",
            (INITIALIZED_EVENT, source_event_id),
        ).fetchone()[0] == 1


def test_zero_risk_does_not_auto_clear_casualty_context(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_casualty(conn)
        source_event_id = _source_event(conn)
        initialize_casualty_state(
            conn,
            casualty_id=CASUALTY,
            deterioration_risk=0.0,
            source_event_id=source_event_id,
            origin_kind="represented_domain_consequence",
        )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(0.0)
        assert conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type=?",
            (CLEARED_EVENT,),
        ).fetchone()[0] == 0


def test_explicit_handoff_event_clears_owned_state_without_asserting_healing(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_casualty(conn)
        origin_event_id = _source_event(conn, event_type="represented_accident_occurred")
        initialize_casualty_state(
            conn,
            casualty_id=CASUALTY,
            deterioration_risk=25.0,
            source_event_id=origin_event_id,
            origin_kind="represented_accident",
        )
        resolution_event_id = _source_event(conn, event_type="represented_handoff_completed")
        result = clear_casualty_state(
            conn,
            casualty_id=CASUALTY,
            source_event_id=resolution_event_id,
            resolution_kind="evacuated_or_handed_off",
        )

        assert result["already_applied"] is False
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD, None) is None
        event = conn.execute(
            "SELECT event_type,caused_by_event_id,payload_json,state_changes_json FROM events WHERE id=?",
            (result["event_id"],),
        ).fetchone()
        assert event["event_type"] == CLEARED_EVENT
        assert event["caused_by_event_id"] == resolution_event_id
        payload = json.loads(event["payload_json"])
        changes = json.loads(event["state_changes_json"])
        assert payload["resolution_kind"] == "evacuated_or_handed_off"
        assert payload["healing_asserted"] is False
        assert payload["diagnosis_resolved"] is False
        assert payload["learning_evidence"] is False
        assert changes["fields"][DETERIORATION_FIELD] == {
            "before": 25.0,
            "after": None,
            "operation": "delete",
        }


def test_clear_cannot_delete_state_owned_by_another_domain(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_casualty(conn)
        set_field(
            conn,
            CASUALTY,
            DETERIORATION_FIELD,
            30.0,
            mode="simulated",
            authority="other_domain",
            source="other-source",
        )
        source_event_id = _source_event(conn)
        with pytest.raises(CasualtyStateLifecycleError, match="own V1 authority"):
            clear_casualty_state(
                conn,
                casualty_id=CASUALTY,
                source_event_id=source_event_id,
                resolution_kind="casualty_context_resolved",
            )
        assert get_field(conn, CASUALTY, DETERIORATION_FIELD) == pytest.approx(30.0)


def test_clear_retry_is_idempotent_for_same_resolution_event(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_casualty(conn)
        origin_event_id = _source_event(conn)
        initialize_casualty_state(
            conn,
            casualty_id=CASUALTY,
            deterioration_risk=45.0,
            source_event_id=origin_event_id,
            origin_kind="represented_domain_consequence",
        )
        resolution_event_id = _source_event(conn, event_type="represented_handoff_completed")
        first = clear_casualty_state(
            conn,
            casualty_id=CASUALTY,
            source_event_id=resolution_event_id,
            resolution_kind="evacuated_or_handed_off",
        )
        second = clear_casualty_state(
            conn,
            casualty_id=CASUALTY,
            source_event_id=resolution_event_id,
            resolution_kind="evacuated_or_handed_off",
        )
        assert second["already_applied"] is True
        assert second["event_id"] == first["event_id"]
        assert conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type=? AND caused_by_event_id=?",
            (CLEARED_EVENT, resolution_event_id),
        ).fetchone()[0] == 1

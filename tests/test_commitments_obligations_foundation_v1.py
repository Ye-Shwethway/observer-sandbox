from __future__ import annotations

import pytest

from observer_sandbox.commitment_schema import COMMITMENT_SCHEMA_VERSION, migrate_commitment_schema
from observer_sandbox.commitments import create_commitment, publish_commitment_notice, set_commitment_status
from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.runtime import initialize
from observer_sandbox.world_stimulus import eligible_world_stimuli, world_stimulus

DARIAN = "char_darian"
KITCHEN = "loc_thorne_estate_kitchen"


def test_commitment_schema_v1_migrates_idempotently(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        migrate_commitment_schema(conn)
        migrate_commitment_schema(conn)
        assert int(conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0]) == SCHEMA_VERSION
        assert int(conn.execute("SELECT value FROM schema_meta WHERE key='commitment_schema_version'").fetchone()[0]) == COMMITMENT_SCHEMA_VERSION == 1
        assert conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='commitments'").fetchone()


def test_commitment_types_are_generic(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        cases = [
            ("appointment", "2025-05-04T10:00:00+00:00", None),
            ("promise", None, "2025-05-04T12:00:00+00:00"),
            ("deadline", None, "2025-05-05T18:00:00+00:00"),
            ("scheduled_responsibility", "2025-05-06T09:00:00+00:00", None),
        ]
        for index, (kind, start, due) in enumerate(cases):
            item = create_commitment(
                conn,
                commitment_id=f"commitment_fixture_{index}",
                character_id=DARIAN,
                commitment_type=kind,
                title=f"Fixture {kind}",
                start_sim_time=start,
                due_sim_time=due,
                flexibility="reschedulable" if kind == "appointment" else "fixed",
                source_type="test_fixture",
            )
            assert item["commitment_type"] == kind
            assert item["status"] == "pending"


def test_commitment_notice_uses_w0_without_automatic_exposure_or_cognition(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        exposure_count = conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0]
        memory_count = conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0]
        mental_cycle_count = conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0]
        mental_artifact_count = conn.execute("SELECT COUNT(*) FROM mental_artifacts").fetchone()[0]

        create_commitment(
            conn,
            commitment_id="commitment_notice_fixture",
            character_id=DARIAN,
            commitment_type="appointment",
            title="Meet in the kitchen",
            start_sim_time="2025-05-04T17:00:00+00:00",
            target_location_id=KITCHEN,
            flexibility="reschedulable",
        )
        notice = publish_commitment_notice(
            conn,
            commitment_id="commitment_notice_fixture",
            stimulus_id="stim_commitment_notice_fixture",
            notice_sim_time="2025-05-04T16:30:00+00:00",
        )
        assert notice["stimulus_type"] == "obligation"
        assert notice["channel"] == "other"
        assert notice["source_type"] == "commitment"
        assert notice["source_id"] == "commitment_notice_fixture"
        assert notice["payload"]["target_location_id"] == KITCHEN
        eligible = eligible_world_stimuli(
            conn,
            character_id=DARIAN,
            sim_time="2025-05-04T16:31:00+00:00",
            location_id=KITCHEN,
        )
        assert [item["stimulus_id"] for item in eligible] == ["stim_commitment_notice_fixture"]
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == exposure_count
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == memory_count
        assert conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0] == mental_cycle_count
        assert conn.execute("SELECT COUNT(*) FROM mental_artifacts").fetchone()[0] == mental_artifact_count


def test_terminal_commitment_retires_linked_notice_and_validation_is_bounded(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        create_commitment(
            conn,
            commitment_id="commitment_terminal_fixture",
            character_id=DARIAN,
            commitment_type="deadline",
            title="Finish fixture",
            due_sim_time="2025-05-04T20:00:00+00:00",
        )
        publish_commitment_notice(
            conn,
            commitment_id="commitment_terminal_fixture",
            stimulus_id="stim_commitment_terminal_fixture",
            notice_sim_time="2025-05-04T19:00:00+00:00",
        )
        assert set_commitment_status(conn, "commitment_terminal_fixture", "completed")["status"] == "completed"
        assert world_stimulus(conn, "stim_commitment_terminal_fixture")["status"] == "retired"

        with pytest.raises(ValueError, match="terminal commitment"):
            publish_commitment_notice(
                conn,
                commitment_id="commitment_terminal_fixture",
                stimulus_id="stim_after_terminal",
                notice_sim_time="2025-05-04T19:30:00+00:00",
            )
        with pytest.raises(ValueError, match="requires start_sim_time or due_sim_time"):
            create_commitment(
                conn,
                commitment_id="commitment_missing_time",
                character_id=DARIAN,
                commitment_type="promise",
                title="No time",
            )
        with pytest.raises(ValueError, match="unsupported commitment_type"):
            create_commitment(
                conn,
                commitment_id="commitment_bad_type",
                character_id=DARIAN,
                commitment_type="unsupported_fixture",
                title="Bad",
                due_sim_time="2025-05-05T00:00:00+00:00",
            )
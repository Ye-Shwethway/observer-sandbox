from __future__ import annotations

import json

import pytest

from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.runtime import initialize
from observer_sandbox.world_input_schema import WORLD_INPUT_SCHEMA_VERSION, migrate_world_input_schema
from observer_sandbox.world_stimulus import (
    add_stimulus_scope,
    create_world_stimulus,
    eligible_world_stimuli,
    recent_character_exposures,
    record_character_exposure,
    world_stimulus,
)


DARIAN = "char_darian"
SUITE = "loc_thorne_estate_master_suite"
KITCHEN = "loc_thorne_estate_kitchen"


def _add_second_character(conn) -> str:
    character_id = "char_world_input_fixture"
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
        (character_id, "character", "World Input Fixture", "{}", "[]"),
    )
    conn.commit()
    return character_id


def test_world_input_schema_v1_migrates_idempotently(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        migrate_world_input_schema(conn)
        migrate_world_input_schema(conn)
        version = int(conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0])
        world_input_version = int(
            conn.execute("SELECT value FROM schema_meta WHERE key='world_input_schema_version'").fetchone()[0]
        )
        assert version == SCHEMA_VERSION
        assert SCHEMA_VERSION >= 9
        assert world_input_version == WORLD_INPUT_SCHEMA_VERSION == 1
        assert conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='world_stimuli'"
        ).fetchone()
        assert conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='world_stimulus_scopes'"
        ).fetchone()
        assert conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='character_exposures'"
        ).fetchone()


def test_stimulus_requires_explicit_matching_scope_and_does_not_record_exposure(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        create_world_stimulus(
            conn,
            stimulus_id="stim_rain_fixture",
            stimulus_type="environment",
            channel="environmental",
            subject="Cold rain outside",
            start_sim_time="2025-05-03T09:00:00+00:00",
            salience=0.7,
            payload={"condition": "rain", "temperature_f": 44},
            source_type="weather_fixture",
            source_id="weather_2025_05_03_0900",
        )
        assert eligible_world_stimuli(
            conn,
            character_id=DARIAN,
            sim_time="2025-05-03T09:05:00+00:00",
            location_id=SUITE,
        ) == []

        add_stimulus_scope(
            conn,
            stimulus_id="stim_rain_fixture",
            scope_type="location",
            scope_id="loc_thorne_estate_mansion_exterior",
        )
        assert eligible_world_stimuli(
            conn,
            character_id=DARIAN,
            sim_time="2025-05-03T09:05:00+00:00",
            location_id=SUITE,
        ) == []
        eligible = eligible_world_stimuli(
            conn,
            character_id=DARIAN,
            sim_time="2025-05-03T09:05:00+00:00",
            location_id="loc_thorne_estate_mansion_exterior",
        )
        assert [item["stimulus_id"] for item in eligible] == ["stim_rain_fixture"]
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == 0


def test_character_targeting_is_generic_and_does_not_leak_to_other_character(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        second = _add_second_character(conn)
        create_world_stimulus(
            conn,
            stimulus_id="stim_private_notice_fixture",
            stimulus_type="information",
            channel="device",
            subject="Private device notice",
            start_sim_time="2025-05-03T10:00:00+00:00",
        )
        add_stimulus_scope(
            conn,
            stimulus_id="stim_private_notice_fixture",
            scope_type="character",
            scope_id=second,
            relation_role="targeted_to",
        )
        assert eligible_world_stimuli(
            conn,
            character_id=DARIAN,
            sim_time="2025-05-03T10:01:00+00:00",
            location_id=SUITE,
        ) == []
        eligible = eligible_world_stimuli(
            conn,
            character_id=second,
            sim_time="2025-05-03T10:01:00+00:00",
            location_id=SUITE,
        )
        assert [item["stimulus_id"] for item in eligible] == ["stim_private_notice_fixture"]


def test_recording_exposure_preserves_world_memory_and_mind_authority_boundaries(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        event_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        memory_count = conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0]
        mental_cycle_count = conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0]

        create_world_stimulus(
            conn,
            stimulus_id="stim_tv_fixture",
            stimulus_type="information",
            channel="media",
            subject="Television news fixture",
            start_sim_time="2025-05-03T11:00:00+00:00",
            payload={"headline": "Fixture headline"},
            source_type="media_item",
            source_id="media_fixture_001",
        )
        add_stimulus_scope(
            conn,
            stimulus_id="stim_tv_fixture",
            scope_type="location",
            scope_id=SUITE,
            relation_role="available_in",
        )
        exposure = record_character_exposure(
            conn,
            exposure_id="exposure_tv_fixture",
            stimulus_id="stim_tv_fixture",
            character_id=DARIAN,
            sim_time="2025-05-03T11:02:00+00:00",
            channel="media",
            source_location_id=SUITE,
            attention_hint=0.4,
            metadata={"producer": "test_fixture"},
        )
        assert exposure["status"] == "exposed"
        assert exposure["attention_hint"] == pytest.approx(0.4)
        assert len(recent_character_exposures(conn, DARIAN)) == 1

        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == event_count
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == memory_count
        assert conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0] == mental_cycle_count


def test_source_provenance_and_payload_remain_world_side(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        stimulus = create_world_stimulus(
            conn,
            stimulus_id="stim_money_notice_fixture",
            stimulus_type="financial",
            channel="device",
            subject="Account notice",
            start_sim_time="2025-05-03T12:00:00+00:00",
            payload={"kind": "balance_notice", "amount": 125.50},
            source_type="account_notice",
            source_id="acct_notice_fixture",
            salience=0.6,
            metadata={"authority": "fixture_financial_system"},
        )
        assert stimulus["source_type"] == "account_notice"
        assert stimulus["source_id"] == "acct_notice_fixture"
        assert stimulus["payload"] == {"amount": 125.50, "kind": "balance_notice"}
        assert stimulus["metadata"]["authority"] == "fixture_financial_system"
        assert world_stimulus(conn, "stim_money_notice_fixture")["subject"] == "Account notice"


def test_vocabularies_and_attention_bounds_are_validated(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        with pytest.raises(ValueError, match="unsupported stimulus_type"):
            create_world_stimulus(
                conn,
                stimulus_id="stim_bad_type",
                stimulus_type="mind_control",
                channel="direct",
                subject="bad",
                start_sim_time="2025-05-03T13:00:00+00:00",
            )

        create_world_stimulus(
            conn,
            stimulus_id="stim_validation_fixture",
            stimulus_type="social",
            channel="visual",
            subject="Visible social cue",
            start_sim_time="2025-05-03T13:00:00+00:00",
        )
        with pytest.raises(ValueError, match="unsupported scope_type"):
            add_stimulus_scope(
                conn,
                stimulus_id="stim_validation_fixture",
                scope_type="omniscient",
                scope_id="all",
            )
        with pytest.raises(ValueError, match="attention_hint"):
            record_character_exposure(
                conn,
                exposure_id="exposure_bad_attention",
                stimulus_id="stim_validation_fixture",
                character_id=DARIAN,
                sim_time="2025-05-03T13:01:00+00:00",
                attention_hint=1.5,
            )

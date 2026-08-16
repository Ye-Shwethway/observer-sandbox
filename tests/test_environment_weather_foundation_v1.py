from __future__ import annotations

import pytest

from observer_sandbox.db import SCHEMA_VERSION, connect, migrate
from observer_sandbox.environment_schema import (
    ENVIRONMENT_SCHEMA_VERSION,
    migrate_environment_schema,
)
from observer_sandbox.environment_weather import (
    current_environment_state,
    environment_context_for_location,
    location_is_outdoor,
    publish_environment_stimulus,
    record_environment_state,
    record_outdoor_environment_exposure,
)
from observer_sandbox.runtime import initialize
from observer_sandbox.world import set_field
from observer_sandbox.world_stimulus import eligible_world_stimuli, world_stimulus


ESTATE = "loc_thorne_estate"
CORE_GROUNDS = "loc_thorne_estate_core_grounds"
REAR_FOREST = "loc_thorne_estate_rear_forest"
SUITE = "loc_thorne_estate_master_suite"
DARIAN = "char_darian"
T0 = "2025-05-03T09:00:00+00:00"
T1 = "2025-05-03T09:15:00+00:00"


def _weather(conn, state_id="weather_estate_fixture", **overrides):
    values = {
        "state_id": state_id,
        "scope_location_id": ESTATE,
        "condition": "rain",
        "temperature_c": 7.5,
        "precipitation_kind": "rain",
        "precipitation_intensity": 0.7,
        "wind_speed_mps": 5.0,
        "visibility_km": 8.0,
        "cloud_cover": 0.9,
        "daylight_state": "day",
        "light_level": 0.45,
        "valid_from_sim_time": T0,
        "source_type": "test_fixture",
        "source_id": state_id,
    }
    values.update(overrides)
    return record_environment_state(conn, **values)


def test_environment_schema_v1_is_idempotent_and_fresh_runtime_invents_no_weather(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        migrate_environment_schema(conn)
        migrate_environment_schema(conn)
        migrate(conn)
        assert SCHEMA_VERSION >= 10
        assert conn.execute(
            "SELECT value FROM schema_meta WHERE key='schema_version'"
        ).fetchone()[0] == str(SCHEMA_VERSION)
        assert int(conn.execute(
            "SELECT value FROM schema_meta WHERE key='environment_schema_version'"
        ).fetchone()[0]) == ENVIRONMENT_SCHEMA_VERSION
        assert ENVIRONMENT_SCHEMA_VERSION >= 1
        assert conn.execute("SELECT COUNT(*) FROM environment_states").fetchone()[0] == 0
        assert current_environment_state(conn, location_id=CORE_GROUNDS, sim_time=T1) is None


def test_estate_weather_resolves_through_containment_and_specific_override_wins(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _weather(conn)
        core = current_environment_state(conn, location_id=CORE_GROUNDS, sim_time=T1)
        assert core is not None
        assert core["state_id"] == "weather_estate_fixture"

        _weather(
            conn,
            state_id="weather_rear_forest_fixture",
            scope_location_id=REAR_FOREST,
            condition="fog",
            precipitation_kind="none",
            precipitation_intensity=0.0,
            visibility_km=0.8,
            cloud_cover=1.0,
        )
        forest = current_environment_state(conn, location_id=REAR_FOREST, sim_time=T1)
        assert forest is not None
        assert forest["state_id"] == "weather_rear_forest_fixture"
        assert forest["condition"] == "fog"
        assert current_environment_state(conn, location_id=CORE_GROUNDS, sim_time=T1)[
            "state_id"
        ] == "weather_estate_fixture"


def test_environment_stimulus_scopes_only_explicit_outdoor_descendants(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _weather(conn)
        stimulus = publish_environment_stimulus(conn, "weather_estate_fixture", salience=0.8)
        assert stimulus is not None
        assert stimulus["stimulus_type"] == "environment"
        assert stimulus["channel"] == "environmental"
        assert stimulus["source_type"] == "environment_state"
        scopes = {
            item["scope_id"]
            for item in stimulus["scopes"]
            if item["scope_type"] == "location"
        }
        assert CORE_GROUNDS in scopes
        assert REAR_FOREST in scopes
        assert SUITE not in scopes
        assert all(location_is_outdoor(conn, location_id) for location_id in scopes)

        assert eligible_world_stimuli(
            conn,
            character_id=DARIAN,
            sim_time=T1,
            location_id=SUITE,
        ) == []
        outdoor = eligible_world_stimuli(
            conn,
            character_id=DARIAN,
            sim_time=T1,
            location_id=CORE_GROUNDS,
        )
        assert [row["stimulus_id"] for row in outdoor] == [
            "environment:weather_estate_fixture"
        ]


def test_direct_weather_exposure_requires_outdoor_location_and_preserves_mind_memory_authority(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _weather(conn)
        publish_environment_stimulus(conn, "weather_estate_fixture")
        event_count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        memory_count = conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0]
        mental_count = conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0]

        assert record_outdoor_environment_exposure(
            conn,
            character_id=DARIAN,
            sim_time=T1,
            location_id=SUITE,
        ) is None
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == 0

        exposure = record_outdoor_environment_exposure(
            conn,
            character_id=DARIAN,
            sim_time=T1,
            location_id=CORE_GROUNDS,
            exposure_id="exp_weather_fixture",
        )
        assert exposure is not None
        assert exposure["stimulus_id"] == "environment:weather_estate_fixture"
        assert exposure["source_location_id"] == CORE_GROUNDS
        assert exposure["metadata"]["environment_state_id"] == "weather_estate_fixture"
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == event_count
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == memory_count
        assert conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0] == mental_count


def test_second_character_uses_same_outdoor_exposure_path_without_identity_logic(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        second = "char_environment_fixture"
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
            (second, "character", "Environment Fixture", "{}", "[]"),
        )
        set_field(conn, second, "runtime.location", REAR_FOREST)
        conn.commit()
        _weather(conn)
        publish_environment_stimulus(conn, "weather_estate_fixture")
        exposure = record_outdoor_environment_exposure(
            conn,
            character_id=second,
            sim_time=T1,
            exposure_id="exp_environment_second_fixture",
        )
        assert exposure is not None
        assert exposure["character_id"] == second
        assert exposure["source_location_id"] == REAR_FOREST


def test_new_same_scope_state_supersedes_previous_state_and_retires_old_stimulus(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _weather(conn, state_id="weather_old")
        publish_environment_stimulus(conn, "weather_old")
        _weather(
            conn,
            state_id="weather_new",
            condition="clear",
            precipitation_kind="none",
            precipitation_intensity=0.0,
            cloud_cover=0.1,
            valid_from_sim_time="2025-05-03T10:00:00+00:00",
        )
        old = conn.execute(
            "SELECT status FROM environment_states WHERE state_id='weather_old'"
        ).fetchone()[0]
        assert old == "superseded"
        assert world_stimulus(conn, "environment:weather_old")["status"] == "retired"
        current = current_environment_state(
            conn, location_id=CORE_GROUNDS, sim_time="2025-05-03T10:05:00+00:00"
        )
        assert current is not None
        assert current["state_id"] == "weather_new"


def test_environment_validation_and_context_are_bounded(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        with pytest.raises(ValueError, match="unsupported condition"):
            _weather(conn, condition="psychic_storm")
        with pytest.raises(ValueError, match="precipitation_intensity"):
            _weather(conn, state_id="bad_intensity", precipitation_intensity=1.5)
        with pytest.raises(ValueError, match="wind_speed_mps"):
            _weather(conn, state_id="bad_wind", wind_speed_mps=-1)

        _weather(conn)
        context = environment_context_for_location(
            conn, location_id=CORE_GROUNDS, sim_time=T1
        )
        assert context["direct_ambient_exposure"] is True
        assert context["environment_state_id"] == "weather_estate_fixture"
        assert context["environment_state"]["condition"] == "rain"
        indoor = environment_context_for_location(conn, location_id=SUITE, sim_time=T1)
        assert indoor["direct_ambient_exposure"] is False
        assert indoor["environment_state_id"] == "weather_estate_fixture"

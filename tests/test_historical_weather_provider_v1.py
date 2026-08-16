from __future__ import annotations

import json
import urllib.parse

import pytest

from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.environment_schema import ENVIRONMENT_SCHEMA_VERSION, migrate_environment_schema
from observer_sandbox.environment_weather import current_environment_state
from observer_sandbox.historical_weather_provider import (
    build_provider_url,
    deterministic_fallback_hour,
    ensure_weather_for_sim_time,
    load_weather_provider_config,
    normalize_provider_hour,
)
from observer_sandbox.runtime import initialize


SIM_HOUR = "2025-05-01T07:23:00+00:00"
ESTATE = "loc_thorne_estate"
OUTDOOR = "loc_thorne_estate_mansion_exterior"
INDOOR = "loc_thorne_estate_master_suite"


def _provider():
    return load_weather_provider_config()["providers"][0]


def _response() -> dict:
    return {
        "latitude": 38.94,
        "longitude": -119.98,
        "timezone": "GMT",
        "hourly": {
            "time": ["2025-05-01T07:00", "2025-05-01T08:00"],
            "temperature_2m": [2.5, 4.0],
            "precipitation": [1.8, 0.0],
            "rain": [1.8, 0.0],
            "snowfall": [0.0, 0.0],
            "weather_code": [61, 1],
            "cloud_cover": [90, 25],
            "visibility": [8000, 22000],
            "wind_speed_10m": [18.0, 7.2],
            "is_day": [0, 1],
        },
    }


def test_provider_schema_and_config_are_versioned_without_exact_estate_geocode(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        migrate_environment_schema(conn)
        migrate_environment_schema(conn)
        schema = int(conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0])
        env_schema = int(conn.execute("SELECT value FROM schema_meta WHERE key='environment_schema_version'").fetchone()[0])
        assert schema == SCHEMA_VERSION
        assert env_schema == ENVIRONMENT_SCHEMA_VERSION == 2
        assert conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weather_provider_cache'").fetchone()

    provider = _provider()
    anchor = provider["geographic_anchor"]
    assert provider["mode"] == "historical_reanalysis"
    assert provider["timezone"] == "GMT"
    assert provider["scope_location_id"] == ESTATE
    assert anchor["coordinate_status"] == "city_area_sampling_anchor_not_exact_estate_coordinate"


def test_provider_url_is_driven_by_simulation_date_not_wall_clock():
    provider = _provider()
    url = build_provider_url(provider, "2025-05-01")
    query = urllib.parse.parse_qs(urllib.parse.urlparse(url).query)
    assert query["start_date"] == ["2025-05-01"]
    assert query["end_date"] == ["2025-05-01"]
    assert query["timezone"] == ["GMT"]
    assert "temperature_2m" in query["hourly"][0]
    assert "weather_code" in query["hourly"][0]


def test_provider_hour_normalizes_into_w1_contract():
    record = normalize_provider_hour(_response(), provider=_provider(), sim_time=SIM_HOUR)
    assert record["valid_from_sim_time"] == "2025-05-01T07:00:00+00:00"
    assert record["condition"] == "rain"
    assert record["temperature_c"] == pytest.approx(2.5)
    assert record["precipitation_kind"] == "rain"
    assert record["precipitation_intensity"] == pytest.approx(0.18)
    assert record["wind_speed_mps"] == pytest.approx(5.0)
    assert record["visibility_km"] == pytest.approx(8.0)
    assert record["cloud_cover"] == pytest.approx(0.9)
    assert record["daylight_state"] == "night"
    assert record["metadata"]["synthetic"] is False
    assert record["source_type"] == "open_meteo_historical_weather"


def test_exact_historical_sync_caches_day_and_publishes_only_outdoor_w0_scopes(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    calls: list[str] = []

    def fetcher(url: str) -> dict:
        calls.append(url)
        return _response()

    with connect(db) as conn:
        first = ensure_weather_for_sim_time(conn, sim_time=SIM_HOUR, fetcher=fetcher)
        second = ensure_weather_for_sim_time(conn, sim_time=SIM_HOUR, fetcher=fetcher)
        assert first["source_type"] == "open_meteo_historical_weather"
        assert first["metadata"]["synthetic"] is False
        assert second["state_id"] == first["state_id"]
        assert len(calls) == 1

        state = current_environment_state(conn, location_id=OUTDOOR, sim_time=SIM_HOUR)
        assert state is not None
        assert state["condition"] == "rain"
        stimuli = conn.execute(
            "SELECT stimulus_id FROM world_stimuli WHERE source_type='environment_state' AND source_id=?",
            (first["state_id"],),
        ).fetchall()
        assert len(stimuli) == 1
        scopes = conn.execute(
            "SELECT scope_type,scope_id FROM world_stimulus_scopes WHERE stimulus_id=? ORDER BY scope_id",
            (stimuli[0]["stimulus_id"],),
        ).fetchall()
        assert [(row["scope_type"], row["scope_id"]) for row in scopes] == [("location", OUTDOOR)]
        assert current_environment_state(conn, location_id=INDOOR, sim_time=SIM_HOUR) is not None


def test_synthetic_fallback_is_deterministic_and_explicit(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    def failing_fetcher(_url: str) -> dict:
        raise RuntimeError("fixture provider failure")

    with connect(db) as conn:
        first = ensure_weather_for_sim_time(conn, sim_time=SIM_HOUR, fetcher=failing_fetcher)
        second = ensure_weather_for_sim_time(conn, sim_time=SIM_HOUR, fetcher=failing_fetcher)
        assert first["source_type"] == "synthetic_weather_fallback"
        assert first["metadata"]["synthetic"] is True
        assert first["metadata"]["fallback_reason"] == "fixture provider failure"
        assert first["metadata"]["provider"] == "open_meteo"
        assert second == first
        assert deterministic_fallback_hour(_provider(), SIM_HOUR) == deterministic_fallback_hour(_provider(), SIM_HOUR)

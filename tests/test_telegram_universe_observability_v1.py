from observer_sandbox.db import connect
from observer_sandbox.environment_weather import record_environment_state
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import set_runtime_value
from observer_sandbox.telegram_universe import (
    _weather_registry,
    locations_view,
    region_view,
    regions_view,
    universe_view,
    weather_view,
)


T0 = "2025-05-03T09:00:00+00:00"
T1 = "2025-05-03T09:15:00+00:00"


def _callbacks(keyboard):
    return [button["callback_data"] for row in keyboard or [] for button in row]


def test_universe_home_splits_weather_regions_and_locations(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        text, keyboard = universe_view(conn)
        callbacks = _callbacks(keyboard)
        assert "🌍 UNIVERSE" in text
        assert "uni:weather" in callbacks
        assert "uni:regions" in callbacks
        assert "uni:locations" in callbacks
        assert "loc:loc_thorne_estate" not in callbacks


def test_weather_registry_links_represented_region_to_provider_without_runtime_region_invention():
    registry = _weather_registry()
    assert len(registry) == 1
    region, provider = registry[0]
    assert region["id"] == "south_lake_tahoe"
    assert region["weather_provider_id"] == provider["id"]
    assert provider["region_id"] == region["id"]
    assert provider["enabled"] is True
    assert provider["scope_location_id"] == "loc_thorne_estate"


def test_locations_section_contains_estate_without_opening_tahoe_traversal(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        text, keyboard = locations_view(conn)
        assert "📍 LOCATIONS" in text
        assert "Thorne Estate" in text
        assert "loc:loc_thorne_estate" in _callbacks(keyboard)
        assert conn.execute("SELECT COUNT(*) FROM entities WHERE id='loc_south_lake_tahoe'").fetchone()[0] == 0


def test_region_context_shows_south_lake_tahoe_then_estate_but_keeps_outward_route_locked(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        regions_text, regions_keyboard = regions_view(conn)
        assert "South Lake Tahoe" in regions_text
        assert "🌤" in regions_text
        assert "region:south_lake_tahoe" in _callbacks(regions_keyboard)

        region_text, region_keyboard = region_view(conn, "south_lake_tahoe")
        assert "SOUTH LAKE TAHOE" in region_text
        assert "Weather           Registered" in region_text
        assert "Thorne Estate" in region_text
        assert "Locked Unimplemented" in region_text
        assert "loc:loc_thorne_estate" in _callbacks(region_keyboard)
        assert "uni:weather" in _callbacks(region_keyboard)
        assert conn.execute("SELECT COUNT(*) FROM relations WHERE source_id='loc_thorne_estate' AND target_id='loc_south_lake_tahoe'").fetchone()[0] == 0


def test_weather_view_reads_registered_region_state_without_creating_mind_or_memory(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_runtime_value(conn, "sim_time", T1)
        conn.commit()
        record_environment_state(
            conn,
            state_id="weather_creator_view_fixture",
            scope_location_id="loc_thorne_estate",
            condition="rain",
            temperature_c=7.5,
            precipitation_kind="rain",
            precipitation_intensity=0.4,
            wind_speed_mps=5.25,
            visibility_km=8.5,
            cloud_cover=0.9,
            daylight_state="day",
            light_level=0.45,
            valid_from_sim_time=T0,
            valid_until_sim_time="2025-05-03T09:59:59+00:00",
            source_type="open_meteo_historical_weather",
            source_id="fixture:historical",
            metadata={"provider_id": "fixture", "synthetic": False},
        )
        memory_before = conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0]
        mind_before = conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0]
        exposure_before = conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0]

        text, keyboard = weather_view(conn)

        assert "🌤 UNIVERSE WEATHER" in text
        assert "Represented regional weather" in text
        assert "🌎 South Lake Tahoe" in text
        assert "South Lake Tahoe, California" in text
        assert "Rain" in text
        assert "7.5 °C" in text
        assert "5.2 m/s" in text
        assert "Historical weather replay" in text
        assert "sampling anchor is regional" in text
        assert "arbitrary Earth lookup remains a future Creator reference utility" in text
        assert "uni:weather" in _callbacks(keyboard)
        assert "uni:regions" in _callbacks(keyboard)
        assert conn.execute("SELECT COUNT(*) FROM character_memories").fetchone()[0] == memory_before
        assert conn.execute("SELECT COUNT(*) FROM mental_cycles").fetchone()[0] == mind_before
        assert conn.execute("SELECT COUNT(*) FROM character_exposures").fetchone()[0] == exposure_before


def test_weather_view_marks_synthetic_fallback_truthfully(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_runtime_value(conn, "sim_time", T1)
        conn.commit()
        record_environment_state(
            conn,
            state_id="weather_creator_fallback_fixture",
            scope_location_id="loc_thorne_estate",
            condition="partly_cloudy",
            temperature_c=9.0,
            precipitation_kind="none",
            precipitation_intensity=0.0,
            wind_speed_mps=2.0,
            visibility_km=20.0,
            cloud_cover=0.4,
            daylight_state="day",
            light_level=0.7,
            valid_from_sim_time=T0,
            valid_until_sim_time="2025-05-03T09:59:59+00:00",
            source_type="deterministic_weather_fallback",
            source_id="fixture:fallback",
            metadata={"provider_id": "fixture", "synthetic": True},
        )
        text, _ = weather_view(conn)
        assert "Synthetic continuity fallback" in text
        assert "not claimed as historical truth" in text

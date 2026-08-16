from observer_sandbox.db import connect
from observer_sandbox.environment_weather import record_environment_state
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_notifications import _notification_weather, format_action_completion


SIM_TIME = "2025-05-03T09:15:00+00:00"


def _state(location: str, location_name: str) -> dict:
    return {
        "actor_id": "char_darian",
        "location": location,
        "location_name": location_name,
        "sim_time": SIM_TIME,
        "energy": 80.0,
        "hunger": 20.0,
        "thirst": 15.0,
        "sleepiness": 10.0,
        "cleanliness": 90.0,
    }


def test_character_update_weather_uses_represented_db_state_for_current_location(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        record_environment_state(
            conn,
            state_id="weather_notification_fixture",
            scope_location_id="loc_thorne_estate",
            condition="snow",
            temperature_c=-1.5,
            precipitation_kind="snow",
            precipitation_intensity=0.6,
            wind_speed_mps=4.0,
            visibility_km=7.0,
            cloud_cover=0.9,
            daylight_state="day",
            light_level=0.4,
            valid_from_sim_time="2025-05-03T09:00:00+00:00",
            valid_until_sim_time="2025-05-03T09:59:59+00:00",
            source_type="test",
            source_id="fixture",
        )
        after = _state("loc_thorne_estate_kitchen", "Kitchen")
        weather = _notification_weather(conn, after)

        assert weather == {"condition": "snow", "temperature_c": -1.5}

        before = dict(after)
        before["energy"] = 75.0
        text = format_action_completion(
            {"action": "eat", "target_name": "Meal Ingredients"},
            before,
            after,
            actor_name="Darian Thorne",
            weather=weather,
        )

        assert "✨ CHARACTER UPDATE" in text
        assert "👤 Darian Thorne\n🌨 Weather · Snow · -1.5 °C\n🎬 Eat → Meal Ingredients" in text
        assert "📍 Kitchen" in text


def test_character_update_omits_weather_line_when_no_valid_db_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        after = _state("loc_thorne_estate_kitchen", "Kitchen")
        weather = _notification_weather(conn, after)
        assert weather is None

        text = format_action_completion(
            {"action": "observe"},
            after,
            after,
            actor_name="Darian Thorne",
            weather=weather,
        )
        assert "Weather ·" not in text

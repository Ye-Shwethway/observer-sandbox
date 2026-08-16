from __future__ import annotations

import sqlite3


ENVIRONMENT_SCHEMA_VERSION = 1

ENVIRONMENT_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS environment_states (
    state_id TEXT PRIMARY KEY,
    scope_location_id TEXT NOT NULL REFERENCES entities(id) ON DELETE CASCADE,
    condition TEXT NOT NULL CHECK(condition IN (
        'clear','partly_cloudy','cloudy','fog','rain','snow','storm','mixed','other'
    )),
    temperature_c REAL NOT NULL,
    precipitation_kind TEXT NOT NULL DEFAULT 'none' CHECK(precipitation_kind IN (
        'none','rain','snow','sleet','mixed','other'
    )),
    precipitation_intensity REAL NOT NULL DEFAULT 0.0
        CHECK(precipitation_intensity >= 0 AND precipitation_intensity <= 1),
    wind_speed_mps REAL NOT NULL DEFAULT 0.0 CHECK(wind_speed_mps >= 0),
    visibility_km REAL NOT NULL DEFAULT 20.0 CHECK(visibility_km >= 0),
    cloud_cover REAL NOT NULL DEFAULT 0.0 CHECK(cloud_cover >= 0 AND cloud_cover <= 1),
    daylight_state TEXT NOT NULL CHECK(daylight_state IN ('day','dawn','dusk','night')),
    light_level REAL NOT NULL CHECK(light_level >= 0 AND light_level <= 1),
    valid_from_sim_time TEXT NOT NULL,
    valid_until_sim_time TEXT,
    status TEXT NOT NULL DEFAULT 'active' CHECK(status IN (
        'active','superseded','expired','retired'
    )),
    source_type TEXT,
    source_id TEXT,
    source_event_id INTEGER REFERENCES events(id) ON DELETE SET NULL,
    metadata_json TEXT NOT NULL DEFAULT '{}',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_environment_states_scope_time
    ON environment_states(scope_location_id, status, valid_from_sim_time DESC);
CREATE INDEX IF NOT EXISTS idx_environment_states_active_window
    ON environment_states(status, valid_from_sim_time, valid_until_sim_time);
"""


def migrate_environment_schema(conn: sqlite3.Connection) -> None:
    """Install the authoritative environment-state schema without inventing weather."""
    conn.executescript(ENVIRONMENT_SCHEMA_SQL)
    conn.execute(
        "INSERT INTO schema_meta(key,value) VALUES('environment_schema_version',?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (str(ENVIRONMENT_SCHEMA_VERSION),),
    )
    conn.commit()

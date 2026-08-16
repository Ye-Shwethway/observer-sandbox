from __future__ import annotations

import json
import sqlite3
from typing import Any
from uuid import uuid4

from .world import get_field
from .world_stimulus import (
    add_stimulus_scope,
    create_world_stimulus,
    record_character_exposure,
    set_stimulus_status,
    world_stimulus,
)


CONDITIONS = {
    "clear",
    "partly_cloudy",
    "cloudy",
    "fog",
    "rain",
    "snow",
    "storm",
    "mixed",
    "other",
}
PRECIPITATION_KINDS = {"none", "rain", "snow", "sleet", "mixed", "other"}
DAYLIGHT_STATES = {"day", "dawn", "dusk", "night"}
ENVIRONMENT_STATUSES = {"active", "superseded", "expired", "retired"}


def _json(value: dict[str, Any] | None) -> str:
    return json.dumps(value or {}, sort_keys=True, separators=(",", ":"))


def _unit(value: float, *, name: str) -> float:
    number = float(value)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")
    return number


def _non_negative(value: float, *, name: str) -> float:
    number = float(value)
    if number < 0:
        raise ValueError(f"{name} must be non-negative")
    return number


def _member(value: str, allowed: set[str], *, name: str) -> str:
    normalized = str(value)
    if normalized not in allowed:
        raise ValueError(f"unsupported {name}: {normalized}")
    return normalized


def _require_location(conn: sqlite3.Connection, location_id: str) -> None:
    row = conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='location'", (location_id,)
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown location: {location_id}")


def _ancestor_chain(conn: sqlite3.Connection, location_id: str) -> list[str]:
    """Return current location then represented containment ancestors, nearest first."""
    _require_location(conn, location_id)
    chain: list[str] = []
    seen: set[str] = set()
    current: str | None = location_id
    while current and current not in seen:
        seen.add(current)
        chain.append(current)
        row = conn.execute(
            """SELECT source_id FROM relations
               WHERE relation_type='contains' AND target_id=?
               ORDER BY source_id LIMIT 1""",
            (current,),
        ).fetchone()
        if row is None:
            break
        parent = str(row["source_id"])
        parent_kind = conn.execute("SELECT entity_type FROM entities WHERE id=?", (parent,)).fetchone()
        if parent_kind is None:
            break
        current = parent if str(parent_kind["entity_type"]) == "location" else None
    return chain


def _descendant_locations(conn: sqlite3.Connection, root_location_id: str) -> list[str]:
    _require_location(conn, root_location_id)
    ordered: list[str] = []
    queue = [root_location_id]
    seen: set[str] = set()
    while queue:
        current = queue.pop(0)
        if current in seen:
            continue
        seen.add(current)
        ordered.append(current)
        rows = conn.execute(
            """SELECT r.target_id
               FROM relations r
               JOIN entities e ON e.id=r.target_id
               WHERE r.source_id=? AND r.relation_type='contains' AND e.entity_type='location'
               ORDER BY r.target_id""",
            (current,),
        ).fetchall()
        queue.extend(str(row["target_id"]) for row in rows)
    return ordered


def location_is_outdoor(conn: sqlite3.Connection, location_id: str) -> bool:
    spatial = get_field(conn, location_id, "world.spatial_container", {})
    return isinstance(spatial, dict) and spatial.get("exposure") == "outdoor"


def environment_state(conn: sqlite3.Connection, state_id: str) -> dict[str, Any]:
    row = conn.execute("SELECT * FROM environment_states WHERE state_id=?", (state_id,)).fetchone()
    if row is None:
        raise ValueError(f"unknown environment state: {state_id}")
    result = dict(row)
    result["metadata"] = json.loads(result.pop("metadata_json"))
    return result


def record_environment_state(
    conn: sqlite3.Connection,
    *,
    state_id: str,
    scope_location_id: str,
    condition: str,
    temperature_c: float,
    daylight_state: str,
    light_level: float,
    valid_from_sim_time: str,
    precipitation_kind: str = "none",
    precipitation_intensity: float = 0.0,
    wind_speed_mps: float = 0.0,
    visibility_km: float = 20.0,
    cloud_cover: float = 0.0,
    valid_until_sim_time: str | None = None,
    source_type: str | None = None,
    source_id: str | None = None,
    source_event_id: int | None = None,
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Record authoritative represented environment truth; do not expose characters."""
    if not str(state_id).strip():
        raise ValueError("state_id is required")
    _require_location(conn, scope_location_id)
    condition = _member(condition, CONDITIONS, name="condition")
    precipitation_kind = _member(
        precipitation_kind, PRECIPITATION_KINDS, name="precipitation_kind"
    )
    daylight_state = _member(daylight_state, DAYLIGHT_STATES, name="daylight_state")
    precipitation_intensity = _unit(
        precipitation_intensity, name="precipitation_intensity"
    )
    cloud_cover = _unit(cloud_cover, name="cloud_cover")
    light_level = _unit(light_level, name="light_level")
    wind_speed_mps = _non_negative(wind_speed_mps, name="wind_speed_mps")
    visibility_km = _non_negative(visibility_km, name="visibility_km")

    overlapping = conn.execute(
        """SELECT state_id FROM environment_states
           WHERE scope_location_id=? AND status='active'
             AND valid_from_sim_time<=?
             AND (valid_until_sim_time IS NULL OR valid_until_sim_time>=?)""",
        (scope_location_id, valid_from_sim_time, valid_from_sim_time),
    ).fetchall()
    for row in overlapping:
        old_id = str(row["state_id"])
        conn.execute(
            "UPDATE environment_states SET status='superseded',updated_at=CURRENT_TIMESTAMP WHERE state_id=?",
            (old_id,),
        )
        stimulus_id = f"environment:{old_id}"
        if conn.execute(
            "SELECT 1 FROM world_stimuli WHERE stimulus_id=? AND status='active'", (stimulus_id,)
        ).fetchone() is not None:
            set_stimulus_status(conn, stimulus_id, "retired")

    conn.execute(
        """
        INSERT INTO environment_states(
            state_id,scope_location_id,condition,temperature_c,precipitation_kind,
            precipitation_intensity,wind_speed_mps,visibility_km,cloud_cover,
            daylight_state,light_level,valid_from_sim_time,valid_until_sim_time,status,
            source_type,source_id,source_event_id,metadata_json
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,'active',?,?,?,?)
        """,
        (
            state_id,
            scope_location_id,
            condition,
            float(temperature_c),
            precipitation_kind,
            precipitation_intensity,
            wind_speed_mps,
            visibility_km,
            cloud_cover,
            daylight_state,
            light_level,
            valid_from_sim_time,
            valid_until_sim_time,
            source_type,
            source_id,
            source_event_id,
            _json(metadata),
        ),
    )
    conn.commit()
    return environment_state(conn, state_id)


def current_environment_state(
    conn: sqlite3.Connection, *, location_id: str, sim_time: str
) -> dict[str, Any] | None:
    """Resolve the most-specific active state through represented containment."""
    for scope_location_id in _ancestor_chain(conn, location_id):
        row = conn.execute(
            """SELECT state_id FROM environment_states
               WHERE scope_location_id=? AND status='active'
                 AND valid_from_sim_time<=?
                 AND (valid_until_sim_time IS NULL OR valid_until_sim_time>=?)
               ORDER BY valid_from_sim_time DESC,created_at DESC,state_id DESC
               LIMIT 1""",
            (scope_location_id, sim_time, sim_time),
        ).fetchone()
        if row is not None:
            return environment_state(conn, str(row["state_id"]))
    return None


def environment_payload(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "condition": state["condition"],
        "temperature_c": state["temperature_c"],
        "precipitation_kind": state["precipitation_kind"],
        "precipitation_intensity": state["precipitation_intensity"],
        "wind_speed_mps": state["wind_speed_mps"],
        "visibility_km": state["visibility_km"],
        "cloud_cover": state["cloud_cover"],
        "daylight_state": state["daylight_state"],
        "light_level": state["light_level"],
        "valid_from_sim_time": state["valid_from_sim_time"],
        "valid_until_sim_time": state["valid_until_sim_time"],
    }


def publish_environment_stimulus(
    conn: sqlite3.Connection,
    state_id: str,
    *,
    salience: float = 0.5,
) -> dict[str, Any] | None:
    """Publish direct ambient weather through W0 for represented outdoor descendants."""
    state = environment_state(conn, state_id)
    if state["status"] != "active":
        raise ValueError("only active environment states can be published")

    outdoor_locations = [
        location_id
        for location_id in _descendant_locations(conn, str(state["scope_location_id"]))
        if location_is_outdoor(conn, location_id)
    ]
    if not outdoor_locations:
        return None

    stimulus_id = f"environment:{state_id}"
    existing = conn.execute(
        "SELECT 1 FROM world_stimuli WHERE stimulus_id=?", (stimulus_id,)
    ).fetchone()
    if existing is None:
        create_world_stimulus(
            conn,
            stimulus_id=stimulus_id,
            stimulus_type="environment",
            channel="environmental",
            subject=f"Ambient environment: {state['condition']}",
            start_sim_time=str(state["valid_from_sim_time"]),
            end_sim_time=state["valid_until_sim_time"],
            payload=environment_payload(state),
            source_type="environment_state",
            source_id=state_id,
            salience=salience,
            metadata={"producer": "environment_weather_v1"},
        )
    for location_id in outdoor_locations:
        add_stimulus_scope(
            conn,
            stimulus_id=stimulus_id,
            scope_type="location",
            scope_id=location_id,
            relation_role="direct_ambient_environment",
        )
    return world_stimulus(conn, stimulus_id)


def record_outdoor_environment_exposure(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    sim_time: str,
    location_id: str | None = None,
    exposure_id: str | None = None,
) -> dict[str, Any] | None:
    """Record direct ambient exposure only at an explicitly outdoor represented location."""
    if conn.execute(
        "SELECT 1 FROM entities WHERE id=? AND entity_type='character'", (character_id,)
    ).fetchone() is None:
        raise ValueError(f"unknown character: {character_id}")
    current_location = location_id or get_field(conn, character_id, "runtime.location", None)
    if not current_location:
        return None
    if not location_is_outdoor(conn, str(current_location)):
        return None
    state = current_environment_state(
        conn, location_id=str(current_location), sim_time=sim_time
    )
    if state is None:
        return None
    stimulus_id = f"environment:{state['state_id']}"
    stimulus_row = conn.execute(
        """SELECT 1 FROM world_stimuli s
           JOIN world_stimulus_scopes sc ON sc.stimulus_id=s.stimulus_id
           WHERE s.stimulus_id=? AND s.status='active'
             AND s.start_sim_time<=?
             AND (s.end_sim_time IS NULL OR s.end_sim_time>=?)
             AND sc.scope_type='location' AND sc.scope_id=?""",
        (stimulus_id, sim_time, sim_time, current_location),
    ).fetchone()
    if stimulus_row is None:
        return None
    return record_character_exposure(
        conn,
        exposure_id=exposure_id or f"exp_env_{uuid4().hex}",
        stimulus_id=stimulus_id,
        character_id=character_id,
        sim_time=sim_time,
        channel="environmental",
        source_location_id=str(current_location),
        metadata={
            "producer": "environment_weather_v1",
            "environment_state_id": state["state_id"],
            "direct_ambient": True,
        },
    )


def environment_context_for_location(
    conn: sqlite3.Connection, *, location_id: str, sim_time: str
) -> dict[str, Any]:
    state = current_environment_state(conn, location_id=location_id, sim_time=sim_time)
    return {
        "location_id": location_id,
        "direct_ambient_exposure": location_is_outdoor(conn, location_id),
        "environment_state": None if state is None else environment_payload(state),
        "environment_state_id": None if state is None else state["state_id"],
    }

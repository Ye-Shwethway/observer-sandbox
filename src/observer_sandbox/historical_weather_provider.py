from __future__ import annotations

import hashlib
import json
import math
import sqlite3
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

from .environment_weather import (
    current_environment_state,
    publish_environment_stimulus,
    record_environment_state,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
PROVIDER_CONFIG_PATH = REPO_ROOT / "config" / "environment" / "weather.providers.v1.json"
HTTP_TIMEOUT_SECONDS = 12.0

FetchJson = Callable[[str, float], dict[str, Any]]


def load_weather_provider_config(path: str | Path = PROVIDER_CONFIG_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _provider(config: dict[str, Any] | None = None) -> dict[str, Any]:
    root = config or load_weather_provider_config()
    providers = root.get("providers") or []
    if not providers:
        raise ValueError("weather provider configuration has no providers")
    return dict(providers[0])


def _parse_sim_time(sim_time: str) -> datetime:
    value = datetime.fromisoformat(str(sim_time).replace("Z", "+00:00"))
    if value.tzinfo is None:
        raise ValueError("simulation time must be timezone-aware")
    return value.astimezone(timezone.utc)


def _hour_start(sim_time: str) -> datetime:
    value = _parse_sim_time(sim_time)
    return value.replace(minute=0, second=0, microsecond=0)


def _hour_end(start: datetime) -> datetime:
    return start + timedelta(hours=1) - timedelta(microseconds=1)


def _http_fetch_json(url: str, timeout: float) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "observer-sandbox-historical-weather/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("weather provider returned non-object JSON")
    return payload


def build_provider_url(provider: dict[str, Any], date_text: str) -> str:
    anchor = provider["geographic_anchor"]
    params = {
        "latitude": anchor["latitude"],
        "longitude": anchor["longitude"],
        "start_date": date_text,
        "end_date": date_text,
        "hourly": ",".join(provider["hourly"]),
        "timezone": provider.get("timezone", "GMT"),
    }
    return f"{provider['endpoint']}?{urllib.parse.urlencode(params)}"


def _cache_row(conn: sqlite3.Connection, provider_id: str, cache_date: str) -> sqlite3.Row | None:
    return conn.execute(
        "SELECT * FROM weather_provider_cache WHERE provider_id=? AND cache_date=?",
        (provider_id, cache_date),
    ).fetchone()


def _store_cache_success(
    conn: sqlite3.Connection,
    *,
    provider_id: str,
    cache_date: str,
    response: dict[str, Any],
) -> None:
    conn.execute(
        """
        INSERT INTO weather_provider_cache(provider_id,cache_date,status,response_json,error_text,fetched_at)
        VALUES(?,?, 'ok', ?, NULL, CURRENT_TIMESTAMP)
        ON CONFLICT(provider_id,cache_date) DO UPDATE SET
            status='ok',response_json=excluded.response_json,error_text=NULL,fetched_at=CURRENT_TIMESTAMP
        """,
        (provider_id, cache_date, json.dumps(response, sort_keys=True, separators=(",", ":"))),
    )
    conn.commit()


def _store_cache_error(
    conn: sqlite3.Connection,
    *,
    provider_id: str,
    cache_date: str,
    error: Exception,
) -> None:
    conn.execute(
        """
        INSERT INTO weather_provider_cache(provider_id,cache_date,status,response_json,error_text,fetched_at)
        VALUES(?,?, 'error', NULL, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(provider_id,cache_date) DO UPDATE SET
            status='error',response_json=NULL,error_text=excluded.error_text,fetched_at=CURRENT_TIMESTAMP
        """,
        (provider_id, cache_date, f"{type(error).__name__}: {error}"[:1000]),
    )
    conn.commit()


def _error_cache_in_cooldown(row: sqlite3.Row, retry_minutes: int) -> bool:
    if row["status"] != "error":
        return False
    fetched_at = datetime.fromisoformat(str(row["fetched_at"]).replace(" ", "T")).replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc) - fetched_at < timedelta(minutes=max(1, retry_minutes))


def provider_day(
    conn: sqlite3.Connection,
    *,
    provider: dict[str, Any],
    date_text: str,
    fetch_json: FetchJson | None = None,
) -> dict[str, Any]:
    provider_id = str(provider["id"])
    row = _cache_row(conn, provider_id, date_text)
    if row is not None and row["status"] == "ok" and row["response_json"]:
        return json.loads(row["response_json"])
    retry_minutes = int(provider.get("error_retry_minutes", 15))
    if row is not None and _error_cache_in_cooldown(row, retry_minutes):
        raise RuntimeError(f"weather provider retry cooldown active for {date_text}")

    url = build_provider_url(provider, date_text)
    fetcher = fetch_json or _http_fetch_json
    try:
        response = fetcher(url, HTTP_TIMEOUT_SECONDS)
        hourly = response.get("hourly")
        if not isinstance(hourly, dict) or not isinstance(hourly.get("time"), list):
            raise ValueError("weather provider response missing hourly time series")
        _store_cache_success(conn, provider_id=provider_id, cache_date=date_text, response=response)
        return response
    except Exception as exc:
        _store_cache_error(conn, provider_id=provider_id, cache_date=date_text, error=exc)
        raise


def _wmo_condition(code: int) -> str:
    if code == 0:
        return "clear"
    if code in {1, 2}:
        return "partly_cloudy"
    if code == 3:
        return "cloudy"
    if code in {45, 48}:
        return "fog"
    if code in {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}:
        return "rain"
    if code in {71, 73, 75, 77, 85, 86}:
        return "snow"
    if code in {95, 96, 99}:
        return "storm"
    return "other"


def _precipitation_kind(*, precipitation: float, rain: float, snowfall: float) -> str:
    if precipitation <= 0 and rain <= 0 and snowfall <= 0:
        return "none"
    if rain > 0 and snowfall > 0:
        return "mixed"
    if snowfall > 0:
        return "snow"
    if rain > 0 or precipitation > 0:
        return "rain"
    return "other"


def _bounded(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _hourly_value(hourly: dict[str, Any], key: str, index: int, default: float = 0.0) -> float:
    values = hourly.get(key)
    if not isinstance(values, list) or index >= len(values) or values[index] is None:
        return float(default)
    return float(values[index])


def normalize_provider_hour(
    response: dict[str, Any],
    *,
    provider: dict[str, Any],
    sim_time: str,
) -> dict[str, Any]:
    start = _hour_start(sim_time)
    target = start.strftime("%Y-%m-%dT%H:00")
    hourly = response["hourly"]
    times = hourly["time"]
    try:
        index = times.index(target)
    except ValueError as exc:
        raise ValueError(f"provider response does not contain requested hour {target}") from exc

    precipitation = _hourly_value(hourly, "precipitation", index)
    rain = _hourly_value(hourly, "rain", index)
    snowfall = _hourly_value(hourly, "snowfall", index)
    cloud_cover = _bounded(_hourly_value(hourly, "cloud_cover", index) / 100.0)
    is_day = int(round(_hourly_value(hourly, "is_day", index, 1.0))) == 1
    weather_code = int(round(_hourly_value(hourly, "weather_code", index)))
    visibility_m = _hourly_value(hourly, "visibility", index, 20000.0)
    wind_kmh = _hourly_value(hourly, "wind_speed_10m", index)

    if is_day:
        daylight_state = "day"
        light_level = _bounded(0.95 - 0.5 * cloud_cover)
    else:
        daylight_state = "night"
        light_level = _bounded(0.12 - 0.08 * cloud_cover)

    return {
        "state_id": f"env_{provider['id']}_{start.strftime('%Y%m%dT%H00Z')}",
        "scope_location_id": provider["scope_location_id"],
        "condition": _wmo_condition(weather_code),
        "temperature_c": _hourly_value(hourly, "temperature_2m", index),
        "precipitation_kind": _precipitation_kind(
            precipitation=precipitation,
            rain=rain,
            snowfall=snowfall,
        ),
        "precipitation_intensity": _bounded(precipitation / 10.0),
        "wind_speed_mps": max(0.0, wind_kmh / 3.6),
        "visibility_km": max(0.0, visibility_m / 1000.0),
        "cloud_cover": cloud_cover,
        "daylight_state": daylight_state,
        "light_level": light_level,
        "valid_from_sim_time": start.isoformat(),
        "valid_until_sim_time": _hour_end(start).isoformat(),
        "source_type": "open_meteo_historical_weather",
        "source_id": f"{provider['id']}:{target}",
        "metadata": {
            "provider_id": provider["id"],
            "provider": provider["provider"],
            "mode": provider["mode"],
            "weather_code": weather_code,
            "raw_precipitation_mm": precipitation,
            "raw_rain_mm": rain,
            "raw_snowfall": snowfall,
            "geographic_anchor": provider["geographic_anchor"],
            "synthetic": False,
        },
    }


def _seasonal_baseline_temperature(month: int) -> float:
    # Coarse high-elevation temperate fallback calibration only; not historical truth.
    values = {1: -1.0, 2: 0.0, 3: 2.5, 4: 5.0, 5: 9.0, 6: 14.0, 7: 18.0, 8: 17.0, 9: 13.0, 10: 7.5, 11: 2.5, 12: -0.5}
    return values[month]


def deterministic_fallback_hour(provider: dict[str, Any], sim_time: str) -> dict[str, Any]:
    start = _hour_start(sim_time)
    seed_text = f"{provider['id']}|{provider['geographic_anchor']['latitude']}|{provider['geographic_anchor']['longitude']}|{start.isoformat()}"
    digest = hashlib.sha256(seed_text.encode("utf-8")).digest()
    u1 = int.from_bytes(digest[:8], "big") / float(2**64 - 1)
    u2 = int.from_bytes(digest[8:16], "big") / float(2**64 - 1)
    u3 = int.from_bytes(digest[16:24], "big") / float(2**64 - 1)

    localish_hour = (start.hour - 8) % 24
    diurnal = 5.0 * math.sin((localish_hour - 7) / 24.0 * math.tau)
    temperature_c = _seasonal_baseline_temperature(start.month) + diurnal + (u1 - 0.5) * 4.0

    wet_season = start.month in {11, 12, 1, 2, 3, 4}
    precip_threshold = 0.24 if wet_season else 0.10
    precipitating = u2 < precip_threshold
    snow = precipitating and temperature_c <= 1.5
    storm = precipitating and u3 > 0.93
    cloud_cover = _bounded(0.35 + (0.5 if precipitating else 0.0) + (u3 - 0.5) * 0.3)
    daylight = 7 <= localish_hour < 19

    if storm:
        condition = "storm"
    elif snow:
        condition = "snow"
    elif precipitating:
        condition = "rain"
    elif cloud_cover > 0.75:
        condition = "cloudy"
    elif cloud_cover > 0.35:
        condition = "partly_cloudy"
    else:
        condition = "clear"

    precipitation_intensity = 0.0 if not precipitating else _bounded(0.15 + u1 * 0.55)
    return {
        "state_id": f"env_fallback_{provider['id']}_{start.strftime('%Y%m%dT%H00Z')}",
        "scope_location_id": provider["scope_location_id"],
        "condition": condition,
        "temperature_c": round(temperature_c, 2),
        "precipitation_kind": "snow" if snow else ("rain" if precipitating else "none"),
        "precipitation_intensity": precipitation_intensity,
        "wind_speed_mps": round(0.8 + u3 * 6.5, 2),
        "visibility_km": round(max(1.0, 25.0 - precipitation_intensity * 18.0), 2),
        "cloud_cover": cloud_cover,
        "daylight_state": "day" if daylight else "night",
        "light_level": _bounded((0.9 - 0.5 * cloud_cover) if daylight else (0.1 - 0.06 * cloud_cover)),
        "valid_from_sim_time": start.isoformat(),
        "valid_until_sim_time": _hour_end(start).isoformat(),
        "source_type": "deterministic_weather_fallback",
        "source_id": f"{provider['id']}:{start.strftime('%Y-%m-%dT%H:00Z')}:fallback",
        "metadata": {
            "provider_id": provider["id"],
            "fallback_mode": provider.get("fallback", {}).get("mode", "deterministic_seasonal_continuity"),
            "geographic_anchor": provider["geographic_anchor"],
            "synthetic": True,
        },
    }


def _record_normalized_state(conn: sqlite3.Connection, record: dict[str, Any]) -> dict[str, Any]:
    existing = conn.execute(
        "SELECT state_id FROM environment_states WHERE state_id=?",
        (record["state_id"],),
    ).fetchone()
    if existing is None:
        state = record_environment_state(conn, **record)
    else:
        state = dict(conn.execute("SELECT * FROM environment_states WHERE state_id=?", (record["state_id"],)).fetchone())
    publish_environment_stimulus(conn, str(record["state_id"]))
    return state


def ensure_weather_for_sim_time(
    conn: sqlite3.Connection,
    *,
    sim_time: str,
    config: dict[str, Any] | None = None,
    fetch_json: FetchJson | None = None,
) -> dict[str, Any] | None:
    provider = _provider(config)
    start = _hour_start(sim_time)

    current = current_environment_state(
        conn,
        location_id=str(provider["scope_location_id"]),
        sim_time=start.isoformat(),
    )
    if current is not None:
        metadata = current.get("metadata", {})
        if current.get("source_type") == "open_meteo_historical_weather" or metadata.get("provider_id") == provider["id"]:
            return current

    date_text = start.date().isoformat()
    try:
        response = provider_day(
            conn,
            provider=provider,
            date_text=date_text,
            fetch_json=fetch_json,
        )
        record = normalize_provider_hour(response, provider=provider, sim_time=start.isoformat())
    except Exception:
        fallback = provider.get("fallback", {})
        if not fallback.get("enabled", False):
            return None
        record = deterministic_fallback_hour(provider, start.isoformat())

    return _record_normalized_state(conn, record)

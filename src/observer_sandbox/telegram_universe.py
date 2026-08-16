from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from .environment_weather import current_environment_state
from .historical_weather_provider import load_weather_provider_config
from .observer_query import list_locations, list_worlds
from .simulation import runtime_value


REPO_ROOT = Path(__file__).resolve().parents[2]
GEOGRAPHY_CONFIG_PATH = REPO_ROOT / "config" / "worlds" / "geography.observer.v1.json"


def _fmt_time(value: str | None) -> str:
    if not value:
        return "Unknown"
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return dt.strftime("%d-%m-%Y (%A) %I:%M %p")
    except (TypeError, ValueError):
        return str(value)


def _fmt_number(value: Any, digits: int = 1) -> str:
    try:
        return f"{float(value):.{digits}f}"
    except (TypeError, ValueError):
        return "Unknown"


def _condition_label(value: str | None) -> str:
    return str(value or "unknown").replace("_", " ").title()


def _condition_icon(value: str | None) -> str:
    return {
        "clear": "☀️",
        "partly_cloudy": "🌤",
        "cloudy": "☁️",
        "fog": "🌫",
        "rain": "🌧",
        "snow": "🌨",
        "storm": "⛈",
        "mixed": "🌦",
    }.get(str(value or ""), "🌤")


def load_observer_geography(path: str | Path = GEOGRAPHY_CONFIG_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _weather_registry() -> list[tuple[dict[str, Any], dict[str, Any]]]:
    """Return represented regions paired with their configured weather provider."""
    geography = load_observer_geography()
    provider_root = load_weather_provider_config()
    providers = {
        str(provider.get("id")): provider
        for provider in provider_root.get("providers") or []
        if provider.get("enabled", True)
    }
    registered: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for region in geography.get("regions") or []:
        provider_id = str(region.get("weather_provider_id") or "")
        provider = providers.get(provider_id)
        if provider is None:
            continue
        # Bidirectional ids prevent accidental cross-region wiring as the world grows.
        configured_region = str(provider.get("region_id") or region.get("id") or "")
        if configured_region != str(region.get("id") or ""):
            continue
        registered.append((region, provider))
    return registered


def universe_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    worlds = list_worlds(conn)
    world_names = ", ".join(world["name"] for world in worlds) or "No represented worlds"
    lines = [
        "🌍 UNIVERSE",
        "━━━━━━━━━━━━━━━━━━",
        world_names,
        "",
        "Observe the world by domain:",
    ]
    keyboard = [
        [
            {"text": "🌤 Weather", "callback_data": "uni:weather"},
            {"text": "🌎 Regions", "callback_data": "uni:regions"},
        ],
        [{"text": "📍 Locations", "callback_data": "uni:locations"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]
    return "\n".join(lines), keyboard


def weather_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    """Render represented regional weather from DB only; never fetch on button press."""
    sim_time = runtime_value(conn, "sim_time", None)
    registry = _weather_registry()
    lines = [
        "🌤 UNIVERSE WEATHER",
        "━━━━━━━━━━━━━━━━━━",
        f"🕒 {_fmt_time(sim_time)}",
        "",
        "Represented regional weather:",
    ]

    if not registry:
        lines.extend([
            "• No represented regions have a weather provider registered.",
            "",
            "Weather registration is geography-driven; this screen is read-only.",
        ])

    for region, provider in registry:
        region_name = str(region.get("name") or region.get("id") or "Region")
        location_id = str(provider.get("scope_location_id") or "")
        anchor = provider.get("geographic_anchor") or {}
        anchor_name = str(anchor.get("label") or region_name)
        state = None
        if sim_time and location_id:
            state = current_environment_state(conn, location_id=location_id, sim_time=str(sim_time))

        lines.extend(["", f"🌎 {region_name}", f"📍 Sampling · {anchor_name}"])
        if state is None:
            lines.append("⚪ No represented weather state is active for this universe time.")
            continue

        metadata = state.get("metadata") or {}
        synthetic = bool(metadata.get("synthetic"))
        source_label = "Synthetic continuity fallback" if synthetic else "Historical weather replay"
        precip_kind = _condition_label(state.get("precipitation_kind"))
        precip_intensity = max(0.0, min(1.0, float(state.get("precipitation_intensity") or 0.0)))
        cloud_cover = max(0.0, min(1.0, float(state.get("cloud_cover") or 0.0)))
        light_level = max(0.0, min(1.0, float(state.get("light_level") or 0.0)))
        lines.extend([
            f"{_condition_icon(state.get('condition'))} Condition · {_condition_label(state.get('condition'))}",
            f"🌡 Temperature · {_fmt_number(state.get('temperature_c'))} °C",
            f"🌧 Precipitation · {precip_kind} · {precip_intensity * 100:.0f}% intensity",
            f"💨 Wind · {_fmt_number(state.get('wind_speed_mps'))} m/s",
            f"👁 Visibility · {_fmt_number(state.get('visibility_km'))} km",
            f"☁️ Cloud · {cloud_cover * 100:.0f}%",
            f"☀️ Daylight · {_condition_label(state.get('daylight_state'))} · light {light_level * 100:.0f}%",
            f"🛰 Source · {source_label}",
            f"⏱ Valid · {_fmt_time(state.get('valid_from_sim_time'))} → {_fmt_time(state.get('valid_until_sim_time'))}",
        ])
        if synthetic:
            lines.append("⚠️ Continuity fallback; not claimed as historical truth.")
        else:
            lines.append("✅ Historical provider state; sampling anchor is regional, not an exact fictional address.")

    lines.extend([
        "",
        "ℹ️ Provider capability is global and coordinate-based. Only represented/registered regions become universe weather state; arbitrary Earth lookup remains a future Creator reference utility and must not mutate the world.",
    ])
    keyboard = [
        [{"text": "↻ Refresh", "callback_data": "uni:weather"}],
        [{"text": "🌎 Regions", "callback_data": "uni:regions"}],
        [{"text": "← Universe", "callback_data": "nav:universe"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]
    return "\n".join(lines), keyboard


def regions_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    geography = load_observer_geography()
    regions = geography.get("regions") or []
    lines = ["🌎 REGIONS", "━━━━━━━━━━━━━━━━━━", "Geographic context represented to the Creator:"]
    keyboard: list[list[dict[str, str]]] = []
    for region in regions:
        weather_mark = " · 🌤" if region.get("weather_provider_id") else ""
        lines.append(f"• {region['name']}{weather_mark}")
        keyboard.append([{"text": f"🌎 {region['name']}", "callback_data": f"region:{region['id']}"}])
    if not regions:
        lines.append("• None")
    keyboard.extend([
        [{"text": "← Universe", "callback_data": "nav:universe"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def region_view(conn, region_id: str) -> tuple[str, list[list[dict[str, str]]]]:
    geography = load_observer_geography()
    region = next((item for item in geography.get("regions") or [] if item.get("id") == region_id), None)
    if region is None:
        return "Unknown geographic region.", [[{"text": "← Regions", "callback_data": "uni:regions"}]]

    location_ids = [str(value) for value in region.get("locations") or []]
    locations: list[dict[str, Any]] = []
    for world in list_worlds(conn):
        for location in list_locations(conn, world["id"]):
            if location["id"] in location_ids:
                locations.append(location)

    traversal = str(region.get("traversal_status") or "unknown").replace("_", " ").title()
    weather_status = "Registered" if region.get("weather_provider_id") else "Not registered"
    lines = [
        f"🌎 {region['name'].upper()}",
        "━━━━━━━━━━━━━━━━━━",
        "Regional geographic context",
        f"🌤 Weather           {weather_status}",
        f"🚧 Outward traversal   {traversal}",
        "",
        "📍 Represented locations",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for location in locations:
        lines.append(f"• {location['name']}")
        keyboard.append([{"text": f"📍 {location['name']}", "callback_data": f"loc:{location['id']}"}])
    if not locations:
        lines.append("• None")
    note = str(region.get("note") or "").strip()
    if note:
        lines.extend(["", note])
    keyboard.extend([
        [{"text": "🌤 Weather", "callback_data": "uni:weather"}],
        [{"text": "← Regions", "callback_data": "uni:regions"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def locations_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    worlds = list_worlds(conn)
    lines = ["📍 LOCATIONS", "━━━━━━━━━━━━━━━━━━", "Represented simulation places:"]
    keyboard: list[list[dict[str, str]]] = []
    for world in worlds:
        for location in list_locations(conn, world["id"]):
            lines.append(f"• {location['name']}")
            keyboard.append([{"text": f"📍 {location['name']}", "callback_data": f"loc:{location['id']}"}])
    if not keyboard:
        lines.append("• None")
    keyboard.extend([
        [{"text": "← Universe", "callback_data": "nav:universe"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard

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
    sim_time = runtime_value(conn, "sim_time", None)
    config = load_weather_provider_config()
    providers = config.get("providers") or []
    provider = providers[0] if providers else None
    location_id = str(provider.get("scope_location_id")) if provider else ""
    anchor = (provider or {}).get("geographic_anchor") or {}
    anchor_name = str(anchor.get("name") or "South Lake Tahoe city-area")

    state = None
    if sim_time and location_id:
        state = current_environment_state(conn, location_id=location_id, sim_time=str(sim_time))

    lines = ["🌤 UNIVERSE WEATHER", "━━━━━━━━━━━━━━━━━━", f"📍 {anchor_name}", f"🕒 {_fmt_time(sim_time)}"]
    if state is None:
        lines.extend([
            "",
            "No represented weather state is active for this universe time.",
            "The weather producer owns synchronization; this screen is read-only.",
        ])
    else:
        metadata = state.get("metadata") or {}
        synthetic = bool(metadata.get("synthetic"))
        source_label = "Synthetic continuity fallback" if synthetic else "Historical weather replay"
        precip_kind = _condition_label(state.get("precipitation_kind"))
        precip_intensity = max(0.0, min(1.0, float(state.get("precipitation_intensity") or 0.0)))
        cloud_cover = max(0.0, min(1.0, float(state.get("cloud_cover") or 0.0)))
        light_level = max(0.0, min(1.0, float(state.get("light_level") or 0.0)))
        lines.extend([
            "",
            f"{_condition_icon(state.get('condition'))} Condition     {_condition_label(state.get('condition'))}",
            f"🌡 Temperature   {_fmt_number(state.get('temperature_c'))} °C",
            f"🌧 Precipitation {precip_kind} · {precip_intensity * 100:.0f}% intensity",
            f"💨 Wind          {_fmt_number(state.get('wind_speed_mps'))} m/s",
            f"👁 Visibility    {_fmt_number(state.get('visibility_km'))} km",
            f"☁️ Cloud cover   {cloud_cover * 100:.0f}%",
            f"☀️ Daylight      {_condition_label(state.get('daylight_state'))} · light {light_level * 100:.0f}%",
            "",
            f"🛰 Source        {source_label}",
            f"⏱ Valid from    {_fmt_time(state.get('valid_from_sim_time'))}",
            f"⏱ Valid until   {_fmt_time(state.get('valid_until_sim_time'))}",
        ])
        if synthetic:
            lines.extend(["", "⚠️ This state preserves simulation continuity; it is not claimed as historical truth."])
        else:
            lines.extend(["", "✅ Historical provider state. Sampling represents the South Lake Tahoe area, not an exact fictional Estate coordinate."])

    keyboard = [
        [{"text": "↻ Refresh", "callback_data": "uni:weather"}],
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
        lines.append(f"• {region['name']}")
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
    lines = [
        f"🌎 {region['name'].upper()}",
        "━━━━━━━━━━━━━━━━━━",
        "Regional geographic context",
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

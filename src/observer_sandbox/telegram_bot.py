from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .autonomy import set_autonomy_paused, set_autonomy_speed
from .creator_control import BASIC_STAT_BASELINE, restore_basic_stats
from .db import connect, migrate
from .observer_query import (
    character_summary,
    list_characters,
    list_locations,
    list_worlds,
    location_summary,
    object_summary,
    observer_status,
    recent_history,
)
from .secrets import load_runtime_secrets
from .simulation import runtime_value, set_runtime_value
from .telegram_cognition_context import cognition_context_view
from .telegram_economy import character_finances_view, location_asset_lines, object_value_lines
from .telegram_profile_browser import character_keyboard, profile_callback_view

DEFAULT_DB = Path(os.environ.get("OBSERVER_SANDBOX_DB", "/var/lib/observer-sandbox/observer.sqlite3"))
NOTIFY_KEY_PREFIX = "telegram_notifications:"


def _parse_user_ids(raw: str) -> set[int]:
    result: set[int] = set()
    for part in raw.replace(";", ",").split(","):
        part = part.strip()
        if part:
            try:
                result.add(int(part))
            except ValueError:
                continue
    return result


def _owner_user_id() -> int | None:
    raw = os.environ.get("OBSERVER_TELEGRAM_OWNER_ID", "").strip()
    if not raw:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def _allowed_user_ids() -> set[int]:
    return _parse_user_ids(os.environ.get("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", ""))


def _user_role(user_id: int) -> str:
    owner_id = _owner_user_id()
    if owner_id is not None and user_id == owner_id:
        return "owner"
    if user_id in _allowed_user_ids():
        return "allowed"
    return "unauthorized"


def _api(token: str, method: str, payload: dict[str, Any] | None = None, *, timeout: int = 30) -> Any:
    data = urllib.parse.urlencode(payload or {}).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/{method}",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = json.loads(response.read().decode("utf-8"))
    if not body.get("ok"):
        raise RuntimeError(body.get("description", "Telegram API request failed"))
    return body.get("result")


def _reply_markup(keyboard: list[list[dict[str, str]]] | None) -> str | None:
    return json.dumps({"inline_keyboard": keyboard}) if keyboard else None


def _send(token: str, chat_id: int, text: str, keyboard: list[list[dict[str, str]]] | None = None) -> None:
    payload: dict[str, Any] = {"chat_id": chat_id, "text": text[:4096]}
    markup = _reply_markup(keyboard)
    if markup:
        payload["reply_markup"] = markup
    _api(token, "sendMessage", payload, timeout=15)


def _edit(token: str, chat_id: int, message_id: int, text: str, keyboard: list[list[dict[str, str]]] | None = None) -> None:
    payload: dict[str, Any] = {"chat_id": chat_id, "message_id": message_id, "text": text[:4096]}
    markup = _reply_markup(keyboard)
    if markup:
        payload["reply_markup"] = markup
    _api(token, "editMessageText", payload, timeout=15)


def _fmt_time(value: str | None) -> str:
    if not value:
        return "Unknown"
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        return dt.strftime("%d-%m-%Y (%A) %I:%M %p")
    except (ValueError, TypeError):
        return str(value)


def _fmt_real_seconds(seconds: float) -> str:
    seconds = max(0.0, float(seconds))
    if seconds < 60:
        return f"~{max(1, round(seconds))} sec real"
    minutes = seconds / 60.0
    if minutes < 90:
        value = round(minutes, 1) if abs(minutes - round(minutes)) >= 0.05 else int(round(minutes))
        return f"~{value} min real"
    hours = minutes / 60.0
    value = round(hours, 1) if abs(hours - round(hours)) >= 0.05 else int(round(hours))
    return f"~{value} hr real"


def _pending_expected_sim_time(pending: dict[str, Any]) -> str | None:
    planned = pending.get("planned_sim_time")
    duration = pending.get("duration_minutes")
    if not planned or duration is None:
        return None
    try:
        return (datetime.fromisoformat(str(planned)) + timedelta(minutes=int(duration))).isoformat()
    except (TypeError, ValueError):
        return None


def _pending_timing_lines(status: dict[str, Any] | None, *, now_wall: float | None = None) -> list[str]:
    pending = (status or {}).get("pending_action")
    if not pending:
        return []
    duration = pending.get("duration_minutes")
    if duration is None:
        return []
    speed = float(pending.get("speed_at_plan") or (status or {}).get("speed") or 1.0)
    wall_seconds = float(duration) * 60.0 / max(speed, 0.000001)
    lines = [f"⏱ Duration   {int(duration)} sim min • {_fmt_real_seconds(wall_seconds)} @ {speed:g}x"]
    expected = _pending_expected_sim_time(pending)
    if expected:
        lines.append(f"⏳ Expected   {_fmt_time(expected)}")
    due = pending.get("due_wall_time")
    if due is not None:
        now = time.time() if now_wall is None else float(now_wall)
        lines.append(f"⌛ Remaining  {_fmt_real_seconds(max(0.0, float(due) - now))}")
    return lines


def _yes_no(value: bool) -> str:
    return "Yes" if value else "No"


def _title_action(value: str | None) -> str:
    return (value or "idle").replace("_", " ").title()


def _friendly_field(value: str) -> str:
    return value.split(".")[-1].replace("_", " ").title()


def _fmt_number(value: Any, *, signed: bool = False) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        number = float(value)
        text = f"{number:.1f}".rstrip("0").rstrip(".")
        if signed and number > 0:
            return f"+{text}"
        return text
    return str(value)


def _fmt_effect_spec(spec: Any) -> str:
    if isinstance(spec, (int, float)):
        return _fmt_number(spec, signed=True)
    if not isinstance(spec, dict):
        return str(spec)
    parts: list[str] = []
    labels = {"add": "Add", "multiply": "×", "set": "Set", "clamp_min": "Min", "clamp_max": "Max"}
    for operation in ("add", "multiply", "set", "clamp_min", "clamp_max"):
        if operation not in spec:
            continue
        value = spec[operation]
        if operation == "add":
            parts.append(_fmt_number(value, signed=True))
        elif operation == "multiply":
            parts.append(f"×{_fmt_number(value)}")
        else:
            parts.append(f"{labels[operation]} {_fmt_number(value)}")
    return ", ".join(parts) if parts else str(spec)


def _notifications_enabled(conn, user_id: int) -> bool:
    return bool(runtime_value(conn, f"{NOTIFY_KEY_PREFIX}{user_id}", True))


def _set_notifications(conn, user_id: int, enabled: bool) -> bool:
    set_runtime_value(conn, f"{NOTIFY_KEY_PREFIX}{user_id}", bool(enabled))
    conn.commit()
    return bool(enabled)


def _boot_message() -> str:
    return (
        "🌌 OBSERVER SANDBOX\n━━━━━━━━━━━━━━━━━━\n✨ Universe is alive!\n🟢 Observer link: Online\n"
        "🧠 Minds: Wake-on-demand\n📡 Creator channel: Connected\n━━━━━━━━━━━━━━━━━━\nUse /start to open the Observer Home."
    )


def _home_message(conn, user_id: int) -> str:
    raw_role = _user_role(user_id)
    status = observer_status(conn, role=raw_role)
    c = status["character"]
    notify = "ON" if _notifications_enabled(conn, user_id) else "OFF"
    role = raw_role.title()
    return (
        "🌌 OBSERVER HOME\n━━━━━━━━━━━━━━━━━━\n✨ Universe is alive.\n\n"
        f"👤 Darian · {_title_action(c['current_action'])}\n📍 {c['location_name']}\n🕒 {_fmt_time(c['sim_time'])}\n"
        f"🔔 Notifications {notify}\n🔐 Access {role}\n\nChoose what you want to observe:"
    )


def _home_keyboard() -> list[list[dict[str, str]]]:
    return [
        [{"text": "🌍 Universe", "callback_data": "nav:universe"}, {"text": "👥 Characters", "callback_data": "nav:characters"}],
        [{"text": "🕒 Runtime", "callback_data": "nav:runtime"}, {"text": "📜 History", "callback_data": "nav:history"}],
    ]


def _back_home_keyboard() -> list[list[dict[str, str]]]:
    return [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]]


def _character_keyboard_for_user(character_id: str, user_id: int) -> list[list[dict[str, str]]]:
    keyboard = character_keyboard(character_id)
    if _user_role(user_id) == "owner":
        keyboard.insert(1, [{"text": "💰 Finances", "callback_data": f"eco:char:{character_id}"}])
        keyboard.insert(2, [{"text": "🧠 Cognition Context", "callback_data": f"cog:{character_id}:1:0"}])
        keyboard.insert(3, [{"text": "🩺 Restore Basic Stats", "callback_data": f"ctl:restore_prompt:{character_id}"}])
    return keyboard


def _fmt_character(data: dict[str, Any], status: dict[str, Any] | None = None, *, now_wall: float | None = None) -> str:
    c = data["character"]
    s = data["state"]
    pending = (status or {}).get("pending_action")
    action_text = _title_action(s["current_action"])
    target = (status or {}).get("pending_target_name") if pending else None
    if target:
        action_text += f" → {target}"
    lines = [
        f"👤 {c['name']}", "━━━━━━━━━━━━━━━━━━", f"📍 Location   {s['location_name']}",
        f"🎬 Action     {action_text}", f"🕒 Sim Time   {_fmt_time(s['sim_time'])}",
    ]
    lines.extend(_pending_timing_lines(status, now_wall=now_wall))
    lines.extend([
        "", f"⚡ Energy       {s['energy']:.1f}", f"🍽 Hunger       {s['hunger']:.1f}",
        f"💧 Thirst       {s['thirst']:.1f}", f"🌙 Sleepiness   {s['sleepiness']:.1f}", f"🫧 Cleanliness  {s['cleanliness']:.1f}",
    ])
    return "\n".join(lines)


def _character_view(conn, character_id: str, *, role: str = "owner", now_wall: float | None = None) -> str:
    return _fmt_character(
        character_summary(conn, character_id, role=role),
        observer_status(conn, character_id, role=role),
        now_wall=now_wall,
    )


def _fmt_restore_prompt(character_name: str) -> str:
    return (
        f"🩺 RESTORE {character_name.upper()} BASIC STATS\n━━━━━━━━━━━━━━━━━━\nCreator authority required.\n\n"
        f"⚡ Energy       {BASIC_STAT_BASELINE['needs.energy']:.0f}\n🍽 Hunger       {BASIC_STAT_BASELINE['needs.hunger']:.0f}\n"
        f"💧 Thirst       {BASIC_STAT_BASELINE['needs.thirst']:.0f}\n🌙 Sleepiness   {BASIC_STAT_BASELINE['needs.sleepiness']:.0f}\n"
        f"🫧 Cleanliness  {BASIC_STAT_BASELINE['physiology.cleanliness']:.0f}\n🛌 Fatigue      {BASIC_STAT_BASELINE['physiology.fatigue']:.0f}\n\n"
        "The current pending autonomous action will be cancelled so cognition can re-evaluate from the restored state. "
        "Location, simulation time, profile canon and autonomy mode are preserved."
    )


def _fmt_restore_result(result: dict[str, Any]) -> str:
    after = result["after"]
    cancelled = "Yes" if result.get("cancelled_action_id") else "No"
    return (
        "✅ CREATOR RESTORE APPLIED\n━━━━━━━━━━━━━━━━━━\n"
        f"👤 {result['character_name']}\n📍 {after['location_name']}\n🕒 {_fmt_time(after['sim_time'])}\n\n"
        f"⚡ Energy       {after['energy']:.1f}\n🍽 Hunger       {after['hunger']:.1f}\n💧 Thirst       {after['thirst']:.1f}\n"
        f"🌙 Sleepiness   {after['sleepiness']:.1f}\n🫧 Cleanliness  {after['cleanliness']:.1f}\n🛌 Fatigue      {after['fatigue']:.1f}\n\n"
        f"🧹 Pending action cancelled: {cancelled}\n🧠 Cognition will re-evaluate on the next wake."
    )


def _access_presentation(value: Any) -> tuple[str, str]:
    """Present the authored access policy without inventing actor-relative denial."""
    access = str(value or "open").strip().lower()
    known = {
        "open": ("🔓", "Open"),
        "public": ("🔓", "Public"),
        "resident": ("🏠", "Resident"),
        "owner_or_resident": ("🏠", "Owner Or Resident"),
        "private": ("🔐", "Private"),
        "authorized": ("🪪", "Authorized"),
        "restricted": ("⚠️", "Restricted"),
        "closed": ("⛔", "Closed"),
        "locked": ("🔒", "Locked"),
    }
    return known.get(access, ("ℹ️", access.replace("_", " ").title() or "Unknown"))


def _location_icon(location: dict[str, Any]) -> str:
    access = str(location.get("access") or "open").strip().lower()
    if access in {"closed", "locked"}:
        return _access_presentation(access)[0]
    kind = str(location.get("kind") or "").lower()
    if kind in {"estate", "residence", "building"}:
        return "🏛"
    if kind in {"floor", "level", "zone"}:
        return "🏢"
    if kind in {"room", "interior"}:
        return "🚪"
    return "📍"


def _fmt_location(data: dict[str, Any], conn=None) -> str:
    loc = data["location"]
    icon = _location_icon(loc)
    lines = [f"{icon} {loc['name']}", "━━━━━━━━━━━━━━━━━━"]
    kind = str(loc.get("kind") or "location").replace("_", " ").title()
    if kind and kind != "Location":
        lines.append(f"🧭 {kind}")
    access_icon, access_label = _access_presentation(loc.get("access"))
    lines.append(f"{access_icon} Access · {access_label}")
    if conn is not None:
        lines.extend(location_asset_lines(conn, str(loc["id"])))
    child_locations = data.get("child_locations") or []
    if child_locations:
        lines.extend(["", "🗺 Areas"])
        for child in child_locations:
            lines.append(f"• {_location_icon(child)} {child['name']}")
    occupants = data.get("occupants") or []
    if occupants:
        lines.extend(["", "👥 Present now"])
        for occupant in occupants:
            lines.append(f"• {occupant['name']} · {_title_action(occupant.get('current_action'))}")
    objects = data.get("objects") or []
    if objects:
        lines.extend(["", "📦 Objects"])
        for obj in objects:
            lines.append(f"• {obj['name']}")
    exits = data.get("exits") or []
    if exits:
        lines.extend(["", "🚪 Exits"])
        for exit_node in exits:
            lines.append(f"• {exit_node['name']}")
    activity = data.get("recent_activity") or []
    if activity:
        lines.extend(["", "🎬 Recent activity"])
        for event in activity:
            action = _title_action(event.get("action"))
            target = event.get("target_name")
            detail = f"{action} → {target}" if target else action
            actor = event.get("actor_name") or "Character"
            lines.append(f"• {actor} · {detail}")
            lines.append(f"  {_fmt_time(event.get('sim_time'))}")
    if not child_locations and not occupants and not objects and not exits and not activity:
        lines.extend(["", "No observable contents yet."])
    return "\n".join(lines)


def _fmt_object(data: dict[str, Any], conn=None) -> str:
    obj = data["object"]
    definition = data.get("definition")
    location = data.get("location")
    capabilities = data.get("capabilities") or []
    effects = data.get("effects") or {}
    lines = [f"📦 {obj['name']}", "━━━━━━━━━━━━━━━━━━", "🧩 Concrete object"]
    if definition:
        lines.append(f"🧬 Definition   {definition['name']}")
    else:
        lines.append("🧬 Definition   Instance-only fixture")
    if location:
        lines.append(f"📍 Location     {location['name']}")
    if conn is not None:
        lines.extend(object_value_lines(conn, str(obj["id"])))
    if capabilities:
        lines.extend(["", "⚙️ Capabilities"])
        lines.append("• " + " · ".join(str(value).replace("_", " ").title() for value in capabilities))
    if effects:
        lines.extend(["", "✨ Authored effects"])
        for action, fields in effects.items():
            lines.append(f"• {_title_action(str(action))}")
            if isinstance(fields, dict):
                for field_key, spec in fields.items():
                    lines.append(f"  ↳ {_friendly_field(str(field_key))}: {_fmt_effect_spec(spec)}")
            else:
                lines.append(f"  ↳ {_fmt_effect_spec(fields)}")
    else:
        lines.extend(["", "✨ Authored effects", "• None"])
    return "\n".join(lines)


def _location_keyboard(data: dict[str, Any]) -> list[list[dict[str, str]]]:
    keyboard: list[list[dict[str, str]]] = []
    for child in data.get("child_locations") or []:
        keyboard.append([{"text": f"{_location_icon(child)} {child['name']}", "callback_data": f"loc:{child['id']}"}])
    for obj in data.get("objects") or []:
        keyboard.append([{"text": f"📦 {obj['name']}", "callback_data": f"obj:{obj['id']}"}])
    parent = data.get("parent")
    if parent:
        if parent.get("type") == "world":
            keyboard.append([{"text": "← Universe", "callback_data": "nav:universe"}])
        else:
            keyboard.append([{"text": f"← {parent['name']}", "callback_data": f"loc:{parent['id']}"}])
    else:
        keyboard.append([{"text": "← Universe", "callback_data": "nav:universe"}])
    keyboard.append([{"text": "⌂ Observer Home", "callback_data": "nav:home"}])
    return keyboard


def _object_keyboard(data: dict[str, Any]) -> list[list[dict[str, str]]]:
    location = data.get("location")
    keyboard: list[list[dict[str, str]]] = []
    if location:
        keyboard.append([{"text": f"← {location['name']}", "callback_data": f"loc:{location['id']}"}])
    keyboard.append([{"text": "⌂ Observer Home", "callback_data": "nav:home"}])
    return keyboard


def _fmt_history(rows: list[dict[str, Any]]) -> str:
    visible = [row for row in rows if row.get("action")]
    if not visible:
        return "🕰 Recent Activity\n━━━━━━━━━━━━━━━━━━\nNo character activity yet."
    lines = ["🕰 Recent Activity", "━━━━━━━━━━━━━━━━━━"]
    for row in visible:
        detail = _title_action(row.get("action"))
        target = row.get("target_name") or row.get("target")
        if target:
            detail += f" → {target}"
        lines.append(f"• {_fmt_time(row['sim_time'])}")
        lines.append(f"  {detail}")
        if row.get("reason"):
            lines.append(f"  ↳ {row['reason']}")
    return "\n".join(lines)


def _fmt_status(data: dict[str, Any], *, now_wall: float | None = None) -> str:
    c = data["character"]
    pending = data.get("pending_action")
    calls = int((data.get("cognition_stats") or {}).get("decision_calls", 0))
    autonomy_icon = "🟢" if data["autonomy_enabled"] else "⚪"
    pending_text = "None"
    if pending:
        pending_text = _title_action(pending.get("action"))
        target = data.get("pending_target_name")
        if target:
            pending_text += f" → {target}"
    lines = [
        "🌌 OBSERVER SANDBOX", "━━━━━━━━━━━━━━━━━━",
        f"{autonomy_icon} Autonomy   {'ON' if data['autonomy_enabled'] else 'OFF'} · {str(data['mode']).replace('_', ' ').title()}",
        f"⏸ Paused     {_yes_no(data['paused'])}", f"⏩ Speed      {data['speed']}x", f"🧠 Mind Calls {calls}", f"⏳ Pending    {pending_text}",
    ]
    lines.extend(_pending_timing_lines(data, now_wall=now_wall))
    lines.extend(["", "👤 Darian Thorne", f"📍 {c['location_name']}", f"🎬 {_title_action(c['current_action'])}", f"🕒 {_fmt_time(c['sim_time'])}"])
    return "\n".join(lines)


def _universe_view(conn) -> tuple[str, list[list[dict[str, str]]]]:
    worlds = list_worlds(conn)
    lines = ["🌍 UNIVERSE", "━━━━━━━━━━━━━━━━━━", "Select a place to observe:"]
    keyboard: list[list[dict[str, str]]] = []
    for world in worlds:
        lines.append(f"• {world['name']}")
        for location in list_locations(conn, world["id"]):
            keyboard.append([{"text": f"{_location_icon(location)} {location['name']}", "callback_data": f"loc:{location['id']}"}])
    keyboard.append([{"text": "⌂ Observer Home", "callback_data": "nav:home"}])
    return "\n".join(lines), keyboard


def _characters_view(conn, *, role: str = "owner") -> tuple[str, list[list[dict[str, str]]]]:
    chars = list_characters(conn, role=role)
    lines = ["👥 CHARACTERS", "━━━━━━━━━━━━━━━━━━", "Select a character:"]
    keyboard: list[list[dict[str, str]]] = []
    for char in chars:
        lines.append(f"• {char['name']} · {_title_action(char['current_action'])} · {char['location_name']}")
        keyboard.append([{"text": f"👤 {char['name']}", "callback_data": f"char:{char['id']}"}])
    keyboard.append([{"text": "⌂ Observer Home", "callback_data": "nav:home"}])
    return "\n".join(lines), keyboard


def _callback_view(conn, user_id: int, callback_data: str) -> tuple[str, list[list[dict[str, str]]] | None]:
    role = _user_role(user_id)
    if callback_data == "nav:home":
        return _home_message(conn, user_id), _home_keyboard()
    if callback_data == "nav:universe":
        return _universe_view(conn)
    if callback_data == "nav:characters":
        return _characters_view(conn, role=role)
    if callback_data == "nav:runtime":
        return _fmt_status(observer_status(conn, role=role)), _back_home_keyboard()
    if callback_data == "nav:history":
        return _fmt_history(recent_history(conn, limit=16, role=role)), _back_home_keyboard()
    if callback_data.startswith("cog:"):
        parts = callback_data.split(":")
        if len(parts) != 4:
            return "Unknown cognition context destination.", _back_home_keyboard()
        character_id, raw_slot, raw_page = parts[1], parts[2], parts[3]
        if role != "owner":
            return "🔒 Creator authority required for cognition context.", character_keyboard(character_id)
        try:
            slot = int(raw_slot)
            page = int(raw_page)
        except ValueError:
            slot, page = 1, 0
        return cognition_context_view(conn, character_id, slot=slot, page=page)
    if callback_data.startswith("ctl:restore_prompt:"):
        character_id = callback_data.split(":", 2)[2]
        if role != "owner":
            return "🔒 Creator authority required for this control.", character_keyboard(character_id)
        data = character_summary(conn, character_id, role=role)
        return _fmt_restore_prompt(data["character"]["name"]), [
            [{"text": "✅ Confirm Restore", "callback_data": f"ctl:restore_apply:{character_id}"}],
            [{"text": "← Character", "callback_data": f"char:{character_id}"}],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ]
    if callback_data.startswith("ctl:restore_apply:"):
        character_id = callback_data.split(":", 2)[2]
        if role != "owner":
            return "🔒 Creator authority required for this control.", character_keyboard(character_id)
        result = restore_basic_stats(conn, character_id, authority="creator", requested_by=f"telegram:{user_id}")
        return _fmt_restore_result(result), _character_keyboard_for_user(character_id, user_id)
    if callback_data.startswith("eco:char:"):
        character_id = callback_data.split(":", 2)[2]
        if role != "owner":
            return "🔒 Creator authority required for financial details.", character_keyboard(character_id)
        try:
            return character_finances_view(conn, character_id)
        except KeyError:
            return "💰 No represented financial state for this character yet.", character_keyboard(character_id)
    profile_view = profile_callback_view(conn, callback_data, role=role)
    if profile_view is not None:
        return profile_view
    if callback_data.startswith("loc:"):
        location_id = callback_data.split(":", 1)[1]
        data = location_summary(conn, location_id, role=role)
        return _fmt_location(data, conn), _location_keyboard(data)
    if callback_data.startswith("obj:"):
        object_id = callback_data.split(":", 1)[1]
        data = object_summary(conn, object_id)
        return _fmt_object(data, conn), _object_keyboard(data)
    if callback_data.startswith("char:"):
        character_id = callback_data.split(":", 1)[1]
        return _character_view(conn, character_id, role=role), _character_keyboard_for_user(character_id, user_id)
    return "Unknown observer destination.", _back_home_keyboard()


def _help(role: str) -> str:
    role_label = "Owner" if role == "owner" else "Authorized User"
    lines = [
        f"🌌 Observer Sandbox · {role_label}", "━━━━━━━━━━━━━━━━━━", "/start — Observer Home", "/status — Runtime overview",
        "/watch — Darian now + recent activity", "/history [n] — Recent activity", "/darian — Character summary", "/home — Thorne Estate summary",
        "/notify on|off — Proactive notifications", "/pause — Pause autonomy", "/resume — Resume autonomy", "/speed <value> — Set runtime speed",
    ]
    if role == "owner":
        lines.append("/restorestats [character_id] — Restore basic living stats")
    lines.append("/whoami — Show your Telegram identity")
    return "\n".join(lines)


def handle_command(db_path: str | Path, *, user_id: int, text: str) -> str:
    role = _user_role(user_id)
    command_line = (text or "").strip()
    first, *rest = command_line.split()
    command = first.split("@", 1)[0].lower() if first else ""
    if command in {"/whoami", "/start"} and role == "unauthorized":
        return f"Observer Sandbox bot is connected. Your Telegram user id is {user_id}. Role: unauthorized. Ask the owner to authorize this id."
    if role == "unauthorized":
        return "Not authorized. Use /whoami to obtain your Telegram user id."
    if command == "/whoami":
        return f"🪪 Telegram Identity\n━━━━━━━━━━━━━━━━━━\nUser ID: {user_id}\nRole: {role.title()}"
    with connect(db_path) as conn:
        migrate(conn)
        if command == "/start":
            return _home_message(conn, user_id)
        if command == "/help":
            return _help(role)
        if command == "/status":
            return _fmt_status(observer_status(conn, role=role))
        if command == "/darian":
            return _character_view(conn, "char_darian", role=role)
        if command == "/home":
            return _fmt_location(location_summary(conn, "loc_thorne_estate", role=role), conn)
        if command == "/watch":
            return _character_view(conn, "char_darian", role=role) + "\n\n" + _fmt_history(recent_history(conn, limit=12, role=role))
        if command == "/history":
            limit = 8
            if rest:
                try:
                    limit = max(1, min(int(rest[0]), 20))
                except ValueError:
                    return "Usage: /history [1-20]"
            return _fmt_history(recent_history(conn, limit=max(limit * 2, 12), role=role))
        if command in {"/notify", "/notification", "/notifications"}:
            if not rest or rest[0].lower() not in {"on", "off"}:
                return f"🔔 Notifications are {'ON' if _notifications_enabled(conn, user_id) else 'OFF'}.\nUse /notify on or /notify off."
            enabled = _set_notifications(conn, user_id, rest[0].lower() == "on")
            return f"🔔 Notifications {'ON' if enabled else 'OFF'}\n━━━━━━━━━━━━━━━━━━\nPreference saved."
        if command in {"/notion/on", "/notion/off"}:
            enabled = _set_notifications(conn, user_id, command.endswith("/on"))
            return f"🔔 Notifications {'ON' if enabled else 'OFF'}\n━━━━━━━━━━━━━━━━━━\nPreference saved."
        if command == "/restorestats":
            if role != "owner":
                return "🔒 Creator authority required for /restorestats."
            character_id = rest[0] if rest else "char_darian"
            try:
                result = restore_basic_stats(conn, character_id, authority="creator", requested_by=f"telegram:{user_id}")
            except KeyError:
                return f"Unknown character: {character_id}"
            return _fmt_restore_result(result)
        if command == "/pause":
            set_autonomy_paused(conn, True)
            return _fmt_status(observer_status(conn, role=role))
        if command == "/resume":
            set_autonomy_paused(conn, False)
            return _fmt_status(observer_status(conn, role=role))
        if command == "/speed":
            if not rest:
                return "Usage: /speed <0-3600>"
            try:
                set_autonomy_speed(conn, float(rest[0]))
                return _fmt_status(observer_status(conn, role=role))
            except ValueError as exc:
                return f"Speed rejected: {exc}"
        return _help(role)


def _command_keyboard(command: str) -> list[list[dict[str, str]]] | None:
    return _home_keyboard() if command == "/start" else None


def run_polling(db_path: str | Path = DEFAULT_DB) -> None:
    load_runtime_secrets()
    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return
    owner_id = _owner_user_id()
    if owner_id is not None:
        try:
            with connect(db_path) as conn:
                migrate(conn)
                notify_owner = _notifications_enabled(conn, owner_id)
            if notify_owner:
                _send(token, owner_id, _boot_message())
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
            pass
    offset: int | None = None
    backoff = 1.0
    while True:
        try:
            payload: dict[str, Any] = {"timeout": 20, "allowed_updates": json.dumps(["message", "callback_query"])}
            if offset is not None:
                payload["offset"] = offset
            updates = _api(token, "getUpdates", payload, timeout=30) or []
            backoff = 1.0
            for update in updates:
                offset = int(update["update_id"]) + 1
                callback = update.get("callback_query") or {}
                if callback:
                    sender = callback.get("from") or {}
                    user_id = int(sender.get("id", 0))
                    message = callback.get("message") or {}
                    chat = message.get("chat") or {}
                    if chat.get("type") != "private" or _user_role(user_id) == "unauthorized":
                        _api(token, "answerCallbackQuery", {"callback_query_id": callback.get("id"), "text": "Not authorized"}, timeout=10)
                        continue
                    try:
                        with connect(db_path) as conn:
                            migrate(conn)
                            text, keyboard = _callback_view(conn, user_id, str(callback.get("data", "")))
                        _edit(token, int(chat["id"]), int(message["message_id"]), text, keyboard)
                        _api(token, "answerCallbackQuery", {"callback_query_id": callback.get("id")}, timeout=10)
                    except Exception:
                        _api(token, "answerCallbackQuery", {"callback_query_id": callback.get("id"), "text": "Observer action failed safely"}, timeout=10)
                    continue
                message = update.get("message") or {}
                chat = message.get("chat") or {}
                sender = message.get("from") or {}
                text = message.get("text")
                if not text or chat.get("type") != "private":
                    continue
                chat_id = int(chat["id"])
                user_id = int(sender.get("id", chat_id))
                try:
                    reply = handle_command(db_path, user_id=user_id, text=text)
                except Exception as exc:
                    reply = f"Observer command failed safely: {type(exc).__name__}"
                command = text.strip().split()[0].split("@", 1)[0].lower() if text.strip() else ""
                _send(token, chat_id, reply, _command_keyboard(command))
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
            time.sleep(backoff)
            backoff = min(backoff * 2.0, 30.0)

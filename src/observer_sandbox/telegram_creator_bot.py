from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

from . import telegram_bot as base
from .creator_control import replenish_inventory_stack
from .creator_studio import CreatorStudioError, ai_draft, manual_draft
from .db import connect, migrate
from .profile_change_observer import (
    reset_all_stat_notification_baselines,
    set_stat_notifications,
    stat_notifications_enabled,
)
from .telegram_ai_control import callback_view as ai_callback_view
from .telegram_ai_control import home_view as ai_home_view
from .telegram_creator_studio import draft_preview_view, studio_callback_view, studio_home_view
from .telegram_inventory import inventory_callback_view, inventory_command_view
from .telegram_news import generate_news_view, news_view
from .telegram_profile_browser import profile_callback_view
from .telegram_real_runtime import handle_real_runtime_command
from .telegram_sandbox_runtime import handle_sandbox_runtime_command
from .telegram_universe import locations_view, region_view, regions_view, universe_view, weather_view
from .telegram_world_layers import world_layer_callback_view

_ORIGINAL_API = base._api
_ORIGINAL_SEND = base._send
_ORIGINAL_EDIT = base._edit
_ORIGINAL_CALLBACK_VIEW = base._callback_view
_ORIGINAL_HOME_MESSAGE = base._home_message
_ORIGINAL_HOME_KEYBOARD = base._home_keyboard
_ORIGINAL_HANDLE_COMMAND = base.handle_command
_ORIGINAL_COMMAND_KEYBOARD = base._command_keyboard
_ORIGINAL_HELP = base._help
_ORIGINAL_CHARACTER_KEYBOARD_FOR_USER = base._character_keyboard_for_user
_DELETE_SENTINEL = "__DELETE_OBSERVER_HOME__"
_HOME_DELETE_DEADLINES: dict[tuple[int, int], float] = {}
_REAL_RUNTIME_COMMANDS = {"/realstatus", "/realpause", "/realresume", "/realspeed", "/realtime"}
_SANDBOX_RUNTIME_COMMANDS = {"/sandboxstatus", "/sandboxpause", "/sandboxresume", "/sandboxspeed", "/sandboxtime"}
_AMBIGUOUS_RUNTIME_COMMANDS = {"/pause", "/resume", "/speed", "/time"}


def _home_ttl_seconds() -> int:
    raw = os.environ.get("OBSERVER_TELEGRAM_HOME_TTL_SECONDS", "300").strip()
    try:
        value = int(raw)
    except ValueError:
        value = 300
    return max(30, min(value, 3600))


def _home_message(conn, user_id: int) -> str:
    ttl_minutes = _home_ttl_seconds() / 60.0
    ttl_text = f"{int(ttl_minutes)} min" if ttl_minutes.is_integer() else f"{ttl_minutes:g} min"
    text = _ORIGINAL_HOME_MESSAGE(conn, user_id).replace(
        "Choose what you want to observe:",
        "Choose a world layer:",
    )
    return text + f"\n\n🧹 Auto-close: {ttl_text}"


def _home_keyboard() -> list[list[dict[str, str]]]:
    return [
        [
            {"text": "🌍 Real World", "callback_data": "nav:real"},
            {"text": "🧪 Sandbox World", "callback_data": "nav:sandbox"},
        ],
        [{"text": "⚙️ Creator Settings", "callback_data": "ai:home"}],
        [{"text": "✕ Close", "callback_data": "nav:close"}],
    ]


def _preserve_owner_context_order(keyboard: list[list[dict[str, str]]]) -> list[list[dict[str, str]]]:
    """Keep Cognition Context directly under Profile as an established UX invariant."""
    for index, row in enumerate(keyboard):
        if not row:
            continue
        callback = str(row[0].get("callback_data") or "")
        if callback.startswith("cog:"):
            if index != 1:
                cognition_row = keyboard.pop(index)
                keyboard.insert(1, cognition_row)
            break
    return keyboard


def _stat_control_index(keyboard: list[list[dict[str, str]]]) -> int:
    """Keep owner-only Cognition Context immediately below Profile when present."""
    if len(keyboard) > 1 and keyboard[1]:
        callback = str(keyboard[1][0].get("callback_data") or "")
        if callback.startswith("cog:"):
            return 2
    return 1


def _character_keyboard_for_user(character_id: str, user_id: int) -> list[list[dict[str, str]]]:
    keyboard = [list(row) for row in _ORIGINAL_CHARACTER_KEYBOARD_FOR_USER(character_id, user_id)]
    keyboard = _preserve_owner_context_order(keyboard)
    if base._user_role(user_id) != "unauthorized":
        keyboard.insert(
            _stat_control_index(keyboard),
            [{"text": "🔔 Stat Updates", "callback_data": f"pref:statnotify:{character_id}:toggle"}],
        )
    return keyboard


def _character_keyboard_with_stat_pref(conn, character_id: str, user_id: int) -> list[list[dict[str, str]]]:
    keyboard = [list(row) for row in _ORIGINAL_CHARACTER_KEYBOARD_FOR_USER(character_id, user_id)]
    keyboard = _preserve_owner_context_order(keyboard)
    if base._user_role(user_id) != "unauthorized":
        enabled = stat_notifications_enabled(conn, user_id, character_id)
        keyboard.insert(
            _stat_control_index(keyboard),
            [{
                "text": f"🔔 Stat Updates: {'ON' if enabled else 'OFF'}",
                "callback_data": f"pref:statnotify:{character_id}:toggle",
            }],
        )
    return keyboard


def _forget_home_delete(chat_id: int, message_id: int) -> None:
    _HOME_DELETE_DEADLINES.pop((int(chat_id), int(message_id)), None)


def _arm_home_delete(chat_id: int, message_id: int) -> None:
    _HOME_DELETE_DEADLINES[(int(chat_id), int(message_id))] = time.time() + _home_ttl_seconds()


def _expire_home_messages(token: str, *, now: float | None = None) -> None:
    current = time.time() if now is None else float(now)
    due = [key for key, deadline in _HOME_DELETE_DEADLINES.items() if deadline <= current]
    for chat_id, message_id in due:
        try:
            _ORIGINAL_API(
                token,
                "deleteMessage",
                {"chat_id": chat_id, "message_id": message_id},
                timeout=10,
            )
        except Exception:
            pass
        finally:
            _forget_home_delete(chat_id, message_id)


def _api(token: str, method: str, payload: dict[str, Any] | None = None, *, timeout: int = 30) -> Any:
    result = _ORIGINAL_API(token, method, payload, timeout=timeout)
    if method == "getUpdates":
        _expire_home_messages(token)
    return result


def _send(token: str, chat_id: int, text: str, keyboard: list[list[dict[str, str]]] | None = None) -> Any:
    payload: dict[str, Any] = {"chat_id": chat_id, "text": text[:4096]}
    markup = base._reply_markup(keyboard)
    if markup:
        payload["reply_markup"] = markup
    result = _ORIGINAL_API(token, "sendMessage", payload, timeout=15)
    if text.startswith("🌌 OBSERVER HOME") and isinstance(result, dict) and result.get("message_id") is not None:
        _arm_home_delete(chat_id, int(result["message_id"]))
    return result


def _edit(token: str, chat_id: int, message_id: int, text: str, keyboard: list[list[dict[str, str]]] | None = None) -> None:
    if text == _DELETE_SENTINEL:
        try:
            _ORIGINAL_API(
                token,
                "deleteMessage",
                {"chat_id": int(chat_id), "message_id": int(message_id)},
                timeout=10,
            )
        finally:
            _forget_home_delete(chat_id, message_id)
        return
    _ORIGINAL_EDIT(token, chat_id, message_id, text, keyboard)
    if text.startswith("🌌 OBSERVER HOME"):
        _arm_home_delete(chat_id, message_id)
    else:
        _forget_home_delete(chat_id, message_id)


def _resolve_character(conn, raw: str) -> tuple[str, str] | None:
    query = raw.strip()
    if not query:
        return None
    row = conn.execute(
        """SELECT e.id,e.name
        FROM entities e JOIN character_profiles p ON p.entity_id=e.id
        WHERE e.entity_type='character' AND p.status='active'
          AND (e.id=? OR lower(e.name)=lower(?))
        LIMIT 1""",
        (query, query),
    ).fetchone()
    if row is None:
        return None
    return str(row["id"]), str(row["name"])


def _statnotify_status(conn, user_id: int) -> str:
    rows = conn.execute(
        """SELECT e.id,e.name
        FROM entities e JOIN character_profiles p ON p.entity_id=e.id
        WHERE e.entity_type='character' AND p.status='active'
        ORDER BY e.name"""
    ).fetchall()
    lines = ["🔔 CHARACTER STAT UPDATES", "━━━━━━━━━━━━━━━━━━"]
    if not rows:
        lines.append("No active characters.")
    for row in rows:
        enabled = stat_notifications_enabled(conn, user_id, str(row["id"]))
        lines.append(f"• {row['name']} · {'ON' if enabled else 'OFF'}")
    lines.extend(["", "Use /statnotify <character> on|off."])
    return "\n".join(lines)


def _callback_view(conn, user_id: int, callback_data: str):
    if callback_data == "nav:close":
        return _DELETE_SENTINEL, None
    if callback_data == "nav:real":
        return world_layer_callback_view(conn, callback_data)
    if callback_data == "nav:runtime" or callback_data == "rw:runtime" or callback_data.startswith("rw:rt:"):
        if callback_data.startswith("rw:rt:") and base._user_role(user_id) != "owner":
            return (
                "🔒 Creator authority required for Real World runtime control.",
                [[{"text": "← Real World", "callback_data": "nav:real"}]],
            )
        return world_layer_callback_view(conn, callback_data)
    if callback_data == "nav:sandbox" or callback_data.startswith("sw:"):
        if base._user_role(user_id) != "owner":
            return (
                "🔒 Creator authority required for the Creation Sandbox.",
                [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]],
            )
        if callback_data == "sw:studio" or callback_data.startswith("sw:cs:"):
            return studio_callback_view(conn, user_id, callback_data)
        return world_layer_callback_view(conn, callback_data)
    if callback_data == "nav:universe":
        return universe_view(conn)
    if callback_data == "uni:weather":
        return weather_view(conn)
    if callback_data == "uni:news":
        return news_view(conn)
    if callback_data == "uni:news:generate":
        if base._user_role(user_id) != "owner":
            return (
                "🔒 Creator authority required to generate universe news.",
                [[{"text": "← News", "callback_data": "uni:news"}]],
            )
        return generate_news_view(conn)
    if callback_data == "uni:regions":
        return regions_view(conn)
    if callback_data == "uni:locations":
        return locations_view(conn)
    if callback_data.startswith("region:"):
        return region_view(conn, callback_data.split(":", 1)[1])
    if callback_data.startswith("pref:statnotify:"):
        role = base._user_role(user_id)
        if role == "unauthorized":
            return "Not authorized.", None
        parts = callback_data.split(":", 3)
        if len(parts) != 4 or parts[3] != "toggle":
            return "Unknown notification preference.", [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]]
        character_id = parts[2]
        found = _resolve_character(conn, character_id)
        if found is None:
            return "Unknown character.", [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]]
        character_id, character_name = found
        enabled = not stat_notifications_enabled(conn, user_id, character_id)
        set_stat_notifications(conn, user_id, character_id, enabled)
        text = base._character_view(conn, character_id, role=role)
        text += f"\n\n🔔 Stat updates {'ON' if enabled else 'OFF'} for {character_name}."
        return text, _character_keyboard_with_stat_pref(conn, character_id, user_id)
    if callback_data.startswith("char:"):
        role = base._user_role(user_id)
        if role == "unauthorized":
            return "Not authorized.", None
        character_id = callback_data.split(":", 1)[1]
        return base._character_view(conn, character_id, role=role), _character_keyboard_with_stat_pref(conn, character_id, user_id)
    if callback_data.startswith("inv:"):
        role = base._user_role(user_id)
        if role == "unauthorized":
            return "Not authorized.", None
        view = inventory_callback_view(
            conn,
            callback_data,
            role=role,
            requested_by=f"telegram:{user_id}",
        )
        if view is not None:
            return view
    if callback_data.startswith(("ai:", "af:")):
        if base._user_role(user_id) != "owner":
            return (
                "🔒 Creator authority required for AI settings.",
                [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]],
            )
        return ai_callback_view(conn, user_id, callback_data)
    if callback_data.startswith(("prof:", "psec:")):
        role = base._user_role(user_id)
        if role == "unauthorized":
            return "Not authorized.", None
        view = profile_callback_view(conn, callback_data, role=role)
        if view is not None:
            return view
    return _ORIGINAL_CALLBACK_VIEW(conn, user_id, callback_data)


def _help(role: str) -> str:
    text = _ORIGINAL_HELP(role)
    text = text.replace("\n/pause — Pause autonomy", "")
    text = text.replace("\n/resume — Resume autonomy", "")
    text = text.replace("\n/speed <value> — Set runtime speed", "")
    text += "\n/realstatus — Real World runtime status"
    if role == "owner":
        text += "\n/realpause | /realresume — Real World pause control"
        text += "\n/realspeed <value> — Real World runtime speed"
        text += "\n/realtime <ISO-8601> — Set Real World time; auto-pauses"
        text += "\n/sandboxstatus — Sandbox World runtime status"
        text += "\n/sandboxpause | /sandboxresume — Sandbox pause control"
        text += "\n/sandboxspeed <value> — Sandbox runtime speed"
        text += "\n/sandboxtime <ISO-8601> — Set Sandbox time; auto-pauses"
    text += "\n/statnotify <character> on|off — Character profile/progression updates"
    text += "\n/inventory — Browse universe inventory"
    if role == "owner":
        text += "\n/replenish <stack_id> <quantity> — Add stock with Creator authority"
        text += "\n/settings — Creator settings and AI cognition"
        text += "\n/studio — Open Creator Studio"
        text += "\n/create character|location <name> — Manual sandbox draft"
        text += "\n/createai character|location <description> — AI-assisted sandbox draft"
    return text


def _studio_command_result(conn, user_id: int, command: str, parts: list[str]) -> str | None:
    if command == "/studio":
        return studio_home_view(conn, user_id)[0]
    if command not in {"/create", "/createai"}:
        return None
    if len(parts) < 3 or parts[1].lower() not in {"character", "location"}:
        verb = "name" if command == "/create" else "description"
        return f"Usage: {command} character|location <{verb}>"
    creation_type = parts[1].lower()
    intent = " ".join(parts[2:]).strip()
    try:
        if command == "/create":
            manual_draft(conn, user_id, creation_type, intent)
        else:
            ai_draft(conn, user_id, creation_type, intent)
    except Exception as exc:
        return f"Creator Studio draft rejected: {exc}"
    return draft_preview_view(conn, user_id)[0]


def _ambiguous_runtime_redirect(command: str) -> str:
    action = command.lstrip("/")
    if action == "time":
        return (
            "🌐 World required for time control.\n"
            "Use /realtime <ISO-8601> for Real World or /sandboxtime <ISO-8601> for Sandbox World."
        )
    return (
        "🌐 World required for runtime control.\n"
        f"Use /real{action} for Real World or /sandbox{action} for Sandbox World."
    )


def handle_command(db_path: str | Path, *, user_id: int, text: str) -> str:
    command_line = (text or "").strip()
    parts = command_line.split()
    first = parts[0] if parts else ""
    command = first.split("@", 1)[0].lower()
    role = base._user_role(user_id)

    if command in _AMBIGUOUS_RUNTIME_COMMANDS:
        if role == "unauthorized":
            return "Not authorized. Use /whoami to obtain your Telegram user id."
        return _ambiguous_runtime_redirect(command)

    if command in _REAL_RUNTIME_COMMANDS:
        if role == "unauthorized":
            return "Not authorized. Use /whoami to obtain your Telegram user id."
        if command != "/realstatus" and role != "owner":
            return "🔒 Creator authority required for Real World runtime control."
        with connect(db_path) as conn:
            migrate(conn)
            return handle_real_runtime_command(
                conn,
                command,
                parts[1:],
                requested_by=f"telegram:{user_id}",
            )

    if command in _SANDBOX_RUNTIME_COMMANDS:
        if role != "owner":
            return "🔒 Creator authority required for Sandbox World runtime control."
        with connect(db_path) as conn:
            migrate(conn)
            return handle_sandbox_runtime_command(conn, command, parts[1:])

    if command in {"/inventory", "/replenish", "/statnotify"} and role == "unauthorized":
        return "Not authorized. Use /whoami to obtain your Telegram user id."

    if command in {"/studio", "/create", "/createai"}:
        if role != "owner":
            return "🔒 Creator authority required for Creator Studio."
        with connect(db_path) as conn:
            migrate(conn)
            result = _studio_command_result(conn, user_id, command, parts)
            if result is not None:
                return result

    if command == "/statnotify":
        with connect(db_path) as conn:
            migrate(conn)
            if len(parts) == 1:
                return _statnotify_status(conn, user_id)
            if len(parts) < 3 or parts[-1].lower() not in {"on", "off"}:
                return "Usage: /statnotify <character name or id> on|off"
            character_query = " ".join(parts[1:-1]).strip()
            found = _resolve_character(conn, character_query)
            if found is None:
                return f"Unknown character: {character_query}"
            character_id, character_name = found
            enabled = set_stat_notifications(conn, user_id, character_id, parts[-1].lower() == "on")
            return (
                f"🔔 {character_name} stat updates {'ON' if enabled else 'OFF'}\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "Preference saved. Notification baseline reset to current state; no historical backlog will be replayed."
            )

    if command == "/inventory":
        with connect(db_path) as conn:
            migrate(conn)
            return inventory_command_view(conn)

    if command == "/replenish":
        if role != "owner":
            return "🔒 Creator authority required for inventory replenishment."
        if len(parts) != 3:
            return "Usage: /replenish <stack_id> <positive_quantity>"
        stack_id = parts[1]
        try:
            amount = float(parts[2])
        except ValueError:
            return "Replenishment quantity must be numeric."
        try:
            with connect(db_path) as conn:
                migrate(conn)
                result = replenish_inventory_stack(
                    conn,
                    stack_id,
                    amount,
                    authority="creator",
                    requested_by=f"telegram:{user_id}",
                )
        except (KeyError, ValueError, RuntimeError) as exc:
            return f"Inventory replenishment rejected: {exc}"
        return (
            "✅ INVENTORY REPLENISHED\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"🧺 {result['item_name']}\n"
            f"➕ Added {result['added_quantity']:g} {result['unit']}\n"
            f"📏 Before {result['before_quantity']:g} {result['unit']}\n"
            f"📏 After {result['after_quantity']:g} {result['unit']}\n"
            "Audit event recorded."
        )

    if command in {"/settings", "/ai"}:
        if role == "unauthorized":
            return "Not authorized. Use /whoami to obtain your Telegram user id."
        if role != "owner":
            return "🔒 Creator authority required for AI settings."
        with connect(db_path) as conn:
            migrate(conn)
            text_value, _ = ai_home_view(conn)
            return text_value

    reply = _ORIGINAL_HANDLE_COMMAND(db_path, user_id=user_id, text=text)
    if command in {"/notify", "/notification", "/notifications", "/notion/on", "/notion/off"}:
        explicit_toggle = (
            command in {"/notion/on", "/notion/off"}
            or (len(parts) >= 2 and parts[1].lower() in {"on", "off"})
        )
        if explicit_toggle:
            with connect(db_path) as conn:
                migrate(conn)
                reset_all_stat_notification_baselines(conn, user_id)
    return reply


def _command_keyboard(command: str):
    if command in _REAL_RUNTIME_COMMANDS:
        return [
            [{"text": "🕒 Real World Runtime", "callback_data": "nav:runtime"}],
            [{"text": "← Real World", "callback_data": "nav:real"}],
        ]
    if command in _SANDBOX_RUNTIME_COMMANDS:
        return [
            [{"text": "🕒 Sandbox Runtime", "callback_data": "sw:runtime"}],
            [{"text": "← Sandbox World", "callback_data": "nav:sandbox"}],
        ]
    if command == "/inventory":
        return [
            [
                {"text": "📍 Locations", "callback_data": "inv:list:locations:0"},
                {"text": "👥 Characters", "callback_data": "inv:list:characters:0"},
            ],
            [
                {"text": "📦 Containers", "callback_data": "inv:list:containers:0"},
                {"text": "🧺 All Stocks", "callback_data": "inv:all:0"},
            ],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ]
    if command in {"/studio", "/create", "/createai"}:
        return [
            [{"text": "📋 Preview Draft", "callback_data": "sw:cs:preview"}],
            [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
            [{"text": "← Sandbox World", "callback_data": "nav:sandbox"}],
        ]
    if command in {"/settings", "/ai"}:
        return [
            [{"text": "🧠 Primary Cognition", "callback_data": "ai:providers"}],
            [{"text": "🛟 Fallback Model", "callback_data": "af:providers"}],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ]
    return _ORIGINAL_COMMAND_KEYBOARD(command)


# Install bounded Creator extensions into the existing polling loop. Telegram
# remains an adapter; inventory/provider/fallback/profile-change semantics live
# in reusable services, while message deletion is presentation lifecycle only.
base._api = _api
base._send = _send
base._edit = _edit
base._home_message = _home_message
base._home_keyboard = _home_keyboard
base._character_keyboard_for_user = _character_keyboard_for_user
base._callback_view = _callback_view
base._help = _help
base.handle_command = handle_command
base._command_keyboard = _command_keyboard

run_polling = base.run_polling
from __future__ import annotations

import json
import os
import urllib.error
from datetime import datetime, timedelta
from typing import Any

from .simulation import runtime_value, set_runtime_value
from .telegram_bot import (
    _allowed_user_ids,
    _fmt_time,
    _notifications_enabled,
    _owner_user_id,
    _send,
    _title_action,
)

LAST_ACTION_NOTIFY_PREFIX = "telegram_last_action_notification:"


def _fmt_delta(label: str, icon: str, before: float, after: float, *, high_is_good: bool) -> str | None:
    delta = float(after) - float(before)
    if abs(delta) < 0.05:
        return None
    direction = "▲" if delta > 0 else "▼"
    beneficial = delta > 0 if high_is_good else delta < 0
    marker = "✓" if beneficial else "•"
    return f"{icon} {label:<11} {before:.1f} → {after:.1f}  {direction}{abs(delta):.1f} {marker}"


def _fmt_number(value: int | float) -> str:
    number = float(value)
    if abs(number - round(number)) < 1e-9:
        return str(int(round(number)))
    return f"{number:.2f}".rstrip("0").rstrip(".")


def _entity_name(conn, entity_id: str | None) -> str | None:
    if not entity_id:
        return None
    row = conn.execute("SELECT name FROM entities WHERE id=?", (entity_id,)).fetchone()
    return str(row["name"]) if row else None


def _action_title(action: dict[str, Any]) -> str:
    title = _title_action(action.get("action"))
    target = action.get("target_name") or action.get("target")
    if target:
        title += f" → {target}"
    return title


def _wall_wait_text(duration_minutes: int | float, speed: float) -> str:
    wall_seconds = max(0.0, float(duration_minutes) * 60.0 / max(float(speed), 0.000001))
    if wall_seconds < 60:
        return f"~{max(1, round(wall_seconds))} sec real"
    wall_minutes = wall_seconds / 60.0
    if wall_minutes < 90:
        value = round(wall_minutes, 1) if abs(wall_minutes - round(wall_minutes)) >= 0.05 else int(round(wall_minutes))
        return f"~{value} min real"
    wall_hours = wall_minutes / 60.0
    value = round(wall_hours, 1) if abs(wall_hours - round(wall_hours)) >= 0.05 else int(round(wall_hours))
    return f"~{value} hr real"


def _duration_line(action: dict[str, Any], *, completed: bool) -> str | None:
    duration = action.get("duration_minutes")
    if duration is None:
        return None
    speed = float(action.get("speed_at_plan") or 1.0)
    prefix = "Took" if completed else "Duration"
    return f"⏱ {prefix} {int(duration)} sim min • {_wall_wait_text(int(duration), speed)} @ {speed:g}x"


def _expected_end_sim_time(action: dict[str, Any]) -> str | None:
    planned = action.get("planned_sim_time")
    duration = action.get("duration_minutes")
    if not planned or duration is None:
        return None
    try:
        return (datetime.fromisoformat(str(planned)) + timedelta(minutes=int(duration))).isoformat()
    except (TypeError, ValueError):
        return None


def _meal_lines(action: dict[str, Any]) -> list[str]:
    nutrition = action.get("nutrition_intake")
    if not isinstance(nutrition, dict) or nutrition.get("source") != "eating-behavior-v1":
        return []
    items = nutrition.get("items")
    lines = ["", "🍽 Meal"]
    if isinstance(items, list):
        for item in items:
            if not isinstance(item, dict):
                continue
            name = item.get("item_name") or item.get("definition_id") or "Food"
            quantity = item.get("quantity")
            unit = item.get("unit")
            if isinstance(quantity, (int, float)) and isinstance(unit, str):
                lines.append(f"• {name} · {_fmt_number(quantity)} {unit}")
    lines.append(
        "🔥 "
        f"{_fmt_number(float(nutrition.get('energy_kcal', 0.0)))} kcal · "
        f"P {_fmt_number(float(nutrition.get('protein_g', 0.0)))} g · "
        f"C {_fmt_number(float(nutrition.get('carbohydrate_g', 0.0)))} g · "
        f"F {_fmt_number(float(nutrition.get('fat_g', 0.0)))} g"
    )
    return lines


def format_action_completion(
    action: dict[str, Any],
    before: dict[str, Any],
    after: dict[str, Any],
    *,
    actor_name: str | None = None,
    next_action: dict[str, Any] | None = None,
) -> str:
    display_actor = actor_name or after.get("actor_name") or after.get("actor_id") or "Character"
    lines = [
        "✨ CHARACTER UPDATE",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {display_actor}",
        f"🎬 {_action_title(action)}",
        f"🕒 {_fmt_time(after.get('sim_time'))}",
    ]
    duration_line = _duration_line(action, completed=True)
    if duration_line:
        lines.append(duration_line)

    if action.get("reason"):
        lines.extend(["", f"💭 {action['reason']}"])

    if before.get("location_name") != after.get("location_name"):
        lines.extend(["", f"📍 {before.get('location_name', 'Unknown')} → {after.get('location_name', 'Unknown')}"])
    else:
        lines.extend(["", f"📍 {after.get('location_name', 'Unknown')}"])

    lines.extend(_meal_lines(action))

    fatigue_change = None
    if "fatigue" in before and "fatigue" in after:
        fatigue_change = _fmt_delta("Fatigue", "💢", before["fatigue"], after["fatigue"], high_is_good=False)

    changes = [
        _fmt_delta("Energy", "⚡", before["energy"], after["energy"], high_is_good=True),
        fatigue_change,
        _fmt_delta("Hunger", "🍽", before["hunger"], after["hunger"], high_is_good=False),
        _fmt_delta("Thirst", "💧", before["thirst"], after["thirst"], high_is_good=False),
        _fmt_delta("Sleepiness", "🌙", before["sleepiness"], after["sleepiness"], high_is_good=False),
        _fmt_delta("Cleanliness", "🫧", before["cleanliness"], after["cleanliness"], high_is_good=True),
    ]
    visible_changes = [row for row in changes if row]
    if visible_changes:
        lines.extend(["", "📊 Changes", *visible_changes])

    if next_action:
        lines.extend(["", f"⏭ Next: {_action_title(next_action)}"])
        if next_action.get("reason"):
            lines.append(f"💭 {next_action['reason']}")
        next_duration = _duration_line(next_action, completed=False)
        expected_sim = _expected_end_sim_time(next_action)
        if next_duration:
            lines.append(next_duration)
        if expected_sim:
            lines.append(f"⏳ Expected update: {_fmt_time(expected_sim)}")

    return "\n".join(lines)


def _completion_nutrition(conn, action_id: str) -> dict[str, Any] | None:
    row = conn.execute(
        "SELECT payload_json FROM events WHERE action_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
        (action_id,),
    ).fetchone()
    if row is None:
        return None
    payload = json.loads(row["payload_json"] or "{}")
    nutrition = payload.get("nutrition_intake")
    if not isinstance(nutrition, dict) or nutrition.get("source") != "eating-behavior-v1":
        return None
    enriched = dict(nutrition)
    items: list[dict[str, Any]] = []
    for raw in nutrition.get("items") or []:
        if not isinstance(raw, dict):
            continue
        item = dict(raw)
        item_name = _entity_name(conn, str(item.get("stack_id") or ""))
        if item_name:
            item["item_name"] = item_name
        items.append(item)
    enriched["items"] = items
    return enriched


def dispatch_action_completion(
    conn,
    *,
    action_id: str,
    action: dict[str, Any],
    before: dict[str, Any],
    after: dict[str, Any],
    next_action: dict[str, Any] | None = None,
) -> int:
    """Best-effort proactive push after a committed action completion."""
    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return 0

    recipients = set(_allowed_user_ids())
    owner_id = _owner_user_id()
    if owner_id is not None:
        recipients.add(owner_id)

    display_action = dict(action)
    target_name = _entity_name(conn, action.get("target"))
    if target_name:
        display_action["target_name"] = target_name
    nutrition = _completion_nutrition(conn, action_id)
    if nutrition is not None:
        display_action["nutrition_intake"] = nutrition

    display_next = None
    if next_action:
        display_next = dict(next_action)
        next_target_name = _entity_name(conn, next_action.get("target"))
        if next_target_name:
            display_next["target_name"] = next_target_name

    actor_id = str(after.get("actor_id") or before.get("actor_id") or "") or None
    actor_name = _entity_name(conn, actor_id)
    message = format_action_completion(
        display_action,
        before,
        after,
        actor_name=actor_name,
        next_action=display_next,
    )

    sent = 0
    for user_id in sorted(recipients):
        if not _notifications_enabled(conn, user_id):
            continue
        key = f"{LAST_ACTION_NOTIFY_PREFIX}{user_id}"
        if runtime_value(conn, key, None) == action_id:
            continue
        try:
            _send(token, user_id, message)
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
            continue
        set_runtime_value(conn, key, action_id)
        conn.commit()
        sent += 1
    return sent
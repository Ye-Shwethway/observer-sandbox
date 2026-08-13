from __future__ import annotations

import os
import urllib.error
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


def _entity_name(conn, entity_id: str | None) -> str | None:
    if not entity_id:
        return None
    row = conn.execute("SELECT name FROM entities WHERE id=?", (entity_id,)).fetchone()
    return str(row["name"]) if row else None


def format_action_completion(
    action: dict[str, Any],
    before: dict[str, Any],
    after: dict[str, Any],
    *,
    actor_name: str | None = None,
) -> str:
    title = _title_action(action.get("action"))
    target = action.get("target_name") or action.get("target")
    if target:
        title += f" → {target}"

    display_actor = actor_name or after.get("actor_name") or after.get("actor_id") or "Character"
    lines = [
        "✨ CHARACTER UPDATE",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {display_actor}",
        f"🎬 {title}",
        f"🕒 {_fmt_time(after.get('sim_time'))}",
    ]
    if action.get("reason"):
        lines.extend(["", f"💭 {action['reason']}"])

    if before.get("location_name") != after.get("location_name"):
        lines.extend(["", f"📍 {before.get('location_name', 'Unknown')} → {after.get('location_name', 'Unknown')}"])
    else:
        lines.extend(["", f"📍 {after.get('location_name', 'Unknown')}"])

    changes = [
        _fmt_delta("Energy", "⚡", before["energy"], after["energy"], high_is_good=True),
        _fmt_delta("Hunger", "🍽", before["hunger"], after["hunger"], high_is_good=False),
        _fmt_delta("Thirst", "💧", before["thirst"], after["thirst"], high_is_good=False),
        _fmt_delta("Sleepiness", "🌙", before["sleepiness"], after["sleepiness"], high_is_good=False),
        _fmt_delta("Cleanliness", "🫧", before["cleanliness"], after["cleanliness"], high_is_good=True),
    ]
    visible_changes = [row for row in changes if row]
    if visible_changes:
        lines.extend(["", "📊 Changes", *visible_changes])
    return "\n".join(lines)


def dispatch_action_completion(
    conn,
    *,
    action_id: str,
    action: dict[str, Any],
    before: dict[str, Any],
    after: dict[str, Any],
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
    actor_id = str(after.get("actor_id") or before.get("actor_id") or "") or None
    actor_name = _entity_name(conn, actor_id)
    message = format_action_completion(display_action, before, after, actor_name=actor_name)

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

from __future__ import annotations

import os
import sqlite3
import time
import urllib.error
from typing import Any

from .profile_change_observer import (
    mark_stat_notification_sent,
    pending_stat_notification_changes,
    stat_notifications_enabled,
)
from .simulation import runtime_value, set_runtime_value
from .telegram_bot import _allowed_user_ids, _fmt_time, _notifications_enabled, _owner_user_id, _send

STAT_LAST_SENT_PREFIX = "telegram_stat_notification_last_sent_wall:"
STAT_NOTIFICATION_COOLDOWN_SECONDS = 300.0


def _entity_name(conn: sqlite3.Connection, actor_id: str) -> str:
    row = conn.execute("SELECT name FROM entities WHERE id=?", (actor_id,)).fetchone()
    return str(row["name"]) if row else actor_id


def _fmt_value(value: float, unit: str | None) -> str:
    number = float(value)
    if unit == "in":
        return f'{number:.2f}"'
    if unit == "lb":
        return f"{number:.2f} lb"
    if unit == "percent":
        return f"{number:.2f}%"
    if unit == "ratio":
        return f"{number:.3f}"
    return f"{number:.2f}".rstrip("0").rstrip(".")


def _grade_code(grade: Any) -> str | None:
    return str(grade.get("grade")) if isinstance(grade, dict) and grade.get("grade") else None


def _change_line(change: dict[str, Any]) -> str:
    delta = float(change.get("delta") or 0.0)
    direction = "▲" if delta > 0 else "▼" if delta < 0 else "•"
    beneficial = change.get("beneficial")
    quality = "🟢" if beneficial is True else "🔴" if beneficial is False else ""
    unit = change.get("unit")
    before = _fmt_value(float(change["before"]), unit)
    after = _fmt_value(float(change["after"]), unit)
    delta_text = _fmt_value(abs(delta), unit)
    line = f"• {quality}{direction} {change['label']}  {before} → {after}  {direction}{delta_text}"
    if change.get("grade_changed"):
        old_code = _grade_code(change.get("old_grade")) or "—"
        new_code = _grade_code(change.get("new_grade")) or "—"
        line += f"  · {old_code}→{new_code}"
    return line


def format_profile_change_notification(actor_name: str, sim_time: str, changes: list[dict[str, Any]]) -> str:
    lines = [
        "📈 CHARACTER PROGRESSION",
        "━━━━━━━━━━━━━━━━━━",
        f"👤 {actor_name}",
        f"🕒 {_fmt_time(sim_time)}",
        "",
    ]
    visible = changes[:12]
    lines.extend(_change_line(change) for change in visible)
    if len(changes) > len(visible):
        lines.append(f"• …and {len(changes) - len(visible)} more meaningful changes")
    return "\n".join(lines)


def _cooldown_key(user_id: int, actor_id: str) -> str:
    return f"{STAT_LAST_SENT_PREFIX}{user_id}:{actor_id}"


def _cooldown_allows(
    conn: sqlite3.Connection,
    user_id: int,
    actor_id: str,
    changes: list[dict[str, Any]],
    *,
    now_wall: float,
) -> bool:
    if any(bool(change.get("grade_changed")) for change in changes):
        return True
    last = runtime_value(conn, _cooldown_key(user_id, actor_id), None)
    if not isinstance(last, (int, float)):
        return True
    return now_wall - float(last) >= STAT_NOTIFICATION_COOLDOWN_SECONDS


def _is_grade_only_recalibration(change: dict[str, Any]) -> bool:
    """Observer grading changes are not character progression without raw state change."""
    if not bool(change.get("grade_changed")):
        return False
    try:
        return abs(float(change.get("after")) - float(change.get("before"))) <= 1e-12
    except (TypeError, ValueError):
        return False


def dispatch_profile_change_notifications(
    conn: sqlite3.Connection,
    *,
    actor_id: str,
    before: dict[str, dict[str, Any]],
    current: dict[str, dict[str, Any]],
    sim_time: str,
    now_wall: float | None = None,
) -> int:
    """Send at most one aggregated, debounced profile-change message per recipient."""
    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return 0

    recipients = set(_allowed_user_ids())
    owner_id = _owner_user_id()
    if owner_id is not None:
        recipients.add(owner_id)
    actor_name = _entity_name(conn, actor_id)
    sent = 0
    wall_time = time.time() if now_wall is None else float(now_wall)

    for user_id in sorted(recipients):
        if not _notifications_enabled(conn, user_id):
            continue
        if not stat_notifications_enabled(conn, user_id, actor_id):
            continue
        raw_changes = pending_stat_notification_changes(
            conn,
            user_id,
            actor_id,
            before,
            current,
            sim_time=sim_time,
        )
        grade_only = [change for change in raw_changes if _is_grade_only_recalibration(change)]
        if grade_only:
            # Consume the observer-only baseline drift so a grading-rule rollout
            # does not repeatedly appear as pending character progression.
            mark_stat_notification_sent(conn, user_id, actor_id, current, grade_only)
        changes = [change for change in raw_changes if not _is_grade_only_recalibration(change)]
        if not changes or not _cooldown_allows(conn, user_id, actor_id, changes, now_wall=wall_time):
            continue
        message = format_profile_change_notification(actor_name, sim_time, changes)
        try:
            _send(token, user_id, message)
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
            continue
        mark_stat_notification_sent(conn, user_id, actor_id, current, changes)
        set_runtime_value(conn, _cooldown_key(user_id, actor_id), wall_time)
        conn.commit()
        sent += 1
    return sent
from __future__ import annotations

import json
import os
import sqlite3
import urllib.error
from typing import Any, Callable

from .creation_sandbox import DEFAULT_SANDBOX_ID, ensure_sandbox, get_sandbox_object

_OBSERVED_EVENT_TYPES = {
    "sandbox_object_activated",
    "sandbox_object_archived",
    "sandbox_object_deleted",
    "sandbox_relation_bound",
    "sandbox_ai_bound",
    "sandbox_runtime_options_changed",
    "sandbox_clock_configured",
    "sandbox_speed_changed",
    "sandbox_paused",
    "sandbox_resumed",
    "sandbox_reset",
}

_LABELS = {
    "sandbox_object_activated": "Creation approved",
    "sandbox_object_archived": "Creation archived",
    "sandbox_object_deleted": "Creation deleted",
    "sandbox_relation_bound": "Sandbox relation changed",
    "sandbox_ai_bound": "Character AI assigned",
    "sandbox_runtime_options_changed": "Runtime options changed",
    "sandbox_clock_configured": "Sandbox clock configured",
    "sandbox_speed_changed": "Sandbox speed changed",
    "sandbox_paused": "Sandbox paused",
    "sandbox_resumed": "Sandbox resumed",
    "sandbox_reset": "Sandbox reset",
}


def _json(value: str | None) -> dict[str, Any]:
    try:
        loaded = json.loads(value or "{}")
    except json.JSONDecodeError:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _current_event_id(conn: sqlite3.Connection, sandbox_id: str = DEFAULT_SANDBOX_ID) -> int:
    row = conn.execute(
        "SELECT COALESCE(MAX(id),0) AS event_id FROM creation_sandbox_events WHERE sandbox_id=?",
        (sandbox_id,),
    ).fetchone()
    return int(row["event_id"] if row else 0)


def _ensure_state(conn: sqlite3.Connection, user_id: int, sandbox_id: str = DEFAULT_SANDBOX_ID) -> dict[str, Any]:
    ensure_sandbox(conn, sandbox_id)
    baseline = _current_event_id(conn, sandbox_id)
    conn.execute(
        """
        INSERT INTO creation_sandbox_notification_state(sandbox_id,user_id,enabled,last_event_id)
        VALUES(?,?,0,?)
        ON CONFLICT(sandbox_id,user_id) DO NOTHING
        """,
        (sandbox_id, int(user_id), baseline),
    )
    conn.commit()
    row = conn.execute(
        "SELECT sandbox_id,user_id,enabled,last_event_id,updated_at FROM creation_sandbox_notification_state WHERE sandbox_id=? AND user_id=?",
        (sandbox_id, int(user_id)),
    ).fetchone()
    return dict(row) if row else {"enabled": 0, "last_event_id": baseline}


def sandbox_notifications_enabled(conn: sqlite3.Connection, user_id: int) -> bool:
    return bool(_ensure_state(conn, user_id)["enabled"])


def set_sandbox_notifications(conn: sqlite3.Connection, user_id: int, enabled: bool) -> bool:
    current = _ensure_state(conn, user_id)
    baseline = _current_event_id(conn) if enabled and not bool(current["enabled"]) else int(current["last_event_id"])
    conn.execute(
        """
        UPDATE creation_sandbox_notification_state
        SET enabled=?,last_event_id=?,updated_at=CURRENT_TIMESTAMP
        WHERE sandbox_id=? AND user_id=?
        """,
        (int(bool(enabled)), baseline, DEFAULT_SANDBOX_ID, int(user_id)),
    )
    conn.commit()
    return bool(enabled)


def _event_name(conn: sqlite3.Connection, object_id: str | None) -> str | None:
    if not object_id:
        return None
    try:
        obj = get_sandbox_object(conn, object_id)
    except Exception:
        return object_id
    return str(obj["identity"].get("name") or object_id)


def pending_sandbox_events(conn: sqlite3.Connection, user_id: int, *, limit: int = 12) -> list[dict[str, Any]]:
    state = _ensure_state(conn, user_id)
    placeholders = ",".join("?" for _ in _OBSERVED_EVENT_TYPES)
    rows = conn.execute(
        f"""
        SELECT id,object_id,event_type,payload_json,created_at
        FROM creation_sandbox_events
        WHERE sandbox_id=? AND id>? AND event_type IN ({placeholders})
        ORDER BY id ASC LIMIT ?
        """,
        (DEFAULT_SANDBOX_ID, int(state["last_event_id"]), *sorted(_OBSERVED_EVENT_TYPES), int(limit)),
    ).fetchall()
    return [
        {
            "id": int(row["id"]),
            "object_id": row["object_id"],
            "event_type": str(row["event_type"]),
            "payload": _json(row["payload_json"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]


def mark_sandbox_events_seen(conn: sqlite3.Connection, user_id: int, event_id: int) -> None:
    _ensure_state(conn, user_id)
    conn.execute(
        """
        UPDATE creation_sandbox_notification_state
        SET last_event_id=CASE WHEN last_event_id<? THEN ? ELSE last_event_id END,updated_at=CURRENT_TIMESTAMP
        WHERE sandbox_id=? AND user_id=?
        """,
        (int(event_id), int(event_id), DEFAULT_SANDBOX_ID, int(user_id)),
    )
    conn.commit()


def _event_line(conn: sqlite3.Connection, event: dict[str, Any]) -> str:
    label = _LABELS.get(event["event_type"], event["event_type"].replace("_", " ").title())
    name = _event_name(conn, event.get("object_id"))
    payload = event.get("payload") or {}
    detail = ""
    if event["event_type"] == "sandbox_ai_bound":
        detail = f"{payload.get('provider_id', '')}/{payload.get('model_id', '')}".strip("/")
    elif event["event_type"] == "sandbox_runtime_options_changed":
        detail = f"{payload.get('count', 0)} options"
    elif event["event_type"] == "sandbox_speed_changed":
        detail = f"{payload.get('speed', '?')}x"
    elif event["event_type"] == "sandbox_relation_bound":
        detail = str(payload.get("relation_type") or "")
    target = f" · {name}" if name else ""
    suffix = f" · {detail}" if detail else ""
    return f"• {label}{target}{suffix}"


def format_sandbox_notification(conn: sqlite3.Connection, events: list[dict[str, Any]]) -> str:
    lines = ["🧪 SANDBOX UPDATE", "━━━━━━━━━━━━━━━━━━"]
    lines.extend(_event_line(conn, event) for event in events)
    lines.extend(["", "Creation Sandbox only · Real World unchanged."])
    return "\n".join(lines)


def sandbox_notification_view(conn: sqlite3.Connection, user_id: int) -> tuple[str, list[list[dict[str, str]]]]:
    enabled = sandbox_notifications_enabled(conn, user_id)
    recent = conn.execute(
        """
        SELECT id,object_id,event_type,payload_json,created_at
        FROM creation_sandbox_events
        WHERE sandbox_id=?
        ORDER BY id DESC LIMIT 8
        """,
        (DEFAULT_SANDBOX_ID,),
    ).fetchall()
    lines = [
        "📡 SANDBOX OBSERVER",
        "━━━━━━━━━━━━━━━━━━",
        f"🔔 Proactive updates: {'ON' if enabled else 'OFF'}",
        "",
        "Observed events are sandbox lifecycle/config/runtime-control facts only.",
        "No autonomous activity is invented.",
    ]
    if recent:
        lines.extend(["", "Recent sandbox events"])
        for row in reversed(recent):
            lines.append(_event_line(conn, {
                "event_type": str(row["event_type"]),
                "object_id": row["object_id"],
                "payload": _json(row["payload_json"]),
            }))
    keyboard = [
        [{"text": f"🔔 Updates: {'ON' if enabled else 'OFF'}", "callback_data": "sw:notif:toggle"}],
        [{"text": "✓ Mark Current Seen", "callback_data": "sw:notif:seen"}],
        [{"text": "← Sandbox World", "callback_data": "nav:sandbox"}],
    ]
    return "\n".join(lines), keyboard


def sandbox_notification_callback_view(conn: sqlite3.Connection, user_id: int, callback_data: str):
    if callback_data == "sw:notif":
        return sandbox_notification_view(conn, user_id)
    if callback_data == "sw:notif:toggle":
        set_sandbox_notifications(conn, user_id, not sandbox_notifications_enabled(conn, user_id))
        return sandbox_notification_view(conn, user_id)
    if callback_data == "sw:notif:seen":
        mark_sandbox_events_seen(conn, user_id, _current_event_id(conn))
        return sandbox_notification_view(conn, user_id)
    raise KeyError(callback_data)


def dispatch_pending_sandbox_notifications(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    send: Callable[[int, str], None],
) -> int:
    if not sandbox_notifications_enabled(conn, user_id):
        return 0
    events = pending_sandbox_events(conn, user_id)
    if not events:
        return 0
    send(int(user_id), format_sandbox_notification(conn, events))
    mark_sandbox_events_seen(conn, user_id, events[-1]["id"])
    return len(events)


def dispatch_owner_sandbox_notifications(conn: sqlite3.Connection) -> int:
    """Transport adapter for the runtime service; event selection remains sandbox-owned."""
    from .telegram_bot import _notifications_enabled, _owner_user_id, _send

    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    owner_id = _owner_user_id()
    if not token or owner_id is None or not _notifications_enabled(conn, owner_id):
        return 0
    try:
        return dispatch_pending_sandbox_notifications(
            conn,
            owner_id,
            send=lambda user_id, text: _send(token, user_id, text),
        )
    except (urllib.error.URLError, TimeoutError, RuntimeError, OSError, ValueError):
        return 0


__all__ = [
    "dispatch_owner_sandbox_notifications",
    "dispatch_pending_sandbox_notifications",
    "format_sandbox_notification",
    "mark_sandbox_events_seen",
    "pending_sandbox_events",
    "sandbox_notification_callback_view",
    "sandbox_notification_view",
    "sandbox_notifications_enabled",
    "set_sandbox_notifications",
]

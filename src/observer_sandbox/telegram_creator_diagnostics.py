from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from .creator_diagnostics import relocate_character_for_diagnostic
from .simulation import runtime_value, set_runtime_value

PAGE_SIZE = 8
CANDIDATE_PREFIX = "telegram_creator_diag_move:"


def _key(user_id: int) -> str:
    return f"{CANDIDATE_PREFIX}{user_id}"


def _candidate(conn, user_id: int) -> dict[str, Any] | None:
    value = runtime_value(conn, _key(user_id), None)
    return dict(value) if isinstance(value, dict) else None


def _save(conn, user_id: int, value: dict[str, Any] | None) -> None:
    set_runtime_value(conn, _key(user_id), value)
    conn.commit()


def _characters(conn):
    return conn.execute(
        """SELECT e.id,e.name
        FROM entities e JOIN character_profiles p ON p.entity_id=e.id
        WHERE e.entity_type='character' AND p.status='active'
        ORDER BY e.name,e.id"""
    ).fetchall()


def _locations(conn):
    return conn.execute(
        "SELECT id,name FROM entities WHERE entity_type='location' ORDER BY name,id"
    ).fetchall()


def _current_time(conn) -> datetime:
    value = runtime_value(conn, "sim_time", None)
    if not isinstance(value, str) or not value:
        raise RuntimeError("Simulation time is not initialized")
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise RuntimeError("Simulation time must include a timezone offset")
    return parsed


def _home():
    return (
        "🧪 CREATOR DIAGNOSTICS\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Administrative controls for controlled runtime experiments.\n\n"
        "Character Relocation can move a character to any represented location while preserving time, or optionally move the universe clock forward too. Confirming a relocation cancels that character's pending action and records an audit event.",
        [
            [{"text": "📍 Move Character", "callback_data": "diag:move"}],
            [{"text": "← Creator Settings", "callback_data": "ai:home"}],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ],
    )


def _character_view(conn, user_id: int):
    rows = _characters(conn)
    lines = ["📍 DIAGNOSTIC RELOCATION", "━━━━━━━━━━━━━━━━━━", "Select a character:"]
    keyboard: list[list[dict[str, str]]] = []
    for index, row in enumerate(rows):
        keyboard.append([{"text": f"👤 {row['name']}", "callback_data": f"diag:c:{index}"}])
    if not rows:
        lines.append("No active characters.")
    keyboard.extend([
        [{"text": "← Diagnostics", "callback_data": "diag:home"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _location_view(conn, user_id: int, page: int):
    candidate = _candidate(conn, user_id)
    if not candidate or not candidate.get("actor_id"):
        return _character_view(conn, user_id)
    rows = _locations(conn)
    pages = max(1, (len(rows) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(int(page), pages - 1))
    start = page * PAGE_SIZE
    visible = rows[start : start + PAGE_SIZE]
    lines = [
        "📍 SELECT TARGET LOCATION",
        "━━━━━━━━━━━━━━━━━━",
        f"Character: {candidate.get('actor_name')}",
        f"Page {page + 1}/{pages}",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for offset, row in enumerate(visible):
        index = start + offset
        label = str(row["name"])
        if len(label) > 44:
            label = label[:41] + "…"
        keyboard.append([{"text": f"📌 {label}", "callback_data": f"diag:l:{index}"}])
    nav: list[dict[str, str]] = []
    if page > 0:
        nav.append({"text": "◀️", "callback_data": f"diag:lp:{page - 1}"})
    if page + 1 < pages:
        nav.append({"text": "▶️", "callback_data": f"diag:lp:{page + 1}"})
    if nav:
        keyboard.append(nav)
    keyboard.extend([
        [{"text": "← Character", "callback_data": "diag:move"}],
        [{"text": "✕ Cancel", "callback_data": "diag:cancel"}],
    ])
    return "\n".join(lines), keyboard


def _time_view(conn, user_id: int):
    candidate = _candidate(conn, user_id)
    if not candidate or not candidate.get("location_id"):
        return _location_view(conn, user_id, 0)
    current = _current_time(conn)
    proposed = datetime.fromisoformat(str(candidate.get("proposed_time") or current.isoformat()))
    lines = [
        "🕒 DIAGNOSTIC TIME",
        "━━━━━━━━━━━━━━━━━━",
        f"Character: {candidate.get('actor_name')}",
        f"Location: {candidate.get('location_name')}",
        f"Current universe time: {current.isoformat()}",
        f"Proposed time: {proposed.isoformat()}",
        "",
        "Keep Time changes location only. Adjust Time performs a raw forward clock jump; elapsed sleep/actions/history are NOT synthesized.",
    ]
    return "\n".join(lines), [
        [{"text": "✅ Keep Current Time", "callback_data": "diag:t:keep"}],
        [
            {"text": "−1h", "callback_data": "diag:t:-1h"},
            {"text": "+1h", "callback_data": "diag:t:+1h"},
            {"text": "+6h", "callback_data": "diag:t:+6h"},
        ],
        [
            {"text": "06:00", "callback_data": "diag:t:06"},
            {"text": "12:00", "callback_data": "diag:t:12"},
            {"text": "18:00", "callback_data": "diag:t:18"},
            {"text": "23:00", "callback_data": "diag:t:23"},
        ],
        [
            {"text": "+1 day", "callback_data": "diag:t:+1d"},
            {"text": "Use Proposed Time", "callback_data": "diag:t:use"},
        ],
        [{"text": "← Location", "callback_data": "diag:lp:0"}],
        [{"text": "✕ Cancel", "callback_data": "diag:cancel"}],
    ]


def _review(conn, user_id: int):
    candidate = _candidate(conn, user_id)
    if not candidate or not candidate.get("actor_id") or not candidate.get("location_id"):
        return _character_view(conn, user_id)
    raw_time = candidate.get("sim_time")
    lines = [
        "⚠️ REVIEW CREATOR RELOCATION",
        "━━━━━━━━━━━━━━━━━━",
        f"Character: {candidate.get('actor_name')} ({candidate.get('actor_id')})",
        f"Target: {candidate.get('location_name')} ({candidate.get('location_id')})",
        f"Time: {'Preserve current universe time' if raw_time is None else str(raw_time)}",
        "",
        "Confirming cancels any pending action for this character, sets current action to idle, clears retry/lease state, wakes autonomy, and records creator_diagnostic_relocation.",
    ]
    if raw_time is not None:
        lines.extend([
            "",
            "⚠️ RAW TIME JUMP: the universe clock moves forward immediately. No sleep, meals, movement, physiology events, or other elapsed history are invented for the skipped interval.",
        ])
    return "\n".join(lines), [
        [{"text": "✅ Confirm Relocation", "callback_data": "diag:confirm"}],
        [{"text": "← Time", "callback_data": "diag:time"}],
        [{"text": "✕ Cancel", "callback_data": "diag:cancel"}],
    ]


def _adjust_time(conn, user_id: int, action: str):
    candidate = _candidate(conn, user_id)
    if not candidate:
        return _character_view(conn, user_id)
    current = _current_time(conn)
    proposed = datetime.fromisoformat(str(candidate.get("proposed_time") or current.isoformat()))
    if action == "+1h":
        proposed += timedelta(hours=1)
    elif action == "+6h":
        proposed += timedelta(hours=6)
    elif action == "+1d":
        proposed += timedelta(days=1)
    elif action == "-1h":
        proposed = max(current, proposed - timedelta(hours=1))
    elif action in {"06", "12", "18", "23"}:
        hour = int(action)
        target = proposed.replace(hour=hour, minute=0, second=0, microsecond=0)
        if target < current:
            target += timedelta(days=1)
        proposed = target
    candidate["proposed_time"] = proposed.isoformat()
    _save(conn, user_id, candidate)
    return _time_view(conn, user_id)


def callback_view(conn, user_id: int, callback_data: str, *, requested_by: str):
    if callback_data == "diag:home":
        return _home()
    if callback_data == "diag:move":
        _save(conn, user_id, None)
        return _character_view(conn, user_id)
    if callback_data == "diag:cancel":
        _save(conn, user_id, None)
        return _home()
    if callback_data.startswith("diag:c:"):
        try:
            index = int(callback_data.split(":", 2)[2])
        except ValueError:
            return _character_view(conn, user_id)
        rows = _characters(conn)
        if index < 0 or index >= len(rows):
            return _character_view(conn, user_id)
        row = rows[index]
        _save(conn, user_id, {"actor_id": str(row["id"]), "actor_name": str(row["name"])})
        return _location_view(conn, user_id, 0)
    if callback_data.startswith("diag:lp:"):
        try:
            page = int(callback_data.split(":", 2)[2])
        except ValueError:
            page = 0
        return _location_view(conn, user_id, page)
    if callback_data.startswith("diag:l:"):
        candidate = _candidate(conn, user_id)
        if not candidate:
            return _character_view(conn, user_id)
        try:
            index = int(callback_data.split(":", 2)[2])
        except ValueError:
            return _location_view(conn, user_id, 0)
        rows = _locations(conn)
        if index < 0 or index >= len(rows):
            return _location_view(conn, user_id, 0)
        row = rows[index]
        candidate.update({
            "location_id": str(row["id"]),
            "location_name": str(row["name"]),
            "proposed_time": _current_time(conn).isoformat(),
            "sim_time": None,
        })
        _save(conn, user_id, candidate)
        return _time_view(conn, user_id)
    if callback_data == "diag:time":
        return _time_view(conn, user_id)
    if callback_data == "diag:t:keep":
        candidate = _candidate(conn, user_id)
        if not candidate:
            return _character_view(conn, user_id)
        candidate["sim_time"] = None
        _save(conn, user_id, candidate)
        return _review(conn, user_id)
    if callback_data == "diag:t:use":
        candidate = _candidate(conn, user_id)
        if not candidate:
            return _character_view(conn, user_id)
        candidate["sim_time"] = str(candidate.get("proposed_time") or _current_time(conn).isoformat())
        _save(conn, user_id, candidate)
        return _review(conn, user_id)
    if callback_data.startswith("diag:t:"):
        return _adjust_time(conn, user_id, callback_data.split(":", 2)[2])
    if callback_data == "diag:confirm":
        candidate = _candidate(conn, user_id)
        if not candidate or not candidate.get("actor_id") or not candidate.get("location_id"):
            return _character_view(conn, user_id)
        try:
            result = relocate_character_for_diagnostic(
                conn,
                str(candidate["actor_id"]),
                str(candidate["location_id"]),
                sim_time=candidate.get("sim_time"),
                authority="creator",
                requested_by=requested_by,
            )
        except (KeyError, ValueError, RuntimeError) as exc:
            return _review(conn, user_id)[0] + f"\n\n❌ Relocation rejected safely: {exc}", _review(conn, user_id)[1]
        _save(conn, user_id, None)
        before = result["before"]
        after = result["after"]
        lines = [
            "✅ CREATOR RELOCATION APPLIED",
            "━━━━━━━━━━━━━━━━━━",
            f"Character: {result['character_name']}",
            f"Location: {before['location_name']} → {after['location_name']}",
            f"Time: {before['sim_time']} → {after['sim_time']}",
            f"Pending action cancelled: {result['cancelled_action_id'] or 'None'}",
            f"Wake reason: creator_diagnostic_relocation",
            "",
            "Audit event recorded. Normal autonomy remains authoritative from the new state.",
        ]
        if result["time_mode"] == "raw_forward_jump":
            lines.append(f"⚠️ Raw skipped interval: {result['elapsed_minutes_without_simulation']:g} sim minutes; elapsed history was not synthesized.")
        return "\n".join(lines), [
            [{"text": "🧪 Diagnostics", "callback_data": "diag:home"}],
            [{"text": "← Creator Settings", "callback_data": "ai:home"}],
            [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
        ]
    return "Unknown Creator diagnostic control.", [[{"text": "🧪 Diagnostics", "callback_data": "diag:home"}]]

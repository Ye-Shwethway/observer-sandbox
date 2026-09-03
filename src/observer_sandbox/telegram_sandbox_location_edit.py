from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from typing import Any

from .sandbox_location_operations import (
    SandboxLocationOperationError,
    location_source_fingerprint,
    preflight_sandbox_location_update_v2,
    update_sandbox_location_v2,
)
from .sandbox_location_v2 import get_sandbox_location_v2


class SandboxLocationEditError(ValueError):
    pass


_SESSIONS: dict[int, dict[str, Any]] = {}

_SECTION_LABELS = {
    "identity": "🪪 Identity",
    "structure": "🏗 Structure",
    "geography": "🗺 Geography",
    "spatial": "📐 Spatial",
    "boundary": "🧱 Boundary",
    "access": "🚪 Access",
    "operations": "⚙️ Operations",
    "topology": "🔗 Topology",
    "facilities": "🏢 Facilities",
    "environment": "🌤 Environment",
    "control": "🔐 Control",
    "economic_policy": "💰 Economics",
    "provenance": "🧾 Provenance",
}


def _save_session(user_id: int, value: dict[str, Any] | None) -> None:
    if value is None:
        _SESSIONS.pop(int(user_id), None)
    else:
        _SESSIONS[int(user_id)] = deepcopy(value)


def get_sandbox_location_edit_session(*, user_id: int) -> dict[str, Any] | None:
    value = _SESSIONS.get(int(user_id))
    return None if value is None else deepcopy(value)


def enter_sandbox_location_edit(conn: sqlite3.Connection, *, user_id: int, object_id: str):
    location = get_sandbox_location_v2(conn, object_id)
    if location["lifecycle_status"] != "active":
        raise SandboxLocationEditError("Location edit target must be active")
    source = deepcopy(location["source"])
    _save_session(user_id, {
        "object_id": object_id,
        "name": source["identity"]["name"],
        "base_fingerprint": location_source_fingerprint(source),
        "pending_section": None,
        "pending_source": None,
    })
    return location_edit_home_view(conn, user_id=user_id)


def exit_sandbox_location_edit(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        return "✏️ No active Sandbox Location edit session.", [[{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]]
    object_id = str(session["object_id"])
    _save_session(user_id, None)
    return (
        "✅ SANDBOX LOCATION EDIT MODE CLOSED\n━━━━━━━━━━━━━━━━━━\n"
        f"{session.get('name') or object_id} editing finished.\n"
        "No runtime pause was needed because approved Sandbox Locations are not running yet.\n"
        "Canonical Real World remained unchanged.",
        [
            [{"text": "← Location", "callback_data": f"sw:o:{object_id}"}],
            [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
        ],
    )


def location_edit_home_view(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Sandbox Location edit session expired")
    location = get_sandbox_location_v2(conn, str(session["object_id"]))
    name = str(location["source"]["identity"]["name"])
    session["name"] = name
    session["pending_section"] = None
    session["pending_source"] = None
    _save_session(user_id, session)
    lines = [
        f"✏️ {name} · SANDBOX LOCATION EDIT",
        "━━━━━━━━━━━━━━━━━━",
        "Choose one schema section to edit.",
        "Send the complete replacement JSON for that section; the whole location-v2 payload is preflighted before Preview.",
        "🔒 Identity key is immutable after creation.",
        "Created Location runtime is not running, so this editor does not pause Sandbox time.",
    ]
    keyboard = [[{"text": label, "callback_data": f"sw:ledit:s:{section}"}] for section, label in _SECTION_LABELS.items()]
    keyboard.extend([
        [{"text": "✅ Done Editing", "callback_data": "sw:ledit:done"}],
        [{"text": "← Location", "callback_data": f"sw:o:{session['object_id']}"}],
    ])
    return "\n".join(lines), keyboard


def location_section_prompt_view(conn: sqlite3.Connection, *, user_id: int, section: str):
    if section not in _SECTION_LABELS:
        raise SandboxLocationEditError("Unknown Location edit section")
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None:
        raise SandboxLocationEditError("Sandbox Location edit session expired")
    location = get_sandbox_location_v2(conn, str(session["object_id"]))
    current = location["source"].get(section)
    session["pending_section"] = section
    session["pending_source"] = None
    _save_session(user_id, session)
    return (
        f"{_SECTION_LABELS[section]} · EDIT\n━━━━━━━━━━━━━━━━━━\n"
        "Send the complete replacement JSON value for this section as your next message.\n"
        "The whole Location will be validated and graph-preflighted before you can Apply.\n"
        + ("Identity.key must remain unchanged.\n" if section == "identity" else "")
        + "\nCurrent value:\n"
        + json.dumps(current, ensure_ascii=False, indent=2, sort_keys=True),
        [
            [{"text": "✕ Cancel Section Edit", "callback_data": "sw:ledit:cancelinput"}],
            [{"text": "✅ Done Editing", "callback_data": "sw:ledit:done"}],
        ],
    )


def handle_sandbox_location_edit_text(conn: sqlite3.Connection, *, user_id: int, text: str):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None or not session.get("pending_section"):
        return None
    section = str(session["pending_section"])
    try:
        replacement = json.loads((text or "").strip())
    except json.JSONDecodeError as exc:
        raise SandboxLocationEditError("Send valid JSON for the complete Location section") from exc

    location = get_sandbox_location_v2(conn, str(session["object_id"]))
    proposal = deepcopy(location["source"])
    proposal[section] = replacement
    try:
        preflight_sandbox_location_update_v2(
            conn,
            str(session["object_id"]),
            proposal,
            expected_source_fingerprint=str(session["base_fingerprint"]),
        )
    except SandboxLocationOperationError as exc:
        raise SandboxLocationEditError(str(exc)) from exc
    session["pending_source"] = proposal
    _save_session(user_id, session)
    return location_edit_preview_view(conn, user_id=user_id)


def _short(value: Any) -> str:
    rendered = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return rendered if len(rendered) <= 500 else rendered[:497] + "..."


def location_edit_preview_view(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None or not isinstance(session.get("pending_source"), dict):
        raise SandboxLocationEditError("No Location edit proposal is ready for Preview")
    section = str(session["pending_section"])
    location = get_sandbox_location_v2(conn, str(session["object_id"]))
    current = location["source"].get(section)
    proposed = session["pending_source"].get(section)
    return (
        "📋 LOCATION EDIT PREVIEW\n━━━━━━━━━━━━━━━━━━\n"
        f"Location: {location['source']['identity']['name']}\n"
        f"Section: {_SECTION_LABELS.get(section, section)}\n\n"
        f"BEFORE\n{_short(current)}\n\n"
        f"AFTER\n{_short(proposed)}\n\n"
        "✅ Exact location-v2 + same-Sandbox graph preflight passed.\n"
        "Apply is stale-guarded against the approved source you started editing.",
        [
            [{"text": "✅ Apply Edit", "callback_data": "sw:ledit:apply"}],
            [{"text": "← Edit Again", "callback_data": f"sw:ledit:s:{section}"}],
            [{"text": "✕ Discard Proposal", "callback_data": "sw:ledit:discard"}],
        ],
    )


def apply_sandbox_location_edit(conn: sqlite3.Connection, *, user_id: int):
    session = get_sandbox_location_edit_session(user_id=user_id)
    if session is None or not isinstance(session.get("pending_source"), dict):
        raise SandboxLocationEditError("No Location edit proposal is ready to Apply")
    try:
        updated = update_sandbox_location_v2(
            conn,
            str(session["object_id"]),
            session["pending_source"],
            expected_source_fingerprint=str(session["base_fingerprint"]),
        )
    except SandboxLocationOperationError as exc:
        raise SandboxLocationEditError(str(exc)) from exc
    session["base_fingerprint"] = location_source_fingerprint(updated["source"])
    session["name"] = updated["source"]["identity"]["name"]
    session["pending_section"] = None
    session["pending_source"] = None
    _save_session(user_id, session)
    return (
        "✅ LOCATION EDIT APPLIED\n━━━━━━━━━━━━━━━━━━\n"
        f"Location: {session['name']}\n"
        "The approved Sandbox Location was atomically updated and audited.\n"
        "Runtime was not started and canonical Real World remained unchanged.",
        [
            [{"text": "✏️ Continue Editing", "callback_data": "sw:ledit:home"}],
            [{"text": "✅ Done Editing", "callback_data": "sw:ledit:done"}],
            [{"text": "← Location", "callback_data": f"sw:o:{session['object_id']}"}],
        ],
    )


def location_edit_callback_view(conn: sqlite3.Connection, *, user_id: int, callback_data: str):
    if callback_data.startswith("sw:ledit:start:"):
        return enter_sandbox_location_edit(conn, user_id=user_id, object_id=callback_data.split(":", 3)[3])
    if callback_data == "sw:ledit:home":
        return location_edit_home_view(conn, user_id=user_id)
    if callback_data.startswith("sw:ledit:s:"):
        return location_section_prompt_view(conn, user_id=user_id, section=callback_data.split(":", 3)[3])
    if callback_data == "sw:ledit:cancelinput":
        return location_edit_home_view(conn, user_id=user_id)
    if callback_data == "sw:ledit:preview":
        return location_edit_preview_view(conn, user_id=user_id)
    if callback_data == "sw:ledit:apply":
        return apply_sandbox_location_edit(conn, user_id=user_id)
    if callback_data == "sw:ledit:discard":
        session = get_sandbox_location_edit_session(user_id=user_id)
        if session is None:
            raise SandboxLocationEditError("Sandbox Location edit session expired")
        session["pending_section"] = None
        session["pending_source"] = None
        _save_session(user_id, session)
        return location_edit_home_view(conn, user_id=user_id)
    if callback_data == "sw:ledit:done":
        return exit_sandbox_location_edit(conn, user_id=user_id)
    raise KeyError(callback_data)


__all__ = [
    "SandboxLocationEditError",
    "apply_sandbox_location_edit",
    "enter_sandbox_location_edit",
    "exit_sandbox_location_edit",
    "get_sandbox_location_edit_session",
    "handle_sandbox_location_edit_text",
    "location_edit_callback_view",
    "location_edit_home_view",
    "location_edit_preview_view",
    "location_section_prompt_view",
]

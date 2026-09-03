from __future__ import annotations

from copy import deepcopy
from typing import Any

from .sandbox_location_cleanup import (
    SandboxLocationCleanupError,
    delete_sandbox_location_v2,
    location_delete_dependencies,
)
from .sandbox_location_operations import location_source_fingerprint
from .sandbox_location_v2 import get_sandbox_location_v2


_SESSIONS: dict[int, dict[str, Any]] = {}


def _save_session(user_id: int, value: dict[str, Any] | None) -> None:
    if value is None:
        _SESSIONS.pop(int(user_id), None)
    else:
        _SESSIONS[int(user_id)] = deepcopy(value)


def _session(user_id: int) -> dict[str, Any] | None:
    value = _SESSIONS.get(int(user_id))
    return None if value is None else deepcopy(value)


def _dependency_icon(creation_type: str) -> str:
    return {
        "character": "👤",
        "item": "📦",
        "location": "📍",
    }.get(str(creation_type), "•")


def location_cleanup_review(conn, *, user_id: int, object_id: str):
    try:
        location = get_sandbox_location_v2(conn, object_id)
    except Exception as exc:
        raise SandboxLocationCleanupError(str(exc)) from exc
    if location["lifecycle_status"] != "active":
        raise SandboxLocationCleanupError("Location cleanup target must be active")

    fingerprint = location_source_fingerprint(location["source"])
    dependencies = location_delete_dependencies(conn, object_id)
    name = str(location.get("source", {}).get("identity", {}).get("name") or object_id)
    _save_session(
        user_id,
        {
            "object_id": object_id,
            "name": name,
            "source_fingerprint": fingerprint,
        },
    )

    lines = [
        "🗑 SANDBOX LOCATION CLEANUP",
        "━━━━━━━━━━━━━━━━━━",
        f"📍 {name}",
        "",
    ]
    if dependencies:
        lines.extend([
            "⛔ This Location cannot be deleted yet.",
            "Active Sandbox state still depends on it:",
            "",
        ])
        for dependency in dependencies:
            icon = _dependency_icon(str(dependency.get("creation_type") or ""))
            dep_name = str(dependency.get("name") or dependency.get("object_id") or "Unknown")
            reason = str(dependency.get("reason") or "reference").replace("_", " ").title()
            lines.append(f"• {icon} {dep_name} · {reason}")
        lines.extend([
            "",
            "Detach or edit these references first. No data was changed.",
        ])
        return "\n".join(lines), [
            [{"text": "← Back to Location", "callback_data": f"sw:o:{object_id}"}],
            [{"text": "← Locations", "callback_data": "sw:list:location"}],
        ]

    lines.extend([
        "No active Sandbox dependencies were found.",
        "",
        "⚠️ Delete this approved Sandbox Location permanently?",
        "The review is revision-bound by its exact source fingerprint.",
        "Real World and canonical state must remain unchanged.",
    ])
    return "\n".join(lines), [
        [{"text": "🗑 Confirm Delete Location", "callback_data": "sw:ldel:apply"}],
        [{"text": "← Cancel", "callback_data": f"sw:o:{object_id}"}],
    ]


def location_cleanup_callback_view(conn, *, user_id: int, callback_data: str):
    if callback_data.startswith("sw:ldel:start:"):
        object_id = callback_data.split(":", 3)[3]
        return location_cleanup_review(conn, user_id=user_id, object_id=object_id)

    if callback_data == "sw:ldel:apply":
        session = _session(user_id)
        if session is None:
            raise SandboxLocationCleanupError("Location delete review expired; open the Location and review again")
        result = delete_sandbox_location_v2(
            conn,
            str(session["object_id"]),
            expected_source_fingerprint=str(session["source_fingerprint"]),
        )
        _save_session(user_id, None)
        return (
            "✅ SANDBOX LOCATION DELETED\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"📍 {result['name']}\n\n"
            "Canonical state fingerprint unchanged.\n"
            "Real World and canonical state were not changed.",
            [
                [{"text": "← Locations", "callback_data": "sw:list:location"}],
                [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
            ],
        )

    raise KeyError(callback_data)


def clear_location_cleanup_session(*, user_id: int) -> None:
    _save_session(user_id, None)


__all__ = [
    "clear_location_cleanup_session",
    "location_cleanup_callback_view",
    "location_cleanup_review",
]

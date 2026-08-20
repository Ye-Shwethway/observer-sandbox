from __future__ import annotations

from copy import deepcopy
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID, list_sandbox_objects
from .sandbox_batch_delete import delete_sandbox_objects

_SESSIONS: dict[int, dict[str, Any]] = {}
_ALLOWED_TYPES = frozenset({"character", "item"})


def _save_session(user_id: int, value: dict[str, Any] | None) -> None:
    if value is None:
        _SESSIONS.pop(int(user_id), None)
    else:
        _SESSIONS[int(user_id)] = deepcopy(value)


def _session(user_id: int) -> dict[str, Any] | None:
    value = _SESSIONS.get(int(user_id))
    return None if value is None else deepcopy(value)


def _candidates(conn) -> list[dict[str, Any]]:
    return [
        value
        for value in list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
        if value["creation_type"] in _ALLOWED_TYPES and value["lifecycle_status"] == "active"
    ]


def _icon(value: dict[str, Any]) -> str:
    return "👤" if value["creation_type"] == "character" else "📦"


def _name(value: dict[str, Any]) -> str:
    return str(value.get("identity", {}).get("name") or value["object_id"])


def sandbox_batch_delete_view(conn, *, user_id: int, reset: bool = False):
    candidates = _candidates(conn)
    valid_ids = {str(value["object_id"]) for value in candidates}
    session = None if reset else _session(user_id)
    if session is None:
        session = {"selected": []}
    selected = [str(value) for value in session.get("selected", []) if str(value) in valid_ids]
    session["selected"] = selected
    _save_session(user_id, session)

    lines = [
        "🗑 SANDBOX BATCH DELETE",
        "━━━━━━━━━━━━━━━━━━",
        "Select Sandbox Characters and Items to delete.",
        "Locations are intentionally excluded from this cleanup tool.",
        "Nothing is deleted until the final confirmation.",
        "",
        f"Selected: {len(selected)} / {len(candidates)}",
    ]
    keyboard: list[list[dict[str, str]]] = []
    if not candidates:
        lines.extend(["", "No active Sandbox Characters or Items to delete."])
    for value in candidates:
        object_id = str(value["object_id"])
        checked = object_id in selected
        mark = "☑️" if checked else "◻️"
        keyboard.append([
            {
                "text": f"{mark} {_icon(value)} {_name(value)}"[:60],
                "callback_data": f"sw:del:toggle:{object_id}",
            }
        ])
    if candidates:
        keyboard.append([
            {"text": "☑️ Select All", "callback_data": "sw:del:all"},
            {"text": "⬜ Clear", "callback_data": "sw:del:clear"},
        ])
    if selected:
        keyboard.append([
            {"text": f"🗑 Review Delete ({len(selected)})", "callback_data": "sw:del:review"}
        ])
    keyboard.append([{"text": "← Cancel", "callback_data": "sw:del:cancel"}])
    return "\n".join(lines), keyboard


def sandbox_batch_delete_review(conn, *, user_id: int):
    session = _session(user_id)
    if session is None or not session.get("selected"):
        return sandbox_batch_delete_view(conn, user_id=user_id)
    candidates = {str(value["object_id"]): value for value in _candidates(conn)}
    selected = [object_id for object_id in session["selected"] if object_id in candidates]
    if not selected:
        session["selected"] = []
        _save_session(user_id, session)
        return sandbox_batch_delete_view(conn, user_id=user_id)

    lines = [
        "⚠️ CONFIRM SANDBOX DELETE",
        "━━━━━━━━━━━━━━━━━━",
        f"The following {len(selected)} Sandbox object(s) will be permanently deleted:",
        "",
    ]
    for object_id in selected:
        value = candidates[object_id]
        lines.append(f"• {_icon(value)} {_name(value)}")
    lines.extend([
        "",
        "This removes only Sandbox objects and dependent Sandbox state.",
        "Real World and canonical state must remain unchanged.",
    ])
    return "\n".join(lines), [
        [{"text": f"🗑 Delete {len(selected)}", "callback_data": "sw:del:apply"}],
        [{"text": "← Back to Selection", "callback_data": "sw:del:home"}],
        [{"text": "✕ Cancel", "callback_data": "sw:del:cancel"}],
    ]


def sandbox_batch_delete_callback_view(conn, *, user_id: int, callback_data: str):
    if callback_data == "sw:del:enter":
        return sandbox_batch_delete_view(conn, user_id=user_id, reset=True)
    if callback_data == "sw:del:home":
        return sandbox_batch_delete_view(conn, user_id=user_id)
    if callback_data == "sw:del:cancel":
        _save_session(user_id, None)
        return None
    if callback_data == "sw:del:all":
        session = _session(user_id) or {"selected": []}
        session["selected"] = [str(value["object_id"]) for value in _candidates(conn)]
        _save_session(user_id, session)
        return sandbox_batch_delete_view(conn, user_id=user_id)
    if callback_data == "sw:del:clear":
        _save_session(user_id, {"selected": []})
        return sandbox_batch_delete_view(conn, user_id=user_id)
    if callback_data.startswith("sw:del:toggle:"):
        object_id = callback_data.split(":", 3)[3]
        valid_ids = {str(value["object_id"]) for value in _candidates(conn)}
        session = _session(user_id) or {"selected": []}
        selected = set(str(value) for value in session.get("selected", []))
        if object_id in valid_ids:
            if object_id in selected:
                selected.remove(object_id)
            else:
                selected.add(object_id)
        session["selected"] = sorted(selected)
        _save_session(user_id, session)
        return sandbox_batch_delete_view(conn, user_id=user_id)
    if callback_data == "sw:del:review":
        return sandbox_batch_delete_review(conn, user_id=user_id)
    if callback_data == "sw:del:apply":
        session = _session(user_id)
        if session is None or not session.get("selected"):
            return sandbox_batch_delete_view(conn, user_id=user_id)
        result = delete_sandbox_objects(conn, session["selected"], sandbox_id=DEFAULT_SANDBOX_ID)
        _save_session(user_id, None)
        deleted = result["deleted"]
        lines = [
            "✅ SANDBOX BATCH DELETE COMPLETE",
            "━━━━━━━━━━━━━━━━━━",
            f"Deleted: {result['deleted_count']}",
        ]
        for value in deleted:
            icon = "👤" if value["creation_type"] == "character" else "📦"
            lines.append(f"• {icon} {value['name']}")
        lines.extend([
            "",
            "Canonical state fingerprint unchanged.",
            "Real World and canonical state were not changed.",
        ])
        return "\n".join(lines), [[{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]]
    raise KeyError(callback_data)


def install_sandbox_batch_delete_world_layers_extension(base_module: Any) -> None:
    if getattr(base_module, "_sandbox_batch_delete_extension_installed", False):
        return
    original_world_view = base_module.sandbox_world_view
    original_callback = base_module.world_layer_callback_view

    def sandbox_world_view(conn):
        text, keyboard = original_world_view(conn)
        rows = [list(row) for row in (keyboard or [])]
        if _candidates(conn) and not any(
            button.get("callback_data") == "sw:del:enter"
            for row in rows
            for button in row
        ):
            insert_at = 1 if rows else 0
            rows.insert(insert_at, [{"text": "🗑 Batch Delete", "callback_data": "sw:del:enter"}])
        return text, rows

    def world_layer_callback_view(conn, callback_data: str):
        if callback_data.startswith("sw:del:"):
            view = sandbox_batch_delete_callback_view(
                conn,
                user_id=base_module._notification_user_id(),
                callback_data=callback_data,
            )
            if view is None:
                return sandbox_world_view(conn)
            return view
        return original_callback(conn, callback_data)

    base_module.sandbox_world_view = sandbox_world_view
    base_module.world_layer_callback_view = world_layer_callback_view
    base_module._sandbox_batch_delete_extension_installed = True


__all__ = [
    "install_sandbox_batch_delete_world_layers_extension",
    "sandbox_batch_delete_callback_view",
    "sandbox_batch_delete_review",
    "sandbox_batch_delete_view",
]

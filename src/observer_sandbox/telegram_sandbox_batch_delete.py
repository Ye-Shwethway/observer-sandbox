from __future__ import annotations

from copy import deepcopy
from typing import Any

from .creation_sandbox import DEFAULT_SANDBOX_ID, list_sandbox_objects
from .sandbox_batch_delete import delete_sandbox_objects

_SESSIONS: dict[int, dict[str, Any]] = {}
_ALLOWED_TYPES = frozenset({"character", "item"})
_ALLOWED_SCOPES = frozenset({"all", "character", "item"})


def _save_session(user_id: int, value: dict[str, Any] | None) -> None:
    if value is None:
        _SESSIONS.pop(int(user_id), None)
    else:
        _SESSIONS[int(user_id)] = deepcopy(value)


def _session(user_id: int) -> dict[str, Any] | None:
    value = _SESSIONS.get(int(user_id))
    return None if value is None else deepcopy(value)


def _normalize_scope(scope: str | None) -> str:
    value = str(scope or "all").strip().lower()
    return value if value in _ALLOWED_SCOPES else "all"


def _candidates(conn, *, scope: str = "all") -> list[dict[str, Any]]:
    scope = _normalize_scope(scope)
    return [
        value
        for value in list_sandbox_objects(conn, sandbox_id=DEFAULT_SANDBOX_ID)
        if value["creation_type"] in _ALLOWED_TYPES
        and value["lifecycle_status"] == "active"
        and (scope == "all" or value["creation_type"] == scope)
    ]


def _icon(value: dict[str, Any]) -> str:
    return "👤" if value["creation_type"] == "character" else "📦"


def _name(value: dict[str, Any]) -> str:
    return str(value.get("identity", {}).get("name") or value["object_id"])


def _scope_label(scope: str) -> str:
    if scope == "item":
        return "SANDBOX ITEM DELETE"
    if scope == "character":
        return "SANDBOX CHARACTER DELETE"
    return "SANDBOX BATCH DELETE"


def _scope_description(scope: str) -> str:
    if scope == "item":
        return "Select Sandbox Items to delete."
    if scope == "character":
        return "Select Sandbox Characters to delete."
    return "Select Sandbox Characters and Items to delete."


def _cancel_callback(scope: str) -> str:
    if scope == "item":
        return "sw:list:item"
    if scope == "character":
        return "sw:list:character"
    return "nav:sandbox"


def sandbox_batch_delete_view(conn, *, user_id: int, reset: bool = False, scope: str | None = None):
    existing = None if reset else _session(user_id)
    resolved_scope = _normalize_scope(scope if scope is not None else (existing or {}).get("scope"))
    candidates = _candidates(conn, scope=resolved_scope)
    valid_ids = {str(value["object_id"]) for value in candidates}
    session = existing or {"selected": [], "scope": resolved_scope}
    session["scope"] = resolved_scope
    selected = [str(value) for value in session.get("selected", []) if str(value) in valid_ids]
    session["selected"] = selected
    _save_session(user_id, session)

    lines = [
        f"🗑 {_scope_label(resolved_scope)}",
        "━━━━━━━━━━━━━━━━━━",
        _scope_description(resolved_scope),
    ]
    if resolved_scope == "all":
        lines.append("Locations are intentionally excluded from this cleanup tool.")
    lines.extend([
        "Nothing is deleted until the final confirmation.",
        "",
        f"Selected: {len(selected)} / {len(candidates)}",
    ])
    keyboard: list[list[dict[str, str]]] = []
    if not candidates:
        noun = "Items" if resolved_scope == "item" else "Characters" if resolved_scope == "character" else "Characters or Items"
        lines.extend(["", f"No active Sandbox {noun} to delete."])
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
    scope = _normalize_scope(session.get("scope"))
    candidates = {str(value["object_id"]): value for value in _candidates(conn, scope=scope)}
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
        return sandbox_batch_delete_view(conn, user_id=user_id, reset=True, scope="all")
    if callback_data in {"sw:del:enter:item", "sw:del:enter:character"}:
        return sandbox_batch_delete_view(
            conn,
            user_id=user_id,
            reset=True,
            scope=callback_data.rsplit(":", 1)[1],
        )
    if callback_data == "sw:del:home":
        return sandbox_batch_delete_view(conn, user_id=user_id)
    if callback_data == "sw:del:cancel":
        session = _session(user_id) or {}
        scope = _normalize_scope(session.get("scope"))
        _save_session(user_id, None)
        return {"return_to": _cancel_callback(scope)}
    if callback_data == "sw:del:all":
        session = _session(user_id) or {"selected": [], "scope": "all"}
        scope = _normalize_scope(session.get("scope"))
        session["selected"] = [str(value["object_id"]) for value in _candidates(conn, scope=scope)]
        _save_session(user_id, session)
        return sandbox_batch_delete_view(conn, user_id=user_id)
    if callback_data == "sw:del:clear":
        session = _session(user_id) or {"scope": "all"}
        session["selected"] = []
        _save_session(user_id, session)
        return sandbox_batch_delete_view(conn, user_id=user_id)
    if callback_data.startswith("sw:del:toggle:"):
        object_id = callback_data.split(":", 3)[3]
        session = _session(user_id) or {"selected": [], "scope": "all"}
        scope = _normalize_scope(session.get("scope"))
        valid_ids = {str(value["object_id"]) for value in _candidates(conn, scope=scope)}
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
        scope = _normalize_scope(session.get("scope"))
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
        return "\n".join(lines), [[{"text": "← Back", "callback_data": _cancel_callback(scope)}]]
    raise KeyError(callback_data)


def install_sandbox_batch_delete_world_layers_extension(base_module: Any) -> None:
    if getattr(base_module, "_sandbox_batch_delete_extension_installed", False):
        return
    original_world_view = base_module.sandbox_world_view
    original_list_view = base_module.sandbox_list_view
    original_callback = base_module.world_layer_callback_view

    def _decorate_list(conn, creation_type: str, view):
        text, keyboard = view
        if creation_type not in {"item", "character"}:
            return text, keyboard
        if not _candidates(conn, scope=creation_type):
            return text, keyboard
        rows = [list(row) for row in (keyboard or [])]
        callback = f"sw:del:enter:{creation_type}"
        if any(button.get("callback_data") == callback for row in rows for button in row):
            return text, rows
        label = "🗑 Select Items to Delete" if creation_type == "item" else "🗑 Select Characters to Delete"
        insert_at = len(rows)
        for index, row in enumerate(rows):
            if any(
                str(button.get("callback_data") or "").startswith("sw:cs:")
                or button.get("callback_data") == "nav:sandbox"
                for button in row
            ):
                insert_at = index
                break
        rows.insert(insert_at, [{"text": label, "callback_data": callback}])
        return text, rows

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

    def sandbox_list_view(conn, creation_type: str):
        return _decorate_list(conn, creation_type, original_list_view(conn, creation_type))

    def _render_target(conn, callback_data: str):
        if callback_data == "nav:sandbox":
            return sandbox_world_view(conn)
        if callback_data == "sw:list:item":
            return _decorate_list(conn, "item", original_callback(conn, callback_data))
        if callback_data == "sw:list:character":
            return _decorate_list(conn, "character", original_callback(conn, callback_data))
        return original_callback(conn, callback_data)

    def world_layer_callback_view(conn, callback_data: str):
        if callback_data.startswith("sw:del:"):
            view = sandbox_batch_delete_callback_view(
                conn,
                user_id=base_module._notification_user_id(),
                callback_data=callback_data,
            )
            if isinstance(view, dict) and view.get("return_to"):
                return _render_target(conn, str(view["return_to"]))
            return view
        if callback_data in {"sw:list:item", "sw:list:character", "nav:sandbox"}:
            return _render_target(conn, callback_data)
        return original_callback(conn, callback_data)

    base_module.sandbox_world_view = sandbox_world_view
    base_module.sandbox_list_view = sandbox_list_view
    base_module.world_layer_callback_view = world_layer_callback_view
    base_module._sandbox_batch_delete_extension_installed = True


__all__ = [
    "install_sandbox_batch_delete_world_layers_extension",
    "sandbox_batch_delete_callback_view",
    "sandbox_batch_delete_review",
    "sandbox_batch_delete_view",
]

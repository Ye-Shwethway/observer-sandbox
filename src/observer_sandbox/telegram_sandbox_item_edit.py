from __future__ import annotations

import json
import sqlite3
from copy import deepcopy
from typing import Any

from .creation_sandbox import get_sandbox_object
from .item_creation_schema import ITEM_RELATION_TYPES, validate_item_payload
from .sandbox_item_creation import get_sandbox_item
from .sandbox_item_operations import SandboxItemOperationError, update_sandbox_item
from .sandbox_runtime import sandbox_runtime_status, set_sandbox_paused


class SandboxItemEditError(ValueError):
    pass


_SESSIONS: dict[int, dict[str, Any]] = {}

_SECTION_LABELS = {
    "definition": "🧬 Definition",
    "instance": "📏 Instance",
    "economic_policy": "💰 Economic Value",
    "modules": "🧩 Modules",
    "requirements": "🪪 Requirements",
    "relationships": "🔗 Relationships",
}

# Null-valued scalar fields need an explicit schema type because Python cannot
# infer a useful editor type from None.
_PATH_TYPES = {
    "economic_policy.currency_code": "string_or_null",
    "economic_policy.market_value_minor": "integer_or_null",
    "economic_policy.replacement_value_minor": "integer_or_null",
    "economic_policy.unit_value_minor": "integer_or_null",
    "economic_policy.unit_quantity": "number_or_null",
    "economic_policy.unit_label": "string_or_null",
    "economic_policy.included_in_parent_ref": "string_or_null",
    "relationships.located_at": "string_or_null",
    "relationships.stored_in": "string_or_null",
    "relationships.owned_by": "string_or_null",
    "relationships.carried_by": "string_or_null",
    "relationships.equipped_by": "string_or_null",
}

_LOCKED_PATHS = frozenset({"definition.key", "instance.mode"})


def _save_session(user_id: int, session: dict[str, Any] | None) -> None:
    if session is None:
        _SESSIONS.pop(int(user_id), None)
    else:
        _SESSIONS[int(user_id)] = deepcopy(session)


def get_sandbox_item_edit_session(*, user_id: int) -> dict[str, Any] | None:
    value = _SESSIONS.get(int(user_id))
    return None if value is None else deepcopy(value)


def _pause_banner() -> list[str]:
    return [
        "⏸ SANDBOX WORLD PAUSED — CREATOR ITEM EDIT MODE",
        "━━━━━━━━━━━━━━━━━━",
        "Sandbox runtime is frozen while this Item editor is open.",
        "Its previous pause state is restored when you finish.",
        "Real World and canonical state remain untouched.",
        "",
    ]


def _item_payload(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    value = get_sandbox_item(conn, object_id)
    payload = deepcopy(value["item"])
    payload.pop("derived", None)
    relationships = {relation_type: None for relation_type in ITEM_RELATION_TYPES}
    for relation in value.get("resolved_relations") or []:
        relation_type = str(relation.get("relation_type") or "")
        if relation_type in relationships:
            relationships[relation_type] = str(relation.get("target_object_id") or "") or None
    payload["relationships"] = relationships
    # Running the canonical validator here guarantees the editor always starts
    # from a payload the same update service can later consume.
    return validate_item_payload(payload)


def _identity(conn: sqlite3.Connection, object_id: str) -> tuple[str, str]:
    obj = get_sandbox_object(conn, object_id)
    if obj["creation_type"] != "item" or obj["lifecycle_status"] != "active":
        raise SandboxItemEditError("Item edit target must be an active Sandbox Item")
    return str(obj["sandbox_id"]), str(obj.get("identity", {}).get("name") or object_id)


def enter_sandbox_item_edit(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    object_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    sandbox_id, name = _identity(conn, object_id)
    existing = get_sandbox_item_edit_session(user_id=user_id)
    if existing is not None and existing.get("object_id") == object_id:
        return item_edit_home_view(conn, user_id=user_id)
    if existing is not None:
        exit_sandbox_item_edit(conn, user_id=user_id)

    # Preflight the exact persisted Item against the current canonical Item
    # contract before changing runtime state. Legacy/incompatible approved Items
    # must fail visibly without leaving the Sandbox paused or opening a session.
    try:
        _item_payload(conn, object_id)
    except Exception as exc:
        raise SandboxItemEditError(f"Current approved Item cannot enter edit mode: {exc}") from exc

    runtime = sandbox_runtime_status(conn, sandbox_id)
    was_paused = bool(runtime["paused"])
    if not was_paused:
        set_sandbox_paused(conn, True, sandbox_id=sandbox_id)

    _save_session(
        user_id,
        {
            "object_id": object_id,
            "item_name": name,
            "sandbox_id": sandbox_id,
            "was_paused_before_edit": was_paused,
            "section": None,
            "field_paths": [],
            "pending_path": None,
            "pending_label": None,
            "pending_proposal": None,
        },
    )
    try:
        return item_edit_home_view(conn, user_id=user_id)
    except Exception:
        _save_session(user_id, None)
        current = sandbox_runtime_status(conn, sandbox_id)
        if not was_paused and bool(current["paused"]):
            set_sandbox_paused(conn, False, sandbox_id=sandbox_id)
        raise


def exit_sandbox_item_edit(
    conn: sqlite3.Connection,
    *,
    user_id: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None:
        return (
            "✏️ No active Sandbox Item edit session.",
            [[{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]],
        )
    sandbox_id = str(session["sandbox_id"])
    was_paused = bool(session.get("was_paused_before_edit", True))
    current = sandbox_runtime_status(conn, sandbox_id)
    if not was_paused and bool(current["paused"]):
        set_sandbox_paused(conn, False, sandbox_id=sandbox_id)
    _save_session(user_id, None)
    state = "remains paused" if was_paused else "resumed"
    object_id = str(session["object_id"])
    return (
        "✅ SANDBOX ITEM EDIT MODE CLOSED\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{session.get('item_name') or object_id} editing finished.\n"
        f"Sandbox World {state}; its pre-edit pause state was restored.\n"
        "Real World and canonical state were not changed.",
        [
            [{"text": "← Item", "callback_data": f"sw:o:{object_id}"}],
            [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
        ],
    )


def item_edit_home_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None:
        raise SandboxItemEditError("Sandbox Item edit session expired")
    payload = _item_payload(conn, str(session["object_id"]))
    name = str(payload["definition"]["name"])
    session["item_name"] = name
    session["pending_path"] = None
    session["pending_proposal"] = None
    _save_session(user_id, session)
    lines = _pause_banner() + [
        f"✏️ {name} · SANDBOX ITEM EDIT",
        "Choose a section, then a field.",
        "🔒 Definition key and instance mode stay immutable after creation.",
        "All updates are previewed and revalidated before Apply.",
    ]
    keyboard = [
        [{"text": label, "callback_data": f"sw:iedit:s:{section}"}]
        for section, label in _SECTION_LABELS.items()
    ]
    keyboard.append([{"text": "✅ Done Editing", "callback_data": "sw:iedit:done"}])
    return "\n".join(lines), keyboard


def _display(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _get_path(payload: dict[str, Any], path: str) -> Any:
    current: Any = payload
    for part in path.split("."):
        if not isinstance(current, dict):
            raise SandboxItemEditError(f"{path} is not editable as a field")
        current = current.get(part)
    return current


def _set_path(payload: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    current: Any = payload
    for part in parts[:-1]:
        if not isinstance(current, dict):
            raise SandboxItemEditError(f"{path} is not editable as a field")
        child = current.get(part)
        if child is None:
            child = {}
            current[part] = child
        if not isinstance(child, dict):
            raise SandboxItemEditError(f"{path} parent is not an object")
        current = child
    current[parts[-1]] = value


def _field_paths(value: Any, prefix: str) -> list[str]:
    if prefix in _PATH_TYPES or not isinstance(value, dict):
        return [prefix]
    paths: list[str] = []
    for key in sorted(value):
        child_prefix = f"{prefix}.{key}" if prefix else str(key)
        child = value[key]
        if isinstance(child, dict) and child:
            paths.extend(_field_paths(child, child_prefix))
        else:
            paths.append(child_prefix)
    return paths


def _parse_value(raw: str, current: Any, path: str) -> Any:
    text = raw.strip()
    explicit = _PATH_TYPES.get(path)
    if explicit:
        if text.lower() in {"null", "none", "clear"} and explicit.endswith("_or_null"):
            return None
        if explicit.startswith("string"):
            return text
        if explicit.startswith("integer"):
            try:
                return int(text)
            except ValueError as exc:
                raise SandboxItemEditError("Send a whole-number minor-unit value, or null") from exc
        if explicit.startswith("number"):
            try:
                return float(text)
            except ValueError as exc:
                raise SandboxItemEditError("Send a numeric value, or null") from exc
    if current is None:
        if text.lower() in {"null", "none", "clear"}:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text
    if isinstance(current, bool):
        lowered = text.lower()
        if lowered in {"true", "yes", "on", "1"}:
            return True
        if lowered in {"false", "no", "off", "0"}:
            return False
        raise SandboxItemEditError("Send true/false")
    if isinstance(current, int) and not isinstance(current, bool):
        try:
            return int(text)
        except ValueError as exc:
            raise SandboxItemEditError("Send a whole number") from exc
    if isinstance(current, float):
        try:
            return float(text)
        except ValueError as exc:
            raise SandboxItemEditError("Send a number") from exc
    if isinstance(current, (dict, list)):
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            raise SandboxItemEditError("Send valid JSON for this structured field") from exc
        if isinstance(current, dict) and not isinstance(value, dict):
            raise SandboxItemEditError("This field requires a JSON object")
        if isinstance(current, list) and not isinstance(value, list):
            raise SandboxItemEditError("This field requires a JSON array")
        return value
    return text


def _section_root(payload: dict[str, Any], section: str) -> Any:
    if section == "modules":
        return payload["definition"].get("modules") or {}
    if section == "requirements":
        return payload["definition"].get("requirements") or {}
    if section == "relationships":
        return payload.get("relationships") or {}
    return payload.get(section) or {}


def _section_prefix(section: str) -> str:
    if section in {"modules", "requirements"}:
        return f"definition.{section}"
    return section


def item_section_edit_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    section: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    if section not in _SECTION_LABELS:
        raise SandboxItemEditError("Unknown Item edit section")
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None:
        raise SandboxItemEditError("Sandbox Item edit session expired")
    payload = _item_payload(conn, str(session["object_id"]))
    root = _section_root(payload, section)
    prefix = _section_prefix(section)
    paths = _field_paths(root, prefix)
    session["section"] = section
    session["field_paths"] = paths
    session["pending_path"] = None
    session["pending_proposal"] = None
    _save_session(user_id, session)

    lines = _pause_banner() + [
        f"{_SECTION_LABELS[section]} · {session['item_name']}",
        "Choose a field to edit.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for index, path in enumerate(paths):
        value = _get_path(payload, path)
        locked = path in _LOCKED_PATHS
        label = path.split(".")[-1].replace("_", " ").title()
        shown = _display(value)
        if len(shown) > 26:
            shown = shown[:23] + "..."
        keyboard.append([
            {
                "text": f"{'🔒' if locked else '✏️'} {label}: {shown}"[:64],
                "callback_data": "sw:iedit:locked" if locked else f"sw:iedit:f:{index}",
            }
        ])
    keyboard.extend([
        [{"text": "← Item Edit", "callback_data": "sw:iedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:iedit:done"}],
    ])
    return "\n".join(lines), keyboard


def item_field_prompt_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    index: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None:
        raise SandboxItemEditError("Sandbox Item edit session expired")
    paths = list(session.get("field_paths") or [])
    if index < 0 or index >= len(paths):
        raise SandboxItemEditError("Unknown Item edit field")
    path = str(paths[index])
    if path in _LOCKED_PATHS:
        raise SandboxItemEditError("That Item field is immutable after creation")
    payload = _item_payload(conn, str(session["object_id"]))
    current = _get_path(payload, path)
    session["pending_path"] = path
    session["pending_label"] = path.split(".")[-1].replace("_", " ").title()
    session["pending_proposal"] = None
    _save_session(user_id, session)
    hint = "Send the new value."
    if isinstance(current, (dict, list)):
        hint = "Send the complete replacement as valid JSON."
    elif current is None or _PATH_TYPES.get(path, "").endswith("_or_null"):
        hint = "Send the new value, or `null` to clear it."
    return (
        "\n".join(_pause_banner() + [
            f"✏️ EDIT {session['pending_label'].upper()}",
            f"Path: {path}",
            f"Current: {_display(current)}",
            "",
            hint,
        ]),
        [[{"text": "Cancel Field Edit", "callback_data": "sw:iedit:cancelinput"}]],
    )


def handle_sandbox_item_edit_text(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    text: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None or not session.get("pending_path"):
        raise SandboxItemEditError("No Sandbox Item field is waiting for a value")
    path = str(session["pending_path"])
    before = _item_payload(conn, str(session["object_id"]))
    current = _get_path(before, path)
    proposed_value = _parse_value(text, current, path)
    candidate = deepcopy(before)
    _set_path(candidate, path, proposed_value)
    try:
        candidate = validate_item_payload(candidate)
    except Exception as exc:
        raise SandboxItemEditError(str(exc)) from exc
    session["pending_proposal"] = {
        "path": path,
        "old_value": current,
        "new_value": proposed_value,
        "before_payload": before,
        "candidate_payload": candidate,
    }
    _save_session(user_id, session)
    return (
        "\n".join(_pause_banner() + [
            "🔎 PREVIEW ITEM CHANGE",
            f"Item: {session['item_name']}",
            f"Field: {path}",
            f"Before: {_display(current)}",
            f"After: {_display(proposed_value)}",
            "",
            "No mutation has occurred yet.",
        ]),
        [
            [{"text": "✅ Apply Change", "callback_data": "sw:iedit:apply"}],
            [{"text": "Cancel", "callback_data": "sw:iedit:cancelinput"}],
        ],
    )


def _apply_proposal(
    conn: sqlite3.Connection,
    *,
    user_id: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None or not session.get("pending_proposal"):
        raise SandboxItemEditError("No previewed Item change is ready to apply")
    proposal = deepcopy(session["pending_proposal"])
    object_id = str(session["object_id"])
    current = _item_payload(conn, object_id)
    if current != proposal["before_payload"]:
        raise SandboxItemEditError("Item changed after preview; reopen the field and preview again")
    try:
        updated = update_sandbox_item(conn, object_id, proposal["candidate_payload"])
    except SandboxItemOperationError as exc:
        raise SandboxItemEditError(str(exc)) from exc

    session["item_name"] = str(updated["item"]["definition"]["name"])
    session["pending_proposal"] = None
    _save_session(user_id, session)
    lines = _pause_banner() + [
        "✅ SANDBOX ITEM UPDATE APPLIED",
        f"Item: {session['item_name']}",
        f"• {proposal['path']}: {_display(proposal['old_value'])} → {_display(proposal['new_value'])}",
        "",
        "Sandbox World remains paused because Creator Item Edit Mode is still open.",
        "Real World and canonical state were not changed.",
    ]
    return "\n".join(lines), [
        [{"text": "✏️ Continue Editing", "callback_data": "sw:iedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:iedit:done"}],
    ]


def sandbox_item_edit_callback_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    callback_data: str,
) -> tuple[str, list[list[dict[str, str]]]] | None:
    if callback_data.startswith("sw:iedit:enter:"):
        return enter_sandbox_item_edit(
            conn,
            user_id=user_id,
            object_id=callback_data.split(":", 3)[3],
        )
    if not callback_data.startswith("sw:iedit:"):
        return None
    if callback_data == "sw:iedit:home":
        return item_edit_home_view(conn, user_id=user_id)
    if callback_data == "sw:iedit:done":
        return exit_sandbox_item_edit(conn, user_id=user_id)
    if callback_data == "sw:iedit:locked":
        session = get_sandbox_item_edit_session(user_id=user_id)
        if session is None:
            raise SandboxItemEditError("Sandbox Item edit session expired")
        section = str(session.get("section") or "definition")
        text, keyboard = item_section_edit_view(conn, user_id=user_id, section=section)
        return text + "\n\n🔒 That field is immutable after Item creation.", keyboard
    if callback_data == "sw:iedit:cancelinput":
        session = get_sandbox_item_edit_session(user_id=user_id)
        if session is None:
            raise SandboxItemEditError("Sandbox Item edit session expired")
        session["pending_path"] = None
        session["pending_label"] = None
        session["pending_proposal"] = None
        section = str(session.get("section") or "")
        _save_session(user_id, session)
        return item_section_edit_view(conn, user_id=user_id, section=section) if section else item_edit_home_view(conn, user_id=user_id)
    if callback_data.startswith("sw:iedit:s:"):
        return item_section_edit_view(
            conn,
            user_id=user_id,
            section=callback_data.split(":", 3)[3],
        )
    if callback_data.startswith("sw:iedit:f:"):
        return item_field_prompt_view(
            conn,
            user_id=user_id,
            index=int(callback_data.split(":", 3)[3]),
        )
    if callback_data == "sw:iedit:apply":
        return _apply_proposal(conn, user_id=user_id)
    raise SandboxItemEditError("Unknown Sandbox Item edit destination")


__all__ = [
    "SandboxItemEditError",
    "enter_sandbox_item_edit",
    "exit_sandbox_item_edit",
    "get_sandbox_item_edit_session",
    "handle_sandbox_item_edit_text",
    "sandbox_item_edit_callback_view",
]

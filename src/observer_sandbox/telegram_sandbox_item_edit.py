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
    return item_edit_home_view(conn, user_id=user_id)


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
        [
            {"text": "🧬 Definition", "callback_data": "sw:iedit:s:definition"},
            {"text": "📏 Instance", "callback_data": "sw:iedit:s:instance"},
        ],
        [
            {"text": "💰 Economic Value", "callback_data": "sw:iedit:s:economic_policy"},
            {"text": "🧩 Modules", "callback_data": "sw:iedit:s:modules"},
        ],
        [
            {"text": "🪪 Requirements", "callback_data": "sw:iedit:s:requirements"},
            {"text": "🔗 Relationships", "callback_data": "sw:iedit:s:relationships"},
        ],
        [{"text": "✅ Done Editing", "callback_data": "sw:iedit:done"}],
    ]
    return "\n".join(lines), keyboard


def _get_path(payload: dict[str, Any], path: str) -> Any:
    value: Any = payload
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            raise SandboxItemEditError(f"Item field is not represented: {path}")
        value = value[part]
    return deepcopy(value)


def _set_path(payload: dict[str, Any], path: str, value: Any) -> None:
    parts = path.split(".")
    target: Any = payload
    for part in parts[:-1]:
        if not isinstance(target, dict) or part not in target:
            raise SandboxItemEditError(f"Item field is not represented: {path}")
        target = target[part]
    if not isinstance(target, dict):
        raise SandboxItemEditError(f"Item field is not writable: {path}")
    target[parts[-1]] = deepcopy(value)


def _display(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
    return str(value)


def _label(path: str) -> str:
    return path.split(".")[-1].replace("_", " ").title()


def _section_paths(payload: dict[str, Any], section: str) -> list[str]:
    if section == "definition":
        return [
            "definition.key",
            "definition.name",
            "definition.kind",
            "definition.description",
            "definition.stackable",
            "definition.mobility",
            "definition.capabilities",
            "definition.tags",
        ]
    if section == "instance":
        paths = ["instance.mode"]
        if payload["instance"]["mode"] == "stack":
            paths.extend(["instance.quantity", "instance.unit"])
        return paths
    if section == "economic_policy":
        return [f"economic_policy.{key}" for key in payload["economic_policy"]]
    if section == "requirements":
        return ["requirements.use"]
    if section == "relationships":
        return [f"relationships.{key}" for key in sorted(ITEM_RELATION_TYPES)]
    if section == "modules":
        # Whole-module JSON buttons permit adding/removing conditional modules;
        # represented module leaves are also exposed for quick detailed edits.
        paths = ["definition.modules"]
        modules = payload["definition"]["modules"]
        for module_name, module in modules.items():
            module_path = f"definition.modules.{module_name}"
            paths.append(module_path)
            if isinstance(module, dict):
                for key, value in module.items():
                    child = f"{module_path}.{key}"
                    paths.append(child)
                    if isinstance(value, dict):
                        for leaf in value:
                            paths.append(f"{child}.{leaf}")
        return paths
    raise SandboxItemEditError("Unknown Item edit section")


def item_section_edit_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    section: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None:
        raise SandboxItemEditError("Sandbox Item edit session expired")
    payload = _item_payload(conn, str(session["object_id"]))
    paths = _section_paths(payload, section)
    session["section"] = section
    session["field_paths"] = paths
    session["pending_path"] = None
    session["pending_proposal"] = None
    _save_session(user_id, session)

    lines = _pause_banner() + [
        f"{_SECTION_LABELS[section]} · ITEM EDIT",
        "Select a field. Complex values use exact JSON.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for index, path in enumerate(paths):
        value = _get_path(payload, path)
        locked = path in _LOCKED_PATHS
        prefix = "🔒" if locked else "✏️"
        text = f"{prefix} {_label(path)}: {_display(value)}"
        keyboard.append([
            {
                "text": text[:60],
                "callback_data": f"sw:iedit:locked" if locked else f"sw:iedit:f:{index}",
            }
        ])
    keyboard.append([{"text": "← Edit Item", "callback_data": "sw:iedit:home"}])
    keyboard.append([{"text": "✅ Done Editing", "callback_data": "sw:iedit:done"}])
    return "\n".join(lines), keyboard


def _expected_type(path: str, current: Any) -> str:
    explicit = _PATH_TYPES.get(path)
    if explicit:
        return explicit
    if isinstance(current, bool):
        return "boolean"
    if isinstance(current, int):
        return "integer"
    if isinstance(current, float):
        return "number"
    if isinstance(current, dict):
        return "json_object"
    if isinstance(current, list):
        return "json_array"
    if current is None:
        return "json_or_null"
    return "string"


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
        raise SandboxItemEditError("Unknown Item field selection")
    path = str(paths[index])
    if path in _LOCKED_PATHS:
        raise SandboxItemEditError(f"{path} is immutable after Item creation")
    payload = _item_payload(conn, str(session["object_id"]))
    current = _get_path(payload, path)
    session["pending_path"] = path
    session["pending_label"] = _label(path)
    session["pending_proposal"] = None
    _save_session(user_id, session)
    lines = _pause_banner() + [
        f"✏️ EDIT {_label(path).upper()}",
        f"Field: {path}",
        f"Current: {_display(current)}",
        f"Expected: {_expected_type(path, current)}",
        "",
        "Send the new value as your next Telegram message.",
        "Use exact JSON for objects/lists; send null for nullable fields.",
        "Monetary *_minor fields use integer minor currency units (for example USD 12.50 = 1250).",
        "Nothing changes until Preview → Apply.",
    ]
    return "\n".join(lines), [
        [{"text": "✕ Cancel Field Edit", "callback_data": "sw:iedit:cancelinput"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:iedit:done"}],
    ]


def _coerce(path: str, current: Any, raw: str) -> Any:
    text = raw.strip()
    kind = _expected_type(path, current)
    nullable = kind.endswith("_or_null") or kind == "json_or_null"
    if text.lower() == "null":
        if nullable:
            return None
        raise SandboxItemEditError(f"{path} is not nullable")
    if kind in {"json_object", "json_array", "json_or_null"}:
        try:
            value = json.loads(text)
        except json.JSONDecodeError as exc:
            raise SandboxItemEditError(f"{path} requires valid JSON") from exc
        if kind == "json_object" and not isinstance(value, dict):
            raise SandboxItemEditError(f"{path} requires a JSON object")
        if kind == "json_array" and not isinstance(value, list):
            raise SandboxItemEditError(f"{path} requires a JSON array")
        return value
    if kind == "boolean":
        if text.lower() in {"true", "yes", "1", "on"}:
            return True
        if text.lower() in {"false", "no", "0", "off"}:
            return False
        raise SandboxItemEditError(f"{path} requires true or false")
    if kind in {"integer", "integer_or_null"}:
        try:
            return int(text)
        except ValueError as exc:
            raise SandboxItemEditError(f"{path} requires an integer") from exc
    if kind in {"number", "number_or_null"}:
        try:
            return float(text)
        except ValueError as exc:
            raise SandboxItemEditError(f"{path} requires a number") from exc
    return text


def handle_sandbox_item_edit_text(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    text: str,
) -> tuple[str, list[list[dict[str, str]]]] | None:
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None or not session.get("pending_path"):
        return None
    object_id = str(session["object_id"])
    path = str(session["pending_path"])
    before = _item_payload(conn, object_id)
    old_value = _get_path(before, path)
    new_value = _coerce(path, old_value, text)
    candidate = deepcopy(before)
    _set_path(candidate, path, new_value)
    try:
        normalized = validate_item_payload(candidate)
    except Exception as exc:
        raise SandboxItemEditError(f"Item contract rejected {path}: {exc}") from exc

    proposal = {
        "object_id": object_id,
        "path": path,
        "label": _label(path),
        "old_value": old_value,
        "new_value": _get_path(normalized, path),
        "before_payload": before,
        "candidate_payload": normalized,
    }
    session["pending_path"] = None
    session["pending_label"] = None
    session["pending_proposal"] = proposal
    _save_session(user_id, session)
    lines = _pause_banner() + [
        "🔎 SANDBOX ITEM CHANGE PREVIEW",
        f"Item: {session.get('item_name') or object_id}",
        f"• {path}",
        f"  {_display(old_value)} → {_display(proposal['new_value'])}",
        "",
        "Apply updates Sandbox state only through the strict Item update contract.",
    ]
    return "\n".join(lines), [
        [{"text": "✅ Apply Change", "callback_data": "sw:iedit:apply"}],
        [{"text": "✕ Cancel Preview", "callback_data": "sw:iedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:iedit:done"}],
    ]


def _apply_proposal(
    conn: sqlite3.Connection,
    *,
    user_id: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_item_edit_session(user_id=user_id)
    if session is None:
        raise SandboxItemEditError("Sandbox Item edit session expired")
    proposal = session.get("pending_proposal")
    if not isinstance(proposal, dict):
        raise SandboxItemEditError("No Item change is awaiting Apply")
    object_id = str(proposal["object_id"])
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

from __future__ import annotations

import json
import sqlite3
from typing import Any

from .creator_profile_edit import CreatorProfileEditError, _coerce, _validate_numeric
from .creation_sandbox import get_sandbox_object
from .sandbox_profile_observer import sandbox_profile_menu, sandbox_profile_section
from .sandbox_runtime import sandbox_runtime_status, set_sandbox_paused


_SESSIONS: dict[int, dict[str, Any]] = {}


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def get_sandbox_profile_edit_session(*, user_id: int) -> dict[str, Any] | None:
    session = _SESSIONS.get(int(user_id))
    return None if session is None else dict(session)


def _save_session(user_id: int, session: dict[str, Any] | None) -> None:
    if session is None:
        _SESSIONS.pop(int(user_id), None)
    else:
        _SESSIONS[int(user_id)] = dict(session)


def _pause_banner() -> list[str]:
    return [
        "⏸ SANDBOX WORLD PAUSED — CREATOR EDIT MODE",
        "━━━━━━━━━━━━━━━━━━",
        "Only Sandbox World runtime is frozen while this profile edit is open.",
        "Real World runtime and canonical state are untouched.",
        "",
    ]


def _sandbox_identity(conn: sqlite3.Connection, object_id: str) -> tuple[str, str]:
    obj = get_sandbox_object(conn, object_id)
    if obj["creation_type"] != "character" or obj["lifecycle_status"] != "active":
        raise CreatorProfileEditError("Sandbox profile edit target must be an active Character")
    return str(obj["sandbox_id"]), str(obj["identity"].get("name") or object_id)


def enter_sandbox_profile_edit(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    character_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    sandbox_id, name = _sandbox_identity(conn, character_id)
    existing = get_sandbox_profile_edit_session(user_id=user_id)
    if existing is not None and existing.get("character_id") == character_id:
        return sandbox_edit_home_view(conn, user_id=user_id)
    if existing is not None:
        exit_sandbox_profile_edit(conn, user_id=user_id)

    runtime = sandbox_runtime_status(conn, sandbox_id)
    was_paused = bool(runtime["paused"])
    if not was_paused:
        set_sandbox_paused(conn, True, sandbox_id=sandbox_id)
    _save_session(
        user_id,
        {
            "character_id": character_id,
            "character_name": name,
            "sandbox_id": sandbox_id,
            "was_paused_before_edit": was_paused,
            "field_picker_section": None,
            "field_picker_keys": [],
            "pending_field_key": None,
            "pending_field_label": None,
            "pending_proposal": None,
        },
    )
    return sandbox_edit_home_view(conn, user_id=user_id)


def exit_sandbox_profile_edit(
    conn: sqlite3.Connection,
    *,
    user_id: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_profile_edit_session(user_id=user_id)
    if session is None:
        return (
            "✏️ No active Sandbox profile edit session.",
            [[{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]],
        )
    sandbox_id = str(session["sandbox_id"])
    was_paused = bool(session.get("was_paused_before_edit", True))
    current = sandbox_runtime_status(conn, sandbox_id)
    if not was_paused and bool(current["paused"]):
        set_sandbox_paused(conn, False, sandbox_id=sandbox_id)
    _save_session(user_id, None)
    state = "remains paused" if was_paused else "resumed"
    character_id = str(session["character_id"])
    return (
        "✅ SANDBOX PROFILE EDIT MODE CLOSED\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{session.get('character_name') or character_id} profile editing finished.\n"
        f"Sandbox World {state}; its pre-edit pause state was restored.\n"
        "Real World was not changed.",
        [
            [{"text": "← Profile", "callback_data": f"sw:prof:{character_id}"}],
            [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
        ],
    )


def sandbox_edit_home_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_profile_edit_session(user_id=user_id)
    if session is None:
        raise CreatorProfileEditError("Sandbox profile edit session expired")
    character_id = str(session["character_id"])
    data = sandbox_profile_menu(conn, character_id, role="owner")
    lines = _pause_banner() + [
        f"✏️ {session.get('character_name') or character_id} · SANDBOX PROFILE EDIT",
        "Choose a represented profile section and field.",
        "Nothing becomes canonical through this editor.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    sections = data.get("sections") or []
    for index in range(0, len(sections), 2):
        row = []
        for section in sections[index : index + 2]:
            row.append(
                {
                    "text": f"{section['icon']} {section['label']}",
                    "callback_data": f"sw:pedit:s:{section['id']}",
                }
            )
        keyboard.append(row)
    keyboard.append([{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}])
    return "\n".join(lines), keyboard


def _writable_items(
    conn: sqlite3.Connection,
    character_id: str,
    section_id: str,
) -> list[dict[str, Any]]:
    data = sandbox_profile_section(conn, character_id, section_id, role="owner")
    items: list[dict[str, Any]] = []
    for item in data.get("content") or []:
        field_key = str(item.get("field_key") or "")
        if (
            item.get("kind") != "field"
            or not field_key
            or str(item.get("mode") or "") == "derived"
            or field_key == "identity.sex"
        ):
            continue
        row = conn.execute(
            "SELECT 1 FROM creation_sandbox_profile_values WHERE object_id=? AND field_key=?",
            (character_id, field_key),
        ).fetchone()
        if row is not None:
            items.append(item)
    return items


def sandbox_section_edit_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    section_id: str,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_profile_edit_session(user_id=user_id)
    if session is None:
        raise CreatorProfileEditError("Sandbox profile edit session expired")
    character_id = str(session["character_id"])
    data = sandbox_profile_section(conn, character_id, section_id, role="owner")
    items = _writable_items(conn, character_id, section_id)
    session["field_picker_section"] = section_id
    session["field_picker_keys"] = [str(item["field_key"]) for item in items]
    session["pending_field_key"] = None
    session["pending_proposal"] = None
    _save_session(user_id, session)
    lines = _pause_banner() + [
        f"{data['section']['icon']} {session.get('character_name')} · {str(data['section']['label']).upper()} EDIT",
        "Select a represented writable field to change.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for index, item in enumerate(items):
        unit = str(item.get("unit") or "")
        value_text = f"{item.get('value')} {unit}".strip()
        keyboard.append(
            [
                {
                    "text": f"✏️ {item.get('label')}: {value_text}"[:60],
                    "callback_data": f"sw:pedit:f:{index}",
                }
            ]
        )
    if not items:
        lines.append("No represented fields in this section are writable through the current editor contract.")
    keyboard.append([{"text": "← Edit Profile", "callback_data": "sw:pedit:home"}])
    keyboard.append([{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}])
    return "\n".join(lines), keyboard


def sandbox_field_prompt_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    index: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_profile_edit_session(user_id=user_id)
    if session is None:
        raise CreatorProfileEditError("Sandbox profile edit session expired")
    keys = list(session.get("field_picker_keys") or [])
    if index < 0 or index >= len(keys):
        raise CreatorProfileEditError("Unknown Sandbox profile field selection")
    field_key = str(keys[index])
    row = conn.execute(
        "SELECT label,data_type,unit FROM profile_field_definitions WHERE field_key=?",
        (field_key,),
    ).fetchone()
    if row is None:
        raise CreatorProfileEditError("Profile field definition disappeared")
    session["pending_field_key"] = field_key
    session["pending_field_label"] = str(row["label"])
    session["pending_proposal"] = None
    _save_session(user_id, session)
    lines = _pause_banner() + [
        f"✏️ EDIT {str(row['label']).upper()}",
        f"Field: {field_key}",
        f"Expected: {row['data_type']}" + (f" · {row['unit']}" if row["unit"] else ""),
        "",
        "Send the new value as your next Telegram message.",
        "Nothing changes until you review and press Apply.",
    ]
    return "\n".join(lines), [
        [{"text": "✕ Cancel Field Edit", "callback_data": "sw:pedit:cancelinput"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}],
    ]


def _current_value(conn: sqlite3.Connection, character_id: str, field_key: str) -> Any:
    row = conn.execute(
        "SELECT value_json,mode FROM creation_sandbox_profile_values WHERE object_id=? AND field_key=?",
        (character_id, field_key),
    ).fetchone()
    if row is None:
        raise CreatorProfileEditError(f"Sandbox profile field is not represented: {field_key}")
    if str(row["mode"]) == "derived":
        raise CreatorProfileEditError(f"Derived field is not directly editable: {field_key}")
    return json.loads(row["value_json"])


def _validate_cross(
    conn: sqlite3.Connection,
    character_id: str,
    field_key: str,
    new_value: Any,
) -> None:
    def value(key: str) -> Any:
        if key == field_key:
            return new_value
        row = conn.execute(
            "SELECT value_json FROM creation_sandbox_profile_values WHERE object_id=? AND field_key=?",
            (character_id, key),
        ).fetchone()
        return None if row is None else json.loads(row["value_json"])

    baseline = value("sexual_anatomy.baseline_erectile_function")
    cap = value("sexual_anatomy.erection_firmness_cap")
    if baseline is not None and cap is not None and float(baseline) > float(cap):
        raise CreatorProfileEditError("baseline erectile function cannot exceed erection firmness cap")
    lean_min = value("genetics.weight_lean_min_lb")
    lean_max = value("genetics.weight_lean_max_lb")
    if lean_min is not None and lean_max is not None and float(lean_min) > float(lean_max):
        raise CreatorProfileEditError("genetic lean-weight minimum cannot exceed maximum")


def handle_sandbox_profile_edit_text(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    text: str,
) -> tuple[str, list[list[dict[str, str]]]] | None:
    session = get_sandbox_profile_edit_session(user_id=user_id)
    if session is None or not session.get("pending_field_key"):
        return None
    field_key = str(session["pending_field_key"])
    character_id = str(session["character_id"])
    definition = conn.execute(
        "SELECT label,data_type,unit FROM profile_field_definitions WHERE field_key=?",
        (field_key,),
    ).fetchone()
    if definition is None:
        raise CreatorProfileEditError(f"Unknown profile field: {field_key}")
    try:
        new_value = _coerce(str(definition["data_type"]), text)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise CreatorProfileEditError(f"Invalid {definition['data_type']} value for {field_key}") from exc
    _validate_numeric(field_key, new_value)
    _validate_cross(conn, character_id, field_key, new_value)
    old_value = _current_value(conn, character_id, field_key)
    proposal = {
        "character_id": character_id,
        "sandbox_id": str(session["sandbox_id"]),
        "field_key": field_key,
        "label": str(definition["label"]),
        "old_value": old_value,
        "new_value": new_value,
    }
    session["pending_field_key"] = None
    session["pending_field_label"] = None
    session["pending_proposal"] = proposal
    _save_session(user_id, session)
    lines = _pause_banner() + [
        "🔎 SANDBOX PROFILE CHANGE PREVIEW",
        f"• {proposal['label']}: {old_value} → {new_value}",
        "",
        "Apply changes Sandbox state only. Real World remains unchanged.",
    ]
    return "\n".join(lines), [
        [{"text": "✅ Apply Change", "callback_data": "sw:pedit:apply"}],
        [{"text": "✕ Cancel Preview", "callback_data": "sw:pedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}],
    ]


def _apply_proposal(
    conn: sqlite3.Connection,
    *,
    user_id: int,
) -> tuple[str, list[list[dict[str, str]]]]:
    session = get_sandbox_profile_edit_session(user_id=user_id)
    if session is None:
        raise CreatorProfileEditError("Sandbox profile edit session expired")
    proposal = session.get("pending_proposal")
    if not isinstance(proposal, dict):
        raise CreatorProfileEditError("No Sandbox profile change is awaiting Apply")
    character_id = str(proposal["character_id"])
    sandbox_id = str(proposal["sandbox_id"])
    field_key = str(proposal["field_key"])
    old_value = proposal["old_value"]
    new_value = proposal["new_value"]
    current = _current_value(conn, character_id, field_key)
    if current != old_value:
        raise CreatorProfileEditError(f"Proposal is stale for {field_key}; preview again before applying")
    _validate_numeric(field_key, new_value)
    _validate_cross(conn, character_id, field_key, new_value)

    nested = conn.in_transaction
    savepoint = "sandbox_profile_edit"
    conn.execute(f"SAVEPOINT {savepoint}" if nested else "BEGIN IMMEDIATE")
    try:
        conn.execute(
            """
            UPDATE creation_sandbox_profile_values
            SET value_json=?,authority='creator',source='creator-sandbox-profile-edit-v1',updated_at=CURRENT_TIMESTAMP
            WHERE object_id=? AND field_key=?
            """,
            (_json(new_value), character_id, field_key),
        )
        if conn.execute("SELECT changes()").fetchone()[0] != 1:
            raise CreatorProfileEditError(f"Sandbox profile field disappeared: {field_key}")
        if field_key == "identity.name":
            obj = get_sandbox_object(conn, character_id)
            identity = dict(obj.get("identity") or {})
            identity["name"] = str(new_value)
            conn.execute(
                "UPDATE creation_sandbox_objects SET identity_json=?,updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
                (_json(identity), character_id),
            )
            session["character_name"] = str(new_value)
        revision_row = conn.execute(
            "SELECT revision FROM creation_sandboxes WHERE sandbox_id=?",
            (sandbox_id,),
        ).fetchone()
        if revision_row is None:
            raise CreatorProfileEditError("Sandbox namespace disappeared during profile edit")
        previous_revision = int(revision_row["revision"])
        revision = previous_revision + 1
        conn.execute(
            "UPDATE creation_sandboxes SET revision=?,updated_at=CURRENT_TIMESTAMP WHERE sandbox_id=?",
            (revision, sandbox_id),
        )
        conn.execute(
            """
            INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json)
            VALUES(?,?,'sandbox_profile_field_edited',?)
            """,
            (
                sandbox_id,
                character_id,
                _json(
                    {
                        "field_key": field_key,
                        "old_value": old_value,
                        "new_value": new_value,
                        "requested_by": f"telegram:{int(user_id)}",
                        "previous_revision": previous_revision,
                        "revision": revision,
                        "source": "creator-sandbox-profile-edit-v1",
                    }
                ),
            ),
        )
        if nested:
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        else:
            conn.commit()
    except Exception:
        if nested:
            conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        else:
            conn.rollback()
        raise

    session["pending_proposal"] = None
    _save_session(user_id, session)
    lines = _pause_banner() + [
        "✅ SANDBOX PROFILE UPDATE APPLIED",
        f"Character: {session.get('character_name') or character_id}",
        f"• {proposal['label']}: {old_value} → {new_value}",
        f"Sandbox revision: {previous_revision} → {revision}",
        "",
        "Sandbox World remains paused because Creator Edit Mode is still open.",
        "Real World canonical/runtime state was not changed.",
    ]
    return "\n".join(lines), [
        [{"text": "✏️ Continue Editing", "callback_data": "sw:pedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}],
    ]


def sandbox_profile_edit_callback_view(
    conn: sqlite3.Connection,
    *,
    user_id: int,
    callback_data: str,
) -> tuple[str, list[list[dict[str, str]]]] | None:
    if callback_data.startswith("sw:pedit:enter:"):
        return enter_sandbox_profile_edit(
            conn,
            user_id=user_id,
            character_id=callback_data.split(":", 3)[3],
        )
    if not callback_data.startswith("sw:pedit:"):
        return None
    if callback_data == "sw:pedit:home":
        return sandbox_edit_home_view(conn, user_id=user_id)
    if callback_data == "sw:pedit:done":
        return exit_sandbox_profile_edit(conn, user_id=user_id)
    if callback_data == "sw:pedit:cancelinput":
        session = get_sandbox_profile_edit_session(user_id=user_id)
        if session is None:
            raise CreatorProfileEditError("Sandbox profile edit session expired")
        session["pending_field_key"] = None
        session["pending_field_label"] = None
        session["pending_proposal"] = None
        section_id = str(session.get("field_picker_section") or "")
        _save_session(user_id, session)
        return (
            sandbox_section_edit_view(conn, user_id=user_id, section_id=section_id)
            if section_id
            else sandbox_edit_home_view(conn, user_id=user_id)
        )
    if callback_data.startswith("sw:pedit:s:"):
        return sandbox_section_edit_view(
            conn,
            user_id=user_id,
            section_id=callback_data.split(":", 3)[3],
        )
    if callback_data.startswith("sw:pedit:f:"):
        return sandbox_field_prompt_view(
            conn,
            user_id=user_id,
            index=int(callback_data.split(":", 3)[3]),
        )
    if callback_data == "sw:pedit:apply":
        return _apply_proposal(conn, user_id=user_id)
    raise CreatorProfileEditError("Unknown Sandbox profile edit destination")


__all__ = [
    "enter_sandbox_profile_edit",
    "exit_sandbox_profile_edit",
    "get_sandbox_profile_edit_session",
    "handle_sandbox_profile_edit_text",
    "sandbox_profile_edit_callback_view",
]

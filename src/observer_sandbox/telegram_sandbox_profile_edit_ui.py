from __future__ import annotations

from typing import Any

from .sandbox_profile_edit import (
    SandboxProfileEditError,
    apply_sandbox_profile_edit,
    preview_sandbox_profile_edit,
)
from .sandbox_profile_observer import sandbox_profile_menu, sandbox_profile_section
from .sandbox_runtime import sandbox_runtime_status, set_sandbox_paused
from .simulation import runtime_value, set_runtime_value

SESSION_PREFIX = "telegram_sandbox_profile_edit_session:"


def _session_key(user_id: int) -> str:
    return f"{SESSION_PREFIX}{int(user_id)}"


def _session(conn, user_id: int) -> dict[str, Any] | None:
    value = runtime_value(conn, _session_key(user_id), None)
    return dict(value) if isinstance(value, dict) else None


def _save_session(conn, user_id: int, session: dict[str, Any] | None) -> None:
    set_runtime_value(conn, _session_key(user_id), session)
    conn.commit()


def _pause_banner() -> list[str]:
    return [
        "⏸ SANDBOX PAUSED — CREATOR EDIT MODE",
        "━━━━━━━━━━━━━━━━━━",
        "Only Sandbox World runtime is frozen while this editor is open.",
        "Real World runtime is untouched.",
        "",
    ]


def enter_sandbox_profile_edit(conn, *, user_id: int, character_id: str):
    data = sandbox_profile_menu(conn, character_id, role="owner")
    existing = _session(conn, user_id)
    if existing is not None and existing.get("character_id") == character_id:
        return edit_home_view(conn, user_id=user_id)
    if existing is not None:
        exit_sandbox_profile_edit(conn, user_id=user_id)

    status = sandbox_runtime_status(conn)
    was_paused = bool(status["paused"])
    if not was_paused:
        set_sandbox_paused(conn, True)
    session = {
        "character_id": character_id,
        "character_name": str(data["character"]["name"]),
        "was_paused_before_edit": was_paused,
        "pending_field_key": None,
        "pending_field_label": None,
        "proposal": None,
    }
    _save_session(conn, user_id, session)
    return edit_home_view(conn, user_id=user_id)


def exit_sandbox_profile_edit(conn, *, user_id: int):
    session = _session(conn, user_id)
    if session is None:
        return (
            "✏️ No active Sandbox profile edit session.",
            [[{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]],
        )
    was_paused = bool(session.get("was_paused_before_edit", False))
    status = sandbox_runtime_status(conn)
    if not was_paused and bool(status["paused"]):
        set_sandbox_paused(conn, False)
    _save_session(conn, user_id, None)
    state = "remains paused" if was_paused else "resumed"
    character_id = str(session["character_id"])
    return (
        "✅ SANDBOX PROFILE EDIT MODE CLOSED\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{session.get('character_name') or character_id} profile editing finished.\n"
        f"Sandbox World {state}; its pre-edit pause state was restored.\n"
        "Real World runtime remained untouched.",
        [
            [{"text": "← Profile", "callback_data": f"sw:prof:{character_id}"}],
            [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
        ],
    )


def edit_home_view(conn, *, user_id: int):
    session = _session(conn, user_id)
    if session is None:
        return (
            "✏️ No active Sandbox profile edit session.",
            [[{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}]],
        )
    character_id = str(session["character_id"])
    data = sandbox_profile_menu(conn, character_id, role="owner")
    lines = _pause_banner() + [
        f"✏️ {session.get('character_name') or character_id} · SANDBOX PROFILE EDIT",
        "Choose a represented profile section.",
        "Nothing changes until a preview is explicitly applied.",
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


def _writable_profile_items(conn, character_id: str, section_id: str) -> list[dict[str, Any]]:
    data = sandbox_profile_section(conn, character_id, section_id, role="owner")
    items: list[dict[str, Any]] = []
    for item in data.get("content") or []:
        field_key = str(item.get("field_key") or "")
        if item.get("kind") != "field" or not field_key or str(item.get("mode") or "") == "derived":
            continue
        represented = conn.execute(
            "SELECT 1 FROM creation_sandbox_profile_values WHERE object_id=? AND field_key=? LIMIT 1",
            (character_id, field_key),
        ).fetchone()
        if represented is not None:
            items.append(item)
    return items


def section_edit_view(conn, *, user_id: int, section_id: str):
    session = _session(conn, user_id)
    if session is None:
        raise SandboxProfileEditError("Sandbox profile edit session expired")
    character_id = str(session["character_id"])
    data = sandbox_profile_section(conn, character_id, section_id, role="owner")
    items = _writable_profile_items(conn, character_id, section_id)
    session["field_picker_section"] = section_id
    session["field_picker_keys"] = [str(item["field_key"]) for item in items]
    session["proposal"] = None
    _save_session(conn, user_id, session)

    lines = _pause_banner() + [
        f"{data['section']['icon']} {session.get('character_name')} · {str(data['section']['label']).upper()} EDIT",
        "Select a represented field to change.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for index, item in enumerate(items):
        value_text = f"{item.get('value')} {item.get('unit') or ''}".strip()
        keyboard.append(
            [
                {
                    "text": f"✏️ {item.get('label')}: {value_text}"[:60],
                    "callback_data": f"sw:pedit:f:{index}",
                }
            ]
        )
    if not items:
        lines.append("No represented writable fields are available in this section.")
    keyboard.append([{"text": "← Edit Profile", "callback_data": "sw:pedit:home"}])
    keyboard.append([{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}])
    return "\n".join(lines), keyboard


def field_prompt_view(conn, *, user_id: int, index: int):
    session = _session(conn, user_id)
    if session is None:
        raise SandboxProfileEditError("Sandbox profile edit session expired")
    keys = list(session.get("field_picker_keys") or [])
    if index < 0 or index >= len(keys):
        raise SandboxProfileEditError("Unknown Sandbox profile field selection")
    field_key = str(keys[index])
    row = conn.execute(
        "SELECT label,data_type,unit FROM profile_field_definitions WHERE field_key=?",
        (field_key,),
    ).fetchone()
    if row is None:
        raise SandboxProfileEditError("Profile field definition disappeared")
    session["pending_field_key"] = field_key
    session["pending_field_label"] = str(row["label"])
    session["proposal"] = None
    _save_session(conn, user_id, session)
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


def _preview_view(conn, *, user_id: int, proposal: dict[str, Any]):
    session = _session(conn, user_id)
    if session is None:
        raise SandboxProfileEditError("Sandbox profile edit session expired")
    session["proposal"] = proposal
    _save_session(conn, user_id, session)
    unit = str(proposal.get("unit") or "")
    lines = _pause_banner() + [
        "🔎 SANDBOX PROFILE CHANGE PREVIEW",
        f"Character: {proposal.get('character_name')}",
        f"Field: {proposal.get('label') or proposal.get('field_key')}",
        f"Current: {proposal.get('old_value')} {unit}".rstrip(),
        f"Proposed: {proposal.get('new_value')} {unit}".rstrip(),
        "",
        "Apply changes Sandbox state only. Real World state is not a target of this operation.",
    ]
    return "\n".join(lines), [
        [{"text": "✅ Apply Change", "callback_data": "sw:pedit:apply"}],
        [{"text": "✕ Cancel Preview", "callback_data": "sw:pedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}],
    ]


def _apply_view(conn, *, user_id: int):
    session = _session(conn, user_id)
    if session is None:
        raise SandboxProfileEditError("Sandbox profile edit session expired")
    proposal = session.get("proposal")
    if not isinstance(proposal, dict):
        raise SandboxProfileEditError("No Sandbox profile preview is pending")
    result = apply_sandbox_profile_edit(
        conn,
        proposal,
        requested_by=f"telegram:{user_id}",
    )
    session["proposal"] = None
    session["pending_field_key"] = None
    session["pending_field_label"] = None
    if result["field_key"] == "identity.name":
        session["character_name"] = result["character_name"]
    _save_session(conn, user_id, session)
    lines = _pause_banner() + [
        "✅ SANDBOX PROFILE UPDATE APPLIED",
        f"Character: {result['character_name']}",
        f"{result['label']}: {result['old_value']} → {result['new_value']}",
        "",
        "Sandbox World remains paused because Creator Edit Mode is still open.",
        "Real World runtime and profile state were untouched.",
    ]
    return "\n".join(lines), [
        [{"text": "✏️ Continue Editing", "callback_data": "sw:pedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}],
    ]


def handle_sandbox_profile_edit_text(conn, *, user_id: int, text: str):
    session = _session(conn, user_id)
    if session is None or not session.get("pending_field_key"):
        return None
    proposal = preview_sandbox_profile_edit(
        conn,
        str(session["character_id"]),
        str(session["pending_field_key"]),
        text,
    )
    session["pending_field_key"] = None
    session["pending_field_label"] = None
    _save_session(conn, user_id, session)
    return _preview_view(conn, user_id=user_id, proposal=proposal)


def sandbox_profile_edit_callback_view(conn, *, user_id: int, callback_data: str):
    if callback_data.startswith("sw:pedit:enter:"):
        return enter_sandbox_profile_edit(
            conn,
            user_id=user_id,
            character_id=callback_data.split(":", 3)[3],
        )
    if not callback_data.startswith("sw:pedit:"):
        return None
    if callback_data == "sw:pedit:home":
        return edit_home_view(conn, user_id=user_id)
    if callback_data == "sw:pedit:done":
        return exit_sandbox_profile_edit(conn, user_id=user_id)
    if callback_data == "sw:pedit:apply":
        return _apply_view(conn, user_id=user_id)
    if callback_data == "sw:pedit:cancelinput":
        session = _session(conn, user_id)
        if session is None:
            raise SandboxProfileEditError("Sandbox profile edit session expired")
        session["pending_field_key"] = None
        session["pending_field_label"] = None
        section_id = str(session.get("field_picker_section") or "")
        _save_session(conn, user_id, session)
        return (
            section_edit_view(conn, user_id=user_id, section_id=section_id)
            if section_id
            else edit_home_view(conn, user_id=user_id)
        )
    if callback_data.startswith("sw:pedit:s:"):
        return section_edit_view(
            conn,
            user_id=user_id,
            section_id=callback_data.split(":", 3)[3],
        )
    if callback_data.startswith("sw:pedit:f:"):
        return field_prompt_view(
            conn,
            user_id=user_id,
            index=int(callback_data.split(":", 3)[3]),
        )
    raise SandboxProfileEditError("Unknown Sandbox profile edit destination")


__all__ = [
    "enter_sandbox_profile_edit",
    "exit_sandbox_profile_edit",
    "handle_sandbox_profile_edit_text",
    "sandbox_profile_edit_callback_view",
]

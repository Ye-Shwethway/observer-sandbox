from __future__ import annotations

import sqlite3
from pathlib import Path

from .creator_studio import (
    CreatorStudioError,
    active_draft,
    ai_draft,
    approve_draft,
    cancel_draft,
    manual_draft,
    reroll_draft,
)

_NEXT_INPUT_KEYBOARD: list[list[dict[str, str]]] | None = None


def _session(conn: sqlite3.Connection, user_id: int):
    row = conn.execute(
        """SELECT creation_type,input_mode,expected_input
        FROM creation_sandbox_studio_sessions
        WHERE sandbox_id='creator-default' AND user_id=?""",
        (int(user_id),),
    ).fetchone()
    return dict(row) if row else None


def _begin_session(conn: sqlite3.Connection, user_id: int, creation_type: str, input_mode: str) -> None:
    if creation_type not in {"character", "location"}:
        raise CreatorStudioError("Unsupported creation type")
    if input_mode not in {"manual", "ai_generated"}:
        raise CreatorStudioError("Unsupported Creator Studio input mode")
    expected = "name" if input_mode == "manual" else "description"
    conn.execute(
        """
        INSERT INTO creation_sandbox_studio_sessions(
            sandbox_id,user_id,creation_type,input_mode,expected_input
        ) VALUES('creator-default',?,?,?,?)
        ON CONFLICT(sandbox_id,user_id) DO UPDATE SET
            creation_type=excluded.creation_type,
            input_mode=excluded.input_mode,
            expected_input=excluded.expected_input,
            updated_at=CURRENT_TIMESTAMP
        """,
        (int(user_id), creation_type, input_mode, expected),
    )
    conn.commit()


def _clear_session(conn: sqlite3.Connection, user_id: int) -> None:
    conn.execute(
        "DELETE FROM creation_sandbox_studio_sessions WHERE sandbox_id='creator-default' AND user_id=?",
        (int(user_id),),
    )
    conn.commit()


def _prompt_view(creation_type: str, input_mode: str):
    icon = "👤" if creation_type == "character" else "📍"
    if input_mode == "manual":
        instruction = f"Send the {creation_type} name as your next message."
        example = "Example: Elias Thorne" if creation_type == "character" else "Example: Lakeside Cabin"
    else:
        instruction = f"Describe the {creation_type} you want the Creation AI to draft."
        example = "You can write naturally and include as much detail as useful."
    return (
        f"{icon} {creation_type.upper()} · {'MANUAL' if input_mode == 'manual' else 'AI DRAFT'}\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{instruction}\n\n{example}\n\n"
        "Your next ordinary text message will be used only for this Creator Studio step.",
        [
            [{"text": "← Change Method", "callback_data": f"sw:cs:type:{creation_type}"}],
            [{"text": "✕ Cancel", "callback_data": "sw:cs:input:cancel"}],
        ],
    )


def _install_input_router() -> None:
    """Install one bounded plain-text router into the existing single-threaded Telegram adapter."""
    from . import telegram_bot as base
    from .db import connect, migrate

    if getattr(base.handle_command, "_creator_studio_input_router", False):
        return
    original_handle = base.handle_command
    original_keyboard = base._command_keyboard

    def routed_handle(db_path: str | Path, *, user_id: int, text: str) -> str:
        global _NEXT_INPUT_KEYBOARD
        raw = (text or "").strip()
        if raw.startswith("/"):
            if raw.split()[0].split("@", 1)[0].lower() == "/cancel":
                with connect(db_path) as conn:
                    migrate(conn)
                    if _session(conn, user_id):
                        _clear_session(conn, user_id)
                        view, keyboard = studio_home_view(conn, user_id)
                        _NEXT_INPUT_KEYBOARD = keyboard
                        return "✕ Creator Studio input cancelled.\n\n" + view
            return original_handle(db_path, user_id=user_id, text=text)
        if base._user_role(user_id) != "owner":
            return original_handle(db_path, user_id=user_id, text=text)
        with connect(db_path) as conn:
            migrate(conn)
            session = _session(conn, user_id)
            if not session:
                return original_handle(db_path, user_id=user_id, text=text)
            try:
                if session["input_mode"] == "manual":
                    manual_draft(conn, user_id, session["creation_type"], raw)
                else:
                    ai_draft(conn, user_id, session["creation_type"], raw)
            except Exception as exc:
                view, keyboard = _prompt_view(session["creation_type"], session["input_mode"])
                _NEXT_INPUT_KEYBOARD = keyboard
                return f"Creator Studio input rejected: {exc}\n\n{view}"
            _clear_session(conn, user_id)
            view, keyboard = draft_preview_view(conn, user_id)
            _NEXT_INPUT_KEYBOARD = keyboard
            return view

    def routed_keyboard(command: str):
        global _NEXT_INPUT_KEYBOARD
        if _NEXT_INPUT_KEYBOARD is not None:
            keyboard = _NEXT_INPUT_KEYBOARD
            _NEXT_INPUT_KEYBOARD = None
            return keyboard
        return original_keyboard(command)

    routed_handle._creator_studio_input_router = True  # type: ignore[attr-defined]
    base.handle_command = routed_handle
    base._command_keyboard = routed_keyboard


def studio_home_view(conn: sqlite3.Connection, user_id: int):
    _install_input_router()
    draft = active_draft(conn, user_id)
    session = _session(conn, user_id)
    lines = [
        "🛠 CREATOR STUDIO",
        "━━━━━━━━━━━━━━━━━━",
        "Create safely in the isolated Creation Sandbox.",
        "Use the guided buttons below, or commands as optional shortcuts.",
    ]
    keyboard = [[{"text": "➕ Create", "callback_data": "sw:cs:create"}]]
    if session:
        lines.extend(["", f"Waiting for {session['expected_input']}: {session['creation_type'].title()}"])
        keyboard.append([{"text": "✕ Cancel Input", "callback_data": "sw:cs:input:cancel"}])
    if draft:
        proposal = draft["proposal"]
        lines.extend([
            "",
            f"Active draft: {proposal['identity'].get('name', 'Unnamed')} · {draft['creation_type'].title()} · r{draft['revision']}",
        ])
        keyboard.append([{"text": "📋 Preview Draft", "callback_data": "sw:cs:preview"}])
    keyboard.extend([
        [{"text": "← Sandbox World", "callback_data": "nav:sandbox"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ])
    return "\n".join(lines), keyboard


def _create_type_view():
    return (
        "➕ CREATE IN SANDBOX\n━━━━━━━━━━━━━━━━━━\nChoose what you want to create.",
        [
            [
                {"text": "👤 Character", "callback_data": "sw:cs:type:character"},
                {"text": "📍 Location", "callback_data": "sw:cs:type:location"},
            ],
            [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
        ],
    )


def _method_view(creation_type: str):
    icon = "👤" if creation_type == "character" else "📍"
    return (
        f"{icon} CREATE {creation_type.upper()}\n━━━━━━━━━━━━━━━━━━\nChoose a creation method.",
        [
            [{"text": "✍️ Build Manually", "callback_data": f"sw:cs:input:{creation_type}:manual"}],
            [{"text": "✨ Generate with AI", "callback_data": f"sw:cs:input:{creation_type}:ai"}],
            [{"text": "← Creation Type", "callback_data": "sw:cs:create"}],
        ],
    )


def draft_preview_view(conn: sqlite3.Connection, user_id: int, *, notice: str | None = None):
    draft = active_draft(conn, user_id)
    if not draft:
        return (
            "🛠 CREATOR STUDIO\n━━━━━━━━━━━━━━━━━━\nNo active draft.",
            [[{"text": "← Creator Studio", "callback_data": "sw:studio"}]],
        )
    p = draft["proposal"]
    lines = [
        "📋 CREATION SANDBOX DRAFT",
        "━━━━━━━━━━━━━━━━━━",
        f"Type: {p['creation_type'].title()}",
        f"Name: {p['identity'].get('name', 'Unnamed')}",
        f"Mode: {'AI Draft' if draft['draft_mode'] == 'ai_generated' else 'Manual'}",
        f"Revision: {draft['revision']}",
        f"Scope: {p['target_scope']}",
    ]
    if p.get("properties"):
        lines.extend(["", "Properties"])
        for key, value in sorted(p["properties"].items()):
            lines.append(f"• {key.replace('_', ' ').title()}: {value}")
    if p.get("capabilities"):
        lines.extend(["", "Capabilities", "• " + ", ".join(p["capabilities"])])
    lines.extend([
        "",
        "Approval creates this object in Creation Sandbox only.",
        "Canonical transmigration remains a separate future validation boundary.",
    ])
    if notice:
        lines.extend(["", notice])
    keyboard = []
    if draft["draft_mode"] == "ai_generated":
        keyboard.append([{"text": "♻️ Reroll", "callback_data": "sw:cs:reroll"}])
    keyboard.extend([
        [{"text": "✅ Approve into Sandbox", "callback_data": "sw:cs:approve"}],
        [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
        [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
    ])
    return "\n".join(lines), keyboard


def studio_callback_view(conn: sqlite3.Connection, user_id: int, callback_data: str):
    _install_input_router()
    if callback_data == "sw:studio":
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:create":
        _clear_session(conn, user_id)
        return _create_type_view()
    if callback_data.startswith("sw:cs:type:"):
        creation_type = callback_data.rsplit(":", 1)[-1]
        if creation_type in {"character", "location"}:
            _clear_session(conn, user_id)
            return _method_view(creation_type)
        return _create_type_view()
    if callback_data.startswith("sw:cs:input:") and callback_data != "sw:cs:input:cancel":
        parts = callback_data.split(":")
        if len(parts) == 5 and parts[3] in {"character", "location"} and parts[4] in {"manual", "ai"}:
            mode = "manual" if parts[4] == "manual" else "ai_generated"
            _begin_session(conn, user_id, parts[3], mode)
            return _prompt_view(parts[3], mode)
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:input:cancel":
        _clear_session(conn, user_id)
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:preview":
        return draft_preview_view(conn, user_id)
    if callback_data == "sw:cs:reroll":
        try:
            reroll_draft(conn, user_id)
        except CreatorStudioError as exc:
            return draft_preview_view(conn, user_id, notice=f"Reroll rejected: {exc}")
        return draft_preview_view(conn, user_id, notice="♻️ AI draft rerolled. Review before approval.")
    if callback_data == "sw:cs:cancel":
        cancel_draft(conn, user_id)
        _clear_session(conn, user_id)
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:approve":
        try:
            obj = approve_draft(conn, user_id)
        except CreatorStudioError as exc:
            return draft_preview_view(conn, user_id, notice=f"Approval rejected: {exc}")
        name = obj["identity"].get("name", obj["object_id"])
        back = "sw:list:character" if obj["creation_type"] == "character" else "sw:list:location"
        return (
            "✅ SANDBOX CREATION APPROVED\n━━━━━━━━━━━━━━━━━━\n"
            f"{obj['creation_type'].title()}: {name}\n"
            f"ID: {obj['object_id']}\n\n"
            "Created in Creation Sandbox only. It is not canonical and not automatically running.",
            [
                [{"text": "🔎 View", "callback_data": f"sw:o:{obj['object_id']}"}],
                [{"text": "← List", "callback_data": back}],
                [{"text": "🛠 Creator Studio", "callback_data": "sw:studio"}],
            ],
        )
    raise KeyError(callback_data)


__all__ = ["draft_preview_view", "studio_callback_view", "studio_home_view"]

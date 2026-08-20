from __future__ import annotations

import sqlite3
from pathlib import Path

from .character_creation_policy import creation_field_keys
from .creator_draft_export import send_full_draft_document
from .creator_studio import (
    CreatorStudioError,
    active_draft,
    ai_draft,
    approve_draft,
    cancel_draft,
    manual_draft,
    reroll_draft,
)
from .manual_character_creation import (
    ManualCharacterCreationError,
    manual_character_baseline_status,
    manual_character_draft,
    update_manual_character_collection,
    update_manual_character_field,
)
from .telegram_character_draft_profile import profile_page_view, profile_summary_lines

_NEXT_INPUT_KEYBOARD: list[list[dict[str, str]]] | None = None
_ROUTER_ORIGINAL_HANDLE = None
_ROUTER_ORIGINAL_KEYBOARD = None
_MANUAL_FIELD_PAGE_SIZE = 12
_MANUAL_SECTIONS = (
    ("identity", "👤", "Identity", ("identity",)),
    ("appearance", "🧬", "Appearance", ("appearance",)),
    ("body", "💪", "Body & Genetics", ("body", "genetics")),
    ("attributes", "⚡", "Attributes", ("raps_pa", "raps_ma", "raps_ia", "social", "raps_vc")),
    ("sexual", "♂️", "Sexual", ("sexual_anatomy", "raps_sa")),
    ("personality", "🧠", "Personality", ("personality",)),
    ("background", "📜", "Background & Training", ("background", "training")),
)
_COLLECTION_LABELS = {
    "skills": "🎯 Skills",
    "preferences": "❤️ Preferences",
    "hobbies": "🎨 Hobbies",
    "habits": "🔁 Habits",
    "compatibility_tags": "🏷 Compatibility Tags",
}


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


def _set_expected_input(conn: sqlite3.Connection, user_id: int, expected_input: str) -> None:
    conn.execute(
        """
        UPDATE creation_sandbox_studio_sessions
        SET creation_type='character',input_mode='manual',expected_input=?,updated_at=CURRENT_TIMESTAMP
        WHERE sandbox_id='creator-default' AND user_id=?
        """,
        (expected_input, int(user_id)),
    )
    if conn.execute("SELECT changes()").fetchone()[0] != 1:
        conn.execute(
            """
            INSERT INTO creation_sandbox_studio_sessions(
                sandbox_id,user_id,creation_type,input_mode,expected_input
            ) VALUES('creator-default',?,'character','manual',?)
            """,
            (int(user_id), expected_input),
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
        if creation_type == "character":
            example = "Example: Elias Thorne\nAfter the name, the guided profile builder opens before approval."
        else:
            example = "Example: Lakeside Cabin"
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


def _manual_section(section_id: str):
    return next((row for row in _MANUAL_SECTIONS if row[0] == section_id), None)


def _manual_fields(conn: sqlite3.Connection, section_id: str) -> list[dict[str, object]]:
    section = _manual_section(section_id)
    if section is None:
        raise CreatorStudioError("Unknown manual Character section")
    domains = set(section[3])
    allowed = creation_field_keys(conn)
    rows = conn.execute(
        """
        SELECT field_key,domain,label,data_type,unit
        FROM profile_field_definitions
        ORDER BY domain,field_key
        """
    ).fetchall()
    return [dict(row) for row in rows if str(row["domain"]) in domains and str(row["field_key"]) in allowed]


def _fmt_short(value: object) -> str:
    if value is None:
        return "—"
    if isinstance(value, float):
        return f"{value:g}"
    if isinstance(value, (dict, list)):
        text = str(value)
        return text if len(text) <= 24 else text[:21] + "…"
    text = str(value)
    return text if len(text) <= 24 else text[:21] + "…"


def manual_character_builder_view(
    conn: sqlite3.Connection,
    user_id: int,
    *,
    notice: str | None = None,
):
    draft = manual_character_draft(conn, user_id)
    p = draft["proposal"]
    profile = p["properties"]["character_profile"]
    values = dict(profile.get("values") or {})
    status = manual_character_baseline_status(conn, user_id)
    lines = [
        "✍️ MANUAL CHARACTER BUILD",
        "━━━━━━━━━━━━━━━━━━",
        f"Character: {p['identity'].get('name', 'Unnamed')}",
        f"Draft revision: {draft['revision']}",
        f"Required baseline: {status['complete']}/{status['total']}",
        f"Profile values represented: {len(values)}",
        "",
        "This uses the same creation-owned field registry and final Character profile structure as AI creation.",
        "Nothing is approved into Sandbox until the required baseline and shared validators pass.",
    ]
    if status["missing"]:
        labels = []
        for key in status["missing"][:5]:
            row = conn.execute("SELECT label FROM profile_field_definitions WHERE field_key=?", (key,)).fetchone()
            labels.append(str(row["label"]) if row else key)
        suffix = " …" if len(status["missing"]) > 5 else ""
        lines.extend(["", "Still required: " + ", ".join(labels) + suffix])
    else:
        lines.extend(["", "✅ Required manual baseline complete. Review the draft before approval."])
    if notice:
        lines.extend(["", notice])

    keyboard: list[list[dict[str, str]]] = []
    for index in range(0, len(_MANUAL_SECTIONS), 2):
        row = []
        for section_id, icon, label, _domains in _MANUAL_SECTIONS[index : index + 2]:
            row.append({"text": f"{icon} {label}", "callback_data": f"sw:cs:manual:s:{section_id}:0"})
        keyboard.append(row)
    keyboard.extend(
        [
            [
                {"text": "🎯 Skills", "callback_data": "sw:cs:manual:c:skills"},
                {"text": "❤️ Preferences", "callback_data": "sw:cs:manual:c:preferences"},
            ],
            [
                {"text": "🎨 Hobbies", "callback_data": "sw:cs:manual:c:hobbies"},
                {"text": "🔁 Habits", "callback_data": "sw:cs:manual:c:habits"},
            ],
            [{"text": "🏷 Compatibility Tags", "callback_data": "sw:cs:manual:c:compatibility_tags"}],
            [{"text": "📋 Review Draft", "callback_data": "sw:cs:preview"}],
            [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
            [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
        ]
    )
    return "\n".join(lines), keyboard


def _manual_section_view(conn: sqlite3.Connection, user_id: int, section_id: str, page: int = 0):
    draft = manual_character_draft(conn, user_id)
    profile = draft["proposal"]["properties"]["character_profile"]
    values = dict(profile.get("values") or {})
    fields = _manual_fields(conn, section_id)
    section = _manual_section(section_id)
    if section is None:
        return manual_character_builder_view(conn, user_id, notice="Unknown manual Character section.")
    total_pages = max(1, (len(fields) + _MANUAL_FIELD_PAGE_SIZE - 1) // _MANUAL_FIELD_PAGE_SIZE)
    page = max(0, min(int(page), total_pages - 1))
    start = page * _MANUAL_FIELD_PAGE_SIZE
    chunk = fields[start : start + _MANUAL_FIELD_PAGE_SIZE]
    lines = [
        f"{section[1]} MANUAL CHARACTER · {section[2].upper()}",
        "━━━━━━━━━━━━━━━━━━",
        f"Page {page + 1}/{total_pages}",
        "Select a creation-owned field. Existing values can be revised before approval.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for offset, field in enumerate(chunk):
        absolute_index = start + offset
        key = str(field["field_key"])
        label = str(field["label"])
        current = _fmt_short(values.get(key))
        keyboard.append(
            [{"text": f"✏️ {label}: {current}"[:60], "callback_data": f"sw:cs:manual:f:{section_id}:{absolute_index}"}]
        )
    nav: list[dict[str, str]] = []
    if page > 0:
        nav.append({"text": "← Previous", "callback_data": f"sw:cs:manual:s:{section_id}:{page - 1}"})
    if page + 1 < total_pages:
        nav.append({"text": "Next →", "callback_data": f"sw:cs:manual:s:{section_id}:{page + 1}"})
    if nav:
        keyboard.append(nav)
    keyboard.append([{"text": "← Manual Character", "callback_data": "sw:cs:manual:home"}])
    return "\n".join(lines), keyboard


def _manual_field_prompt(conn: sqlite3.Connection, user_id: int, section_id: str, index: int):
    fields = _manual_fields(conn, section_id)
    if index < 0 or index >= len(fields):
        return _manual_section_view(conn, user_id, section_id, 0)
    field = fields[index]
    field_key = str(field["field_key"])
    _set_expected_input(conn, user_id, f"manual-field:{field_key}")
    _install_input_router()
    expected = str(field["data_type"])
    unit = str(field["unit"] or "")
    examples = {
        "date": "Example: 2001-05-12",
        "boolean": "Example: true or false",
        "json": 'Send valid JSON, for example: ["scar over left eyebrow"]',
        "number": "Send a number only.",
        "integer": "Send a whole number only.",
        "text": "Send the text value.",
    }
    return (
        "✏️ MANUAL CHARACTER FIELD\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{field['label']}\n"
        f"Field: {field_key}\n"
        f"Expected: {expected}" + (f" · {unit}" if unit else "") + "\n\n"
        f"{examples.get(expected, 'Send the new value.')}\n"
        "The value is validated before it enters the draft.",
        [
            [{"text": "✕ Cancel Input", "callback_data": "sw:cs:manual:cancelinput"}],
            [{"text": "← Manual Character", "callback_data": "sw:cs:manual:home"}],
        ],
    )


def _manual_collection_prompt(conn: sqlite3.Connection, user_id: int, collection: str):
    if collection not in _COLLECTION_LABELS:
        return manual_character_builder_view(conn, user_id, notice="Unknown Character collection.")
    _set_expected_input(conn, user_id, f"manual-collection:{collection}")
    _install_input_router()
    examples = {
        "skills": '[{"skill_key":"navigation","category":null,"score":75,"tier":null,"experience":0}]',
        "preferences": '[{"preference_type":"like","subject":"quiet mornings","intensity":70}]',
        "hobbies": '[{"name":"hiking","proficiency":60,"frequency":"weekly","enjoyment":85}]',
        "habits": '[{"name":"morning stretching","description":null,"frequency":"daily","strength":70}]',
        "compatibility_tags": '["realistic-human","modern-setting"]',
    }
    return (
        f"{_COLLECTION_LABELS[collection]} · MANUAL CHARACTER\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "Send the complete JSON array for this collection. Sending [] clears it.\n\n"
        f"Example:\n{examples[collection]}\n\n"
        "The collection is validated before it enters the draft.",
        [
            [{"text": "✕ Cancel Input", "callback_data": "sw:cs:manual:cancelinput"}],
            [{"text": "← Manual Character", "callback_data": "sw:cs:manual:home"}],
        ],
    )


def _manual_retry_view(conn: sqlite3.Connection, user_id: int, expected: str, error: Exception):
    if expected.startswith("manual-field:"):
        field_key = expected.split(":", 1)[1]
        row = conn.execute(
            "SELECT label,data_type,unit FROM profile_field_definitions WHERE field_key=?",
            (field_key,),
        ).fetchone()
        label = str(row["label"]) if row else field_key
        return (
            f"Manual Character value rejected: {error}\n\n"
            f"✏️ {label}\nSend a corrected value, or cancel this input.",
            [
                [{"text": "✕ Cancel Input", "callback_data": "sw:cs:manual:cancelinput"}],
                [{"text": "← Manual Character", "callback_data": "sw:cs:manual:home"}],
            ],
        )
    if expected.startswith("manual-collection:"):
        collection = expected.split(":", 1)[1]
        return (
            f"Manual Character collection rejected: {error}\n\n"
            f"Send a corrected JSON array for {_COLLECTION_LABELS.get(collection, collection)}, or cancel this input.",
            [
                [{"text": "✕ Cancel Input", "callback_data": "sw:cs:manual:cancelinput"}],
                [{"text": "← Manual Character", "callback_data": "sw:cs:manual:home"}],
            ],
        )
    session = _session(conn, user_id)
    if session:
        return _prompt_view(str(session["creation_type"]), str(session["input_mode"]))
    return studio_home_view(conn, user_id)


def _restore_input_router() -> None:
    global _ROUTER_ORIGINAL_HANDLE, _ROUTER_ORIGINAL_KEYBOARD
    from . import telegram_bot as base
    if _ROUTER_ORIGINAL_HANDLE is not None:
        base.handle_command = _ROUTER_ORIGINAL_HANDLE
    if _ROUTER_ORIGINAL_KEYBOARD is not None:
        base._command_keyboard = _ROUTER_ORIGINAL_KEYBOARD
    _ROUTER_ORIGINAL_HANDLE = None
    _ROUTER_ORIGINAL_KEYBOARD = None


def _install_input_router() -> None:
    """Install a one-shot plain-text router into the single-threaded Telegram adapter."""
    global _ROUTER_ORIGINAL_HANDLE, _ROUTER_ORIGINAL_KEYBOARD
    from . import telegram_bot as base
    from .db import connect, migrate

    if getattr(base.handle_command, "_creator_studio_input_router", False):
        return
    original_handle = base.handle_command
    original_keyboard = base._command_keyboard
    _ROUTER_ORIGINAL_HANDLE = original_handle
    _ROUTER_ORIGINAL_KEYBOARD = original_keyboard

    def routed_handle(db_path: str | Path, *, user_id: int, text: str) -> str:
        global _NEXT_INPUT_KEYBOARD
        raw = (text or "").strip()
        if raw.startswith("/"):
            if raw.split()[0].split("@", 1)[0].lower() == "/cancel":
                with connect(db_path) as conn:
                    migrate(conn)
                    session = _session(conn, user_id)
                    if session:
                        expected = str(session.get("expected_input") or "")
                        _clear_session(conn, user_id)
                        if expected.startswith("manual-"):
                            view, keyboard = manual_character_builder_view(conn, user_id, notice="✕ Manual input cancelled.")
                        else:
                            view, keyboard = studio_home_view(conn, user_id)
                        _NEXT_INPUT_KEYBOARD = keyboard
                        return view
            return original_handle(db_path, user_id=user_id, text=text)
        if base._user_role(user_id) != "owner":
            return original_handle(db_path, user_id=user_id, text=text)
        with connect(db_path) as conn:
            migrate(conn)
            session = _session(conn, user_id)
            if not session:
                return original_handle(db_path, user_id=user_id, text=text)
            expected = str(session.get("expected_input") or "")
            try:
                if expected.startswith("manual-field:"):
                    field_key = expected.split(":", 1)[1]
                    update_manual_character_field(conn, user_id, field_key, raw)
                    _clear_session(conn, user_id)
                    view, keyboard = manual_character_builder_view(conn, user_id, notice="✅ Draft field updated.")
                elif expected.startswith("manual-collection:"):
                    collection = expected.split(":", 1)[1]
                    update_manual_character_collection(conn, user_id, collection, raw)
                    _clear_session(conn, user_id)
                    view, keyboard = manual_character_builder_view(conn, user_id, notice="✅ Draft collection updated.")
                elif session["input_mode"] == "manual":
                    manual_draft(conn, user_id, session["creation_type"], raw)
                    _clear_session(conn, user_id)
                    if session["creation_type"] == "character":
                        view, keyboard = manual_character_builder_view(conn, user_id)
                    else:
                        view, keyboard = draft_preview_view(conn, user_id)
                else:
                    ai_draft(conn, user_id, session["creation_type"], raw)
                    _clear_session(conn, user_id)
                    view, keyboard = draft_preview_view(conn, user_id)
            except (CreatorStudioError, ManualCharacterCreationError, ValueError, TypeError) as exc:
                view, keyboard = _manual_retry_view(conn, user_id, expected, exc)
            _NEXT_INPUT_KEYBOARD = keyboard
            return view

    def routed_keyboard(command: str):
        global _NEXT_INPUT_KEYBOARD
        if _NEXT_INPUT_KEYBOARD is not None:
            keyboard = _NEXT_INPUT_KEYBOARD
            _NEXT_INPUT_KEYBOARD = None
            _restore_input_router()
            return keyboard
        return original_keyboard(command)

    routed_handle._creator_studio_input_router = True  # type: ignore[attr-defined]
    base.handle_command = routed_handle
    base._command_keyboard = routed_keyboard


def studio_home_view(conn: sqlite3.Connection, user_id: int):
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
        _install_input_router()
        lines.extend(["", f"Waiting for {session['expected_input']}: {session['creation_type'].title()}"])
        keyboard.append([{"text": "✕ Cancel Input", "callback_data": "sw:cs:input:cancel"}])
    if draft:
        proposal = draft["proposal"]
        lines.extend([
            "",
            f"Active draft: {proposal['identity'].get('name', 'Unnamed')} · {draft['creation_type'].title()} · r{draft['revision']}",
        ])
        if draft["creation_type"] == "character" and draft["draft_mode"] == "manual":
            keyboard.append([{"text": "✍️ Continue Manual Build", "callback_data": "sw:cs:manual:home"}])
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
    manual_text = "✍️ Build Manually"
    if creation_type == "character":
        manual_text = "✍️ Build Manually · Guided"
    return (
        f"{icon} CREATE {creation_type.upper()}\n━━━━━━━━━━━━━━━━━━\nChoose a creation method.",
        [
            [{"text": manual_text, "callback_data": f"sw:cs:input:{creation_type}:manual"}],
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
    profile = None
    manual_ready = True
    if p["creation_type"] == "character":
        candidate = p.get("properties", {}).get("character_profile")
        if isinstance(candidate, dict):
            profile = candidate
            lines.extend(profile_summary_lines(profile))
        if draft["draft_mode"] == "manual":
            status = manual_character_baseline_status(conn, user_id)
            manual_ready = bool(status["ready"])
            lines.extend([
                "",
                f"Manual required baseline: {status['complete']}/{status['total']}",
                "✅ Ready for final validation" if manual_ready else f"⚠️ {len(status['missing'])} required field(s) still missing",
            ])
    visible_properties = {
        key: value
        for key, value in (p.get("properties") or {}).items()
        if key != "character_profile"
    }
    if visible_properties:
        lines.extend(["", "Properties"])
        for key, value in sorted(visible_properties.items()):
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
    if profile is not None:
        keyboard.append([{"text": "👤 View Full Profile", "callback_data": "sw:cs:profile:0"}])
    if draft["creation_type"] == "character" and draft["draft_mode"] == "manual":
        keyboard.append([{"text": "✍️ Continue Manual Build", "callback_data": "sw:cs:manual:home"}])
    keyboard.append([{"text": "📄 Export Full Draft (.txt)", "callback_data": "sw:cs:export"}])
    if draft["draft_mode"] == "ai_generated":
        keyboard.append([{"text": "♻️ Reroll", "callback_data": "sw:cs:reroll"}])
    if manual_ready:
        keyboard.append([{"text": "✅ Approve into Sandbox", "callback_data": "sw:cs:approve"}])
    else:
        keyboard.append([{"text": "⚠️ Complete Required Baseline", "callback_data": "sw:cs:manual:home"}])
    keyboard.extend([
        [{"text": "✕ Cancel Draft", "callback_data": "sw:cs:cancel"}],
        [{"text": "← Creator Studio", "callback_data": "sw:studio"}],
    ])
    return "\n".join(lines), keyboard


def _approval_confirmation_view(conn: sqlite3.Connection, user_id: int):
    draft = active_draft(conn, user_id)
    if not draft:
        return draft_preview_view(conn, user_id)
    if draft["creation_type"] == "character" and draft["draft_mode"] == "manual":
        status = manual_character_baseline_status(conn, user_id)
        if not status["ready"]:
            return manual_character_builder_view(
                conn,
                user_id,
                notice="⚠️ Approval is locked until the required manual baseline is complete.",
            )
    proposal = draft["proposal"]
    name = proposal["identity"].get("name", "Unnamed")
    revision = int(draft["revision"])
    return (
        "⚠️ CONFIRM SANDBOX APPROVAL\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"{proposal['creation_type'].title()}: {name}\n"
        f"Draft revision: {revision}\n\n"
        "This will create the reviewed revision as an active object in Creation Sandbox.\n"
        "It will NOT become canonical, transmigrate to Real World, or start autonomy.\n\n"
        "Confirm only if this is the exact draft you intend to approve.",
        [
            [{"text": "✅ Confirm Approve", "callback_data": f"sw:cs:approve:confirm:{revision}"}],
            [{"text": "← Review Draft", "callback_data": "sw:cs:preview"}],
        ],
    )


def studio_callback_view(conn: sqlite3.Connection, user_id: int, callback_data: str):
    if callback_data == "sw:studio":
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:create":
        _clear_session(conn, user_id)
        _restore_input_router()
        return _create_type_view()
    if callback_data.startswith("sw:cs:type:"):
        creation_type = callback_data.rsplit(":", 1)[-1]
        if creation_type in {"character", "location"}:
            _clear_session(conn, user_id)
            _restore_input_router()
            return _method_view(creation_type)
        return _create_type_view()
    if callback_data.startswith("sw:cs:input:") and callback_data != "sw:cs:input:cancel":
        parts = callback_data.split(":")
        if len(parts) == 5 and parts[3] in {"character", "location"} and parts[4] in {"manual", "ai"}:
            mode = "manual" if parts[4] == "manual" else "ai_generated"
            _begin_session(conn, user_id, parts[3], mode)
            _install_input_router()
            return _prompt_view(parts[3], mode)
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:input:cancel":
        _clear_session(conn, user_id)
        _restore_input_router()
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:manual:home":
        _clear_session(conn, user_id)
        _restore_input_router()
        try:
            return manual_character_builder_view(conn, user_id)
        except ManualCharacterCreationError as exc:
            return draft_preview_view(conn, user_id, notice=str(exc))
    if callback_data == "sw:cs:manual:cancelinput":
        _clear_session(conn, user_id)
        _restore_input_router()
        return manual_character_builder_view(conn, user_id, notice="✕ Manual input cancelled.")
    if callback_data.startswith("sw:cs:manual:s:"):
        parts = callback_data.split(":")
        if len(parts) == 6:
            try:
                return _manual_section_view(conn, user_id, parts[4], int(parts[5]))
            except (ValueError, ManualCharacterCreationError) as exc:
                return manual_character_builder_view(conn, user_id, notice=f"Section unavailable: {exc}")
    if callback_data.startswith("sw:cs:manual:f:"):
        parts = callback_data.split(":")
        if len(parts) == 6:
            try:
                return _manual_field_prompt(conn, user_id, parts[4], int(parts[5]))
            except (ValueError, ManualCharacterCreationError) as exc:
                return manual_character_builder_view(conn, user_id, notice=f"Field unavailable: {exc}")
    if callback_data.startswith("sw:cs:manual:c:"):
        collection = callback_data.rsplit(":", 1)[-1]
        try:
            return _manual_collection_prompt(conn, user_id, collection)
        except ManualCharacterCreationError as exc:
            return manual_character_builder_view(conn, user_id, notice=f"Collection unavailable: {exc}")
    if callback_data == "sw:cs:preview":
        return draft_preview_view(conn, user_id)
    if callback_data == "sw:cs:export":
        try:
            filename = send_full_draft_document(conn, user_id)
        except Exception as exc:
            return draft_preview_view(conn, user_id, notice=f"Export failed: {exc}")
        return draft_preview_view(conn, user_id, notice=f"📄 Export sent: {filename}")
    if callback_data.startswith("sw:cs:profile:"):
        draft = active_draft(conn, user_id)
        if not draft or draft["creation_type"] != "character":
            return draft_preview_view(conn, user_id)
        profile = draft["proposal"].get("properties", {}).get("character_profile")
        if not isinstance(profile, dict):
            return draft_preview_view(conn, user_id)
        try:
            page = int(callback_data.rsplit(":", 1)[-1])
        except ValueError:
            page = 0
        return profile_page_view(profile, page)
    if callback_data == "sw:cs:reroll":
        try:
            reroll_draft(conn, user_id)
        except CreatorStudioError as exc:
            return draft_preview_view(conn, user_id, notice=f"Reroll rejected: {exc}")
        return draft_preview_view(conn, user_id, notice="♻️ AI draft rerolled. Review before approval.")
    if callback_data == "sw:cs:cancel":
        cancel_draft(conn, user_id)
        _clear_session(conn, user_id)
        _restore_input_router()
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:approve":
        return _approval_confirmation_view(conn, user_id)
    if callback_data.startswith("sw:cs:approve:confirm:"):
        try:
            expected_revision = int(callback_data.rsplit(":", 1)[-1])
        except ValueError:
            return draft_preview_view(conn, user_id, notice="Approval confirmation is invalid. Review the current draft again.")
        draft = active_draft(conn, user_id)
        if not draft:
            return draft_preview_view(conn, user_id)
        if int(draft["revision"]) != expected_revision:
            return draft_preview_view(
                conn,
                user_id,
                notice="⚠️ Draft changed after confirmation. Review the current revision before approving.",
            )
        try:
            obj = approve_draft(conn, user_id)
        except (CreatorStudioError, ManualCharacterCreationError) as exc:
            if draft["creation_type"] == "character" and draft["draft_mode"] == "manual":
                return manual_character_builder_view(conn, user_id, notice=f"Approval rejected: {exc}")
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


__all__ = [
    "draft_preview_view",
    "manual_character_builder_view",
    "studio_callback_view",
    "studio_home_view",
]

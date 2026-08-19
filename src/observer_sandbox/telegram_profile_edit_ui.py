from __future__ import annotations

import json
from typing import Any

from .autonomy import set_autonomy_paused
from .body_grade_target import BodyGradeTargetError, preview_body_grade_target
from .creator_profile_edit import (
    CreatorProfileEditError,
    apply_saved_proposal,
    preview_profile_edit,
    preview_section_grade_target,
    save_proposal,
)
from .profile_observer import profile_menu, profile_section
from .simulation import runtime_value, set_runtime_value

SESSION_PREFIX = "telegram_creator_profile_edit_session:"
UI_SENTINEL = "__OBSERVER_PROFILE_EDIT_UI__:"
GRADE_GROUPS = (
    ("body", "Body Measurements"),
    ("physical", "Physical Attributes"),
    ("mental", "Mental Attributes"),
    ("intellectual", "Intellectual Attributes"),
    ("verbal", "Verbal Charisma"),
    ("attributes", "All Attributes"),
    ("skills", "All Skills"),
)


def _session_key(user_id: int) -> str:
    return f"{SESSION_PREFIX}{int(user_id)}"


def _session(conn, user_id: int) -> dict[str, Any] | None:
    value = runtime_value(conn, _session_key(user_id), None)
    return dict(value) if isinstance(value, dict) else None


def _save_session(conn, user_id: int, session: dict[str, Any] | None) -> None:
    set_runtime_value(conn, _session_key(user_id), session)
    conn.commit()


def _character_name(conn, character_id: str) -> str:
    data = profile_menu(conn, character_id, role="owner")
    return str(data["character"]["name"])


def _pause_banner(session: dict[str, Any]) -> list[str]:
    return [
        "⏸ UNIVERSE PAUSED — CREATOR EDIT MODE",
        "━━━━━━━━━━━━━━━━━━",
        "Character simulation is frozen while profile editing is open.",
        "Finish with ‘Done Editing’ to restore the universe to its previous pause state.",
        "",
    ]


def enter_profile_edit(conn, *, user_id: int, character_id: str) -> tuple[str, list[list[dict[str, str]]]]:
    name = _character_name(conn, character_id)
    existing = _session(conn, user_id)
    if existing is not None and existing.get("character_id") == character_id:
        return edit_home_view(conn, user_id=user_id)
    if existing is not None and existing.get("character_id") != character_id:
        exit_profile_edit(conn, user_id=user_id)
    was_paused = bool(runtime_value(conn, "paused", False))
    if not was_paused:
        set_autonomy_paused(conn, True, actor_id=character_id)
    session = {
        "character_id": character_id,
        "character_name": name,
        "was_paused_before_edit": was_paused,
        "pending_field_key": None,
        "pending_field_label": None,
    }
    _save_session(conn, user_id, session)
    return edit_home_view(conn, user_id=user_id)


def exit_profile_edit(conn, *, user_id: int) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(conn, user_id)
    if session is None:
        return "✏️ No active Creator profile edit session.", [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]]
    character_id = str(session["character_id"])
    was_paused = bool(session.get("was_paused_before_edit", False))
    if not was_paused and bool(runtime_value(conn, "paused", False)):
        set_autonomy_paused(conn, False, actor_id=character_id)
    _save_session(conn, user_id, None)
    state = "remains paused" if was_paused else "resumed"
    return (
        f"✅ CREATOR PROFILE EDIT MODE CLOSED\n━━━━━━━━━━━━━━━━━━\n"
        f"{session.get('character_name') or character_id} profile editing finished.\n"
        f"Universe {state}; the pre-edit pause state was restored.",
        [[{"text": "← Profile", "callback_data": f"prof:{character_id}"}], [{"text": "⌂ Observer Home", "callback_data": "nav:home"}]],
    )


def edit_home_view(conn, *, user_id: int) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(conn, user_id)
    if session is None:
        return "✏️ No active Creator profile edit session.", [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]]
    character_id = str(session["character_id"])
    data = profile_menu(conn, character_id, role="owner")
    lines = _pause_banner(session) + [
        f"✏️ {session.get('character_name') or character_id} · PROFILE EDIT",
        "Choose a profile section or a grade target.",
        "Raw values remain authoritative; grades are recalculated from the edited values.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    sections = data.get("sections") or []
    for index in range(0, len(sections), 2):
        row = []
        for section in sections[index:index + 2]:
            row.append({"text": f"{section['icon']} {section['label']}", "callback_data": f"pedit:s:{section['id']}"})
        keyboard.append(row)
    keyboard.append([{"text": "🎯 Grade Target", "callback_data": "pedit:grades"}])
    keyboard.append([{"text": "✅ Done Editing", "callback_data": "pedit:done"}])
    return "\n".join(lines), keyboard


def _writable_profile_items(conn, character_id: str, section_id: str) -> list[dict[str, Any]]:
    data = profile_section(conn, character_id, section_id, role="owner")
    items: list[dict[str, Any]] = []
    for item in data.get("content") or []:
        field_key = str(item.get("field_key") or "")
        if item.get("kind") != "field" or not field_key or str(item.get("mode") or "") == "derived":
            continue
        represented = conn.execute(
            "SELECT 1 FROM character_profile_values WHERE entity_id=? AND field_key=? UNION ALL SELECT 1 FROM fields WHERE entity_id=? AND field_key=? LIMIT 1",
            (character_id, field_key, character_id, field_key),
        ).fetchone()
        if represented is None:
            continue
        items.append(item)
    return items


def section_edit_view(conn, *, user_id: int, section_id: str) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(conn, user_id)
    if session is None:
        return "✏️ Edit session expired. Re-enter Profile → Edit Profile.", [[{"text": "⌂ Observer Home", "callback_data": "nav:home"}]]
    character_id = str(session["character_id"])
    data = profile_section(conn, character_id, section_id, role="owner")
    items = _writable_profile_items(conn, character_id, section_id)
    session["field_picker_section"] = section_id
    session["field_picker_keys"] = [str(item["field_key"]) for item in items]
    _save_session(conn, user_id, session)
    lines = _pause_banner(session) + [
        f"{data['section']['icon']} {session.get('character_name')} · {str(data['section']['label']).upper()} EDIT",
        "Select a represented field to change.",
    ]
    keyboard: list[list[dict[str, str]]] = []
    for index, item in enumerate(items):
        value = item.get("value")
        unit = str(item.get("unit") or "")
        value_text = f"{value} {unit}".strip()
        keyboard.append([{"text": f"✏️ {item.get('label')}: {value_text}"[:60], "callback_data": f"pedit:f:{index}"}])
    if not items:
        lines.append("No fields in this section are writable through the current profile editor contract.")
    if section_id == "body":
        keyboard.append([{"text": "🎯 Body Grade Target", "callback_data": "pedit:gg:body"}])
    keyboard.append([{"text": "← Edit Profile", "callback_data": "pedit:home"}])
    keyboard.append([{"text": "✅ Done Editing", "callback_data": "pedit:done"}])
    return "\n".join(lines), keyboard


def field_prompt_view(conn, *, user_id: int, index: int) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(conn, user_id)
    if session is None:
        raise CreatorProfileEditError("Profile edit session expired")
    keys = list(session.get("field_picker_keys") or [])
    if index < 0 or index >= len(keys):
        raise CreatorProfileEditError("Unknown profile field selection")
    field_key = str(keys[index])
    character_id = str(session["character_id"])
    row = conn.execute(
        "SELECT label,data_type,unit FROM profile_field_definitions WHERE field_key=?",
        (field_key,),
    ).fetchone()
    if row is None:
        raise CreatorProfileEditError("Profile field definition disappeared")
    session["pending_field_key"] = field_key
    session["pending_field_label"] = str(row["label"])
    _save_session(conn, user_id, session)
    lines = _pause_banner(session) + [
        f"✏️ EDIT {str(row['label']).upper()}",
        f"Field: {field_key}",
        f"Expected: {row['data_type']}" + (f" · {row['unit']}" if row["unit"] else ""),
        "",
        "Send the new value as your next Telegram message.",
        "Nothing changes until you review and press Apply.",
    ]
    return "\n".join(lines), [[{"text": "✕ Cancel Field Edit", "callback_data": "pedit:cancelinput"}], [{"text": "✅ Done Editing", "callback_data": "pedit:done"}]]


def grade_groups_view(conn, *, user_id: int) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(conn, user_id)
    if session is None:
        raise CreatorProfileEditError("Profile edit session expired")
    lines = _pause_banner(session) + ["🎯 GRADE TARGET", "Choose a compatible grading group to retarget."]
    keyboard = [[{"text": label, "callback_data": f"pedit:gg:{group}"}] for group, label in GRADE_GROUPS]
    keyboard.append([{"text": "← Edit Profile", "callback_data": "pedit:home"}])
    return "\n".join(lines), keyboard


def grade_choice_view(conn, *, user_id: int, group: str) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(conn, user_id)
    if session is None:
        raise CreatorProfileEditError("Profile edit session expired")
    label = dict(GRADE_GROUPS).get(group, group)
    detail = (
        "Body uses sex-aware aesthetic ratios and a deterministic inverse measurement solver. Preserve Shape is the default."
        if group == "body"
        else "Choose target grade. Preserve Shape is the default adjustment mode."
    )
    lines = _pause_banner(session) + [f"🎯 {label.upper()}", detail]
    keyboard = []
    for grade in ("E", "D", "C", "B", "A", "S"):
        keyboard.append([
            {"text": f"{grade} · Preserve", "callback_data": f"pedit:gt:{group}:{grade}:p"},
            {"text": f"{grade} · Normalize", "callback_data": f"pedit:gt:{group}:{grade}:n"},
        ])
    keyboard.append([{"text": "← Grade Target", "callback_data": "pedit:grades"}])
    return "\n".join(lines), keyboard


def _preview_view(conn, *, user_id: int, proposal: dict[str, Any]) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(conn, user_id)
    if session is None:
        raise CreatorProfileEditError("Profile edit session expired")
    token = save_proposal(conn, proposal, requested_by=f"telegram:{user_id}")
    lines = _pause_banner(session) + ["🔎 CREATOR PROFILE CHANGE PREVIEW"]
    if proposal.get("kind") in {"section_grade_target", "body_grade_target"}:
        old = proposal.get("old_aggregate") or {}
        new = proposal.get("new_aggregate") or {}
        lines.extend([
            f"Target: {proposal.get('group')} → Grade {proposal.get('target_grade')}",
            f"Mode: {proposal.get('mode')}",
            f"Overall: {old.get('grade')} {old.get('value')} → {new.get('grade')} {new.get('value')}",
        ])
        if proposal.get("kind") == "body_grade_target":
            coverage = proposal.get("new_coverage") or {}
            lines.extend([
                f"Reference: {proposal.get('reference_profile')}",
                f"Metric coverage: {coverage.get('active_metrics')}/{coverage.get('eligible_metrics')}",
                "",
                "Projected proportions:",
            ])
            for metric in proposal.get("new_metrics") or []:
                grade = metric.get("grade") or {}
                lines.append(
                    f"• {metric.get('label')}: {metric.get('value')} · {grade.get('grade') or '—'}"
                )
            health = proposal.get("health_context") or []
            if health:
                lines.extend(["", "Health context (not aesthetic score):"])
                for metric in health:
                    grade = metric.get("grade") or {}
                    lines.append(f"• {metric.get('label')}: {metric.get('value')} · {grade.get('grade') or '—'}")
            lines.extend(["", "Proposed measurements:"])
        else:
            lines.append("")
    for change in proposal.get("changes") or []:
        lines.append(f"• {change.get('label') or change.get('field_key')}: {change.get('old_value')} → {change.get('new_value')}")
    lines.extend(["", "⚠️ Apply will correct authoritative profile state and reconcile only dependent profile-derived state."])
    return "\n".join(lines), [
        [{"text": "✅ Apply Change", "callback_data": f"pedit:apply:{token}"}],
        [{"text": "✕ Cancel Preview", "callback_data": "pedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "pedit:done"}],
    ]


def _apply_view(conn, *, user_id: int, token: str) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(conn, user_id)
    if session is None:
        raise CreatorProfileEditError("Profile edit session expired")
    result = apply_saved_proposal(conn, token, requested_by=f"telegram:{user_id}")
    lines = _pause_banner(session) + [
        "✅ PROFILE UPDATE APPLIED",
        f"Character: {result['character_name']}",
        f"Changed values: {len(result.get('changes') or [])}",
    ]
    if result.get("target_grade"):
        aggregate = result.get("new_aggregate") or {}
        lines.append(f"Verified grade: {aggregate.get('grade')} ({aggregate.get('value')})")
    lines.extend(["", "Universe remains paused because Creator Edit Mode is still open."])
    return "\n".join(lines), [[{"text": "✏️ Continue Editing", "callback_data": "pedit:home"}], [{"text": "✅ Done Editing", "callback_data": "pedit:done"}]]


def handle_profile_edit_text(conn, *, user_id: int, text: str) -> tuple[str, list[list[dict[str, str]]]] | None:
    session = _session(conn, user_id)
    if session is None or not session.get("pending_field_key"):
        return None
    field_key = str(session["pending_field_key"])
    character_id = str(session["character_id"])
    proposal = preview_profile_edit(conn, character_id, field_key, text)
    session["pending_field_key"] = None
    session["pending_field_label"] = None
    _save_session(conn, user_id, session)
    return _preview_view(conn, user_id=user_id, proposal=proposal)


def profile_edit_callback_view(conn, *, user_id: int, callback_data: str) -> tuple[str, list[list[dict[str, str]]]] | None:
    if callback_data.startswith("pedit:enter:"):
        return enter_profile_edit(conn, user_id=user_id, character_id=callback_data.split(":", 2)[2])
    if not callback_data.startswith("pedit:"):
        return None
    if callback_data == "pedit:home":
        return edit_home_view(conn, user_id=user_id)
    if callback_data == "pedit:grades":
        return grade_groups_view(conn, user_id=user_id)
    if callback_data == "pedit:done":
        return exit_profile_edit(conn, user_id=user_id)
    if callback_data == "pedit:cancelinput":
        session = _session(conn, user_id)
        if session is None:
            raise CreatorProfileEditError("Profile edit session expired")
        session["pending_field_key"] = None
        session["pending_field_label"] = None
        section_id = str(session.get("field_picker_section") or "")
        _save_session(conn, user_id, session)
        return section_edit_view(conn, user_id=user_id, section_id=section_id) if section_id else edit_home_view(conn, user_id=user_id)
    if callback_data.startswith("pedit:s:"):
        return section_edit_view(conn, user_id=user_id, section_id=callback_data.split(":", 2)[2])
    if callback_data.startswith("pedit:f:"):
        return field_prompt_view(conn, user_id=user_id, index=int(callback_data.split(":", 2)[2]))
    if callback_data.startswith("pedit:gg:"):
        return grade_choice_view(conn, user_id=user_id, group=callback_data.split(":", 2)[2])
    if callback_data.startswith("pedit:gt:"):
        parts = callback_data.split(":")
        if len(parts) != 5:
            raise CreatorProfileEditError("Invalid grade target callback")
        _, _, group, grade, mode_code = parts
        session = _session(conn, user_id)
        if session is None:
            raise CreatorProfileEditError("Profile edit session expired")
        mode = "preserve_shape" if mode_code == "p" else "normalize"
        try:
            proposal = (
                preview_body_grade_target(conn, str(session["character_id"]), grade, mode=mode)
                if group == "body"
                else preview_section_grade_target(conn, str(session["character_id"]), group, grade, mode=mode)
            )
        except BodyGradeTargetError as exc:
            raise CreatorProfileEditError(str(exc)) from exc
        return _preview_view(conn, user_id=user_id, proposal=proposal)
    if callback_data.startswith("pedit:apply:"):
        return _apply_view(conn, user_id=user_id, token=callback_data.split(":", 2)[2])
    raise CreatorProfileEditError("Unknown Creator profile edit destination")


def pack_profile_edit_ui(view: tuple[str, list[list[dict[str, str]]]]) -> str:
    text, keyboard = view
    return UI_SENTINEL + json.dumps({"text": text, "keyboard": keyboard}, ensure_ascii=False, separators=(",", ":"))


def unpack_profile_edit_ui(value: str) -> tuple[str, list[list[dict[str, str]]]] | None:
    if not value.startswith(UI_SENTINEL):
        return None
    payload = json.loads(value[len(UI_SENTINEL):])
    return str(payload["text"]), list(payload.get("keyboard") or [])

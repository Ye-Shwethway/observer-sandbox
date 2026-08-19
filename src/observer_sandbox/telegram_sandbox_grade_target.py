from __future__ import annotations

import json
import sqlite3
from typing import Any

from .creator_profile_edit import CreatorProfileEditError
from .sandbox_grade_target import preview_sandbox_body_grade_target, preview_sandbox_section_grade_target
from .telegram_profile_edit_ui import GRADE_GROUPS
from .telegram_sandbox_profile_edit import (
    _save_session,
    get_sandbox_profile_edit_session,
    sandbox_profile_edit_callback_view as _base_callback_view,
)


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _banner() -> list[str]:
    return [
        "⏸ SANDBOX WORLD PAUSED — CREATOR EDIT MODE",
        "━━━━━━━━━━━━━━━━━━",
        "Only Sandbox World runtime is frozen while this profile edit is open.",
        "Real World runtime and canonical state are untouched.",
        "",
    ]


def _with_grade_target(view: tuple[str, list[list[dict[str, str]]]]) -> tuple[str, list[list[dict[str, str]]]]:
    text, keyboard = view
    rows = [list(row) for row in keyboard]
    if not any(button.get("callback_data") == "sw:pedit:grades" for row in rows for button in row):
        insert_at = max(0, len(rows) - 1)
        rows.insert(insert_at, [{"text": "🎯 Grade Target", "callback_data": "sw:pedit:grades"}])
    return text.replace("Choose a represented profile section and field.", "Choose a profile section or a grade target."), rows


def _session(user_id: int) -> dict[str, Any]:
    value = get_sandbox_profile_edit_session(user_id=user_id)
    if value is None:
        raise CreatorProfileEditError("Sandbox profile edit session expired")
    return value


def grade_groups_view(*, user_id: int) -> tuple[str, list[list[dict[str, str]]]]:
    _session(user_id)
    lines = _banner() + ["🎯 GRADE TARGET", "Choose a compatible grading group to retarget."]
    keyboard = [[{"text": label, "callback_data": f"sw:pedit:gg:{group}"}] for group, label in GRADE_GROUPS]
    keyboard.append([{"text": "← Edit Profile", "callback_data": "sw:pedit:home"}])
    return "\n".join(lines), keyboard


def grade_choice_view(*, user_id: int, group: str) -> tuple[str, list[list[dict[str, str]]]]:
    _session(user_id)
    label = dict(GRADE_GROUPS).get(group, group)
    detail = (
        "Body uses sex-aware aesthetic ratios and a deterministic inverse measurement solver. Preserve Shape is the default."
        if group == "body"
        else "Choose target grade. Preserve Shape is the default adjustment mode."
    )
    lines = _banner() + [f"🎯 {label.upper()}", detail]
    keyboard = []
    for grade in ("E", "D", "C", "B", "A", "S"):
        keyboard.append([
            {"text": f"{grade} · Preserve", "callback_data": f"sw:pedit:gt:{group}:{grade}:p"},
            {"text": f"{grade} · Normalize", "callback_data": f"sw:pedit:gt:{group}:{grade}:n"},
        ])
    keyboard.append([{"text": "← Grade Target", "callback_data": "sw:pedit:grades"}])
    return "\n".join(lines), keyboard


def _preview_view(conn: sqlite3.Connection, *, user_id: int, proposal: dict[str, Any]) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(user_id)
    proposal = dict(proposal)
    proposal["sandbox_id"] = str(session["sandbox_id"])
    session["pending_proposal"] = proposal
    _save_session(user_id, session)
    old = proposal.get("old_aggregate") or {}
    new = proposal.get("new_aggregate") or {}
    lines = _banner() + [
        "🔎 SANDBOX PROFILE CHANGE PREVIEW",
        f"Target: {proposal.get('group')} → Grade {proposal.get('target_grade')}",
        f"Mode: {proposal.get('mode')}",
        f"Overall: {old.get('grade')} {old.get('value')} → {new.get('grade')} {new.get('value')}",
    ]
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
            lines.append(f"• {metric.get('label')}: {metric.get('value')} · {grade.get('grade') or '—'}")
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
    lines.extend(["", "⚠️ Apply changes Sandbox state only. Real World remains unchanged."])
    return "\n".join(lines), [
        [{"text": "✅ Apply Change", "callback_data": "sw:pedit:gapply"}],
        [{"text": "✕ Cancel Preview", "callback_data": "sw:pedit:home"}],
        [{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}],
    ]


def _current(conn: sqlite3.Connection, object_id: str, change: dict[str, Any]) -> Any:
    if change.get("store") == "skill":
        key = str(change["field_key"]).split(":", 1)[1]
        row = conn.execute("SELECT score FROM creation_sandbox_character_skills WHERE object_id=? AND skill_key=?", (object_id, key)).fetchone()
        return None if row is None else float(row["score"])
    row = conn.execute("SELECT value_json FROM creation_sandbox_profile_values WHERE object_id=? AND field_key=?", (object_id, str(change["field_key"]))).fetchone()
    return None if row is None else json.loads(row["value_json"])


def _apply_grade_target(conn: sqlite3.Connection, *, user_id: int) -> tuple[str, list[list[dict[str, str]]]]:
    session = _session(user_id)
    proposal = session.get("pending_proposal")
    if not isinstance(proposal, dict) or proposal.get("kind") not in {"section_grade_target", "body_grade_target"}:
        raise CreatorProfileEditError("No Sandbox Grade Target proposal is awaiting Apply")
    object_id = str(proposal["character_id"])
    sandbox_id = str(session["sandbox_id"])
    changes = list(proposal.get("changes") or [])
    for change in changes:
        if _current(conn, object_id, change) != change.get("old_value"):
            raise CreatorProfileEditError(f"Proposal is stale for {change.get('field_key')}; preview again before applying")

    nested = conn.in_transaction
    savepoint = "sandbox_grade_target"
    conn.execute(f"SAVEPOINT {savepoint}" if nested else "BEGIN IMMEDIATE")
    try:
        for change in changes:
            if change.get("store") == "skill":
                skill_key = str(change["field_key"]).split(":", 1)[1]
                conn.execute(
                    "UPDATE creation_sandbox_character_skills SET score=?,updated_at=CURRENT_TIMESTAMP WHERE object_id=? AND skill_key=?",
                    (float(change["new_value"]), object_id, skill_key),
                )
            else:
                conn.execute(
                    "UPDATE creation_sandbox_profile_values SET value_json=?,authority='creator',source='creator-sandbox-grade-target-v1',updated_at=CURRENT_TIMESTAMP WHERE object_id=? AND field_key=?",
                    (_json(change["new_value"]), object_id, str(change["field_key"])),
                )
            if conn.execute("SELECT changes()").fetchone()[0] != 1:
                raise CreatorProfileEditError(f"Sandbox Grade Target field disappeared: {change.get('field_key')}")
        row = conn.execute("SELECT revision FROM creation_sandboxes WHERE sandbox_id=?", (sandbox_id,)).fetchone()
        if row is None:
            raise CreatorProfileEditError("Sandbox namespace disappeared during Grade Target apply")
        previous_revision = int(row["revision"])
        revision = previous_revision + 1
        conn.execute("UPDATE creation_sandboxes SET revision=?,updated_at=CURRENT_TIMESTAMP WHERE sandbox_id=?", (revision, sandbox_id))
        conn.execute(
            "INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json) VALUES(?,?,'sandbox_profile_grade_target_applied',?)",
            (sandbox_id, object_id, _json({
                "group": proposal.get("group"), "target_grade": proposal.get("target_grade"), "mode": proposal.get("mode"),
                "changes": [{"field_key": c.get("field_key"), "old_value": c.get("old_value"), "new_value": c.get("new_value")} for c in changes],
                "requested_by": f"telegram:{int(user_id)}", "previous_revision": previous_revision, "revision": revision,
                "source": "creator-sandbox-grade-target-v1",
            })),
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
    aggregate = proposal.get("new_aggregate") or {}
    lines = _banner() + [
        "✅ PROFILE UPDATE APPLIED",
        f"Character: {session.get('character_name') or object_id}",
        f"Changed values: {len(changes)}",
        f"Verified grade: {aggregate.get('grade')} ({aggregate.get('value')})",
        f"Sandbox revision: {previous_revision} → {revision}",
        "",
        "Sandbox World remains paused because Creator Edit Mode is still open.",
        "Real World canonical/runtime state was not changed.",
    ]
    return "\n".join(lines), [[{"text": "✏️ Continue Editing", "callback_data": "sw:pedit:home"}], [{"text": "✅ Done Editing", "callback_data": "sw:pedit:done"}]]


def sandbox_profile_edit_callback_view(conn: sqlite3.Connection, *, user_id: int, callback_data: str):
    if callback_data == "sw:pedit:grades":
        return grade_groups_view(user_id=user_id)
    if callback_data.startswith("sw:pedit:gg:"):
        return grade_choice_view(user_id=user_id, group=callback_data.split(":", 3)[3])
    if callback_data.startswith("sw:pedit:gt:"):
        parts = callback_data.split(":")
        if len(parts) != 6:
            raise CreatorProfileEditError("Invalid Sandbox Grade Target destination")
        group, grade, mode_code = parts[3], parts[4], parts[5]
        mode = "preserve_shape" if mode_code == "p" else "normalize"
        session = _session(user_id)
        object_id = str(session["character_id"])
        proposal = (
            preview_sandbox_body_grade_target(conn, object_id, grade, mode=mode)
            if group == "body"
            else preview_sandbox_section_grade_target(conn, object_id, group, grade, mode=mode)
        )
        return _preview_view(conn, user_id=user_id, proposal=proposal)
    if callback_data == "sw:pedit:gapply":
        return _apply_grade_target(conn, user_id=user_id)
    view = _base_callback_view(conn, user_id=user_id, callback_data=callback_data)
    if view is not None and (callback_data.startswith("sw:pedit:enter:") or callback_data == "sw:pedit:home"):
        return _with_grade_target(view)
    return view


__all__ = ["sandbox_profile_edit_callback_view"]

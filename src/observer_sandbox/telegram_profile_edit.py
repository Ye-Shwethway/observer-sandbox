from __future__ import annotations

from typing import Any

from .creator_profile_edit import (
    CreatorProfileEditError,
    apply_saved_proposal,
    preview_profile_edit,
    preview_section_grade_target,
    save_proposal,
)


def _fmt_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.6f}".rstrip("0").rstrip(".")
    return str(value)


def _grade_text(payload: dict[str, Any] | None) -> str:
    if not isinstance(payload, dict) or not payload.get("grade"):
        return "—"
    return f"{payload['grade']} · {payload.get('label') or ''}".rstrip(" ·")


def _preview_text(proposal: dict[str, Any], token: str) -> str:
    kind = str(proposal.get("kind") or "")
    lines = ["✏️ CREATOR PROFILE PREVIEW", "━━━━━━━━━━━━━━━━━━"]
    if kind == "section_grade_target":
        lines.extend([
            f"Target: {proposal.get('group')} → Grade {proposal.get('target_grade')} ({proposal.get('target_label')})",
            f"Mode: {proposal.get('mode')}",
            f"Overall: {proposal.get('old_aggregate', {}).get('grade')} {proposal.get('old_aggregate', {}).get('value')} → {proposal.get('new_aggregate', {}).get('grade')} {proposal.get('new_aggregate', {}).get('value')}",
            "",
        ])
    for change in proposal.get("changes") or []:
        old_grade = _grade_text(change.get("old_grade"))
        new_grade = _grade_text(change.get("new_grade"))
        grade_suffix = "" if old_grade == "—" and new_grade == "—" else f" · {old_grade} → {new_grade}"
        lines.append(
            f"• {change.get('label') or change.get('field_key')}: "
            f"{_fmt_value(change.get('old_value'))} → {_fmt_value(change.get('new_value'))}{grade_suffix}"
        )
    lines.extend([
        "",
        f"Apply: /profileapply {token}",
        "Cancel: do nothing; unapplied previews have no character-state effect.",
    ])
    return "\n".join(lines)


def profile_edit_command(conn, *, character_id: str, field_key: str, raw_value: str, requested_by: str) -> str:
    proposal = preview_profile_edit(conn, character_id, field_key, raw_value)
    token = save_proposal(conn, proposal, requested_by=requested_by)
    return _preview_text(proposal, token)


def profile_grade_command(
    conn,
    *,
    character_id: str,
    group: str,
    grade: str,
    mode: str,
    requested_by: str,
) -> str:
    normalized_mode = {"preserve": "preserve_shape", "preserve-shape": "preserve_shape"}.get(mode, mode)
    proposal = preview_section_grade_target(conn, character_id, group, grade, mode=normalized_mode)
    token = save_proposal(conn, proposal, requested_by=requested_by)
    return _preview_text(proposal, token)


def profile_apply_command(conn, *, token: str, requested_by: str) -> str:
    result = apply_saved_proposal(conn, token, requested_by=requested_by)
    lines = [
        "✅ CREATOR PROFILE UPDATE APPLIED",
        "━━━━━━━━━━━━━━━━━━",
        f"Character: {result['character_name']}",
        f"Changed values: {len(result.get('changes') or [])}",
    ]
    if result.get("target_grade"):
        aggregate = result.get("new_aggregate") or {}
        lines.append(
            f"Target grade: {result['target_grade']} · verified aggregate {aggregate.get('grade')} ({aggregate.get('value')})"
        )
    retired = len(result.get("retired_profile_self_knowledge") or [])
    if retired:
        lines.append(f"Reconciled stale self-knowledge: {retired}")
    lines.extend([
        "Profile grading will now derive from the new raw values.",
        "Progression/stat-notification baselines were re-anchored; this Creator edit is not reported as earned progress.",
    ])
    return "\n".join(lines)


def profile_edit_usage() -> str:
    return (
        "✏️ CREATOR PROFILE EDIT\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "/profileedit <character_id> <field_key> <value>\n"
        "/profilegrade <character_id> <group> <grade> [preserve|normalize]\n"
        "/profileapply <preview_token>\n\n"
        "Examples:\n"
        "/profileedit char_darian raps_pa.strength 82\n"
        "/profilegrade char_darian physical B preserve\n\n"
        "Edits are preview-first. Grades remain derived from raw values."
    )


__all__ = [
    "CreatorProfileEditError",
    "profile_apply_command",
    "profile_edit_command",
    "profile_edit_usage",
    "profile_grade_command",
]

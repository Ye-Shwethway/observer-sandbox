from __future__ import annotations

import sqlite3

from .creator_studio import (
    CreatorStudioError,
    active_draft,
    approve_draft,
    cancel_draft,
    reroll_draft,
)


def studio_home_view(conn: sqlite3.Connection, user_id: int):
    draft = active_draft(conn, user_id)
    lines = [
        "🛠 CREATOR STUDIO",
        "━━━━━━━━━━━━━━━━━━",
        "Create safely in the isolated Creation Sandbox.",
        "Nothing becomes canonical from this Studio.",
        "",
        "Manual draft:",
        "/create character <name>",
        "/create location <name>",
        "",
        "AI-assisted draft:",
        "/createai character <description>",
        "/createai location <description>",
    ]
    keyboard = [
        [
            {"text": "👤 Character", "callback_data": "sw:cs:help:character"},
            {"text": "📍 Location", "callback_data": "sw:cs:help:location"},
        ],
    ]
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
    if callback_data == "sw:studio":
        return studio_home_view(conn, user_id)
    if callback_data == "sw:cs:preview":
        return draft_preview_view(conn, user_id)
    if callback_data.startswith("sw:cs:help:"):
        kind = callback_data.rsplit(":", 1)[-1]
        if kind not in {"character", "location"}:
            return studio_home_view(conn, user_id)
        icon = "👤" if kind == "character" else "📍"
        return (
            f"{icon} CREATE {kind.upper()}\n━━━━━━━━━━━━━━━━━━\n"
            f"Manual: /create {kind} <name>\n"
            f"AI Draft: /createai {kind} <description>\n\n"
            "Both paths create a preview first. Nothing is written to the sandbox object registry until explicit approval.",
            [[{"text": "← Creator Studio", "callback_data": "sw:studio"}]],
        )
    if callback_data == "sw:cs:reroll":
        try:
            reroll_draft(conn, user_id)
        except CreatorStudioError as exc:
            return draft_preview_view(conn, user_id, notice=f"Reroll rejected: {exc}")
        return draft_preview_view(conn, user_id, notice="♻️ AI draft rerolled. Review before approval.")
    if callback_data == "sw:cs:cancel":
        cancel_draft(conn, user_id)
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

from __future__ import annotations

import json
import os
import re
import urllib.request
from typing import Any

from .creator_studio import active_draft


def _display(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", str(value or "").lower()).strip("-")
    return text or "draft"


def render_full_draft_text(conn, user_id: int) -> tuple[str, str]:
    draft = active_draft(conn, user_id)
    if not draft:
        raise ValueError("No active Creator Studio draft")
    proposal = draft["proposal"]
    name = str(proposal.get("identity", {}).get("name") or "unnamed")
    creation_type = _slug(str(proposal.get("creation_type") or "draft"))
    safe_name = _slug(name)
    filename = f"creator-studio-{creation_type}-{safe_name}-r{draft['revision']}.txt"

    lines = [
        "CREATION SANDBOX DRAFT",
        "=" * 72,
        f"Type: {str(proposal['creation_type']).title()}",
        f"Name: {name}",
        f"Mode: {'AI Draft' if draft['draft_mode'] == 'ai_generated' else 'Manual'}",
        f"Revision: {draft['revision']}",
        f"Scope: {proposal['target_scope']}",
        "",
    ]

    profile = proposal.get("properties", {}).get("character_profile")
    if isinstance(profile, dict):
        values = dict(profile.get("values") or {})
        lines.extend(["CHARACTER PROFILE VALUES", "-" * 72])
        for key in sorted(values):
            lines.append(f"{key}: {_display(values[key])}")

        for title, key, formatter in (
            ("SKILLS", "skills", lambda item: f"{item.get('skill_key')} | category={item.get('category')} | score={item.get('score')} | tier={item.get('tier')} | experience={item.get('experience')}"),
            ("PREFERENCES", "preferences", lambda item: f"{item.get('preference_type')}: {item.get('subject')} | intensity={item.get('intensity')}"),
            ("HOBBIES", "hobbies", lambda item: f"{item.get('name')} | proficiency={item.get('proficiency')} | frequency={item.get('frequency')} | enjoyment={item.get('enjoyment')}"),
            ("HABITS", "habits", lambda item: f"{item.get('name')} | {item.get('description')} | frequency={item.get('frequency')} | strength={item.get('strength')}"),
        ):
            lines.extend(["", title, "-" * 72])
            items = profile.get(key) or []
            if items:
                lines.extend(formatter(dict(item)) for item in items if isinstance(item, dict))
            else:
                lines.append("(none)")

    visible_properties = {
        key: value
        for key, value in (proposal.get("properties") or {}).items()
        if key != "character_profile"
    }
    lines.extend(["", "PROPERTIES", "-" * 72])
    if visible_properties:
        for key in sorted(visible_properties):
            lines.append(f"{key}: {_display(visible_properties[key])}")
    else:
        lines.append("(none)")

    lines.extend(["", "CAPABILITIES", "-" * 72])
    capabilities = proposal.get("capabilities") or []
    lines.extend(str(value) for value in capabilities) if capabilities else lines.append("(none)")

    lines.extend(["", "RELATIONSHIPS", "-" * 72])
    relationships = proposal.get("relationships") or []
    lines.extend(_display(value) for value in relationships) if relationships else lines.append("(none)")

    lines.extend(["", "PROVENANCE", "-" * 72])
    for key, value in sorted((proposal.get("provenance") or {}).items()):
        lines.append(f"{key}: {_display(value)}")

    lines.extend([
        "",
        "BOUNDARY",
        "-" * 72,
        "This is a Creation Sandbox draft only.",
        "It is not canonical and has not been transmigrated or started.",
    ])
    return filename, "\n".join(lines) + "\n"


def send_full_draft_document(conn, user_id: int) -> str:
    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("Telegram bot token is not configured")
    filename, text = render_full_draft_text(conn, user_id)
    boundary = "----ObserverSandboxDraftBoundary7MA4YWxkTrZu0gW"
    body = bytearray()

    def field(name: str, value: str) -> None:
        body.extend(f"--{boundary}\r\n".encode())
        body.extend(f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode())
        body.extend(value.encode("utf-8"))
        body.extend(b"\r\n")

    field("chat_id", str(int(user_id)))
    field("caption", "📄 Full Creator Studio draft export")
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(f'Content-Disposition: form-data; name="document"; filename="{filename}"\r\n'.encode())
    body.extend(b"Content-Type: text/plain; charset=utf-8\r\n\r\n")
    body.extend(text.encode("utf-8"))
    body.extend(b"\r\n")
    body.extend(f"--{boundary}--\r\n".encode())

    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendDocument",
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not payload.get("ok"):
        raise RuntimeError(str(payload.get("description") or "Telegram document upload failed"))
    return filename


__all__ = ["render_full_draft_text", "send_full_draft_document"]

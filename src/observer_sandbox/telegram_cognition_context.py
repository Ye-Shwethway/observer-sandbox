from __future__ import annotations

import textwrap
from datetime import datetime
from typing import Any

from .cognition_context_snapshots import cognition_context_snapshots


PAGE_CONTENT_LIMIT = 3000
_VALUE_WRAP = 420

_LABELS = {
    "action_options": "Available Action Options",
    "available_actions": "Available Action Vocabulary",
    "autonomy_policy": "Autonomy Policy",
    "capability_awareness": "Capability Awareness",
    "character": "Character Context",
    "decision_correction": "Decision Correction",
    "decision_signals": "Decision Signals",
    "meal_choice_context": "Meal Choice Context",
    "object_familiarity": "Object Familiarity",
    "recent_events": "Recent Events",
    "resource_awareness": "Resource Awareness",
    "solo_sexual_regulation": "Solo Regulation",
    "training_load_guard": "Training Load Guard",
}


def _label(key: Any) -> str:
    raw = str(key)
    if raw in _LABELS:
        return _LABELS[raw]
    return raw.replace(".", " · ").replace("_", " ").strip().title()


def _scalar(value: Any) -> str:
    if value is None:
        return "None"
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, float):
        return f"{value:.3f}".rstrip("0").rstrip(".")
    return str(value)


def _wrapped(prefix: str, value: Any, *, indent: int) -> list[str]:
    text = _scalar(value)
    initial = " " * indent + prefix
    subsequent = " " * (indent + 2)
    return textwrap.wrap(
        text,
        width=_VALUE_WRAP,
        initial_indent=initial,
        subsequent_indent=subsequent,
        break_long_words=True,
        break_on_hyphens=False,
    ) or [initial]


def _human_lines(value: Any, *, key: str | None = None, depth: int = 0) -> list[str]:
    indent = depth * 2
    lines: list[str] = []
    if key is not None:
        title = _label(key)
        if isinstance(value, (dict, list)):
            lines.append(" " * indent + title)
            indent += 2
            depth += 1
        else:
            return _wrapped(f"• {title}: ", value, indent=indent)

    if isinstance(value, dict):
        if not value:
            lines.append(" " * indent + "• Empty")
            return lines
        for child_key, child_value in value.items():
            lines.extend(_human_lines(child_value, key=str(child_key), depth=depth))
        return lines

    if isinstance(value, list):
        if not value:
            lines.append(" " * indent + "• None")
            return lines
        if all(not isinstance(item, (dict, list)) for item in value):
            for item in value:
                lines.extend(_wrapped("• ", item, indent=indent))
            return lines
        for index, item in enumerate(value, start=1):
            if isinstance(item, dict):
                lines.append(" " * indent + f"[{index}]")
                for child_key, child_value in item.items():
                    lines.extend(_human_lines(child_value, key=str(child_key), depth=depth + 1))
            elif isinstance(item, list):
                lines.append(" " * indent + f"[{index}]")
                lines.extend(_human_lines(item, depth=depth + 1))
            else:
                lines.extend(_wrapped("• ", item, indent=indent))
        return lines

    lines.extend(_wrapped("• ", value, indent=indent))
    return lines


def _pages(lines: list[str], limit: int = PAGE_CONTENT_LIMIT) -> list[str]:
    pages: list[str] = []
    current: list[str] = []
    current_len = 0
    for line in lines:
        addition = len(line) + (1 if current else 0)
        if current and current_len + addition > limit:
            pages.append("\n".join(current))
            current = []
            current_len = 0
        current.append(line)
        current_len += len(line) + (1 if current_len else 0)
    if current or not pages:
        pages.append("\n".join(current))
    return pages


def _fmt_time(value: Any) -> str:
    if not value:
        return "Unknown"
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).strftime("%d-%m-%Y %I:%M %p")
    except ValueError:
        return str(value)


def cognition_context_view(
    conn,
    character_id: str,
    *,
    slot: int = 1,
    page: int = 0,
) -> tuple[str, list[list[dict[str, str]]]]:
    row = conn.execute("SELECT name FROM entities WHERE id=? AND entity_type='character'", (character_id,)).fetchone()
    character_name = str(row[0]) if row is not None else character_id
    snapshots = cognition_context_snapshots(conn, character_id)
    slot = max(1, min(3, int(slot)))
    selected = snapshots[slot - 1] if slot <= len(snapshots) else None

    if selected is None:
        text = (
            f"🧠 {character_name} · COGNITION CONTEXT\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"Snapshot {slot}\n\nNo captured model injection yet."
        )
        return text, _keyboard(character_id, slot=slot, page=0, page_count=1)

    context = selected.get("context") if isinstance(selected.get("context"), dict) else {}
    body_lines: list[str] = []
    body_lines.extend(_human_lines(selected.get("available_actions") or [], key="available_actions"))
    body_lines.append("")
    for key, value in context.items():
        body_lines.extend(_human_lines(value, key=str(key)))
        body_lines.append("")
    while body_lines and body_lines[-1] == "":
        body_lines.pop()
    pages = _pages(body_lines)
    page = max(0, min(int(page), len(pages) - 1))

    injection = str(selected.get("injection_type") or "primary").replace("_", " ").title()
    provider = str(selected.get("provider_id") or "Unknown")
    model = str(selected.get("model_id") or "Unknown")
    latest = " · Latest" if slot == 1 else ""
    header = (
        f"🧠 {character_name} · COGNITION CONTEXT\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"Snapshot {slot}{latest} · {injection}\n"
        f"🕒 Sim Time  {_fmt_time(selected.get('sim_time'))}\n"
        f"🤖 Configured Model  {provider} / {model}\n"
        f"📄 Page      {page + 1}/{len(pages)}\n\n"
    )
    text = header + pages[page]
    return text, _keyboard(character_id, slot=slot, page=page, page_count=len(pages))


def _keyboard(
    character_id: str,
    *,
    slot: int,
    page: int,
    page_count: int,
) -> list[list[dict[str, str]]]:
    selectors: list[dict[str, str]] = []
    for index in (1, 2, 3):
        label = f"{'✓ ' if index == slot else ''}{index}{' · Latest' if index == 1 else ''}"
        selectors.append({"text": label, "callback_data": f"cog:{character_id}:{index}:0"})
    keyboard: list[list[dict[str, str]]] = [selectors]
    if page_count > 1:
        row: list[dict[str, str]] = []
        if page > 0:
            row.append({"text": "◀ Prev", "callback_data": f"cog:{character_id}:{slot}:{page - 1}"})
        row.append({"text": f"{page + 1}/{page_count}", "callback_data": f"cog:{character_id}:{slot}:{page}"})
        if page + 1 < page_count:
            row.append({"text": "Next ▶", "callback_data": f"cog:{character_id}:{slot}:{page + 1}"})
        keyboard.append(row)
    keyboard.append([{"text": "← Character", "callback_data": f"char:{character_id}"}])
    keyboard.append([{"text": "⌂ Observer Home", "callback_data": "nav:home"}])
    return keyboard

from __future__ import annotations

from typing import Any

from .profile_change_observer import attach_profile_display_deltas
from .profile_observer import profile_menu, profile_section
from .telegram_memory import memory_callback_view


_DOMAIN_LABELS = {
    "raps_pa": "Physical",
    "raps_ma": "Mental",
    "raps_ia": "Intellectual",
    "social": "Social",
    "raps_vc": "Verbal Charisma",
}


def character_keyboard(character_id: str) -> list[list[dict[str, str]]]:
    return [
        [{"text": "📖 Profile", "callback_data": f"prof:{character_id}"}],
        [{"text": "🗃️ Memory", "callback_data": f"mem:{character_id}:all:0"}],
        [{"text": "← Characters", "callback_data": "nav:characters"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]


def profile_callback_view(
    conn,
    callback_data: str,
    *,
    role: str = "allowed",
) -> tuple[str, list[list[dict[str, str]]]] | None:
    memory_view = memory_callback_view(conn, callback_data)
    if memory_view is not None:
        return memory_view
    if callback_data.startswith("prof:"):
        character_id = callback_data.split(":", 1)[1]
        data = profile_menu(conn, character_id, role=role)
        return _fmt_profile_menu(data), _profile_menu_keyboard(data)
    if callback_data.startswith("psec:"):
        parts = callback_data.split(":", 2)
        if len(parts) != 3:
            return None
        _, character_id, section_id = parts
        try:
            data = profile_section(conn, character_id, section_id, role=role)
            data = attach_profile_display_deltas(conn, character_id, data)
        except PermissionError:
            return (
                "🔒 Creator authority required for this profile section.",
                _profile_section_keyboard(character_id),
            )
        return _fmt_profile_section(data), _profile_section_keyboard(character_id)
    return None


def _fmt_profile_menu(data: dict[str, Any]) -> str:
    character = data["character"]
    lines = [
        f"📖 {character['name']} · PROFILE",
        "━━━━━━━━━━━━━━━━━━",
        "Read-only character profile",
        "",
        "Choose a section:",
    ]
    for section in data.get("sections") or []:
        lines.append(f"• {section['icon']} {section['label']}")
    return "\n".join(lines)


def _profile_menu_keyboard(data: dict[str, Any]) -> list[list[dict[str, str]]]:
    character_id = data["character"]["id"]
    keyboard: list[list[dict[str, str]]] = []
    sections = data.get("sections") or []
    for index in range(0, len(sections), 2):
        row: list[dict[str, str]] = []
        for section in sections[index:index + 2]:
            row.append(
                {
                    "text": f"{section['icon']} {section['label']}",
                    "callback_data": f"psec:{character_id}:{section['id']}",
                }
            )
        keyboard.append(row)
    keyboard.append([{"text": f"← {data['character']['name']}", "callback_data": f"char:{character_id}"}])
    keyboard.append([{"text": "⌂ Observer Home", "callback_data": "nav:home"}])
    return keyboard


def _profile_section_keyboard(character_id: str) -> list[list[dict[str, str]]]:
    return [
        [{"text": "← Profile", "callback_data": f"prof:{character_id}"}],
        [{"text": "← Character", "callback_data": f"char:{character_id}"}],
        [{"text": "⌂ Observer Home", "callback_data": "nav:home"}],
    ]


def _fmt_profile_section(data: dict[str, Any]) -> str:
    character = data["character"]
    section = data["section"]
    content = data.get("content") or []
    lines = [
        f"{section['icon']} {character['name']} · {str(section['label']).upper()}",
        "━━━━━━━━━━━━━━━━━━",
    ]
    if not content:
        lines.append("No represented data yet.")
        return "\n".join(lines)

    renderer = str(section.get("renderer") or "fields")
    if renderer == "grouped_attributes":
        return _fmt_attributes(lines, content, section)

    overall = _fmt_grade(section.get("overall_grade"))
    if overall:
        overall_delta = _fmt_delta(section.get("overall_delta"))
        lines.extend([f"Overall {overall}{f'  {overall_delta}' if overall_delta else ''}", ""])

    if renderer == "skills":
        for item in content:
            score = _fmt_number(item.get("score")) if item.get("score") is not None else "Represented"
            grade = _fmt_grade(item.get("grade"))
            if grade:
                score = f"{score} {grade}"
            delta = _fmt_delta(item.get("delta"))
            if delta:
                score = f"{score}  {delta}"
            category = str(item.get("category") or "").replace("_", " ").title()
            suffix = f" · {category}" if category else ""
            lines.append(f"• {item['label']}   {score}{suffix}")
        return "\n".join(lines)
    if renderer == "preferences":
        return _fmt_preferences(lines, content)

    for item in content:
        label = item.get("label") or str(item.get("field_key", "Field"))
        value = _fmt_profile_value(item)
        grade = _fmt_grade(item.get("grade"))
        if grade:
            value = f"{value} {grade}"
        delta = _fmt_delta(item.get("delta"))
        if delta:
            value = f"{value}  {delta}"
        lines.append(f"• {label}: {value}")
    return "\n".join(lines)


def _fmt_grade(grade: dict[str, Any] | None) -> str | None:
    if not grade or not grade.get("grade"):
        return None
    label = str(grade.get("label") or "").strip()
    suffix = f" · {label}" if label else ""
    return f"({grade['grade']}){suffix}"


def _fmt_delta(delta: dict[str, Any] | None) -> str | None:
    if not isinstance(delta, dict):
        return None
    amount = float(delta.get("delta") or 0.0)
    direction = "▲" if amount > 0 else "▼" if amount < 0 else "•"
    beneficial = delta.get("beneficial")
    quality = "🟢" if beneficial is True else "🔴" if beneficial is False else ""
    unit = str(delta.get("unit") or "")
    absolute = abs(amount)
    if unit == "in":
        value = f'{absolute:.2f}"'
    elif unit == "lb":
        value = f"{absolute:.2f} lb"
    elif unit == "percent":
        value = f"{absolute:.2f}%"
    elif unit == "ratio":
        value = f"{absolute:.3f}"
    else:
        value = f"{absolute:.2f}".rstrip("0").rstrip(".")
    text = f"{quality}{direction} {value}"
    if delta.get("grade_changed"):
        old_grade = delta.get("old_grade") or {}
        new_grade = delta.get("new_grade") or {}
        old_code = old_grade.get("grade") if isinstance(old_grade, dict) else None
        new_code = new_grade.get("grade") if isinstance(new_grade, dict) else None
        if old_code or new_code:
            text += f" · {old_code or '—'}→{new_code or '—'}"
    return text


def _fmt_attributes(
    lines: list[str],
    content: list[dict[str, Any]],
    section: dict[str, Any],
) -> str:
    overall = _fmt_grade(section.get("overall_grade"))
    if overall:
        overall_delta = _fmt_delta(section.get("overall_delta"))
        lines.extend([f"Overall {overall}{f'  {overall_delta}' if overall_delta else ''}", ""])

    group_grades = section.get("group_grades") or {}
    last_domain: str | None = None
    for item in content:
        domain = str(item.get("domain") or "")
        if domain != last_domain:
            if last_domain is not None:
                lines.append("")
            label = _DOMAIN_LABELS.get(domain, domain.replace("_", " ").title())
            group_grade = _fmt_grade(group_grades.get(domain))
            lines.append(f"{label}{f' {group_grade}' if group_grade else ''}")
            last_domain = domain
        value = _fmt_profile_value(item)
        grade = _fmt_grade(item.get("grade"))
        if grade:
            value = f"{value} {grade}"
        delta = _fmt_delta(item.get("delta"))
        if delta:
            value = f"{value}  {delta}"
        lines.append(f"• {item['label']}   {value}")
    return "\n".join(lines)


def _fmt_preferences(lines: list[str], content: list[dict[str, Any]]) -> str:
    likes = [item["subject"] for item in content if item.get("kind") == "preference" and item.get("preference_type") == "like"]
    dislikes = [item["subject"] for item in content if item.get("kind") == "preference" and item.get("preference_type") == "dislike"]
    hobbies = [item["name"] for item in content if item.get("kind") == "hobby"]
    habits = [item["name"] for item in content if item.get("kind") == "habit"]
    for label, values in (("Likes", likes), ("Dislikes", dislikes), ("Hobbies", hobbies), ("Habits", habits)):
        if values:
            lines.extend(["", label])
            lines.extend(f"• {value}" for value in values)
    return "\n".join(lines)


def _fmt_profile_value(item: dict[str, Any]) -> str:
    value = item.get("value")
    unit = item.get("unit")
    field_key = str(item.get("field_key") or "")

    if field_key == "body.height_in" and isinstance(value, (int, float)):
        inches = int(round(float(value)))
        return f"{inches // 12}'{inches % 12}\""
    if isinstance(value, list):
        return ", ".join(str(part) for part in value)
    if isinstance(value, dict):
        return "; ".join(f"{str(key).replace('_', ' ').title()}: {part}" for key, part in value.items())
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if unit == "ratio" and isinstance(value, (int, float)):
        return f"{float(value):.3f}".rstrip("0").rstrip(".")
    if field_key.startswith("body.") and unit == "in" and isinstance(value, (int, float)):
        return f'{float(value):.2f}"'

    formatted = _fmt_number(value)
    if unit == "in":
        return f'{formatted}"'
    if unit == "lb":
        return f"{formatted} lb"
    if unit == "percent":
        return f"{formatted}%"
    if unit == "years":
        return f"{formatted} years"
    return formatted


def _fmt_number(value: Any) -> str:
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        number = float(value)
        return f"{number:.1f}".rstrip("0").rstrip(".")
    return str(value)

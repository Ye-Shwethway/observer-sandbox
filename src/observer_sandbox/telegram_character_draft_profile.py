from __future__ import annotations

from typing import Any

PAGE_SIZE = 14


def _fmt(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:g}"
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if isinstance(value, dict):
        return ", ".join(f"{key}={item}" for key, item in value.items())
    return str(value)


def profile_summary_lines(profile: dict[str, Any]) -> list[str]:
    values = dict(profile.get("values") or {})
    lines = [
        "",
        "Character Profile",
        f"• Profile values: {len(values)}",
        f"• Skills: {len(profile.get('skills') or [])}",
        f"• Preferences: {len(profile.get('preferences') or [])}",
        f"• Hobbies: {len(profile.get('hobbies') or [])}",
        f"• Habits: {len(profile.get('habits') or [])}",
    ]
    for key in ("identity.sex", "identity.date_of_birth", "body.height_in", "body.weight_lb", "body.body_fat_pct"):
        if key in values:
            lines.append(f"• {key}: {_fmt(values[key])}")
    return lines


def profile_page_view(profile: dict[str, Any], page: int) -> tuple[str, list[list[dict[str, str]]]]:
    values = sorted(dict(profile.get("values") or {}).items())
    total_pages = max(1, (len(values) + PAGE_SIZE - 1) // PAGE_SIZE)
    page = max(0, min(int(page), total_pages - 1))
    start = page * PAGE_SIZE
    chunk = values[start : start + PAGE_SIZE]
    lines = [
        "👤 CHARACTER PROFILE DRAFT",
        "━━━━━━━━━━━━━━━━━━",
        f"Profile values · page {page + 1}/{total_pages}",
        "",
    ]
    lines.extend(f"• {key}: {_fmt(value)}" for key, value in chunk)
    if page == total_pages - 1:
        skills = profile.get("skills") or []
        preferences = profile.get("preferences") or []
        hobbies = profile.get("hobbies") or []
        habits = profile.get("habits") or []
        if skills:
            lines.extend(["", "Skills"])
            lines.extend(
                f"• {item.get('skill_key')} · {item.get('score') if item.get('score') is not None else '—'}"
                for item in skills[:10]
            )
            if len(skills) > 10:
                lines.append(f"• …and {len(skills) - 10} more")
        if preferences:
            lines.extend(["", "Preferences"])
            lines.extend(f"• {item.get('preference_type')}: {item.get('subject')}" for item in preferences[:8])
        if hobbies:
            lines.extend(["", "Hobbies", "• " + ", ".join(str(item.get("name")) for item in hobbies[:8])])
        if habits:
            lines.extend(["", "Habits", "• " + ", ".join(str(item.get("name")) for item in habits[:8])])
    nav: list[dict[str, str]] = []
    if page > 0:
        nav.append({"text": "← Previous", "callback_data": f"sw:cs:profile:{page - 1}"})
    if page + 1 < total_pages:
        nav.append({"text": "Next →", "callback_data": f"sw:cs:profile:{page + 1}"})
    keyboard: list[list[dict[str, str]]] = []
    if nav:
        keyboard.append(nav)
    keyboard.append([{"text": "← Draft Preview", "callback_data": "sw:cs:preview"}])
    return "\n".join(lines), keyboard


__all__ = ["profile_page_view", "profile_summary_lines"]

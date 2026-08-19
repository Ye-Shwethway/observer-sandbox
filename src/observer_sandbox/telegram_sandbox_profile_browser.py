from __future__ import annotations

from .sandbox_profile_observer import sandbox_profile_menu, sandbox_profile_section
from .telegram_profile_browser import _fmt_profile_menu, _fmt_profile_section


def _profile_menu_keyboard(data, *, role: str = "allowed"):
    character_id = data["character"]["id"]
    keyboard = []
    sections = data.get("sections") or []
    for index in range(0, len(sections), 2):
        row = []
        for section in sections[index : index + 2]:
            row.append(
                {
                    "text": f"{section['icon']} {section['label']}",
                    "callback_data": f"sw:psec:{character_id}:{section['id']}",
                }
            )
        keyboard.append(row)
    if role == "owner":
        keyboard.append(
            [
                {
                    "text": "✏️ Edit Profile",
                    "callback_data": f"sw:pedit:enter:{character_id}",
                }
            ]
        )
    keyboard.append(
        [
            {
                "text": f"← {data['character']['name']}",
                "callback_data": f"sw:o:{character_id}",
            }
        ]
    )
    keyboard.append([{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}])
    return keyboard


def _profile_section_keyboard(character_id: str):
    return [
        [{"text": "← Profile", "callback_data": f"sw:prof:{character_id}"}],
        [{"text": "← Character", "callback_data": f"sw:o:{character_id}"}],
        [{"text": "⌂ Sandbox World", "callback_data": "nav:sandbox"}],
    ]


def sandbox_profile_callback_view(conn, callback_data: str, *, role: str = "allowed"):
    if callback_data.startswith("sw:prof:"):
        character_id = callback_data.split(":", 2)[2]
        data = sandbox_profile_menu(conn, character_id, role=role)
        return _fmt_profile_menu(data), _profile_menu_keyboard(data, role=role)

    if callback_data.startswith("sw:psec:"):
        parts = callback_data.split(":", 3)
        if len(parts) != 4:
            return None
        _, _, character_id, section_id = parts
        try:
            data = sandbox_profile_section(conn, character_id, section_id, role=role)
            if section_id == "identity":
                # Keep Sandbox presentation in parity with the Real World profile:
                # biological sex remains represented but is not duplicated here.
                data["content"] = [
                    item
                    for item in data.get("content") or []
                    if item.get("field_key") != "identity.sex"
                ]
        except PermissionError:
            return (
                "🔒 Creator authority required for this profile section.",
                _profile_section_keyboard(character_id),
            )
        return _fmt_profile_section(data), _profile_section_keyboard(character_id)

    return None


__all__ = ["sandbox_profile_callback_view"]

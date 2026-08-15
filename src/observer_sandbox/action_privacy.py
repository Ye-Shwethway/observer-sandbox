from __future__ import annotations

from typing import Any


# Action sensitivity is a presentation/access policy, not a simulation rule.
# Keep it action-key driven so future sensitive actions can opt into the same
# observer boundary without character-specific branches.
ACTION_SENSITIVITY: dict[str, str] = {
    "self_satisfaction": "intimate",
}


def action_sensitivity(action_name: str | None) -> str:
    if not action_name:
        return "normal"
    return ACTION_SENSITIVITY.get(str(action_name), "normal")


def action_visible_to_role(action_name: str | None, role: str) -> bool:
    sensitivity = action_sensitivity(action_name)
    if sensitivity in {"private", "intimate"}:
        return role == "owner"
    return role in {"owner", "allowed", "authorized"}


def filter_action_rows(rows: list[dict[str, Any]], *, role: str) -> list[dict[str, Any]]:
    return [row for row in rows if action_visible_to_role(row.get("action"), role)]


def display_action_name(action_name: str | None, *, role: str) -> str | None:
    if action_visible_to_role(action_name, role):
        return action_name
    return None

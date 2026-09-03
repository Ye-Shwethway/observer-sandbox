from __future__ import annotations

from . import telegram_bot as _telegram_bot
from . import telegram_creator_studio_base as _base
from .telegram_creator_studio_item_extension import install_item_creator_studio_extension
from .telegram_creator_studio_item_retry_extension import install_item_retry_extension
from .telegram_creator_studio_item_review_extension import install_item_review_extension
from .telegram_creator_studio_location_extension import install_location_creator_studio_extension
from .telegram_creator_studio_location_feedback_extension import install_location_ai_feedback_extension
from .telegram_creator_studio_location_composition_extension import install_location_composition_creator_studio_extension
from .telegram_sandbox_item_edit_adapter import install_sandbox_item_edit_text_adapter
from .telegram_sandbox_location_edit_adapter import install_sandbox_location_edit_text_adapter

# Install transport compatibility adapters before telegram_creator_bot captures
# the legacy handle_command/_command_keyboard hooks. They only intercept text
# while an explicit Item/Location edit input session is active.
install_sandbox_item_edit_text_adapter(_telegram_bot)
install_sandbox_location_edit_text_adapter(_telegram_bot)
install_item_creator_studio_extension(_base)
install_item_retry_extension(_base)
install_item_review_extension(_base)
# Location reuses the fully-composed shared/Item Studio surfaces while owning the
# location-v2 Manual/AI routes. UX-only typing feedback is layered after routing.
install_location_creator_studio_extension(_base)
install_location_ai_feedback_extension(_base)
# L11.5 composes exact Location + Item members on top of the already-composed
# Location Studio surface while preserving the shared draft/export/approval shell.
install_location_composition_creator_studio_extension(_base)

for _name in _base.__all__:
    globals()[_name] = getattr(_base, _name)

__all__ = list(_base.__all__)


def _sync_public_overrides() -> None:
    # Keep the historical module-level patch/test contract intact even though
    # the implementation is split behind thin extension wrappers.
    for name in (
        "send_full_draft_document",
        "manual_draft",
        "ai_draft",
        "reroll_draft",
        "approve_draft",
    ):
        if name in globals():
            setattr(_base, name, globals()[name])


def _canonicalize_navigation_keyboard(keyboard):
    """Normalize legacy Creator Studio navigation callbacks at the public boundary."""
    if not isinstance(keyboard, list):
        return keyboard
    normalized = []
    for row in keyboard:
        if not isinstance(row, list):
            normalized.append(row)
            continue
        normalized_row = []
        for button in row:
            if isinstance(button, dict) and button.get("callback_data") == "sw:world":
                button = dict(button)
                button["callback_data"] = "nav:sandbox"
            normalized_row.append(button)
        normalized.append(normalized_row)
    return normalized


def studio_callback_view(conn, user_id: int, callback_data: str):
    _sync_public_overrides()
    text, keyboard = _base.studio_callback_view(conn, user_id, callback_data)
    return text, _canonicalize_navigation_keyboard(keyboard)


def __getattr__(name: str):
    return getattr(_base, name)

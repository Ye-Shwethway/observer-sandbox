from __future__ import annotations

from . import telegram_bot as _telegram_bot
from . import telegram_creator_studio_base as _base
from .telegram_creator_studio_item_extension import install_item_creator_studio_extension
from .telegram_creator_studio_item_retry_extension import install_item_retry_extension
from .telegram_creator_studio_item_review_extension import install_item_review_extension
from .telegram_creator_studio_location_extension import install_location_creator_studio_extension
from .telegram_sandbox_item_edit_adapter import install_sandbox_item_edit_text_adapter

# Install the transport compatibility adapter before telegram_creator_bot captures
# the legacy handle_command/_command_keyboard hooks. This keeps field-edit text
# routing available through the existing polling loop without widening its API.
install_sandbox_item_edit_text_adapter(_telegram_bot)
install_item_creator_studio_extension(_base)
install_item_retry_extension(_base)
install_item_review_extension(_base)
# Location is layered last so it can reuse the fully-composed shared/Item Studio
# surfaces while owning only the location-v2 Manual route.
install_location_creator_studio_extension(_base)

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


def studio_callback_view(conn, user_id: int, callback_data: str):
    _sync_public_overrides()
    return _base.studio_callback_view(conn, user_id, callback_data)


def __getattr__(name: str):
    return getattr(_base, name)

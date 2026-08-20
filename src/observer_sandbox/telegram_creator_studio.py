from __future__ import annotations

from . import telegram_creator_studio_base as _base
from .telegram_creator_studio_item_extension import install_item_creator_studio_extension
from .telegram_creator_studio_item_retry_extension import install_item_retry_extension

install_item_creator_studio_extension(_base)
install_item_retry_extension(_base)

for _name in _base.__all__:
    globals()[_name] = getattr(_base, _name)

__all__ = list(_base.__all__)


def _sync_public_overrides() -> None:
    # Keep the historical module-level patch/test contract intact even though
    # the implementation is split behind a thin extension wrapper.
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

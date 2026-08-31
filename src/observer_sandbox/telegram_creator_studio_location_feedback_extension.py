from __future__ import annotations

import os

from .creator_studio import active_draft


def _best_effort_typing(user_id: int) -> None:
    token = os.environ.get("OBSERVER_TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        return
    try:
        from . import telegram_bot

        telegram_bot._api(
            token,
            "sendChatAction",
            {"chat_id": int(user_id), "action": "typing"},
            timeout=10,
        )
    except Exception:
        # Transport feedback is UX-only and must never change Creation semantics.
        return


def install_location_ai_feedback_extension(base) -> None:
    original_ai_draft = base.ai_draft
    original_callback = base.studio_callback_view

    def ai_draft(conn, user_id, creation_type, prompt_text, **kwargs):
        session = base._session(conn, user_id)
        expected = str(session.get("expected_input") or "") if session else ""
        if creation_type == "location" and expected == "description":
            _best_effort_typing(user_id)
        return original_ai_draft(conn, user_id, creation_type, prompt_text, **kwargs)

    def studio_callback_view(conn, user_id: int, callback_data: str):
        if callback_data == "sw:cs:reroll":
            draft = active_draft(conn, user_id)
            if draft and draft.get("creation_type") == "location" and draft.get("draft_mode") == "ai_generated":
                _best_effort_typing(user_id)
        return original_callback(conn, user_id, callback_data)

    base.ai_draft = ai_draft
    base.studio_callback_view = studio_callback_view


__all__ = ["install_location_ai_feedback_extension"]

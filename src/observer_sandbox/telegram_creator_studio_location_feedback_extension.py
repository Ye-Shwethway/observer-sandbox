from __future__ import annotations

import os
import re

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


def _safe_error_reason(error: Exception) -> str:
    text = " ".join(str(error or "").split()).strip()
    if not text:
        text = error.__class__.__name__
    # Creator-facing diagnostics should remain useful without echoing likely
    # credentials from provider/transport exception bodies.
    text = re.sub(r"(?i)(authorization\s*:\s*bearer\s+)[^\s,;]+", r"\1[redacted]", text)
    text = re.sub(r"(?i)(api[-_ ]?key\s*[=:]\s*)[^\s,;]+", r"\1[redacted]", text)
    text = re.sub(r"\bsk-[A-Za-z0-9_-]{8,}\b", "[redacted-token]", text)
    return text[:700] + ("…" if len(text) > 700 else "")


def install_location_ai_feedback_extension(base) -> None:
    original_ai_draft = base.ai_draft
    original_callback = base.studio_callback_view
    original_retry_view = getattr(base, "_manual_retry_view", None)

    def ai_draft(conn, user_id, creation_type, prompt_text, **kwargs):
        session = base._session(conn, user_id)
        expected = str(session.get("expected_input") or "") if session else ""
        if creation_type == "location" and expected == "description":
            _best_effort_typing(user_id)
        return original_ai_draft(conn, user_id, creation_type, prompt_text, **kwargs)

    def retry_view(conn, user_id: int, expected: str, error: Exception):
        session = base._session(conn, user_id)
        if (
            session
            and str(session.get("creation_type") or "") == "location"
            and str(session.get("input_mode") or "") == "ai_generated"
            and expected == "description"
        ):
            _prompt, keyboard = base._prompt_view("location", "ai_generated")
            reason = _safe_error_reason(error)
            return (
                "⚠️ LOCATION AI DRAFT FAILED\n"
                "━━━━━━━━━━━━━━━━━━\n"
                f"Reason: {reason}\n\n"
                "Nothing was approved or materialized. Your Location AI input session is still open. "
                "You can send the prompt again after reviewing the reason, change method, or cancel.",
                keyboard,
            )
        if original_retry_view is not None:
            return original_retry_view(conn, user_id, expected, error)
        raise error

    def studio_callback_view(conn, user_id: int, callback_data: str):
        if callback_data == "sw:cs:reroll":
            draft = active_draft(conn, user_id)
            if draft and draft.get("creation_type") == "location" and draft.get("draft_mode") == "ai_generated":
                _best_effort_typing(user_id)
        return original_callback(conn, user_id, callback_data)

    base.ai_draft = ai_draft
    if original_retry_view is not None:
        base._manual_retry_view = retry_view
    base.studio_callback_view = studio_callback_view


__all__ = ["install_location_ai_feedback_extension"]

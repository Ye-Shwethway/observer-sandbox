from types import SimpleNamespace

from observer_sandbox.telegram_creator_studio_location_feedback_extension import (
    install_location_ai_feedback_extension,
)


def _base(session):
    def original_retry(_conn, _user_id, _expected, _error):
        return "ORIGINAL", []

    return SimpleNamespace(
        ai_draft=lambda *args, **kwargs: {"ok": True},
        studio_callback_view=lambda *args, **kwargs: ("CALLBACK", []),
        _manual_retry_view=original_retry,
        _session=lambda _conn, _user_id: session,
        _prompt_view=lambda creation_type, input_mode: (
            f"PROMPT {creation_type} {input_mode}",
            [[{"text": "Cancel", "callback_data": "sw:cs:input:cancel"}]],
        ),
    )


def test_location_ai_failure_surfaces_sanitized_reason_and_preserves_input_session():
    base = _base(
        {
            "creation_type": "location",
            "input_mode": "ai_generated",
            "expected_input": "description",
        }
    )
    install_location_ai_feedback_extension(base)

    text, keyboard = base._manual_retry_view(
        None,
        123,
        "description",
        ValueError("provider rejected schema api_key=super-secret sk-abcdefghijklmnop"),
    )

    assert "LOCATION AI DRAFT FAILED" in text
    assert "provider rejected schema" in text
    assert "super-secret" not in text
    assert "sk-abcdefghijklmnop" not in text
    assert "[redacted]" in text or "[redacted-token]" in text
    assert "session is still open" in text
    assert keyboard[0][0]["callback_data"] == "sw:cs:input:cancel"


def test_non_location_ai_failure_keeps_existing_retry_behavior():
    base = _base(
        {
            "creation_type": "character",
            "input_mode": "ai_generated",
            "expected_input": "description",
        }
    )
    install_location_ai_feedback_extension(base)

    assert base._manual_retry_view(None, 123, "description", ValueError("boom")) == ("ORIGINAL", [])

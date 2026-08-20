from __future__ import annotations

from observer_sandbox.ai_runtime import AIDecisionError
from observer_sandbox.telegram_error_diagnostics import safe_exception_diagnostic


def test_polling_command_failure_contract_keeps_exception_message():
    exc = AIDecisionError("HTTP 400: Bad Request: invalid response schema")
    reply = "Observer command failed safely:\n" + safe_exception_diagnostic(exc)

    assert reply == (
        "Observer command failed safely:\n"
        "AIDecisionError: HTTP 400: Bad Request: invalid response schema"
    )

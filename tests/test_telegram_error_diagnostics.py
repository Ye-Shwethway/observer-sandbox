from __future__ import annotations

import json

from observer_sandbox.ai_runtime import AIDecisionError
from observer_sandbox.telegram_error_diagnostics import safe_exception_diagnostic


def test_safe_exception_diagnostic_preserves_ai_detail():
    exc = AIDecisionError('HTTP 400: Bad Request: {"error":{"message":"Invalid response schema"}}')

    rendered = safe_exception_diagnostic(exc)

    assert rendered.startswith("AIDecisionError: HTTP 400: Bad Request")
    assert "Invalid response schema" in rendered


def test_safe_exception_diagnostic_includes_safe_parse_cause():
    try:
        json.loads("not-json")
    except json.JSONDecodeError as cause:
        exc = AIDecisionError("Provider returned unusable structured output")
        exc.__cause__ = cause

    rendered = safe_exception_diagnostic(exc)

    assert "AIDecisionError: Provider returned unusable structured output" in rendered
    assert "Cause: JSONDecodeError:" in rendered


def test_safe_exception_diagnostic_redacts_credentials_and_bounds_output():
    exc = AIDecisionError("Authorization: Bearer abcdefghijklmnop token=super-secret-value " + "x" * 3000)

    rendered = safe_exception_diagnostic(exc)

    assert "abcdefghijklmnop" not in rendered
    assert "super-secret-value" not in rendered
    assert "[REDACTED]" in rendered
    assert len(rendered) < 1900

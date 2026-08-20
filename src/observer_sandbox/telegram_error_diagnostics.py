from __future__ import annotations

import json
import re
from typing import Final


_MAX_DETAIL: Final[int] = 1800
_SECRET_PATTERNS: Final[tuple[re.Pattern[str], ...]] = (
    re.compile(r"(?i)(authorization\s*[:=]\s*bearer\s+)[^\s,}\]]+"),
    re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{8,}"),
    re.compile(r"(?i)((?:api[_-]?key|x-goog-api-key|token|secret)\s*[:=]\s*[\"']?)[^\s\"',}\]]+"),
)
_SAFE_CAUSES: Final[tuple[type[BaseException], ...]] = (
    json.JSONDecodeError,
    KeyError,
    TypeError,
    ValueError,
)


def _sanitize(text: str) -> str:
    value = str(text or "").strip()
    for pattern in _SECRET_PATTERNS:
        value = pattern.sub(r"\1[REDACTED]", value)
    value = re.sub(r"\s+", " ", value)
    if len(value) > _MAX_DETAIL:
        value = value[: _MAX_DETAIL - 1].rstrip() + "…"
    return value


def safe_exception_diagnostic(exc: BaseException) -> str:
    """Return a Creator-useful exception summary without secrets or traceback noise."""

    name = type(exc).__name__
    detail = _sanitize(str(exc))
    result = f"{name}: {detail}" if detail else name

    cause = exc.__cause__
    if isinstance(cause, _SAFE_CAUSES):
        cause_detail = _sanitize(str(cause))
        if cause_detail and cause_detail != detail:
            result += f"\nCause: {type(cause).__name__}: {cause_detail}"
    return result


__all__ = ["safe_exception_diagnostic"]

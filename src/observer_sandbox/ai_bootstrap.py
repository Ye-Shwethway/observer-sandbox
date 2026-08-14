from __future__ import annotations

import re
import sqlite3
from typing import Any

from .actor_selection import resolve_actor_id
from .ai import (
    AIConfigurationError,
    configure_provider,
    list_models,
    refresh_catalog,
    resolve_binding,
    set_binding,
)
from .secrets import load_runtime_secrets


_EXCLUDED_MODEL_TERMS = (
    "image",
    "tts",
    "audio",
    "embedding",
    "live",
    "computer-use",
)

_GROQ_EXCLUDED_MODEL_TERMS = (
    "whisper",
    "audio",
    "tts",
    "guard",
    "compound",
)


def _version_score(model_id: str) -> tuple[int, ...]:
    match = re.search(r"gemini-(\d+(?:\.\d+)*)", model_id.lower())
    if not match:
        return ()
    return tuple(int(part) for part in match.group(1).split("."))


def _gemini_candidate_score(model: dict[str, Any]) -> tuple[Any, ...]:
    model_id = str(model["model_id"]).lower()
    actions = {str(action).lower() for action in model.get("capabilities", {}).get("actions", [])}
    can_generate = "generatecontent" in actions or "generate_content" in actions
    excluded = any(term in model_id for term in _EXCLUDED_MODEL_TERMS)
    preview = any(term in model_id for term in ("preview", "experimental", "exp"))
    flash_lite = "flash-lite" in model_id or "flash_lite" in model_id
    flash = "flash" in model_id
    return (
        int(can_generate and not excluded),
        int(not preview),
        int(flash_lite),
        int(flash),
        _version_score(model_id),
        model_id,
    )


def _groq_candidate_score(model: dict[str, Any]) -> tuple[Any, ...]:
    model_id = str(model["model_id"]).lower()
    excluded = any(term in model_id for term in _GROQ_EXCLUDED_MODEL_TERMS)
    structured_family = "gpt-oss" in model_id
    lightweight = "20b" in model_id
    stable = not any(term in model_id for term in ("preview", "experimental", "exp"))
    context = int(model.get("context_window") or 0)
    return (
        int(not excluded and structured_family),
        int(stable),
        int(lightweight),
        context,
        model_id,
    )


def choose_gemini_flash_model(conn: sqlite3.Connection) -> dict[str, Any]:
    candidates = list_models(conn, "gemini")
    candidates = [
        model
        for model in candidates
        if _gemini_candidate_score(model)[0] == 1 and "flash" in str(model["model_id"]).lower()
    ]
    if not candidates:
        raise AIConfigurationError("Gemini catalog contains no usable Flash-family generateContent model")
    return max(candidates, key=_gemini_candidate_score)


def choose_groq_cognition_model(conn: sqlite3.Connection) -> dict[str, Any]:
    candidates = [model for model in list_models(conn, "groq") if _groq_candidate_score(model)[0] == 1]
    if not candidates:
        raise AIConfigurationError("Groq catalog contains no supported structured-output cognition model")
    return max(candidates, key=_groq_candidate_score)


def _preserved_existing_binding(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    role: str,
    force: bool,
) -> dict[str, Any] | None:
    existing = resolve_binding(conn, role=role, character_id=character_id)
    if existing is None or force:
        return None
    return {
        "ok": True,
        "changed": False,
        "reason": "existing_binding_preserved",
        "binding": existing,
    }


def bootstrap_gemini_cognition(
    conn: sqlite3.Connection,
    *,
    character_id: str | None = None,
    role: str = "cognition",
    force: bool = False,
) -> dict[str, Any]:
    """Provision Gemini for the selected/default actor when no explicit binding exists."""
    character_id = resolve_actor_id(conn, character_id)
    load_runtime_secrets()
    preserved = _preserved_existing_binding(
        conn,
        character_id=character_id,
        role=role,
        force=force,
    )
    if preserved is not None:
        return preserved

    configure_provider(conn, "gemini", enabled=True)
    model_count = refresh_catalog(conn, "gemini")
    selected = choose_gemini_flash_model(conn)
    set_binding(
        conn,
        scope_type="character",
        scope_id=character_id,
        role=role,
        provider_id="gemini",
        model_id=selected["model_id"],
        parameters={},
    )
    binding = resolve_binding(conn, role=role, character_id=character_id)
    return {
        "ok": True,
        "changed": True,
        "provider": "gemini",
        "catalog_model_count": model_count,
        "selected_model": selected["model_id"],
        "binding": binding,
    }


def bootstrap_groq_cognition(
    conn: sqlite3.Connection,
    *,
    character_id: str | None = None,
    role: str = "cognition",
    force: bool = False,
) -> dict[str, Any]:
    """Provision Groq for the selected/default actor when no explicit binding exists.

    Normal deployment must never overwrite a Creator-selected provider binding.
    `force=True` remains available only for an explicit administrative migration.
    """
    character_id = resolve_actor_id(conn, character_id)
    load_runtime_secrets()
    preserved = _preserved_existing_binding(
        conn,
        character_id=character_id,
        role=role,
        force=force,
    )
    if preserved is not None:
        return preserved

    configure_provider(conn, "groq", enabled=True)
    model_count = refresh_catalog(conn, "groq")
    selected = choose_groq_cognition_model(conn)
    set_binding(
        conn,
        scope_type="character",
        scope_id=character_id,
        role=role,
        provider_id="groq",
        model_id=selected["model_id"],
        parameters={},
    )
    binding = resolve_binding(conn, role=role, character_id=character_id)
    return {
        "ok": True,
        "changed": True,
        "provider": "groq",
        "catalog_model_count": model_count,
        "selected_model": selected["model_id"],
        "binding": binding,
    }

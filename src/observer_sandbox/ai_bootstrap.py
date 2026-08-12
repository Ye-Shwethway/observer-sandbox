from __future__ import annotations

import re
import sqlite3
from typing import Any

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
    # Prefer stable lightweight Flash models for the early sandbox, then stable
    # Flash, while keeping the exact model ID entirely catalog-driven.
    return (
        int(can_generate and not excluded),
        int(not preview),
        int(flash_lite),
        int(flash),
        _version_score(model_id),
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


def bootstrap_gemini_cognition(
    conn: sqlite3.Connection,
    *,
    character_id: str = "char_darian",
    role: str = "cognition",
    force: bool = False,
) -> dict[str, Any]:
    """Provision the first Gemini cognition binding without hard-coding a model ID.

    Existing bindings are preserved unless force=True so later Telegram/user model
    selection is not silently overwritten by deployments.
    """
    load_runtime_secrets()

    existing = resolve_binding(conn, role=role, character_id=character_id)
    if existing is not None and not force:
        return {
            "ok": True,
            "changed": False,
            "reason": "existing_binding_preserved",
            "binding": existing,
        }

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

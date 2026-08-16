from __future__ import annotations

import os
import sqlite3
from typing import Any

from .actor_runtime import actor_runtime, set_actor_runtime, set_retry
from .ai import AIConfigurationError, resolve_binding
from .ai_bootstrap import bootstrap_gemini_cognition
from .ai_runtime import AIDecisionError
from .event_log import record_event
from .model_decision import dry_run_model_decision
from .simulation import snapshot


RECOVERABLE_PROVIDER_ERRORS = (AIDecisionError, AIConfigurationError)


def _credential_present(name: str) -> bool:
    return bool(os.environ.get(name, "").strip())


def _clear_provider_retry_and_wake(conn: sqlite3.Connection, character_id: str) -> bool:
    runtime = actor_runtime(conn, character_id)
    retry = runtime["retry"] or {}
    if retry.get("last_error") not in {"AIDecisionError", "AIConfigurationError"}:
        return False
    set_retry(conn, character_id, None)
    if runtime["autonomy_enabled"] and runtime["pending_action_id"] is None:
        set_actor_runtime(conn, character_id, wake_reason="cognition_provider_recovered")
    conn.commit()
    return True


def _probe(conn: sqlite3.Connection, character_id: str, role: str) -> dict[str, Any]:
    return dry_run_model_decision(conn, character_id=character_id, role=role)


def ensure_cognition_live(
    conn: sqlite3.Connection,
    *,
    character_id: str,
    role: str = "cognition",
) -> dict[str, Any]:
    """Verify cognition with a real non-mutating decision call and recover provider binding if needed.

    The current explicit binding is always probed first. If it cannot produce a
    valid dry-run decision, this recovery currently prefers Gemini only when its
    credential is actually present. A replacement binding is accepted only after
    a second live dry-run succeeds. Provider retry/backoff is cleared only after
    that verified success, so an outage is never disguised as synthetic behavior.
    """
    before = resolve_binding(conn, role=role, character_id=character_id)
    if before is None:
        raise AIConfigurationError(f"No AI binding resolved for {character_id}/{role}")

    primary_error: str | None = None
    try:
        probe = _probe(conn, character_id, role)
        retry_cleared = _clear_provider_retry_and_wake(conn, character_id)
        return {
            "ok": True,
            "changed": False,
            "provider": before["provider_id"],
            "model": before["model_id"],
            "probe": probe,
            "retry_cleared": retry_cleared,
        }
    except RECOVERABLE_PROVIDER_ERRORS as exc:
        primary_error = f"{type(exc).__name__}: {str(exc)[:500]}"

    if str(before["provider_id"]) == "gemini" or not _credential_present("OBSERVER_GEMINI_API_KEY"):
        raise AIDecisionError(
            "Current cognition binding failed live verification and no distinct verified recovery provider is available. "
            f"Primary: {primary_error}"
        )

    bootstrap = bootstrap_gemini_cognition(
        conn,
        character_id=character_id,
        role=role,
        force=True,
    )
    try:
        probe = _probe(conn, character_id, role)
    except RECOVERABLE_PROVIDER_ERRORS as fallback_exc:
        # Restore the prior explicit binding if the candidate cannot actually
        # generate a valid decision. set_binding validation is already satisfied
        # because this binding was active before the recovery attempt.
        from .ai import set_binding

        set_binding(
            conn,
            scope_type=str(before["scope_type"]),
            scope_id=str(before["scope_id"]),
            role=str(before["role"]),
            provider_id=str(before["provider_id"]),
            model_id=str(before["model_id"]),
            parameters=dict(before.get("parameters") or {}),
        )
        raise AIDecisionError(
            "Current cognition binding failed and Gemini recovery candidate also failed live verification. "
            f"Primary: {primary_error} | Gemini: {type(fallback_exc).__name__}: {str(fallback_exc)[:500]}"
        ) from fallback_exc

    after = resolve_binding(conn, role=role, character_id=character_id)
    retry_cleared = _clear_provider_retry_and_wake(conn, character_id)
    state = snapshot(conn, character_id)
    record_event(
        conn,
        sim_time=str(state["sim_time"]),
        actor_id=character_id,
        event_type="cognition_provider_recovered",
        location_id=str(state["location"]),
        payload={
            "source": "verified-cognition-provider-recovery-v1",
            "role": role,
            "from_provider": str(before["provider_id"]),
            "from_model": str(before["model_id"]),
            "to_provider": str(after["provider_id"]) if after else None,
            "to_model": str(after["model_id"]) if after else None,
            "primary_error_type": primary_error.split(":", 1)[0] if primary_error else None,
            "live_probe_verified": True,
            "retry_cleared": retry_cleared,
        },
    )
    conn.commit()
    return {
        "ok": True,
        "changed": True,
        "provider": after["provider_id"] if after else bootstrap.get("provider"),
        "model": after["model_id"] if after else bootstrap.get("selected_model"),
        "primary_error": primary_error,
        "probe": probe,
        "retry_cleared": retry_cleared,
    }

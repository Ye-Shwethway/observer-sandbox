import pytest

from observer_sandbox import ai_runtime
from observer_sandbox.ai import set_binding
from observer_sandbox.ai_control import activate_cognition_fallback
from observer_sandbox.ai_fallback import last_fallback_use, set_fallback_binding
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def _add_model(conn, provider_id: str, model_id: str) -> None:
    conn.execute("UPDATE ai_providers SET enabled=1 WHERE id=?", (provider_id,))
    conn.execute(
        "INSERT INTO ai_models(provider_id, model_id, display_name, active) VALUES (?, ?, ?, 1)",
        (provider_id, model_id, model_id),
    )
    conn.commit()


def _bind_primary(conn, provider_id: str, model_id: str) -> None:
    set_binding(
        conn,
        scope_type="character",
        scope_id="char_darian",
        role="cognition",
        provider_id=provider_id,
        model_id=model_id,
        parameters={},
    )


def _idle_state():
    return {"action_options": [{"action": "idle", "target": None, "duration": [1, 20]}]}


def test_provider_failure_uses_one_configured_fallback_without_changing_primary(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "gemini-primary")
        _add_model(conn, "groq", "groq-fallback")
        _bind_primary(conn, "gemini", "gemini-primary")
        set_fallback_binding(conn, "groq", "groq-fallback", tested_at="2026-08-14T00:00:00+00:00")

        calls = []

        def fake_generate(_conn, binding, _prompt):
            calls.append((binding["provider_id"], binding["model_id"]))
            if binding["provider_id"] == "gemini":
                raise ai_runtime.AIDecisionError("HTTP 429: quota exhausted")
            return {"action": "idle", "duration_minutes": 5, "target": "", "reason": "brief pause"}

        monkeypatch.setattr(ai_runtime, "_generate_for_binding", fake_generate)
        decision = ai_runtime.generate_character_decision(
            conn,
            character_id="char_darian",
            role="cognition",
            state=_idle_state(),
            available_actions=["idle"],
        )
        primary = conn.execute(
            "SELECT provider_id, model_id FROM ai_bindings WHERE scope_type='character' AND scope_id='char_darian' AND role='cognition'"
        ).fetchone()
        last = last_fallback_use(conn)

    assert calls == [("gemini", "gemini-primary"), ("groq", "groq-fallback")]
    assert decision["action"] == "idle"
    assert tuple(primary) == ("gemini", "gemini-primary")
    assert last["fallback_provider_id"] == "groq"
    assert "429" in last["primary_error"]


def test_deterministic_decision_validation_failure_never_triggers_fallback(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "gemini-primary")
        _add_model(conn, "groq", "groq-fallback")
        _bind_primary(conn, "gemini", "gemini-primary")
        set_fallback_binding(conn, "groq", "groq-fallback")
        calls = []

        def invalid_primary(_conn, binding, _prompt):
            calls.append(binding["provider_id"])
            return {"action": "train", "duration_minutes": 5, "target": "", "reason": "invalid here"}

        monkeypatch.setattr(ai_runtime, "_generate_for_binding", invalid_primary)
        with pytest.raises(ai_runtime.AIDecisionError, match="unavailable action"):
            ai_runtime.generate_character_decision(
                conn,
                character_id="char_darian",
                role="cognition",
                state=_idle_state(),
                available_actions=["idle"],
            )

    assert calls == ["gemini"]


def test_fallback_configuration_is_distinct_from_primary_binding(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "gemini-primary")
        _add_model(conn, "groq", "groq-fallback")
        _bind_primary(conn, "gemini", "gemini-primary")
        fallback = activate_cognition_fallback(
            conn,
            "groq",
            "groq-fallback",
            tested_at="2026-08-14T00:00:00+00:00",
        )
        primary = conn.execute(
            "SELECT provider_id, model_id FROM ai_bindings WHERE scope_type='character' AND scope_id='char_darian' AND role='cognition'"
        ).fetchone()

    assert fallback["provider_id"] == "groq"
    assert tuple(primary) == ("gemini", "gemini-primary")

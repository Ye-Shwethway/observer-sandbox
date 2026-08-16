import pytest

from observer_sandbox import ai_recovery
from observer_sandbox.actor_runtime import actor_runtime, set_actor_runtime, set_retry
from observer_sandbox.ai import resolve_binding, set_binding
from observer_sandbox.ai_runtime import AIDecisionError
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


ACTOR = "char_darian"


def _seed_model(conn, provider: str, model: str) -> None:
    conn.execute("UPDATE ai_providers SET enabled=1 WHERE id=?", (provider,))
    conn.execute(
        """INSERT INTO ai_models(provider_id,model_id,display_name,capabilities_json,metadata_json,active)
           VALUES(?,?,?,'{}','{}',1)
           ON CONFLICT(provider_id,model_id) DO UPDATE SET active=1""",
        (provider, model, model),
    )
    conn.commit()


def _bind(conn, provider: str, model: str) -> None:
    set_binding(
        conn,
        scope_type="character",
        scope_id=ACTOR,
        role="cognition",
        provider_id=provider,
        model_id=model,
        parameters={},
    )


def test_failed_primary_switches_only_after_verified_gemini_probe_and_clears_provider_retry(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_model(conn, "groq", "groq-test")
        _seed_model(conn, "gemini", "gemini-test")
        _bind(conn, "groq", "groq-test")
        set_retry(conn, ACTOR, {"failures": 6, "retry_after": 9999999999.0, "last_error": "AIDecisionError"})
        set_actor_runtime(conn, ACTOR, autonomy_enabled=True, pending_action_id=None)
        conn.commit()

        calls = {"count": 0}

        def fake_probe(_conn, _character_id, _role):
            calls["count"] += 1
            if calls["count"] == 1:
                raise AIDecisionError("primary access denied")
            return {"ok": True, "validated": True, "mutated": False}

        def fake_bootstrap(_conn, *, character_id, role, force):
            assert character_id == ACTOR and role == "cognition" and force is True
            _bind(_conn, "gemini", "gemini-test")
            return {"ok": True, "changed": True, "provider": "gemini", "selected_model": "gemini-test"}

        monkeypatch.setattr(ai_recovery, "_probe", fake_probe)
        monkeypatch.setattr(ai_recovery, "bootstrap_gemini_cognition", fake_bootstrap)
        monkeypatch.setenv("OBSERVER_GEMINI_API_KEY", "present-for-test")

        result = ai_recovery.ensure_cognition_live(conn, character_id=ACTOR)

        assert result["ok"] is True
        assert result["changed"] is True
        assert result["provider"] == "gemini"
        assert result["retry_cleared"] is True
        binding = resolve_binding(conn, role="cognition", character_id=ACTOR)
        assert binding["provider_id"] == "gemini"
        runtime = actor_runtime(conn, ACTOR)
        assert runtime["retry"] is None
        assert runtime["wake_reason"] == "cognition_provider_recovered"
        event = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id=? AND event_type='cognition_provider_recovered' ORDER BY id DESC LIMIT 1",
            (ACTOR,),
        ).fetchone()
        assert event is not None


def test_failed_recovery_probe_restores_original_binding_and_preserves_retry(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_model(conn, "groq", "groq-test")
        _seed_model(conn, "gemini", "gemini-test")
        _bind(conn, "groq", "groq-test")
        set_retry(conn, ACTOR, {"failures": 4, "retry_after": 9999999999.0, "last_error": "AIDecisionError"})
        conn.commit()

        def always_fail(_conn, _character_id, _role):
            raise AIDecisionError("provider unavailable")

        def fake_bootstrap(_conn, *, character_id, role, force):
            _bind(_conn, "gemini", "gemini-test")
            return {"ok": True, "changed": True, "provider": "gemini", "selected_model": "gemini-test"}

        monkeypatch.setattr(ai_recovery, "_probe", always_fail)
        monkeypatch.setattr(ai_recovery, "bootstrap_gemini_cognition", fake_bootstrap)
        monkeypatch.setenv("OBSERVER_GEMINI_API_KEY", "present-for-test")

        with pytest.raises(AIDecisionError):
            ai_recovery.ensure_cognition_live(conn, character_id=ACTOR)

        binding = resolve_binding(conn, role="cognition", character_id=ACTOR)
        assert binding["provider_id"] == "groq"
        assert actor_runtime(conn, ACTOR)["retry"] is not None

from observer_sandbox import ai_control, ai_runtime, telegram_ai_control
from observer_sandbox.ai import resolve_binding, set_binding
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view


def _add_model(conn, provider_id: str, model_id: str, *, enabled: bool = False) -> None:
    conn.execute("UPDATE ai_providers SET enabled=? WHERE id=?", (int(enabled), provider_id))
    conn.execute(
        """
        INSERT INTO ai_models(provider_id, model_id, display_name, active)
        VALUES (?, ?, ?, 1)
        ON CONFLICT(provider_id, model_id) DO UPDATE SET display_name=excluded.display_name, active=1
        """,
        (provider_id, model_id, model_id),
    )
    conn.commit()


def test_catalog_refresh_does_not_enable_provider_or_change_binding(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    fetched = [{
        "model_id": "candidate/model",
        "display_name": "Candidate Model",
        "context_window": 8192,
        "capabilities": {"text": True},
        "metadata": {},
    }]
    monkeypatch.setattr(ai_control, "_fetch_models_without_activation", lambda provider, catalog_mode=None: fetched)

    with connect(db) as conn:
        assert conn.execute("SELECT enabled FROM ai_providers WHERE id='openrouter'").fetchone()[0] == 0
        assert resolve_binding(conn, role="cognition", character_id="char_darian") is None
        assert ai_control.refresh_provider_catalog(conn, "openrouter") == 1
        assert conn.execute("SELECT enabled FROM ai_providers WHERE id='openrouter'").fetchone()[0] == 0
        assert resolve_binding(conn, role="cognition", character_id="char_darian") is None
        assert ai_control.models_for_provider(conn, "openrouter")[0]["model_id"] == "candidate/model"


def test_nanogpt_provider_view_exposes_subscription_and_all_fetch_modes(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    calls: list[tuple[str, str | None]] = []

    def fake_refresh(conn, provider_id, *, catalog_mode=None):
        calls.append((provider_id, catalog_mode))
        return 12 if catalog_mode == "subscription" else 34

    monkeypatch.setattr(telegram_ai_control, "refresh_provider_catalog", fake_refresh)
    with connect(db) as conn:
        text, keyboard = _callback_view(conn, 111, "ai:p:nanogpt")
        callbacks = [button["callback_data"] for row in keyboard for button in row]
        assert "Subscription Only" in text
        assert "Paid" in text
        assert "ai:r:nanogpt:subscription" in callbacks
        assert "ai:r:nanogpt:all" in callbacks

        subscription_text, _ = _callback_view(conn, 111, "ai:r:nanogpt:subscription")
        all_text, _ = _callback_view(conn, 111, "ai:r:nanogpt:all")
        assert "Subscription-only catalog refreshed: 12" in subscription_text
        assert "All-model catalog refreshed: 34" in all_text
        assert calls == [("nanogpt", "subscription"), ("nanogpt", "all")]


def test_probe_is_real_adapter_path_but_non_mutating(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_OPENROUTER_API_KEY", "test-key")
    calls = []

    def fake_generate(provider, key, model_id, prompt, parameters):
        calls.append((provider["id"], key, model_id, prompt, parameters))
        return {"action": "idle", "duration_minutes": 1, "target": "", "reason": "probe"}

    monkeypatch.setattr(ai_runtime, "_generate_openai_compatible", fake_generate)
    with connect(db) as conn:
        _add_model(conn, "openrouter", "candidate/model", enabled=False)
        before = resolve_binding(conn, role="cognition", character_id="char_darian")
        result = ai_control.probe_model(conn, "openrouter", "candidate/model")
        after = resolve_binding(conn, role="cognition", character_id="char_darian")
        enabled = conn.execute("SELECT enabled FROM ai_providers WHERE id='openrouter'").fetchone()[0]

    assert result["ok"] is True
    assert result["provider_id"] == "openrouter"
    assert result["model_id"] == "candidate/model"
    assert result["latency_ms"] >= 0
    assert before == after is None
    assert enabled == 0
    assert calls and calls[0][0:3] == ("openrouter", "test-key", "candidate/model")


def test_test_before_save_gate_and_activation(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        _add_model(conn, "groq", "current/model", enabled=True)
        _add_model(conn, "openrouter", "candidate/model", enabled=False)
        set_binding(
            conn,
            scope_type="character",
            scope_id="char_darian",
            role="cognition",
            provider_id="groq",
            model_id="current/model",
        )

        text, keyboard = _callback_view(conn, 111, "ai:m:openrouter:0")
        assert "candidate/model" in text
        assert "Not passed" in text
        assert not any(button.get("callback_data") == "ai:save" for row in keyboard for button in row)

        blocked, _ = _callback_view(conn, 111, "ai:save")
        assert "Test" in blocked
        assert resolve_binding(conn, role="cognition", character_id="char_darian")["provider_id"] == "groq"

        monkeypatch.setattr(
            telegram_ai_control,
            "probe_model",
            lambda conn, provider_id, model_id: {
                "ok": True,
                "provider_id": provider_id,
                "model_id": model_id,
                "latency_ms": 42,
                "tested_at": "2026-08-14T00:00:00+00:00",
            },
        )
        tested, tested_keyboard = _callback_view(conn, 111, "ai:test")
        assert "Real inference succeeded" in tested
        assert any(button.get("callback_data") == "ai:save" for row in tested_keyboard for button in row)
        assert resolve_binding(conn, role="cognition", character_id="char_darian")["provider_id"] == "groq"

        saved, _ = _callback_view(conn, 111, "ai:save")
        binding = resolve_binding(conn, role="cognition", character_id="char_darian")
        assert "AI COGNITION ACTIVATED" in saved
        assert binding["provider_id"] == "openrouter"
        assert binding["model_id"] == "candidate/model"


def test_failed_probe_preserves_current_binding(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        _add_model(conn, "groq", "current/model", enabled=True)
        _add_model(conn, "openrouter", "candidate/model", enabled=False)
        set_binding(conn, scope_type="character", scope_id="char_darian", role="cognition", provider_id="groq", model_id="current/model")
        _callback_view(conn, 111, "ai:m:openrouter:0")

        def fail_probe(conn, provider_id, model_id):
            raise ai_runtime.AIDecisionError("HTTP 429: rate limit reached")

        monkeypatch.setattr(telegram_ai_control, "probe_model", fail_probe)
        failed, keyboard = _callback_view(conn, 111, "ai:test")
        assert "Rate / quota limit reached" in failed
        assert not any(button.get("callback_data") == "ai:save" for row in keyboard for button in row)
        binding = resolve_binding(conn, role="cognition", character_id="char_darian")
        assert binding["provider_id"] == "groq"
        assert conn.execute("SELECT enabled FROM ai_providers WHERE id='openrouter'").fetchone()[0] == 0


def test_ai_callbacks_are_owner_only_and_model_ids_stay_server_side(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")
    with connect(db) as conn:
        _add_model(conn, "openrouter", "provider/this-is-a-very-long-model-identifier-that-must-not-enter-callback-data", enabled=False)
        locked, _ = _callback_view(conn, 222, "ai:providers")
        assert "Creator authority required" in locked

        _, keyboard = _callback_view(conn, 111, "ai:page:openrouter:0")
        callbacks = [button["callback_data"] for row in keyboard for button in row if "callback_data" in button]
        assert all(len(value.encode("utf-8")) <= 64 for value in callbacks)
        assert all("this-is-a-very-long-model-identifier" not in value for value in callbacks)

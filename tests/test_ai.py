from observer_sandbox import ai
from observer_sandbox.ai import (
    list_providers,
    nanogpt_subscription_usage,
    resolve_binding,
    set_binding,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def _add_model(conn, provider, model):
    conn.execute("UPDATE ai_providers SET enabled=1 WHERE id=?", (provider,))
    conn.execute(
        """
        INSERT INTO ai_models(provider_id, model_id, display_name)
        VALUES (?, ?, ?)
        """,
        (provider, model, model),
    )
    conn.commit()


def test_builtin_providers_seeded(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        providers = {p["id"]: p for p in list_providers(conn)}
    assert {"gemini", "nanogpt", "openai", "openrouter"}.issubset(providers)
    assert providers["nanogpt"]["adapter_type"] == "nanogpt"
    assert providers["nanogpt"]["base_url"] == "https://nano-gpt.com/api"


def test_nanogpt_subscription_catalog_and_usage(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    calls = []

    def fake_get_json(url, headers=None, timeout=20.0):
        calls.append((url, headers))
        if url.endswith("/subscription/v1/usage"):
            return {"active": True, "daily": {"remaining": 10}, "monthly": {"remaining": 100}}
        return {
            "data": [
                {
                    "id": "example/model",
                    "name": "Example Model",
                    "context_length": 131072,
                    "capabilities": {"reasoning": True, "tool_calling": True},
                }
            ]
        }

    monkeypatch.setattr(ai, "_get_json", fake_get_json)
    monkeypatch.setenv("OBSERVER_NANOGPT_API_KEY", "test-key")

    with connect(db) as conn:
        provider = conn.execute("SELECT * FROM ai_providers WHERE id='nanogpt'").fetchone()
        models = ai._fetch_nanogpt(provider)
        usage = nanogpt_subscription_usage(conn)

    assert models[0]["model_id"] == "example/model"
    assert models[0]["capabilities"]["reasoning"] is True
    assert usage["active"] is True
    assert calls[0][0].endswith("/subscription/v1/models?detailed=true")
    assert calls[1][0].endswith("/subscription/v1/usage")
    assert calls[0][1]["Authorization"] == "Bearer test-key"


def test_binding_precedence(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "g-default")
        _add_model(conn, "openrouter", "or-character")
        _add_model(conn, "openai", "o-task")

        set_binding(
            conn,
            scope_type="global",
            scope_id="default",
            role="default",
            provider_id="gemini",
            model_id="g-default",
        )
        set_binding(
            conn,
            scope_type="character",
            scope_id="darian",
            role="cognition",
            provider_id="openrouter",
            model_id="or-character",
        )
        set_binding(
            conn,
            scope_type="task",
            scope_id="decision-1",
            role="cognition",
            provider_id="openai",
            model_id="o-task",
        )

        character = resolve_binding(conn, role="cognition", character_id="darian")
        task = resolve_binding(
            conn,
            role="cognition",
            character_id="darian",
            task_id="decision-1",
        )
        fallback = resolve_binding(conn, role="narration", character_id="darian")

    assert character["provider_id"] == "openrouter"
    assert task["provider_id"] == "openai"
    assert fallback["provider_id"] == "gemini"

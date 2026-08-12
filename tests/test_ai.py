from observer_sandbox.ai import (
    list_providers,
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
        ids = {p["id"] for p in list_providers(conn)}
    assert {"gemini", "nanogpt", "openai", "openrouter"}.issubset(ids)


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

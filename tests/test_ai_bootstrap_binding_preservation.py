from observer_sandbox import ai_bootstrap
from observer_sandbox.ai import set_binding
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def _add_model(conn, provider_id: str, model_id: str) -> None:
    conn.execute("UPDATE ai_providers SET enabled=1 WHERE id=?", (provider_id,))
    conn.execute(
        "INSERT INTO ai_models(provider_id, model_id, display_name, active) VALUES (?, ?, ?, 1)",
        (provider_id, model_id, model_id),
    )
    conn.commit()


def test_groq_bootstrap_preserves_creator_selected_gemini_binding(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "gemini-creator-selected")
        set_binding(
            conn,
            scope_type="character",
            scope_id="char_darian",
            role="cognition",
            provider_id="gemini",
            model_id="gemini-creator-selected",
            parameters={},
        )
        monkeypatch.setattr(
            ai_bootstrap,
            "refresh_catalog",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("catalog refresh must not run")),
        )
        result = ai_bootstrap.bootstrap_groq_cognition(conn)

    assert result["changed"] is False
    assert result["reason"] == "existing_binding_preserved"
    assert result["binding"]["provider_id"] == "gemini"
    assert result["binding"]["model_id"] == "gemini-creator-selected"


def test_gemini_bootstrap_preserves_creator_selected_groq_binding(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "groq", "groq-creator-selected")
        set_binding(
            conn,
            scope_type="character",
            scope_id="char_darian",
            role="cognition",
            provider_id="groq",
            model_id="groq-creator-selected",
            parameters={},
        )
        monkeypatch.setattr(
            ai_bootstrap,
            "refresh_catalog",
            lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("catalog refresh must not run")),
        )
        result = ai_bootstrap.bootstrap_gemini_cognition(conn)

    assert result["changed"] is False
    assert result["binding"]["provider_id"] == "groq"


def test_force_still_allows_explicit_administrative_migration(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "gemini-old")
        _add_model(conn, "groq", "openai/gpt-oss-20b")
        set_binding(
            conn,
            scope_type="character",
            scope_id="char_darian",
            role="cognition",
            provider_id="gemini",
            model_id="gemini-old",
            parameters={},
        )
        monkeypatch.setattr(ai_bootstrap, "refresh_catalog", lambda *_args, **_kwargs: 1)
        monkeypatch.setattr(
            ai_bootstrap,
            "choose_groq_cognition_model",
            lambda _conn: {"model_id": "openai/gpt-oss-20b"},
        )
        result = ai_bootstrap.bootstrap_groq_cognition(conn, force=True)

    assert result["changed"] is True
    assert result["binding"]["provider_id"] == "groq"

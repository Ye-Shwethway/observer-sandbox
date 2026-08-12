import json

from observer_sandbox.ai_bootstrap import choose_gemini_flash_model
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def _insert_model(conn, model_id: str, actions=None):
    conn.execute(
        """
        INSERT INTO ai_models(
            provider_id, model_id, display_name, capabilities_json,
            context_window, metadata_json, active, last_seen_at
        ) VALUES ('gemini', ?, ?, ?, 100000, '{}', 1, CURRENT_TIMESTAMP)
        """,
        (model_id, model_id, json.dumps({"actions": actions or ["generateContent"]})),
    )


def test_choose_gemini_flash_prefers_stable_lite_without_hardcoded_id(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _insert_model(conn, "gemini-9.1-flash-preview")
        _insert_model(conn, "gemini-8.0-flash")
        _insert_model(conn, "gemini-7.5-flash-lite")
        _insert_model(conn, "gemini-10.0-flash-image")
        selected = choose_gemini_flash_model(conn)
        assert selected["model_id"] == "gemini-7.5-flash-lite"


def test_choose_gemini_flash_falls_back_to_stable_flash(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _insert_model(conn, "gemini-6.0-flash-preview")
        _insert_model(conn, "gemini-5.0-flash")
        selected = choose_gemini_flash_model(conn)
        assert selected["model_id"] == "gemini-5.0-flash"

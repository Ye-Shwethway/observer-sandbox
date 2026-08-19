from observer_sandbox.creation_sandbox import canonical_state_fingerprint, list_sandbox_objects
from observer_sandbox.creator_studio import active_draft, ai_draft, approve_draft, manual_draft
from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view, _command_keyboard, handle_command


def test_schema_v19_registers_creator_studio_drafts(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert SCHEMA_VERSION == 19
        assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "19"
        assert conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='creation_sandbox_drafts'"
        ).fetchone() is not None


def test_manual_draft_is_not_object_until_approval(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        draft = manual_draft(conn, 111, "character", "Draft Person")
        assert draft["proposal"]["identity"]["name"] == "Draft Person"
        assert list_sandbox_objects(conn) == []
        assert canonical_state_fingerprint(conn) == before

        obj = approve_draft(conn, 111)
        assert obj["creation_type"] == "character"
        assert obj["identity"]["name"] == "Draft Person"
        assert active_draft(conn, 111) is None
        assert len(list_sandbox_objects(conn)) == 1
        assert canonical_state_fingerprint(conn) == before


def test_ai_draft_uses_creation_binding_and_remains_unapproved(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute("UPDATE ai_providers SET enabled=1 WHERE id='gemini'")
        conn.execute(
            "INSERT INTO ai_models(provider_id,model_id,display_name,active) VALUES('gemini','studio-test','Studio Test',1)"
        )
        conn.execute(
            "INSERT INTO ai_bindings(scope_type,scope_id,role,provider_id,model_id,parameters_json,enabled) "
            "VALUES('engine','creator_creation','creator_creation_assist','gemini','studio-test','{}',1)"
        )
        conn.commit()

        def fake_generate(*args, **kwargs):
            return {
                "proposal_version": 1,
                "creation_type": "location",
                "schema_version": 1,
                "target_scope": "sandbox",
                "identity": {"name": "AI Studio Room"},
                "properties": {"kind": "room"},
                "relationships": [],
                "capabilities": ["rest"],
                "provenance": {"mode": "ai_generated", "requested_by": None},
            }

        monkeypatch.setattr("observer_sandbox.creator_studio.generate_structured", fake_generate)
        draft = ai_draft(conn, 111, "location", "A quiet room")
        assert draft["draft_mode"] == "ai_generated"
        assert draft["proposal"]["provenance"]["requested_by"] == "telegram:111"
        assert list_sandbox_objects(conn) == []


def test_telegram_sandbox_world_exposes_creator_studio_and_owner_commands(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        text, keyboard = _callback_view(conn, 111, "nav:sandbox")
        callbacks = {button["callback_data"] for row in keyboard for button in row}
        assert "SANDBOX WORLD" in text
        assert "sw:studio" in callbacks

        studio_text, studio_keyboard = _callback_view(conn, 111, "sw:studio")
        assert "CREATOR STUDIO" in studio_text
        assert any(
            button["callback_data"] == "sw:cs:help:character"
            for row in studio_keyboard for button in row
        )

    result = handle_command(db, user_id=111, text="/create character Telegram Draft")
    assert "CREATION SANDBOX DRAFT" in result
    assert "Telegram Draft" in result
    assert any(
        button["callback_data"] == "sw:cs:preview"
        for row in _command_keyboard("/create") for button in row
    )


def test_non_owner_cannot_use_creator_studio_commands(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")
    assert handle_command(db, user_id=222, text="/create location No") == "🔒 Creator authority required for Creator Studio."

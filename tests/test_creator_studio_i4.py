from observer_sandbox.creation_sandbox import canonical_state_fingerprint, list_sandbox_objects
from observer_sandbox.creator_studio import active_draft, ai_draft, approve_draft, manual_draft
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view, _command_keyboard, handle_command


def _callbacks(keyboard):
    return [button["callback_data"] for row in keyboard or [] for button in row]


def test_creator_studio_registers_drafts_and_input_sessions(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"creation_sandbox_drafts", "creation_sandbox_studio_sessions"} <= tables


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


def test_telegram_sandbox_world_exposes_creator_studio_and_dual_creation_paths(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        text, keyboard = _callback_view(conn, 111, "nav:sandbox")
        callbacks = set(_callbacks(keyboard))
        assert "SANDBOX WORLD" in text
        assert "sw:studio" in callbacks

        studio_text, studio_keyboard = _callback_view(conn, 111, "sw:studio")
        assert "CREATOR STUDIO" in studio_text
        assert "sw:cs:create" in _callbacks(studio_keyboard)

        create_text, create_keyboard = _callback_view(conn, 111, "sw:cs:create")
        assert "CREATE IN SANDBOX" in create_text
        assert {"sw:cs:type:character", "sw:cs:type:location"} <= set(_callbacks(create_keyboard))

        _, method_keyboard = _callback_view(conn, 111, "sw:cs:type:character")
        assert {"sw:cs:input:character:manual", "sw:cs:input:character:ai"} <= set(_callbacks(method_keyboard))

    result = handle_command(db, user_id=111, text="/create character Telegram Draft")
    assert "CREATION SANDBOX DRAFT" in result
    assert "Telegram Draft" in result
    assert "sw:cs:preview" in _callbacks(_command_keyboard("/create"))


def test_guided_plain_text_input_creates_draft_and_preview_keyboard(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        prompt, keyboard = _callback_view(conn, 111, "sw:cs:input:character:manual")
        assert "next message" in prompt.lower()
        assert "sw:cs:input:cancel" in _callbacks(keyboard)
        row = conn.execute("SELECT expected_input FROM creation_sandbox_studio_sessions WHERE user_id=111").fetchone()
        assert row[0] == "name"

    from observer_sandbox import telegram_bot as base
    result = base.handle_command(db, user_id=111, text="Guided Darian")
    assert "CREATION SANDBOX DRAFT" in result
    assert "Guided Darian" in result
    assert "sw:cs:approve" in _callbacks(base._command_keyboard(""))
    with connect(db) as conn:
        assert active_draft(conn, 111) is not None
        assert list_sandbox_objects(conn) == []
        assert conn.execute("SELECT 1 FROM creation_sandbox_studio_sessions WHERE user_id=111").fetchone() is None


def test_guided_input_cancel_and_non_owner_isolation(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")

    with connect(db) as conn:
        _callback_view(conn, 111, "sw:cs:input:location:manual")
        text, _ = _callback_view(conn, 111, "sw:cs:input:cancel")
        assert "CREATOR STUDIO" in text
        assert conn.execute("SELECT 1 FROM creation_sandbox_studio_sessions WHERE user_id=111").fetchone() is None

    assert handle_command(db, user_id=222, text="/create location No") == "🔒 Creator authority required for Creator Studio."

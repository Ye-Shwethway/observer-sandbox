from observer_sandbox import telegram_bot as base
from observer_sandbox.creator_studio import manual_draft
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_studio import (
    _manual_fields,
    bind_input_prompt_message,
    studio_callback_view,
)
from observer_sandbox.telegram_fast_polling import _deliver_message_reply


def _callback_for_field(conn, section: str, field_key: str) -> str:
    fields = _manual_fields(conn, section)
    index = next(i for i, field in enumerate(fields) if str(field["field_key"]) == field_key)
    return f"sw:cs:manual:f:{section}:{index}"


def test_accepted_manual_field_input_deletes_prompt_then_sends_same_section_card(tmp_path, monkeypatch):
    db = tmp_path / "manual-input-cleanup.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "42")

    with connect(db) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        callback = _callback_for_field(conn, "identity", "identity.gender")
        text, _keyboard = studio_callback_view(conn, 42, callback)
        assert "MANUAL CHARACTER FIELD" in text
        assert bind_input_prompt_message(conn, 42, 42, 777) is True

    reply = base.handle_command(db, user_id=42, text="man")
    keyboard = base._command_keyboard("")
    assert "MANUAL CHARACTER · IDENTITY" in reply
    assert "✅ Draft field updated." in reply

    api_calls = []
    sent = []
    edited = []

    def fake_api(token, method, payload=None, *, timeout=30):
        api_calls.append((method, payload, timeout))
        return True

    monkeypatch.setattr(base, "_api", fake_api)
    monkeypatch.setattr(base, "_send", lambda token, chat_id, text, kb=None: sent.append((chat_id, text, kb)))
    monkeypatch.setattr(base, "_edit", lambda *args, **kwargs: edited.append((args, kwargs)))

    _deliver_message_reply("token", 42, reply, keyboard)

    assert [(method, payload) for method, payload, _timeout in api_calls] == [
        ("deleteMessage", {"chat_id": 42, "message_id": 777})
    ]
    assert len(sent) == 1
    assert "MANUAL CHARACTER · IDENTITY" in sent[0][1]
    assert edited == []


def test_rejected_manual_field_input_edits_existing_prompt_into_retry_state(tmp_path, monkeypatch):
    db = tmp_path / "manual-input-retry.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "42")

    with connect(db) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        callback = _callback_for_field(conn, "body", "body.height_in")
        text, _keyboard = studio_callback_view(conn, 42, callback)
        assert "Expected: number" in text
        assert bind_input_prompt_message(conn, 42, 42, 778) is True

    reply = base.handle_command(db, user_id=42, text="not-a-number")
    keyboard = base._command_keyboard("")
    assert "Manual Character value rejected" in reply

    api_calls = []
    sent = []
    edited = []

    monkeypatch.setattr(base, "_api", lambda *args, **kwargs: api_calls.append((args, kwargs)))
    monkeypatch.setattr(base, "_send", lambda *args, **kwargs: sent.append((args, kwargs)))
    monkeypatch.setattr(base, "_edit", lambda *args, **kwargs: edited.append((args, kwargs)))

    _deliver_message_reply("token", 42, reply, keyboard)

    assert len(edited) == 1
    args, _kwargs = edited[0]
    assert args[1:3] == (42, 778)
    assert "Manual Character value rejected" in args[3]
    assert sent == []
    assert api_calls == []


def test_creator_studio_session_schema_tracks_temporary_prompt_message(tmp_path):
    db = tmp_path / "manual-input-session-schema.sqlite3"
    initialize(db)
    with connect(db) as conn:
        columns = {
            str(row["name"])
            for row in conn.execute("PRAGMA table_info(creation_sandbox_studio_sessions)").fetchall()
        }
        assert {"prompt_chat_id", "prompt_message_id"} <= columns

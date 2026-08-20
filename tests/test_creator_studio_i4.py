import json

import pytest

from observer_sandbox.creation_sandbox import canonical_state_fingerprint, list_sandbox_objects
from observer_sandbox.creation_socket import CreationProposalError
from observer_sandbox.creator_studio import CreatorStudioError, active_draft, ai_draft, approve_draft, manual_draft
from observer_sandbox.db import connect
from observer_sandbox.manual_character_creation import manual_character_required_field_keys, update_manual_character_field
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view, _command_keyboard, handle_command


def _callbacks(keyboard):
    return [button["callback_data"] for row in keyboard or [] for button in row]


def _manual_value(key: str, data_type: str):
    specials = {
        "identity.full_name": "Draft Person",
        "identity.date_of_birth": "2001-05-12",
        "identity.sex": "male",
        "identity.gender": "man",
        "body.height_in": 74,
        "genetics.height_max_in": 76,
        "body.weight_lb": 190,
        "body.body_fat_pct": 12,
        "genetics.weight_lean_min_lb": 150,
        "genetics.weight_lean_max_lb": 220,
        "genetics.body_fat_floor_pct": 6,
        "body.neck_in": 16,
        "body.shoulders_in": 48,
        "body.chest_in": 42,
        "body.waist_in": 32,
        "body.hips_in": 38,
        "body.biceps_relaxed_in": 15,
        "body.biceps_flexed_in": 16,
        "body.triceps_in": 14,
        "body.forearms_in": 13,
        "body.thighs_in": 23,
        "body.calves_in": 16,
        "genetics.waist_target_in": 32,
        "sexual_anatomy.penis_length_in": 6,
        "sexual_anatomy.penis_girth_in": 5,
        "genetics.penis_length_in": 6,
        "genetics.penis_girth_in": 5,
        "training.training_age_years": 0,
        "raps_ia.iq": 120,
    }
    if key in specials:
        value = specials[key]
    elif key.startswith("genetics.") and data_type in {"number", "integer"}:
        value = 60
    elif data_type == "number":
        value = 50
    elif data_type == "integer":
        value = 1
    elif data_type == "boolean":
        value = True
    elif data_type == "date":
        value = "2001-05-12"
    elif data_type == "datetime":
        value = "2025-05-01T07:00:00+00:00"
    elif data_type == "json":
        value = []
    else:
        value = "manual value"
    return json.dumps(value) if data_type == "json" else str(value).lower() if isinstance(value, bool) else str(value)


def _fill_manual_exact_seed(conn, user_id=111):
    for key in manual_character_required_field_keys(conn):
        row = conn.execute("SELECT data_type FROM profile_field_definitions WHERE field_key=?", (key,)).fetchone()
        assert row is not None
        update_manual_character_field(conn, user_id, key, _manual_value(key, str(row["data_type"])))


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
        assert draft["proposal"]["properties"]["character_profile"]["values"]["identity.full_name"] == "Draft Person"
        assert list_sandbox_objects(conn) == []
        assert canonical_state_fingerprint(conn) == before

        with pytest.raises(CreatorStudioError, match="baseline is incomplete"):
            approve_draft(conn, 111)
        assert list_sandbox_objects(conn) == []
        assert canonical_state_fingerprint(conn) == before

        _fill_manual_exact_seed(conn)
        obj = approve_draft(conn, 111)
        assert obj["creation_type"] == "character"
        assert obj["identity"]["name"] == "Draft Person"
        assert active_draft(conn, 111) is None
        assert len(list_sandbox_objects(conn)) == 1
        assert canonical_state_fingerprint(conn) == before


def test_legacy_location_ai_draft_fails_closed_until_location_v2_ai_slice(tmp_path, monkeypatch):
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
        with pytest.raises(CreationProposalError, match="schema version mismatch for location"):
            ai_draft(conn, 111, "location", "A quiet room")
        assert active_draft(conn, 111) is None
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


def test_guided_plain_text_input_creates_structured_manual_builder(tmp_path, monkeypatch):
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
    assert "MANUAL CHARACTER BUILD" in result
    assert "Guided Darian" in result
    callbacks = _callbacks(base._command_keyboard(""))
    assert "sw:cs:preview" in callbacks
    assert "sw:cs:approve" not in callbacks
    with connect(db) as conn:
        draft = active_draft(conn, 111)
        assert draft is not None
        assert draft["proposal"]["properties"]["character_profile"]["values"]["identity.full_name"] == "Guided Darian"
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

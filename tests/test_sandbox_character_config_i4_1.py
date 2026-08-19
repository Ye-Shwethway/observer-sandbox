from observer_sandbox.creation_sandbox import (
    activate_creation_proposal,
    canonical_state_fingerprint,
)
from observer_sandbox.creation_socket import build_creation_proposal
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_runtime import sandbox_character_readiness
from observer_sandbox.telegram_creator_bot import _callback_view


def _callbacks(keyboard):
    return [button["callback_data"] for row in keyboard or [] for button in row]


def _vertical(conn):
    location = activate_creation_proposal(
        conn,
        build_creation_proposal(
            "location",
            identity={"name": "Config Studio"},
            properties={"kind": "room"},
            capabilities=["read", "rest"],
            requested_by="test:creator",
        ),
    )
    character = activate_creation_proposal(
        conn,
        build_creation_proposal(
            "character",
            identity={"name": "Config Character"},
            properties={"reference": "human"},
            capabilities=["idle", "relax"],
            requested_by="test:creator",
        ),
    )
    conn.execute("UPDATE ai_providers SET enabled=1 WHERE id='gemini'")
    conn.execute(
        """
        INSERT INTO ai_models(provider_id,model_id,display_name,active)
        VALUES('gemini','i4-config-model','I4 Config Model',1)
        ON CONFLICT(provider_id,model_id) DO UPDATE SET display_name=excluded.display_name,active=1
        """
    )
    conn.commit()
    return character, location


def test_character_detail_exposes_inline_configuration(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        character, _ = _vertical(conn)
        text, keyboard = _callback_view(conn, 111, f"sw:o:{character['object_id']}")
        assert "Ready: No" in text
        assert f"sw:cfg:{character['object_id']}" in _callbacks(keyboard)

        config_text, config_keyboard = _callback_view(conn, 111, f"sw:cfg:{character['object_id']}")
        assert "SANDBOX CHARACTER CONFIG" in config_text
        assert "NOT RUNTIME READY" in config_text
        callbacks = _callbacks(config_keyboard)
        assert f"sw:cfg:l:{character['object_id']}" in callbacks
        assert f"sw:cfg:a:{character['object_id']}" in callbacks
        assert f"sw:cfg:o:{character['object_id']}" in callbacks
        assert f"sw:cfg:t:{character['object_id']}" in callbacks
        assert all(len(value.encode("utf-8")) <= 64 for value in callbacks)


def test_inline_configuration_reaches_runtime_ready_without_starting_or_canonical_mutation(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        character, location = _vertical(conn)
        before = canonical_state_fingerprint(conn)

        location_text, location_keyboard = _callback_view(conn, 111, f"sw:cfg:l:{character['object_id']}")
        assert "ASSIGN SANDBOX LOCATION" in location_text
        location_choice = next(value for value in _callbacks(location_keyboard) if value.startswith("sw:cfg:ls:"))
        assigned_text, _ = _callback_view(conn, 111, location_choice)
        assert "Location assigned: Config Studio" in assigned_text
        readiness = sandbox_character_readiness(conn, character["object_id"])
        assert readiness["location_object_id"] == location["object_id"]
        assert {item["action_key"] for item in readiness["runtime_options"]} == {"idle", "read", "relax", "rest"}

        provider_text, provider_keyboard = _callback_view(conn, 111, f"sw:cfg:a:{character['object_id']}")
        assert "ASSIGN CHARACTER AI" in provider_text
        provider_choice = next(value for value in _callbacks(provider_keyboard) if value.startswith("sw:cfg:ap:"))
        model_text, model_keyboard = _callback_view(conn, 111, provider_choice)
        assert "CHOOSE CHARACTER MODEL" in model_text
        model_choice = next(value for value in _callbacks(model_keyboard) if value.startswith("sw:cfg:am:"))
        assert len(model_choice.encode("utf-8")) <= 64
        ai_text, _ = _callback_view(conn, 111, model_choice)
        assert "Character AI assigned" in ai_text

        clock_text, _ = _callback_view(conn, 111, f"sw:cfg:t:{character['object_id']}")
        assert "Sandbox clock initialized" in clock_text

        ready = sandbox_character_readiness(conn, character["object_id"])
        assert ready["ready"] is True
        assert ready["activation_status"] == "runtime_ready"
        actor = conn.execute(
            "SELECT activation_status,autonomy_enabled FROM creation_sandbox_actor_runtime WHERE object_id=?",
            (character["object_id"],),
        ).fetchone()
        assert actor["activation_status"] == "runtime_ready"
        assert actor["autonomy_enabled"] == 0
        assert canonical_state_fingerprint(conn) == before


def test_no_location_or_models_gives_guided_recovery_surfaces(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        character = activate_creation_proposal(
            conn,
            build_creation_proposal(
                "character",
                identity={"name": "Bare Character"},
                requested_by="test:creator",
            ),
        )
        conn.execute("UPDATE ai_providers SET enabled=0")
        conn.commit()

        location_text, location_keyboard = _callback_view(conn, 111, f"sw:cfg:l:{character['object_id']}")
        assert "No active sandbox Locations" in location_text
        assert "sw:studio" in _callbacks(location_keyboard)

        ai_text, ai_keyboard = _callback_view(conn, 111, f"sw:cfg:a:{character['object_id']}")
        assert "No enabled providers" in ai_text
        assert "ai:settings" in _callbacks(ai_keyboard)

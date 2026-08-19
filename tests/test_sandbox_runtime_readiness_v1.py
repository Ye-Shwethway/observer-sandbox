from observer_sandbox.ai import resolve_binding, set_binding
from observer_sandbox.creation_sandbox import (
    activate_creation_proposal,
    bind_sandbox_character_to_location,
    canonical_state_fingerprint,
    reset_sandbox,
)
from observer_sandbox.creation_socket import build_creation_proposal
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_runtime import (
    bind_sandbox_character_ai,
    configure_sandbox_clock,
    replace_sandbox_runtime_options,
    sandbox_character_readiness,
    sandbox_runtime_status,
    set_sandbox_paused,
    set_sandbox_speed,
)
from observer_sandbox.simulation import runtime_value, set_runtime_value
from observer_sandbox.telegram_world_layers import world_layer_callback_view


def _add_model(conn, provider: str, model: str) -> None:
    conn.execute("UPDATE ai_providers SET enabled=1 WHERE id=?", (provider,))
    conn.execute(
        """
        INSERT INTO ai_models(provider_id,model_id,display_name,active)
        VALUES(?,?,?,1)
        ON CONFLICT(provider_id,model_id) DO UPDATE SET display_name=excluded.display_name,active=1
        """,
        (provider, model, model),
    )
    conn.commit()


def _sandbox_character_and_location(conn):
    character = activate_creation_proposal(
        conn,
        build_creation_proposal(
            "character",
            identity={"name": "Runtime Test Character"},
            properties={"sex": "Male"},
            requested_by="test:creator",
        ),
    )
    location = activate_creation_proposal(
        conn,
        build_creation_proposal(
            "location",
            identity={"name": "Runtime Test Room"},
            properties={"kind": "room"},
            requested_by="test:creator",
        ),
    )
    return character, location


def test_sandbox_clock_speed_pause_are_isolated_from_real_world_runtime(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_runtime_value(conn, "sim_time", "2025-05-14T09:00:00+00:00")
        set_runtime_value(conn, "speed", 60.0)
        set_runtime_value(conn, "paused", False)
        conn.commit()
        before = canonical_state_fingerprint(conn)

        configure_sandbox_clock(conn, "2031-01-02T03:04:00+00:00")
        set_sandbox_speed(conn, 12.0)
        set_sandbox_paused(conn, False, now_wall=1000.0)

        sandbox = sandbox_runtime_status(conn)
        assert sandbox["sim_time"] == "2031-01-02T03:04:00+00:00"
        assert sandbox["speed"] == 12.0
        assert sandbox["paused"] is False
        assert runtime_value(conn, "sim_time", None) == "2025-05-14T09:00:00+00:00"
        assert runtime_value(conn, "speed", None) == 60.0
        assert runtime_value(conn, "paused", None) is False
        assert canonical_state_fingerprint(conn) == before


def test_character_requires_location_options_ai_and_clock_before_runtime_ready(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "sandbox-cognition")
        character, location = _sandbox_character_and_location(conn)
        before = canonical_state_fingerprint(conn)

        first = sandbox_character_readiness(conn, character["object_id"])
        assert first["ready"] is False
        assert set(first["missing"]) == {
            "location_assigned",
            "runtime_options_available",
            "cognition_ai_bound",
            "clock_configured",
        }

        bind_sandbox_character_to_location(conn, character["object_id"], location["object_id"])
        second = sandbox_character_readiness(conn, character["object_id"])
        assert second["ready"] is False
        assert "location_assigned" not in second["missing"]

        replace_sandbox_runtime_options(
            conn,
            character["object_id"],
            [{"action_key": "rest", "source_object_id": location["object_id"]}],
        )
        bind_sandbox_character_ai(
            conn,
            character["object_id"],
            "gemini",
            "sandbox-cognition",
        )
        configure_sandbox_clock(conn, "2025-05-14T09:00:00+00:00")

        ready = sandbox_character_readiness(conn, character["object_id"])
        assert ready["ready"] is True
        assert ready["activation_status"] == "runtime_ready"
        assert ready["missing"] == []
        assert ready["location_object_id"] == location["object_id"]
        assert ready["ai_binding"]["model_id"] == "sandbox-cognition"
        assert [value["action_key"] for value in ready["runtime_options"]] == ["rest"]
        assert canonical_state_fingerprint(conn) == before


def test_sandbox_character_ai_binding_does_not_replace_real_character_binding(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "real-cognition")
        _add_model(conn, "gemini", "sandbox-cognition")
        set_binding(
            conn,
            scope_type="character",
            scope_id="char_darian",
            role="cognition",
            provider_id="gemini",
            model_id="real-cognition",
        )
        character, _ = _sandbox_character_and_location(conn)

        bind_sandbox_character_ai(
            conn,
            character["object_id"],
            "gemini",
            "sandbox-cognition",
        )

        real = resolve_binding(conn, role="cognition", character_id="char_darian")
        sandbox = sandbox_character_readiness(conn, character["object_id"])["ai_binding"]
        assert real["model_id"] == "real-cognition"
        assert sandbox["model_id"] == "sandbox-cognition"
        canonical_sandbox_binding = conn.execute(
            "SELECT 1 FROM ai_bindings WHERE scope_type='character' AND scope_id=?",
            (character["object_id"],),
        ).fetchone()
        assert canonical_sandbox_binding is None


def test_sandbox_runtime_reset_removes_clock_actor_binding_and_options(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn, "gemini", "sandbox-cognition")
        character, location = _sandbox_character_and_location(conn)
        bind_sandbox_character_to_location(conn, character["object_id"], location["object_id"])
        replace_sandbox_runtime_options(conn, character["object_id"], ["idle"])
        bind_sandbox_character_ai(conn, character["object_id"], "gemini", "sandbox-cognition")
        configure_sandbox_clock(conn, "2025-05-14T09:00:00+00:00")

        reset_sandbox(conn)

        assert conn.execute("SELECT COUNT(*) FROM creation_sandbox_actor_runtime").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM creation_sandbox_ai_bindings").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM creation_sandbox_runtime_options").fetchone()[0] == 0
        assert conn.execute("SELECT COUNT(*) FROM creation_sandbox_runtime").fetchone()[0] == 0


def test_telegram_sandbox_world_exposes_separate_runtime_surface(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        text, keyboard = world_layer_callback_view(conn, "nav:sandbox")
        callbacks = {button["callback_data"] for row in keyboard for button in row}
        assert "SANDBOX WORLD" in text
        assert "sw:runtime" in callbacks

        runtime_text, runtime_keyboard = world_layer_callback_view(conn, "sw:runtime")
        assert "SANDBOX RUNTIME" in runtime_text
        assert "Not configured" in runtime_text
        assert any(
            button["callback_data"] == "nav:sandbox"
            for row in runtime_keyboard
            for button in row
        )

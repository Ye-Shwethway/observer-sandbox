from observer_sandbox.creation_sandbox import (
    activate_creation_proposal,
    bind_sandbox_character_to_location,
    canonical_state_fingerprint,
    delete_sandbox_object,
    ensure_sandbox,
    get_sandbox_object,
    list_sandbox_objects,
    reset_sandbox,
)
from observer_sandbox.creation_socket import build_creation_proposal
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view, _home_keyboard, _home_message


def _callbacks(keyboard):
    return [button["callback_data"] for row in keyboard or [] for button in row]


def _sandbox_pair(conn):
    location = activate_creation_proposal(
        conn,
        build_creation_proposal(
            "location",
            identity={"name": "Sandbox Cabin"},
            properties={"kind": "residence"},
            requested_by="test:creator",
        ),
    )
    character = activate_creation_proposal(
        conn,
        build_creation_proposal(
            "character",
            identity={"name": "Sandbox Person"},
            properties={"sex": "male"},
            requested_by="test:creator",
        ),
    )
    character = bind_sandbox_character_to_location(
        conn,
        character["object_id"],
        location["object_id"],
    )
    return character, location


def test_isolated_creation_sandbox_runtime_tables_exist(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {
            "creation_sandboxes", "creation_sandbox_objects", "creation_sandbox_relations",
            "creation_sandbox_events", "creation_sandbox_runtime", "creation_sandbox_actor_runtime",
            "creation_sandbox_ai_bindings", "creation_sandbox_runtime_options",
            "creation_sandbox_profile_values", "creation_sandbox_character_skills", "creation_sandbox_drafts",
        } <= tables


def test_character_location_activation_and_binding_do_not_mutate_canonical_universe(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        character, location = _sandbox_pair(conn)
        after = canonical_state_fingerprint(conn)
        assert before == after
        assert character["object_id"].startswith("sbx_character_")
        assert location["object_id"].startswith("sbx_location_")
        assert character["resolved_relations"] == [{"relation_type": "located_in", "target_object_id": location["object_id"], "metadata": {}}]
        assert conn.execute("SELECT 1 FROM entities WHERE id=?", (character["object_id"],)).fetchone() is None
        assert conn.execute("SELECT 1 FROM entities WHERE id=?", (location["object_id"],)).fetchone() is None
        assert conn.execute("SELECT 1 FROM relations WHERE source_id=? OR target_id=?", (character["object_id"], location["object_id"])).fetchone() is None


def test_delete_and_reset_are_sandbox_only_and_revisioned(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        sandbox = ensure_sandbox(conn)
        character, location = _sandbox_pair(conn)
        delete_sandbox_object(conn, character["object_id"])
        assert [value["object_id"] for value in list_sandbox_objects(conn)] == [location["object_id"]]
        reset = reset_sandbox(conn)
        assert reset["revision"] == sandbox["revision"] + 1
        assert list_sandbox_objects(conn) == []
        assert canonical_state_fingerprint(conn) == before


def test_start_menu_uses_real_and_sandbox_world_upper_layers(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        text = _home_message(conn, 111)
        callbacks = _callbacks(_home_keyboard())
        assert "Choose a world layer" in text
        assert callbacks == ["nav:real", "nav:sandbox", "ai:home", "nav:close"]
        assert "inv:home" not in callbacks
        assert "nav:universe" not in callbacks
        assert "nav:characters" not in callbacks
        real_text, real_keyboard = _callback_view(conn, 111, "nav:real")
        assert "REAL WORLD" in real_text
        assert {"nav:universe", "nav:characters", "nav:runtime", "nav:history", "inv:home"} <= set(_callbacks(real_keyboard))
        sandbox_text, sandbox_keyboard = _callback_view(conn, 111, "nav:sandbox")
        assert "SANDBOX WORLD" in sandbox_text
        assert "Canonical universe: unchanged" in sandbox_text
        assert {"sw:studio", "sw:universe", "sw:list:character", "sw:list:location", "sw:runtime", "sw:history"} <= set(_callbacks(sandbox_keyboard))


def test_sandbox_world_is_creator_only_and_lists_isolated_objects(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")
    with connect(db) as conn:
        locked, _ = _callback_view(conn, 222, "nav:sandbox")
        assert "Creator authority required" in locked
        character, location = _sandbox_pair(conn)
        character_text, character_keyboard = _callback_view(conn, 111, "sw:list:character")
        location_text, location_keyboard = _callback_view(conn, 111, "sw:list:location")
        assert "Sandbox Person" in character_text
        assert "Sandbox Cabin" in location_text
        assert f"sw:o:{character['object_id']}" in _callbacks(character_keyboard)
        assert f"sw:o:{location['object_id']}" in _callbacks(location_keyboard)
        detail, _ = _callback_view(conn, 111, f"sw:o:{character['object_id']}")
        assert "Creation Sandbox" in detail
        assert "Canonical universe: unchanged" in detail
        assert location["object_id"] in detail
        assert get_sandbox_object(conn, character["object_id"])["sandbox_id"] == "creator-default"

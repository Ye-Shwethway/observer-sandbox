import json

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize, status
from observer_sandbox.world import set_field


def test_initialize_and_status(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    result = status(db)
    assert result.healthy is True
    assert result.schema_version == 4
    assert result.runtime_state["paused"] is False
    assert result.runtime_state["speed"] == 1.0
    assert result.runtime_state["world_id"] == "world_observer_universe"
    assert result.runtime_state["autonomy_enabled"] is False

    with connect(db) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert conn.execute("SELECT entity_type FROM entities WHERE id='world_observer_universe'").fetchone()[0] == "world"
        assert conn.execute("SELECT entity_type FROM entities WHERE id='loc_thorne_estate'").fetchone()[0] == "location"
        assert conn.execute("SELECT 1 FROM relations WHERE source_id='world_observer_universe' AND relation_type='contains' AND target_id='loc_thorne_estate'").fetchone() is not None
        assert conn.execute("SELECT 1 FROM entities WHERE id='home'").fetchone() is None
        assert conn.execute("SELECT 1 FROM entities WHERE id='room_kitchen'").fetchone() is None
        assert conn.execute("SELECT COUNT(*) FROM action_definitions").fetchone()[0] >= 11
        assert conn.execute("SELECT actor_id FROM actor_runtime WHERE actor_id='char_darian'").fetchone()[0] == "char_darian"
    assert {
        "entities", "relations", "fields", "events", "runtime_state",
        "entity_definitions", "action_definitions", "action_instances", "action_participants",
        "actor_runtime", "active_modifiers", "event_participants",
        "profile_field_definitions", "character_profiles", "character_profile_values", "character_profile_history",
        "character_preferences", "character_hobbies", "character_habits", "character_routines", "character_skills",
        "character_relationship_state", "ai_providers", "ai_models", "ai_bindings", "ai_catalog_sync",
    } <= tables


def test_legacy_spatial_ids_are_cleanly_reset_and_runtime_is_remapped(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        conn.execute("DELETE FROM runtime_state WHERE key='world_identity_revision'")
        conn.execute("INSERT INTO entities(id, entity_type, name, capabilities_json) VALUES('room_kitchen','location','Legacy Kitchen','[]')")
        set_field(conn, "char_darian", "runtime.location", "room_kitchen")
        set_field(conn, "char_darian", "runtime.current_action", "move")
        conn.execute("INSERT OR REPLACE INTO runtime_state(key, value_json) VALUES('paused', 'false')")
        conn.execute(
            "INSERT OR REPLACE INTO runtime_state(key, value_json) VALUES('autonomy_pending_action', ?)",
            (json.dumps({"action": "drink", "target": "obj_water", "action_id": "legacy-action"}),),
        )
        conn.commit()

    initialize(db)
    with connect(db) as conn:
        assert json.loads(conn.execute("SELECT value_json FROM runtime_state WHERE key='paused'").fetchone()[0]) is True
        legacy_pending = conn.execute("SELECT value_json FROM runtime_state WHERE key='autonomy_pending_action'").fetchone()
        assert legacy_pending is None or json.loads(legacy_pending[0]) is None
        assert conn.execute("SELECT 1 FROM entities WHERE id='room_kitchen'").fetchone() is None
        location = json.loads(conn.execute("SELECT value_json FROM fields WHERE entity_id='char_darian' AND field_key='runtime.location'").fetchone()[0])
        assert location == "loc_thorne_estate_kitchen"

    initialize(db)
    result = status(db)
    assert result.runtime_state["paused"] is False
    assert result.runtime_state["world_id"] == "world_observer_universe"
    assert result.runtime_state["world_identity_revision"] == "thorne-estate-v3.0-scoped-ids"

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize, status


def test_initialize_and_status(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    result = status(db)
    assert result.healthy is True
    assert result.schema_version == 3
    assert result.runtime_state["paused"] is False
    assert result.runtime_state["speed"] == 1.0
    assert result.runtime_state["world_id"] == "world_observer_universe"

    with connect(db) as conn:
        tables = {
            row[0]
            for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        assert conn.execute("SELECT entity_type FROM entities WHERE id='world_observer_universe'").fetchone()[0] == "world"
        assert conn.execute("SELECT entity_type FROM entities WHERE id='loc_thorne_estate'").fetchone()[0] == "location"
        assert conn.execute(
            "SELECT 1 FROM relations WHERE source_id='world_observer_universe' AND relation_type='contains' AND target_id='loc_thorne_estate'"
        ).fetchone() is not None
        assert conn.execute("SELECT 1 FROM entities WHERE id='home'").fetchone() is None
        assert conn.execute("SELECT 1 FROM entities WHERE id='room_kitchen'").fetchone() is None
    assert {
        "entities",
        "relations",
        "fields",
        "events",
        "runtime_state",
        "profile_field_definitions",
        "character_profiles",
        "character_profile_values",
        "character_profile_history",
        "character_preferences",
        "character_hobbies",
        "character_habits",
        "character_routines",
        "character_skills",
        "character_relationship_state",
        "ai_providers",
        "ai_models",
        "ai_bindings",
        "ai_catalog_sync",
    } <= tables

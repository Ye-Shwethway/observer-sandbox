from observer_sandbox.cognition_capability_awareness import cognition_capability_awareness
from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.need_resolution import shape_action_options_for_needs
from observer_sandbox.resource_awareness import reachable_location_awareness
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import action_options, snapshot
from observer_sandbox.spatial_familiarity import spatial_familiarity_context, spatial_familiarity_state
from observer_sandbox.world import get_field, set_field


def test_spatial_familiarity_is_seeded_as_generic_semantic_memory(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert get_field(conn, "char_darian", "world.spatial_familiarity", None) is None
        state = spatial_familiarity_state(conn, "char_darian")
        assert state is not None
        locations = state["locations"]
        assert state["source"] == "character_semantic_memory"
        assert state["revision"] == "initial-semantic-memory-v1"
        assert locations["loc_thorne_estate_master_suite"]["familiarity"] == "intimate"
        assert locations["loc_thorne_estate_tactical_obstacle_course"]["familiarity"] == "intimate"
        assert locations["loc_thorne_estate_rear_forest"]["familiarity"] == "familiar"
        passage = locations["loc_thorne_estate_concealed_forest_passage"]
        assert passage["familiarity"] == "familiar" and passage["secret"] is True
        assert "loc_south_lake_tahoe" not in locations
        assert "loc_thorne_estate_exterior_boundary" not in locations
        assert conn.execute(
            "SELECT COUNT(*) FROM character_memories WHERE character_id='char_darian' AND memory_type='semantic' AND source_type='seed'"
        ).fetchone()[0] == 32
        assert conn.execute(
            "SELECT value_json FROM runtime_state WHERE key='spatial_familiarity_revision'"
        ).fetchone() is None


def test_semantic_seed_is_idempotent_and_does_not_overwrite_evolved_memory(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    memory_id = "mem_seed_spatial_familiarity_char_darian_loc_thorne_estate_rear_forest"
    with connect(db) as conn:
        row = conn.execute(
            "SELECT content_json FROM character_memories WHERE memory_id=?", (memory_id,)
        ).fetchone()
        assert row is not None
        import json
        content = json.loads(row[0])
        content["familiarity"] = "intimate"
        conn.execute(
            "UPDATE character_memories SET content_json=? WHERE memory_id=?",
            (json.dumps(content), memory_id),
        )
        conn.commit()

    initialize(db)
    with connect(db) as conn:
        state = spatial_familiarity_state(conn, "char_darian")
        assert state["locations"]["loc_thorne_estate_rear_forest"]["familiarity"] == "intimate"
        assert conn.execute(
            "SELECT COUNT(*) FROM character_memories WHERE memory_id=?", (memory_id,)
        ).fetchone()[0] == 1


def test_known_home_map_is_available_from_master_suite_not_only_one_hop(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert snapshot(conn, "char_darian")["location"] == "loc_thorne_estate_master_suite"
        context = spatial_familiarity_context(conn, "char_darian")
        intimate = set(context["known_locations_by_familiarity"]["intimate"])
        familiar = set(context["known_locations_by_familiarity"]["familiar"])
        assert context["mode"] == "semantic_memory_spatial_familiarity_v1"
        assert "Tactical Obstacle Course" in intimate
        assert "Private Lake Access" in intimate
        assert "Main Security Gate" in intimate
        assert "Rear Forested Estate" in familiar
        assert ["Core Estate Grounds", "Mansion Exterior"] in context["known_connections"]


def test_spatial_knowledge_reaches_cognition_context(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        awareness = cognition_capability_awareness(conn, "char_darian")
        spatial = awareness["reasoning_profile"]["spatial_knowledge"]
        assert spatial["mode"] == "semantic_memory_spatial_familiarity_v1"
        assert "Tactical Obstacle Course" in spatial["known_locations_by_familiarity"]["intimate"]
        assert "Hidden Dock" in spatial["known_secret_or_concealed_locations"]


def test_unknown_hidden_neighbor_stays_world_true_but_is_not_offered_to_cognition(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,capabilities_json) VALUES('loc_test_secret_vault','location','Secret Vault','[]')"
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES('loc_thorne_estate_master_suite','connected_to','loc_test_secret_vault')"
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES('loc_test_secret_vault','connected_to','loc_thorne_estate_master_suite')"
        )
        set_field(conn, "loc_test_secret_vault", "world.metadata", {"discovery_visibility": "hidden"})
        conn.commit()

        raw = action_options(conn, "char_darian")
        assert any(o.get("action") == "move" and o.get("target") == "loc_test_secret_vault" for o in raw)

        state = snapshot(conn, "char_darian")
        shaped = shape_action_options_for_needs(
            conn,
            state=state,
            action_options=raw,
            decision_signals={"needs_attention": []},
        )
        assert not any(o.get("action") == "move" and o.get("target") == "loc_test_secret_vault" for o in shaped)


def test_generic_preview_hides_concealed_destination_but_exact_known_move_remains(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, "char_darian", "loc_thorne_estate_private_lake_access")
        conn.commit()

        raw = action_options(conn, "char_darian")
        assert any(o.get("action") == "move" and o.get("target") == "loc_thorne_estate_hidden_dock" for o in raw)
        shaped = shape_action_options_for_needs(
            conn,
            state=snapshot(conn, "char_darian"),
            action_options=raw,
            decision_signals={"needs_attention": []},
        )
        assert any(o.get("action") == "move" and o.get("target") == "loc_thorne_estate_hidden_dock" for o in shaped)

        preview_names = {row["location_name"] for row in reachable_location_awareness(conn, "loc_thorne_estate_private_lake_access")}
        assert "Hidden Dock" not in preview_names

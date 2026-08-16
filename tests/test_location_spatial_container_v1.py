import json

from observer_sandbox.db import connect
from observer_sandbox.observer_query import location_summary
from observer_sandbox.runtime import initialize
from observer_sandbox.world import get_field, load_spatial_seed, load_world_seed


def test_all_existing_estate_locations_have_spatial_container_metadata(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    world = load_world_seed()
    spatial_seed = load_spatial_seed()

    expected_ids = {row["id"] for row in world["locations"]}
    assert set(spatial_seed["locations"]) == expected_ids

    with connect(db) as conn:
        for location_id in expected_ids:
            spatial = get_field(conn, location_id, "world.spatial_container")
            assert spatial["container"] is True
            assert spatial["source_status"]
            assert spatial["layout_status"]
            assert spatial["exposure"]
            assert spatial["interface_model"]
            assert spatial["completeness"] in {"L1", "L2", "L3", "L4"}

        revision = conn.execute(
            "SELECT value_json FROM runtime_state WHERE key='world_spatial_revision'"
        ).fetchone()
        assert json.loads(revision[0]) == spatial_seed["spatial_revision"]


def test_estate_container_preserves_source_backed_extent_without_identity_churn(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        estate = location_summary(conn, "loc_thorne_estate")
        spatial = get_field(conn, "loc_thorne_estate", "world.spatial_container")

        assert estate["location"]["id"] == "loc_thorne_estate"
        assert estate["location"]["kind"] == "estate"
        assert estate["parent"]["id"] == "world_observer_universe"
        assert spatial == {
            "container": True,
            "source_status": "source_confirmed",
            "layout_status": "canonical_structure",
            "exposure": "mixed",
            "extent": {"area_acres": 50.0, "precision": "approximate"},
            "boundary_type": "private_property",
            "interface_model": "topology_derived",
            "completeness": "L1",
        }

        spatial_row = conn.execute(
            """
            SELECT mode, authority, source
            FROM fields
            WHERE entity_id='loc_thorne_estate' AND field_key='world.spatial_container'
            """
        ).fetchone()
        assert tuple(spatial_row) == (
            "static",
            "world_definition",
            "thorne-estate-spatial-v1",
        )


def test_location_source_confidence_is_separate_from_layout_confidence(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        living = get_field(conn, "loc_thorne_estate_living_room", "world.spatial_container")
        foyer = get_field(conn, "loc_thorne_estate_foyer", "world.spatial_container")
        ground = get_field(conn, "loc_thorne_estate_ground_floor", "world.spatial_container")

        assert living["source_status"] == "source_confirmed"
        assert living["layout_status"] == "provisional_layout"
        assert foyer["source_status"] == "project_established"
        assert foyer["layout_status"] == "provisional_layout"
        assert ground["source_status"] == "source_confirmed"
        assert ground["layout_status"] == "provisional_layout"


def test_exterior_boundary_remains_a_locked_nontraversable_container(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        exterior = location_summary(conn, "loc_thorne_estate_exterior_boundary")
        spatial = get_field(
            conn,
            "loc_thorne_estate_exterior_boundary",
            "world.spatial_container",
        )

        assert exterior["location"]["access"] == "locked"
        assert exterior["exits"] == []
        assert spatial["container"] is True
        assert spatial["source_status"] == "structurally_inferred"
        assert spatial["boundary_type"] == "property_perimeter"
        assert spatial["exposure"] == "outdoor"
        assert spatial["traversable"] is False


def test_spatial_refactor_base_locations_are_preserved_and_outside_world_stays_absent(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    base_ids = {row["id"] for row in load_world_seed()["locations"]}

    with connect(db) as conn:
        actual_ids = {
            row[0]
            for row in conn.execute(
                "SELECT id FROM entities WHERE entity_type='location' ORDER BY id"
            ).fetchall()
        }

    assert base_ids <= actual_ids
    assert "loc_south_lake_tahoe" not in actual_ids
    assert not any(location_id.startswith("loc_south_lake_tahoe") for location_id in actual_ids)


def test_spatial_refactor_is_idempotent_and_preserves_actor_location(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    initialize(db)

    with connect(db) as conn:
        assert get_field(conn, "char_darian", "runtime.location") == "loc_thorne_estate_master_suite"
        duplicate_edges = conn.execute(
            """
            SELECT source_id, relation_type, target_id, COUNT(*) AS n
            FROM relations
            WHERE relation_type IN ('contains', 'connected_to')
            GROUP BY source_id, relation_type, target_id
            HAVING n > 1
            """
        ).fetchall()
        assert duplicate_edges == []

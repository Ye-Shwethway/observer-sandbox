from observer_sandbox.db import connect
from observer_sandbox.location_runtime import current_location
from observer_sandbox.observer_query import location_summary
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action
from observer_sandbox.world import get_field


CAMPUS_LOCATION_IDS = {
    "loc_thorne_estate_mansion_exterior",
    "loc_thorne_estate_core_grounds",
    "loc_thorne_estate_tactical_obstacle_course",
    "loc_thorne_estate_private_lake_access",
    "loc_thorne_estate_hidden_dock",
    "loc_thorne_estate_rear_forest",
    "loc_thorne_estate_concealed_forest_passage",
    "loc_thorne_estate_main_approach",
    "loc_thorne_estate_main_security_gate",
}


def _move(conn, target):
    options = action_options(conn, "char_darian")
    option = next(
        row for row in options
        if row.get("action") == "move" and row.get("target") == target
    )
    duration = max(5, int(option["duration"][0]))
    apply_action(conn, Action("move", duration, target, f"move to {option['target_name']}"), "char_darian")


def test_campus_seed_adds_only_private_estate_locations(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        ids = {
            row[0]
            for row in conn.execute(
                "SELECT id FROM entities WHERE entity_type='location'"
            ).fetchall()
        }
        assert CAMPUS_LOCATION_IDS <= ids
        assert "loc_south_lake_tahoe" not in ids
        assert not any(location_id.startswith("loc_south_lake_tahoe") for location_id in ids)

        revision = conn.execute(
            "SELECT value_json FROM runtime_state WHERE key='estate_campus_revision'"
        ).fetchone()
        assert revision is not None


def test_darian_can_leave_mansion_and_reach_outdoor_obstacle_course(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        assert current_location(conn, "char_darian") == "loc_thorne_estate_master_suite"

        _move(conn, "loc_thorne_estate_foyer")
        _move(conn, "loc_thorne_estate_mansion_exterior")
        _move(conn, "loc_thorne_estate_core_grounds")
        _move(conn, "loc_thorne_estate_tactical_obstacle_course")

        assert current_location(conn, "char_darian") == "loc_thorne_estate_tactical_obstacle_course"
        options = action_options(conn, "char_darian")
        train = [
            row for row in options
            if row.get("action") == "train"
            and row.get("target") == "obj_thorne_estate_outdoor_obstacle_course"
        ]
        assert train

        spatial = get_field(
            conn,
            "loc_thorne_estate_tactical_obstacle_course",
            "world.spatial_container",
        )
        assert spatial["source_status"] == "source_confirmed"
        assert spatial["exposure"] == "outdoor"
        assert spatial["completeness"] == "L3"


def test_darian_can_return_from_campus_to_mansion(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        for target in (
            "loc_thorne_estate_foyer",
            "loc_thorne_estate_mansion_exterior",
            "loc_thorne_estate_core_grounds",
            "loc_thorne_estate_rear_forest",
        ):
            _move(conn, target)

        assert current_location(conn, "char_darian") == "loc_thorne_estate_rear_forest"

        for target in (
            "loc_thorne_estate_core_grounds",
            "loc_thorne_estate_mansion_exterior",
            "loc_thorne_estate_foyer",
            "loc_thorne_estate_master_suite",
        ):
            _move(conn, target)

        assert current_location(conn, "char_darian") == "loc_thorne_estate_master_suite"


def test_three_estate_side_egress_endpoints_remain_closed_to_outside_world(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        gate = location_summary(conn, "loc_thorne_estate_main_security_gate")
        forest = location_summary(conn, "loc_thorne_estate_concealed_forest_passage")
        dock = location_summary(conn, "loc_thorne_estate_hidden_dock")
        legacy_boundary = location_summary(conn, "loc_thorne_estate_exterior_boundary")

        assert {row["id"] for row in gate["exits"]} == {"loc_thorne_estate_main_approach"}
        assert {row["id"] for row in forest["exits"]} == {"loc_thorne_estate_rear_forest"}
        assert {row["id"] for row in dock["exits"]} == {"loc_thorne_estate_private_lake_access"}
        assert legacy_boundary["exits"] == []

        for location in (gate, forest, dock, legacy_boundary):
            exit_ids = {row["id"] for row in location["exits"]}
            assert not any("south_lake_tahoe" in target for target in exit_ids)


def test_campus_locations_expose_meaningful_machine_readable_options(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        placements = {
            "loc_thorne_estate_tactical_obstacle_course": ("train", "obj_thorne_estate_outdoor_obstacle_course"),
            "loc_thorne_estate_private_lake_access": ("use", "obj_thorne_estate_lake_water_purification"),
            "loc_thorne_estate_hidden_dock": ("use", "obj_thorne_estate_hidden_dock_fixture"),
            "loc_thorne_estate_rear_forest": ("use", "obj_thorne_estate_rear_forest_trail"),
            "loc_thorne_estate_main_security_gate": ("use", "obj_thorne_estate_main_gate_control"),
        }

        for location_id, (action_name, target_id) in placements.items():
            conn.execute(
                "DELETE FROM relations WHERE source_id='char_darian' AND relation_type='located_at'"
            )
            conn.execute(
                "INSERT INTO relations(source_id,relation_type,target_id) VALUES('char_darian','located_at',?)",
                (location_id,),
            )
            conn.commit()
            options = action_options(conn, "char_darian")
            assert any(
                option.get("action") == action_name and option.get("target") == target_id
                for option in options
            )


def test_campus_seed_is_idempotent_and_preserves_base_interior_topology(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    initialize(db)

    with connect(db) as conn:
        duplicate_relations = conn.execute(
            """
            SELECT source_id, relation_type, target_id, COUNT(*) AS n
            FROM relations
            WHERE relation_type IN ('contains', 'connected_to')
            GROUP BY source_id, relation_type, target_id
            HAVING n > 1
            """
        ).fetchall()
        assert duplicate_relations == []

        foyer_exits = {
            row["id"]
            for row in location_summary(conn, "loc_thorne_estate_foyer")["exits"]
        }
        assert "loc_thorne_estate_living_room" in foyer_exits
        assert "loc_thorne_estate_library" in foyer_exits
        assert "loc_thorne_estate_mansion_exterior" in foyer_exits

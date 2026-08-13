from observer_sandbox.db import connect
from observer_sandbox.observer_query import character_summary, location_summary, observer_status, recent_history
from observer_sandbox.runtime import initialize


def test_observer_query_surfaces_are_generic(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        character = character_summary(conn, "char_darian")
        assert character["character"]["id"] == "char_darian"
        assert character["state"]["location"] == "loc_thorne_estate_master_suite"

        home = location_summary(conn, "loc_thorne_estate")
        assert home["location"]["id"] == "loc_thorne_estate"
        assert home["location"]["kind"] == "estate"
        assert home["parent"]["id"] == "world_observer_universe"
        assert {child["id"] for child in home["child_locations"]} >= {
            "loc_thorne_estate_ground_floor",
            "loc_thorne_estate_second_floor",
            "loc_thorne_estate_third_floor",
            "loc_thorne_estate_underground",
            "loc_thorne_estate_exterior_boundary",
        }
        assert any(row["id"] == "char_darian" for row in home["residents"])

        underground = location_summary(conn, "loc_thorne_estate_underground")
        assert {child["id"] for child in underground["child_locations"]} >= {
            "loc_thorne_estate_training_hall",
            "loc_thorne_estate_home_gym",
            "loc_thorne_estate_medical_bay",
            "loc_thorne_estate_armory",
            "loc_thorne_estate_food_storage",
            "loc_thorne_estate_bunker",
        }

        bedroom = location_summary(conn, "loc_thorne_estate_master_suite")
        assert bedroom["parent"]["id"] == "loc_thorne_estate_second_floor"
        assert any(child["id"] == "obj_thorne_estate_master_bed" for child in bedroom["objects"])
        assert any(row["id"] == "char_darian" for row in bedroom["occupants"])
        assert bedroom["exits"]

        exterior = location_summary(conn, "loc_thorne_estate_exterior_boundary")
        assert exterior["location"]["access"] == "locked"
        assert exterior["exits"] == []

        assert recent_history(conn, limit=5) == []
        status = observer_status(conn)
        assert status["autonomy_enabled"] is False
        assert status["recent_history"] == []

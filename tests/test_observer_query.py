from observer_sandbox.db import connect
from observer_sandbox.observer_query import character_summary, location_summary, observer_status, recent_history
from observer_sandbox.runtime import initialize


def test_observer_query_surfaces_are_generic(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        character = character_summary(conn, "char_darian")
        assert character["character"]["id"] == "char_darian"
        assert character["state"]["location"] == "room_bedroom"

        home = location_summary(conn, "home")
        assert home["location"]["id"] == "home"
        assert home["location"]["kind"] == "estate"
        assert home["parent"]["id"] == "observer_universe"
        assert {child["id"] for child in home["child_locations"]} >= {
            "zone_ground",
            "zone_second",
            "zone_third",
            "zone_underground",
            "boundary_exterior",
        }
        assert any(row["id"] == "char_darian" for row in home["residents"])

        underground = location_summary(conn, "zone_underground")
        assert {child["id"] for child in underground["child_locations"]} >= {
            "room_training",
            "room_gym",
            "room_medical",
            "room_armory",
            "room_food_storage",
            "room_bunker",
        }

        bedroom = location_summary(conn, "room_bedroom")
        assert bedroom["parent"]["id"] == "zone_second"
        assert any(child["id"] == "obj_bed" for child in bedroom["objects"])
        assert any(row["id"] == "char_darian" for row in bedroom["occupants"])
        assert bedroom["exits"]

        exterior = location_summary(conn, "boundary_exterior")
        assert exterior["location"]["access"] == "locked"
        assert exterior["exits"] == []

        assert recent_history(conn, limit=5) == []
        status = observer_status(conn)
        assert status["autonomy_enabled"] is False
        assert status["recent_history"] == []

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
        assert {child["id"] for child in home["children"]} >= {"room_bedroom", "room_kitchen", "room_gym"}
        assert any(row["id"] == "char_darian" for row in home["residents"])

        bedroom = location_summary(conn, "room_bedroom")
        assert any(child["id"] == "obj_bed" for child in bedroom["children"])
        assert any(row["id"] == "char_darian" for row in bedroom["occupants"])

        assert recent_history(conn, limit=5) == []
        status = observer_status(conn)
        assert status["autonomy_enabled"] is False
        assert status["recent_history"] == []

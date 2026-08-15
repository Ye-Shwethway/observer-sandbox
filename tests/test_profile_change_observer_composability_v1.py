from observer_sandbox.db import connect
from observer_sandbox.profile_change_observer import capture_profile_change_state, observe_profile_changes
from observer_sandbox.runtime import initialize


def test_profile_change_observer_noops_for_actor_without_profile(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        conn.execute("INSERT INTO entities(id,entity_type,name) VALUES('char_synthetic','character','Synthetic Actor')")
        conn.commit()
        assert capture_profile_change_state(conn, "char_synthetic") == {}
        assert observe_profile_changes(
            conn,
            "char_synthetic",
            {},
            {},
            sim_time="2025-05-06T06:00:00+00:00",
        ) == []

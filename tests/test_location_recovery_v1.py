from observer_sandbox.db import connect
from observer_sandbox.location_runtime import current_location, set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import load_world_seed, set_field


def _erase_actor_location(conn, actor_id: str) -> None:
    conn.execute(
        "DELETE FROM relations WHERE source_id=? AND relation_type='located_at'",
        (actor_id,),
    )
    # Preserve the field row but make its value unusable. This reproduces the
    # production-invalid state that ordinary seed-if-missing logic cannot repair.
    set_field(conn, actor_id, "runtime.location", None)
    conn.commit()


def test_initialize_repairs_missing_default_actor_location_from_world_start(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _erase_actor_location(conn, "char_darian")
        assert current_location(conn, "char_darian") is None

    initialize(db)

    with connect(db) as conn:
        expected = load_world_seed()["start_location"]
        assert current_location(conn, "char_darian") == expected
        assert snapshot(conn, "char_darian")["location"] == expected


def test_initialize_prefers_latest_represented_action_place_over_seed_fallback(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_dynamic_location(conn, "char_darian", "loc_thorne_estate_kitchen")
        conn.execute(
            """INSERT INTO action_instances(
                id,action_type,actor_id,place_id,target_id,status,duration_minutes,intent,
                participants_json,resources_json,conditions_json,modifiers_json,planned_sim_time,
                started_sim_time,ended_sim_time
            ) VALUES(?,?,?,?,?,'completed',?,?,?,?,?,?,?,?,?)""",
            (
                "location-recovery-evidence",
                "idle",
                "char_darian",
                "loc_thorne_estate_kitchen",
                None,
                5,
                "location recovery fixture",
                "[]",
                "[]",
                "{}",
                "{}",
                "2025-05-03T09:00:00+00:00",
                "2025-05-03T09:00:00+00:00",
                "2025-05-03T09:05:00+00:00",
            ),
        )
        conn.commit()
        _erase_actor_location(conn, "char_darian")

    initialize(db)

    with connect(db) as conn:
        assert current_location(conn, "char_darian") == "loc_thorne_estate_kitchen"

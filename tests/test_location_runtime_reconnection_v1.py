from observer_sandbox.db import connect
from observer_sandbox.location_runtime import current_location
from observer_sandbox.observer_query import location_summary, object_summary, recent_history
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.world import get_field


def _option(options, action, target):
    return next(
        row for row in options
        if row.get("action") == action and row.get("target") == target
    )


def test_refactored_location_metadata_coexists_with_current_gameplay_snapshot(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        spatial = get_field(conn, state["location"], "world.spatial_container")

        assert state["location"] == "loc_thorne_estate_master_suite"
        assert state["location_name"] == "Darian's Master Suite"
        assert spatial["container"] is True
        assert spatial["exposure"] == "indoor"
        assert spatial["layout_status"] == "provisional_layout"


def test_refactored_location_metadata_does_not_change_legal_local_options(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        options = action_options(conn, "char_darian")

        _option(options, "move", "loc_thorne_estate_master_bathroom")
        _option(options, "sleep", "obj_thorne_estate_master_bed")

        move_targets = {
            row["target"]
            for row in options
            if row.get("action") == "move"
        }
        assert "loc_thorne_estate_exterior_boundary" not in move_targets
        assert all(not target.startswith("loc_south_lake_tahoe") for target in move_targets)


def test_move_reconnects_location_state_event_history_and_followup_options(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        apply_action(
            conn,
            Action(
                "move",
                5,
                "loc_thorne_estate_master_bathroom",
                "go to the bathroom",
            ),
            "char_darian",
        )

        assert current_location(conn, "char_darian") == "loc_thorne_estate_master_bathroom"
        state = snapshot(conn, "char_darian")
        assert state["location"] == "loc_thorne_estate_master_bathroom"

        history = recent_history(conn, character_id="char_darian", limit=3)
        assert history[0]["action"] == "move"
        assert history[0]["target"] == "loc_thorne_estate_master_bathroom"

        event = conn.execute(
            """
            SELECT location_id, action_id
            FROM events
            WHERE actor_id='char_darian' AND event_type='action_completed'
            ORDER BY id DESC LIMIT 1
            """
        ).fetchone()
        assert event["location_id"] == "loc_thorne_estate_master_suite"
        assert event["action_id"]

        followup = action_options(conn, "char_darian")
        _option(followup, "move", "loc_thorne_estate_master_suite")
        _option(followup, "shower", "obj_thorne_estate_master_shower")


def test_observer_location_query_and_object_location_stay_connected(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        room = location_summary(conn, "loc_thorne_estate_home_gym")
        bag = object_summary(conn, "obj_thorne_estate_gym_heavy_bag")
        spatial = get_field(conn, "loc_thorne_estate_home_gym", "world.spatial_container")

        assert room["location"]["id"] == "loc_thorne_estate_home_gym"
        assert room["parent"]["id"] == "loc_thorne_estate_underground"
        assert any(obj["id"] == "obj_thorne_estate_gym_heavy_bag" for obj in room["objects"])
        assert bag["location"]["id"] == "loc_thorne_estate_home_gym"
        assert "train" in bag["capabilities"]
        assert spatial["completeness"] == "L3"


def test_training_location_consumer_remains_available_after_spatial_refactor(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        conn.execute(
            "DELETE FROM relations WHERE source_id='char_darian' AND relation_type='located_at'"
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id) VALUES('char_darian','located_at','loc_thorne_estate_home_gym')"
        )
        conn.commit()

        options = action_options(conn, "char_darian")
        train_targets = {
            row["target"]
            for row in options
            if row.get("action") == "train"
        }

        assert "obj_thorne_estate_gym_free_weights" in train_targets
        assert "obj_thorne_estate_gym_heavy_bag" in train_targets
        assert current_location(conn, "char_darian") == "loc_thorne_estate_home_gym"


def test_locked_exterior_remains_absent_from_observer_exit_and_gameplay_options(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        boundary = location_summary(conn, "loc_thorne_estate_exterior_boundary")
        assert boundary["location"]["access"] == "locked"
        assert boundary["exits"] == []

        all_move_targets = set()
        rows = conn.execute(
            "SELECT id FROM entities WHERE entity_type='location' AND id != 'loc_thorne_estate_exterior_boundary'"
        ).fetchall()
        for row in rows:
            conn.execute(
                "DELETE FROM relations WHERE source_id='char_darian' AND relation_type='located_at'"
            )
            conn.execute(
                "INSERT INTO relations(source_id,relation_type,target_id) VALUES('char_darian','located_at',?)",
                (row["id"],),
            )
            conn.commit()
            all_move_targets.update(
                option["target"]
                for option in action_options(conn, "char_darian")
                if option.get("action") == "move"
            )

        assert "loc_thorne_estate_exterior_boundary" not in all_move_targets

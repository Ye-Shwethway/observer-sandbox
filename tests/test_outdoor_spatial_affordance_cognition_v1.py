from observer_sandbox.cognition_capability_awareness import cognition_capability_awareness
from observer_sandbox.db import connect
from observer_sandbox.resource_awareness import reachable_location_awareness
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import ACTION_NAMES, Action, action_options, apply_action


DAR = "char_darian"


def _place(conn, location_id: str) -> None:
    conn.execute(
        "DELETE FROM relations WHERE source_id=? AND relation_type='located_at'",
        (DAR,),
    )
    conn.execute(
        "INSERT INTO relations(source_id,relation_type,target_id) VALUES(?, 'located_at', ?)",
        (DAR, location_id),
    )
    conn.commit()


def _actions(conn) -> set[str]:
    return {str(option["action"]) for option in action_options(conn, DAR)}


def test_outdoor_activity_actions_are_generic_runtime_vocabulary(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    assert {"walk", "relax", "observe"} <= set(ACTION_NAMES)
    with connect(db) as conn:
        rows = {
            row["action_type"]: row
            for row in conn.execute(
                "SELECT action_type,target_mode,required_capability FROM action_definitions WHERE action_type IN ('walk','relax','observe')"
            ).fetchall()
        }
        assert set(rows) == {"walk", "relax", "observe"}
        assert all(rows[name]["target_mode"] == "none" for name in rows)
        assert rows["walk"]["required_capability"] == "walk"
        assert rows["relax"]["required_capability"] == "relax"
        assert rows["observe"]["required_capability"] == "observe"


def test_location_authored_affordances_create_outdoor_actions_only_where_supported(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _place(conn, "loc_thorne_estate_core_grounds")
        assert {"walk", "relax", "observe"} <= _actions(conn)

        _place(conn, "loc_thorne_estate_private_lake_access")
        lake = _actions(conn)
        assert {"relax", "observe"} <= lake
        assert "walk" not in lake

        _place(conn, "loc_thorne_estate_rear_forest")
        assert {"walk", "relax", "observe"} <= _actions(conn)

        _place(conn, "loc_thorne_estate_main_security_gate")
        gate = _actions(conn)
        assert "walk" not in gate
        assert "relax" not in gate
        assert "observe" not in gate

        _place(conn, "loc_thorne_estate_master_suite")
        indoors = _actions(conn)
        assert "walk" not in indoors
        assert "relax" not in indoors
        assert "observe" not in indoors


def test_outdoor_walk_executes_without_becoming_travel_or_hard_requirement(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _place(conn, "loc_thorne_estate_core_grounds")
        before = conn.execute(
            "SELECT value_json FROM fields WHERE entity_id=? AND field_key='needs.energy' ORDER BY id DESC LIMIT 1",
            (DAR,),
        ).fetchone()
        apply_action(conn, Action("walk", 30, None, "take an easy walk around the grounds"), DAR)

        located = conn.execute(
            "SELECT target_id FROM relations WHERE source_id=? AND relation_type='located_at'",
            (DAR,),
        ).fetchone()
        assert located["target_id"] == "loc_thorne_estate_core_grounds"

        event = conn.execute(
            "SELECT payload_json FROM events WHERE actor_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
            (DAR,),
        ).fetchone()
        assert '"action": "walk"' in event["payload_json"]

        # Ordinary indoor rest remains legal elsewhere; this feature adds choices rather than a forced outing.
        _place(conn, "loc_thorne_estate_living_room")
        assert "rest" in _actions(conn)


def test_one_hop_preview_explains_what_core_grounds_offer_after_arrival(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        previews = reachable_location_awareness(conn, "loc_thorne_estate_mansion_exterior")
        core = next(row for row in previews if row["location_name"] == "Core Estate Grounds")
        assert {"walk", "relax", "observe"} <= set(core["available_actions_after_move"])
        assert {"walk", "relax", "observe"} <= set(core["location_affordances"])
        assert core["planning_only"] is True


def test_known_map_projects_normal_outdoor_lifestyle_destinations_without_egress_bias(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        awareness = cognition_capability_awareness(conn, DAR)
        spatial = awareness["reasoning_profile"]["spatial_knowledge"]
        destinations = {
            row["location_name"]: set(row["activities"])
            for row in spatial["outdoor_lifestyle_destinations"]
        }

        assert {"walk", "relax", "observe"} <= destinations["Core Estate Grounds"]
        assert {"relax", "observe"} <= destinations["Private Lake Access"]
        assert {"walk", "relax", "observe"} <= destinations["Rear Forested Estate"]
        assert {"observe", "relax"} <= destinations["Mansion Exterior"]

        assert "Hidden Dock" not in destinations
        assert "Concealed Forest Passage" not in destinations
        assert "Main Security Gate" not in destinations
        assert "Main Estate Approach" not in destinations
        assert not any("Tahoe" in name for name in destinations)

        assert "quota" in spatial["outdoor_guidance"]
        assert all(row["planning_only"] is True for row in spatial["outdoor_lifestyle_destinations"])

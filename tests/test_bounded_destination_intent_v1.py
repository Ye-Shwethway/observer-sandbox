from observer_sandbox.bounded_destination_intent import bounded_destination_intent_awareness
from observer_sandbox.cognition_capability_awareness import cognition_capability_awareness
from observer_sandbox.db import connect
from observer_sandbox.location_runtime import set_dynamic_location
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import action_options


ACTOR = "char_darian"
LIVING_ROOM = "loc_thorne_estate_living_room"
FOYER = "loc_thorne_estate_foyer"
MANSION_EXTERIOR = "loc_thorne_estate_mansion_exterior"
CORE_GROUNDS = "loc_thorne_estate_core_grounds"


def _route_by_destination(awareness):
    return {row["destination_name"]: row for row in awareness["routes"]}


def _place_actor(conn, location_id):
    set_dynamic_location(conn, ACTOR, location_id)
    conn.commit()


def test_known_distant_destination_exposes_purpose_bearing_first_hop_only(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _place_actor(conn, LIVING_ROOM)

        exact_moves = {
            row["target"]: row["target_name"]
            for row in action_options(conn, ACTOR)
            if row.get("action") == "move"
        }
        assert FOYER in exact_moves
        assert CORE_GROUNDS not in exact_moves

        awareness = bounded_destination_intent_awareness(conn, ACTOR)
        routes = _route_by_destination(awareness)
        grounds = routes["Core Estate Grounds"]

        assert awareness["mode"] == "bounded_route_awareness_v1"
        assert grounds["first_hop_name"] == exact_moves[FOYER] == "Grand Foyer"
        assert grounds["route_hops"] == 3
        assert {"walk", "relax", "observe"} <= set(grounds["arrival_affordances"])
        assert grounds["planning_only"] is True
        assert "destination_id" not in grounds
        assert "first_hop_id" not in grounds
        assert all(not key.endswith("_id") for row in awareness["routes"] for key in row)


def test_unknown_destination_is_not_leaked_from_objective_topology(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _place_actor(conn, LIVING_ROOM)
        conn.execute(
            """DELETE FROM character_memories
               WHERE character_id=? AND memory_type='semantic'
                 AND json_extract(content_json,'$.knowledge_kind')='spatial_familiarity'
                 AND json_extract(content_json,'$.location_id')=?""",
            (ACTOR, CORE_GROUNDS),
        )
        conn.commit()

        awareness = bounded_destination_intent_awareness(conn, ACTOR)
        assert "Core Estate Grounds" not in _route_by_destination(awareness)


def test_route_preview_is_bounded_and_reacts_to_topology_change(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _place_actor(conn, LIVING_ROOM)

        bounded = bounded_destination_intent_awareness(conn, ACTOR, max_hops=2)
        names = set(_route_by_destination(bounded))
        assert "Mansion Exterior" in names
        assert "Core Estate Grounds" not in names

        conn.execute(
            "DELETE FROM relations WHERE source_id=? AND relation_type='connected_to' AND target_id=?",
            (FOYER, MANSION_EXTERIOR),
        )
        conn.commit()
        changed = bounded_destination_intent_awareness(conn, ACTOR)
        assert "Core Estate Grounds" not in _route_by_destination(changed)


def test_no_represented_spatial_memory_means_no_multi_hop_world_truth_leak(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _place_actor(conn, LIVING_ROOM)
        conn.execute(
            """DELETE FROM character_memories
               WHERE character_id=? AND memory_type='semantic'
                 AND json_extract(content_json,'$.knowledge_kind')='spatial_familiarity'""",
            (ACTOR,),
        )
        conn.commit()

        awareness = bounded_destination_intent_awareness(conn, ACTOR)
        assert awareness["mode"] == "unavailable_without_represented_spatial_knowledge"
        assert awareness["routes"] == []


def test_cognition_capability_context_includes_bounded_destination_awareness(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _place_actor(conn, LIVING_ROOM)
        awareness = cognition_capability_awareness(conn, ACTOR)
        bounded = awareness["reasoning_profile"]["bounded_destination_intent"]
        routes = _route_by_destination(bounded)

        assert routes["Core Estate Grounds"]["first_hop_name"] == "Grand Foyer"
        assert "plans or action authority" in bounded["guidance"]

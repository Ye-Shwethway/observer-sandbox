from observer_sandbox.db import connect
from observer_sandbox.resource_awareness import enrich_options_with_usage
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import action_options


FOYER = "loc_thorne_estate_foyer"
EXTERIOR = "loc_thorne_estate_mansion_exterior"


def _place_actor(conn, location_id: str) -> None:
    conn.execute(
        "DELETE FROM relations WHERE source_id='char_darian' AND relation_type='located_at'"
    )
    conn.execute(
        "INSERT INTO relations(source_id,relation_type,target_id) VALUES('char_darian','located_at',?)",
        (location_id,),
    )
    conn.commit()


def _move_targets(options):
    return {
        str(option["target"])
        for option in options
        if option.get("action") == "move" and isinstance(option.get("target"), str)
    }


def _repeated_usage(legal_moves):
    return {
        ("move", target): {
            "recent_uses": 8,
            "last_used_sim_time": "2025-05-10T09:00:00+00:00",
            "recently_repeated": True,
            "event_distance": 0,
            "last_before": {},
            "last_after": {},
        }
        for target in legal_moves
    }


def test_repetition_shaping_preserves_every_legal_foyer_route(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _place_actor(conn, FOYER)
        raw = action_options(conn, "char_darian")
        legal_moves = _move_targets(raw)
        assert EXTERIOR in legal_moves
        assert len(legal_moves) > 1

        shaped = enrich_options_with_usage(raw, _repeated_usage(legal_moves))

        assert _move_targets(shaped) == legal_moves


def test_repeated_transit_history_is_context_not_route_removal(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _place_actor(conn, FOYER)
        raw = action_options(conn, "char_darian")
        legal_moves = _move_targets(raw)
        shaped = enrich_options_with_usage(raw, _repeated_usage(legal_moves))

        exterior = next(
            option for option in shaped
            if option.get("action") == "move" and option.get("target") == EXTERIOR
        )
        assert exterior["recent_usage"]["recent_uses"] == 8
        assert exterior["recent_usage"]["recently_repeated"] is True
        assert EXTERIOR in _move_targets(shaped)

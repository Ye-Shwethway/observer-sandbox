from observer_sandbox.db import connect
from observer_sandbox.need_resolution import shape_action_options_for_needs
from observer_sandbox.resource_awareness import enrich_options_with_usage
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import action_options, snapshot


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


def test_repetition_shaping_preserves_every_legal_foyer_route(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _place_actor(conn, FOYER)
        raw = action_options(conn, "char_darian")
        legal_moves = _move_targets(raw)
        assert EXTERIOR in legal_moves
        assert len(legal_moves) > 1

        usage = {
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
        shaped = enrich_options_with_usage(raw, usage)

        assert _move_targets(shaped) == legal_moves


def test_strong_need_shaping_keeps_all_legal_transit_edges_visible(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        _place_actor(conn, FOYER)
        state = snapshot(conn, "char_darian")
        state["hunger"] = 90.0
        raw = action_options(conn, "char_darian")
        legal_moves = _move_targets(raw)
        assert EXTERIOR in legal_moves
        assert len(legal_moves) > 1

        decision_signals = {
            "needs_attention": [
                {
                    "need": "hunger",
                    "level": "strong",
                    "value": 90.0,
                    "threshold": 70.0,
                }
            ],
            "highest_priority": {
                "need": "hunger",
                "level": "strong",
                "value": 90.0,
                "threshold": 70.0,
            },
        }
        shaped = shape_action_options_for_needs(
            conn,
            state=state,
            action_options=raw,
            decision_signals=decision_signals,
        )

        assert _move_targets(shaped) == legal_moves
        guided = [option for option in shaped if option.get("action") == "move"]
        assert all(option.get("need_route", {}).get("need") == "hunger" for option in guided)
        assert any(option.get("need_route", {}).get("recommended") for option in guided)

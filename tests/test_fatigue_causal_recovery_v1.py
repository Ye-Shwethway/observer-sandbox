from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, action_options, apply_action, snapshot
from observer_sandbox.world import set_field

TRAINING_HALL = "loc_thorne_estate_training_hall"


def _set_state(
    conn,
    *,
    fatigue: float,
    location: str = TRAINING_HALL,
    energy: float = 75.0,
    sleepiness: float = 15.0,
    thirst: float = 15.0,
    hunger: float = 20.0,
    cleanliness: float = 80.0,
) -> None:
    set_field(conn, "char_darian", "runtime.location", location)
    set_field(conn, "char_darian", "physiology.fatigue", fatigue)
    set_field(conn, "char_darian", "needs.energy", energy)
    set_field(conn, "char_darian", "needs.sleepiness", sleepiness)
    set_field(conn, "char_darian", "needs.thirst", thirst)
    set_field(conn, "char_darian", "needs.hunger", hunger)
    set_field(conn, "char_darian", "physiology.cleanliness", cleanliness)
    conn.commit()


def _enriched(conn):
    return ModelDecisionProvider(conn)._enrich_state(snapshot(conn, "char_darian"))


def test_critical_fatigue_forces_causal_recovery_and_blocks_training_adjacent_inspection(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_state(conn, fatigue=72.4)
        enriched = _enriched(conn)

        highest = enriched["decision_signals"]["highest_priority"]
        assert highest["need"] == "fatigue"
        assert highest["level"] == "critical"
        assert highest["threshold"] == 70.0
        assert {(o["action"], o["target"]) for o in enriched["action_options"]} == {("rest", None)}
        assert all(o["action"] not in {"train", "inspect", "use"} for o in enriched["action_options"])


def test_rest_naturally_reduces_fatigue_below_strong_recovery_threshold(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_state(conn, fatigue=72.4)
        before = snapshot(conn, "char_darian")
        after = apply_action(conn, Action("rest", 180, None, "recover from systemic fatigue"), "char_darian")

        assert after["fatigue"] < before["fatigue"]
        assert after["fatigue"] < 55.0
        enriched = _enriched(conn)
        assert all(item["need"] != "fatigue" for item in enriched["decision_signals"]["needs_attention"])


def test_immediate_repeat_of_same_inspect_target_is_removed_from_candidates(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_state(conn, fatigue=20.0)
        raw = action_options(conn, "char_darian")
        inspect_option = next(option for option in raw if option["action"] == "inspect")
        sim_time = snapshot(conn, "char_darian")["sim_time"]
        record_event(
            conn,
            sim_time=sim_time,
            actor_id="char_darian",
            event_type="action_completed",
            location_id=TRAINING_HALL,
            payload={
                "action": "inspect",
                "target": inspect_option["target"],
                "reason": "check equipment",
            },
        )
        conn.commit()

        enriched = _enriched(conn)
        pairs = {(o["action"], o["target"]) for o in enriched["action_options"]}
        assert ("inspect", inspect_option["target"]) not in pairs
        assert pairs


def test_two_same_room_discretionary_object_interactions_suppress_further_inspect_use_loop(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_state(conn, fatigue=20.0)
        sim_time = snapshot(conn, "char_darian")["sim_time"]
        for action, target in (("inspect", "fixture_a"), ("use", "fixture_b")):
            record_event(
                conn,
                sim_time=sim_time,
                actor_id="char_darian",
                event_type="action_completed",
                location_id=TRAINING_HALL,
                payload={"action": action, "target": target, "reason": "fixture"},
            )
        conn.commit()

        enriched = _enriched(conn)
        assert enriched["action_options"]
        assert all(option["action"] not in {"inspect", "use"} for option in enriched["action_options"])
        assert any(option["action"] in {"move", "rest", "idle", "train"} for option in enriched["action_options"])

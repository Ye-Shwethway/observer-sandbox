from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field


FOOD_STORAGE = "loc_thorne_estate_food_storage"
HOME_GYM = "loc_thorne_estate_home_gym"
TRAINING_HALL = "loc_thorne_estate_training_hall"
LIVING_ROOM = "loc_thorne_estate_living_room"
SUPPLY_SHELVES = "obj_thorne_estate_food_storage_supply_shelves"
FOOD_PROVISIONS = "obj_thorne_estate_food_storage_provisions"


def _set_strong_hunger(conn, *, location: str, hunger: float = 61.3, thirst: float = 50.2) -> None:
    set_field(conn, "char_darian", "runtime.location", location)
    set_field(conn, "char_darian", "needs.hunger", hunger)
    set_field(conn, "char_darian", "needs.thirst", thirst)
    set_field(conn, "char_darian", "needs.energy", 69.6)
    set_field(conn, "char_darian", "needs.sleepiness", 10.8)
    set_field(conn, "char_darian", "physiology.cleanliness", 41.3)
    conn.commit()


def test_food_storage_exposes_real_food_and_suppresses_inspect_loop_under_strong_hunger(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_strong_hunger(conn, location=FOOD_STORAGE)
        state = snapshot(conn, "char_darian")
        enriched = ModelDecisionProvider(conn)._enrich_state(state)
        options = enriched["action_options"]

        assert options == [
            {
                "action": "eat",
                "target": FOOD_PROVISIONS,
                "target_name": "Stored Food Provisions",
                "duration": (5, 90),
                "effects": {"needs.hunger": -50.0, "needs.energy": 8.0, "needs.thirst": 2.0},
            }
        ]
        assert all(option.get("target") != SUPPLY_SHELVES for option in options)
        assert all(option["action"] != "train" for option in options)


def test_eating_stored_food_resolves_strong_hunger(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_strong_hunger(conn, location=FOOD_STORAGE)
        before = snapshot(conn, "char_darian")
        after = apply_action(
            conn,
            Action("eat", 20, FOOD_PROVISIONS, "resolve strong hunger with stored provisions"),
            "char_darian",
        )
        assert before["hunger"] == 61.3
        assert after["hunger"] < 55.0
        assert after["hunger"] < before["hunger"]

        follow_up = ModelDecisionProvider(conn)._enrich_state(after)["action_options"]
        assert len(follow_up) > 1
        assert any(option["action"] != "eat" for option in follow_up)


def test_strong_hunger_routes_only_toward_nearest_authored_food_resolvers(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_strong_hunger(conn, location=HOME_GYM, thirst=49.0)
        state = snapshot(conn, "char_darian")
        options = ModelDecisionProvider(conn)._enrich_state(state)["action_options"]

        assert options
        assert all(option["action"] == "move" for option in options)
        assert {option["target"] for option in options} == {TRAINING_HALL, LIVING_ROOM}
        assert all(option["action"] != "train" for option in options)


def test_competing_critical_need_prevents_hunger_guard_from_overriding_priority(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_strong_hunger(conn, location=FOOD_STORAGE, hunger=61.3, thirst=80.0)
        state = snapshot(conn, "char_darian")
        options = ModelDecisionProvider(conn)._enrich_state(state)["action_options"]

        # v1 must not force hunger resolution over a different critical need.
        assert any(option["action"] == "inspect" and option["target"] == SUPPLY_SHELVES for option in options)
        assert any(option["action"] == "eat" and option["target"] == FOOD_PROVISIONS for option in options)

from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field


FOOD_STORAGE = "loc_thorne_estate_food_storage"
HOME_GYM = "loc_thorne_estate_home_gym"
TRAINING_HALL = "loc_thorne_estate_training_hall"
LIVING_ROOM = "loc_thorne_estate_living_room"
KITCHEN = "loc_thorne_estate_kitchen"
SUPPLY_SHELVES = "obj_thorne_estate_food_storage_supply_shelves"
FOOD_PROVISIONS = "obj_thorne_estate_food_storage_provisions"
DRINKING_WATER = "obj_thorne_estate_kitchen_drinking_water"


def _set_needs(
    conn,
    *,
    location: str,
    hunger: float = 61.3,
    thirst: float = 49.0,
    energy: float = 69.6,
    sleepiness: float = 10.8,
    cleanliness: float = 60.0,
) -> None:
    set_field(conn, "char_darian", "runtime.location", location)
    set_field(conn, "char_darian", "needs.hunger", hunger)
    set_field(conn, "char_darian", "needs.thirst", thirst)
    set_field(conn, "char_darian", "needs.energy", energy)
    set_field(conn, "char_darian", "needs.sleepiness", sleepiness)
    set_field(conn, "char_darian", "physiology.cleanliness", cleanliness)
    conn.commit()


def test_food_storage_exposes_real_food_and_suppresses_inspect_loop_under_strong_hunger(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=FOOD_STORAGE, hunger=61.3, thirst=49.0)
        state = snapshot(conn, "char_darian")
        options = ModelDecisionProvider(conn)._enrich_state(state)["action_options"]

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


def test_same_level_thirst_precedes_hunger_using_authored_need_order(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=FOOD_STORAGE, hunger=62.9, thirst=51.9)
        state = snapshot(conn, "char_darian")
        enriched = ModelDecisionProvider(conn)._enrich_state(state)

        assert [item["need"] for item in enriched["decision_signals"]["needs_attention"][:2]] == ["thirst", "hunger"]
        options = enriched["action_options"]
        assert options
        assert all(option["action"] == "move" for option in options)
        assert {option["target"] for option in options} == {TRAINING_HALL}
        assert all(option["action"] != "train" for option in options)
        assert all(option["action"] != "eat" for option in options)


def test_strong_thirst_routes_to_water_and_blocks_training_until_resolved(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=TRAINING_HALL, hunger=13.7, thirst=55.2)
        state = snapshot(conn, "char_darian")
        options = ModelDecisionProvider(conn)._enrich_state(state)["action_options"]

        assert options
        assert all(option["action"] == "move" for option in options)
        assert all(option["action"] != "train" for option in options)

        _set_needs(conn, location=KITCHEN, hunger=13.7, thirst=55.2)
        kitchen_state = snapshot(conn, "char_darian")
        local = ModelDecisionProvider(conn)._enrich_state(kitchen_state)["action_options"]
        assert local == [
            {
                "action": "drink",
                "target": DRINKING_WATER,
                "target_name": "Drinking Water",
                "duration": (1, 30),
                "effects": {"needs.thirst": -55.0},
            }
        ]

        after = apply_action(conn, Action("drink", 5, DRINKING_WATER, "rehydrate before training"), "char_darian")
        assert after["thirst"] < 50.0


def test_eating_stored_food_resolves_strong_hunger_but_does_not_claim_hydration(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=FOOD_STORAGE, hunger=61.3, thirst=49.0)
        before = snapshot(conn, "char_darian")
        after = apply_action(
            conn,
            Action("eat", 20, FOOD_PROVISIONS, "resolve strong hunger with stored provisions"),
            "char_darian",
        )
        assert before["hunger"] == 61.3
        assert after["hunger"] < 55.0
        assert after["hunger"] < before["hunger"]
        assert after["thirst"] > before["thirst"]


def test_strong_hunger_routes_only_toward_nearest_authored_food_resolvers(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=HOME_GYM, hunger=61.3, thirst=49.0)
        state = snapshot(conn, "char_darian")
        options = ModelDecisionProvider(conn)._enrich_state(state)["action_options"]

        assert options
        assert all(option["action"] == "move" for option in options)
        assert {option["target"] for option in options} == {TRAINING_HALL, LIVING_ROOM}
        assert all(option["action"] != "train" for option in options)


def test_unsupported_higher_priority_need_is_not_skipped(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=TRAINING_HALL, hunger=13.7, thirst=55.2, sleepiness=70.0)
        state = snapshot(conn, "char_darian")
        enriched = ModelDecisionProvider(conn)._enrich_state(state)
        assert enriched["decision_signals"]["highest_priority"]["need"] == "sleepiness"
        # Thirst is supported by the causal guard, but must not jump ahead of the
        # higher-priority sleepiness signal until that domain gets its own guard.
        assert any(option["action"] == "train" for option in enriched["action_options"])

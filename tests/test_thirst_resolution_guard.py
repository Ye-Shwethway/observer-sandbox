from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field


FOOD_STORAGE = "loc_thorne_estate_food_storage"
TRAINING_HALL = "loc_thorne_estate_training_hall"
KITCHEN = "loc_thorne_estate_kitchen"
DRINKING_WATER = "obj_thorne_estate_kitchen_drinking_water"


def _set_incident_state(conn, *, location: str, hunger: float = 13.7, thirst: float = 54.9) -> dict:
    set_field(conn, "char_darian", "runtime.location", location)
    set_field(conn, "char_darian", "needs.energy", 75.6)
    set_field(conn, "char_darian", "needs.hunger", hunger)
    set_field(conn, "char_darian", "needs.thirst", thirst)
    set_field(conn, "char_darian", "needs.sleepiness", 13.8)
    set_field(conn, "char_darian", "physiology.cleanliness", 40.5)
    conn.commit()
    return snapshot(conn)


def test_post_meal_strong_thirst_routes_toward_authored_water_before_training(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = _set_incident_state(conn, location=FOOD_STORAGE)
        enriched = ModelDecisionProvider(conn)._enrich_state(state)
        options = enriched["action_options"]

        assert options
        assert {(option["action"], option["target"]) for option in options} == {
            ("move", TRAINING_HALL)
        }
        assert all(option["action"] != "train" for option in options)
        assert enriched["decision_signals"]["highest_priority"]["need"] == "thirst"
        assert enriched["decision_signals"]["highest_priority"]["level"] == "strong"


def test_local_strong_thirst_exposes_only_authored_drinking_water(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = _set_incident_state(conn, location=KITCHEN)
        enriched = ModelDecisionProvider(conn)._enrich_state(state)
        options = enriched["action_options"]

        assert {(option["action"], option["target"]) for option in options} == {
            ("drink", DRINKING_WATER)
        }
        assert options[0]["effects"]["needs.thirst"] == -55.0

        after = apply_action(conn, Action("drink", 5, DRINKING_WATER, "rehydrate before training"))
        assert after["thirst"] < 50.0


def test_critical_hunger_still_outranks_strong_thirst(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = _set_incident_state(conn, location=FOOD_STORAGE, hunger=82.0, thirst=55.0)
        enriched = ModelDecisionProvider(conn)._enrich_state(state)
        options = enriched["action_options"]

        assert enriched["decision_signals"]["highest_priority"]["need"] == "hunger"
        assert enriched["decision_signals"]["highest_priority"]["level"] == "critical"
        assert {(option["action"], option["target"]) for option in options} == {
            ("eat", "obj_thorne_estate_food_storage_provisions")
        }

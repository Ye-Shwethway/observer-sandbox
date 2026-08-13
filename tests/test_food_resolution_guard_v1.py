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
FOYER = "loc_thorne_estate_foyer"
MASTER_BATHROOM = "loc_thorne_estate_master_bathroom"
SUPPLY_SHELVES = "obj_thorne_estate_food_storage_supply_shelves"
FOOD_PROVISIONS = "obj_thorne_estate_food_storage_provisions"
DRINKING_WATER = "obj_thorne_estate_kitchen_drinking_water"
MASTER_SHOWER = "obj_thorne_estate_master_shower"


def _set_needs(conn, *, location: str, hunger: float = 20.0, thirst: float = 15.0, energy: float = 75.0, sleepiness: float = 15.0, cleanliness: float = 80.0) -> None:
    set_field(conn, "char_darian", "runtime.location", location)
    set_field(conn, "char_darian", "needs.hunger", hunger)
    set_field(conn, "char_darian", "needs.thirst", thirst)
    set_field(conn, "char_darian", "needs.energy", energy)
    set_field(conn, "char_darian", "needs.sleepiness", sleepiness)
    set_field(conn, "char_darian", "physiology.cleanliness", cleanliness)
    conn.commit()


def _enriched(conn):
    return ModelDecisionProvider(conn)._enrich_state(snapshot(conn, "char_darian"))


def test_strong_hunger_and_thirst_resolvers_remain_causal(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=FOOD_STORAGE, hunger=61.3, thirst=49.0)
        options = _enriched(conn)["action_options"]
        assert {(o["action"], o["target"]) for o in options} == {("eat", FOOD_PROVISIONS)}
        assert all(o.get("target") != SUPPLY_SHELVES for o in options)

        _set_needs(conn, location=KITCHEN, hunger=20.0, thirst=55.2)
        options = _enriched(conn)["action_options"]
        assert {(o["action"], o["target"]) for o in options} == {("drink", DRINKING_WATER)}


def test_energy_exemplar_uses_increasing_rest_effect_and_blocks_training(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=TRAINING_HALL, energy=35.0)
        before = snapshot(conn, "char_darian")
        enriched = _enriched(conn)
        assert enriched["decision_signals"]["highest_priority"]["need"] == "energy"
        assert {(o["action"], o["target"]) for o in enriched["action_options"]} == {("rest", None)}
        after = apply_action(conn, Action("rest", 60, None, "recover energy"), "char_darian")
        assert after["energy"] > before["energy"]
        assert after["energy"] > 40.0


def test_sleepiness_batch_routes_strong_and_critical_to_real_sleep(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=TRAINING_HALL, sleepiness=70.0)
        strong = _enriched(conn)
        assert strong["decision_signals"]["highest_priority"]["need"] == "sleepiness"
        assert {(o["action"], o["target"]) for o in strong["action_options"]} == {("move", FOYER)}

        _set_needs(conn, location=TRAINING_HALL, sleepiness=85.0)
        critical = _enriched(conn)
        assert critical["decision_signals"]["highest_priority"]["level"] == "critical"
        assert {(o["action"], o["target"]) for o in critical["action_options"]} == {("move", FOYER)}
        assert all(o["action"] != "train" for o in critical["action_options"])


def test_cleanliness_batch_routes_to_shower_and_resolves_locally(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=TRAINING_HALL, cleanliness=40.0)
        routed = _enriched(conn)
        assert routed["decision_signals"]["highest_priority"]["need"] == "cleanliness"
        assert {(o["action"], o["target"]) for o in routed["action_options"]} == {("move", FOYER)}

        _set_needs(conn, location=MASTER_BATHROOM, cleanliness=40.0)
        before = snapshot(conn, "char_darian")
        local = _enriched(conn)
        assert {(o["action"], o["target"]) for o in local["action_options"]} == {("shower", MASTER_SHOWER)}
        after = apply_action(conn, Action("shower", 10, MASTER_SHOWER, "restore cleanliness"), "char_darian")
        assert after["cleanliness"] > before["cleanliness"]
        assert after["cleanliness"] > 50.0


def test_authored_priority_order_controls_full_supported_family(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=TRAINING_HALL, sleepiness=70.0, energy=35.0, thirst=55.0, hunger=60.0, cleanliness=40.0)
        enriched = _enriched(conn)
        attention = enriched["decision_signals"]["needs_attention"]
        assert [x["need"] for x in attention[:5]] == ["sleepiness", "energy", "thirst", "hunger", "cleanliness"]
        assert {(o["action"], o["target"]) for o in enriched["action_options"]} == {("move", FOYER)}


def test_hunger_route_still_uses_nearest_authored_resolver(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_needs(conn, location=HOME_GYM, hunger=61.3, thirst=49.0)
        options = _enriched(conn)["action_options"]
        assert {o["target"] for o in options} == {TRAINING_HALL, LIVING_ROOM}
        assert all(o["action"] == "move" for o in options)

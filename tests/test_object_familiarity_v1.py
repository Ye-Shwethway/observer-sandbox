from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action, snapshot
from observer_sandbox.world import set_field


HOME_GYM = "loc_thorne_estate_home_gym"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"
NOVEL_OBJECT = "obj_test_novel_inspect_only"


def _enriched(conn):
    state = snapshot(conn, "char_darian")
    return ModelDecisionProvider(conn, character_id="char_darian")._enrich_state(state)


def test_functional_training_resource_is_not_offered_for_routine_inspection(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        conn.commit()
        enriched = _enriched(conn)
        assert any(
            option["action"] == "train" and option["target"] == FREE_WEIGHTS
            for option in enriched["action_options"]
        )
        assert not any(
            option["action"] == "inspect" and option["target"] == FREE_WEIGHTS
            for option in enriched["action_options"]
        )
        suppressed = enriched["object_familiarity"]["suppressed"]
        assert any(
            row["target"] == FREE_WEIGHTS and row["basis"] == "established_functional_resource"
            for row in suppressed
        )


def test_unknown_inspect_only_object_is_available_once_then_becomes_familiar(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", HOME_GYM)
        conn.execute(
            "INSERT INTO entities(id,entity_type,name,state_json,capabilities_json) VALUES(?,?,?,?,?)",
            (NOVEL_OBJECT, "object", "Unfamiliar Test Object", "{}", '["inspect"]'),
        )
        conn.execute(
            "INSERT INTO relations(source_id,relation_type,target_id,metadata_json) VALUES(?,?,?,?)",
            (HOME_GYM, "contains", NOVEL_OBJECT, "{}"),
        )
        conn.commit()

        before = _enriched(conn)
        assert any(
            option["action"] == "inspect" and option["target"] == NOVEL_OBJECT
            for option in before["action_options"]
        )

        apply_action(conn, Action("inspect", 3, NOVEL_OBJECT, "identify an unfamiliar object"), "char_darian")
        after = _enriched(conn)
        assert not any(
            option["action"] == "inspect" and option["target"] == NOVEL_OBJECT
            for option in after["action_options"]
        )
        suppressed = after["object_familiarity"]["suppressed"]
        assert any(
            row["target"] == NOVEL_OBJECT and row["basis"] == "prior_interaction"
            for row in suppressed
        )

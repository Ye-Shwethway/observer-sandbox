import json

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action
from observer_sandbox.training_stimulus import FREE_WEIGHTS_TARGET, training_stimulus_evidence
from observer_sandbox.world import set_field


def test_stimulus_evaluator_is_free_weights_strength_only():
    load = {"effective_minutes": 45.0}
    evidence = training_stimulus_evidence(action_name="train", target=FREE_WEIGHTS_TARGET, training_load=load)
    assert evidence == {
        "domain": "strength",
        "target": FREE_WEIGHTS_TARGET,
        "effective_minutes": 45.0,
        "stimulus_units": 0.75,
        "unit": "session_strength_stimulus",
        "source": "minimum-training-stimulus-v1",
    }
    assert training_stimulus_evidence(action_name="train", target="obj_thorne_estate_gym_heavy_bag", training_load=load) is None
    assert training_stimulus_evidence(action_name="rest", target=FREE_WEIGHTS_TARGET, training_load=load) is None


def test_free_weights_completion_persists_stimulus_without_progression(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", "loc_thorne_estate_home_gym")
        raw_before = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()[0]

        action_id = "stimulus-proof-action"
        apply_action(conn, Action("train", 60, FREE_WEIGHTS_TARGET, "stimulus proof"), action_id=action_id)

        row = conn.execute("SELECT outcome_json FROM action_instances WHERE id=?", (action_id,)).fetchone()
        outcome = json.loads(row[0])
        assert outcome["training_load"]["effective_minutes"] == 60.0
        assert outcome["training_stimulus"] == {
            "domain": "strength",
            "target": FREE_WEIGHTS_TARGET,
            "effective_minutes": 60.0,
            "stimulus_units": 1.0,
            "unit": "session_strength_stimulus",
            "source": "minimum-training-stimulus-v1",
        }

        event = conn.execute(
            "SELECT payload_json FROM events WHERE action_id=? AND event_type='action_completed' ORDER BY id DESC LIMIT 1",
            (action_id,),
        ).fetchone()
        payload = json.loads(event[0])
        assert payload["training_stimulus"] == outcome["training_stimulus"]

        raw_after = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()[0]
        assert raw_after == raw_before == "90"


def test_non_free_weights_training_has_no_strength_stimulus(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", "loc_thorne_estate_home_gym")
        action_id = "heavy-bag-no-strength-stimulus"
        apply_action(conn, Action("train", 30, "obj_thorne_estate_gym_heavy_bag", "negative proof"), action_id=action_id)
        outcome = json.loads(conn.execute("SELECT outcome_json FROM action_instances WHERE id=?", (action_id,)).fetchone()[0])
        assert "training_load" in outcome
        assert "training_stimulus" not in outcome

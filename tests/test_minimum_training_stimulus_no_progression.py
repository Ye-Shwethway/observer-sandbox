from observer_sandbox.db import connect
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import Action, apply_action
from observer_sandbox.training_stimulus import FREE_WEIGHTS_TARGET
from observer_sandbox.world import set_field


def test_training_stimulus_does_not_change_strength_or_grade(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", "loc_thorne_estate_home_gym")
        before = profile_section(conn, "char_darian", "attributes")
        before_strength = next(item for item in before["content"] if item["field_key"] == "raps_pa.strength")

        apply_action(conn, Action("train", 60, FREE_WEIGHTS_TARGET, "no progression guard"), action_id="stimulus-no-progression")

        after = profile_section(conn, "char_darian", "attributes")
        after_strength = next(item for item in after["content"] if item["field_key"] == "raps_pa.strength")
        assert before_strength["value"] == after_strength["value"] == 90
        assert before_strength["grade"] == after_strength["grade"]

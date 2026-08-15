from __future__ import annotations

import pytest

from observer_sandbox.training_methods import validate_training_movements_for_target


COMBAT_PIT = "obj_thorne_estate_training_combat_pit"
AI_COMBAT_SIM = "obj_thorne_estate_training_ai_combat_sim"
FREE_WEIGHTS = "obj_thorne_estate_gym_free_weights"


def test_method_without_movement_subcatalog_canonicalizes_auxiliary_labels() -> None:
    assert validate_training_movements_for_target(COMBAT_PIT, ["sparring"]) == ()
    assert validate_training_movements_for_target(
        AI_COMBAT_SIM,
        ["defensive_repositioning"],
    ) == ()


def test_explicit_movement_contract_still_accepts_only_catalog_ids() -> None:
    assert validate_training_movements_for_target(
        FREE_WEIGHTS,
        ["horizontal_press", "row"],
    ) == ("horizontal_press", "row")

    with pytest.raises(ValueError, match="not allowed for the selected method"):
        validate_training_movements_for_target(FREE_WEIGHTS, ["sparring"])


def test_missing_or_unbound_target_remains_fail_closed() -> None:
    with pytest.raises(ValueError, match="not allowed for the selected method"):
        validate_training_movements_for_target(None, ["invented_label"])
    with pytest.raises(ValueError, match="not allowed for the selected method"):
        validate_training_movements_for_target("obj_unknown", ["invented_label"])

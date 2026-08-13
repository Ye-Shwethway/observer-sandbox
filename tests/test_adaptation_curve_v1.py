import math

import pytest

from observer_sandbox.adaptation_curve import strength_level_factor
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def test_strength_level_curve_slows_sharply_near_ceiling():
    expected = {
        20: 0.64,
        40: 0.36,
        60: 0.16,
        75: 0.0625,
        90: 0.01,
        95: 0.0025,
        99: 0.0001,
        100: 0.0,
    }
    factors = []
    for value, factor in expected.items():
        evidence = strength_level_factor(value)
        assert evidence.level_factor == pytest.approx(factor, abs=1e-9)
        factors.append(evidence.level_factor)
    assert factors == sorted(factors, reverse=True)


def test_effective_ceiling_modifier_changes_headroom_without_changing_raw_value():
    natural = strength_level_factor(90)
    raised = strength_level_factor(90, ceiling_multiplier=1.05)

    assert natural.effective_ceiling == 100.0
    assert raised.effective_ceiling == 105.0
    assert natural.level_factor == pytest.approx(0.01)
    assert raised.level_factor == pytest.approx((15.0 / 105.0) ** 2)
    assert raised.level_factor > natural.level_factor
    assert raised.current_value == natural.current_value == 90.0


def test_at_or_above_effective_ceiling_has_zero_ordinary_headroom():
    assert strength_level_factor(100).level_factor == 0.0
    assert strength_level_factor(105, natural_ceiling=100, ceiling_multiplier=1.05).level_factor == 0.0
    assert strength_level_factor(110, natural_ceiling=100, ceiling_multiplier=1.05).level_factor == 0.0


def test_curve_rejects_invalid_parameters():
    with pytest.raises(ValueError):
        strength_level_factor(-1)
    with pytest.raises(ValueError):
        strength_level_factor(50, natural_ceiling=0)
    with pytest.raises(ValueError):
        strength_level_factor(50, ceiling_multiplier=0)
    with pytest.raises(ValueError):
        strength_level_factor(50, exponent=0)


def test_curve_evaluation_does_not_mutate_strength_profile(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = conn.execute(
            "SELECT value_json,mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        assert before["value_json"] == "90"

        evidence = strength_level_factor(float(before["value_json"]))
        assert evidence.level_factor == pytest.approx(0.01)

        after = conn.execute(
            "SELECT value_json,mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        assert dict(after) == dict(before)

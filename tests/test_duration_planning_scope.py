from observer_sandbox.duration_planning import GENERIC_PROFILES, TARGET_PROFILES


def test_v1_scope_stays_bounded():
    assert "sleep" not in GENERIC_PROFILES
    assert "research" in GENERIC_PROFILES
    assert "monitor" in GENERIC_PROFILES
    assert "self_satisfaction" in GENERIC_PROFILES
    assert len(GENERIC_PROFILES) == 13
    assert len(TARGET_PROFILES) == 5
    assert all(action != "train" for action, _target in TARGET_PROFILES)

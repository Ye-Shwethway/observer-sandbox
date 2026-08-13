from observer_sandbox.duration_planning import GENERIC_PROFILES, TARGET_PROFILES


def test_v1_scope_stays_bounded():
    assert "sleep" not in GENERIC_PROFILES
    assert "research" in GENERIC_PROFILES
    assert len(GENERIC_PROFILES) == 11
    assert len(TARGET_PROFILES) == 9

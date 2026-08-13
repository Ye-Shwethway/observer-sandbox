from observer_sandbox.stamina_progression import STIMULUS_MINUTES_PER_UNIT, _stimulus_from_payload


def payload(method_id, channels, minutes=36.0):
    return {"training_method": {"method_id": method_id, "source": "training-method-semantics-v1", "workload_channels": channels, "effective_load": {"effective_minutes": minutes}}}


def test_pure_conditioning_methods_share_one_conversion():
    for method_id in ("steady_state_cardio", "rowing_conditioning", "altitude_conditioning"):
        units, minutes = _stimulus_from_payload(payload(method_id, ["conditioning"]))
        assert minutes == 36.0
        assert units == round(36.0 / STIMULUS_MINUTES_PER_UNIT, 6)


def test_mixed_conditioning_method_is_not_stamina_equivalent():
    assert _stimulus_from_payload(payload("speed_agility_drills", ["conditioning", "movement"])) is None

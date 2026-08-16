from observer_sandbox.resource_awareness import enrich_options_with_usage


def _usage(*, uses=1, distance=0, after=None):
    return {
        "recent_uses": uses,
        "last_used_sim_time": "2025-05-10T09:00:00+00:00",
        "recently_repeated": uses >= 2,
        "event_distance": distance,
        "last_before": {},
        "last_after": after or {},
    }


def test_recent_shower_with_negligible_cleanliness_benefit_is_suppressed():
    options = [
        {
            "action": "shower",
            "target": "obj_shower",
            "effects": {"physiology.cleanliness": {"set": 100}},
            "duration": (5, 60),
        },
        {"action": "idle", "target": None, "duration": (1, 120)},
    ]
    usage = {
        ("shower", "obj_shower"): _usage(after={"cleanliness": 98.5}),
    }

    shaped = enrich_options_with_usage(options, usage)

    assert ("shower", "obj_shower") not in {
        (row["action"], row.get("target")) for row in shaped
    }
    assert any(row["action"] == "idle" for row in shaped)


def test_recent_shower_remains_available_when_it_still_has_meaningful_benefit():
    options = [
        {
            "action": "shower",
            "target": "obj_shower",
            "effects": {"physiology.cleanliness": {"set": 100}},
            "duration": (5, 60),
        },
        {"action": "idle", "target": None, "duration": (1, 120)},
    ]
    usage = {
        ("shower", "obj_shower"): _usage(after={"cleanliness": 70.0}),
    }

    shaped = enrich_options_with_usage(options, usage)

    assert any(row["action"] == "shower" for row in shaped)


def test_repeated_move_target_is_suppressed_when_other_choices_exist():
    options = [
        {"action": "move", "target": "loc_desk", "duration": (1, 30)},
        {"action": "read", "target": "obj_book", "duration": (5, 240)},
        {"action": "idle", "target": None, "duration": (1, 120)},
    ]
    usage = {
        ("move", "loc_desk"): _usage(uses=2, distance=2),
    }

    shaped = enrich_options_with_usage(options, usage)

    assert ("move", "loc_desk") not in {
        (row["action"], row.get("target")) for row in shaped
    }
    assert {row["action"] for row in shaped} == {"read", "idle"}


def test_choice_shaping_never_erases_the_only_legal_option():
    options = [
        {
            "action": "shower",
            "target": "obj_shower",
            "effects": {"physiology.cleanliness": {"set": 100}},
            "duration": (5, 60),
        }
    ]
    usage = {
        ("shower", "obj_shower"): _usage(after={"cleanliness": 99.0}),
    }

    shaped = enrich_options_with_usage(options, usage)

    assert len(shaped) == 1
    assert shaped[0]["action"] == "shower"

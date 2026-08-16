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


def test_repeated_move_target_remains_available_when_other_choices_exist():
    options = [
        {"action": "move", "target": "loc_desk", "duration": (1, 30)},
        {"action": "read", "target": "obj_book", "duration": (5, 240)},
        {"action": "idle", "target": None, "duration": (1, 120)},
    ]
    usage = {
        ("move", "loc_desk"): _usage(uses=2, distance=2),
    }

    shaped = enrich_options_with_usage(options, usage)

    move = next(
        row for row in shaped
        if row["action"] == "move" and row.get("target") == "loc_desk"
    )
    assert move["recent_usage"]["recent_uses"] == 2
    assert move["recent_usage"]["recently_repeated"] is True
    assert {row["action"] for row in shaped} == {"move", "read", "idle"}


def test_all_legal_move_targets_survive_repetition_shaping():
    options = [
        {"action": "move", "target": "loc_foyer", "duration": (1, 30)},
        {"action": "move", "target": "loc_exterior", "duration": (1, 30)},
        {"action": "move", "target": "loc_grounds", "duration": (1, 30)},
        {"action": "idle", "target": None, "duration": (1, 120)},
    ]
    usage = {
        ("move", "loc_foyer"): _usage(uses=7, distance=0),
        ("move", "loc_exterior"): _usage(uses=5, distance=1),
        ("move", "loc_grounds"): _usage(uses=3, distance=2),
    }

    shaped = enrich_options_with_usage(options, usage)

    assert {
        row.get("target") for row in shaped if row["action"] == "move"
    } == {"loc_foyer", "loc_exterior", "loc_grounds"}


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

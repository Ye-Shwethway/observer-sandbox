from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.resource_awareness import reachable_location_awareness
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import action_options, snapshot


ACTOR = "char_darian"


def test_reachable_resource_previews_expose_no_actionable_ids(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        state = snapshot(conn, ACTOR)
        previews = reachable_location_awareness(conn, state["location"])

        assert previews
        for preview in previews:
            assert preview["planning_only"] is True
            assert "location" not in preview
            assert "location_name" in preview
            assert "exact target ID appears in current action_options" in preview["instruction"]
            for resource in preview["resources"]:
                assert resource["planning_only"] is True
                assert "id" not in resource
                assert "name" in resource


def test_action_options_remain_the_only_surface_with_exact_move_target_ids(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        raw_options = action_options(conn, ACTOR)
        move_targets = {
            item["target"]
            for item in raw_options
            if item.get("action") == "move" and isinstance(item.get("target"), str)
        }
        assert move_targets

        enriched = ModelDecisionProvider(conn, character_id=ACTOR)._enrich_state(snapshot(conn, ACTOR))
        awareness_text = repr(enriched["resource_awareness"]["reachable_locations"])
        for target in move_targets:
            assert target not in awareness_text

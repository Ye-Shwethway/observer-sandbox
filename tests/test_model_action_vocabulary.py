from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import ACTION_NAMES, snapshot
from observer_sandbox.world import set_field

LIBRARY = "loc_thorne_estate_library"
RESEARCH_DESK = "obj_thorne_estate_library_research_desk"


def test_model_vocabulary_includes_semantic_actions_from_current_options(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_field(conn, "char_darian", "runtime.location", LIBRARY)
        conn.commit()
        captured = {}

        def fake_generate(conn, *, character_id, role, state, available_actions):
            captured["available_actions"] = available_actions
            assert any(
                option["action"] == "research" and option["target"] == RESEARCH_DESK
                for option in state["action_options"]
            )
            return {
                "action": "research",
                "duration_minutes": 45,
                "target": RESEARCH_DESK,
                "reason": "review estate records",
            }

        monkeypatch.setattr("observer_sandbox.model_decision.generate_character_decision", fake_generate)
        action = ModelDecisionProvider(conn).choose(snapshot(conn), ACTION_NAMES)
        assert "research" in captured["available_actions"]
        assert action.name == "research"
        assert action.target == RESEARCH_DESK

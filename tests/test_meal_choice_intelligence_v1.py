import json

from observer_sandbox.db import connect
from observer_sandbox.meal_choice_intelligence import meal_choice_context
from observer_sandbox.model_decision import ModelDecisionProvider
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot


def _insert_completed(conn, sim_time: str, payload: dict):
    conn.execute(
        "INSERT INTO events(sim_time,actor_id,event_type,payload_json) VALUES(?,?,?,?)",
        (sim_time, "char_darian", "action_completed", json.dumps(payload)),
    )


def test_context_aggregates_today_last_meal_and_recent_training(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _insert_completed(
            conn,
            "2025-05-05T08:00:00+00:00",
            {
                "action": "eat",
                "duration_minutes": 20,
                "action_started_sim_time": "2025-05-05T07:40:00+00:00",
                "action_ended_sim_time": "2025-05-05T08:00:00+00:00",
                "nutrition_intake": {
                    "energy_kcal": 500.0,
                    "protein_g": 40.0,
                    "carbohydrate_g": 55.0,
                    "fat_g": 15.0,
                    "source": "eating-behavior-v1",
                },
                "energy_expenditure": {"estimated_kcal": 30.0},
            },
        )
        _insert_completed(
            conn,
            "2025-05-05T09:30:00+00:00",
            {
                "action": "train",
                "duration_minutes": 60,
                "action_started_sim_time": "2025-05-05T08:30:00+00:00",
                "action_ended_sim_time": "2025-05-05T09:30:00+00:00",
                "energy_expenditure": {"estimated_kcal": 500.0},
            },
        )
        conn.commit()

        state = {
            "sim_time": "2025-05-05T12:00:00+00:00",
            "hunger": 60.0,
            "energy": 75.0,
            "fatigue": 20.0,
            "sleepiness": 10.0,
            "thirst": 15.0,
        }
        policy = {
            "nutrition_policy": {
                "goal": "fixture nutrition goal",
                "energy_intent": "maintenance",
                "protein_priority": "high after training",
                "dietary_constraints": ["example constraint"],
                "guidance": "choose contextually",
            }
        }
        context = meal_choice_context(conn, "char_darian", state=state, autonomy_policy=policy)

    assert context["today"]["intake_kcal"] == 500.0
    assert context["today"]["protein_g"] == 40.0
    assert context["today"]["meal_count"] == 1
    assert context["last_meal"]["minutes_ago"] == 240.0
    assert context["last_meal"]["energy_kcal"] == 500.0
    assert context["recent_training"]["completed_sessions"] == 1
    assert context["recent_training"]["completed_minutes"] == 60.0
    assert context["recent_training"]["minutes_since_last_training"] == 150.0
    assert context["character_nutrition_policy"]["goal"] == "fixture nutrition goal"
    assert context["resting_energy_reference"]["ree_kcal_day"] > 0.0
    assert "not a daily calorie target" in context["resting_energy_reference"]["note"]


def test_context_is_read_only_and_is_included_in_existing_cognition_state(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        state = snapshot(conn, "char_darian")
        before_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        provider = ModelDecisionProvider(conn, character_id="char_darian")
        enriched = provider._enrich_state(state)
        after_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

    assert before_events == after_events
    context = enriched["meal_choice_context"]
    assert context["source"] == "meal-choice-intelligence-v1"
    assert context["today"]["meal_count"] >= 0
    assert context["last_meal"] is None
    assert context["character_nutrition_policy"]["goal"].startswith("Support represented physiological needs")
    assert "character-specific diet objective" in context["character_nutrition_policy"]["goal"]
    assert context["character_nutrition_policy"]["dietary_constraints"] == []

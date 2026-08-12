from __future__ import annotations

import json

from observer_sandbox.ai import configure_provider, set_binding
from observer_sandbox.ai_runtime import generate_character_decision
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def test_nanogpt_model_decision_uses_resolved_binding_without_mutating_world(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    monkeypatch.setenv("OBSERVER_NANOGPT_API_KEY", "test-key")

    with connect(db) as conn:
        configure_provider(conn, "nanogpt", enabled=True)
        conn.execute(
            """
            INSERT INTO ai_models(provider_id, model_id, display_name, capabilities_json, metadata_json, active)
            VALUES ('nanogpt', 'fixture/model', 'Fixture Model', '{}', '{}', 1)
            """
        )
        conn.commit()
        set_binding(
            conn,
            scope_type="character",
            scope_id="char_darian",
            role="cognition",
            provider_id="nanogpt",
            model_id="fixture/model",
        )

        before_events = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

        def fake_post(url, *, headers, payload, timeout=45.0):
            assert url.endswith("/subscription/v1/chat/completions")
            assert payload["model"] == "fixture/model"
            assert payload["response_format"]["type"] == "json_schema"
            return {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "action": "move",
                                    "duration_minutes": 5,
                                    "target": "room_living",
                                    "reason": "start the day",
                                }
                            )
                        }
                    }
                ]
            }

        monkeypatch.setattr("observer_sandbox.ai_runtime._post_json", fake_post)
        decision = generate_character_decision(
            conn,
            character_id="char_darian",
            role="cognition",
            state={"location": "room_bedroom", "reachable_rooms": [{"id": "room_living"}]},
            available_actions=["move", "idle"],
        )

        assert decision["action"] == "move"
        assert decision["target"] == "room_living"
        assert conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == before_events

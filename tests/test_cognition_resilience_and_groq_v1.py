from __future__ import annotations

import json

from observer_sandbox.ai import configure_provider, list_providers, set_binding
from observer_sandbox.ai_runtime import generate_character_decision
from observer_sandbox.db import connect
from observer_sandbox.duration_planning import enrich_action_options
from observer_sandbox.runtime import initialize


TRAIN_TARGET = "fixture_train_target"


def test_groq_is_seeded_as_openai_compatible_provider(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        providers = {item["id"]: item for item in list_providers(conn)}
    assert providers["groq"]["adapter_type"] == "openai_compatible"
    assert providers["groq"]["base_url"] == "https://api.groq.com/openai/v1"
    assert providers["groq"]["credential_ref"] == "OBSERVER_GROQ_API_KEY"


def test_runtime_shaped_duration_overrides_ordinary_training_preference():
    option = {"action": "train", "target": TRAIN_TARGET, "duration": (10, 20)}
    enriched = enrich_action_options([option])[0]
    assert enriched["preferred_duration"] == (10, 20)


def test_openai_compatible_decision_clamps_to_authoritative_option_duration(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_GROQ_API_KEY", "test-key")

    with connect(db) as conn:
        configure_provider(conn, "groq", enabled=True)
        conn.execute(
            """
            INSERT INTO ai_models(provider_id, model_id, display_name, capabilities_json, metadata_json, active)
            VALUES ('groq', 'openai/gpt-oss-20b', 'GPT OSS 20B', '{}', '{}', 1)
            """
        )
        conn.commit()
        set_binding(
            conn,
            scope_type="character",
            scope_id="char_darian",
            role="cognition",
            provider_id="groq",
            model_id="openai/gpt-oss-20b",
        )

        def fake_post(url, *, headers, payload, timeout=45.0):
            assert url == "https://api.groq.com/openai/v1/chat/completions"
            assert headers["Authorization"] == "Bearer test-key"
            assert payload["response_format"]["type"] == "json_schema"
            return {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "action": "train",
                                    "duration_minutes": 30,
                                    "target": TRAIN_TARGET,
                                    "reason": "continue with a bounded training block",
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
            state={
                "location": "loc_thorne_estate_home_gym",
                "action_options": [
                    {"action": "train", "target": TRAIN_TARGET, "duration": (10, 20)}
                ],
            },
            available_actions=["train"],
        )

    assert decision["duration_minutes"] == 20
    assert decision["target"] == TRAIN_TARGET

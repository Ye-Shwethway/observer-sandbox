from __future__ import annotations

import io
import json
import urllib.error

import pytest

from observer_sandbox import ai, ai_runtime
from observer_sandbox.ai import configure_provider, list_providers, set_binding
from observer_sandbox.ai_runtime import AIDecisionError, _compact_prompt_state, generate_character_decision
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


def test_groq_catalog_uses_standard_openai_compatible_headers(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_GROQ_API_KEY", "test-key")
    captured = {}

    def fake_get_json(url, headers=None, timeout=20.0):
        captured["url"] = url
        captured["headers"] = headers
        return {"data": []}

    monkeypatch.setattr(ai, "_get_json", fake_get_json)
    with connect(db) as conn:
        configure_provider(conn, "groq", enabled=True)
        provider = conn.execute("SELECT * FROM ai_providers WHERE id='groq'").fetchone()
        ai._fetch_openai_compatible(provider)

    assert captured["url"] == "https://api.groq.com/openai/v1/models"
    assert captured["headers"]["Authorization"] == "Bearer test-key"
    assert captured["headers"]["Content-Type"] == "application/json"
    assert captured["headers"]["Accept"] == "application/json"
    assert captured["headers"]["User-Agent"].startswith("observer-sandbox/")


def test_live_ai_http_error_preserves_bounded_provider_detail(monkeypatch):
    error = urllib.error.HTTPError(
        "https://api.groq.com/openai/v1/chat/completions",
        400,
        "Bad Request",
        hdrs=None,
        fp=io.BytesIO(b'{"error":{"message":"fixture provider detail"}}'),
    )

    def fake_urlopen(request, timeout=45.0):
        assert request.get_header("User-agent").startswith("observer-sandbox/")
        raise error

    monkeypatch.setattr(ai_runtime.urllib.request, "urlopen", fake_urlopen)
    with pytest.raises(AIDecisionError, match="fixture provider detail"):
        ai_runtime._post_json(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer test-key"},
            payload={"model": "fixture"},
        )


def test_prompt_compaction_removes_derived_duplicates_but_keeps_authority():
    state = {
        "autonomy_policy": {
            "policy_revision": "fixture-v1",
            "decision_principles": ["choose purposefully"],
            "reason_style": "short",
            "need_priorities": {"strong": {"fatigue_gte": 55}},
            "routine_windows": [{"name": "evening"}],
        },
        "training_load_guard": {"source": "training-session-load-recovery-guard-v1", "allowed": True},
        "object_familiarity": {
            "source": "object-familiarity-inspect-utility-v1",
            "suppressed_inspect_count": 2,
            "suppressed": [{"target": "a"}, {"target": "b"}],
            "guidance": "familiar resources are already filtered",
        },
        "action_options": [
            {
                "action": "train",
                "target": TRAIN_TARGET,
                "duration": (10, 20),
                "training_load_guard": {"source": "training-session-load-recovery-guard-v1", "allowed": True},
            }
        ],
    }

    compact = _compact_prompt_state(state)

    assert compact["autonomy_policy"] == {
        "policy_revision": "fixture-v1",
        "decision_principles": ["choose purposefully"],
        "reason_style": "short",
    }
    assert compact["training_load_guard"]["source"] == "training-session-load-recovery-guard-v1"
    assert "training_load_guard" not in compact["action_options"][0]
    assert compact["action_options"][0]["duration"] == (10, 20)
    assert compact["action_options"][0]["preferred_duration"] == (10, 20)
    assert "suppressed" not in compact["object_familiarity"]
    assert compact["object_familiarity"]["suppressed_inspect_count"] == 2


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

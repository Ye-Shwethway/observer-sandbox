from __future__ import annotations

from copy import deepcopy

import observer_sandbox.creator_studio_item_batch as batch_studio
from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.creator_studio_item_batch import ai_item_batch_draft
from observer_sandbox.db import connect
from observer_sandbox.item_metrics import DEFAULT_ITEM_METRIC_REGISTRY
from observer_sandbox.runtime import initialize


def test_batch_ai_uses_creator_creation_binding_and_full_item_schema(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    payload = manual_item_template()
    payload["definition"]["key"] = "bound_item"
    captured = {}

    monkeypatch.setattr(
        batch_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "creator-provider", "model_id": "creator-model", "parameters": {"temperature": 0.2}},
    )

    def fake_generate(conn, **kwargs):
        captured.update(kwargs)
        return {"items": [{"ref": "item", "payload": deepcopy(payload)}]}

    monkeypatch.setattr(batch_studio, "generate_structured", fake_generate)

    creator_intent = "Create five useful camping items"
    with connect(db) as conn:
        draft = ai_item_batch_draft(conn, 44, creator_intent)

    assert draft["draft_mode"] == "ai_generated"
    assert draft["prompt_text"] == creator_intent
    assert captured["provider_id"] == "creator-provider"
    assert captured["model_id"] == "creator-model"
    assert captured["parameters"] == {"temperature": 0.2}
    assert captured["schema_name"] == "observer_creator_studio_item_batch_v1"

    schema = captured["schema"]
    payload_schema = schema["properties"]["items"]["items"]["properties"]["payload"]
    assert payload_schema["required"] == [
        "schema_version", "definition", "instance", "economic_policy", "requirements", "relationships"
    ]
    definition = payload_schema["properties"]["definition"]
    assert definition["required"] == [
        "key", "name", "kind", "description", "stackable", "mobility", "capabilities", "tags", "modules"
    ]
    modules = definition["properties"]["modules"]
    assert modules["required"] == ["physical", "stack", "nutrition", "container", "resistance_training", "metrics"]
    assert modules["additionalProperties"] is False
    metrics = modules["properties"]["metrics"]["anyOf"][0]
    assert set(metrics["properties"]) == set(DEFAULT_ITEM_METRIC_REGISTRY.metric_ids())
    assert metrics["additionalProperties"] is False

    # The Creator supplies only natural intent; technical shaping belongs to the system prompt/contracts.
    assert f"Creator intent: {creator_intent}" in captured["prompt"]
    assert "Use stable unique lowercase refs" in captured["prompt"]
    assert "definition.modules.metrics" in captured["prompt"]
    assert "Leave unknown or inapplicable slots null" in captured["prompt"]
    assert "Do not duplicate container capacity or resistance load into metrics" in captured["prompt"]
    assert "STACK INVARIANT" in captured["prompt"]
    assert "Never populate modules.stack for a non-stackable Item" in captured["prompt"]
    assert "For requested batch-local storage, use stored_in='$ref'" in captured["prompt"]
    assert "Do not author derived grades, grading thresholds, evaluator ids or reference profiles" in captured["prompt"]
    assert "Module exact shapes" not in captured["prompt"]

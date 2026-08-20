from __future__ import annotations

from copy import deepcopy

import observer_sandbox.creator_studio_item as item_studio
from observer_sandbox.creator_studio_item import ai_item_draft, manual_item_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def test_single_item_ai_prompt_carries_shared_first_attempt_authoring_contract(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    payload = manual_item_template()
    captured = {}

    monkeypatch.setattr(
        item_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "creator-provider", "model_id": "creator-model", "parameters": {}},
    )

    def fake_generate(conn, **kwargs):
        captured.update(kwargs)
        return deepcopy(payload)

    monkeypatch.setattr(item_studio, "generate_structured", fake_generate)

    creator_intent = "Create a useful camping flashlight"
    with connect(db) as conn:
        draft = ai_item_draft(conn, 88, creator_intent)

    assert draft["prompt_text"] == creator_intent
    prompt = captured["prompt"]
    assert f"Creator intent: {creator_intent}" in prompt
    assert "produce a validator-ready proposal on the first attempt" in prompt
    assert "schema as available structure, not a checklist of facts to invent" in prompt
    assert "do not fill every available metric slot" in prompt
    assert "water-resistant" in prompt and "do not justify a depth value" in prompt
    assert "power, runtime and energy_capacity must be mutually plausible" in prompt
    assert "nutrition requires a genuinely stackable consumable" in prompt
    assert "container requires capability 'store'" in prompt
    assert "resistance_training requires capability 'train'" in prompt
    assert "Prefer fewer defensible facts over many speculative ones" in prompt
    assert "Do not author derived grades" in prompt

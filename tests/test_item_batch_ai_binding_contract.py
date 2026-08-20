from __future__ import annotations

from copy import deepcopy

import observer_sandbox.creator_studio_item_batch as batch_studio
from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.creator_studio_item_batch import ai_item_batch_draft
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


def test_batch_ai_uses_creator_creation_binding_and_structured_schema(tmp_path, monkeypatch):
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

    with connect(db) as conn:
        draft = ai_item_batch_draft(conn, 44, "Create one bound Item")

    assert draft["draft_mode"] == "ai_generated"
    assert captured["provider_id"] == "creator-provider"
    assert captured["model_id"] == "creator-model"
    assert captured["parameters"] == {"temperature": 0.2}
    assert captured["schema_name"] == "observer_creator_studio_item_batch_v1"
    assert captured["schema"]["required"] == ["items"]
    assert "container={'capacity_volume'" in captured["prompt"]

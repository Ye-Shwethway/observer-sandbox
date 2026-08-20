from __future__ import annotations

from copy import deepcopy

import pytest

import observer_sandbox.creator_studio_item as single_studio
import observer_sandbox.creator_studio_item_batch as batch_studio
from observer_sandbox.creator_studio import CreatorStudioError
from observer_sandbox.creator_studio_item import ai_item_draft, manual_item_template
from observer_sandbox.creator_studio_item_batch import ai_item_batch_draft
from observer_sandbox.db import connect
from observer_sandbox.item_creation_realism import ItemRealismError, validate_item_default_realism
from observer_sandbox.runtime import initialize


def _container(*, key: str = "pack", capacity_l: float = 40, length_cm: float = 50, width_cm: float = 30, height_cm: float = 20):
    value = manual_item_template()
    value["definition"].update({
        "key": key,
        "name": "Camping Backpack",
        "kind": "container",
        "capabilities": ["inspect", "store", "wear"],
        "modules": {
            "physical": {
                "mass": {"value": 1.2, "unit": "kg"},
                "length": {"value": length_cm, "unit": "cm"},
                "width": {"value": width_cm, "unit": "cm"},
                "height": {"value": height_cm, "unit": "cm"},
            },
            "container": {"capacity_volume": {"value": capacity_l, "unit": "l"}},
        },
    })
    return value


def test_default_realism_rejects_container_capacity_larger_than_outer_volume():
    with pytest.raises(ItemRealismError, match="outer bounding volume"):
        validate_item_default_realism(_container())


def test_default_realism_accepts_plausible_container_capacity():
    validate_item_default_realism(_container(capacity_l=25))


def test_default_realism_skips_cross_field_check_when_dimensions_are_unknown():
    value = _container()
    value["definition"]["modules"]["physical"]["width"] = None
    validate_item_default_realism(value)


def test_single_ai_uses_shared_realism_instruction_and_rejects_impossible_candidate(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    seen = {}
    monkeypatch.setattr(single_studio, "creator_creation_binding", lambda conn: {"provider_id": "fake", "model_id": "fake", "parameters": {}})

    def generate(*args, **kwargs):
        seen["prompt"] = kwargs["prompt"]
        return deepcopy(_container())

    monkeypatch.setattr(single_studio, "generate_structured", generate)
    with connect(db) as conn:
        with pytest.raises(CreatorStudioError, match="physically inconsistent"):
            ai_item_draft(conn, 1, "Create a 40 L camping backpack")
    assert "REALISM INVARIANT" in seen["prompt"]
    assert "outer bounding volume" in seen["prompt"]
    assert "use null" in seen["prompt"].lower()


def test_batch_ai_uses_same_realism_instruction_and_rejects_impossible_member(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    seen = {}
    monkeypatch.setattr(batch_studio, "creator_creation_binding", lambda conn: {"provider_id": "fake", "model_id": "fake", "parameters": {}})

    def generate(*args, **kwargs):
        seen["prompt"] = kwargs["prompt"]
        return {"items": [{"ref": "backpack", "payload": deepcopy(_container(key="backpack"))}]}

    monkeypatch.setattr(batch_studio, "generate_structured", generate)
    with connect(db) as conn:
        with pytest.raises(CreatorStudioError, match="physically inconsistent"):
            ai_item_batch_draft(conn, 2, "Create a 40 L camping backpack")
    assert "REALISM INVARIANT" in seen["prompt"]
    assert "outer bounding volume" in seen["prompt"]


def test_single_and_batch_share_exact_realism_instruction():
    assert single_studio.DEFAULT_ITEM_REALISM_INSTRUCTION is batch_studio.DEFAULT_ITEM_REALISM_INSTRUCTION

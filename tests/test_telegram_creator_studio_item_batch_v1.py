from __future__ import annotations

from copy import deepcopy

import observer_sandbox.creator_studio_item_batch as batch_studio
from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_studio import active_draft
from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.creator_studio_item_batch import ai_item_batch_draft, approve_item_batch_draft
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_studio import draft_preview_view, studio_callback_view
from observer_sandbox.telegram_world_layers import sandbox_list_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if button.get("callback_data")
    }


def _container_payload():
    value = manual_item_template()
    value["definition"]["key"] = "batch_storage_bin"
    value["definition"]["name"] = "Storage Bin"
    value["definition"]["kind"] = "container"
    value["definition"]["capabilities"] = ["inspect", "store"]
    value["definition"]["modules"] = {
        "container": {"capacity_volume": {"value": 10, "unit": "L"}}
    }
    return value


def _stack_payload():
    value = manual_item_template()
    value["definition"]["key"] = "batch_energy_bar"
    value["definition"]["name"] = "Energy Bar"
    value["definition"]["kind"] = "consumable"
    value["definition"]["stackable"] = True
    value["definition"]["capabilities"] = ["inspect", "eat"]
    value["definition"]["modules"] = {
        "stack": {"canonical_unit": "piece", "initial_quantity": 6},
        "nutrition": {
            "basis_quantity": 1,
            "unit": "piece",
            "energy_kcal": 200,
            "protein_g": 10,
            "carbohydrate_g": 25,
            "fat_g": 7,
        },
    }
    value["instance"] = {"mode": "stack", "quantity": 6, "unit": "piece"}
    value["economic_policy"] = {
        "classification": "consumable_stock",
        "currency_code": "USD",
        "market_value_minor": None,
        "replacement_value_minor": None,
        "unit_value_minor": 250,
        "unit_quantity": 1,
        "unit_label": "piece",
        "net_worth_treatment": "derived_stock",
        "included_in_parent_ref": None,
        "valuation_method": "creator_explicit",
    }
    value["relationships"]["stored_in"] = "$bin"
    return value


def _batch_candidate():
    bottle = manual_item_template()
    bottle["definition"]["key"] = "batch_water_bottle"
    return {
        "items": [
            {"ref": "bottle", "payload": bottle},
            {"ref": "bars", "payload": _stack_payload()},
            {"ref": "bin", "payload": _container_payload()},
        ]
    }


def test_item_method_menu_exposes_batch_ai_and_exact_json(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        text, keyboard = studio_callback_view(conn, 1, "sw:cs:type:item")
        callbacks = _callbacks(keyboard)
        assert "atomic Item batch" in text
        assert "sw:cs:input:item:batch-ai" in callbacks
        assert "sw:cs:input:item:batch-manual" in callbacks

        prompt, _ = studio_callback_view(conn, 1, "sw:cs:input:item:batch-ai")
        assert "ITEM BATCH · AI DRAFT" in prompt
        session = conn.execute(
            "SELECT creation_type,input_mode,expected_input FROM creation_sandbox_studio_sessions WHERE user_id=1"
        ).fetchone()
        assert tuple(session) == ("item", "ai_generated", "item-batch-description")


def test_ai_batch_preview_and_atomic_approval_reuse_i5_8(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    candidate = _batch_candidate()
    monkeypatch.setattr(
        batch_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "fake", "model_id": "fake-model", "parameters": {}},
    )
    monkeypatch.setattr(batch_studio, "generate_structured", lambda *args, **kwargs: deepcopy(candidate))

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        draft = ai_item_batch_draft(conn, 9, "Create a bottle, six energy bars, and a storage bin holding the bars")
        assert draft["proposal"]["properties"]["item_batch"]["items"][1]["payload"]["relationships"]["stored_in"] == "$bin"

        text, keyboard = draft_preview_view(conn, 9)
        assert "ITEM BATCH SANDBOX DRAFT" in text
        assert "Items: 3" in text
        assert "Whole-batch I5.8 validation passed" in text
        assert "stored in $bin" in text
        assert "sw:cs:approve" in _callbacks(keyboard)

        created = approve_item_batch_draft(conn, 9, int(draft["revision"]))
        assert len(created) == 3
        assert active_draft(conn, 9) is None
        assert canonical_state_fingerprint(conn) == before

        names = {obj["item"]["definition"]["name"] for obj in created}
        assert names == {"Steel Water Bottle", "Energy Bar", "Storage Bin"}
        bin_id = next(obj["object_id"] for obj in created if obj["item"]["definition"]["name"] == "Storage Bin")
        bars = next(obj for obj in created if obj["item"]["definition"]["name"] == "Energy Bar")
        assert ("stored_in", bin_id) in {
            (rel["relation_type"], rel["target_object_id"]) for rel in bars["resolved_relations"]
        }

        list_text, _ = sandbox_list_view(conn, "item")
        assert "Steel Water Bottle" in list_text
        assert "Energy Bar" in list_text
        assert "Storage Bin" in list_text


def test_batch_callback_confirmation_materializes_entire_graph(tmp_path, monkeypatch) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setattr(
        batch_studio,
        "creator_creation_binding",
        lambda conn: {"provider_id": "fake", "model_id": "fake-model", "parameters": {}},
    )
    monkeypatch.setattr(batch_studio, "generate_structured", lambda *args, **kwargs: _batch_candidate())

    with connect(db) as conn:
        draft = ai_item_batch_draft(conn, 12, "Create a small supply set")
        confirm_text, confirm_keyboard = studio_callback_view(conn, 12, "sw:cs:approve")
        confirm = f"sw:cs:approve:confirm:{draft['revision']}"
        assert confirm in _callbacks(confirm_keyboard)
        assert "Item Batch (3)" in confirm_text

        approved_text, approved_keyboard = studio_callback_view(conn, 12, confirm)
        assert "SANDBOX ITEM BATCH APPROVED" in approved_text
        assert "Created atomically: 3 Items" in approved_text
        assert "sw:list:item" in _callbacks(approved_keyboard)

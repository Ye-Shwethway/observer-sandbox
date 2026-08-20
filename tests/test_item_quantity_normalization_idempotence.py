from __future__ import annotations

from copy import deepcopy

import pytest

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.db import connect
from observer_sandbox.item_creation_schema import ItemSchemaError, validate_item_payload
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import create_sandbox_item
from observer_sandbox.telegram_sandbox_item_edit import enter_sandbox_item_edit, exit_sandbox_item_edit


def _revalidatable(normalized: dict) -> dict:
    payload = deepcopy(normalized)
    payload.pop("derived", None)
    return payload


def test_validator_accepts_its_normalized_physical_quantity_shape():
    first = validate_item_payload(manual_item_template())
    mass = first["definition"]["modules"]["physical"]["mass"]
    assert mass == {"kind": "mass", "value": pytest.approx(0.317514659), "unit": "kg"}

    second = validate_item_payload(_revalidatable(first))
    assert second["definition"]["modules"]["physical"]["mass"] == mass


def test_normalized_quantity_kind_must_match_expected_dimension():
    normalized = validate_item_payload(manual_item_template())
    payload = _revalidatable(normalized)
    payload["definition"]["modules"]["physical"]["mass"]["kind"] = "length"

    with pytest.raises(ItemSchemaError, match="modules.physical.mass.kind must be 'mass'"):
        validate_item_payload(payload)


def test_quantity_still_rejects_unregistered_extra_fields():
    payload = manual_item_template()
    payload["definition"]["modules"]["physical"]["mass"]["source"] = "guess"

    with pytest.raises(ItemSchemaError, match="unknown field"):
        validate_item_payload(payload)


def test_fresh_materialized_item_can_enter_edit_after_normalization(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        item = create_sandbox_item(conn, manual_item_template(), requested_by="test")
        text, _ = enter_sandbox_item_edit(conn, user_id=91, object_id=item["object_id"])
        assert "SANDBOX ITEM EDIT" in text
        exit_sandbox_item_edit(conn, user_id=91)

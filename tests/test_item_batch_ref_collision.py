import pytest

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.db import connect
from observer_sandbox.item_ai_contract import canonicalize_ai_item_batch_fill
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_item_creation import SandboxItemBatchError, preview_sandbox_item_batch


def test_canonical_ref_collision_remains_invalid(tmp_path):
    first = manual_item_template()
    first["definition"]["key"] = "first"
    second = manual_item_template()
    second["definition"]["key"] = "second"

    candidate = canonicalize_ai_item_batch_fill({
        "items": [
            {"ref": "LED Flashlight", "payload": first},
            {"ref": "LED   Flashlight", "payload": second},
        ]
    })
    assert [entry["ref"] for entry in candidate["items"]] == ["led_flashlight", "led_flashlight"]

    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        with pytest.raises(SandboxItemBatchError):
            preview_sandbox_item_batch(conn, candidate["items"])

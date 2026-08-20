from copy import deepcopy

from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.item_creation_schema import validate_item_payload
from observer_sandbox.telegram_item_draft_review import item_detail_view, render_item_draft_text
from observer_sandbox.telegram_world_layers_item_extension import approved_item_detail_text


def _training_item():
    payload = manual_item_template()
    physical = deepcopy(payload["definition"]["modules"]["physical"])
    payload["definition"].update(
        {
            "key": "fixed_dumbbell_55lb",
            "name": "55 lb Fixed Dumbbell",
            "kind": "equipment",
            "capabilities": ["inspect", "train"],
            "tags": ["dumbbell", "training"],
            "modules": {
                "physical": physical,
                "resistance_training": {"resistance_load": {"value": 55, "unit": "lb"}},
            },
        }
    )
    return payload


def _draft(payload):
    return {
        "revision": 1,
        "draft_mode": "manual",
        "proposal": {"properties": {"item_payload": payload}},
    }


def test_training_item_draft_review_uses_socket_derived_resistance_grade():
    detail, _ = item_detail_view(_draft(_training_item()), 0)
    assert "GRADING" in detail
    assert "Resistance Load: S · Expert" in detail
    assert "item-resistance-load-v1" not in detail


def test_approved_training_item_uses_same_socket_grade_from_normalized_facts():
    normalized = validate_item_payload(_training_item())
    normalized.pop("relationships")
    value = {
        "object_id": "sbx_item_dumbbell",
        "lifecycle_status": "active",
        "resolved_relations": [],
        "item": normalized,
    }
    detail = approved_item_detail_text(None, value)
    assert "🏅 GRADING" in detail
    assert "Resistance Load: S · Expert" in detail
    assert "item-resistance-load-v1" not in detail


def test_ordinary_item_is_explicitly_ungraded_without_fabricated_overall_grade():
    payload = manual_item_template()
    detail, _ = item_detail_view(_draft(payload), 0)
    assert "GRADING" in detail
    assert "No registered grading dimensions apply to this Item yet." in detail
    assert "Overall" not in detail


def test_raw_item_draft_export_does_not_gain_grading_authority_fields():
    draft = _draft(_training_item())
    _, exported = render_item_draft_text(draft)
    assert '"resistance_load": {' in exported
    assert '"value": 55' in exported
    assert '"unit": "lb"' in exported
    assert "grade_plan" not in exported
    assert "universal-grade-plan-v1" not in exported
    assert "Resistance Load: S" not in exported

from __future__ import annotations

import pytest

from observer_sandbox.grading import evaluate_item_resistance_load, evaluate_raps_100
from observer_sandbox.physical_quantity import normalize_physical_quantity
from observer_sandbox.requirements import (
    RequirementContext,
    RequirementContractError,
    evaluate_access_policy,
    evaluate_location_entry,
    evaluate_requirements,
)


def _context(
    *,
    strength: int = 50,
    owned: tuple[str, ...] = (),
    resident: tuple[str, ...] = (),
    authorized: tuple[str, ...] = (),
    skills: tuple[str, ...] = (),
    items: tuple[str, ...] = (),
    equipped: tuple[str, ...] = (),
    states: dict[str, object] | None = None,
) -> RequirementContext:
    strength_grade = evaluate_raps_100(strength)
    return RequirementContext(
        grades={("character", "strength"): strength_grade},
        values={"raps_pa.strength": strength},
        skills=frozenset(skills),
        item_refs=frozenset(items),
        equipped_refs=frozenset(equipped),
        owned_refs=frozenset(owned),
        resident_locations=frozenset(resident),
        authorized_locations=frozenset(authorized),
        states=states or {},
    )


def test_public_access_does_not_depend_on_location_or_character_grade() -> None:
    low_grade_character = _context(strength=10)

    result = evaluate_location_entry(
        {"mode": "public"},
        "open",
        low_grade_character,
        location_id="loc_public_high_grade",
    )

    assert result["allowed"] is True
    assert result["access_allowed"] is True
    assert result["operating_allowed"] is True


def test_private_owner_or_resident_access_rejects_unauthorized_high_grade_actor() -> None:
    high_grade_character = _context(strength=100)

    denied = evaluate_access_policy(
        {"mode": "owner_or_resident"},
        high_grade_character,
        location_id="loc_private_estate",
    )
    owner = evaluate_access_policy(
        {"mode": "owner_or_resident"},
        _context(strength=10, owned=("loc_private_estate",)),
        location_id="loc_private_estate",
    )
    resident = evaluate_access_policy(
        {"mode": "owner_or_resident"},
        _context(strength=10, resident=("loc_private_estate",)),
        location_id="loc_private_estate",
    )

    assert denied["allowed"] is False
    assert denied["failures"][0]["reason"] == "owner_or_resident_required"
    assert owner["allowed"] is True
    assert resident["allowed"] is True


def test_grade_gated_requirement_uses_character_grade_dimension_not_item_grade() -> None:
    context = _context(strength=75)
    requirement = {
        "type": "minimum_grade",
        "domain": "character",
        "dimension": "strength",
        "minimum": "S",
    }

    result = evaluate_requirements(requirement, context)

    assert result["satisfied"] is False
    assert result["failures"][0]["actual"] == "A"

    item_grade = evaluate_item_resistance_load(normalize_physical_quantity("mass", 55, "lb"))
    assert item_grade.grade == "S"
    assert item_grade.domain == "item"
    assert ("item", "resistance_load") not in context.grades


def test_requirement_all_and_any_composition_is_deterministic() -> None:
    context = _context(
        strength=90,
        skills=("skill_climbing",),
        items=("item_rope",),
    )
    requirement = {
        "all": [
            {
                "type": "minimum_grade",
                "domain": "character",
                "dimension": "strength",
                "minimum": "S",
            },
            {
                "any": [
                    {"type": "has_skill", "skill": "skill_climbing"},
                    {"type": "has_item", "ref": "item_grappling_device"},
                ]
            },
            {"type": "has_item", "ref": "item_rope"},
        ]
    }

    result = evaluate_requirements(requirement, context)

    assert result["satisfied"] is True
    assert result["failures"] == []
    assert len(result["evaluated"]) == 4


def test_missing_authoritative_evidence_fails_closed_without_fabrication() -> None:
    context = _context()

    grade = evaluate_requirements(
        {
            "type": "minimum_grade",
            "domain": "character",
            "dimension": "navigation",
            "minimum": "B",
        },
        context,
    )
    state = evaluate_requirements(
        {"type": "state_compare", "key": "quest.bridge_open", "operator": "eq", "value": True},
        context,
    )

    assert grade["satisfied"] is False
    assert state["satisfied"] is False


def test_possession_equipment_ownership_and_authorization_are_distinct() -> None:
    context = _context(
        owned=("item_key",),
        items=("item_flashlight",),
        equipped=("item_flashlight",),
        authorized=("loc_lab",),
    )

    assert evaluate_requirements({"type": "owns", "ref": "item_key"}, context)["satisfied"] is True
    assert evaluate_requirements({"type": "has_item", "ref": "item_key"}, context)["satisfied"] is False
    assert evaluate_requirements({"type": "has_item", "ref": "item_flashlight"}, context)["satisfied"] is True
    assert evaluate_requirements({"type": "equipped", "ref": "item_flashlight"}, context)["satisfied"] is True
    assert evaluate_requirements({"type": "authorized_for", "location_id": "loc_lab"}, context)["satisfied"] is True


def test_authorized_access_and_restricted_access_are_explicit() -> None:
    allowed = evaluate_access_policy(
        {"mode": "authorized"},
        _context(authorized=("loc_lab",)),
        location_id="loc_lab",
    )
    denied = evaluate_access_policy(
        {"mode": "restricted"},
        _context(strength=100, authorized=("loc_lab",)),
        location_id="loc_lab",
    )

    assert allowed["allowed"] is True
    assert denied["allowed"] is False
    assert denied["failures"][0]["reason"] == "restricted"


def test_requirement_based_access_returns_structured_unmet_requirements() -> None:
    policy = {
        "mode": "requirements",
        "requirements": {
            "all": [
                {
                    "type": "minimum_grade",
                    "domain": "character",
                    "dimension": "strength",
                    "minimum": "S",
                },
                {"type": "authorized_for", "location_id": "loc_training_vault"},
            ]
        },
    }

    result = evaluate_access_policy(
        policy,
        _context(strength=75),
        location_id="loc_training_vault",
    )

    assert result["allowed"] is False
    assert result["requirements"]["satisfied"] is False
    assert len(result["failures"]) == 2


def test_operating_state_is_separate_from_access_authority() -> None:
    context = _context()

    open_result = evaluate_location_entry({"mode": "public"}, "open", context, location_id="loc_shop")
    closed_result = evaluate_location_entry({"mode": "public"}, "closed", context, location_id="loc_shop")

    assert open_result["allowed"] is True
    assert closed_result["access_allowed"] is True
    assert closed_result["operating_allowed"] is False
    assert closed_result["allowed"] is False
    assert closed_result["failures"][-1]["reason"] == "operating_state_closed"


def test_value_and_state_compare_reuse_fail_closed_comparison_semantics() -> None:
    context = RequirementContext(
        grades={},
        values={"body.weight_lb": 200, "clearance": "alpha"},
        states={"quest.gate": "open"},
    )

    assert evaluate_requirements(
        {"type": "value_compare", "key": "body.weight_lb", "operator": "gte", "value": 180},
        context,
    )["satisfied"] is True
    assert evaluate_requirements(
        {"type": "state_compare", "key": "quest.gate", "operator": "eq", "value": "open"},
        context,
    )["satisfied"] is True


def test_malformed_contracts_fail_closed_as_contract_errors() -> None:
    context = _context()

    with pytest.raises(RequirementContractError, match="typed leaf"):
        evaluate_requirements({"foo": []}, context)
    with pytest.raises(RequirementContractError, match="non-empty list"):
        evaluate_requirements({"all": []}, context)
    with pytest.raises(RequirementContractError, match="unknown field"):
        evaluate_requirements({"type": "has_skill", "skill": "x", "extra": True}, context)
    with pytest.raises(RequirementContractError, match="Unsupported access policy mode"):
        evaluate_access_policy({"mode": "magic"}, context, location_id="loc_x")
    with pytest.raises(RequirementContractError, match="Unsupported operating state"):
        evaluate_location_entry({"mode": "public"}, "maybe", context, location_id="loc_x")

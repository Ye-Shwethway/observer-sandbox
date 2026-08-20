from __future__ import annotations

import math

import pytest

from observer_sandbox.grading import (
    BODY_PHYSIQUE_COMPOSITE_SCHEME_ID,
    GRADE_VOCABULARY,
    ITEM_RESISTANCE_LOAD_SCHEME_ID,
    LOCATION_COMPLETENESS_SCHEME_ID,
    RAPS_100_PROOF_SCHEME_ID,
    GradeResult,
    build_grade_profile,
    compare_grades,
    evaluate_item_resistance_load,
    evaluate_location_completeness,
    evaluate_raps_100,
    grade_rank,
    grading_scheme,
    meets_minimum_grade,
)
from observer_sandbox.physical_quantity import (
    display_physical_quantity,
    normalize_physical_quantity,
)


def test_shared_grade_vocabulary_has_deterministic_order() -> None:
    grades = [grade for grade, _label in GRADE_VOCABULARY]

    assert grades == ["E", "D", "C", "B", "A", "S", "SS", "SSS", "X", "XX"]
    assert [grade_rank(grade) for grade in grades] == list(range(10))
    assert compare_grades("E", "S") == -1
    assert compare_grades("SS", "SS") == 0
    assert compare_grades("XX", "X") == 1
    assert meets_minimum_grade("S", "A") is True
    assert meets_minimum_grade("B", "A") is False

    with pytest.raises(ValueError, match="Unknown grade"):
        grade_rank("Z")


def test_existing_character_grading_behavior_is_preserved() -> None:
    result = evaluate_raps_100(90)
    scheme = grading_scheme(RAPS_100_PROOF_SCHEME_ID)

    assert result.grade == "S"
    assert result.label == "Expert"
    assert result.value == 90.0
    assert result.scheme_id == RAPS_100_PROOF_SCHEME_ID
    assert result.domain == "character"
    assert result.dimension == "attribute_capability"
    assert scheme.supported_grades == ("E", "D", "C", "B", "A", "S")


def test_item_load_grade_derives_from_normalized_physical_truth() -> None:
    from_pounds = normalize_physical_quantity("mass", 55, "lb")
    from_metric = normalize_physical_quantity("mass", 24.94758035, "kg")

    pounds_result = evaluate_item_resistance_load(from_pounds)
    metric_result = evaluate_item_resistance_load(from_metric)

    assert pounds_result.scheme_id == metric_result.scheme_id
    assert pounds_result.grade == metric_result.grade
    assert pounds_result.label == metric_result.label
    assert pounds_result.domain == metric_result.domain
    assert pounds_result.dimension == metric_result.dimension
    assert math.isclose(pounds_result.value, metric_result.value, rel_tol=0.0, abs_tol=1e-12)
    assert pounds_result.scheme_id == ITEM_RESISTANCE_LOAD_SCHEME_ID
    assert pounds_result.domain == "item"
    assert pounds_result.dimension == "resistance_load"
    assert pounds_result.grade == "S"


def test_display_unit_changes_cannot_change_item_grade() -> None:
    quantity = normalize_physical_quantity("mass", 55, "lb")
    before = evaluate_item_resistance_load(quantity)

    imperial = display_physical_quantity(quantity, system="imperial")
    metric = display_physical_quantity(quantity, system="metric")
    after = evaluate_item_resistance_load(quantity)

    assert imperial["unit"] == "lb"
    assert metric["unit"] == "kg"
    assert before == after


def test_item_load_grade_is_not_a_character_requirement() -> None:
    scheme = grading_scheme(ITEM_RESISTANCE_LOAD_SCHEME_ID)
    result = evaluate_item_resistance_load(normalize_physical_quantity("mass", 55, "lb"))

    assert result.grade == "S"
    assert scheme.domain == "item"
    assert scheme.dimension == "resistance_load"
    assert "not a Character strength requirement" in scheme.description


def test_location_completeness_reuses_existing_l0_l4_contract() -> None:
    assert evaluate_location_completeness("L0").grade == "E"
    assert evaluate_location_completeness("L1").grade == "D"
    assert evaluate_location_completeness("L2").grade == "C"
    assert evaluate_location_completeness("L3").grade == "B"
    result = evaluate_location_completeness("L4")

    assert result.grade == "A"
    assert result.scheme_id == LOCATION_COMPLETENESS_SCHEME_ID
    assert result.domain == "location"
    assert result.dimension == "completeness"
    assert grading_scheme(LOCATION_COMPLETENESS_SCHEME_ID).supported_grades == ("E", "D", "C", "B", "A")

    with pytest.raises(ValueError, match="expects L0..L4"):
        evaluate_location_completeness("L5")


def test_grade_profile_groups_explicit_domain_dimensions_without_persisting_new_truth() -> None:
    load = evaluate_item_resistance_load(normalize_physical_quantity("mass", 20, "lb"))
    profile = build_grade_profile("item", {"resistance_load": load})

    assert profile.domain == "item"
    assert profile.dimensions["resistance_load"] is load
    assert profile.overall is None

    with pytest.raises(ValueError, match="belongs to character, not item"):
        build_grade_profile("item", {"strength": evaluate_raps_100(90)})


def test_overall_grade_requires_explicit_composite_scheme() -> None:
    load = evaluate_item_resistance_load(normalize_physical_quantity("mass", 20, "lb"))

    with pytest.raises(ValueError, match="explicit composite scheme"):
        build_grade_profile("item", {"resistance_load": load}, overall=load)

    body_overall = GradeResult(
        scheme_id=BODY_PHYSIQUE_COMPOSITE_SCHEME_ID,
        grade="A",
        label="Advanced",
        value=82.5,
        domain="body",
        dimension="physique_composite",
    )
    body_dimension = GradeResult(
        scheme_id="body-aesthetic-proportion-v1",
        grade="A",
        label="Advanced",
        value=0.62,
        domain="body",
        dimension="aesthetic_proportion",
    )
    profile = build_grade_profile("body", {"aesthetic_proportion": body_dimension}, overall=body_overall)

    assert profile.overall is body_overall

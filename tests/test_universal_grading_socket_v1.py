import pytest

from observer_sandbox.grading import GradeResult
from observer_sandbox.grading_socket import (
    DEFAULT_UNIVERSE_GRADING_POLICY_ID,
    DimensionSpec,
    EvaluatorSpec,
    GradingSocketError,
    GradingSocketRegistry,
    UniverseGradingPolicy,
    resolve_grade_profile,
)


def _resistance_source(base_kg: float = 55.0 * 0.45359237):
    return {
        "definition": {
            "modules": {
                "resistance_training": {
                    "resistance_load": {"kind": "mass", "value": base_kg, "unit": "kg"}
                }
            }
        }
    }


def test_default_item_resistance_plan_preserves_existing_grade():
    plan, profile = resolve_grade_profile("item", _resistance_source())
    assert plan.universe_policy_id == DEFAULT_UNIVERSE_GRADING_POLICY_ID
    assert [row.dimension_id for row in plan.dimensions] == ["resistance_load"]
    assert profile is not None
    result = profile.dimensions["resistance_load"]
    assert result.scheme_id == "item-resistance-load-v1"
    assert result.grade == "S"
    assert result.domain == "item"
    assert result.dimension == "resistance_load"


def test_ordinary_item_without_registered_dimension_is_ungraded():
    plan, profile = resolve_grade_profile(
        "item",
        {"definition": {"modules": {"physical": {"mass": {"kind": "mass", "value": 1.0, "unit": "kg"}}}}},
    )
    assert plan.dimensions == ()
    assert profile is None


def test_new_dimension_and_evaluator_plug_in_without_resolver_change():
    registry = GradingSocketRegistry()

    def durability_evaluator(evidence, _reference):
        value = float(evidence["definition.modules.durability.rating"])
        grade = "A" if value >= 80 else "C"
        return GradeResult(
            scheme_id="item-durability-proof-v1",
            grade=grade,
            label="Advanced" if grade == "A" else "Capable",
            value=value,
            domain="item",
            dimension="durability",
        )

    registry.register_evaluator(
        EvaluatorSpec(
            evaluator_id="item-durability-proof-v1",
            family="monotonic",
            domain="item",
            supported_grades=("C", "A"),
        ),
        durability_evaluator,
    )
    registry.register_dimension(
        DimensionSpec(
            dimension_id="durability",
            domain="item",
            label="Durability",
            evaluator_id="item-durability-proof-v1",
            source_paths=("definition.modules.durability.rating",),
        )
    )
    registry.register_universe_policy(
        UniverseGradingPolicy(
            policy_id="synthetic-world-v1",
            allowed_domains=frozenset({"item"}),
            allowed_dimensions=frozenset({"durability"}),
            allowed_evaluators=frozenset({"item-durability-proof-v1"}),
            grade_ceiling="S",
        )
    )

    plan, profile = registry.resolve(
        "item",
        {"definition": {"modules": {"durability": {"rating": 85}}}},
        universe_policy_id="synthetic-world-v1",
    )
    assert [row.dimension_id for row in plan.dimensions] == ["durability"]
    assert profile is not None
    assert profile.dimensions["durability"].grade == "A"


def test_dimension_registration_fails_closed_for_unknown_evaluator():
    registry = GradingSocketRegistry()
    with pytest.raises(GradingSocketError, match="Unknown evaluator"):
        registry.register_dimension(
            DimensionSpec(
                dimension_id="mystery",
                domain="item",
                label="Mystery",
                evaluator_id="missing-v1",
                source_paths=("definition.modules.mystery.value",),
            )
        )


def test_missing_reference_profile_fails_closed_when_dimension_is_considered():
    registry = GradingSocketRegistry()
    registry.register_evaluator(
        EvaluatorSpec("item-reference-proof-v1", "reference-relative", "item", ("B",)),
        lambda evidence, reference: GradeResult(
            "item-reference-proof-v1", "B", "Skilled", float(evidence["x"]), "item", "reference_score"
        ),
    )
    registry.register_dimension(
        DimensionSpec(
            "reference_score",
            "item",
            "Reference Score",
            "item-reference-proof-v1",
            ("x",),
            reference_profile_id="missing-reference-v1",
        )
    )
    registry.register_universe_policy(
        UniverseGradingPolicy(
            "reference-world-v1",
            allowed_domains=frozenset({"item"}),
            allowed_dimensions=frozenset({"reference_score"}),
            allowed_evaluators=frozenset({"item-reference-proof-v1"}),
        )
    )
    with pytest.raises(GradingSocketError, match="unknown reference profile"):
        registry.build_plan("item", {"x": 1}, universe_policy_id="reference-world-v1")


def test_default_realistic_policy_does_not_auto_admit_new_dimension():
    from observer_sandbox.grading_socket import build_default_grading_socket_registry

    registry = build_default_grading_socket_registry()
    registry.register_evaluator(
        EvaluatorSpec("item-magical-potency-v1", "monotonic", "item", ("S",)),
        lambda evidence, reference: GradeResult(
            "item-magical-potency-v1", "S", "Expert", float(evidence["magic"]), "item", "magical_potency"
        ),
    )
    registry.register_dimension(
        DimensionSpec(
            "magical_potency",
            "item",
            "Magical Potency",
            "item-magical-potency-v1",
            ("magic",),
        )
    )
    plan, profile = registry.resolve("item", {"magic": 100})
    assert plan.dimensions == ()
    assert profile is None


def test_policy_rejects_manual_plan_dimension_outside_allowlist():
    registry = GradingSocketRegistry()
    registry.register_evaluator(
        EvaluatorSpec("item-proof-v1", "monotonic", "item", ("B",)),
        lambda evidence, reference: GradeResult("item-proof-v1", "B", "Skilled", 1.0, "item", "proof"),
    )
    registry.register_dimension(DimensionSpec("proof", "item", "Proof", "item-proof-v1", ("x",)))
    registry.register_universe_policy(
        UniverseGradingPolicy(
            "blocked-world-v1",
            allowed_domains=frozenset({"item"}),
            allowed_dimensions=frozenset(),
            allowed_evaluators=frozenset(),
        )
    )
    plan = registry.build_plan("item", {"x": 1}, universe_policy_id="blocked-world-v1")
    assert plan.dimensions == ()


def test_evaluator_mismatched_scheme_id_is_rejected():
    registry = GradingSocketRegistry()
    registry.register_evaluator(
        EvaluatorSpec("item-correct-v1", "monotonic", "item", ("B",)),
        lambda evidence, reference: GradeResult("item-wrong-v1", "B", "Skilled", 1.0, "item", "proof"),
    )
    registry.register_dimension(DimensionSpec("proof", "item", "Proof", "item-correct-v1", ("x",)))
    registry.register_universe_policy(
        UniverseGradingPolicy(
            "strict-world-v1",
            allowed_domains=frozenset({"item"}),
            allowed_dimensions=frozenset({"proof"}),
            allowed_evaluators=frozenset({"item-correct-v1"}),
        )
    )
    plan = registry.build_plan("item", {"x": 1}, universe_policy_id="strict-world-v1")
    with pytest.raises(GradingSocketError, match="mismatched scheme id"):
        registry.evaluate_plan(plan, {"x": 1})


def test_policy_grade_ceiling_is_enforced():
    registry = GradingSocketRegistry()
    registry.register_evaluator(
        EvaluatorSpec("item-overcap-v1", "monotonic", "item", ("SS",)),
        lambda evidence, reference: GradeResult("item-overcap-v1", "SS", "Elite", 1.0, "item", "power"),
    )
    registry.register_dimension(DimensionSpec("power", "item", "Power", "item-overcap-v1", ("x",)))
    registry.register_universe_policy(
        UniverseGradingPolicy(
            "capped-world-v1",
            allowed_domains=frozenset({"item"}),
            allowed_dimensions=frozenset({"power"}),
            allowed_evaluators=frozenset({"item-overcap-v1"}),
            grade_ceiling="S",
        )
    )
    plan = registry.build_plan("item", {"x": 1}, universe_policy_id="capped-world-v1")
    with pytest.raises(GradingSocketError, match="caps grades at S"):
        registry.evaluate_plan(plan, {"x": 1})

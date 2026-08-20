from __future__ import annotations

from typing import Any, Mapping

from .grading import GRADE_LABELS, GradeResult
from .grading_socket import (
    DimensionSpec,
    EvaluatorSpec,
    GradingSocketError,
    GradingSocketRegistry,
    ReferenceProfile,
    UniverseGradingPolicy,
    build_default_grading_socket_registry,
)


ITEM_COVERAGE_POLICY_ID = "default-realistic-item-coverage-v1"
REFERENCE_BAND_GRADES = ("E", "D", "C", "B", "A", "S")


def _band_evaluator(
    *,
    evaluator_id: str,
    dimension_id: str,
    source_path: str,
):
    def evaluate(evidence: Mapping[str, Any], reference: ReferenceProfile | None) -> GradeResult:
        if reference is None:
            raise GradingSocketError(f"{dimension_id} requires a reference profile")
        raw = evidence.get(source_path)
        if not isinstance(raw, Mapping) or set(raw) != {"value", "unit"}:
            # Existing physical-quantity modules persist `kind` as well.
            if not isinstance(raw, Mapping) or set(raw) != {"kind", "value", "unit"}:
                raise GradingSocketError(f"{source_path} must be a normalized quantity/metric")
        unit = str(raw.get("unit") or "")
        expected_unit = str(reference.data.get("unit") or "")
        if unit != expected_unit:
            raise GradingSocketError(
                f"{dimension_id} expects canonical unit {expected_unit!r}, got {unit!r}"
            )
        value = float(raw["value"])
        bands = reference.data.get("bands")
        if not isinstance(bands, list) or not bands:
            raise GradingSocketError(f"{reference.reference_id} must define non-empty bands")
        selected = None
        last_minimum = None
        for band in bands:
            if not isinstance(band, Mapping) or set(band) != {"grade", "minimum"}:
                raise GradingSocketError(f"{reference.reference_id} has invalid band shape")
            grade = str(band["grade"]).upper()
            if grade not in REFERENCE_BAND_GRADES:
                raise GradingSocketError(f"{reference.reference_id} has unsupported grade {grade}")
            minimum = float(band["minimum"])
            if last_minimum is not None and minimum <= last_minimum:
                raise GradingSocketError(f"{reference.reference_id} bands must be strictly ascending")
            last_minimum = minimum
            if value >= minimum:
                selected = grade
        if selected is None:
            selected = str(bands[0]["grade"]).upper()
        return GradeResult(
            scheme_id=evaluator_id,
            grade=selected,
            label=GRADE_LABELS[selected],
            value=value,
            domain="item",
            dimension=dimension_id,
        )

    return evaluate


def _register_band_dimension(
    registry: GradingSocketRegistry,
    *,
    dimension_id: str,
    label: str,
    source_path: str,
    unit: str,
    minima: tuple[float, float, float, float, float, float],
    note: str,
) -> tuple[str, str]:
    evaluator_id = f"item-{dimension_id.replace('_', '-')}-magnitude-v1"
    reference_id = f"item-{dimension_id.replace('_', '-')}-bands-v1"
    registry.register_evaluator(
        EvaluatorSpec(evaluator_id, "reference-bands", "item", REFERENCE_BAND_GRADES),
        _band_evaluator(
            evaluator_id=evaluator_id,
            dimension_id=dimension_id,
            source_path=source_path,
        ),
    )
    registry.register_dimension(
        DimensionSpec(
            dimension_id=dimension_id,
            domain="item",
            label=label,
            evaluator_id=evaluator_id,
            source_paths=(source_path,),
            reference_profile_id=reference_id,
        )
    )
    registry.register_reference_profile(
        ReferenceProfile(
            reference_id=reference_id,
            domain="item",
            dimension_id=dimension_id,
            data={
                "unit": unit,
                "bands": [
                    {"grade": grade, "minimum": minimum}
                    for grade, minimum in zip(REFERENCE_BAND_GRADES, minima)
                ],
                "semantic": "capability_magnitude",
                "note": note,
            },
        )
    )
    return evaluator_id, reference_id


def build_item_grading_coverage_registry() -> GradingSocketRegistry:
    registry = build_default_grading_socket_registry()
    allowed_dimensions = {"resistance_load"}
    allowed_evaluators = {"item-resistance-load-v1"}
    allowed_references: set[str] = set()

    configs = (
        ("storage_capacity", "Storage Capacity", "definition.modules.container.capacity_volume", "m3", (0.0001, 0.001, 0.005, 0.02, 0.05, 0.2), "Physical container-volume magnitude; not storage quality."),
        ("luminous_flux", "Luminous Flux", "definition.modules.metrics.luminous_flux", "lm", (1, 50, 150, 500, 1000, 3000), "Visible light-output magnitude."),
        ("runtime", "Runtime", "definition.modules.metrics.runtime", "h", (0.25, 1, 4, 8, 24, 72), "Represented continuous operating-duration magnitude."),
        ("power", "Power", "definition.modules.metrics.power", "W", (0.1, 1, 10, 100, 1000, 10000), "Represented power magnitude; not efficiency."),
        ("energy_capacity", "Energy Capacity", "definition.modules.metrics.energy_capacity", "Wh", (0.1, 1, 10, 100, 1000, 10000), "Represented stored-energy magnitude."),
        ("range", "Range", "definition.modules.metrics.range", "m", (1, 10, 100, 1000, 10000, 100000), "Represented operating/reach range magnitude."),
        ("speed", "Speed", "definition.modules.metrics.speed", "m/s", (0.1, 1, 5, 20, 100, 300), "Represented speed magnitude."),
        ("data_rate", "Data Rate", "definition.modules.metrics.data_rate", "Mbps", (0.1, 1, 10, 100, 1000, 10000), "Represented data-throughput magnitude."),
        ("digital_storage", "Digital Storage", "definition.modules.metrics.digital_storage", "GB", (0.001, 0.1, 1, 100, 1000, 10000), "Represented digital-storage magnitude."),
        ("beam_distance", "Beam Distance", "definition.modules.metrics.beam_distance", "m", (10, 50, 100, 250, 500, 1000), "Represented useful beam-distance magnitude."),
        ("water_resistance_depth", "Water Resistance Depth", "definition.modules.metrics.water_resistance_depth", "m", (0.1, 1, 5, 10, 30, 100), "Represented water-depth resistance magnitude; not a certification claim."),
        ("payload_capacity", "Payload Capacity", "definition.modules.metrics.payload_capacity", "kg", (0.1, 1, 5, 20, 50, 200), "Represented supported payload/load-capacity magnitude."),
    )

    for dimension_id, label, source_path, unit, minima, note in configs:
        evaluator_id, reference_id = _register_band_dimension(
            registry,
            dimension_id=dimension_id,
            label=label,
            source_path=source_path,
            unit=unit,
            minima=minima,
            note=note,
        )
        allowed_dimensions.add(dimension_id)
        allowed_evaluators.add(evaluator_id)
        allowed_references.add(reference_id)

    registry.register_universe_policy(
        UniverseGradingPolicy(
            policy_id=ITEM_COVERAGE_POLICY_ID,
            allowed_domains=frozenset({"item"}),
            allowed_dimensions=frozenset(allowed_dimensions),
            allowed_evaluators=frozenset(allowed_evaluators),
            allowed_reference_profiles=frozenset(allowed_references),
            grade_ceiling="S",
        )
    )
    return registry


ITEM_GRADING_COVERAGE_REGISTRY = build_item_grading_coverage_registry()


__all__ = [
    "ITEM_COVERAGE_POLICY_ID",
    "ITEM_GRADING_COVERAGE_REGISTRY",
    "REFERENCE_BAND_GRADES",
    "build_item_grading_coverage_registry",
]

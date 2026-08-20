from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Callable, Mapping

from .grading import GradeProfile, GradeResult, build_grade_profile, evaluate_item_resistance_load
from .physical_quantity import PhysicalQuantity


GRADE_PLAN_VERSION = "universal-grade-plan-v1"
DEFAULT_UNIVERSE_GRADING_POLICY_ID = "default-realistic-v1"

_ID_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._-][a-z0-9]+)*$")


class GradingSocketError(ValueError):
    pass


@dataclass(frozen=True)
class EvaluatorSpec:
    evaluator_id: str
    family: str
    domain: str
    supported_grades: tuple[str, ...]


@dataclass(frozen=True)
class DimensionSpec:
    dimension_id: str
    domain: str
    label: str
    evaluator_id: str
    source_paths: tuple[str, ...]
    reference_profile_id: str | None = None
    critical: bool = False


@dataclass(frozen=True)
class ReferenceProfile:
    reference_id: str
    domain: str
    dimension_id: str
    data: Mapping[str, Any]


@dataclass(frozen=True)
class UniverseGradingPolicy:
    policy_id: str
    allowed_domains: frozenset[str] | None = None
    allowed_dimensions: frozenset[str] | None = None
    allowed_evaluators: frozenset[str] | None = None
    allowed_reference_profiles: frozenset[str] | None = None
    grade_ceiling: str | None = None


@dataclass(frozen=True)
class GradePlanDimension:
    dimension_id: str
    label: str
    evaluator_id: str
    source_paths: tuple[str, ...]
    reference_profile_id: str | None = None
    critical: bool = False


@dataclass(frozen=True)
class GradePlan:
    plan_version: str
    domain: str
    universe_policy_id: str
    dimensions: tuple[GradePlanDimension, ...]


Evaluator = Callable[[Mapping[str, Any], ReferenceProfile | None], GradeResult]
Applicability = Callable[[Mapping[str, Any]], bool]


def _stable_id(value: str, *, label: str) -> str:
    normalized = str(value or "").strip().lower()
    if not _ID_RE.fullmatch(normalized):
        raise GradingSocketError(f"{label} must be a stable lowercase id")
    return normalized


def _path_value(source: Mapping[str, Any], path: str) -> Any:
    current: Any = source
    for part in str(path).split("."):
        if not isinstance(current, Mapping) or part not in current:
            return None
        current = current[part]
    return current


class GradingSocketRegistry:
    def __init__(self) -> None:
        self._evaluators: dict[str, tuple[EvaluatorSpec, Evaluator]] = {}
        self._dimensions: dict[str, tuple[DimensionSpec, Applicability | None]] = {}
        self._references: dict[str, ReferenceProfile] = {}
        self._policies: dict[str, UniverseGradingPolicy] = {}

    def register_evaluator(self, spec: EvaluatorSpec, evaluator: Evaluator) -> None:
        evaluator_id = _stable_id(spec.evaluator_id, label="evaluator_id")
        domain = _stable_id(spec.domain, label="evaluator domain")
        family = _stable_id(spec.family, label="evaluator family")
        if evaluator_id in self._evaluators:
            raise GradingSocketError(f"Evaluator already registered: {evaluator_id}")
        if not callable(evaluator):
            raise TypeError("evaluator must be callable")
        supported = tuple(str(value).strip().upper() for value in spec.supported_grades)
        if not supported:
            raise GradingSocketError("Evaluator must declare supported grades")
        self._evaluators[evaluator_id] = (
            EvaluatorSpec(evaluator_id, family, domain, supported),
            evaluator,
        )

    def register_dimension(
        self,
        spec: DimensionSpec,
        *,
        applicability: Applicability | None = None,
    ) -> None:
        dimension_id = _stable_id(spec.dimension_id, label="dimension_id")
        domain = _stable_id(spec.domain, label="dimension domain")
        evaluator_id = _stable_id(spec.evaluator_id, label="dimension evaluator_id")
        if dimension_id in self._dimensions:
            raise GradingSocketError(f"Dimension already registered: {dimension_id}")
        evaluator_entry = self._evaluators.get(evaluator_id)
        if evaluator_entry is None:
            raise GradingSocketError(f"Unknown evaluator for dimension {dimension_id}: {evaluator_id}")
        if evaluator_entry[0].domain != domain:
            raise GradingSocketError(
                f"Evaluator {evaluator_id} belongs to {evaluator_entry[0].domain}, not {domain}"
            )
        paths = tuple(str(path).strip() for path in spec.source_paths if str(path).strip())
        if not paths:
            raise GradingSocketError("Dimension must declare at least one authoritative source path")
        reference_id = None
        if spec.reference_profile_id is not None:
            reference_id = _stable_id(spec.reference_profile_id, label="reference_profile_id")
        self._dimensions[dimension_id] = (
            DimensionSpec(
                dimension_id=dimension_id,
                domain=domain,
                label=str(spec.label or "").strip() or dimension_id.replace("_", " ").title(),
                evaluator_id=evaluator_id,
                source_paths=paths,
                reference_profile_id=reference_id,
                critical=bool(spec.critical),
            ),
            applicability,
        )

    def register_reference_profile(self, profile: ReferenceProfile) -> None:
        reference_id = _stable_id(profile.reference_id, label="reference_id")
        domain = _stable_id(profile.domain, label="reference domain")
        dimension_id = _stable_id(profile.dimension_id, label="reference dimension_id")
        if reference_id in self._references:
            raise GradingSocketError(f"Reference profile already registered: {reference_id}")
        dimension_entry = self._dimensions.get(dimension_id)
        if dimension_entry is None:
            raise GradingSocketError(f"Unknown dimension for reference profile: {dimension_id}")
        if dimension_entry[0].domain != domain:
            raise GradingSocketError(
                f"Dimension {dimension_id} belongs to {dimension_entry[0].domain}, not {domain}"
            )
        self._references[reference_id] = ReferenceProfile(
            reference_id, domain, dimension_id, dict(profile.data)
        )

    def register_universe_policy(self, policy: UniverseGradingPolicy) -> None:
        policy_id = _stable_id(policy.policy_id, label="policy_id")
        if policy_id in self._policies:
            raise GradingSocketError(f"Universe grading policy already registered: {policy_id}")
        self._policies[policy_id] = UniverseGradingPolicy(
            policy_id=policy_id,
            allowed_domains=None if policy.allowed_domains is None else frozenset(
                _stable_id(value, label="allowed domain") for value in policy.allowed_domains
            ),
            allowed_dimensions=None if policy.allowed_dimensions is None else frozenset(
                _stable_id(value, label="allowed dimension") for value in policy.allowed_dimensions
            ),
            allowed_evaluators=None if policy.allowed_evaluators is None else frozenset(
                _stable_id(value, label="allowed evaluator") for value in policy.allowed_evaluators
            ),
            allowed_reference_profiles=None if policy.allowed_reference_profiles is None else frozenset(
                _stable_id(value, label="allowed reference profile")
                for value in policy.allowed_reference_profiles
            ),
            grade_ceiling=None if policy.grade_ceiling is None else str(policy.grade_ceiling).strip().upper(),
        )

    def evaluator_spec(self, evaluator_id: str) -> EvaluatorSpec:
        key = _stable_id(evaluator_id, label="evaluator_id")
        try:
            return self._evaluators[key][0]
        except KeyError as exc:
            raise GradingSocketError(f"Unknown evaluator: {key}") from exc

    def dimension_spec(self, dimension_id: str) -> DimensionSpec:
        key = _stable_id(dimension_id, label="dimension_id")
        try:
            return self._dimensions[key][0]
        except KeyError as exc:
            raise GradingSocketError(f"Unknown dimension: {key}") from exc

    def universe_policy(self, policy_id: str) -> UniverseGradingPolicy:
        key = _stable_id(policy_id, label="policy_id")
        try:
            return self._policies[key]
        except KeyError as exc:
            raise GradingSocketError(f"Unknown universe grading policy: {key}") from exc

    def build_plan(
        self,
        domain: str,
        source: Mapping[str, Any],
        *,
        universe_policy_id: str = DEFAULT_UNIVERSE_GRADING_POLICY_ID,
    ) -> GradePlan:
        normalized_domain = _stable_id(domain, label="domain")
        policy = self.universe_policy(universe_policy_id)
        if policy.allowed_domains is not None and normalized_domain not in policy.allowed_domains:
            raise GradingSocketError(
                f"Universe grading policy {policy.policy_id} does not allow domain {normalized_domain}"
            )
        rows: list[GradePlanDimension] = []
        for dimension_id, (spec, applicability) in sorted(self._dimensions.items()):
            if spec.domain != normalized_domain:
                continue
            if policy.allowed_dimensions is not None and dimension_id not in policy.allowed_dimensions:
                continue
            if policy.allowed_evaluators is not None and spec.evaluator_id not in policy.allowed_evaluators:
                continue
            if spec.reference_profile_id is not None:
                if spec.reference_profile_id not in self._references:
                    raise GradingSocketError(
                        f"Dimension {dimension_id} requires unknown reference profile: {spec.reference_profile_id}"
                    )
                if (
                    policy.allowed_reference_profiles is not None
                    and spec.reference_profile_id not in policy.allowed_reference_profiles
                ):
                    continue
            if any(_path_value(source, path) is None for path in spec.source_paths):
                continue
            if applicability is not None and not bool(applicability(source)):
                continue
            rows.append(
                GradePlanDimension(
                    dimension_id=dimension_id,
                    label=spec.label,
                    evaluator_id=spec.evaluator_id,
                    source_paths=spec.source_paths,
                    reference_profile_id=spec.reference_profile_id,
                    critical=spec.critical,
                )
            )
        return GradePlan(
            plan_version=GRADE_PLAN_VERSION,
            domain=normalized_domain,
            universe_policy_id=policy.policy_id,
            dimensions=tuple(rows),
        )

    def evaluate_plan(
        self,
        plan: GradePlan,
        source: Mapping[str, Any],
    ) -> GradeProfile | None:
        policy = self.universe_policy(plan.universe_policy_id)
        results: dict[str, GradeResult] = {}
        for row in plan.dimensions:
            spec = self.dimension_spec(row.dimension_id)
            if spec.domain != plan.domain:
                raise GradingSocketError(
                    f"Dimension {spec.dimension_id} belongs to {spec.domain}, not {plan.domain}"
                )
            evaluator_spec, evaluator = self._evaluators.get(row.evaluator_id, (None, None))
            if evaluator_spec is None or evaluator is None:
                raise GradingSocketError(f"Unknown evaluator: {row.evaluator_id}")
            if policy.allowed_dimensions is not None and row.dimension_id not in policy.allowed_dimensions:
                raise GradingSocketError(
                    f"Universe grading policy {policy.policy_id} does not allow dimension {row.dimension_id}"
                )
            if policy.allowed_evaluators is not None and row.evaluator_id not in policy.allowed_evaluators:
                raise GradingSocketError(
                    f"Universe grading policy {policy.policy_id} does not allow evaluator {row.evaluator_id}"
                )
            evidence = {path: _path_value(source, path) for path in row.source_paths}
            if any(value is None for value in evidence.values()):
                raise GradingSocketError(f"Missing authoritative evidence for dimension {row.dimension_id}")
            reference = None
            if row.reference_profile_id is not None:
                try:
                    reference = self._references[row.reference_profile_id]
                except KeyError as exc:
                    raise GradingSocketError(
                        f"Unknown reference profile: {row.reference_profile_id}"
                    ) from exc
            result = evaluator(evidence, reference)
            if result.domain is not None and result.domain != plan.domain:
                raise GradingSocketError(
                    f"Evaluator {row.evaluator_id} returned domain {result.domain}, expected {plan.domain}"
                )
            if result.dimension is not None and result.dimension != row.dimension_id:
                raise GradingSocketError(
                    f"Evaluator {row.evaluator_id} returned dimension {result.dimension}, expected {row.dimension_id}"
                )
            if result.grade not in evaluator_spec.supported_grades:
                raise GradingSocketError(
                    f"Evaluator {row.evaluator_id} returned unsupported grade {result.grade}"
                )
            results[row.dimension_id] = result
        if not results:
            return None
        return build_grade_profile(plan.domain, results)

    def resolve(
        self,
        domain: str,
        source: Mapping[str, Any],
        *,
        universe_policy_id: str = DEFAULT_UNIVERSE_GRADING_POLICY_ID,
    ) -> tuple[GradePlan, GradeProfile | None]:
        plan = self.build_plan(domain, source, universe_policy_id=universe_policy_id)
        return plan, self.evaluate_plan(plan, source)


def _normalized_quantity_evaluator(
    expected_path: str,
    expected_kind: str,
    evaluator: Callable[[PhysicalQuantity], GradeResult],
) -> Evaluator:
    def run(evidence: Mapping[str, Any], _reference: ReferenceProfile | None) -> GradeResult:
        raw = evidence.get(expected_path)
        if not isinstance(raw, Mapping):
            raise GradingSocketError(f"{expected_path} must be a normalized physical quantity")
        if set(raw) != {"kind", "value", "unit"}:
            raise GradingSocketError(
                f"{expected_path} must contain exactly kind, value and unit after normalization"
            )
        if str(raw["kind"]) != expected_kind:
            raise GradingSocketError(f"{expected_path}.kind must be {expected_kind!r}")
        quantity = PhysicalQuantity(expected_kind, float(raw["value"]))
        if str(raw["unit"]) != quantity.base_unit:
            raise GradingSocketError(
                f"{expected_path}.unit must be canonical base unit {quantity.base_unit!r}"
            )
        return evaluator(quantity)

    return run


def build_default_grading_socket_registry() -> GradingSocketRegistry:
    registry = GradingSocketRegistry()
    registry.register_evaluator(
        EvaluatorSpec(
            evaluator_id="item-resistance-load-v1",
            family="monotonic",
            domain="item",
            supported_grades=("E", "D", "C", "B", "A", "S"),
        ),
        _normalized_quantity_evaluator(
            "definition.modules.resistance_training.resistance_load",
            "mass",
            evaluate_item_resistance_load,
        ),
    )
    registry.register_dimension(
        DimensionSpec(
            dimension_id="resistance_load",
            domain="item",
            label="Resistance Load",
            evaluator_id="item-resistance-load-v1",
            source_paths=("definition.modules.resistance_training.resistance_load",),
        )
    )
    registry.register_universe_policy(
        UniverseGradingPolicy(
            policy_id=DEFAULT_UNIVERSE_GRADING_POLICY_ID,
            allowed_domains=frozenset({"item", "location", "character", "body"}),
            allowed_dimensions=None,
            allowed_evaluators=None,
            allowed_reference_profiles=None,
            grade_ceiling="S",
        )
    )
    return registry


DEFAULT_GRADING_SOCKET_REGISTRY = build_default_grading_socket_registry()


def resolve_grade_profile(
    domain: str,
    source: Mapping[str, Any],
    *,
    universe_policy_id: str = DEFAULT_UNIVERSE_GRADING_POLICY_ID,
    registry: GradingSocketRegistry = DEFAULT_GRADING_SOCKET_REGISTRY,
) -> tuple[GradePlan, GradeProfile | None]:
    return registry.resolve(domain, source, universe_policy_id=universe_policy_id)


__all__ = [
    "DEFAULT_GRADING_SOCKET_REGISTRY",
    "DEFAULT_UNIVERSE_GRADING_POLICY_ID",
    "DimensionSpec",
    "EvaluatorSpec",
    "GRADE_PLAN_VERSION",
    "GradePlan",
    "GradePlanDimension",
    "GradingSocketError",
    "GradingSocketRegistry",
    "ReferenceProfile",
    "UniverseGradingPolicy",
    "build_default_grading_socket_registry",
    "resolve_grade_profile",
]

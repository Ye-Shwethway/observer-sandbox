from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .action_conditions import ActionConditionError, _compare
from .grading import GradeResult, meets_minimum_grade


class RequirementContractError(ValueError):
    pass


@dataclass(frozen=True)
class RequirementContext:
    grades: Mapping[tuple[str, str], GradeResult]
    values: Mapping[str, Any]
    skills: frozenset[str] = frozenset()
    item_refs: frozenset[str] = frozenset()
    equipped_refs: frozenset[str] = frozenset()
    owned_refs: frozenset[str] = frozenset()
    resident_locations: frozenset[str] = frozenset()
    authorized_locations: frozenset[str] = frozenset()
    states: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "skills", frozenset(self.skills))
        object.__setattr__(self, "item_refs", frozenset(self.item_refs))
        object.__setattr__(self, "equipped_refs", frozenset(self.equipped_refs))
        object.__setattr__(self, "owned_refs", frozenset(self.owned_refs))
        object.__setattr__(self, "resident_locations", frozenset(self.resident_locations))
        object.__setattr__(self, "authorized_locations", frozenset(self.authorized_locations))
        if self.states is None:
            object.__setattr__(self, "states", {})


_ALLOWED_LEAF_TYPES = {
    "minimum_grade",
    "value_compare",
    "has_skill",
    "has_item",
    "equipped",
    "owns",
    "resident_of",
    "authorized_for",
    "state_compare",
}


def _require_exact_keys(payload: Mapping[str, Any], required: set[str], optional: set[str] | None = None) -> None:
    optional = optional or set()
    keys = set(payload)
    missing = required - keys
    unknown = keys - required - optional
    if missing:
        raise RequirementContractError(f"Requirement is missing required field(s): {sorted(missing)}")
    if unknown:
        raise RequirementContractError(f"Requirement has unknown field(s): {sorted(unknown)}")


def _evaluation_item(requirement: Mapping[str, Any], *, satisfied: bool, actual: Any = None) -> dict[str, Any]:
    item = {"requirement": dict(requirement), "satisfied": bool(satisfied)}
    if actual is not None:
        item["actual"] = actual
    return item


def _evaluate_leaf(requirement: Mapping[str, Any], context: RequirementContext) -> dict[str, Any]:
    requirement_type = requirement.get("type")
    if requirement_type not in _ALLOWED_LEAF_TYPES:
        raise RequirementContractError(f"Unsupported requirement type: {requirement_type!r}")

    if requirement_type == "minimum_grade":
        _require_exact_keys(requirement, {"type", "domain", "dimension", "minimum"})
        domain = str(requirement["domain"] or "").strip().lower()
        dimension = str(requirement["dimension"] or "").strip()
        minimum = str(requirement["minimum"] or "").strip().upper()
        if not domain or not dimension or not minimum:
            raise RequirementContractError("minimum_grade requires domain, dimension and minimum")
        result = context.grades.get((domain, dimension))
        if result is None:
            return _evaluation_item(requirement, satisfied=False, actual=None)
        satisfied = meets_minimum_grade(result.grade, minimum)
        return _evaluation_item(requirement, satisfied=satisfied, actual=result.grade)

    if requirement_type in {"value_compare", "state_compare"}:
        _require_exact_keys(requirement, {"type", "key", "operator", "value"})
        key = str(requirement["key"] or "").strip()
        operator = str(requirement["operator"] or "").strip()
        if not key:
            raise RequirementContractError(f"{requirement_type} requires a key")
        source = context.values if requirement_type == "value_compare" else (context.states or {})
        if key not in source:
            return _evaluation_item(requirement, satisfied=False, actual=None)
        actual = source[key]
        try:
            satisfied = _compare(actual, operator, requirement["value"])
        except ActionConditionError as exc:
            raise RequirementContractError(str(exc)) from exc
        return _evaluation_item(requirement, satisfied=satisfied, actual=actual)

    if requirement_type == "has_skill":
        _require_exact_keys(requirement, {"type", "skill"})
        ref = str(requirement["skill"] or "").strip()
        if not ref:
            raise RequirementContractError("has_skill requires a skill")
        return _evaluation_item(requirement, satisfied=ref in context.skills, actual=ref in context.skills)

    if requirement_type in {"has_item", "equipped", "owns"}:
        _require_exact_keys(requirement, {"type", "ref"})
        ref = str(requirement["ref"] or "").strip()
        if not ref:
            raise RequirementContractError(f"{requirement_type} requires a ref")
        source = {
            "has_item": context.item_refs,
            "equipped": context.equipped_refs,
            "owns": context.owned_refs,
        }[requirement_type]
        return _evaluation_item(requirement, satisfied=ref in source, actual=ref in source)

    if requirement_type in {"resident_of", "authorized_for"}:
        _require_exact_keys(requirement, {"type", "location_id"})
        location_id = str(requirement["location_id"] or "").strip()
        if not location_id:
            raise RequirementContractError(f"{requirement_type} requires a location_id")
        source = context.resident_locations if requirement_type == "resident_of" else context.authorized_locations
        return _evaluation_item(requirement, satisfied=location_id in source, actual=location_id in source)

    raise AssertionError("unreachable requirement type")


def evaluate_requirements(requirement: Mapping[str, Any] | None, context: RequirementContext) -> dict[str, Any]:
    """Evaluate the universal typed requirement contract.

    A requirement is either one typed leaf or exactly one non-empty `all`/`any`
    composition. Missing authoritative evidence fails closed; malformed contracts
    raise a deterministic contract error.
    """

    if requirement is None:
        return {"satisfied": True, "evaluated": [], "failures": []}
    if not isinstance(requirement, Mapping):
        raise RequirementContractError("Requirement must be an object")

    keys = set(requirement)
    if keys in ({"all"}, {"any"}):
        mode = next(iter(keys))
        children = requirement[mode]
        if not isinstance(children, list) or not children:
            raise RequirementContractError(f"Requirement '{mode}' must be a non-empty list")
        child_results = [evaluate_requirements(child, context) for child in children]
        satisfied = all(result["satisfied"] for result in child_results) if mode == "all" else any(
            result["satisfied"] for result in child_results
        )
        evaluated = [item for result in child_results for item in result["evaluated"]]
        if satisfied:
            failures: list[dict[str, Any]] = []
        elif mode == "all":
            failures = [item for result in child_results for item in result["failures"]]
        else:
            failures = [
                {
                    "composition": "any",
                    "message": "No alternative requirement branch was satisfied",
                    "branches": [result["failures"] for result in child_results],
                }
            ]
        return {"satisfied": satisfied, "evaluated": evaluated, "failures": failures}

    if "type" not in requirement:
        raise RequirementContractError("Requirement must be a typed leaf or exactly one 'all'/'any' composition")
    item = _evaluate_leaf(requirement, context)
    return {
        "satisfied": bool(item["satisfied"]),
        "evaluated": [item],
        "failures": [] if item["satisfied"] else [item],
    }


_ACCESS_MODES = {
    "public",
    "owner_or_resident",
    "authorized",
    "restricted",
    "requirements",
}


def evaluate_access_policy(
    policy: Mapping[str, Any],
    context: RequirementContext,
    *,
    location_id: str,
) -> dict[str, Any]:
    if not isinstance(policy, Mapping):
        raise RequirementContractError("Access policy must be an object")
    mode = str(policy.get("mode") or "").strip().lower()
    if mode not in _ACCESS_MODES:
        raise RequirementContractError(f"Unsupported access policy mode: {mode!r}")

    if mode == "public":
        _require_exact_keys(policy, {"mode"})
        return {"allowed": True, "mode": mode, "failures": []}

    if mode == "owner_or_resident":
        _require_exact_keys(policy, {"mode"})
        allowed = location_id in context.owned_refs or location_id in context.resident_locations
        return {
            "allowed": allowed,
            "mode": mode,
            "failures": [] if allowed else [{"reason": "owner_or_resident_required", "location_id": location_id}],
        }

    if mode == "authorized":
        _require_exact_keys(policy, {"mode"})
        allowed = location_id in context.authorized_locations
        return {
            "allowed": allowed,
            "mode": mode,
            "failures": [] if allowed else [{"reason": "authorization_required", "location_id": location_id}],
        }

    if mode == "restricted":
        _require_exact_keys(policy, {"mode"})
        return {
            "allowed": False,
            "mode": mode,
            "failures": [{"reason": "restricted", "location_id": location_id}],
        }

    _require_exact_keys(policy, {"mode", "requirements"})
    result = evaluate_requirements(policy["requirements"], context)
    return {"allowed": result["satisfied"], "mode": mode, "failures": result["failures"], "requirements": result}


def evaluate_location_entry(
    access_policy: Mapping[str, Any],
    operating_state: str,
    context: RequirementContext,
    *,
    location_id: str,
) -> dict[str, Any]:
    """Compose access authority with separate current operating state."""

    state = str(operating_state or "").strip().lower()
    if state not in {"open", "closed", "locked", "blocked"}:
        raise RequirementContractError(f"Unsupported operating state: {operating_state!r}")
    access = evaluate_access_policy(access_policy, context, location_id=location_id)
    operating_allowed = state == "open"
    failures = list(access["failures"])
    if not operating_allowed:
        failures.append({"reason": f"operating_state_{state}", "location_id": location_id})
    return {
        "allowed": bool(access["allowed"] and operating_allowed),
        "access_allowed": bool(access["allowed"]),
        "operating_allowed": operating_allowed,
        "access": access,
        "operating_state": state,
        "failures": failures,
    }


__all__ = [
    "RequirementContext",
    "RequirementContractError",
    "evaluate_access_policy",
    "evaluate_location_entry",
    "evaluate_requirements",
]

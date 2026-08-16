from __future__ import annotations

from typing import Any


class ActionConditionError(ValueError):
    pass


SUPPORTED_OPERATORS = {"lt", "lte", "gt", "gte", "eq", "ne"}


def _compare(actual: Any, operator: str, expected: Any) -> bool:
    if operator not in SUPPORTED_OPERATORS:
        raise ActionConditionError(f"Unsupported action condition operator: {operator!r}")
    if operator == "eq":
        return actual == expected
    if operator == "ne":
        return actual != expected
    if isinstance(actual, bool) or isinstance(expected, bool):
        raise ActionConditionError(f"Operator {operator!r} requires non-boolean comparable values")
    if not isinstance(actual, (int, float, str)) or not isinstance(expected, type(actual)):
        if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
            actual = float(actual)
            expected = float(expected)
        else:
            raise ActionConditionError(f"Operator {operator!r} received incompatible values")
    if operator == "lt":
        return actual < expected
    if operator == "lte":
        return actual <= expected
    if operator == "gt":
        return actual > expected
    return actual >= expected


def evaluate_action_conditions(
    conditions: dict[str, Any] | None,
    values: dict[str, Any],
) -> dict[str, Any]:
    """Evaluate the bounded v1 action-definition prerequisite contract.

    V1 accepts only an optional `all` list. Every clause requires exactly a
    `field_key`, `operator`, and `value`. Missing fields and malformed contracts
    fail closed rather than silently authorizing the action.
    """

    if not conditions:
        return {"satisfied": True, "clauses": [], "failures": []}
    if not isinstance(conditions, dict) or set(conditions) != {"all"}:
        raise ActionConditionError("Action conditions v1 requires exactly an 'all' clause list")
    clauses = conditions["all"]
    if not isinstance(clauses, list) or not clauses:
        raise ActionConditionError("Action conditions 'all' must be a non-empty list")

    evaluated: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for index, clause in enumerate(clauses):
        if not isinstance(clause, dict) or set(clause) != {"field_key", "operator", "value"}:
            raise ActionConditionError(f"Action condition clause {index} has an invalid shape")
        field_key = clause["field_key"]
        operator = clause["operator"]
        if not isinstance(field_key, str) or not field_key:
            raise ActionConditionError(f"Action condition clause {index} requires a field_key")
        if not isinstance(operator, str):
            raise ActionConditionError(f"Action condition clause {index} requires an operator")
        if field_key not in values:
            raise ActionConditionError(f"Action condition field is unavailable: {field_key}")
        actual = values[field_key]
        expected = clause["value"]
        satisfied = _compare(actual, operator, expected)
        item = {
            "field_key": field_key,
            "operator": operator,
            "expected": expected,
            "actual": actual,
            "satisfied": satisfied,
        }
        evaluated.append(item)
        if not satisfied:
            failures.append(item)
    return {"satisfied": not failures, "clauses": evaluated, "failures": failures}

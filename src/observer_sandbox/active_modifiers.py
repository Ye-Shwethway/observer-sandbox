from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from typing import Any


class ActiveModifierError(ValueError):
    pass


def _parse_sim_time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(str(value))
    except ValueError as exc:
        raise ActiveModifierError(f"Invalid modifier simulation time: {value!r}") from exc


def _numeric_value(raw_json: str, *, modifier_id: str) -> float:
    try:
        value = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ActiveModifierError(f"Modifier {modifier_id!r} has invalid value JSON") from exc
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ActiveModifierError(f"Modifier {modifier_id!r} requires a numeric value")
    return float(value)


def _conditions_match(raw_json: str, context: dict[str, Any] | None) -> bool:
    try:
        conditions = json.loads(raw_json or "{}")
    except json.JSONDecodeError as exc:
        raise ActiveModifierError("Active modifier conditions must be valid JSON") from exc
    if not isinstance(conditions, dict):
        raise ActiveModifierError("Active modifier conditions must be an object")
    if not conditions:
        return True
    if context is None:
        return False
    return all(context.get(str(key)) == expected for key, expected in conditions.items())


def active_modifier_rows(
    conn: sqlite3.Connection,
    subject_id: str,
    field_key: str,
    *,
    as_of_sim_time: str,
    context: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return active, condition-matching modifier rows for one subject/field.

    Time bounds are half-open: starts_sim_time <= as_of < ends_sim_time. An
    absent end time means the modifier remains active until explicitly removed.
    Conditions v1 are exact key/value matches against caller-supplied context.
    """

    as_of = _parse_sim_time(as_of_sim_time)
    rows = conn.execute(
        """
        SELECT id,subject_id,source_entity_id,source_action_id,field_key,operation,
               value_json,starts_sim_time,ends_sim_time,stack_key,stack_policy,
               conditions_json,metadata_json
        FROM active_modifiers
        WHERE subject_id=? AND field_key=?
        ORDER BY starts_sim_time,id
        """,
        (subject_id, field_key),
    ).fetchall()
    result: list[dict[str, Any]] = []
    for row in rows:
        starts = _parse_sim_time(str(row["starts_sim_time"]))
        ends = _parse_sim_time(str(row["ends_sim_time"])) if row["ends_sim_time"] else None
        if as_of < starts or (ends is not None and as_of >= ends):
            continue
        if not _conditions_match(str(row["conditions_json"] or "{}"), context):
            continue
        modifier_id = str(row["id"])
        result.append(
            {
                "id": modifier_id,
                "subject_id": str(row["subject_id"]),
                "source_entity_id": row["source_entity_id"],
                "source_action_id": row["source_action_id"],
                "field_key": str(row["field_key"]),
                "operation": str(row["operation"]),
                "value": _numeric_value(str(row["value_json"]), modifier_id=modifier_id),
                "starts_sim_time": str(row["starts_sim_time"]),
                "ends_sim_time": row["ends_sim_time"],
                "stack_key": row["stack_key"],
                "stack_policy": str(row["stack_policy"]),
                "conditions": json.loads(row["conditions_json"] or "{}"),
                "metadata": json.loads(row["metadata_json"] or "{}"),
            }
        )
    return result


def _select_stack_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        group_key = str(row["stack_key"]) if row["stack_key"] is not None else f"__modifier__:{row['id']}"
        grouped.setdefault(group_key, []).append(row)

    selected: list[dict[str, Any]] = []
    for group_key, group in grouped.items():
        policies = {str(row["stack_policy"]) for row in group}
        if len(policies) != 1:
            raise ActiveModifierError(f"Modifier stack {group_key!r} mixes stack policies")
        policy = next(iter(policies))
        ordered = sorted(group, key=lambda row: (str(row["starts_sim_time"]), str(row["id"])))
        if policy == "stack":
            selected.extend(ordered)
        elif policy == "replace":
            selected.append(ordered[-1])
        elif policy == "max":
            selected.append(max(ordered, key=lambda row: (float(row["value"]), str(row["starts_sim_time"]), str(row["id"]))))
        elif policy == "min":
            selected.append(min(ordered, key=lambda row: (float(row["value"]), str(row["starts_sim_time"]), str(row["id"]))))
        else:
            raise ActiveModifierError(f"Unsupported stack policy: {policy!r}")
    return sorted(selected, key=lambda row: (str(row["starts_sim_time"]), str(row["id"])))


def resolve_active_modifier_value(
    conn: sqlite3.Connection,
    subject_id: str,
    field_key: str,
    base_value: float | int,
    *,
    as_of_sim_time: str,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Resolve one effective numeric value without mutating authoritative state."""

    if isinstance(base_value, bool) or not isinstance(base_value, (int, float)):
        raise ActiveModifierError("Active Modifier Runtime v1 supports numeric base values only")
    rows = _select_stack_rows(
        active_modifier_rows(
            conn,
            subject_id,
            field_key,
            as_of_sim_time=as_of_sim_time,
            context=context,
        )
    )
    value = float(base_value)
    applied: list[dict[str, Any]] = []
    for row in rows:
        amount = float(row["value"])
        operation = str(row["operation"])
        before = value
        if operation == "add":
            value += amount
        elif operation == "multiply":
            value *= amount
        elif operation == "set":
            value = amount
        elif operation == "clamp_min":
            value = max(value, amount)
        elif operation == "clamp_max":
            value = min(value, amount)
        else:
            raise ActiveModifierError(f"Unsupported modifier operation: {operation!r}")
        applied.append(
            {
                "id": row["id"],
                "operation": operation,
                "value": amount,
                "before": before,
                "after": value,
                "stack_key": row["stack_key"],
                "stack_policy": row["stack_policy"],
                "source_entity_id": row["source_entity_id"],
                "source_action_id": row["source_action_id"],
            }
        )
    return {
        "subject_id": subject_id,
        "field_key": field_key,
        "as_of_sim_time": as_of_sim_time,
        "base_value": float(base_value),
        "effective_value": value,
        "applied": applied,
    }

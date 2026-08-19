from __future__ import annotations

import json
import sqlite3
from typing import Any

from .creation_sandbox import get_sandbox_object
from .creator_profile_edit import _coerce, _validate_numeric
from .sandbox_representation import set_sandbox_profile_values


class SandboxProfileEditError(RuntimeError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _character(conn: sqlite3.Connection, object_id: str) -> dict[str, Any]:
    value = get_sandbox_object(conn, object_id)
    if value["creation_type"] != "character" or value["lifecycle_status"] != "active":
        raise KeyError(f"Unknown active sandbox Character: {object_id}")
    return value


def sandbox_field_state(conn: sqlite3.Connection, object_id: str, field_key: str) -> dict[str, Any]:
    _character(conn, object_id)
    row = conn.execute(
        """
        SELECT v.field_key,v.value_json,v.mode,v.authority,v.source,
               d.label,d.data_type,d.unit,d.domain
        FROM creation_sandbox_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.object_id=? AND v.field_key=?
        """,
        (object_id, field_key),
    ).fetchone()
    if row is None:
        raise SandboxProfileEditError(f"{field_key} has no represented Sandbox value")
    if str(row["mode"]) == "derived":
        raise SandboxProfileEditError(
            f"{field_key} is deterministic derived state; edit authoritative inputs instead"
        )
    return {
        "field_key": str(row["field_key"]),
        "label": str(row["label"]),
        "data_type": str(row["data_type"]),
        "unit": row["unit"],
        "domain": str(row["domain"]),
        "mode": str(row["mode"]),
        "authority": str(row["authority"]),
        "source": row["source"],
        "value": json.loads(row["value_json"]),
    }


def _sandbox_cross_values(
    conn: sqlite3.Connection,
    object_id: str,
    changes: dict[str, Any],
) -> dict[str, Any]:
    result = dict(changes)
    for key in (
        "sexual_anatomy.baseline_erectile_function",
        "sexual_anatomy.erection_firmness_cap",
        "genetics.weight_lean_min_lb",
        "genetics.weight_lean_max_lb",
    ):
        if key in result:
            continue
        row = conn.execute(
            "SELECT value_json FROM creation_sandbox_profile_values WHERE object_id=? AND field_key=?",
            (object_id, key),
        ).fetchone()
        if row is not None:
            result[key] = json.loads(row["value_json"])
    return result


def _validate_cross(conn: sqlite3.Connection, object_id: str, changes: dict[str, Any]) -> None:
    values = _sandbox_cross_values(conn, object_id, changes)
    baseline = values.get("sexual_anatomy.baseline_erectile_function")
    cap = values.get("sexual_anatomy.erection_firmness_cap")
    if baseline is not None and cap is not None and float(baseline) > float(cap):
        raise ValueError("Baseline erectile function cannot exceed erection firmness cap")
    low = values.get("genetics.weight_lean_min_lb")
    high = values.get("genetics.weight_lean_max_lb")
    if low is not None and high is not None and float(low) > float(high):
        raise ValueError("Genetic lean-weight minimum cannot exceed maximum")


def preview_sandbox_profile_edit(
    conn: sqlite3.Connection,
    object_id: str,
    field_key: str,
    raw_value: Any,
) -> dict[str, Any]:
    character = _character(conn, object_id)
    state = sandbox_field_state(conn, object_id, field_key)
    value = _coerce(state["data_type"], raw_value)
    if state["data_type"] in {"number", "integer"}:
        _validate_numeric(field_key, value)
    _validate_cross(conn, object_id, {field_key: value})
    return {
        "object_id": object_id,
        "sandbox_id": character["sandbox_id"],
        "character_name": str(character["identity"].get("name") or object_id),
        "field_key": field_key,
        "label": state["label"],
        "unit": state["unit"],
        "old_value": state["value"],
        "new_value": value,
        "mode": state["mode"],
    }


def apply_sandbox_profile_edit(
    conn: sqlite3.Connection,
    proposal: dict[str, Any],
    *,
    requested_by: str,
) -> dict[str, Any]:
    object_id = str(proposal["object_id"])
    field_key = str(proposal["field_key"])
    character = _character(conn, object_id)
    state = sandbox_field_state(conn, object_id, field_key)
    if state["value"] != proposal.get("old_value"):
        raise SandboxProfileEditError(
            "Sandbox profile changed after preview; reopen the field before applying"
        )
    value = proposal.get("new_value")
    if state["data_type"] in {"number", "integer"}:
        _validate_numeric(field_key, value)
    _validate_cross(conn, object_id, {field_key: value})

    set_sandbox_profile_values(
        conn,
        object_id,
        {field_key: value},
        authority="creator",
        source="telegram-sandbox-profile-edit",
    )
    if field_key == "identity.name":
        identity = dict(character.get("identity") or {})
        identity["name"] = value
        conn.execute(
            "UPDATE creation_sandbox_objects SET identity_json=?,updated_at=CURRENT_TIMESTAMP WHERE object_id=?",
            (_json(identity), object_id),
        )

    conn.execute(
        "UPDATE creation_sandboxes SET revision=revision+1,updated_at=CURRENT_TIMESTAMP WHERE sandbox_id=?",
        (character["sandbox_id"],),
    )
    conn.execute(
        """
        INSERT INTO creation_sandbox_events(sandbox_id,object_id,event_type,payload_json)
        VALUES(?,?, 'sandbox_creator_profile_edit_applied', ?)
        """,
        (
            character["sandbox_id"],
            object_id,
            _json(
                {
                    "field_key": field_key,
                    "old_value": state["value"],
                    "new_value": value,
                    "requested_by": requested_by,
                }
            ),
        ),
    )
    conn.commit()
    return {
        "object_id": object_id,
        "character_name": str(value) if field_key == "identity.name" else str(character["identity"].get("name") or object_id),
        "field_key": field_key,
        "label": state["label"],
        "old_value": state["value"],
        "new_value": value,
    }


__all__ = [
    "SandboxProfileEditError",
    "apply_sandbox_profile_edit",
    "preview_sandbox_profile_edit",
    "sandbox_field_state",
]

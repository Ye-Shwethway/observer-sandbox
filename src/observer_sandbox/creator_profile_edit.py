from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime, timezone
from statistics import fmean
from typing import Any

from .creator_progression_reanchor import reanchor_creator_progression
from .event_log import record_event
from .grading import (
    ATTRIBUTE_RAPS_100_FIELDS,
    GRADE_LABELS,
    evaluate_profile_field,
    evaluate_raps_100,
    evaluate_skill_score,
)
from .profile_change_observer import capture_profile_change_state
from .simulation import runtime_value, set_runtime_value
from .world import set_field

PROPOSAL_PREFIX = "creator_profile_edit_proposal:"
PROPOSAL_VERSION = 1
GRADE_INTERVALS = {
    "E": (0.0, 20.0),
    "D": (20.0, 40.0),
    "C": (40.0, 60.0),
    "B": (60.0, 75.0),
    "A": (75.0, 90.0),
    "S": (90.0, 100.000001),
}
GROUP_ALIASES = {
    "physical": "raps_pa",
    "pa": "raps_pa",
    "mental": "raps_ma",
    "ma": "raps_ma",
    "intellectual": "raps_ia",
    "ia": "raps_ia",
    "verbal": "raps_vc",
    "vc": "raps_vc",
    "attributes": "attributes",
    "all": "attributes",
    "skills": "skills",
}
RAPS_DOMAINS = {"raps_pa", "raps_ma", "raps_ia", "social", "raps_vc"}


class CreatorProfileEditError(RuntimeError):
    pass


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _character(conn: sqlite3.Connection, character_id: str):
    row = conn.execute(
        """
        SELECT e.id,e.name
        FROM entities e JOIN character_profiles p ON p.entity_id=e.id
        WHERE e.id=? AND e.entity_type='character' AND p.status='active'
        """,
        (character_id,),
    ).fetchone()
    if row is None:
        raise KeyError(f"Unknown active character: {character_id}")
    return row


def _definition(conn: sqlite3.Connection, field_key: str):
    row = conn.execute(
        """
        SELECT field_key,label,data_type,unit,default_mode,default_authority,domain
        FROM profile_field_definitions WHERE field_key=?
        """,
        (field_key,),
    ).fetchone()
    if row is None:
        raise KeyError(f"Unknown profile field: {field_key}")
    return row


def _coerce(data_type: str, raw: Any) -> Any:
    if data_type == "number":
        if isinstance(raw, bool):
            raise ValueError("Expected a number")
        try:
            return float(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("Expected a number") from exc
    if data_type == "integer":
        if isinstance(raw, bool):
            raise ValueError("Expected an integer")
        try:
            value = float(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError("Expected an integer") from exc
        if not value.is_integer():
            raise ValueError("Expected an integer")
        return int(value)
    if data_type == "boolean":
        if isinstance(raw, bool):
            return raw
        text = str(raw).strip().lower()
        if text in {"true", "yes", "1", "on"}:
            return True
        if text in {"false", "no", "0", "off"}:
            return False
        raise ValueError("Expected true/false")
    if data_type == "json":
        if isinstance(raw, (dict, list)):
            return raw
        try:
            return json.loads(str(raw))
        except json.JSONDecodeError as exc:
            raise ValueError("Expected valid JSON") from exc
    if data_type in {"text", "date"}:
        value = str(raw).strip()
        if not value:
            raise ValueError("Value cannot be empty")
        if data_type == "date":
            try:
                datetime.fromisoformat(value)
            except ValueError as exc:
                raise ValueError("Expected ISO date/date-time") from exc
        return value
    return raw


def _field_state(conn: sqlite3.Connection, character_id: str, field_key: str) -> dict[str, Any]:
    _character(conn, character_id)
    definition = _definition(conn, field_key)
    row = conn.execute(
        "SELECT value_json,mode,authority FROM character_profile_values WHERE entity_id=? AND field_key=?",
        (character_id, field_key),
    ).fetchone()
    store = "profile"
    if row is None:
        row = conn.execute(
            "SELECT value_json,mode,authority FROM fields WHERE entity_id=? AND field_key=?",
            (character_id, field_key),
        ).fetchone()
        store = "runtime"
    if row is None:
        if str(definition["default_mode"]) == "derived":
            raise CreatorProfileEditError(
                f"{field_key} is deterministic derived state; edit authoritative inputs instead"
            )
        raise CreatorProfileEditError(
            f"{field_key} has no represented writable value for {character_id}"
        )
    return {
        "store": store,
        "field_key": field_key,
        "label": str(definition["label"]),
        "data_type": str(definition["data_type"]),
        "unit": definition["unit"],
        "mode": str(row["mode"]),
        "authority": str(row["authority"]),
        "value": json.loads(row["value_json"]),
    }


def _validate_numeric(field_key: str, value: Any) -> None:
    if field_key in ATTRIBUTE_RAPS_100_FIELDS:
        evaluate_raps_100(value)
    if field_key in {
        "sexual_anatomy.baseline_erectile_function",
        "sexual_anatomy.erection_firmness_cap",
        "sexual_anatomy.erection_firmness",
        "sexual_anatomy.sensitivity",
    }:
        if not 0.0 <= float(value) <= 100.0:
            raise ValueError(f"{field_key} must be within 0..100")


def _cross_values(
    conn: sqlite3.Connection,
    character_id: str,
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
            "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
            (character_id, key),
        ).fetchone()
        if row is not None:
            result[key] = json.loads(row["value_json"])
    return result


def _validate_cross(
    conn: sqlite3.Connection,
    character_id: str,
    changes: dict[str, Any],
) -> None:
    values = _cross_values(conn, character_id, changes)
    baseline = values.get("sexual_anatomy.baseline_erectile_function")
    cap = values.get("sexual_anatomy.erection_firmness_cap")
    if baseline is not None and cap is not None and float(baseline) > float(cap):
        raise ValueError("Baseline erectile function cannot exceed erection firmness cap")
    low = values.get("genetics.weight_lean_min_lb")
    high = values.get("genetics.weight_lean_max_lb")
    if low is not None and high is not None and float(low) > float(high):
        raise ValueError("Genetic lean-weight minimum cannot exceed maximum")


def _grade(field_key: str, value: Any) -> dict[str, Any] | None:
    result = evaluate_profile_field(field_key, value)
    if result is None:
        return None
    return {
        "grade": result.grade,
        "label": result.label,
        "value": round(float(result.value), 3),
    }


def preview_profile_edit(
    conn: sqlite3.Connection,
    character_id: str,
    field_key: str,
    raw_value: Any,
    *,
    mutation_class: str = "canonical_correction",
) -> dict[str, Any]:
    if mutation_class not in {"canonical_correction", "creator_override"}:
        raise ValueError("Invalid mutation class")
    state = _field_state(conn, character_id, field_key)
    value = _coerce(state["data_type"], raw_value)
    _validate_numeric(field_key, value)
    _validate_cross(conn, character_id, {field_key: value})
    return {
        "proposal_version": PROPOSAL_VERSION,
        "kind": "field_edit",
        "character_id": character_id,
        "mutation_class": mutation_class,
        "changes": [
            {
                **{
                    key: state[key]
                    for key in (
                        "store",
                        "field_key",
                        "label",
                        "data_type",
                        "unit",
                        "mode",
                        "authority",
                    )
                },
                "old_value": state["value"],
                "new_value": value,
                "old_grade": _grade(field_key, state["value"]),
                "new_grade": _grade(field_key, value),
            }
        ],
    }


def _target(grade: str) -> float:
    if grade == "S":
        return 95.0
    low, high = GRADE_INTERVALS[grade]
    return (low + high) / 2.0


def _group_items(
    conn: sqlite3.Connection,
    character_id: str,
    group: str,
) -> list[dict[str, Any]]:
    domain = GROUP_ALIASES.get(group.strip().lower(), group.strip().lower())
    if domain == "skills":
        rows = conn.execute(
            "SELECT skill_key,score FROM character_skills WHERE entity_id=? AND score IS NOT NULL ORDER BY skill_key",
            (character_id,),
        ).fetchall()
        return [
            {
                "store": "skill",
                "field_key": f"skill:{row['skill_key']}",
                "label": str(row["skill_key"]),
                "value": float(row["score"]),
            }
            for row in rows
        ]
    domains = RAPS_DOMAINS if domain == "attributes" else {domain}
    if not domains.issubset(RAPS_DOMAINS):
        raise CreatorProfileEditError(f"Unsupported inverse-grade group: {group}")
    rows = conn.execute(
        """
        SELECT v.field_key,v.value_json,d.label,d.domain
        FROM character_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.entity_id=? ORDER BY d.rowid
        """,
        (character_id,),
    ).fetchall()
    items: list[dict[str, Any]] = []
    for row in rows:
        key = str(row["field_key"])
        value = json.loads(row["value_json"])
        if (
            str(row["domain"]) in domains
            and key in ATTRIBUTE_RAPS_100_FIELDS
            and isinstance(value, (int, float))
            and not isinstance(value, bool)
        ):
            items.append(
                {
                    "store": "profile",
                    "field_key": key,
                    "label": str(row["label"]),
                    "value": float(value),
                }
            )
    return items


def _aggregate(store: str, values: list[float]) -> dict[str, Any]:
    mean = fmean(values)
    result = evaluate_skill_score(mean) if store == "skill" else evaluate_raps_100(mean)
    return {"value": round(mean, 3), "grade": result.grade, "label": result.label}


def preview_section_grade_target(
    conn: sqlite3.Connection,
    character_id: str,
    group: str,
    target_grade: str,
    *,
    mode: str = "preserve_shape",
) -> dict[str, Any]:
    _character(conn, character_id)
    grade = target_grade.strip().upper()
    if grade not in GRADE_INTERVALS:
        raise CreatorProfileEditError(
            f"Grade {grade} has no implemented inverse numeric interval in v1"
        )
    if mode not in {"preserve_shape", "normalize"}:
        raise ValueError("mode must be preserve_shape or normalize")
    items = _group_items(conn, character_id, group)
    if not items:
        raise CreatorProfileEditError(f"No inverse-grade-compatible values in group: {group}")
    stores = {item["store"] for item in items}
    if len(stores) != 1:
        raise CreatorProfileEditError(
            "Inverse-grade group must use one compatible grading family"
        )
    store = stores.pop()
    old_values = [float(item["value"]) for item in items]
    target = _target(grade)
    if mode == "normalize":
        proposed = [target] * len(old_values)
    else:
        delta = target - fmean(old_values)
        proposed = [max(0.0, min(100.0, value + delta)) for value in old_values]
        for _ in range(4):
            residual = target - fmean(proposed)
            if abs(residual) <= 1e-9:
                break
            adjustable = [
                index
                for index, value in enumerate(proposed)
                if (residual > 0 and value < 100) or (residual < 0 and value > 0)
            ]
            if not adjustable:
                break
            step = residual * len(proposed) / len(adjustable)
            for index in adjustable:
                proposed[index] = max(0.0, min(100.0, proposed[index] + step))
    aggregate = _aggregate(store, proposed)
    if aggregate["grade"] != grade:
        raise CreatorProfileEditError(
            f"Unable to produce requested grade {grade}; got {aggregate['grade']}"
        )
    changes: list[dict[str, Any]] = []
    for item, new_value in zip(items, proposed):
        old_eval = (
            evaluate_skill_score(item["value"])
            if store == "skill"
            else evaluate_raps_100(item["value"])
        )
        new_eval = (
            evaluate_skill_score(new_value)
            if store == "skill"
            else evaluate_raps_100(new_value)
        )
        changes.append(
            {
                **item,
                "old_value": round(item["value"], 6),
                "new_value": round(new_value, 6),
                "old_grade": {"grade": old_eval.grade, "label": old_eval.label},
                "new_grade": {"grade": new_eval.grade, "label": new_eval.label},
            }
        )
    low, high = GRADE_INTERVALS[grade]
    return {
        "proposal_version": PROPOSAL_VERSION,
        "kind": "section_grade_target",
        "character_id": character_id,
        "mutation_class": "canonical_correction",
        "group": group,
        "target_grade": grade,
        "target_label": GRADE_LABELS[grade],
        "target_interval": [low, 100.0 if grade == "S" else high],
        "interval_upper_exclusive": grade != "S",
        "mode": mode,
        "old_aggregate": _aggregate(store, old_values),
        "new_aggregate": aggregate,
        "changes": changes,
    }


def save_proposal(
    conn: sqlite3.Connection,
    proposal: dict[str, Any],
    *,
    requested_by: str,
) -> str:
    token = uuid.uuid4().hex[:12]
    payload = dict(proposal)
    payload.update(
        {"requested_by": requested_by, "created_at": datetime.now(timezone.utc).isoformat()}
    )
    set_runtime_value(conn, f"{PROPOSAL_PREFIX}{token}", payload)
    conn.commit()
    return token


def load_proposal(conn: sqlite3.Connection, token: str) -> dict[str, Any]:
    payload = runtime_value(conn, f"{PROPOSAL_PREFIX}{token}", None)
    if not isinstance(payload, dict):
        raise KeyError("Unknown or expired Creator profile proposal")
    return payload


def _sim_time(conn: sqlite3.Connection) -> str:
    value = runtime_value(conn, "sim_time", None)
    if not isinstance(value, str) or not value:
        raise RuntimeError("Creator profile editing requires initialized simulation time")
    return value


def _retire_self_knowledge(
    conn: sqlite3.Connection,
    character_id: str,
    field_keys: set[str],
    sim_time: str,
) -> list[str]:
    retired: list[str] = []
    rows = conn.execute(
        """
        SELECT memory_id,content_json,metadata_json
        FROM character_memories
        WHERE character_id=? AND memory_type='semantic' AND status='active'
        """,
        (character_id,),
    ).fetchall()
    for row in rows:
        content = json.loads(row["content_json"] or "{}")
        metadata = json.loads(row["metadata_json"] or "{}")
        claimed: set[str] = set()
        for source in (content, metadata):
            if not isinstance(source, dict):
                continue
            if isinstance(source.get("profile_field_key"), str):
                claimed.add(source["profile_field_key"])
            if isinstance(source.get("profile_field_keys"), list):
                claimed.update(str(value) for value in source["profile_field_keys"])
        if not claimed.intersection(field_keys):
            continue
        metadata = dict(metadata) if isinstance(metadata, dict) else {}
        metadata.update(
            {"retired_by": "creator_profile_correction", "retired_sim_time": sim_time}
        )
        conn.execute(
            "UPDATE character_memories SET status='retired',metadata_json=? WHERE memory_id=?",
            (_json(metadata), row["memory_id"]),
        )
        retired.append(str(row["memory_id"]))
    return retired


def _reanchor_ledgers(conn: sqlite3.Connection, character_id: str) -> None:
    snapshot = capture_profile_change_state(conn, character_id)
    refs = {
        key: {
            "value": float(value["value"]),
            "grade": value.get("grade"),
            "label": value.get("label"),
            "unit": value.get("unit"),
            "domain": value.get("domain"),
            "kind": value.get("kind"),
        }
        for key, value in snapshot.items()
    }
    set_runtime_value(
        conn,
        f"profile_change_display_ledger:{character_id}",
        {"baselines": refs, "display": {}},
    )
    for row in conn.execute(
        "SELECT key FROM runtime_state WHERE key LIKE ?",
        (f"telegram_stat_notification_baseline:%:{character_id}",),
    ).fetchall():
        set_runtime_value(conn, str(row["key"]), refs)


def _fresh(conn: sqlite3.Connection, proposal: dict[str, Any]) -> None:
    character_id = str(proposal["character_id"])
    for change in proposal.get("changes") or []:
        store = str(change["store"])
        key = str(change["field_key"])
        if store == "profile":
            row = conn.execute(
                "SELECT value_json FROM character_profile_values WHERE entity_id=? AND field_key=?",
                (character_id, key),
            ).fetchone()
            current = None if row is None else json.loads(row["value_json"])
        elif store == "runtime":
            row = conn.execute(
                "SELECT value_json FROM fields WHERE entity_id=? AND field_key=?",
                (character_id, key),
            ).fetchone()
            current = None if row is None else json.loads(row["value_json"])
        elif store == "skill":
            row = conn.execute(
                "SELECT score FROM character_skills WHERE entity_id=? AND skill_key=?",
                (character_id, key.split(":", 1)[1]),
            ).fetchone()
            current = None if row is None else float(row["score"])
        else:
            raise CreatorProfileEditError(f"Unknown proposal store: {store}")
        old = change.get("old_value")
        matches = (
            abs(float(current) - float(old)) <= 1e-9
            if isinstance(current, (int, float)) and isinstance(old, (int, float))
            else current == old
        )
        if not matches:
            raise CreatorProfileEditError(
                f"Proposal is stale for {key}; preview again before applying"
            )


def apply_profile_proposal(
    conn: sqlite3.Connection,
    proposal: dict[str, Any],
    *,
    authority: str = "creator",
    requested_by: str | None = None,
) -> dict[str, Any]:
    if int(proposal.get("proposal_version", 0)) != PROPOSAL_VERSION:
        raise CreatorProfileEditError("Unsupported proposal version")
    character_id = str(proposal["character_id"])
    character = _character(conn, character_id)
    changes = list(proposal.get("changes") or [])
    if not changes:
        raise CreatorProfileEditError("Proposal has no changes")
    _fresh(conn, proposal)
    profile_changes = {
        str(change["field_key"]): change["new_value"]
        for change in changes
        if change["store"] in {"profile", "runtime"}
    }
    for key, value in profile_changes.items():
        _validate_numeric(key, value)
    _validate_cross(conn, character_id, profile_changes)
    sim_time = _sim_time(conn)
    nested = conn.in_transaction
    savepoint = "creator_profile_edit"
    conn.execute(f"SAVEPOINT {savepoint}" if nested else "BEGIN IMMEDIATE")
    try:
        applied: list[dict[str, Any]] = []
        affected: set[str] = set()
        for change in changes:
            store = str(change["store"])
            key = str(change["field_key"])
            old = change["old_value"]
            new = change["new_value"]
            if store == "profile":
                row = conn.execute(
                    "SELECT mode,authority FROM character_profile_values WHERE entity_id=? AND field_key=?",
                    (character_id, key),
                ).fetchone()
                if row is None:
                    raise CreatorProfileEditError(f"Missing profile field: {key}")
                conn.execute(
                    """
                    INSERT INTO character_profile_history(
                        entity_id,field_key,old_value_json,new_value_json,mode,authority,reason,sim_time
                    ) VALUES(?,?,?,?,?,?,?,?)
                    """,
                    (
                        character_id,
                        key,
                        _json(old),
                        _json(new),
                        row["mode"],
                        row["authority"],
                        f"creator profile {proposal.get('mutation_class') or 'correction'}",
                        sim_time,
                    ),
                )
                conn.execute(
                    """
                    UPDATE character_profile_values
                    SET value_json=?,source=?,confidence=1.0,observed_at=?,updated_at=CURRENT_TIMESTAMP
                    WHERE entity_id=? AND field_key=?
                    """,
                    (_json(new), "creator-profile-control-v1", sim_time, character_id, key),
                )
                affected.add(key)
            elif store == "runtime":
                row = conn.execute(
                    "SELECT mode,authority FROM fields WHERE entity_id=? AND field_key=?",
                    (character_id, key),
                ).fetchone()
                if row is None:
                    raise CreatorProfileEditError(f"Missing runtime field: {key}")
                set_field(
                    conn,
                    character_id,
                    key,
                    new,
                    mode=str(row["mode"]),
                    authority=str(row["authority"]),
                    source="creator-profile-control-v1",
                )
                affected.add(key)
            elif store == "skill":
                skill_key = key.split(":", 1)[1]
                evaluate_skill_score(new)
                row = conn.execute(
                    "SELECT metadata_json FROM character_skills WHERE entity_id=? AND skill_key=?",
                    (character_id, skill_key),
                ).fetchone()
                if row is None:
                    raise CreatorProfileEditError(f"Missing skill: {skill_key}")
                metadata = json.loads(row["metadata_json"] or "{}")
                metadata = dict(metadata) if isinstance(metadata, dict) else {}
                metadata.update(
                    {
                        "creator_reanchored": True,
                        "creator_reanchored_sim_time": sim_time,
                        "creator_previous_score": old,
                    }
                )
                conn.execute(
                    "UPDATE character_skills SET score=?,metadata_json=? WHERE entity_id=? AND skill_key=?",
                    (float(new), _json(metadata), character_id, skill_key),
                )
            else:
                raise CreatorProfileEditError(f"Unknown proposal store: {store}")
            applied.append(
                {"field_key": key, "store": store, "before": old, "after": new, "new_value": new}
            )

        progression_reanchor = reanchor_creator_progression(
            conn,
            character_id,
            applied,
            sim_time=sim_time,
        )
        retired = _retire_self_knowledge(conn, character_id, affected, sim_time)
        _reanchor_ledgers(conn, character_id)
        record_event(
            conn,
            sim_time=sim_time,
            actor_id=character_id,
            event_type="creator_profile_corrected",
            state_changes={
                item["field_key"]: {"before": item["before"], "after": item["after"]}
                for item in applied
            },
            payload={
                "authority": authority,
                "requested_by": requested_by,
                "mutation_class": proposal.get("mutation_class"),
                "proposal_kind": proposal.get("kind"),
                "target_grade": proposal.get("target_grade"),
                "target_group": proposal.get("group"),
                "target_mode": proposal.get("mode"),
                "retired_profile_self_knowledge": retired,
                "progression_reanchor": progression_reanchor,
                "changes": applied,
            },
        )
        if nested:
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        else:
            conn.commit()
    except Exception:
        if nested:
            conn.execute(f"ROLLBACK TO SAVEPOINT {savepoint}")
            conn.execute(f"RELEASE SAVEPOINT {savepoint}")
        else:
            conn.rollback()
        raise

    return {
        "ok": True,
        "character_id": character_id,
        "character_name": str(character["name"]),
        "proposal_kind": proposal.get("kind"),
        "changes": applied,
        "retired_profile_self_knowledge": retired,
        "progression_reanchor": progression_reanchor,
        "target_grade": proposal.get("target_grade"),
        "new_aggregate": proposal.get("new_aggregate"),
    }


def apply_saved_proposal(
    conn: sqlite3.Connection,
    token: str,
    *,
    requested_by: str,
) -> dict[str, Any]:
    proposal = load_proposal(conn, token)
    owner = proposal.get("requested_by")
    if owner and owner != requested_by:
        raise PermissionError("Creator profile proposal belongs to another requester")
    result = apply_profile_proposal(conn, proposal, requested_by=requested_by)
    conn.execute("DELETE FROM runtime_state WHERE key=?", (f"{PROPOSAL_PREFIX}{token}",))
    conn.commit()
    return result

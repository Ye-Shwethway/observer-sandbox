from __future__ import annotations

import sqlite3
from typing import Any

from .profile_observer import profile_section
from .simulation import runtime_value, set_runtime_value

DISPLAY_LEDGER_PREFIX = "profile_change_display_ledger:"
STAT_PREF_PREFIX = "telegram_stat_notifications:"
STAT_BASELINE_PREFIX = "telegram_stat_notification_baseline:"

_GRADE_RANK = {"E": 0, "D": 1, "C": 2, "B": 3, "A": 4, "S": 5, "SS": 6, "SSS": 7, "X": 8, "XX": 9}
_TRACKED_SECTIONS = ("attributes", "body", "skills")


def _grade_code(entry: dict[str, Any] | None) -> str | None:
    if not isinstance(entry, dict):
        return None
    grade = entry.get("grade")
    if not isinstance(grade, dict):
        return None
    value = grade.get("grade")
    return str(value) if value else None


def _ref(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "value": float(entry["value"]),
        "grade": entry.get("grade"),
        "label": entry.get("label"),
        "unit": entry.get("unit"),
        "domain": entry.get("domain"),
        "kind": entry.get("kind"),
    }


def _entry_key(section_id: str, item: dict[str, Any]) -> str | None:
    if section_id == "skills":
        key = item.get("key")
        return f"skill:{key}" if key else None
    key = item.get("field_key")
    return str(key) if key else None


def capture_profile_change_state(conn: sqlite3.Connection, actor_id: str) -> dict[str, dict[str, Any]]:
    """Capture represented progression surfaces; actors without a profile no-op."""
    captured: dict[str, dict[str, Any]] = {}
    for section_id in _TRACKED_SECTIONS:
        try:
            data = profile_section(conn, actor_id, section_id, role="owner")
        except (KeyError, PermissionError):
            continue
        for item in data.get("content") or []:
            key = _entry_key(section_id, item)
            raw_value = item.get("score") if section_id == "skills" else item.get("value")
            if not key or not isinstance(raw_value, (int, float)) or isinstance(raw_value, bool):
                continue
            captured[key] = {
                "key": key,
                "section_id": section_id,
                "kind": item.get("kind") or ("skill" if section_id == "skills" else "field"),
                "label": item.get("label") or key,
                "domain": item.get("domain") or item.get("category") or section_id,
                "value": float(raw_value),
                "unit": item.get("unit") or ("score" if section_id == "skills" else None),
                "grade": item.get("grade"),
            }
        overall = (data.get("section") or {}).get("overall_grade")
        if isinstance(overall, dict) and isinstance(overall.get("value"), (int, float)):
            key = f"@overall:{section_id}"
            captured[key] = {
                "key": key,
                "section_id": section_id,
                "kind": "section_grade",
                "label": f"{str((data.get('section') or {}).get('label') or section_id)} overall",
                "domain": section_id,
                "value": float(overall["value"]),
                "unit": "score",
                "grade": overall,
            }
    return captured


def _threshold(entry: dict[str, Any]) -> float:
    key = str(entry.get("key") or "")
    unit = str(entry.get("unit") or "")
    kind = str(entry.get("kind") or "")
    if kind == "section_grade":
        return float("inf")
    if key.startswith("skill:") or key.startswith("raps_"):
        return 0.10
    if unit == "in":
        return 0.10 if key == "body.height_in" else 0.05
    if unit == "lb":
        return 0.25
    if unit == "percent":
        return 0.10
    if unit == "ratio":
        return 0.01
    return 0.10


def _beneficial(key: str, old: dict[str, Any], new: dict[str, Any], delta: float) -> bool | None:
    old_grade = _grade_code(old)
    new_grade = _grade_code(new)
    if old_grade != new_grade and old_grade in _GRADE_RANK and new_grade in _GRADE_RANK:
        return _GRADE_RANK[new_grade] > _GRADE_RANK[old_grade]
    if key.startswith("skill:") or key.startswith("raps_"):
        return delta > 0
    return None


def _meaningful(key: str, baseline: dict[str, Any], current: dict[str, Any]) -> bool:
    grade_changed = _grade_code(baseline) != _grade_code(current)
    delta = float(current["value"]) - float(baseline["value"])
    return grade_changed or abs(delta) + 1e-12 >= _threshold(current)


def _change_payload(key: str, baseline: dict[str, Any], current: dict[str, Any], sim_time: str) -> dict[str, Any]:
    delta = float(current["value"]) - float(baseline["value"])
    old_grade = baseline.get("grade") if isinstance(baseline.get("grade"), dict) else None
    new_grade = current.get("grade") if isinstance(current.get("grade"), dict) else None
    return {
        "key": key,
        "label": current.get("label") or baseline.get("label") or key,
        "section_id": current.get("section_id"),
        "domain": current.get("domain"),
        "kind": current.get("kind"),
        "unit": current.get("unit"),
        "before": round(float(baseline["value"]), 6),
        "after": round(float(current["value"]), 6),
        "delta": round(delta, 6),
        "direction": "up" if delta > 0 else "down" if delta < 0 else "flat",
        "beneficial": _beneficial(key, baseline, current, delta),
        "old_grade": old_grade,
        "new_grade": new_grade,
        "grade_changed": _grade_code(baseline) != _grade_code(current),
        "sim_time": sim_time,
    }


def observe_profile_changes(
    conn: sqlite3.Connection,
    actor_id: str,
    before: dict[str, dict[str, Any]],
    after: dict[str, dict[str, Any]],
    *,
    sim_time: str,
) -> list[dict[str, Any]]:
    """Accumulate microscopic changes and retain latest meaningful display deltas."""
    if not before and not after:
        return []
    key = f"{DISPLAY_LEDGER_PREFIX}{actor_id}"
    ledger = runtime_value(conn, key, None)
    if not isinstance(ledger, dict):
        ledger = {"baselines": {}, "display": {}}
    baselines = dict(ledger.get("baselines") or {})
    display = dict(ledger.get("display") or {})
    surfaced: list[dict[str, Any]] = []

    for field_key, current in after.items():
        baseline = baselines.get(field_key)
        if not isinstance(baseline, dict):
            seed = before.get(field_key) or current
            baseline = _ref(seed)
            baselines[field_key] = baseline
        if not _meaningful(field_key, baseline, current):
            continue
        change = _change_payload(field_key, baseline, current, sim_time)
        display[field_key] = change
        baselines[field_key] = _ref(current)
        surfaced.append(change)

    set_runtime_value(conn, key, {"baselines": baselines, "display": display})
    conn.commit()
    return surfaced


def attach_profile_display_deltas(conn: sqlite3.Connection, actor_id: str, data: dict[str, Any]) -> dict[str, Any]:
    ledger = runtime_value(conn, f"{DISPLAY_LEDGER_PREFIX}{actor_id}", {})
    display = (ledger or {}).get("display") if isinstance(ledger, dict) else {}
    if not isinstance(display, dict) or not display:
        return data
    section_id = str((data.get("section") or {}).get("id") or "")
    for item in data.get("content") or []:
        key = _entry_key(section_id, item)
        if key and isinstance(display.get(key), dict):
            item["delta"] = display[key]
    overall_key = f"@overall:{section_id}"
    if isinstance(display.get(overall_key), dict):
        data["section"]["overall_delta"] = display[overall_key]
    return data


def stat_notifications_enabled(conn: sqlite3.Connection, user_id: int, actor_id: str) -> bool:
    explicit = runtime_value(conn, f"{STAT_PREF_PREFIX}{user_id}:{actor_id}", None)
    if explicit is not None:
        return bool(explicit)
    return actor_id == runtime_value(conn, "default_actor_id", None)


def _baseline_key(user_id: int, actor_id: str) -> str:
    return f"{STAT_BASELINE_PREFIX}{user_id}:{actor_id}"


def _serialize_snapshot(snapshot: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {key: _ref(value) for key, value in snapshot.items()}


def reset_stat_notification_baseline(
    conn: sqlite3.Connection,
    user_id: int,
    actor_id: str,
    snapshot: dict[str, dict[str, Any]] | None = None,
) -> None:
    current = snapshot if snapshot is not None else capture_profile_change_state(conn, actor_id)
    set_runtime_value(conn, _baseline_key(user_id, actor_id), _serialize_snapshot(current))


def set_stat_notifications(conn: sqlite3.Connection, user_id: int, actor_id: str, enabled: bool) -> bool:
    set_runtime_value(conn, f"{STAT_PREF_PREFIX}{user_id}:{actor_id}", bool(enabled))
    reset_stat_notification_baseline(conn, user_id, actor_id)
    conn.commit()
    return bool(enabled)


def reset_all_stat_notification_baselines(conn: sqlite3.Connection, user_id: int) -> None:
    rows = conn.execute(
        "SELECT entity_id FROM character_profiles WHERE status='active' ORDER BY entity_id"
    ).fetchall()
    for row in rows:
        reset_stat_notification_baseline(conn, user_id, str(row["entity_id"]))
    conn.commit()


def pending_stat_notification_changes(
    conn: sqlite3.Connection,
    user_id: int,
    actor_id: str,
    before: dict[str, dict[str, Any]],
    current: dict[str, dict[str, Any]],
    *,
    sim_time: str,
) -> list[dict[str, Any]]:
    if not before and not current:
        return []
    stored = runtime_value(conn, _baseline_key(user_id, actor_id), None)
    baselines = dict(stored) if isinstance(stored, dict) else _serialize_snapshot(before or current)
    if not isinstance(stored, dict):
        set_runtime_value(conn, _baseline_key(user_id, actor_id), baselines)
        conn.commit()

    changes: list[dict[str, Any]] = []
    for field_key, entry in current.items():
        baseline = baselines.get(field_key)
        if not isinstance(baseline, dict):
            baseline = _ref(before.get(field_key) or entry)
            baselines[field_key] = baseline
        if _meaningful(field_key, baseline, entry):
            changes.append(_change_payload(field_key, baseline, entry, sim_time))
    return changes


def mark_stat_notification_sent(
    conn: sqlite3.Connection,
    user_id: int,
    actor_id: str,
    current: dict[str, dict[str, Any]],
    changes: list[dict[str, Any]],
) -> None:
    stored = runtime_value(conn, _baseline_key(user_id, actor_id), {})
    baselines = dict(stored) if isinstance(stored, dict) else {}
    for change in changes:
        field_key = str(change.get("key") or "")
        if field_key and field_key in current:
            baselines[field_key] = _ref(current[field_key])
    set_runtime_value(conn, _baseline_key(user_id, actor_id), baselines)
    conn.commit()

from __future__ import annotations

import sqlite3
from typing import Any

from .creation_sandbox import get_sandbox_object


def _title(value: Any) -> str:
    return str(value).replace("_", " ").replace("-", " ").strip().title()


def _resolve_ref(conn: sqlite3.Connection, value: Any) -> str | None:
    if value is None:
        return "—"
    if not isinstance(value, str):
        return None
    try:
        obj = get_sandbox_object(conn, value)
    except Exception:
        return None
    identity = obj.get("identity") or {}
    name = str(identity.get("name") or "").strip()
    creation_type = str(obj.get("creation_type") or "").strip().title()
    if name and creation_type:
        return f"{name} ({creation_type})"
    return name or None


def _human(conn: sqlite3.Connection, value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, bool):
        return "Enabled" if value else "Disabled"
    resolved = _resolve_ref(conn, value)
    if resolved is not None:
        return resolved
    if isinstance(value, str):
        return _title(value) if value.islower() else value
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:g}" if isinstance(value, float) else str(value)
    if isinstance(value, list):
        if not value:
            return "None"
        if all(not isinstance(item, (dict, list)) for item in value):
            return ", ".join(_human(conn, item) for item in value)
        return f"{len(value)} represented entr{'y' if len(value) == 1 else 'ies'}"
    if isinstance(value, dict):
        if {"kind", "value", "unit"} <= set(value):
            number = value.get("value")
            unit = str(value.get("unit") or "").replace("m2", "m²").replace("m3", "m³")
            if isinstance(number, (int, float)) and not isinstance(number, bool):
                return f"{float(number):g} {unit}".strip()
        parts = []
        for key, item in value.items():
            parts.append(f"{_title(key)}: {_human(conn, item)}")
        return "; ".join(parts) if parts else "None"
    return str(value)


def _field_labels(location_edit_module: Any) -> dict[tuple[str, ...], str]:
    labels: dict[tuple[str, ...], str] = {}
    for spec in getattr(location_edit_module, "_FIELD_SPECS", {}).values():
        path = tuple(str(part) for part in (spec.get("path") or ()))
        label = str(spec.get("label") or "").strip()
        if path and label:
            labels[path] = label
    return labels


def _label_for(path: tuple[str, ...], labels: dict[tuple[str, ...], str]) -> str:
    if path in labels:
        return labels[path]
    for length in range(len(path) - 1, 0, -1):
        prefix = path[:length]
        if prefix in labels:
            suffix = " · ".join(_title(part) for part in path[length:])
            return f"{labels[prefix]} · {suffix}" if suffix else labels[prefix]
    return " · ".join(_title(part) for part in path[1:] or path)


def _diff_values(
    current: Any,
    proposed: Any,
    *,
    path: tuple[str, ...],
    labels: dict[tuple[str, ...], str],
) -> list[tuple[str, Any, Any]]:
    if current == proposed:
        return []
    if isinstance(current, dict) and isinstance(proposed, dict):
        rows: list[tuple[str, Any, Any]] = []
        keys = list(dict.fromkeys([*current.keys(), *proposed.keys()]))
        for key in keys:
            rows.extend(
                _diff_values(
                    current.get(key),
                    proposed.get(key),
                    path=(*path, str(key)),
                    labels=labels,
                )
            )
        return rows
    return [(_label_for(path, labels), current, proposed)]


def _interface_name(value: dict[str, Any], fallback: str) -> str:
    return str(value.get("name") or value.get("key") or fallback)


def _topology_diff(conn: sqlite3.Connection, current: Any, proposed: Any) -> list[str]:
    before = list((current or {}).get("interfaces") or []) if isinstance(current, dict) else []
    after = list((proposed or {}).get("interfaces") or []) if isinstance(proposed, dict) else []
    before_by_key = {str(item.get("key")): item for item in before if isinstance(item, dict) and item.get("key")}
    after_by_key = {str(item.get("key")): item for item in after if isinstance(item, dict) and item.get("key")}
    lines: list[str] = []
    for key, item in before_by_key.items():
        if key not in after_by_key:
            lines.append(f"• Interface removed: {_interface_name(item, key)}")
    for key, item in after_by_key.items():
        if key not in before_by_key:
            lines.append(f"• Interface added: {_interface_name(item, key)}")
            continue
        old = before_by_key[key]
        for field in ("name", "kind", "destination_ref", "directionality", "enabled", "traversal_modes", "base_duration_minutes", "distance"):
            if old.get(field) != item.get(field):
                lines.append(
                    f"• {_interface_name(item, key)} · {_title(field)}: "
                    f"{_human(conn, old.get(field))} → {_human(conn, item.get(field))}"
                )
    if not lines and before != after:
        lines.append(f"• Interfaces: {_human(conn, before)} → {_human(conn, after)}")
    return lines


def human_location_edit_preview_view(location_edit_module: Any, conn: sqlite3.Connection, *, user_id: int):
    session = location_edit_module.get_sandbox_location_edit_session(user_id=user_id)
    if session is None or not isinstance(session.get("pending_source"), dict):
        raise location_edit_module.SandboxLocationEditError("No Location edit proposal is ready for Preview")

    section = str(session["pending_section"])
    location = location_edit_module.get_sandbox_location_v2(conn, str(session["object_id"]))
    current = location["source"].get(section)
    proposed = session["pending_source"].get(section)

    if section == "topology":
        change_lines = _topology_diff(conn, current, proposed)
    else:
        labels = _field_labels(location_edit_module)
        rows = _diff_values(current, proposed, path=(section,), labels=labels)
        change_lines = [
            f"• {label}: {_human(conn, before)} → {_human(conn, after)}"
            for label, before, after in rows
        ]

    if not change_lines:
        change_lines = ["• No effective field change detected."]

    section_label = getattr(location_edit_module, "_SECTION_LABELS", {}).get(section, _title(section))
    text = (
        "📋 LOCATION EDIT PREVIEW\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"Location: {location['source']['identity']['name']}\n"
        f"Section: {section_label}\n\n"
        "CHANGES\n"
        + "\n".join(change_lines)
        + "\n\n✅ Exact location-v2 + same-Sandbox graph preflight passed.\n"
        "Nothing has changed yet. Apply Edit to save this proposal."
    )
    return text, [
        [{"text": "✅ Apply Edit", "callback_data": "sw:ledit:apply"}],
        [{"text": "← Edit Section", "callback_data": f"sw:ledit:s:{section}"}],
        [{"text": "✕ Discard Proposal", "callback_data": "sw:ledit:discard"}],
    ]


def install_location_edit_preview_renderer(location_edit_module: Any) -> None:
    if getattr(location_edit_module, "_human_preview_renderer_installed", False):
        return

    def preview(conn: sqlite3.Connection, *, user_id: int):
        return human_location_edit_preview_view(location_edit_module, conn, user_id=user_id)

    location_edit_module.location_edit_preview_view = preview
    location_edit_module._human_preview_renderer_installed = True


__all__ = ["human_location_edit_preview_view", "install_location_edit_preview_renderer"]

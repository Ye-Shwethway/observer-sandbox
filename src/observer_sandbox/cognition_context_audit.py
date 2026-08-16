from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from .ai_runtime import _decision_prompt
from .cognition_context_snapshots import cognition_context_snapshots
from .db import connect, migrate


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _rough_tokens(characters: int) -> int:
    """Model-neutral planning estimate only; provider tokenizers may differ."""
    return math.ceil(max(0, characters) / 4)


def _size(value: Any) -> dict[str, int]:
    text = _json(value)
    return {
        "characters": len(text),
        "utf8_bytes": len(text.encode("utf-8")),
        "rough_estimated_tokens": _rough_tokens(len(text)),
    }


def _entry_size(key: str, value: Any) -> dict[str, int]:
    text = f"{json.dumps(key, ensure_ascii=False)}: {_json(value)}"
    return {
        "characters": len(text),
        "utf8_bytes": len(text.encode("utf-8")),
        "rough_estimated_tokens": _rough_tokens(len(text)),
    }


def _nested_breakdown(value: Any) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    if isinstance(value, dict):
        for key, child in value.items():
            row = {"name": str(key), **_entry_size(str(key), child)}
            if isinstance(child, list):
                row["items"] = len(child)
            elif isinstance(child, dict):
                row["items"] = len(child)
            rows.append(row)
    elif isinstance(value, list) and value and all(isinstance(item, dict) for item in value):
        aggregate: dict[str, dict[str, int]] = {}
        for item in value:
            assert isinstance(item, dict)
            for key, child in item.items():
                size = _entry_size(str(key), child)
                bucket = aggregate.setdefault(
                    str(key),
                    {"characters": 0, "utf8_bytes": 0, "rough_estimated_tokens": 0, "occurrences": 0},
                )
                bucket["characters"] += size["characters"]
                bucket["utf8_bytes"] += size["utf8_bytes"]
                bucket["rough_estimated_tokens"] += size["rough_estimated_tokens"]
                bucket["occurrences"] += 1
        rows = [{"name": key, **values} for key, values in aggregate.items()]
    return sorted(rows, key=lambda row: int(row["characters"]), reverse=True)


def audit_snapshot(snapshot: dict[str, Any]) -> dict[str, Any]:
    context = snapshot.get("context") if isinstance(snapshot.get("context"), dict) else {}
    available_actions = snapshot.get("available_actions") if isinstance(snapshot.get("available_actions"), list) else []

    context_text = _json(context)
    action_text = _json(available_actions)
    prompt_text = _decision_prompt(context, [str(item) for item in available_actions])

    section_rows: list[dict[str, Any]] = []
    section_character_total = 0
    for key, value in context.items():
        size = _entry_size(str(key), value)
        section_character_total += size["characters"]
        row: dict[str, Any] = {"name": str(key), **size}
        if isinstance(value, (dict, list)):
            row["items"] = len(value)
            nested = _nested_breakdown(value)
            if nested:
                row["largest_children"] = nested[:12]
        section_rows.append(row)

    for row in section_rows:
        row["share_of_section_characters_pct"] = round(
            (100.0 * int(row["characters"]) / section_character_total) if section_character_total else 0.0,
            2,
        )
    section_rows.sort(key=lambda row: int(row["characters"]), reverse=True)

    context_size = {
        "characters": len(context_text),
        "utf8_bytes": len(context_text.encode("utf-8")),
        "rough_estimated_tokens": _rough_tokens(len(context_text)),
    }
    prompt_size = {
        "characters": len(prompt_text),
        "utf8_bytes": len(prompt_text.encode("utf-8")),
        "rough_estimated_tokens": _rough_tokens(len(prompt_text)),
    }
    action_size = {
        "characters": len(action_text),
        "utf8_bytes": len(action_text.encode("utf-8")),
        "rough_estimated_tokens": _rough_tokens(len(action_text)),
    }

    return {
        "ok": True,
        "character_id": snapshot.get("character_id"),
        "captured_at": snapshot.get("captured_at"),
        "sim_time": snapshot.get("sim_time"),
        "injection_type": snapshot.get("injection_type"),
        "configured_provider_id": snapshot.get("provider_id"),
        "configured_model_id": snapshot.get("model_id"),
        "measurement_note": (
            "Character/byte counts are exact for the persisted JSON snapshot and reconstructed decision prompt. "
            "rough_estimated_tokens uses characters/4 only for model-neutral planning; provider tokenizers and billed tokens may differ."
        ),
        "full_prompt": prompt_size,
        "runtime_context": context_size,
        "available_action_vocabulary": {**action_size, "items": len(available_actions)},
        "prompt_non_context_characters": max(0, len(prompt_text) - len(context_text) - len(action_text)),
        "sections": section_rows,
    }


def audit_cognition_context(conn, character_id: str, *, slot: int = 1) -> dict[str, Any]:
    slot = max(1, min(3, int(slot)))
    snapshots = cognition_context_snapshots(conn, character_id)
    if slot > len(snapshots):
        return {
            "ok": False,
            "character_id": character_id,
            "slot": slot,
            "reason": "no_captured_model_injection",
        }
    snapshot = dict(snapshots[slot - 1])
    snapshot["character_id"] = character_id
    result = audit_snapshot(snapshot)
    result["slot"] = slot
    return result


def main() -> None:
    parser = argparse.ArgumentParser(prog="python -m observer_sandbox.cognition_context_audit")
    parser.add_argument("--db", type=Path, required=True)
    parser.add_argument("--character", required=True)
    parser.add_argument("--slot", type=int, default=1)
    args = parser.parse_args()

    with connect(args.db) as conn:
        migrate(conn)
        result = audit_cognition_context(conn, args.character, slot=args.slot)
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()

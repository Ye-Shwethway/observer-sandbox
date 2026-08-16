from __future__ import annotations

import json

from observer_sandbox.cognition_context_audit import audit_cognition_context, audit_snapshot
from observer_sandbox.cognition_context_snapshots import record_cognition_context_snapshot
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize


ACTOR = "char_darian"


def test_audit_ranks_sections_and_reports_prompt_size_without_raw_values():
    snapshot = {
        "captured_at": "2026-08-16T00:00:00+00:00",
        "sim_time": "2025-05-07T12:00:00+00:00",
        "injection_type": "primary",
        "provider_id": "gemini",
        "model_id": "test-model",
        "available_actions": ["idle", "move"],
        "context": {
            "sim_time": "2025-05-07T12:00:00+00:00",
            "small": {"value": 1},
            "large": {"description": "x" * 4000, "other": "y" * 1000},
            "action_options": [
                {"action": "idle", "target": None, "guidance": "z" * 500},
                {"action": "move", "target": "loc_test", "guidance": "z" * 500},
            ],
        },
    }

    result = audit_snapshot(snapshot)

    assert result["ok"] is True
    assert result["full_prompt"]["characters"] > result["runtime_context"]["characters"]
    assert result["full_prompt"]["rough_estimated_tokens"] > 0
    assert result["sections"][0]["name"] == "large"
    action_options = next(row for row in result["sections"] if row["name"] == "action_options")
    assert action_options["items"] == 2
    assert action_options["largest_children"][0]["name"] == "guidance"
    serialized = json.dumps(result)
    assert "xxxx" not in serialized
    assert "zzzz" not in serialized


def test_persisted_snapshot_audit_is_read_only_and_uses_selected_slot(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        record_cognition_context_snapshot(
            conn,
            character_id=ACTOR,
            role="cognition",
            injection_type="primary",
            provider_id="gemini",
            model_id="test-model",
            available_actions=["idle"],
            context={"sim_time": "2025-05-07T12:00:00+00:00", "marker": "older"},
        )
        record_cognition_context_snapshot(
            conn,
            character_id=ACTOR,
            role="cognition",
            injection_type="corrective_retry",
            provider_id="groq",
            model_id="fallback-model",
            available_actions=["idle"],
            context={"sim_time": "2025-05-07T12:01:00+00:00", "marker": "newer"},
        )
        conn.commit()
        before = conn.total_changes
        result = audit_cognition_context(conn, ACTOR, slot=1)
        after = conn.total_changes

    assert result["ok"] is True
    assert result["slot"] == 1
    assert result["injection_type"] == "corrective_retry"
    assert result["configured_provider_id"] == "groq"
    assert result["configured_model_id"] == "fallback-model"
    assert result["runtime_context"]["characters"] > 0
    assert after == before


def test_audit_reports_missing_snapshot_without_mutation(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = conn.total_changes
        result = audit_cognition_context(conn, ACTOR, slot=1)
        after = conn.total_changes

    assert result == {
        "ok": False,
        "character_id": ACTOR,
        "slot": 1,
        "reason": "no_captured_model_injection",
    }
    assert after == before

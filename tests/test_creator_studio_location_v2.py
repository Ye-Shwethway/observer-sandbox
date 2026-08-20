from __future__ import annotations

import json
from copy import deepcopy

import pytest

from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_draft_export import render_full_draft_text
from observer_sandbox.creator_studio import CreatorStudioError, active_draft, cancel_draft
from observer_sandbox.creator_studio_location import (
    approve_location_draft,
    manual_location_draft,
    manual_location_template,
)
from observer_sandbox.db import connect
from observer_sandbox.location_creation_schema_v2 import validate_location_payload_v2
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_studio import draft_preview_view, studio_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if button.get("callback_data")
    }


def _location_count(conn) -> int:
    return int(conn.execute("SELECT COUNT(*) FROM creation_sandbox_location_profiles").fetchone()[0])


def test_manual_location_template_is_exact_v2_source_and_has_no_authored_derived() -> None:
    template = manual_location_template()
    result = validate_location_payload_v2(template)
    assert template["schema_version"] == "location-v2"
    assert "derived" not in template
    assert result["derived"]["completeness_level"] == "L0"


def test_manual_location_rejects_invalid_json_and_authored_derived_without_materialization(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        with pytest.raises(CreatorStudioError, match="Location JSON is invalid"):
            manual_location_draft(conn, 7, "{")
        assert active_draft(conn, 7) is None
        assert _location_count(conn) == 0

        bad = manual_location_template()
        bad["derived"] = {"completeness_level": "L4"}
        with pytest.raises(CreatorStudioError, match="unknown field"):
            manual_location_draft(conn, 7, json.dumps(bad))
        assert active_draft(conn, 7) is None
        assert _location_count(conn) == 0


def test_manual_location_draft_preview_and_export_are_write_free(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        draft = manual_location_draft(conn, 11, json.dumps(manual_location_template()))
        stored = draft["proposal"]["properties"]["location_payload"]

        assert draft["creation_type"] == "location"
        assert draft["proposal"]["schema_version"] == 2
        assert stored["schema_version"] == "location-v2"
        assert "derived" not in stored
        assert _location_count(conn) == 0

        text, keyboard = draft_preview_view(conn, 11)
        assert "LOCATION SANDBOX DRAFT" in text
        assert "Exact location-v2 source validation passed" in text
        assert "sw:cs:export" in _callbacks(keyboard)
        assert "sw:cs:approve" in _callbacks(keyboard)
        assert _location_count(conn) == 0

        filename, exported = render_full_draft_text(conn, 11)
        assert filename == "creator-studio-location-example-room-r1.txt"
        assert "location_payload" in exported
        assert "location-v2" in exported
        assert _location_count(conn) == 0
        assert canonical_state_fingerprint(conn) == before


def test_stale_location_approval_is_rejected_and_cancel_is_zero_write(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        draft = manual_location_draft(conn, 13, json.dumps(manual_location_template()))
        with pytest.raises(CreatorStudioError, match="Draft changed"):
            approve_location_draft(conn, 13, int(draft["revision"]) + 1)
        assert _location_count(conn) == 0
        assert active_draft(conn, 13) is not None

        assert cancel_draft(conn, 13) is True
        assert active_draft(conn, 13) is None
        assert _location_count(conn) == 0


def test_location_approval_revalidates_graph_and_keeps_failed_draft(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    value = manual_location_template()
    value["identity"]["key"] = "place.child.missing_parent"
    value["identity"]["name"] = "Missing Parent Room"
    value["structure"]["parent_ref"] = "sbx_location_missing"

    with connect(db) as conn:
        draft = manual_location_draft(conn, 17, json.dumps(value))
        with pytest.raises(CreatorStudioError, match="same Sandbox"):
            approve_location_draft(conn, 17, draft["revision"])
        assert active_draft(conn, 17) is not None
        assert _location_count(conn) == 0
        assert conn.execute(
            "SELECT COUNT(*) FROM creation_sandbox_objects WHERE creation_type='location'"
        ).fetchone()[0] == 0


def test_location_telegram_revision_confirmation_materializes_via_v2_only(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)

        method_text, method_keyboard = studio_callback_view(conn, 23, "sw:cs:type:location")
        assert "CREATE LOCATION" in method_text
        assert "sw:cs:input:location:manual" in _callbacks(method_keyboard)
        assert "sw:cs:input:location:ai" not in _callbacks(method_keyboard)

        prompt_text, _ = studio_callback_view(conn, 23, "sw:cs:input:location:manual")
        assert "LOCATION · EXACT JSON" in prompt_text
        session = conn.execute(
            "SELECT creation_type,input_mode,expected_input FROM creation_sandbox_studio_sessions WHERE sandbox_id='creator-default' AND user_id=?",
            (23,),
        ).fetchone()
        assert dict(session) == {
            "creation_type": "location",
            "input_mode": "manual",
            "expected_input": "location-json",
        }

        draft = manual_location_draft(conn, 23, json.dumps(manual_location_template()))
        assert _location_count(conn) == 0

        confirm_text, confirm_keyboard = studio_callback_view(conn, 23, "sw:cs:approve")
        confirm = f"sw:cs:approve:confirm:{draft['revision']}"
        assert confirm in _callbacks(confirm_keyboard)
        assert "approval" in confirm_text.lower()
        assert _location_count(conn) == 0

        approved_text, _ = studio_callback_view(conn, 23, confirm)
        assert "SANDBOX LOCATION APPROVED" in approved_text
        assert "Example Room" in approved_text
        assert active_draft(conn, 23) is None
        assert _location_count(conn) == 1
        row = conn.execute(
            "SELECT object_id,schema_version,source_json FROM creation_sandbox_location_profiles"
        ).fetchone()
        assert row["schema_version"] == "location-v2"
        source = json.loads(row["source_json"])
        assert source["identity"]["name"] == "Example Room"
        assert "derived" not in source
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_actor_runtime WHERE object_id=?",
            (row["object_id"],),
        ).fetchone() is None
        assert canonical_state_fingerprint(conn) == before

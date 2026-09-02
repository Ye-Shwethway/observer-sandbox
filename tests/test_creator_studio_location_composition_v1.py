from __future__ import annotations

import json

import pytest

from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_draft_export import render_full_draft_text
from observer_sandbox.creator_studio import CreatorStudioError, active_draft
from observer_sandbox.creator_studio_location_composition import (
    approve_location_composition_draft,
    location_composition_template,
    manual_location_composition_draft,
    preview_location_composition_draft,
    start_location_composition_draft,
)
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_studio import draft_preview_view, studio_callback_view


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard
        for button in row
        if button.get("callback_data")
    }


def _counts(conn):
    return {
        "objects": conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0],
        "locations": conn.execute("SELECT COUNT(*) FROM creation_sandbox_location_profiles").fetchone()[0],
        "items": conn.execute("SELECT COUNT(*) FROM creation_sandbox_item_instances").fetchone()[0],
        "relations": conn.execute("SELECT COUNT(*) FROM creation_sandbox_relations").fetchone()[0],
    }


def test_location_composition_starter_is_exact_previewable_and_write_free(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before_real = canonical_state_fingerprint(conn)
        before = _counts(conn)
        draft = start_location_composition_draft(conn, 71)
        preview = preview_location_composition_draft(conn, 71)

        assert draft["creation_type"] == "location"
        assert draft["draft_mode"] == "manual"
        assert draft["revision"] == 1
        assert draft["proposal"]["schema_version"] == 2
        assert draft["proposal"]["properties"]["location_composition"]["schema_version"] == "location-composition-v1"
        assert preview["count"] == 3
        assert [entry["ref"] for entry in preview["locations"]] == ["property", "room"]
        assert preview["locations"][1]["source"]["structure"]["parent_ref"] == "$property"
        assert preview["items"][0]["resolved_relationships"] == [
            {"relation_type": "located_at", "target_kind": "location", "target": "room"}
        ]
        assert _counts(conn) == before
        assert canonical_state_fingerprint(conn) == before_real


def test_location_composition_telegram_method_preview_and_export(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before_real = canonical_state_fingerprint(conn)
        method_text, method_keyboard = studio_callback_view(conn, 73, "sw:cs:type:location")
        callbacks = _callbacks(method_keyboard)
        assert "Nested Composition" in method_text
        assert "sw:cs:location:composition:starter" in callbacks
        assert "sw:cs:location:composition:json" in callbacks

        text, keyboard = studio_callback_view(conn, 73, "sw:cs:location:composition:starter")
        assert "LOCATION COMPOSITION DRAFT" in text
        assert "Locations: 2" in text
        assert "Items: 1" in text
        assert "$property" in text
        assert "$room" in text
        assert "sw:cs:export" in _callbacks(keyboard)
        assert "sw:cs:approve" in _callbacks(keyboard)
        assert _counts(conn)["objects"] == 0

        filename, exported = render_full_draft_text(conn, 73)
        assert filename.endswith("-r1.txt")
        assert "location_composition" in exported
        assert "location-composition-v1" in exported
        assert "place.creator.composition_test_property.room" in exported
        assert _counts(conn)["objects"] == 0
        assert canonical_state_fingerprint(conn) == before_real


def test_location_composition_exact_json_replacement_increments_revision_and_stale_guard(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        first = start_location_composition_draft(conn, 75)
        candidate = location_composition_template()
        candidate["locations"][0]["payload"]["identity"]["name"] = "Revised Composition Property"
        second = manual_location_composition_draft(conn, 75, json.dumps(candidate))
        assert first["revision"] == 1
        assert second["revision"] == 2

        with pytest.raises(CreatorStudioError, match="Draft changed after confirmation"):
            approve_location_composition_draft(conn, 75, 1)
        assert _counts(conn)["objects"] == 0

        current = active_draft(conn, 75)
        assert current is not None
        assert current["revision"] == 2
        assert current["proposal"]["properties"]["location_composition"]["locations"][0]["payload"]["identity"]["name"] == "Revised Composition Property"


def test_location_composition_telegram_revision_bound_approval_materializes_whole_graph(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before_real = canonical_state_fingerprint(conn)
        studio_callback_view(conn, 77, "sw:cs:location:composition:starter")

        confirmation, keyboard = studio_callback_view(conn, 77, "sw:cs:approve")
        assert "CONFIRM COMPOSITION APPROVAL" in confirmation
        assert "Total members: 3" in confirmation
        assert "sw:cs:approve:confirm:1" in _callbacks(keyboard)
        assert _counts(conn)["objects"] == 0

        approved, approved_keyboard = studio_callback_view(conn, 77, "sw:cs:approve:confirm:1")
        assert "SANDBOX COMPOSITION APPROVED" in approved
        assert "Locations: 2" in approved
        assert "Items: 1" in approved
        assert active_draft(conn, 77) is None
        assert "nav:sandbox" in _callbacks(approved_keyboard)

        counts = _counts(conn)
        assert counts["objects"] == 3
        assert counts["locations"] == 2
        assert counts["items"] == 1

        root = conn.execute(
            "SELECT object_id FROM creation_sandbox_location_profiles WHERE location_key='place.creator.composition_test_property'"
        ).fetchone()[0]
        room = conn.execute(
            "SELECT object_id FROM creation_sandbox_location_profiles WHERE location_key='place.creator.composition_test_property.room'"
        ).fetchone()[0]
        item = conn.execute(
            "SELECT object_id FROM creation_sandbox_item_instances WHERE definition_key='item.creator.composition_test_bottle'"
        ).fetchone()[0]
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='contains' AND target_object_id=?",
            (root, room),
        ).fetchone() is not None
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='located_at' AND target_object_id=?",
            (item, room),
        ).fetchone() is not None
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_actor_runtime WHERE object_id IN (?,?,?) LIMIT 1",
            (root, room, item),
        ).fetchone() is None
        assert canonical_state_fingerprint(conn) == before_real


def test_invalid_composition_json_never_replaces_valid_draft_or_materializes(tmp_path) -> None:
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        start_location_composition_draft(conn, 79)
        before = _counts(conn)
        with pytest.raises(CreatorStudioError, match="unknown local target"):
            bad = location_composition_template()
            bad["items"][0]["payload"]["relationships"]["located_at"] = "$missing"
            manual_location_composition_draft(conn, 79, json.dumps(bad))
        current = active_draft(conn, 79)
        assert current is not None and current["revision"] == 1
        assert _counts(conn) == before

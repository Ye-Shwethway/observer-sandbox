from __future__ import annotations

import copy

import pytest

import observer_sandbox.sandbox_location_composition as composition
from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.creator_studio_item import manual_item_template
from observer_sandbox.creator_studio_location import manual_location_template
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_location_composition import (
    SandboxLocationCompositionError,
    materialize_location_composition,
    preview_location_composition,
)


def _location(ref: str, *, name: str, key: str, kind: str = "room", parent_ref=None):
    payload = manual_location_template()
    payload["identity"]["key"] = key
    payload["identity"]["name"] = name
    payload["identity"]["kind"] = kind
    payload["identity"]["description"] = f"{name} composition test location."
    payload["structure"]["parent_ref"] = parent_ref
    payload["structure"]["exposure"] = "mixed" if kind == "property" else "indoor"
    return {"ref": ref, "payload": payload}


def _item(ref: str, *, name: str, key: str, located_at=None, stored_in=None):
    payload = manual_item_template()
    payload["definition"]["key"] = key
    payload["definition"]["name"] = name
    payload["definition"]["description"] = f"{name} composition test Item."
    payload["relationships"]["located_at"] = located_at
    payload["relationships"]["stored_in"] = stored_in
    return {"ref": ref, "payload": payload}


def _container(ref: str, *, name: str, key: str, located_at=None):
    member = _item(ref, name=name, key=key, located_at=located_at)
    payload = member["payload"]
    payload["definition"]["capabilities"] = sorted(set(payload["definition"]["capabilities"] + ["store"]))
    payload["definition"]["modules"]["container"] = {
        "capacity_volume": {"value": 20, "unit": "l"}
    }
    return member


def _envelope(*, locations, items=None):
    return {
        "schema_version": "location-composition-v1",
        "locations": locations,
        "items": items or [],
    }


def _sandbox_counts(conn):
    return {
        "objects": conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0],
        "locations": conn.execute("SELECT COUNT(*) FROM creation_sandbox_location_profiles").fetchone()[0],
        "items": conn.execute("SELECT COUNT(*) FROM creation_sandbox_item_instances").fetchone()[0],
        "relations": conn.execute("SELECT COUNT(*) FROM creation_sandbox_relations").fetchone()[0],
    }


def test_preview_property_room_item_graph_is_write_free(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    envelope = _envelope(
        locations=[
            _location("estate", name="Test Estate", key="place.test.estate", kind="property"),
            _location("study", name="Study", key="place.test.estate.study", parent_ref="$estate"),
        ],
        items=[_item("lamp", name="Study Lamp", key="item.test.study_lamp", located_at="$study")],
    )

    with connect(db) as conn:
        before_real = canonical_state_fingerprint(conn)
        before = _sandbox_counts(conn)
        preview = preview_location_composition(conn, envelope)
        assert preview["schema_version"] == "location-composition-v1"
        assert preview["count"] == 3
        assert [entry["ref"] for entry in preview["locations"]] == ["estate", "study"]
        assert preview["items"][0]["resolved_relationships"] == [
            {"relation_type": "located_at", "target_kind": "location", "target": "study"}
        ]
        assert _sandbox_counts(conn) == before
        assert canonical_state_fingerprint(conn) == before_real


def test_materialize_property_room_item_graph_resolves_local_refs_atomically(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    envelope = _envelope(
        locations=[
            _location("estate", name="Test Estate", key="place.test.estate", kind="property"),
            _location("study", name="Study", key="place.test.estate.study", parent_ref="$estate"),
        ],
        items=[_item("lamp", name="Study Lamp", key="item.test.study_lamp", located_at="$study")],
    )

    with connect(db) as conn:
        before_real = canonical_state_fingerprint(conn)
        created = materialize_location_composition(conn, envelope, requested_by="test")
        refs = created["refs"]
        assert set(refs) == {"estate", "study", "lamp"}
        assert len(created["locations"]) == 2
        assert len(created["items"]) == 1

        study = next(value for value in created["locations"] if value["location_key"] == "place.test.estate.study")
        assert study["source"]["structure"]["parent_ref"] == refs["estate"]
        contains = conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='contains' AND target_object_id=?",
            (refs["estate"], refs["study"]),
        ).fetchone()
        assert contains is not None
        located = conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='located_at' AND target_object_id=?",
            (refs["lamp"], refs["study"]),
        ).fetchone()
        assert located is not None
        assert conn.execute(
            "SELECT 1 FROM creation_sandbox_actor_runtime WHERE object_id IN (?,?,?) LIMIT 1",
            (refs["estate"], refs["study"], refs["lamp"]),
        ).fetchone() is None
        assert canonical_state_fingerprint(conn) == before_real


def test_local_topology_is_resolved_to_created_location_ids(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    room_a = _location("room_a", name="Room A", key="place.test.room_a", kind="property")
    room_b = _location("room_b", name="Room B", key="place.test.room_b", kind="property")
    room_a["payload"]["topology"]["interfaces"] = [{
        "key": "door_b",
        "name": "Door to B",
        "kind": "door",
        "destination_ref": "$room_b",
        "directionality": "two_way",
        "enabled": True,
        "traversal_modes": ["walk"],
        "base_duration_minutes": 1,
        "distance": None,
    }]
    envelope = _envelope(locations=[room_a, room_b])

    with connect(db) as conn:
        created = materialize_location_composition(conn, envelope)
        refs = created["refs"]
        a = next(value for value in created["locations"] if value["location_key"] == "place.test.room_a")
        assert a["source"]["topology"]["interfaces"][0]["destination_ref"] == refs["room_b"]
        forward = conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='connected_to' AND target_object_id=?",
            (refs["room_a"], refs["room_b"]),
        ).fetchone()
        reverse = conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='connected_to' AND target_object_id=?",
            (refs["room_b"], refs["room_a"]),
        ).fetchone()
        assert forward is not None and reverse is not None


def test_item_can_be_stored_in_local_container_item(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    envelope = _envelope(
        locations=[_location("room", name="Storage Room", key="place.test.storage", kind="property")],
        items=[
            _container("box", name="Storage Box", key="item.test.storage_box", located_at="$room"),
            _item("note", name="Paper Note", key="item.test.paper_note", stored_in="$box"),
        ],
    )

    with connect(db) as conn:
        created = materialize_location_composition(conn, envelope)
        refs = created["refs"]
        stored = conn.execute(
            "SELECT 1 FROM creation_sandbox_relations WHERE source_object_id=? AND relation_type='stored_in' AND target_object_id=?",
            (refs["note"], refs["box"]),
        ).fetchone()
        assert stored is not None


def test_unknown_local_ref_and_parent_cycle_fail_before_writes(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before = _sandbox_counts(conn)
        bad_ref = _envelope(
            locations=[_location("root", name="Root", key="place.test.root", kind="property")],
            items=[_item("lamp", name="Lamp", key="item.test.lamp", located_at="$missing")],
        )
        with pytest.raises(SandboxLocationCompositionError, match="unknown local target"):
            materialize_location_composition(conn, bad_ref)
        assert _sandbox_counts(conn) == before

        cycle = _envelope(locations=[
            _location("a", name="A", key="place.test.a", kind="property", parent_ref="$b"),
            _location("b", name="B", key="place.test.b", kind="property", parent_ref="$a"),
        ])
        with pytest.raises(SandboxLocationCompositionError, match="acyclic"):
            materialize_location_composition(conn, cycle)
        assert _sandbox_counts(conn) == before


def test_mid_transaction_failure_rolls_back_all_members(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    envelope = _envelope(
        locations=[
            _location("estate", name="Rollback Estate", key="place.test.rollback", kind="property"),
            _location("room", name="Rollback Room", key="place.test.rollback.room", parent_ref="$estate"),
        ],
        items=[_item("lamp", name="Rollback Lamp", key="item.test.rollback_lamp", located_at="$room")],
    )

    with connect(db) as conn:
        before = _sandbox_counts(conn)
        before_real = canonical_state_fingerprint(conn)

        def explode(*args, **kwargs):
            raise RuntimeError("forced composition failure")

        monkeypatch.setattr(composition, "_insert_item", explode)
        with pytest.raises(RuntimeError, match="forced composition failure"):
            materialize_location_composition(conn, envelope)
        assert _sandbox_counts(conn) == before
        assert canonical_state_fingerprint(conn) == before_real

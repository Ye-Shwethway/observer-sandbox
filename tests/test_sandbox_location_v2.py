from __future__ import annotations

import json
from copy import deepcopy

import pytest

from observer_sandbox.creation_sandbox import (
    archive_sandbox_object,
    canonical_state_fingerprint,
    ensure_sandbox,
)
from observer_sandbox.creation_socket import socket_definition
from observer_sandbox.db import connect, migrate
from observer_sandbox.sandbox_location_v2 import (
    SandboxLocationV2Error,
    get_sandbox_location_v2,
    materialize_sandbox_location_v2,
)


def payload(*, key: str = "place.test", kind: str = "property", parent_ref=None):
    return {
        "schema_version": "location-v2",
        "identity": {
            "key": key,
            "name": key.replace(".", " ").title(),
            "kind": kind,
            "description": "A represented Location used by the Sandbox Location v2 materializer tests.",
            "functional_classes": [],
            "tags": [],
        },
        "structure": {"parent_ref": parent_ref, "exposure": "mixed" if kind == "property" else "indoor"},
        "geography": {
            "address_text": None,
            "locality": None,
            "region": None,
            "country_code": None,
            "position": None,
            "bounds": None,
        },
        "spatial": {
            "area": None,
            "length": None,
            "width": None,
            "height": None,
            "elevation": None,
            "terrain": None,
            "surface": "mixed" if kind == "property" else "interior_floor",
            "orientation_notes": None,
        },
        "boundary": {
            "type": "mixed" if kind == "property" else "physical",
            "enclosure": "partially_enclosed" if kind == "property" else "enclosed",
            "notes": None,
        },
        "access": {"policy": {"mode": "public"}},
        "operations": {"initial_state": "open"},
        "topology": {"interfaces": []},
        "facilities": {
            "capabilities": ["inspect"],
            "facility_types": [],
            "resource_types": [],
            "utilities": [],
        },
        "environment": {"lighting_profile": "unknown", "weather_exposure": "unknown"},
        "control": {"ownership_class": "unknown", "owner_ref": None, "operator_ref": None},
        "economic_policy": None,
        "provenance": {"source_status": "creator_authored", "source_note": None},
    }


def interface(key: str, destination: str, *, directionality: str = "two_way"):
    return {
        "key": key,
        "name": key.replace(".", " ").title(),
        "kind": "door",
        "destination_ref": destination,
        "directionality": directionality,
        "enabled": True,
        "traversal_modes": ["walk"],
        "base_duration_minutes": 0.2,
        "distance": None,
    }


def setup_conn(tmp_path):
    conn = connect(tmp_path / "location-v2.db")
    migrate(conn)
    return conn


def count_v2_locations(conn, sandbox_id="creator-default"):
    return conn.execute(
        "SELECT COUNT(*) FROM creation_sandbox_location_profiles WHERE sandbox_id=?",
        (sandbox_id,),
    ).fetchone()[0]


def test_location_socket_is_registered_at_v2():
    assert socket_definition("location").schema_version == 2


def test_root_location_materializes_without_runtime_activation_and_preserves_canonical_state(tmp_path):
    conn = setup_conn(tmp_path)
    before = canonical_state_fingerprint(conn)
    result = materialize_sandbox_location_v2(conn, payload())
    after = canonical_state_fingerprint(conn)

    assert result["schema_version"] == "location-v2"
    assert result["source"]["identity"]["key"] == "place.test"
    assert "derived" not in result["source"]
    assert result["derived"]["completeness_level"] == "L1"
    assert before == after
    assert conn.execute(
        "SELECT 1 FROM creation_sandbox_actor_runtime WHERE object_id=?",
        (result["object_id"],),
    ).fetchone() is None


def test_child_location_requires_active_same_sandbox_v2_parent_and_materializes_contains(tmp_path):
    conn = setup_conn(tmp_path)
    parent = materialize_sandbox_location_v2(conn, payload(key="place.parent"))
    child = materialize_sandbox_location_v2(
        conn,
        payload(key="place.child", kind="room", parent_ref=parent["object_id"]),
    )
    relation = conn.execute(
        """
        SELECT source_object_id,target_object_id,metadata_json
        FROM creation_sandbox_relations
        WHERE relation_type='contains' AND target_object_id=?
        """,
        (child["object_id"],),
    ).fetchone()
    assert relation is not None
    assert relation["source_object_id"] == parent["object_id"]
    assert json.loads(relation["metadata_json"])["structural"] is True

    archive_sandbox_object(conn, parent["object_id"])
    before = count_v2_locations(conn)
    with pytest.raises(SandboxLocationV2Error, match="active"):
        materialize_sandbox_location_v2(
            conn,
            payload(key="place.blocked", kind="room", parent_ref=parent["object_id"]),
        )
    assert count_v2_locations(conn) == before


def test_cross_sandbox_parent_fails_without_location_write(tmp_path):
    conn = setup_conn(tmp_path)
    ensure_sandbox(conn, "other")
    other_parent = materialize_sandbox_location_v2(conn, payload(key="place.other"), sandbox_id="other")
    before = count_v2_locations(conn)
    with pytest.raises(SandboxLocationV2Error, match="same Sandbox"):
        materialize_sandbox_location_v2(
            conn,
            payload(key="place.cross", kind="room", parent_ref=other_parent["object_id"]),
        )
    assert count_v2_locations(conn) == before


def test_interface_destination_must_be_active_same_sandbox_v2_location(tmp_path):
    conn = setup_conn(tmp_path)
    value = payload(key="place.source")
    value["topology"]["interfaces"] = [interface("door.missing", "sbx_location_missing")]
    with pytest.raises(SandboxLocationV2Error, match="same Sandbox"):
        materialize_sandbox_location_v2(conn, value)
    assert count_v2_locations(conn) == 0


def test_multiple_interfaces_preserve_full_source_and_coarse_connected_projection(tmp_path):
    conn = setup_conn(tmp_path)
    destination = materialize_sandbox_location_v2(conn, payload(key="place.destination"))
    value = payload(key="place.source")
    value["topology"]["interfaces"] = [
        interface("door.north", destination["object_id"]),
        interface("door.south", destination["object_id"]),
    ]
    source = materialize_sandbox_location_v2(conn, value)

    assert [row["key"] for row in source["source"]["topology"]["interfaces"]] == ["door.north", "door.south"]
    rows = conn.execute(
        """
        SELECT source_object_id,target_object_id,metadata_json
        FROM creation_sandbox_relations
        WHERE relation_type='connected_to'
          AND source_object_id=? AND target_object_id=?
        """,
        (source["object_id"], destination["object_id"]),
    ).fetchall()
    assert len(rows) == 1
    metadata = json.loads(rows[0]["metadata_json"])
    assert metadata["interface_keys"] == ["door.north", "door.south"]
    assert metadata["authoritative_interface_details"] == "creation_sandbox_location_profiles.source_json"


def test_inbound_interface_projects_destination_to_new_location_only(tmp_path):
    conn = setup_conn(tmp_path)
    destination = materialize_sandbox_location_v2(conn, payload(key="place.destination"))
    value = payload(key="place.inbound")
    value["topology"]["interfaces"] = [
        interface("door.in", destination["object_id"], directionality="inbound")
    ]
    source = materialize_sandbox_location_v2(conn, value)
    assert conn.execute(
        """SELECT 1 FROM creation_sandbox_relations
        WHERE relation_type='connected_to' AND source_object_id=? AND target_object_id=?""",
        (destination["object_id"], source["object_id"]),
    ).fetchone() is not None
    assert conn.execute(
        """SELECT 1 FROM creation_sandbox_relations
        WHERE relation_type='connected_to' AND source_object_id=? AND target_object_id=?""",
        (source["object_id"], destination["object_id"]),
    ).fetchone() is None


def test_duplicate_location_key_rolls_back_generic_object_insert(tmp_path):
    conn = setup_conn(tmp_path)
    materialize_sandbox_location_v2(conn, payload(key="place.duplicate"))
    object_count = conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]
    with pytest.raises(SandboxLocationV2Error, match="atomically"):
        materialize_sandbox_location_v2(conn, payload(key="place.duplicate"))
    assert count_v2_locations(conn) == 1
    assert conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0] == object_count


def test_owner_and_included_parent_refs_validate_and_remain_distinct(tmp_path):
    conn = setup_conn(tmp_path)
    owner = materialize_sandbox_location_v2(conn, payload(key="place.owner"))
    parent = materialize_sandbox_location_v2(conn, payload(key="place.asset_parent"))
    value = payload(key="place.component", kind="room", parent_ref=parent["object_id"])
    value["control"] = {
        "ownership_class": "private",
        "owner_ref": owner["object_id"],
        "operator_ref": None,
    }
    value["economic_policy"] = {
        "classification": "component",
        "currency_code": "USD",
        "market_value_minor": None,
        "replacement_value_minor": None,
        "net_worth_treatment": "included_in_parent",
        "included_in_parent_ref": parent["object_id"],
        "valuation_method": "included_in_parent",
    }
    result = materialize_sandbox_location_v2(conn, value)
    assert result["source"]["control"]["owner_ref"] == owner["object_id"]
    assert result["source"]["economic_policy"]["included_in_parent_ref"] == parent["object_id"]
    assert conn.execute(
        """SELECT 1 FROM creation_sandbox_relations
        WHERE source_object_id=? AND relation_type='owned_by' AND target_object_id=?""",
        (result["object_id"], owner["object_id"]),
    ).fetchone() is not None


def test_corrupt_existing_parent_cycle_is_rejected_before_new_writes(tmp_path):
    conn = setup_conn(tmp_path)
    first = materialize_sandbox_location_v2(conn, payload(key="place.first"))
    second = materialize_sandbox_location_v2(
        conn,
        payload(key="place.second", kind="room", parent_ref=first["object_id"]),
    )
    first_source = get_sandbox_location_v2(conn, first["object_id"])["source"]
    first_source["structure"]["parent_ref"] = second["object_id"]
    conn.execute(
        "UPDATE creation_sandbox_location_profiles SET source_json=? WHERE object_id=?",
        (json.dumps(first_source), first["object_id"]),
    )
    conn.commit()

    before = count_v2_locations(conn)
    with pytest.raises(SandboxLocationV2Error, match="cycle"):
        materialize_sandbox_location_v2(
            conn,
            payload(key="place.third", kind="room", parent_ref=first["object_id"]),
        )
    assert count_v2_locations(conn) == before

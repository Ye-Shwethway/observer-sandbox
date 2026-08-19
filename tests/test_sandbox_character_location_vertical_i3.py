import pytest

from observer_sandbox.creation_sandbox import (
    activate_creation_proposal,
    bind_sandbox_character_to_location,
    canonical_state_fingerprint,
)
from observer_sandbox.creation_socket import build_creation_proposal
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_affordances import refresh_sandbox_runtime_options
from observer_sandbox.sandbox_representation import (
    SandboxRepresentationError,
    bind_sandbox_location_parent,
    replace_sandbox_skills,
    sandbox_location_parent,
    sandbox_profile_values,
    sandbox_skills,
    set_sandbox_profile_values,
)
from observer_sandbox.sandbox_runtime import (
    bind_sandbox_character_ai,
    configure_sandbox_clock,
    sandbox_character_readiness,
)


def _add_model(conn):
    conn.execute("UPDATE ai_providers SET enabled=1 WHERE id='gemini'")
    conn.execute(
        """
        INSERT INTO ai_models(provider_id,model_id,display_name,active)
        VALUES('gemini','i3-cognition','I3 Cognition',1)
        ON CONFLICT(provider_id,model_id) DO UPDATE SET active=1
        """
    )
    conn.commit()


def _create_vertical(conn):
    estate = activate_creation_proposal(conn, build_creation_proposal("location", identity={"name": "Sandbox Estate"}, properties={"kind": "estate"}, capabilities=["observe", "walk"], requested_by="test:creator"))
    room = activate_creation_proposal(conn, build_creation_proposal("location", identity={"name": "Sandbox Study"}, properties={"kind": "room"}, capabilities=["observe", "read", "rest"], requested_by="test:creator"))
    character = activate_creation_proposal(conn, build_creation_proposal("character", identity={"name": "I3 Test Character"}, properties={"reference": "human"}, capabilities=["idle", "relax"], requested_by="test:creator"))
    bind_sandbox_location_parent(conn, room["object_id"], estate["object_id"])
    bind_sandbox_character_to_location(conn, character["object_id"], room["object_id"])
    return character, room, estate


def test_isolated_profile_and_skill_representation_tables_exist(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {"creation_sandbox_profile_values", "creation_sandbox_character_skills"} <= tables


def test_character_profile_and_skills_reuse_canonical_vocabulary_without_canonical_rows(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        character, _, _ = _create_vertical(conn)
        before = canonical_state_fingerprint(conn)
        set_sandbox_profile_values(conn, character["object_id"], {"identity.full_name": "I3 Test Character", "identity.sex": "male", "body.height_in": 72.0, "body.weight_lb": 180.0, "raps_pa.strength": 76.0})
        replace_sandbox_skills(conn, character["object_id"], [{"skill_key": "medicine", "category": "knowledge", "score": 82.0, "tier": "A"}, {"skill_key": "cooking", "category": "practical", "score": 64.0, "tier": "B"}])
        profile = {item["field_key"]: item for item in sandbox_profile_values(conn, character["object_id"])}
        assert profile["body.height_in"]["value"] == 72.0
        assert profile["body.height_in"]["unit"] == "in"
        assert profile["identity.sex"]["domain"] == "identity"
        assert [item["skill_key"] for item in sandbox_skills(conn, character["object_id"])] == ["cooking", "medicine"]
        assert conn.execute("SELECT 1 FROM character_profile_values WHERE entity_id=?", (character["object_id"],)).fetchone() is None
        assert conn.execute("SELECT 1 FROM character_skills WHERE entity_id=?", (character["object_id"],)).fetchone() is None
        assert canonical_state_fingerprint(conn) == before


def test_unknown_profile_field_fails_closed(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        character, _, _ = _create_vertical(conn)
        with pytest.raises(SandboxRepresentationError, match="Unknown profile field"):
            set_sandbox_profile_values(conn, character["object_id"], {"magic.power": 100})


def test_location_containment_is_isolated_and_cycle_safe(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _, room, estate = _create_vertical(conn)
        before = canonical_state_fingerprint(conn)
        assert sandbox_location_parent(conn, room["object_id"]) == estate["object_id"]
        with pytest.raises(SandboxRepresentationError, match="cycle"):
            bind_sandbox_location_parent(conn, estate["object_id"], room["object_id"])
        assert canonical_state_fingerprint(conn) == before


def test_represented_capabilities_drive_options_and_runtime_ready(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_model(conn)
        character, room, _ = _create_vertical(conn)
        before = canonical_state_fingerprint(conn)
        options = refresh_sandbox_runtime_options(conn, character["object_id"])
        assert [(item["action_key"], item["source_object_id"]) for item in options] == [
            ("idle", character["object_id"]), ("observe", room["object_id"]), ("read", room["object_id"]),
            ("relax", character["object_id"]), ("rest", room["object_id"]),
        ]
        bind_sandbox_character_ai(conn, character["object_id"], "gemini", "i3-cognition")
        configure_sandbox_clock(conn, "2025-05-14T09:00:00+00:00")
        ready = sandbox_character_readiness(conn, character["object_id"])
        assert ready["ready"] is True
        assert ready["activation_status"] == "runtime_ready"
        assert ready["gates"]["runtime_options_available"] is True
        assert canonical_state_fingerprint(conn) == before

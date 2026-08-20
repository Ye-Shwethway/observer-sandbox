import json

import pytest

from observer_sandbox.creator_studio import CreatorStudioError, approve_draft, manual_draft
from observer_sandbox.db import connect
from observer_sandbox.manual_character_creation import (
    ManualCharacterCreationError,
    manual_character_baseline_status,
    manual_character_draft,
    update_manual_character_collection,
    update_manual_character_field,
)
from observer_sandbox.runtime import initialize


def _conn(tmp_path):
    db = tmp_path / "manual-character.sqlite3"
    initialize(db)
    return connect(db)


def _fill_required_baseline(conn, user_id=42):
    values = {
        "identity.date_of_birth": "2001-05-12",
        "identity.sex": "male",
        "identity.gender": "man",
        "body.height_in": "74",
        "body.weight_lb": "190",
        "body.body_fat_pct": "12",
        "personality.primary_motivation": "Protect the people he cares about",
        "personality.primary_traits": '["calm","disciplined","curious"]',
        "background.origins": "Raised in a small mountain town.",
    }
    for key, raw in values.items():
        update_manual_character_field(conn, user_id, key, raw)


def test_manual_character_starts_as_structured_profile_not_name_only_shell(tmp_path):
    with _conn(tmp_path) as conn:
        draft = manual_draft(conn, 42, "character", "Rowan Hale")
        profile = draft["proposal"]["properties"]["character_profile"]

        assert profile["values"] == {"identity.full_name": "Rowan Hale"}
        assert profile["preferences"] == []
        assert profile["hobbies"] == []
        assert profile["habits"] == []
        assert profile["skills"] == []
        assert draft["proposal"]["properties"]["compatibility_tags"] == []

        status = manual_character_baseline_status(conn, 42)
        assert status["ready"] is False
        assert "identity.date_of_birth" in status["missing"]


def test_name_only_manual_character_cannot_be_approved(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        before = conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]

        with pytest.raises(CreatorStudioError, match="baseline is incomplete"):
            approve_draft(conn, 42)

        after = conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]
        assert after == before
        assert manual_character_draft(conn, 42)["proposal"]["identity"]["name"] == "Rowan Hale"


def test_manual_fields_use_shared_creation_registry_and_validation(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")

        with pytest.raises(ManualCharacterCreationError, match="not creation-owned"):
            update_manual_character_field(conn, 42, "identity.age_years", "24")

        with pytest.raises(ManualCharacterCreationError, match="plausible human creation range"):
            update_manual_character_field(conn, 42, "body.body_fat_pct", "1")

        update_manual_character_field(conn, 42, "identity.full_name", "Rowan Mercer")
        draft = manual_character_draft(conn, 42)
        assert draft["proposal"]["identity"]["name"] == "Rowan Mercer"
        assert draft["proposal"]["properties"]["character_profile"]["values"]["identity.full_name"] == "Rowan Mercer"


def test_complete_manual_character_approves_into_same_sandbox_profile_storage(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        _fill_required_baseline(conn)
        update_manual_character_field(conn, 42, "raps_pa.strength", "78")
        update_manual_character_collection(
            conn,
            42,
            "preferences",
            '[{"preference_type":"like","subject":"quiet mornings","intensity":70}]',
        )
        update_manual_character_collection(
            conn,
            42,
            "compatibility_tags",
            '["realistic-human","modern-setting"]',
        )

        status = manual_character_baseline_status(conn, 42)
        assert status["ready"] is True

        obj = approve_draft(conn, 42)
        assert obj["creation_type"] == "character"
        assert obj["identity"]["name"] == "Rowan Hale"

        profile_rows = conn.execute(
            "SELECT field_key,value_json,source FROM creation_sandbox_profile_values WHERE object_id=?",
            (obj["object_id"],),
        ).fetchall()
        values = {row["field_key"]: json.loads(row["value_json"]) for row in profile_rows}
        assert values["identity.date_of_birth"] == "2001-05-12"
        assert values["body.height_in"] == 74.0
        assert values["raps_pa.strength"] == 78.0
        assert all(row["source"] == "creator-studio-manual-profile" for row in profile_rows)

        preferences = conn.execute(
            "SELECT preference_type,subject,intensity FROM creation_sandbox_character_preferences WHERE object_id=?",
            (obj["object_id"],),
        ).fetchall()
        assert [(row["preference_type"], row["subject"], row["intensity"]) for row in preferences] == [
            ("like", "quiet mornings", 70.0)
        ]
        assert conn.execute(
            "SELECT COUNT(*) FROM entities WHERE id=?", (obj["object_id"],)
        ).fetchone()[0] == 0


def test_trained_manual_background_requires_structured_skills_before_approval(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        _fill_required_baseline(conn)
        update_manual_character_field(
            conn,
            42,
            "background.origins",
            "Professional wilderness rescue training with navigation and first aid.",
        )

        with pytest.raises(CreatorStudioError, match="structured skills are empty"):
            approve_draft(conn, 42)

        update_manual_character_collection(
            conn,
            42,
            "skills",
            '[{"skill_key":"navigation","category":null,"score":75,"tier":null,"experience":0}]',
        )
        obj = approve_draft(conn, 42)
        skills = conn.execute(
            "SELECT skill_key,score FROM creation_sandbox_character_skills WHERE object_id=?",
            (obj["object_id"],),
        ).fetchall()
        assert [(row["skill_key"], row["score"]) for row in skills] == [("navigation", 75.0)]


def test_manual_location_path_remains_lightweight_and_approvable(tmp_path):
    with _conn(tmp_path) as conn:
        draft = manual_draft(conn, 42, "location", "Test Ridge")
        assert draft["proposal"]["properties"] == {}
        obj = approve_draft(conn, 42)
        assert obj["creation_type"] == "location"
        assert obj["identity"]["name"] == "Test Ridge"

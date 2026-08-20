import json

import pytest

from observer_sandbox.creator_studio import CreatorStudioError, approve_draft, manual_draft
from observer_sandbox.db import connect
from observer_sandbox.manual_character_creation import (
    ManualCharacterCreationError,
    manual_character_baseline_status,
    manual_character_draft,
    manual_character_required_field_keys,
    update_manual_character_collection,
    update_manual_character_field,
)
from observer_sandbox.runtime import initialize


def _conn(tmp_path):
    db = tmp_path / "manual-character.sqlite3"
    initialize(db)
    return connect(db)


def _manual_value(key: str, data_type: str):
    specials = {
        "identity.full_name": "Rowan Hale",
        "identity.date_of_birth": "2001-05-12",
        "identity.sex": "male",
        "identity.gender": "man",
        "body.height_in": 74,
        "genetics.height_max_in": 76,
        "body.weight_lb": 190,
        "body.body_fat_pct": 12,
        "genetics.weight_lean_min_lb": 150,
        "genetics.weight_lean_max_lb": 220,
        "genetics.body_fat_floor_pct": 6,
        "body.neck_in": 16,
        "body.shoulders_in": 48,
        "body.chest_in": 42,
        "body.waist_in": 32,
        "body.hips_in": 38,
        "body.biceps_relaxed_in": 15,
        "body.biceps_flexed_in": 16,
        "body.triceps_in": 14,
        "body.forearms_in": 13,
        "body.thighs_in": 23,
        "body.calves_in": 16,
        "genetics.waist_target_in": 32,
        "sexual_anatomy.penis_length_in": 6,
        "sexual_anatomy.penis_girth_in": 5,
        "genetics.penis_length_in": 6,
        "genetics.penis_girth_in": 5,
        "training.training_age_years": 0,
        "raps_ia.iq": 120,
    }
    if key in specials:
        value = specials[key]
    elif key.startswith("genetics.") and data_type in {"number", "integer"}:
        value = 60
    elif data_type == "number":
        value = 50
    elif data_type == "integer":
        value = 1
    elif data_type == "boolean":
        value = True
    elif data_type == "date":
        value = "2001-05-12"
    elif data_type == "datetime":
        value = "2025-05-01T07:00:00+00:00"
    elif data_type == "json":
        value = []
    else:
        value = "manual value"
    return json.dumps(value) if data_type == "json" else str(value).lower() if isinstance(value, bool) else str(value)


def _fill_exact_seed(conn, user_id=42):
    for key in manual_character_required_field_keys(conn):
        row = conn.execute(
            "SELECT data_type FROM profile_field_definitions WHERE field_key=?", (key,)
        ).fetchone()
        assert row is not None
        update_manual_character_field(conn, user_id, key, _manual_value(key, str(row["data_type"])))


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

        required = set(manual_character_required_field_keys(conn))
        status = manual_character_baseline_status(conn, 42)
        assert status["ready"] is False
        assert status["total"] == len(required)
        assert set(status["missing"]) == required - {"identity.full_name"}


def test_manual_required_field_set_matches_ai_exact_seed_contract(tmp_path):
    with _conn(tmp_path) as conn:
        expected = set(manual_character_required_field_keys(conn))
        assert "raps_pa.practical_skills" in expected
        assert "raps_pa.practical_skill" not in expected
        assert "identity.age_years" not in expected
        assert "needs.energy" not in expected


def test_name_only_manual_character_cannot_be_approved(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        before = conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]

        with pytest.raises(CreatorStudioError, match="baseline is incomplete"):
            approve_draft(conn, 42)

        after = conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]
        assert after == before
        assert manual_character_draft(conn, 42)["proposal"]["identity"]["name"] == "Rowan Hale"


def test_manual_fields_use_same_canonical_creation_registry_and_validation(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")

        with pytest.raises(ManualCharacterCreationError, match="not a canonical creation-owned field"):
            update_manual_character_field(conn, 42, "identity.age_years", "24")
        with pytest.raises(ManualCharacterCreationError, match="not a canonical creation-owned field"):
            update_manual_character_field(conn, 42, "raps_pa.practical_skill", "legacy")

        with pytest.raises(ManualCharacterCreationError, match="plausible human creation range"):
            update_manual_character_field(conn, 42, "body.body_fat_pct", "1")

        update_manual_character_field(conn, 42, "identity.full_name", "Rowan Mercer")
        draft = manual_character_draft(conn, 42)
        assert draft["proposal"]["identity"]["name"] == "Rowan Mercer"
        assert draft["proposal"]["properties"]["character_profile"]["values"]["identity.full_name"] == "Rowan Mercer"


def test_complete_exact_manual_character_approves_into_same_sandbox_profile_storage(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        _fill_exact_seed(conn)
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
        draft_values = manual_character_draft(conn, 42)["proposal"]["properties"]["character_profile"]["values"]
        assert set(draft_values) == set(manual_character_required_field_keys(conn))

        obj = approve_draft(conn, 42)
        assert obj["creation_type"] == "character"
        assert obj["identity"]["name"] == "Rowan Hale"

        profile_rows = conn.execute(
            "SELECT field_key,value_json,source FROM creation_sandbox_profile_values WHERE object_id=?",
            (obj["object_id"],),
        ).fetchall()
        values = {row["field_key"]: json.loads(row["value_json"]) for row in profile_rows}
        assert set(values) == set(manual_character_required_field_keys(conn))
        assert values["identity.date_of_birth"] == "2001-05-12"
        assert values["body.height_in"] == 74.0
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
        _fill_exact_seed(conn)
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

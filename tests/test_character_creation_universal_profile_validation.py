import json

from observer_sandbox.character_creation_policy import sanitize_creation_profile_values
from observer_sandbox.creator_studio import (
    CreatorStudioError,
    _explicit_requested_age,
    _validate_character_payload,
    _validate_requested_age,
)
from observer_sandbox.db import connect, migrate
from observer_sandbox.profile_schema import seed_profile_field_definitions
from observer_sandbox.profile_schema_source_union import seed_source_union_extensions


def _conn(tmp_path):
    conn = connect(tmp_path / "creation-validation.sqlite3")
    migrate(conn)
    seed_profile_field_definitions(conn)
    seed_source_union_extensions(conn)
    return conn


def test_creation_profile_strips_runtime_fields_and_normalizes_source_union_alias(tmp_path):
    with _conn(tmp_path) as conn:
        value = sanitize_creation_profile_values(
            conn,
            {
                "identity.full_name": "Adrian Vale",
                "body.height_in": 71,
                "genetics.height_max_in": 72,
                "raps_pa.practical_skill": 72,
                "needs.energy": 80,
                "sleep.quality": 90,
            },
        )
    assert value["raps_pa.practical_skills"] == 72
    assert "raps_pa.practical_skill" not in value
    assert "needs.energy" not in value
    assert "sleep.quality" not in value


def test_creation_profile_respects_registered_text_raps_fields(tmp_path):
    with _conn(tmp_path) as conn:
        value = sanitize_creation_profile_values(
            conn,
            {
                "raps_ia.capability_notes": "Practical thinker with strong real-world judgment.",
                "raps_ia.problem_solving": 75,
            },
        )
    assert value["raps_ia.capability_notes"].startswith("Practical thinker")
    assert value["raps_ia.problem_solving"] == 75


def test_creation_profile_rejects_wrong_type_for_registered_text_raps_field(tmp_path):
    with _conn(tmp_path) as conn:
        try:
            sanitize_creation_profile_values(conn, {"raps_ia.capability_notes": 75})
        except ValueError as exc:
            assert "must be text" in str(exc)
        else:
            raise AssertionError("Expected registered text type rejection")


def test_creation_profile_rejects_conflicting_compatibility_aliases(tmp_path):
    with _conn(tmp_path) as conn:
        try:
            sanitize_creation_profile_values(
                conn,
                {
                    "raps_pa.practical_skill": 70,
                    "raps_pa.practical_skills": 74,
                },
            )
        except ValueError as exc:
            assert "alias conflict" in str(exc)
        else:
            raise AssertionError("Expected conflicting alias rejection")


def test_creation_profile_rejects_body_above_genetic_ceiling(tmp_path):
    with _conn(tmp_path) as conn:
        try:
            sanitize_creation_profile_values(
                conn,
                {
                    "identity.full_name": "Adrian Vale",
                    "body.height_in": 73,
                    "genetics.height_max_in": 72,
                },
            )
        except ValueError as exc:
            assert "body.height_in cannot exceed genetics.height_max_in" in str(exc)
        else:
            raise AssertionError("Expected genetic ceiling rejection")


def test_creation_profile_rejects_bad_ranges_and_invalid_date(tmp_path):
    with _conn(tmp_path) as conn:
        for values, expected in (
            ({"raps_pa.strength": 101}, "0..100"),
            ({"body.body_fat_pct": 0.5}, "plausible human creation range"),
            ({"identity.date_of_birth": "not-a-date"}, "ISO date"),
            (
                {
                    "sexual_anatomy.penis_length_in": 7.0,
                    "genetics.penis_length_in": 7.5,
                },
                "must match fixed genetic value",
            ),
        ):
            try:
                sanitize_creation_profile_values(conn, values)
            except ValueError as exc:
                assert expected in str(exc)
            else:
                raise AssertionError(f"Expected rejection for {values}")


def test_explicit_age_parser_supports_current_age_and_ignores_biography_ages():
    assert _explicit_requested_age("Create a male character who is 24 years old") == 24
    assert _explicit_requested_age("Create a 24-year-old male character") == 24
    assert _explicit_requested_age("Character age: 31, physically capable") == 31
    assert _explicit_requested_age("Create a character aged 28") == 28
    assert _explicit_requested_age("At age 20 he joined wilderness search-and-rescue.") is None
    assert _explicit_requested_age("He started boxing at age 17 and joined SAR at age 20.") is None
    assert _explicit_requested_age(
        "Create Adrian, a 24-year-old man. At age 20 he joined professional wilderness search-and-rescue."
    ) == 24
    assert _explicit_requested_age("No age specified") is None


def test_requested_age_must_match_dob_on_universe_reference_date(tmp_path):
    with _conn(tmp_path) as conn:
        conn.execute(
            "INSERT INTO runtime_state(key,value_json) VALUES('sim_time',?)",
            (json.dumps("2025-05-14T09:11:00+00:00"),),
        )
        conn.commit()
        _validate_requested_age(
            conn,
            "Create Adrian as a 24 years old man; at age 20 he joined SAR",
            {"identity.date_of_birth": "2001-05-12"},
        )
        try:
            _validate_requested_age(
                conn,
                "Create Adrian as a 24 years old man",
                {"identity.date_of_birth": "1999-05-12"},
            )
        except CreatorStudioError as exc:
            assert "requested 24" in str(exc)
            assert "gives age 26" in str(exc)
        else:
            raise AssertionError("Expected Creator-requested age mismatch rejection")


def test_trained_background_cannot_survive_with_empty_structured_skills(tmp_path):
    with _conn(tmp_path) as conn:
        proposal = {
            "identity": {"name": "Adrian Vale"},
            "properties": {
                "character_profile": {
                    "values": {
                        "identity.full_name": "Adrian Vale",
                        "background.origins": "Professional wilderness search-and-rescue training with navigation and first aid.",
                    },
                    "preferences": [],
                    "hobbies": [],
                    "habits": [],
                    "skills": [],
                }
            },
        }
        try:
            _validate_character_payload(conn, proposal)
        except CreatorStudioError as exc:
            assert "structured skills are empty" in str(exc)
        else:
            raise AssertionError("Expected trained-background skill consistency rejection")

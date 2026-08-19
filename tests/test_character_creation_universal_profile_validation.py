import json

from observer_sandbox.character_creation_policy import sanitize_creation_profile_values
from observer_sandbox.creator_studio import CreatorStudioError, _explicit_requested_age, _validate_requested_age
from observer_sandbox.db import connect, migrate
from observer_sandbox.profile_schema import seed_profile_field_definitions
from observer_sandbox.profile_schema_source_union import seed_source_union_extensions


def _conn(tmp_path):
    conn = connect(tmp_path / "creation-validation.sqlite3")
    migrate(conn)
    seed_profile_field_definitions(conn)
    seed_source_union_extensions(conn)
    return conn


def test_creation_profile_strips_runtime_fields_but_keeps_registered_source_union(tmp_path):
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
    assert value["raps_pa.practical_skill"] == 72
    assert "needs.energy" not in value
    assert "sleep.quality" not in value


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


def test_explicit_age_parser_supports_creator_phrasing():
    assert _explicit_requested_age("Create a male character who is 24 years old") == 24
    assert _explicit_requested_age("Character age: 31, physically capable") == 31
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
            "Create Adrian as a 24 years old man",
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

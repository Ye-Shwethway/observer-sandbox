from observer_sandbox.character_creation_policy import sanitize_creation_profile_values
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

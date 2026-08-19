from observer_sandbox.creator_profile_edit import apply_profile_proposal, preview_section_grade_target
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_profile_notifications import _is_grade_only_recalibration


def test_creator_grade_target_survives_normal_reinitialize(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        seeded = float(
            conn.execute(
                "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key='raps_pa.agility'"
            ).fetchone()[0]
        )
        proposal = preview_section_grade_target(conn, "char_darian", "physical", "A", mode="preserve_shape")
        apply_profile_proposal(conn, proposal, requested_by="test-creator")
        corrected_row = conn.execute(
            "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id='char_darian' AND field_key='raps_pa.agility'"
        ).fetchone()
        corrected = float(corrected_row["value_json"])
        assert corrected != seeded
        assert corrected_row["source"] == "creator-profile-control-v1"
        original_mode = corrected_row["mode"]
        original_authority = corrected_row["authority"]

    # Runtime status/init paths call canonical world/profile seeding again. An
    # explicit Creator correction must remain authoritative over that ordinary
    # initialization baseline.
    initialize(db)

    with connect(db) as conn:
        row = conn.execute(
            "SELECT value_json,mode,authority,source FROM character_profile_values WHERE entity_id='char_darian' AND field_key='raps_pa.agility'"
        ).fetchone()
        assert float(row["value_json"]) == corrected
        assert row["source"] == "creator-profile-control-v1"
        assert row["mode"] == original_mode
        assert row["authority"] == original_authority


def test_grade_only_observer_recalibration_is_not_character_progression():
    grade_only = {
        "before": 0.846153,
        "after": 0.846153,
        "delta": 0.0,
        "grade_changed": True,
        "old_grade": {"grade": "S"},
        "new_grade": {"grade": "A"},
    }
    assert _is_grade_only_recalibration(grade_only) is True

    real_crossing = dict(grade_only)
    real_crossing.update({"after": 0.8459, "delta": -0.000253})
    assert _is_grade_only_recalibration(real_crossing) is False

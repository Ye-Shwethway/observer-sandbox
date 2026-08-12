from observer_sandbox.db import connect
from observer_sandbox.profile_schema import profile_schema_summary
from observer_sandbox.runtime import initialize


def test_profile_schema_is_deep_and_domain_complete(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        summary = profile_schema_summary(conn)
        keys = {
            row[0]
            for row in conn.execute("SELECT field_key FROM profile_field_definitions")
        }
        intimate = {
            row[0]
            for row in conn.execute(
                "SELECT field_key FROM profile_field_definitions WHERE sensitivity='intimate'"
            )
        }

    assert summary["field_count"] >= 100
    assert {
        "identity", "body", "appearance", "sexual_anatomy", "raps_pa", "raps_ma",
        "raps_ia", "raps_sa", "raps_vc", "social", "needs", "physiology",
        "genetics", "personality", "background", "narrative",
    } <= set(summary["domains"])
    assert {
        "body.biceps_relaxed_in",
        "body.biceps_flexed_in",
        "body.triceps_in",
        "body.forearms_in",
        "sexual_anatomy.penis_length_in",
        "sexual_anatomy.penis_girth_in",
        "sexual_anatomy.erection_firmness",
        "raps_sa.self_satisfaction_weekly",
        "genetics.penis_length_in",
    } <= keys
    assert "sexual_anatomy.penis_length_in" in intimate
    assert "sexual_anatomy.penis_girth_in" in intimate

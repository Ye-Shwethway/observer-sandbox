from observer_sandbox.db import connect
from observer_sandbox.grading import (
    BODY_AESTHETIC_PROPORTION_SCHEME_ID,
    BODY_CENTRAL_ADIPOSITY_SCHEME_ID,
    BODY_REFERENCE_RANGES,
    SCHEME_REGISTRY,
    SKILL_PROFICIENCY_100_SCHEME_ID,
    derive_body_grade_items,
    evaluate_skill_score,
    evaluate_target_range,
)
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_profile_browser import _fmt_profile_section


def test_scheme_registry_and_skill_proficiency_are_explicit():
    assert SCHEME_REGISTRY["raps-100-proof-v1"].family == "monotonic"
    assert SCHEME_REGISTRY[SKILL_PROFICIENCY_100_SCHEME_ID].family == "monotonic"
    assert SCHEME_REGISTRY[BODY_AESTHETIC_PROPORTION_SCHEME_ID].family == "target_range"
    assert SCHEME_REGISTRY[BODY_CENTRAL_ADIPOSITY_SCHEME_ID].family == "target_range"

    assert evaluate_skill_score(90).grade == "S"
    assert evaluate_skill_score(87).grade == "A"
    assert evaluate_skill_score(75).grade == "A"


def test_target_range_penalizes_deviation_in_both_directions():
    target = BODY_REFERENCE_RANGES["body.waist_to_hips_ratio"]
    inside = evaluate_target_range(0.85, target, scheme_id=BODY_AESTHETIC_PROPORTION_SCHEME_ID)
    low = evaluate_target_range(0.65, target, scheme_id=BODY_AESTHETIC_PROPORTION_SCHEME_ID)
    high = evaluate_target_range(1.05, target, scheme_id=BODY_AESTHETIC_PROPORTION_SCHEME_ID)

    assert inside.grade == "S"
    assert low.grade != "S"
    assert high.grade != "S"


def test_body_derivation_uses_ratios_not_raw_larger_is_better():
    values = {
        "body.height_in": 76.0,
        "body.shoulders_in": 52.0,
        "body.chest_in": 45.0,
        "body.waist_in": 33.0,
        "body.hips_in": 39.0,
    }
    items = derive_body_grade_items(values)
    by_key = {item["field_key"]: item for item in items}

    assert round(by_key["body.waist_to_shoulders_ratio"]["value"], 3) == 0.635
    assert round(by_key["body.waist_to_hips_ratio"]["value"], 3) == 0.846
    assert round(by_key["body.waist_to_height_ratio"]["value"], 3) == 0.434
    assert by_key["body.chest_to_waist_ratio"]["kind"] == "derived_context"
    assert "grade_result" not in by_key["body.chest_to_waist_ratio"]


def test_profile_query_and_telegram_render_body_and_skill_grades_without_persisting_them(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        before_tiers = [
            tuple(row)
            for row in conn.execute(
                "SELECT skill_key,tier,score,experience FROM character_skills WHERE entity_id='char_darian' ORDER BY skill_key"
            ).fetchall()
        ]

        skills = profile_section(conn, "char_darian", "skills")
        by_skill = {item["key"]: item for item in skills["content"]}
        assert by_skill["hand_to_hand_combat"]["grade"]["grade"] == "S"
        assert by_skill["weapons"]["grade"]["grade"] == "A"
        assert skills["section"]["overall_grade"] is not None
        skill_text = _fmt_profile_section(skills)
        assert "Hand To Hand Combat   90 (S) · Expert" in skill_text
        assert "Weapons   87 (A) · Advanced" in skill_text

        body = profile_section(conn, "char_darian", "body")
        body_text = _fmt_profile_section(body)
        assert "Overall (S) · Expert" in body_text
        assert "Waist / Shoulders: 0.635 (S) · Expert" in body_text
        assert "Waist / Height: 0.434 (S) · Expert" in body_text
        assert "Chest / Waist: 1.364" in body_text

        after_tiers = [
            tuple(row)
            for row in conn.execute(
                "SELECT skill_key,tier,score,experience FROM character_skills WHERE entity_id='char_darian' ORDER BY skill_key"
            ).fetchall()
        ]
        assert after_tiers == before_tiers
        assert conn.execute("PRAGMA table_info(character_profile_values)").fetchall()
        assert all(row[1] != "grade" for row in conn.execute("PRAGMA table_info(character_profile_values)").fetchall())

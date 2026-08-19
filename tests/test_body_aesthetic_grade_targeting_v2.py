import json

import pytest

from observer_sandbox.body_aesthetic import evaluate_body
from observer_sandbox.body_grade_target import (
    BodyGradeTargetError,
    load_body_shape_preservation_policy,
    preview_body_grade_target,
)
from observer_sandbox.creator_profile_edit import apply_profile_proposal
from observer_sandbox.db import connect
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import runtime_value
from observer_sandbox.telegram_profile_edit_ui import (
    enter_profile_edit,
    profile_edit_callback_view,
    section_edit_view,
)


def _body_values(conn, character_id="char_darian"):
    rows = conn.execute(
        """
        SELECT v.field_key,v.value_json
        FROM character_profile_values v
        JOIN profile_field_definitions d ON d.field_key=v.field_key
        WHERE v.entity_id=? AND d.domain='body'
        """,
        (character_id,),
    ).fetchall()
    return {row["field_key"]: json.loads(row["value_json"]) for row in rows}


def _set_profile_value(conn, key, value, character_id="char_darian"):
    conn.execute(
        "UPDATE character_profile_values SET value_json=? WHERE entity_id=? AND field_key=?",
        (json.dumps(value), character_id, key),
    )
    conn.commit()


def test_male_body_v2_grades_waist_chest_and_keeps_health_context_out_of_aesthetic_composite(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        section = profile_section(conn, "char_darian", "body", role="owner")
        items = {item.get("field_key"): item for item in section["content"]}

        assert "body.waist_to_chest_ratio" in items
        assert items["body.waist_to_chest_ratio"]["grade"]["scheme_id"] == "body-aesthetic-proportion-v1"
        assert items["body.waist_to_height_ratio"]["role"] == "health_context"
        assert section["section"]["body_reference_profile"] == "body-aesthetic-male-v2"
        coverage = section["section"]["body_grade_coverage"]
        assert coverage["active_metrics"] == 3
        assert coverage["eligible_metrics"] == 3
        assert section["section"]["overall_grade"]["grade"] in {"E", "D", "C", "B", "A", "S"}


def test_female_registry_uses_female_whr_without_reusing_male_chest_semantics(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_profile_value(conn, "identity.sex", "Female")
        _set_profile_value(conn, "body.waist_in", 28.0)
        _set_profile_value(conn, "body.hips_in", 40.0)
        evaluation = evaluate_body(_body_values(conn), "Female")

        assert evaluation["reference_profile"] == "body-aesthetic-female-v2"
        assert evaluation["coverage"]["active_metrics"] == 1
        assert evaluation["coverage"]["eligible_metrics"] == 1
        assert [item["field_key"] for item in evaluation["aesthetic_items"]] == ["body.waist_to_hips_ratio"]
        assert evaluation["aesthetic_items"][0]["grade_result"].grade == "S"
        assert evaluation["overall_grade"].grade == "S"


def test_body_grade_b_preserve_proposes_raw_measurements_and_forward_verifies(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = _body_values(conn)
        proposal = preview_body_grade_target(conn, "char_darian", "B", mode="preserve_shape")

        assert proposal["kind"] == "body_grade_target"
        assert proposal["reference_profile"] == "body-aesthetic-male-v2"
        assert proposal["target_grade"] == "B"
        assert proposal["new_aggregate"]["grade"] == "B"
        assert proposal["hard_anchors"] == ["body.height_in"]
        assert all(change["field_key"] != "body.height_in" for change in proposal["changes"])
        assert len(proposal["changes"]) >= 2

        proposed_values = dict(before)
        for change in proposal["changes"]:
            proposed_values[change["field_key"]] = change["new_value"]
        forward = evaluate_body(proposed_values, "Male")
        assert forward["overall_grade"].grade == "B"


def test_body_grade_target_apply_is_atomic_and_profile_regrades_from_raw_values(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before_height = _body_values(conn)["body.height_in"]
        proposal = preview_body_grade_target(conn, "char_darian", "B", mode="preserve_shape")
        result = apply_profile_proposal(conn, proposal, requested_by="test:creator")
        assert result["target_grade"] == "B"
        assert _body_values(conn)["body.height_in"] == before_height

        section = profile_section(conn, "char_darian", "body", role="owner")
        assert section["section"]["overall_grade"]["grade"] == "B"


def test_body_preserve_rejects_when_already_at_requested_grade(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        current = profile_section(conn, "char_darian", "body", role="owner")["section"]["overall_grade"]["grade"]
        with pytest.raises(BodyGradeTargetError, match="already evaluates"):
            preview_body_grade_target(conn, "char_darian", current, mode="preserve_shape")


def test_body_grade_target_is_native_to_paused_body_edit_ux(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        text, _ = enter_profile_edit(conn, user_id=123, character_id="char_darian")
        assert "UNIVERSE PAUSED" in text
        assert runtime_value(conn, "paused", False) is True

        body_text, body_keyboard = section_edit_view(conn, user_id=123, section_id="body")
        assert "BODY EDIT" in body_text
        assert any(
            button.get("callback_data") == "pedit:gg:body"
            for row in body_keyboard
            for button in row
        )

        choice_text, choice_keyboard = profile_edit_callback_view(conn, user_id=123, callback_data="pedit:gg:body")
        assert "BODY MEASUREMENTS" in choice_text
        assert any(
            button.get("callback_data") == "pedit:gt:body:B:p"
            for row in choice_keyboard
            for button in row
        )

        preview_text, preview_keyboard = profile_edit_callback_view(conn, user_id=123, callback_data="pedit:gt:body:B:p")
        assert "Reference: body-aesthetic-male-v2" in preview_text
        assert "Projected proportions:" in preview_text
        assert "Health context (not aesthetic score):" in preview_text
        assert any(button.get("text") == "✅ Apply Change" for row in preview_keyboard for button in row)
        assert runtime_value(conn, "paused", False) is True


def test_male_preserve_shape_projects_all_represented_muscular_circumferences(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = _body_values(conn)
        proposal = preview_body_grade_target(conn, "char_darian", "A", mode="preserve_shape")
        changes = {change["field_key"]: change for change in proposal["changes"]}
        projected = set(proposal["shape_preservation"]["projected_fields"])

        expected_dependents = {
            "body.neck_in",
            "body.biceps_relaxed_in",
            "body.biceps_flexed_in",
            "body.triceps_in",
            "body.forearms_in",
            "body.thighs_in",
            "body.calves_in",
        }
        assert proposal["proposal_version"] == 2
        assert proposal["shape_preservation"]["revision"] == "body-shape-preservation-v2.1"
        assert expected_dependents <= projected
        assert expected_dependents <= set(changes)
        assert "body.height_in" not in changes

        after = dict(before)
        after.update({key: change["new_value"] for key, change in changes.items()})
        assert evaluate_body(after, "Male")["overall_grade"].grade == "A"


def test_preserve_shape_secondary_ratio_drift_is_bounded_by_projected_follow_through(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        before = _body_values(conn)
        proposal = preview_body_grade_target(conn, "char_darian", "A", mode="preserve_shape")
        after = dict(before)
        after.update({change["field_key"]: change["new_value"] for change in proposal["changes"]})
        policy = load_body_shape_preservation_policy()

        for rule in policy["secondary_ratio_constraints"]:
            n = rule["numerator_field"]
            d = rule["denominator_field"]
            if n not in before or d not in before or n not in after or d not in after:
                continue
            old_ratio = float(before[n]) / float(before[d])
            new_ratio = float(after[n]) / float(after[d])
            assert abs(new_ratio / old_ratio - 1.0) < 0.03


def test_female_target_reuses_generic_shape_projection_without_male_grade_metrics(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _set_profile_value(conn, "identity.sex", "Female")
        _set_profile_value(conn, "body.waist_in", 28.0)
        _set_profile_value(conn, "body.hips_in", 40.0)
        proposal = preview_body_grade_target(conn, "char_darian", "A", mode="preserve_shape")
        changed = {change["field_key"] for change in proposal["changes"]}

        assert proposal["reference_profile"] == "body-aesthetic-female-v2"
        assert [item["field_key"] for item in proposal["new_metrics"]] == ["body.waist_to_hips_ratio"]
        assert "body.thighs_in" in changed
        assert "body.calves_in" in changed
        assert proposal["new_aggregate"]["grade"] == "A"


def test_missing_dependent_measurement_is_skipped_not_fabricated(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        conn.execute(
            "DELETE FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "body.calves_in"),
        )
        conn.commit()
        proposal = preview_body_grade_target(conn, "char_darian", "A", mode="preserve_shape")

        assert "body.calves_in" not in proposal["shape_preservation"]["projected_fields"]
        assert all(change["field_key"] != "body.calves_in" for change in proposal["changes"])

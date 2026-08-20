from observer_sandbox.body_aesthetic import evaluate_body


def test_male_body_output_exposes_only_grade_driving_waist_chest_ratio():
    evaluation = evaluate_body(
        {
            "body.height_in": 74.0,
            "body.chest_in": 43.06,
            "body.waist_in": 36.45,
            "body.shoulders_in": 49.26,
            "body.hips_in": 37.91,
        },
        "Male",
    )

    items = evaluation["aesthetic_items"]
    by_key = {item["field_key"]: item for item in items}
    labels = {item["label"] for item in items}

    assert "body.waist_to_chest_ratio" in by_key
    assert by_key["body.waist_to_chest_ratio"]["grade_result"] is not None
    assert "body.chest_to_waist_ratio" not in by_key
    assert "Chest / Waist" not in labels

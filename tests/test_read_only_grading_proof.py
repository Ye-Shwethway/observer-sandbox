from observer_sandbox.db import connect
from observer_sandbox.grading import evaluate_raps_100
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_bot import _callback_view


def test_strength_grade_is_derived_without_mutating_raw_value(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        before = conn.execute(
            "SELECT value_json, mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        assert before["value_json"] == "90"
        assert before["mode"] == "static"

        attributes = profile_section(conn, "char_darian", "attributes")
        strength = next(item for item in attributes["content"] if item["field_key"] == "raps_pa.strength")
        assert strength["value"] == 90
        assert strength["grade"] == {
            "scheme_id": "raps-100-proof-v1",
            "grade": "S",
            "label": "Exceptional",
        }

        after = conn.execute(
            "SELECT value_json, mode FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        assert dict(after) == dict(before)

        text, _ = _callback_view(conn, 111, "psec:char_darian:attributes")
        assert "Strength   90 · Grade S" in text
        assert "Stamina   85 · Grade" not in text


def test_proof_scheme_boundaries_are_deterministic():
    assert evaluate_raps_100(100).grade == "S"
    assert evaluate_raps_100(90).grade == "S"
    assert evaluate_raps_100(89.999).grade == "A"
    assert evaluate_raps_100(75).grade == "A"
    assert evaluate_raps_100(60).grade == "B"
    assert evaluate_raps_100(40).grade == "C"
    assert evaluate_raps_100(20).grade == "D"
    assert evaluate_raps_100(0).grade == "E"

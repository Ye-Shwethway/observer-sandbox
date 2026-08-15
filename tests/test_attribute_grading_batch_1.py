from observer_sandbox.db import connect
from observer_sandbox.grading import ATTRIBUTE_RAPS_100_FIELDS
from observer_sandbox.profile_observer import profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_bot import _callback_view


def test_all_explicit_attribute_batch_fields_receive_derived_grades(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        attributes = profile_section(conn, "char_darian", "attributes")
        by_key = {item["field_key"]: item for item in attributes["content"]}

        assert len(ATTRIBUTE_RAPS_100_FIELDS) == 36
        assert ATTRIBUTE_RAPS_100_FIELDS <= by_key.keys()
        assert all("grade" in by_key[key] for key in ATTRIBUTE_RAPS_100_FIELDS)
        assert all(by_key[key]["grade"]["scheme_id"] == "raps-100-proof-v1" for key in ATTRIBUTE_RAPS_100_FIELDS)

        assert "grade" not in by_key["raps_ia.iq"]
        assert by_key["raps_ia.iq"]["value"] == 140

        text, _ = _callback_view(conn, 111, "psec:char_darian:attributes")
        assert "Overall (A) · Advanced" in text
        assert "Physical (A) · Advanced" in text
        assert "Strength   90 (S) · Expert" in text
        assert "Stamina   85 (A) · Advanced" in text
        assert "Medical knowledge   75 (A) · Advanced" in text
        assert "IQ   140 (" not in text


def test_body_and_skill_sections_use_distinct_explicit_schemes(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    with connect(db) as conn:
        body = profile_section(conn, "char_darian", "body")
        raw_body = [item for item in body["content"] if item.get("kind") == "field"]
        derived_body = [item for item in body["content"] if item.get("kind") == "derived_grade"]
        assert raw_body
        assert all("grade" not in item for item in raw_body)
        assert derived_body
        assert all(item["grade"]["scheme_id"] != "raps-100-proof-v1" for item in derived_body)

        skills = profile_section(conn, "char_darian", "skills")
        assert skills["content"]
        assert all(item["grade"]["scheme_id"] == "skill-proficiency-100-v1" for item in skills["content"])

import json

import pytest

from observer_sandbox.db import connect
from observer_sandbox.profile_observer import profile_menu, profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_profile_browser import profile_callback_view


def _grade(section, domain=None):
    if domain is None:
        return section["section"]["overall_grade"]
    return section["section"]["group_grades"][domain]


def test_owner_sees_sexual_profile_and_allowed_user_does_not(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        owner_menu = profile_menu(conn, "char_darian", role="owner")
        allowed_menu = profile_menu(conn, "char_darian", role="allowed")

        owner_ids = [section["id"] for section in owner_menu["sections"]]
        allowed_ids = [section["id"] for section in allowed_menu["sections"]]
        assert "sexual" in owner_ids
        assert "sexual" not in allowed_ids

        sexual = profile_section(conn, "char_darian", "sexual", role="owner")
        by_key = {item["field_key"]: item for item in sexual["content"]}
        assert by_key["sexual_anatomy.penis_length_in"]["value"] == 10.0
        assert by_key["sexual_anatomy.penis_girth_in"]["value"] == 5.0
        assert by_key["sexual_anatomy.baseline_erectile_function"]["value"] == 95.0
        assert by_key["sexual_anatomy.erection_firmness_cap"]["value"] == 98.0
        assert by_key["raps_sa.libido"]["value"] == 85

        with pytest.raises(PermissionError):
            profile_section(conn, "char_darian", "sexual", role="allowed")


def test_telegram_sexual_section_is_owner_only_and_renders_canonical_physiology(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        owner_menu_text, owner_keyboard = profile_callback_view(
            conn, "prof:char_darian", role="owner"
        )
        assert "Sexual Anatomy & Physiology" in owner_menu_text
        assert any(
            button["callback_data"] == "psec:char_darian:sexual"
            for row in owner_keyboard
            for button in row
        )

        allowed_menu_text, allowed_keyboard = profile_callback_view(
            conn, "prof:char_darian", role="allowed"
        )
        assert "Sexual Anatomy & Physiology" not in allowed_menu_text
        assert all(
            button["callback_data"] != "psec:char_darian:sexual"
            for row in allowed_keyboard
            for button in row
        )

        locked_text, _ = profile_callback_view(
            conn, "psec:char_darian:sexual", role="allowed"
        )
        assert "Creator authority required" in locked_text

        text, _ = profile_callback_view(conn, "psec:char_darian:sexual", role="owner")
        assert "SEXUAL ANATOMY & PHYSIOLOGY" in text.upper()
        assert "Penis length: 10\"" in text
        assert "Penis girth: 5\"" in text
        assert "Baseline erectile function: 95" in text
        assert "Erection firmness physiological cap: 98" in text


def test_attribute_rows_and_group_overall_grades_use_current_values(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        attributes = profile_section(conn, "char_darian", "attributes", role="owner")
        physical = _grade(attributes, "raps_pa")
        overall = _grade(attributes)

        assert physical["value"] == pytest.approx(86.538, abs=0.001)
        assert physical["grade"] == "A"
        assert physical["label"] == "Advanced"
        assert overall["value"] == pytest.approx(86.583, abs=0.001)
        assert overall["grade"] == "A"
        assert overall["label"] == "Advanced"

        text, _ = profile_callback_view(conn, "psec:char_darian:attributes", role="owner")
        assert "Overall (A) · Advanced" in text
        assert "Physical (A) · Advanced" in text
        assert "Strength   90 (S) · Expert" in text
        assert "IQ   140" in text
        assert "IQ   140 (" not in text

        # Change only current authoritative local test values. No grade state is persisted;
        # a fresh query must recompute both item and group grades from the new values.
        for field_key in (
            "raps_pa.strength",
            "raps_pa.stamina",
            "raps_pa.agility",
            "raps_pa.speed",
            "raps_pa.reflexes",
            "raps_pa.endurance",
            "raps_pa.flexibility",
            "raps_pa.combat_skill",
            "raps_pa.weapons_proficiency",
            "raps_pa.survival_skill",
            "raps_pa.powerlifting_capacity",
            "raps_pa.focus_precision",
            "raps_pa.practical_skills",
        ):
            conn.execute(
                "UPDATE character_profile_values SET value_json='10' WHERE entity_id='char_darian' AND field_key=?",
                (field_key,),
            )
        conn.commit()

        changed = profile_section(conn, "char_darian", "attributes", role="owner")
        changed_physical = _grade(changed, "raps_pa")
        assert changed_physical["value"] == 10.0
        assert changed_physical["grade"] == "E"
        assert changed_physical["label"] == "Beginner"

        changed_text, _ = profile_callback_view(conn, "psec:char_darian:attributes", role="owner")
        assert "Physical (E) · Beginner" in changed_text
        assert "Strength   10 (E) · Beginner" in changed_text


def test_new_ordinary_section_is_config_only_and_telegram_generic(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)

    source = json.loads(open("config/profile_sections.v1.json", encoding="utf-8").read())
    source["sections"].append(
        {
            "id": "genetic_context",
            "label": "Genetic Context",
            "icon": "🧬",
            "order": 65,
            "renderer": "fields",
            "domains": ["genetics"],
            "visibility": "authorized",
            "sensitivities": ["normal"],
        }
    )
    config = tmp_path / "profile_sections.json"
    config.write_text(json.dumps(source), encoding="utf-8")
    monkeypatch.setenv("OBSERVER_PROFILE_SECTIONS_PATH", str(config))

    with connect(db) as conn:
        menu = profile_menu(conn, "char_darian", role="allowed")
        ids = [section["id"] for section in menu["sections"]]
        assert "genetic_context" in ids

        text, keyboard = profile_callback_view(conn, "prof:char_darian", role="allowed")
        assert "Genetic Context" in text
        assert any(
            button["callback_data"] == "psec:char_darian:genetic_context"
            for row in keyboard
            for button in row
        )

        section_text, _ = profile_callback_view(
            conn, "psec:char_darian:genetic_context", role="allowed"
        )
        assert "GENETIC CONTEXT" in section_text.upper()
        assert "Genetic maximum height" in section_text
        assert "Genetically fixed penis length" not in section_text


def test_all_ten_canonical_grade_descriptions_remain_defined():
    from observer_sandbox.grading import GRADE_VOCABULARY

    assert GRADE_VOCABULARY == (
        ("E", "Beginner"),
        ("D", "Novice"),
        ("C", "Capable"),
        ("B", "Skilled"),
        ("A", "Advanced"),
        ("S", "Expert"),
        ("SS", "Elite"),
        ("SSS", "Master"),
        ("X", "Mythic"),
        ("XX", "Transcendent"),
    )

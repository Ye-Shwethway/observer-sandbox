from observer_sandbox.db import connect
from observer_sandbox.profile_observer import profile_menu, profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_bot import _callback_view


def test_profile_query_exposes_seeded_public_sections_and_filters_sensitive_fields(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        menu = profile_menu(conn, "char_darian")
        labels = [section["label"] for section in menu["sections"]]
        assert labels == [
            "Identity",
            "Appearance",
            "Body",
            "Attributes",
            "Personality",
            "Skills",
            "Preferences & Habits",
            "Background",
        ]

        identity = profile_section(conn, "char_darian", "identity")
        identity_keys = {item["field_key"] for item in identity["content"]}
        assert "identity.full_name" in identity_keys
        assert "identity.date_of_birth" in identity_keys
        assert "identity.sexual_orientation" not in identity_keys

        attributes = profile_section(conn, "char_darian", "attributes")
        attribute_keys = {item["field_key"] for item in attributes["content"]}
        assert "raps_pa.strength" in attribute_keys
        assert "raps_ia.iq" in attribute_keys
        assert all(not key.startswith("raps_sa.") for key in attribute_keys)


def test_telegram_profile_browser_is_readable_and_navigable(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        character_text, character_keyboard = _callback_view(conn, 111, "char:char_darian")
        assert "Darian Thorne" in character_text
        assert character_keyboard[0][0]["callback_data"] == "prof:char_darian"

        profile_text, profile_keyboard = _callback_view(conn, 111, "prof:char_darian")
        assert "Darian Thorne · PROFILE" in profile_text
        assert "Identity" in profile_text
        assert "Body" in profile_text
        assert any(
            button["callback_data"] == "psec:char_darian:body"
            for row in profile_keyboard
            for button in row
        )

        body_text, body_keyboard = _callback_view(conn, 111, "psec:char_darian:body")
        assert "DARIAN THORNE · BODY" in body_text.upper()
        assert "Height: 6'4\"" in body_text
        assert "Weight: 215 lb" in body_text
        assert body_keyboard[0][0]["callback_data"] == "prof:char_darian"

        attributes_text, _ = _callback_view(conn, 111, "psec:char_darian:attributes")
        assert "Physical" in attributes_text
        assert "Strength   90" in attributes_text
        assert "Intellectual" in attributes_text
        assert "IQ   140" in attributes_text

        preferences_text, _ = _callback_view(conn, 111, "psec:char_darian:preferences")
        assert "Likes" in preferences_text
        assert "intense training" in preferences_text
        assert "Hobbies" in preferences_text
        assert "physical fitness" in preferences_text

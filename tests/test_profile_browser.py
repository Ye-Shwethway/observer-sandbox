from observer_sandbox.db import connect
from observer_sandbox.event_log import record_event
from observer_sandbox.profile_observer import profile_menu, profile_section
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import snapshot
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
            "Recovery",
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

        recovery = profile_section(conn, "char_darian", "recovery")
        assert recovery["content"][0]["field_key"] == "physiology.fatigue"
        assert recovery["content"][0]["value"] == 0.0
        recovery_keys = {item["field_key"] for item in recovery["content"]}
        assert {
            "training.readiness",
            "strength.progression.raw",
            "strength.progression.stimulus",
            "strength.progression.level_factor",
            "strength.progression.saturation",
            "strength.progression.recovery",
            "strength.progression.status",
            "strength.progression.settlement",
            "strength.progression.detraining",
            "strength.progression.next",
        } <= recovery_keys


def test_strength_progression_observability_is_read_only_and_reflects_event_evidence(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        raw_before = conn.execute(
            "SELECT value_json,mode,authority FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        event_count_before = int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])

        sim_time = snapshot(conn, "char_darian")["sim_time"]
        record_event(
            conn,
            sim_time=sim_time,
            actor_id="char_darian",
            event_type="action_completed",
            payload={"training_stimulus": {"domain": "strength", "stimulus_units": 1.0}},
        )
        conn.commit()
        seeded_event_count = int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0])

        recovery = profile_section(conn, "char_darian", "recovery")
        by_key = {item["field_key"]: item for item in recovery["content"]}
        assert by_key["strength.progression.raw"]["value"] == "90.000000"
        assert by_key["strength.progression.stimulus"]["value"].startswith("1.000 units")
        assert by_key["strength.progression.level_factor"]["value"] == "1.000%"
        assert by_key["strength.progression.status"]["value"].startswith("Recovering")
        assert "14.0 d remaining" in by_key["strength.progression.detraining"]["value"]

        raw_after = conn.execute(
            "SELECT value_json,mode,authority FROM character_profile_values WHERE entity_id=? AND field_key=?",
            ("char_darian", "raps_pa.strength"),
        ).fetchone()
        assert dict(raw_after) == dict(raw_before)
        assert int(conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]) == seeded_event_count
        assert seeded_event_count == event_count_before + 1


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
        assert "Recovery" in profile_text
        assert any(
            button["callback_data"] == "psec:char_darian:body"
            for row in profile_keyboard
            for button in row
        )
        assert any(
            button["callback_data"] == "psec:char_darian:recovery"
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

        recovery_text, _ = _callback_view(conn, 111, "psec:char_darian:recovery")
        assert "RECOVERY" in recovery_text.upper()
        assert "Systemic fatigue" in recovery_text
        assert "Training readiness" in recovery_text
        assert "Strength raw" in recovery_text
        assert "Recent Strength stimulus" in recovery_text
        assert "Level adaptation factor" in recovery_text
        assert "Saturation yield" in recovery_text
        assert "Recovery realization" in recovery_text
        assert "Adaptation status" in recovery_text
        assert "Latest settlement" in recovery_text
        assert "Detraining" in recovery_text
        assert "Next progression boundary" in recovery_text

        preferences_text, _ = _callback_view(conn, 111, "psec:char_darian:preferences")
        assert "Likes" in preferences_text
        assert "intense training" in preferences_text
        assert "Hobbies" in preferences_text
        assert "physical fitness" in preferences_text

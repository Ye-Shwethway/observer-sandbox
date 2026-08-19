import observer_sandbox.creator_studio as studio
import observer_sandbox.telegram_creator_studio as telegram_studio
from observer_sandbox.character_creation_policy import creation_field_keys
from observer_sandbox.creator_draft_export import render_full_draft_text
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_representation import sandbox_profile_values


def _proposal(user_id=111):
    return {
        "proposal_version": 1,
        "creation_type": "character",
        "schema_version": 1,
        "target_scope": "sandbox",
        "identity": {"name": "Darian Thorne"},
        "properties": {
            "character_profile": {
                "values": {
                    "identity.full_name": "Darian Thorne",
                    "identity.date_of_birth": "2002-09-03",
                    "body.height_in": 76.0,
                    "body.weight_lb": 199.0,
                    "body.body_fat_pct": 10.5,
                    "body.bmi": 24.2,
                    "needs.energy": 85,
                    "sleep.quality": 82,
                    "physiology.fatigue": 20,
                    "raps_sa.self_satisfaction_weekly": 20,
                    "raps_pa.strength": 78,
                    "personality.primary_traits": ["disciplined", "guarded"],
                    "training.training_age_years": 9,
                    "training.accumulated_stimulus": "runtime-like accumulated state",
                },
                "preferences": [{"preference_type": "like", "subject": "intense training", "intensity": 90}],
                "hobbies": [{"name": "swimming", "proficiency": 80, "frequency": "weekly", "enjoyment": 90}],
                "habits": [{"name": "perimeter checks", "description": "Checks surroundings.", "frequency": "daily", "strength": 75}],
                "skills": [
                    {"skill_key": "weapons", "category": "combat", "score": 79, "tier": "A", "experience": 55},
                    {"skill_key": "weapon_mastery", "category": "combat", "score": 80, "tier": "A", "experience": 56},
                    {"skill_key": "survival", "category": "fieldcraft", "score": 78, "tier": "A", "experience": 55},
                ],
            },
            "compatibility_tags": ["human", "realistic", "pre-prime"],
        },
        "relationships": [],
        "capabilities": ["train", "observe"],
        "provenance": {"mode": "ai_generated", "requested_by": f"telegram:{user_id}"},
    }


def test_creation_schema_excludes_runtime_and_derived_fields(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        allowed = creation_field_keys(conn)
        assert "body.height_in" in allowed
        assert "raps_pa.strength" in allowed
        assert "training.training_age_years" in allowed
        for denied in (
            "body.bmi",
            "needs.energy",
            "sleep.quality",
            "physiology.fatigue",
            "identity.age_years",
            "raps_sa.self_satisfaction_weekly",
            "training.accumulated_stimulus",
        ):
            assert denied not in allowed
        schema_values = studio._schema(conn, "character")["properties"]["properties"]["properties"]["character_profile"]["properties"]["values"]["properties"]
        assert "body.height_in" in schema_values
        assert "needs.energy" not in schema_values
        assert "body.bmi" not in schema_values


def test_ai_payload_is_sanitized_and_skills_are_deduplicated_before_approval(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setattr(studio, "creator_creation_binding", lambda conn: {"provider_id": "test", "model_id": "model", "parameters": {}})
    monkeypatch.setattr(studio, "generate_structured", lambda conn, **kwargs: _proposal())
    with connect(db) as conn:
        draft = studio.ai_draft(conn, 111, "character", "Darian Thorne age 19 developmental snapshot")
        profile = draft["proposal"]["properties"]["character_profile"]
        values = profile["values"]
        assert "body.height_in" in values
        assert "needs.energy" not in values
        assert "body.bmi" not in values
        assert "sleep.quality" not in values
        assert "raps_sa.self_satisfaction_weekly" not in values
        assert "training.accumulated_stimulus" not in values
        skill_keys = [item["skill_key"] for item in profile["skills"]]
        assert skill_keys.count("weapons") == 1
        assert "weapon_mastery" not in skill_keys

        obj = studio.approve_draft(conn, 111)
        stored = {item["field_key"] for item in sandbox_profile_values(conn, obj["object_id"])}
        assert "body.height_in" in stored
        assert "needs.energy" not in stored
        assert "body.bmi" not in stored


def test_full_draft_text_export_and_button(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setattr(studio, "creator_creation_binding", lambda conn: {"provider_id": "test", "model_id": "model", "parameters": {}})
    monkeypatch.setattr(studio, "generate_structured", lambda conn, **kwargs: _proposal())
    with connect(db) as conn:
        studio.ai_draft(conn, 111, "character", "Darian Thorne age 19")
        filename, text = render_full_draft_text(conn, 111)
        assert filename.endswith(".txt")
        assert "CHARACTER PROFILE VALUES" in text
        assert "body.height_in: 76.0" in text
        assert "SKILLS" in text
        assert "PREFERENCES" in text
        assert "PROVENANCE" in text
        assert "needs.energy" not in text

        preview, keyboard = telegram_studio.draft_preview_view(conn, 111)
        callbacks = {button["callback_data"] for row in keyboard for button in row}
        assert "sw:cs:export" in callbacks
        assert "CREATION SANDBOX DRAFT" in preview

        sent = []
        monkeypatch.setattr(telegram_studio, "send_full_draft_document", lambda conn, user_id: sent.append(user_id) or "creator-studio-darian-thorne-r1.txt")
        exported, _ = telegram_studio.studio_callback_view(conn, 111, "sw:cs:export")
        assert sent == [111]
        assert "Export sent" in exported

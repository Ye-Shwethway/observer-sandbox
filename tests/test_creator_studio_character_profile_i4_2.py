import observer_sandbox.creator_studio as studio
from observer_sandbox.creation_sandbox import canonical_state_fingerprint
from observer_sandbox.db import SCHEMA_VERSION, connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_character_facets import sandbox_habits, sandbox_hobbies, sandbox_preferences
from observer_sandbox.sandbox_representation import sandbox_profile_values, sandbox_skills
from observer_sandbox.telegram_creator_studio import draft_preview_view, studio_callback_view


def _generated_character(user_id: int):
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
                    "identity.sex": "male",
                    "body.height_in": 75.5,
                    "body.weight_lb": 185.0,
                    "body.body_fat_pct": 10.0,
                    "appearance.eye_color": "deep blue",
                    "appearance.hair_color": "jet black",
                    "raps_pa.strength": 78,
                    "raps_ma.emotional_stability": 72,
                    "raps_ia.iq": 140,
                    "personality.primary_traits": ["disciplined", "guarded", "driven"],
                },
                "preferences": [
                    {"preference_type": "like", "subject": "intense training", "intensity": 88.0}
                ],
                "hobbies": [
                    {"name": "physical fitness", "proficiency": 82.0, "frequency": "daily", "enjoyment": 90.0}
                ],
                "habits": [
                    {"name": "perimeter checks", "description": "Checks surroundings habitually.", "frequency": "daily", "strength": 76.0}
                ],
                "skills": [
                    {"skill_key": "hand_to_hand_combat", "category": "combat", "score": 80.0, "tier": "A", "experience": 60.0},
                    {"skill_key": "survival", "category": "fieldcraft", "score": 78.0, "tier": "A", "experience": 55.0},
                ],
            },
            "compatibility_tags": ["human", "realistic"],
        },
        "relationships": [],
        "capabilities": ["train", "observe", "relax"],
        "provenance": {"mode": "ai_generated", "requested_by": f"telegram:{user_id}"},
    }


def test_schema_v21_registers_full_sandbox_character_facets(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert SCHEMA_VERSION == 21
        assert conn.execute("SELECT value FROM schema_meta WHERE key='schema_version'").fetchone()[0] == "21"
        tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        assert {
            "creation_sandbox_character_preferences",
            "creation_sandbox_character_hobbies",
            "creation_sandbox_character_habits",
        } <= tables


def test_ai_character_draft_uses_registered_profile_schema_and_canonical_reference(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    captured = {}
    monkeypatch.setattr(studio, "creator_creation_binding", lambda conn: {"provider_id": "test", "model_id": "model", "parameters": {}})

    def fake_generate(conn, **kwargs):
        captured.update(kwargs)
        return _generated_character(111)

    monkeypatch.setattr(studio, "generate_structured", fake_generate)
    with connect(db) as conn:
        assert conn.execute("SELECT 1 FROM entities WHERE id='char_darian'").fetchone() is not None
        draft = studio.ai_draft(
            conn,
            111,
            "character",
            "Create Darian Thorne at age 19, before his full physical prime.",
        )
        assert draft["proposal"]["properties"]["character_profile"]["values"]["body.height_in"] == 75.5
        schema_values = captured["schema"]["properties"]["properties"]["properties"]["character_profile"]["properties"]["values"]
        assert "body.height_in" in schema_values["properties"]
        assert "raps_pa.strength" in schema_values["properties"]
        assert "Reference JSON" in captured["prompt"]
        assert '"name":"Darian Thorne"' in captured["prompt"]
        assert '"body.height_in":76.0' in captured["prompt"]


def test_character_profile_preview_and_approval_materialize_isolated_structured_state(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setattr(studio, "creator_creation_binding", lambda conn: {"provider_id": "test", "model_id": "model", "parameters": {}})
    monkeypatch.setattr(studio, "generate_structured", lambda conn, **kwargs: _generated_character(111))
    with connect(db) as conn:
        before = canonical_state_fingerprint(conn)
        studio.ai_draft(conn, 111, "character", "Darian Thorne age 19 developmental snapshot")
        text, keyboard = draft_preview_view(conn, 111)
        callbacks = {button["callback_data"] for row in keyboard for button in row}
        assert "Character Profile" in text
        assert "Profile values: 12" in text
        assert "body.height_in: 75.5" in text
        assert "sw:cs:profile:0" in callbacks

        full_text, _ = studio_callback_view(conn, 111, "sw:cs:profile:0")
        assert "CHARACTER PROFILE DRAFT" in full_text
        assert "appearance.eye_color: deep blue" in full_text

        obj = studio.approve_draft(conn, 111)
        object_id = obj["object_id"]
        profile = {item["field_key"]: item["value"] for item in sandbox_profile_values(conn, object_id)}
        assert profile["body.height_in"] == 75.5
        assert profile["raps_ia.iq"] == 140
        assert [item["skill_key"] for item in sandbox_skills(conn, object_id)] == ["hand_to_hand_combat", "survival"]
        assert sandbox_preferences(conn, object_id)[0]["subject"] == "intense training"
        assert sandbox_hobbies(conn, object_id)[0]["name"] == "physical fitness"
        assert sandbox_habits(conn, object_id)[0]["name"] == "perimeter checks"
        assert "character_profile" not in obj["properties"]
        assert canonical_state_fingerprint(conn) == before

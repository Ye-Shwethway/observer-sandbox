from observer_sandbox.creation_sandbox import (
    activate_creation_proposal,
    canonical_state_fingerprint,
)
from observer_sandbox.creation_socket import build_creation_proposal
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_character_facets import (
    replace_sandbox_habits,
    replace_sandbox_hobbies,
    replace_sandbox_preferences,
)
from observer_sandbox.sandbox_representation import (
    replace_sandbox_skills,
    set_sandbox_profile_values,
)
from observer_sandbox.telegram_creator_bot import _callback_view


def _callbacks(keyboard):
    return [button["callback_data"] for row in keyboard or [] for button in row]


def _character(conn):
    character = activate_creation_proposal(
        conn,
        build_creation_proposal(
            "character",
            identity={"name": "Adrian Vale"},
            requested_by="test:creator",
        ),
    )
    object_id = character["object_id"]
    set_sandbox_profile_values(
        conn,
        object_id,
        {
            "identity.sex": "male",
            "identity.gender": "male",
            "identity.sexual_orientation": "heterosexual",
            "body.height_in": 74.0,
            "body.weight_lb": 200.0,
            "body.body_fat_pct": 14.0,
            "raps_pa.strength": 82.0,
            "raps_pa.stamina": 85.0,
            "raps_ma.resilience": 80.0,
            "background.summary": "Wilderness search-and-rescue professional.",
        },
    )
    replace_sandbox_skills(
        conn,
        object_id,
        [
            {
                "skill_key": "survival",
                "category": "fieldcraft",
                "score": 80.0,
                "experience": 4.0,
            },
            {
                "skill_key": "field_medicine",
                "category": "medical",
                "score": 72.0,
                "experience": 4.0,
            },
        ],
    )
    replace_sandbox_preferences(
        conn,
        object_id,
        [{"preference_type": "like", "subject": "quiet outdoor environments", "intensity": 80}],
    )
    replace_sandbox_hobbies(
        conn,
        object_id,
        [{"name": "Hiking", "frequency": "weekly", "enjoyment": 90}],
    )
    replace_sandbox_habits(
        conn,
        object_id,
        [{"name": "Equipment checks", "frequency": "before field work", "strength": 85}],
    )
    return character


def test_sandbox_character_card_exposes_profile_before_configuration(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        character = _character(conn)
        _, keyboard = _callback_view(conn, 111, f"sw:o:{character['object_id']}")
        callbacks = _callbacks(keyboard)
        assert callbacks.index(f"sw:prof:{character['object_id']}") < callbacks.index(
            f"sw:cfg:{character['object_id']}"
        )


def test_sandbox_profile_reuses_real_world_presentation_and_sandbox_navigation(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        character = _character(conn)
        object_id = character["object_id"]
        before = canonical_state_fingerprint(conn)

        text, keyboard = _callback_view(conn, 111, f"sw:prof:{object_id}")
        assert "📖 Adrian Vale · PROFILE" in text
        assert "Read-only character profile" in text
        assert "💪 Body" in text
        assert "⚡ Attributes" in text
        assert "🎯 Skills" in text
        assert "❤️ Preferences & Habits" in text
        assert "🛌 Recovery" not in text
        callbacks = _callbacks(keyboard)
        assert f"sw:psec:{object_id}:body" in callbacks
        assert f"sw:psec:{object_id}:skills" in callbacks
        assert f"sw:o:{object_id}" in callbacks
        assert "nav:sandbox" in callbacks
        assert all(not value.startswith("prof:") for value in callbacks)
        assert canonical_state_fingerprint(conn) == before


def test_sandbox_profile_sections_use_shared_formatters_without_fake_runtime(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        character = _character(conn)
        object_id = character["object_id"]

        body_text, body_keyboard = _callback_view(conn, 111, f"sw:psec:{object_id}:body")
        assert "💪 Adrian Vale · BODY" in body_text
        assert "• Height: 6'2\"" in body_text
        assert "• Weight: 200 lb" in body_text
        assert f"sw:prof:{object_id}" in _callbacks(body_keyboard)
        assert "nav:sandbox" in _callbacks(body_keyboard)

        skill_text, _ = _callback_view(conn, 111, f"sw:psec:{object_id}:skills")
        assert "🎯 Adrian Vale · SKILLS" in skill_text
        assert "• Survival   80" in skill_text
        assert "· Fieldcraft" in skill_text
        assert "• Field Medicine   72" in skill_text

        preference_text, _ = _callback_view(
            conn, 111, f"sw:psec:{object_id}:preferences"
        )
        assert "❤️ Adrian Vale · PREFERENCES & HABITS" in preference_text
        assert "quiet outdoor environments" in preference_text
        assert "Hiking" in preference_text
        assert "Equipment checks" in preference_text

        identity_text, _ = _callback_view(conn, 111, f"sw:psec:{object_id}:identity")
        assert "Biological sex" not in identity_text
        assert "Gender" in identity_text

import json

import observer_sandbox.telegram_world_layers_base as world_layers
from observer_sandbox.creation_sandbox import canonical_state_fingerprint, ensure_sandbox
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_character_profile_export import render_sandbox_character_profile_text
from observer_sandbox.sandbox_representation import set_sandbox_profile_values
from observer_sandbox.telegram_sandbox_profile_browser import sandbox_profile_callback_view


CHARACTER_ID = "sbx_character_export_test"
SANDBOX_ID = "creator-default"


def _callbacks(keyboard):
    return {
        button.get("callback_data")
        for row in keyboard or []
        for button in row
        if button.get("callback_data")
    }


def _seed(conn):
    ensure_sandbox(conn, SANDBOX_ID)
    conn.execute(
        """
        INSERT INTO creation_sandbox_objects(
            object_id,sandbox_id,creation_type,schema_version,lifecycle_status,
            identity_json,properties_json,relationships_json,capabilities_json,provenance_json
        ) VALUES(?,?, 'character',1,'active',?,?,?,?,?)
        """,
        (
            CHARACTER_ID,
            SANDBOX_ID,
            json.dumps({"name": "Export Test", "kind": "Character"}),
            json.dumps({"compatibility_tags": ["test"]}),
            "[]",
            json.dumps(["inspect"]),
            json.dumps({"mode": "manual", "requested_by": "telegram:1"}),
        ),
    )
    conn.commit()
    set_sandbox_profile_values(
        conn,
        CHARACTER_ID,
        {
            "identity.full_name": "Export Test",
            "identity.sex": "male",
            "raps_pa.strength": 72.0,
        },
        authority="creator",
        source="profile-export-test",
    )
    # Prove the export reads the current approved value rather than original creation state.
    set_sandbox_profile_values(
        conn,
        CHARACTER_ID,
        {"raps_pa.strength": 81.0},
        authority="creator",
        source="profile-export-edit-test",
    )
    conn.execute(
        """
        INSERT INTO creation_sandbox_character_skills(
            object_id,skill_key,category,score,tier,experience,metadata_json
        ) VALUES(?,?,?,?,?,?,?)
        """,
        (CHARACTER_ID, "first_aid", "medical", 67.0, "B", 120.0, "{}"),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_character_preferences(object_id,preference_type,subject,intensity) VALUES(?,?,?,?)",
        (CHARACTER_ID, "likes", "quiet mornings", 80.0),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_character_hobbies(object_id,name,proficiency,frequency,enjoyment) VALUES(?,?,?,?,?)",
        (CHARACTER_ID, "Hiking", 55.0, "weekly", 90.0),
    )
    conn.execute(
        "INSERT INTO creation_sandbox_character_habits(object_id,name,description,frequency,strength) VALUES(?,?,?,?,?)",
        (CHARACTER_ID, "Hydration", "Carries water", "daily", 75.0),
    )
    conn.commit()


def test_full_profile_renderer_exports_current_approved_character_snapshot(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed(conn)
        before = canonical_state_fingerprint(conn)
        filename, text = render_sandbox_character_profile_text(conn, CHARACTER_ID)
        after = canonical_state_fingerprint(conn)

        assert filename == "sandbox-character-export-test-full-profile.txt"
        assert "SANDBOX CHARACTER — FULL PROFILE SNAPSHOT" in text
        assert "identity.full_name | Full Name: Export Test" in text
        assert "identity.sex" in text
        assert "raps_pa.strength" in text
        assert "81.0" in text
        assert "profile-export-edit-test" in text
        assert "first_aid | category=medical | score=67.0" in text
        assert "likes: quiet mornings | intensity=80.0" in text
        assert "Hiking | proficiency=55.0 | frequency=weekly | enjoyment=90.0" in text
        assert "Hydration | Carries water | frequency=daily | strength=75.0" in text
        assert "Live runtime-owned changing state is intentionally outside this profile export." in text
        assert before == after


def test_character_detail_and_profile_menu_expose_same_export_callback(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed(conn)
        _, detail_keyboard = world_layers.sandbox_object_view(conn, CHARACTER_ID)
        assert f"sw:pexport:{CHARACTER_ID}" in _callbacks(detail_keyboard)

        _, profile_keyboard = sandbox_profile_callback_view(
            conn, f"sw:prof:{CHARACTER_ID}", role="owner"
        )
        assert f"sw:pexport:{CHARACTER_ID}" in _callbacks(profile_keyboard)


def test_export_callback_delivers_txt_without_mutating_state(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    delivered = {}

    with connect(db) as conn:
        _seed(conn)
        before = canonical_state_fingerprint(conn)

        def fake_send(inner_conn, object_id, *, chat_id):
            delivered.update(object_id=object_id, chat_id=chat_id)
            return "sandbox-character-export-test-full-profile.txt"

        monkeypatch.setattr(world_layers, "send_sandbox_character_profile_document", fake_send)
        monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")
        text, keyboard = world_layers.world_layer_callback_view(
            conn, f"sw:pexport:{CHARACTER_ID}"
        )

        assert delivered == {"object_id": CHARACTER_ID, "chat_id": 123}
        assert "Full profile exported: sandbox-character-export-test-full-profile.txt" in text
        assert f"sw:pexport:{CHARACTER_ID}" in _callbacks(keyboard)
        assert canonical_state_fingerprint(conn) == before

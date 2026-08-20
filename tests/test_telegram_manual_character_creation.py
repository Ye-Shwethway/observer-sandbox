from observer_sandbox.creator_studio import manual_draft
from observer_sandbox.db import connect, migrate
from observer_sandbox.manual_character_creation import update_manual_character_field
from observer_sandbox.telegram_creator_studio import (
    draft_preview_view,
    manual_character_builder_view,
    studio_callback_view,
)


def _conn(tmp_path):
    conn = connect(tmp_path / "manual-character-ui.sqlite3")
    migrate(conn)
    return conn


def _button_callbacks(keyboard):
    return [button["callback_data"] for row in keyboard for button in row]


def _fill_required_baseline(conn, user_id=42):
    values = {
        "identity.date_of_birth": "2001-05-12",
        "identity.sex": "male",
        "identity.gender": "man",
        "body.height_in": "74",
        "body.weight_lb": "190",
        "body.body_fat_pct": "12",
        "personality.primary_motivation": "Protect the people he cares about",
        "personality.primary_traits": '["calm","disciplined"]',
        "background.origins": "Raised in a mountain town.",
    }
    for key, raw in values.items():
        update_manual_character_field(conn, user_id, key, raw)


def test_manual_character_builder_exposes_full_creation_sections_and_collections(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        text, keyboard = manual_character_builder_view(conn, 42)
        callbacks = _button_callbacks(keyboard)

        assert "MANUAL CHARACTER BUILD" in text
        assert "Required baseline: 1/10" in text
        assert "sw:cs:manual:s:identity:0" in callbacks
        assert "sw:cs:manual:s:appearance:0" in callbacks
        assert "sw:cs:manual:s:body:0" in callbacks
        assert "sw:cs:manual:s:attributes:0" in callbacks
        assert "sw:cs:manual:s:sexual:0" in callbacks
        assert "sw:cs:manual:s:personality:0" in callbacks
        assert "sw:cs:manual:s:background:0" in callbacks
        assert "sw:cs:manual:c:skills" in callbacks
        assert "sw:cs:manual:c:preferences" in callbacks
        assert "sw:cs:manual:c:hobbies" in callbacks
        assert "sw:cs:manual:c:habits" in callbacks
        assert "sw:cs:manual:c:compatibility_tags" in callbacks


def test_manual_draft_preview_locks_approval_until_required_baseline_is_complete(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        text, keyboard = draft_preview_view(conn, 42)
        callbacks = _button_callbacks(keyboard)

        assert "Manual required baseline: 1/10" in text
        assert "sw:cs:approve" not in callbacks
        assert "sw:cs:manual:home" in callbacks

        _fill_required_baseline(conn)
        text, keyboard = draft_preview_view(conn, 42)
        callbacks = _button_callbacks(keyboard)
        assert "Manual required baseline: 10/10" in text
        assert "sw:cs:approve" in callbacks


def test_manual_character_section_uses_registry_fields_and_opens_typed_input(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        text, keyboard = studio_callback_view(conn, 42, "sw:cs:manual:s:identity:0")
        assert "MANUAL CHARACTER · IDENTITY" in text
        field_callbacks = [value for value in _button_callbacks(keyboard) if value.startswith("sw:cs:manual:f:identity:")]
        assert field_callbacks

        text, keyboard = studio_callback_view(conn, 42, field_callbacks[0])
        assert "MANUAL CHARACTER FIELD" in text
        assert "Expected:" in text
        assert "sw:cs:manual:cancelinput" in _button_callbacks(keyboard)


def test_manual_approval_confirmation_still_uses_revision_lock(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        _fill_required_baseline(conn)

        text, keyboard = studio_callback_view(conn, 42, "sw:cs:approve")
        assert "CONFIRM SANDBOX APPROVAL" in text
        confirm = keyboard[0][0]["callback_data"]
        assert confirm.startswith("sw:cs:approve:confirm:")

        update_manual_character_field(conn, 42, "appearance.eye_color", "green")
        before = conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]
        text, _keyboard = studio_callback_view(conn, 42, confirm)
        assert "Draft changed after confirmation" in text
        assert conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0] == before

import json

from observer_sandbox.creator_studio import manual_draft
from observer_sandbox.db import connect
from observer_sandbox.manual_character_creation import (
    manual_character_baseline_status,
    manual_character_required_field_keys,
    update_manual_character_field,
)
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_studio import (
    _manual_fields,
    draft_preview_view,
    manual_character_builder_view,
    studio_callback_view,
)


def _conn(tmp_path):
    db = tmp_path / "manual-character-ui.sqlite3"
    initialize(db)
    return connect(db)


def _button_callbacks(keyboard):
    return [button["callback_data"] for row in keyboard for button in row]


def _manual_value(key: str, data_type: str):
    specials = {
        "identity.full_name": "Rowan Hale",
        "identity.date_of_birth": "2001-05-12",
        "identity.sex": "male",
        "identity.gender": "man",
        "body.height_in": 74,
        "genetics.height_max_in": 76,
        "body.weight_lb": 190,
        "body.body_fat_pct": 12,
        "genetics.weight_lean_min_lb": 150,
        "genetics.weight_lean_max_lb": 220,
        "genetics.body_fat_floor_pct": 6,
        "body.neck_in": 16,
        "body.shoulders_in": 48,
        "body.chest_in": 42,
        "body.waist_in": 32,
        "body.hips_in": 38,
        "body.biceps_relaxed_in": 15,
        "body.biceps_flexed_in": 16,
        "body.triceps_in": 14,
        "body.forearms_in": 13,
        "body.thighs_in": 23,
        "body.calves_in": 16,
        "genetics.waist_target_in": 32,
        "sexual_anatomy.penis_length_in": 6,
        "sexual_anatomy.penis_girth_in": 5,
        "genetics.penis_length_in": 6,
        "genetics.penis_girth_in": 5,
        "training.training_age_years": 0,
        "raps_ia.iq": 120,
    }
    if key in specials:
        value = specials[key]
    elif key.startswith("genetics.") and data_type in {"number", "integer"}:
        value = 60
    elif data_type == "number":
        value = 50
    elif data_type == "integer":
        value = 1
    elif data_type == "boolean":
        value = True
    elif data_type == "date":
        value = "2001-05-12"
    elif data_type == "datetime":
        value = "2025-05-01T07:00:00+00:00"
    elif data_type == "json":
        value = []
    else:
        value = "manual value"
    return json.dumps(value) if data_type == "json" else str(value).lower() if isinstance(value, bool) else str(value)


def _fill_exact_seed(conn, user_id=42):
    for key in manual_character_required_field_keys(conn):
        row = conn.execute("SELECT data_type FROM profile_field_definitions WHERE field_key=?", (key,)).fetchone()
        assert row is not None
        update_manual_character_field(conn, user_id, key, _manual_value(key, str(row["data_type"])))


def test_manual_character_builder_exposes_full_creation_sections_and_collections(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        status = manual_character_baseline_status(conn, 42)
        text, keyboard = manual_character_builder_view(conn, 42)
        callbacks = _button_callbacks(keyboard)

        assert "MANUAL CHARACTER BUILD" in text
        assert f"Exact seed fields: 1/{status['total']}" in text
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


def test_manual_draft_preview_locks_approval_until_exact_field_set_is_complete(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        initial = manual_character_baseline_status(conn, 42)
        text, keyboard = draft_preview_view(conn, 42)
        callbacks = _button_callbacks(keyboard)

        assert f"Manual exact seed fields: 1/{initial['total']}" in text
        assert "sw:cs:approve" not in callbacks
        assert "sw:cs:manual:home" in callbacks

        _fill_exact_seed(conn)
        complete = manual_character_baseline_status(conn, 42)
        text, keyboard = draft_preview_view(conn, 42)
        callbacks = _button_callbacks(keyboard)
        assert complete["ready"] is True
        assert f"Manual exact seed fields: {complete['total']}/{complete['total']}" in text
        assert "sw:cs:approve" in callbacks


def test_manual_character_section_uses_exact_ai_field_set_and_opens_typed_input(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        attribute_keys = {str(item["field_key"]) for item in _manual_fields(conn, "attributes")}
        assert "raps_pa.practical_skills" in attribute_keys
        assert "raps_pa.practical_skill" not in attribute_keys

        text, keyboard = studio_callback_view(conn, 42, "sw:cs:manual:s:identity:0")
        assert "MANUAL CHARACTER · IDENTITY" in text
        field_callbacks = [value for value in _button_callbacks(keyboard) if value.startswith("sw:cs:manual:f:identity:")]
        assert field_callbacks

        text, keyboard = studio_callback_view(conn, 42, field_callbacks[0])
        assert "MANUAL CHARACTER FIELD" in text
        assert "Expected:" in text
        assert "sw:cs:manual:s:identity:0" in _button_callbacks(keyboard)


def test_manual_field_save_returns_to_same_section_and_page(tmp_path, monkeypatch):
    db = tmp_path / "manual-character-section-return.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "42")

    with connect(db) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        fields = _manual_fields(conn, "attributes")
        assert len(fields) > 12
        target = fields[12]
        key = str(target["field_key"])
        raw = _manual_value(key, str(target["data_type"]))

        text, keyboard = studio_callback_view(conn, 42, "sw:cs:manual:f:attributes:12")
        assert "MANUAL CHARACTER FIELD" in text
        assert "sw:cs:manual:s:attributes:1" in _button_callbacks(keyboard)

    from observer_sandbox import telegram_bot as base

    result = base.handle_command(db, user_id=42, text=raw)
    callbacks = _button_callbacks(base._command_keyboard(""))
    assert "MANUAL CHARACTER · ATTRIBUTES" in result
    assert "Page 2/" in result
    assert "✅ Draft field updated." in result
    assert "sw:cs:manual:home" in callbacks
    assert any(value.startswith("sw:cs:manual:f:attributes:") for value in callbacks)


def test_manual_approval_confirmation_still_uses_revision_lock(tmp_path):
    with _conn(tmp_path) as conn:
        manual_draft(conn, 42, "character", "Rowan Hale")
        _fill_exact_seed(conn)

        text, keyboard = studio_callback_view(conn, 42, "sw:cs:approve")
        assert "CONFIRM SANDBOX APPROVAL" in text
        confirm = keyboard[0][0]["callback_data"]
        assert confirm.startswith("sw:cs:approve:confirm:")

        update_manual_character_field(conn, 42, "appearance.eye_color", "green")
        before = conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0]
        text, _keyboard = studio_callback_view(conn, 42, confirm)
        assert "Draft changed after confirmation" in text
        assert conn.execute("SELECT COUNT(*) FROM creation_sandbox_objects").fetchone()[0] == before

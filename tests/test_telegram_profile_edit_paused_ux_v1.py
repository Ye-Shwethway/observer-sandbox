from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import runtime_value, set_runtime_value
from observer_sandbox.telegram_profile_edit_ui import unpack_profile_edit_ui
from observer_sandbox.telegram_runtime_bot import _callback_view, handle_command


def _button_callback(keyboard, contains):
    for row in keyboard or []:
        for button in row:
            if contains in button.get("text", ""):
                return button["callback_data"]
    raise AssertionError(f"button containing {contains!r} not found")


def test_profile_menu_exposes_edit_only_to_creator_and_edit_mode_pauses_then_restores(monkeypatch, tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "456")

    with connect(db) as conn:
        owner_text, owner_keyboard = _callback_view(conn, 123, "prof:char_darian")
        allowed_text, allowed_keyboard = _callback_view(conn, 456, "prof:char_darian")
        assert "PROFILE" in owner_text and "PROFILE" in allowed_text
        assert _button_callback(owner_keyboard, "Edit Profile") == "pedit:enter:char_darian"
        assert not any("Edit Profile" in button.get("text", "") for row in allowed_keyboard for button in row)
        assert runtime_value(conn, "paused", False) is False

        edit_text, edit_keyboard = _callback_view(conn, 123, "pedit:enter:char_darian")
        assert "UNIVERSE PAUSED" in edit_text
        assert "restore the universe to its previous pause state" in edit_text
        assert runtime_value(conn, "paused", False) is True
        assert _button_callback(edit_keyboard, "Done Editing") == "pedit:done"

        done_text, done_keyboard = _callback_view(conn, 123, "pedit:done")
        assert "EDIT MODE CLOSED" in done_text
        assert "Universe resumed" in done_text
        assert runtime_value(conn, "paused", False) is False
        assert _button_callback(done_keyboard, "Profile") == "prof:char_darian"


def test_profile_edit_preserves_preexisting_pause_state(monkeypatch, tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")

    with connect(db) as conn:
        set_runtime_value(conn, "paused", True)
        conn.commit()
        _callback_view(conn, 123, "pedit:enter:char_darian")
        assert runtime_value(conn, "paused", False) is True
        done_text, _ = _callback_view(conn, 123, "pedit:done")
        assert "remains paused" in done_text
        assert runtime_value(conn, "paused", False) is True


def test_creator_can_edit_field_entirely_inside_profile_ux_and_apply_while_paused(monkeypatch, tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")

    with connect(db) as conn:
        _callback_view(conn, 123, "pedit:enter:char_darian")
        section_text, section_keyboard = _callback_view(conn, 123, "pedit:s:attributes")
        assert "ATTRIBUTES EDIT" in section_text
        strength_callback = _button_callback(section_keyboard, "Strength:")
        prompt_text, _ = _callback_view(conn, 123, strength_callback)
        assert "EDIT STRENGTH" in prompt_text
        assert "Send the new value" in prompt_text
        assert runtime_value(conn, "paused", False) is True

    packed = handle_command(db, user_id=123, text="68")
    preview = unpack_profile_edit_ui(packed)
    assert preview is not None
    preview_text, preview_keyboard = preview
    assert "PROFILE CHANGE PREVIEW" in preview_text
    assert "Strength: 90" in preview_text
    assert "→ 68" in preview_text
    apply_callback = _button_callback(preview_keyboard, "Apply Change")

    with connect(db) as conn:
        before = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key='raps_pa.strength'"
        ).fetchone()[0]
        assert before == "90"
        applied_text, applied_keyboard = _callback_view(conn, 123, apply_callback)
        assert "PROFILE UPDATE APPLIED" in applied_text
        assert "Universe remains paused" in applied_text
        assert runtime_value(conn, "paused", False) is True
        after = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key='raps_pa.strength'"
        ).fetchone()[0]
        assert float(after) == 68.0
        assert _button_callback(applied_keyboard, "Done Editing") == "pedit:done"

        _callback_view(conn, 123, "pedit:done")
        assert runtime_value(conn, "paused", False) is False


def test_grade_target_is_available_as_native_buttons_and_keeps_universe_paused(monkeypatch, tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")

    with connect(db) as conn:
        _callback_view(conn, 123, "pedit:enter:char_darian")
        groups_text, groups_keyboard = _callback_view(conn, 123, "pedit:grades")
        assert "GRADE TARGET" in groups_text
        physical_callback = _button_callback(groups_keyboard, "Physical Attributes")
        _, grade_keyboard = _callback_view(conn, 123, physical_callback)
        grade_b_callback = _button_callback(grade_keyboard, "B · Preserve")
        preview_text, preview_keyboard = _callback_view(conn, 123, grade_b_callback)
        assert "Target: physical → Grade B" in preview_text
        assert "Overall:" in preview_text
        assert "→ B 67.5" in preview_text
        assert runtime_value(conn, "paused", False) is True
        assert _button_callback(preview_keyboard, "Apply Change").startswith("pedit:apply:")

import json

import pytest

from observer_sandbox.creation_sandbox import ensure_sandbox
from observer_sandbox.creator_profile_edit import CreatorProfileEditError
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_representation import set_sandbox_profile_values
from observer_sandbox.sandbox_runtime import (
    ensure_sandbox_runtime,
    sandbox_runtime_status,
    set_sandbox_paused,
)
from observer_sandbox.telegram_sandbox_profile_browser import sandbox_profile_callback_view
from observer_sandbox.telegram_sandbox_profile_edit import (
    enter_sandbox_profile_edit,
    exit_sandbox_profile_edit,
    get_sandbox_profile_edit_session,
    handle_sandbox_profile_edit_text,
    sandbox_field_prompt_view,
    sandbox_profile_edit_callback_view,
    sandbox_section_edit_view,
)


SANDBOX_ID = "profile-edit-test"
CHARACTER_ID = "sbx_character_profile_edit_test"
USER_ID = 123


def _seed_sandbox_character(conn):
    ensure_sandbox(conn, SANDBOX_ID, label="Profile Edit Test")
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
            json.dumps({"name": "Adrian Test", "kind": "Character"}),
            "{}",
            "[]",
            "[]",
            json.dumps({"source": "test"}),
        ),
    )
    conn.commit()
    set_sandbox_profile_values(
        conn,
        CHARACTER_ID,
        {
            "identity.name": "Adrian Test",
            "raps_pa.strength": 72.0,
        },
        authority="creator",
        source="test",
    )
    ensure_sandbox_runtime(conn, SANDBOX_ID)


def _canonical_snapshot(conn):
    profile = conn.execute(
        """
        SELECT field_key,value_json,mode,authority,source
        FROM character_profile_values
        WHERE entity_id='char_darian'
        ORDER BY field_key
        """
    ).fetchall()
    runtime = conn.execute(
        "SELECT key,value_json FROM runtime_state ORDER BY key"
    ).fetchall()
    return (
        tuple(tuple(row) for row in profile),
        tuple(tuple(row) for row in runtime),
    )


def test_sandbox_profile_menu_exposes_creator_edit_entry(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_sandbox_character(conn)
        text, keyboard = sandbox_profile_callback_view(
            conn, f"sw:prof:{CHARACTER_ID}", role="owner"
        )
        assert "Adrian Test" in text
        callbacks = [button["callback_data"] for row in keyboard for button in row]
        assert f"sw:pedit:enter:{CHARACTER_ID}" in callbacks


def test_sandbox_profile_edit_preview_apply_and_pause_are_isolated(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_sandbox_character(conn)
        set_sandbox_paused(conn, False, sandbox_id=SANDBOX_ID)
        canonical_before = _canonical_snapshot(conn)
        revision_before = conn.execute(
            "SELECT revision FROM creation_sandboxes WHERE sandbox_id=?", (SANDBOX_ID,)
        ).fetchone()[0]

        text, _ = enter_sandbox_profile_edit(
            conn, user_id=USER_ID, character_id=CHARACTER_ID
        )
        assert "SANDBOX WORLD PAUSED" in text
        assert sandbox_runtime_status(conn, SANDBOX_ID)["paused"] is True
        session = get_sandbox_profile_edit_session(user_id=USER_ID)
        assert session["was_paused_before_edit"] is False

        _, keyboard = sandbox_section_edit_view(
            conn, user_id=USER_ID, section_id="physical"
        )
        field_callbacks = [
            button["callback_data"]
            for row in keyboard
            for button in row
            if button["callback_data"].startswith("sw:pedit:f:")
        ]
        assert field_callbacks
        strength_index = None
        session = get_sandbox_profile_edit_session(user_id=USER_ID)
        for index, field_key in enumerate(session["field_picker_keys"]):
            if field_key == "raps_pa.strength":
                strength_index = index
                break
        assert strength_index is not None

        prompt, _ = sandbox_field_prompt_view(
            conn, user_id=USER_ID, index=strength_index
        )
        assert "Send the new value" in prompt
        preview = handle_sandbox_profile_edit_text(
            conn, user_id=USER_ID, text="81"
        )
        assert preview is not None
        assert "72.0 → 81.0" in preview[0]
        stored_before_apply = conn.execute(
            """
            SELECT value_json FROM creation_sandbox_profile_values
            WHERE object_id=? AND field_key='raps_pa.strength'
            """,
            (CHARACTER_ID,),
        ).fetchone()[0]
        assert float(json.loads(stored_before_apply)) == 72.0
        assert _canonical_snapshot(conn) == canonical_before

        applied, _ = sandbox_profile_edit_callback_view(
            conn, user_id=USER_ID, callback_data="sw:pedit:apply"
        )
        assert "SANDBOX PROFILE UPDATE APPLIED" in applied
        stored_after_apply = conn.execute(
            """
            SELECT value_json FROM creation_sandbox_profile_values
            WHERE object_id=? AND field_key='raps_pa.strength'
            """,
            (CHARACTER_ID,),
        ).fetchone()[0]
        assert float(json.loads(stored_after_apply)) == 81.0
        revision_after = conn.execute(
            "SELECT revision FROM creation_sandboxes WHERE sandbox_id=?", (SANDBOX_ID,)
        ).fetchone()[0]
        assert revision_after == revision_before + 1
        event = conn.execute(
            """
            SELECT payload_json FROM creation_sandbox_events
            WHERE sandbox_id=? AND object_id=? AND event_type='sandbox_profile_field_edited'
            ORDER BY id DESC LIMIT 1
            """,
            (SANDBOX_ID, CHARACTER_ID),
        ).fetchone()
        assert event is not None
        payload = json.loads(event[0])
        assert payload["field_key"] == "raps_pa.strength"
        assert payload["old_value"] == 72.0
        assert payload["new_value"] == 81.0
        assert _canonical_snapshot(conn) == canonical_before

        closed, _ = exit_sandbox_profile_edit(conn, user_id=USER_ID)
        assert "PROFILE EDIT MODE CLOSED" in closed
        assert sandbox_runtime_status(conn, SANDBOX_ID)["paused"] is False
        assert _canonical_snapshot(conn) == canonical_before


def test_sandbox_profile_edit_restores_preexisting_pause_and_rejects_bad_value(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed_sandbox_character(conn)
        assert sandbox_runtime_status(conn, SANDBOX_ID)["paused"] is True
        canonical_before = _canonical_snapshot(conn)
        enter_sandbox_profile_edit(conn, user_id=USER_ID + 1, character_id=CHARACTER_ID)
        sandbox_section_edit_view(conn, user_id=USER_ID + 1, section_id="physical")
        session = get_sandbox_profile_edit_session(user_id=USER_ID + 1)
        strength_index = session["field_picker_keys"].index("raps_pa.strength")
        sandbox_field_prompt_view(conn, user_id=USER_ID + 1, index=strength_index)

        with pytest.raises(CreatorProfileEditError):
            handle_sandbox_profile_edit_text(conn, user_id=USER_ID + 1, text="not-a-number")
        stored = conn.execute(
            """
            SELECT value_json FROM creation_sandbox_profile_values
            WHERE object_id=? AND field_key='raps_pa.strength'
            """,
            (CHARACTER_ID,),
        ).fetchone()[0]
        assert float(json.loads(stored)) == 72.0
        assert _canonical_snapshot(conn) == canonical_before

        exit_sandbox_profile_edit(conn, user_id=USER_ID + 1)
        assert sandbox_runtime_status(conn, SANDBOX_ID)["paused"] is True
        assert _canonical_snapshot(conn) == canonical_before

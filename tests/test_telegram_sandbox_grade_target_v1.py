import json

from observer_sandbox.creation_sandbox import ensure_sandbox
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_representation import replace_sandbox_skills, set_sandbox_profile_values
from observer_sandbox.sandbox_runtime import ensure_sandbox_runtime
from observer_sandbox.telegram_sandbox_grade_target import sandbox_profile_edit_callback_view

SANDBOX_ID = "sandbox-grade-target-test"
CHARACTER_ID = "sbx_grade_target_character"
USER_ID = 555


def _seed(conn):
    ensure_sandbox(conn, SANDBOX_ID, label="Grade Target Test")
    conn.execute(
        """
        INSERT INTO creation_sandbox_objects(
            object_id,sandbox_id,creation_type,schema_version,lifecycle_status,
            identity_json,properties_json,relationships_json,capabilities_json,provenance_json
        ) VALUES(?,?, 'character',1,'active',?,?,?,?,?)
        """,
        (CHARACTER_ID, SANDBOX_ID, json.dumps({"name": "Sandbox Target"}), "{}", "[]", "[]", "{}"),
    )
    conn.commit()
    set_sandbox_profile_values(
        conn,
        CHARACTER_ID,
        {
            "raps_pa.strength": 62.0,
            "raps_pa.stamina": 64.0,
            "raps_pa.agility": 66.0,
            "raps_pa.speed": 68.0,
        },
        source="test",
    )
    replace_sandbox_skills(
        conn,
        CHARACTER_ID,
        [
            {"skill_key": "survival", "score": 61.0},
            {"skill_key": "tracking", "score": 65.0},
        ],
    )
    ensure_sandbox_runtime(conn, SANDBOX_ID)


def _real_snapshot(conn):
    profile = conn.execute(
        "SELECT entity_id,field_key,value_json FROM character_profile_values ORDER BY entity_id,field_key"
    ).fetchall()
    skills = conn.execute(
        "SELECT entity_id,skill_key,score FROM character_skills ORDER BY entity_id,skill_key"
    ).fetchall()
    return tuple(tuple(row) for row in profile), tuple(tuple(row) for row in skills)


def test_sandbox_editor_reuses_real_world_grade_target_format(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed(conn)
        text, keyboard = sandbox_profile_edit_callback_view(
            conn, user_id=USER_ID, callback_data=f"sw:pedit:enter:{CHARACTER_ID}"
        )
        assert "Choose a profile section or a grade target." in text
        callbacks = [b["callback_data"] for row in keyboard for b in row]
        assert "sw:pedit:grades" in callbacks

        text, keyboard = sandbox_profile_edit_callback_view(
            conn, user_id=USER_ID, callback_data="sw:pedit:grades"
        )
        assert "🎯 GRADE TARGET" in text
        labels = [b["text"] for row in keyboard for b in row]
        assert "Body Measurements" in labels
        assert "Physical Attributes" in labels
        assert "All Skills" in labels

        text, keyboard = sandbox_profile_edit_callback_view(
            conn, user_id=USER_ID, callback_data="sw:pedit:gg:physical"
        )
        assert "PRESERVE" in " ".join(b["text"].upper() for row in keyboard for b in row)
        callbacks = [b["callback_data"] for row in keyboard for b in row]
        assert "sw:pedit:gt:physical:A:p" in callbacks
        assert "sw:pedit:gt:physical:A:n" in callbacks


def test_sandbox_attribute_grade_target_preview_apply_is_real_world_isolated(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed(conn)
        real_before = _real_snapshot(conn)
        revision_before = conn.execute(
            "SELECT revision FROM creation_sandboxes WHERE sandbox_id=?", (SANDBOX_ID,)
        ).fetchone()[0]
        sandbox_profile_edit_callback_view(conn, user_id=USER_ID + 1, callback_data=f"sw:pedit:enter:{CHARACTER_ID}")
        preview, _ = sandbox_profile_edit_callback_view(
            conn, user_id=USER_ID + 1, callback_data="sw:pedit:gt:physical:A:p"
        )
        assert "Target: physical → Grade A" in preview
        assert "Apply changes Sandbox state only" in preview
        assert _real_snapshot(conn) == real_before

        applied, _ = sandbox_profile_edit_callback_view(
            conn, user_id=USER_ID + 1, callback_data="sw:pedit:gapply"
        )
        assert "Verified grade: A" in applied
        values = [
            float(json.loads(row[0]))
            for row in conn.execute(
                "SELECT value_json FROM creation_sandbox_profile_values WHERE object_id=? AND field_key LIKE 'raps_pa.%' ORDER BY field_key",
                (CHARACTER_ID,),
            ).fetchall()
        ]
        assert 75.0 <= sum(values) / len(values) < 90.0
        revision_after = conn.execute(
            "SELECT revision FROM creation_sandboxes WHERE sandbox_id=?", (SANDBOX_ID,)
        ).fetchone()[0]
        assert revision_after == revision_before + 1
        event = conn.execute(
            "SELECT payload_json FROM creation_sandbox_events WHERE sandbox_id=? AND event_type='sandbox_profile_grade_target_applied' ORDER BY id DESC LIMIT 1",
            (SANDBOX_ID,),
        ).fetchone()
        assert event is not None
        payload = json.loads(event[0])
        assert payload["group"] == "physical"
        assert payload["target_grade"] == "A"
        assert _real_snapshot(conn) == real_before


def test_sandbox_skill_grade_target_reuses_same_grade_method(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _seed(conn)
        real_before = _real_snapshot(conn)
        sandbox_profile_edit_callback_view(conn, user_id=USER_ID + 2, callback_data=f"sw:pedit:enter:{CHARACTER_ID}")
        preview, _ = sandbox_profile_edit_callback_view(
            conn, user_id=USER_ID + 2, callback_data="sw:pedit:gt:skills:S:n"
        )
        assert "Target: skills → Grade S" in preview
        sandbox_profile_edit_callback_view(conn, user_id=USER_ID + 2, callback_data="sw:pedit:gapply")
        scores = [row[0] for row in conn.execute(
            "SELECT score FROM creation_sandbox_character_skills WHERE object_id=? ORDER BY skill_key", (CHARACTER_ID,)
        ).fetchall()]
        assert scores == [95.0, 95.0]
        assert _real_snapshot(conn) == real_before

import re

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_runtime_bot import handle_command


def test_creator_profile_commands_are_owner_only_preview_first_and_apply(monkeypatch, tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "456")

    denied = handle_command(
        db,
        user_id=456,
        text="/profileedit char_darian raps_pa.strength 68",
    )
    assert "Creator authority required" in denied

    preview = handle_command(
        db,
        user_id=123,
        text="/profileedit char_darian raps_pa.strength 68",
    )
    assert "CREATOR PROFILE PREVIEW" in preview
    assert "Strength" in preview
    assert "90" in preview and "68" in preview
    token_match = re.search(r"/profileapply ([0-9a-f]{12})", preview)
    assert token_match is not None

    with connect(db) as conn:
        before = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key='raps_pa.strength'"
        ).fetchone()[0]
        assert before == "90"

    applied = handle_command(db, user_id=123, text=f"/profileapply {token_match.group(1)}")
    assert "CREATOR PROFILE UPDATE APPLIED" in applied
    with connect(db) as conn:
        after = conn.execute(
            "SELECT value_json FROM character_profile_values WHERE entity_id='char_darian' AND field_key='raps_pa.strength'"
        ).fetchone()[0]
        assert float(after) == 68.0


def test_creator_can_preview_physical_grade_b_from_telegram(monkeypatch, tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "123")

    preview = handle_command(
        db,
        user_id=123,
        text="/profilegrade char_darian physical B preserve",
    )
    assert "CREATOR PROFILE PREVIEW" in preview
    assert "physical → Grade B" in preview
    assert "Overall:" in preview
    assert "→ B 67.5" in preview
    assert "/profileapply" in preview

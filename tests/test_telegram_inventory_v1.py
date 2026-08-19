import json

from observer_sandbox import telegram_bot as base
from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_creator_bot import _callback_view, _home_keyboard, handle_command


def _contains_callback(keyboard, callback_data: str) -> bool:
    return any(button.get("callback_data") == callback_data for row in keyboard for button in row)


def test_home_exposes_inventory_under_real_world(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")
    keyboard = _home_keyboard()
    assert _contains_callback(keyboard, "nav:real")
    assert not _contains_callback(keyboard, "inv:home")
    with connect(db) as conn:
        text, real_keyboard = _callback_view(conn, 100, "nav:real")
        assert "REAL WORLD" in text
        assert _contains_callback(real_keyboard, "inv:home")


def test_inventory_home_is_universe_scoped(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        text, keyboard = _callback_view(conn, 100, "inv:home")
        assert "Browse inventory anywhere in the universe" in text
        assert _contains_callback(keyboard, "inv:list:locations:0")
        assert _contains_callback(keyboard, "inv:list:characters:0")
        assert _contains_callback(keyboard, "inv:list:containers:0")
        assert _contains_callback(keyboard, "inv:all:0")


def test_allowed_user_can_browse_but_not_replenish(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "200")

    with connect(db) as conn:
        text, keyboard = _callback_view(conn, 200, "inv:stack:stack_estate_apples")
        assert "Apple" in text
        assert not _contains_callback(keyboard, "inv:replenish:stack_estate_apples")

        denied, _ = _callback_view(conn, 200, "inv:replenish:stack_estate_apples")
        assert "Creator authority required" in denied


def test_owner_replenish_requires_confirmation_and_records_audit(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        before = conn.execute(
            "SELECT quantity FROM inventory_stacks WHERE entity_id='stack_estate_apples'"
        ).fetchone()[0]

        detail, keyboard = _callback_view(conn, 100, "inv:stack:stack_estate_apples")
        assert "Apple" in detail
        assert _contains_callback(keyboard, "inv:replenish:stack_estate_apples")

        prompt, keyboard = _callback_view(conn, 100, "inv:addprompt:stack_estate_apples:24")
        assert "CONFIRM INVENTORY CHANGE" in prompt
        assert _contains_callback(keyboard, "inv:addapply:stack_estate_apples:24")
        unchanged = conn.execute(
            "SELECT quantity FROM inventory_stacks WHERE entity_id='stack_estate_apples'"
        ).fetchone()[0]
        assert unchanged == before

        result, _ = _callback_view(conn, 100, "inv:addapply:stack_estate_apples:24")
        assert "INVENTORY REPLENISHED" in result
        after = conn.execute(
            "SELECT quantity FROM inventory_stacks WHERE entity_id='stack_estate_apples'"
        ).fetchone()[0]
        assert after == before + 24.0
        row = conn.execute(
            "SELECT payload_json FROM events WHERE event_type='creator_inventory_replenished' ORDER BY id DESC LIMIT 1"
        ).fetchone()
        assert row is not None
        payload = json.loads(row[0])
        assert payload["requested_by"] == "telegram:100"


def test_inventory_commands_keep_read_and_write_permissions_separate(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "200")

    browse = handle_command(db, user_id=200, text="/inventory")
    assert "INVENTORY" in browse
    assert "Active stock stacks" in browse

    denied = handle_command(db, user_id=200, text="/replenish stack_estate_apples 12")
    assert "Creator authority required" in denied

    applied = handle_command(db, user_id=100, text="/replenish stack_estate_apples 12")
    assert "INVENTORY REPLENISHED" in applied


def test_location_and_character_inventory_lists_are_generic(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "100")

    with connect(db) as conn:
        locations_text, locations_keyboard = _callback_view(conn, 100, "inv:list:locations:0")
        assert "INVENTORY · LOCATIONS" in locations_text
        assert not _contains_callback(locations_keyboard, "inv:scope:char_darian")

        characters_text, characters_keyboard = _callback_view(conn, 100, "inv:list:characters:0")
        assert "INVENTORY · CHARACTERS" in characters_text
        assert "Darian Thorne" in characters_text
        assert _contains_callback(characters_keyboard, "inv:scope:char_darian")

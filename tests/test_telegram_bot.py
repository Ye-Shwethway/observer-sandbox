from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.telegram_bot import _callback_view, _home_keyboard, _notifications_enabled, handle_command
from observer_sandbox.telegram_notifications import dispatch_action_completion, format_action_completion


def test_unauthorized_user_gets_only_identity_bootstrap(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.delenv("OBSERVER_TELEGRAM_OWNER_ID", raising=False)
    monkeypatch.delenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", raising=False)
    text = handle_command(db, user_id=12345, text="/start")
    assert "12345" in text
    assert "unauthorized" in text
    assert handle_command(db, user_id=12345, text="/status").startswith("Not authorized")


def test_owner_is_authorized_without_duplicate_allowlist_entry(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.delenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", raising=False)
    assert "Role: Owner" in handle_command(db, user_id=111, text="/whoami")
    assert "OBSERVER SANDBOX" in handle_command(db, user_id=111, text="/status")
    start = handle_command(db, user_id=111, text="/start")
    assert "OBSERVER HOME" in start
    assert "Access Owner" in start


def test_allowed_user_is_separate_non_owner_role(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222,333")
    assert "Role: Allowed" in handle_command(db, user_id=222, text="/whoami")
    assert "OBSERVER SANDBOX" in handle_command(db, user_id=222, text="/status")
    assert handle_command(db, user_id=444, text="/status").startswith("Not authorized")


def test_authorized_mvp_commands_and_controls(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "12345")
    status = handle_command(db, user_id=12345, text="/status")
    assert "OBSERVER SANDBOX" in status
    assert "01-05-2025 (Thursday) 07:00 AM" in status
    assert "Darian" in handle_command(db, user_id=12345, text="/darian")
    assert "Thorne Estate" in handle_command(db, user_id=12345, text="/home")
    assert "Recent Activity" in handle_command(db, user_id=12345, text="/history")
    assert "Paused     Yes" in handle_command(db, user_id=12345, text="/pause")
    assert "Paused     No" in handle_command(db, user_id=12345, text="/resume")
    assert "Speed      60.0x" in handle_command(db, user_id=12345, text="/speed 60")


def test_notifications_default_on_and_persist_per_user(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")
    with connect(db) as conn:
        assert _notifications_enabled(conn, 111) is True
        assert _notifications_enabled(conn, 222) is True
    assert "Notifications OFF" in handle_command(db, user_id=111, text="/notify off")
    with connect(db) as conn:
        assert _notifications_enabled(conn, 111) is False
        assert _notifications_enabled(conn, 222) is True
    assert "Notifications ON" in handle_command(db, user_id=111, text="/notion/on")
    assert "Notifications OFF" in handle_command(db, user_id=111, text="/notion/off")


def test_observer_home_uses_stable_inline_navigation(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    keyboard = _home_keyboard()
    assert keyboard[0][0]["callback_data"] == "nav:universe"
    assert keyboard[0][1]["callback_data"] == "nav:characters"
    with connect(db) as conn:
        text, universe_keyboard = _callback_view(conn, 111, "nav:universe")
        assert "UNIVERSE" in text
        assert any(button[0]["callback_data"] == "loc:loc_thorne_estate" for button in universe_keyboard[:-1])
        chars_text, chars_keyboard = _callback_view(conn, 111, "nav:characters")
        assert "Darian Thorne" in chars_text
        assert chars_keyboard[0][0]["callback_data"] == "char:char_darian"


def test_recursive_estate_browser_uses_graph_parent_and_room_details(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        estate_text, estate_keyboard = _callback_view(conn, 111, "loc:loc_thorne_estate")
        assert "Thorne Estate" in estate_text
        assert "Areas" in estate_text
        assert any(row[0]["callback_data"] == "loc:loc_thorne_estate_ground_floor" for row in estate_keyboard)
        assert any("🔒" in row[0]["text"] and row[0]["callback_data"] == "loc:loc_thorne_estate_exterior_boundary" for row in estate_keyboard)
        assert estate_keyboard[-2][0]["callback_data"] == "nav:universe"

        floor_text, floor_keyboard = _callback_view(conn, 111, "loc:loc_thorne_estate_ground_floor")
        assert "Ground Floor" in floor_text
        assert any(row[0]["callback_data"] == "loc:loc_thorne_estate_kitchen" for row in floor_keyboard)
        assert floor_keyboard[-2][0]["callback_data"] == "loc:loc_thorne_estate"

        kitchen_text, kitchen_keyboard = _callback_view(conn, 111, "loc:loc_thorne_estate_kitchen")
        assert "Kitchen" in kitchen_text
        assert "Objects" in kitchen_text
        assert "Exits" in kitchen_text
        assert kitchen_keyboard[-2][0]["callback_data"] == "loc:loc_thorne_estate_ground_floor"
        assert kitchen_keyboard[-1][0]["callback_data"] == "nav:home"


def test_action_completion_notification_is_human_friendly():
    before = {
        "sim_time": "2025-05-01T12:40:00+00:00",
        "location_name": "Kitchen",
        "energy": 23.8,
        "hunger": 63.7,
        "thirst": 28.3,
        "sleepiness": 34.8,
        "cleanliness": 43.2,
    }
    after = {
        "sim_time": "2025-05-01T13:00:00+00:00",
        "location_name": "Kitchen",
        "energy": 31.2,
        "hunger": 14.5,
        "thirst": 31.3,
        "sleepiness": 35.8,
        "cleanliness": 42.9,
    }
    action = {"action": "eat", "target_name": "Meal Ingredients", "reason": "Eating to recover from hunger."}
    text = format_action_completion(action, before, after)
    assert "✨ CHARACTER UPDATE" in text
    assert "Eat → Meal Ingredients" in text
    assert "01-05-2025 (Thursday) 01:00 PM" in text
    assert "Hunger" in text and "63.7 → 14.5" in text
    assert "Energy" in text and "23.8 → 31.2" in text


def test_action_completion_push_obeys_preferences_and_deduplicates(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_BOT_TOKEN", "test-token")
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "111,222")
    sent = []
    monkeypatch.setattr("observer_sandbox.telegram_notifications._send", lambda token, user_id, text: sent.append((user_id, text)))
    handle_command(db, user_id=222, text="/notify off")

    before = {
        "sim_time": "2025-05-01T12:40:00+00:00",
        "location_name": "Kitchen",
        "energy": 23.8,
        "hunger": 63.7,
        "thirst": 28.3,
        "sleepiness": 34.8,
        "cleanliness": 43.2,
    }
    after = {
        "sim_time": "2025-05-01T13:00:00+00:00",
        "location_name": "Kitchen",
        "energy": 31.2,
        "hunger": 14.5,
        "thirst": 31.3,
        "sleepiness": 35.8,
        "cleanliness": 42.9,
    }
    action = {"action": "eat", "target": "obj_thorne_estate_kitchen_meal_ingredients", "reason": "Eating to recover from hunger."}
    with connect(db) as conn:
        assert dispatch_action_completion(conn, action_id="a-1", action=action, before=before, after=after) == 1
        assert dispatch_action_completion(conn, action_id="a-1", action=action, before=before, after=after) == 0
    assert [user_id for user_id, _ in sent] == [111]
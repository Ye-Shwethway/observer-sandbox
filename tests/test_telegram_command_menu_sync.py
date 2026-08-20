import json

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.simulation import set_runtime_value
from observer_sandbox.telegram_command_menu import commands_from_help, sync_bot_commands


def _names(commands):
    return [item["command"] for item in commands]


def test_help_contract_builds_unique_telegram_commands_and_expands_shared_lines():
    commands = commands_from_help(
        "\n".join(
            [
                "/start — Observer Home",
                "/realpause | /realresume — Real World pause control",
                "/history [n] — Recent activity",
                "/start — duplicate should not duplicate menu",
            ]
        )
    )

    assert _names(commands) == ["start", "help", "realpause", "realresume", "history"]
    assert commands[2]["description"] == "Real World pause control"
    assert commands[3]["description"] == "Real World pause control"


def test_final_runtime_help_contract_exposes_current_role_appropriate_menu():
    # Importing the runtime adapter installs the complete bounded Telegram command
    # chain. The menu parser intentionally reads this final role-aware help view.
    from observer_sandbox import telegram_runtime_bot as runtime

    owner = set(_names(commands_from_help(runtime.base._help("owner"))))
    allowed = set(_names(commands_from_help(runtime.base._help("allowed"))))

    assert {
        "start",
        "help",
        "status",
        "watch",
        "history",
        "darian",
        "home",
        "notify",
        "whoami",
        "realstatus",
        "realpause",
        "realresume",
        "realspeed",
        "realtime",
        "sandboxstatus",
        "sandboxpause",
        "sandboxresume",
        "sandboxspeed",
        "sandboxtime",
        "statnotify",
        "inventory",
        "replenish",
        "settings",
        "studio",
        "create",
        "createai",
        "logs",
        "profileedit",
        "profilegrade",
        "profileapply",
    } <= owner

    assert {"start", "help", "status", "realstatus", "statnotify", "inventory", "whoami"} <= allowed
    assert "restorestats" in owner
    assert "restorestats" not in allowed
    assert "studio" not in allowed
    assert "sandboxpause" not in allowed
    assert "logs" not in allowed
    # Legacy world-ambiguous redirects still work but are deliberately not
    # advertised in the refreshed Telegram command menu.
    assert "pause" not in owner
    assert "resume" not in owner
    assert "speed" not in owner


def test_sync_publishes_safe_default_and_role_scoped_chat_menus(tmp_path):
    db = tmp_path / "telegram-command-menu.sqlite3"
    initialize(db)
    calls = []

    def fake_api(token, method, payload=None, *, timeout=30):
        calls.append((token, method, payload, timeout))
        return True

    def help_renderer(role):
        common = "/start — Home\n/status — Status\n/whoami — Identity"
        if role == "owner":
            return common + "\n/studio — Creator Studio\n/realpause — Pause Real World"
        return common

    result = sync_bot_commands(
        fake_api,
        "TOKEN",
        db,
        help_renderer=help_renderer,
        owner_id=42,
        allowed_user_ids={42, 77, 88},
    )

    assert result == {"default": 2, "allowed": 4, "owner": 6, "scoped_chats": 3}
    set_calls = [payload for _token, method, payload, _timeout in calls if method == "setMyCommands"]
    assert len(set_calls) == 4

    default = next(payload for payload in set_calls if json.loads(payload["scope"])["type"] == "default")
    assert _names(json.loads(default["commands"])) == ["start", "whoami"]

    owner = next(payload for payload in set_calls if json.loads(payload["scope"]).get("chat_id") == 42)
    allowed = next(payload for payload in set_calls if json.loads(payload["scope"]).get("chat_id") == 77)
    assert "studio" in _names(json.loads(owner["commands"]))
    assert "realpause" in _names(json.loads(owner["commands"]))
    assert "studio" not in _names(json.loads(allowed["commands"]))
    assert "help" in _names(json.loads(allowed["commands"]))


def test_sync_deletes_removed_private_chat_scope_before_recording_new_set(tmp_path):
    db = tmp_path / "telegram-command-menu-stale.sqlite3"
    initialize(db)
    with connect(db) as conn:
        set_runtime_value(conn, "telegram_command_menu:chat_ids", [42, 77, 999])
        conn.commit()

    calls = []

    def fake_api(token, method, payload=None, *, timeout=30):
        calls.append((method, payload))
        return True

    sync_bot_commands(
        fake_api,
        "TOKEN",
        db,
        help_renderer=lambda role: "/start — Home\n/whoami — Identity",
        owner_id=42,
        allowed_user_ids={77},
    )

    deletes = [payload for method, payload in calls if method == "deleteMyCommands"]
    assert len(deletes) == 1
    assert json.loads(deletes[0]["scope"]) == {"type": "chat", "chat_id": 999}

    with connect(db) as conn:
        stored = conn.execute(
            "SELECT value_json FROM runtime_state WHERE key='telegram_command_menu:chat_ids'"
        ).fetchone()
        assert json.loads(stored["value_json"]) == [42, 77]

from observer_sandbox.db import connect
from observer_sandbox.runtime import initialize
from observer_sandbox.sandbox_runtime import ensure_sandbox_runtime, sandbox_runtime_status
from observer_sandbox.simulation import runtime_value
from observer_sandbox.telegram_creator_bot import _callback_view, handle_command


def _callbacks(keyboard):
    return [button["callback_data"] for row in keyboard or [] for button in row]


def test_ambiguous_runtime_commands_do_not_mutate_either_world(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        ensure_sandbox_runtime(conn)
        real_before = float(runtime_value(conn, "speed", 1.0))
        sandbox_before = sandbox_runtime_status(conn)["speed"]

    reply = handle_command(db, user_id=111, text="/speed 60")
    assert "World required" in reply
    assert "/realspeed" in reply
    assert "/sandboxspeed" in reply

    with connect(db) as conn:
        assert float(runtime_value(conn, "speed", 1.0)) == real_before
        assert sandbox_runtime_status(conn)["speed"] == sandbox_before


def test_real_and_sandbox_speed_commands_are_isolated(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    real_reply = handle_command(db, user_id=111, text="/realspeed 60")
    assert "REAL WORLD RUNTIME" in real_reply
    assert "60x" in real_reply
    with connect(db) as conn:
        assert float(runtime_value(conn, "speed", 1.0)) == 60.0
        assert sandbox_runtime_status(conn)["speed"] == 1.0

    sandbox_reply = handle_command(db, user_id=111, text="/sandboxspeed 120")
    assert "SANDBOX RUNTIME" in sandbox_reply
    assert "120x" in sandbox_reply
    with connect(db) as conn:
        assert float(runtime_value(conn, "speed", 1.0)) == 60.0
        assert sandbox_runtime_status(conn)["speed"] == 120.0


def test_manual_time_controls_auto_pause_only_the_named_world(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")

    with connect(db) as conn:
        ensure_sandbox_runtime(conn)
        real_original = runtime_value(conn, "sim_time", None)

    sandbox_reply = handle_command(db, user_id=111, text="/sandboxtime 2030-01-02T03:04:05+00:00")
    assert "auto-paused" in sandbox_reply
    with connect(db) as conn:
        sandbox = sandbox_runtime_status(conn)
        assert sandbox["paused"] is True
        assert sandbox["sim_time"].startswith("2030-01-02T03:04:05")
        assert runtime_value(conn, "sim_time", None) == real_original

    real_reply = handle_command(db, user_id=111, text="/realtime 2031-02-03T04:05:06+00:00")
    assert "auto-paused" in real_reply
    with connect(db) as conn:
        assert bool(runtime_value(conn, "paused", False)) is True
        assert str(runtime_value(conn, "sim_time", "")).startswith("2031-02-03T04:05:06")
        sandbox = sandbox_runtime_status(conn)
        assert sandbox["sim_time"].startswith("2030-01-02T03:04:05")


def test_real_and_sandbox_runtime_inline_ux_use_separate_namespaces(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    with connect(db) as conn:
        ensure_sandbox_runtime(conn)
        real_text, real_keyboard = _callback_view(conn, 111, "nav:runtime")
        assert "REAL WORLD RUNTIME" in real_text
        real_callbacks = _callbacks(real_keyboard)
        assert any(value.startswith("rw:rt:") for value in real_callbacks)
        assert all(not value.startswith("sw:rt:") for value in real_callbacks)

        sandbox_text, sandbox_keyboard = _callback_view(conn, 111, "sw:runtime")
        assert "SANDBOX RUNTIME" in sandbox_text
        sandbox_callbacks = _callbacks(sandbox_keyboard)
        assert all(not value.startswith("rw:rt:") for value in sandbox_callbacks)


def test_non_owner_cannot_mutate_real_world_runtime(tmp_path, monkeypatch):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    monkeypatch.setenv("OBSERVER_TELEGRAM_OWNER_ID", "111")
    monkeypatch.setenv("OBSERVER_TELEGRAM_ALLOWED_USER_IDS", "222")
    with connect(db) as conn:
        before = float(runtime_value(conn, "speed", 1.0))

    reply = handle_command(db, user_id=222, text="/realspeed 90")
    assert "Creator authority required" in reply
    with connect(db) as conn:
        assert float(runtime_value(conn, "speed", 1.0)) == before

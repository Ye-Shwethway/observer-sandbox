from __future__ import annotations

import json

import pytest

from observer_sandbox.actor_runtime import actor_runtime, set_actor_runtime
from observer_sandbox.actor_selection import DEFAULT_ACTOR_KEY, resolve_actor_id
from observer_sandbox.character_config import load_character_autonomy_policy
from observer_sandbox.db import connect
from observer_sandbox.model_decision import ModelDecisionProvider, load_autonomy_policy
from observer_sandbox.runtime import initialize, status
from observer_sandbox.autonomy import set_autonomy_paused


def _add_character_stub(conn, actor_id: str, name: str) -> None:
    conn.execute(
        "INSERT INTO entities(id,entity_type,name,capabilities_json) VALUES(?,?,?,'[]')",
        (actor_id, "character", name),
    )
    set_actor_runtime(conn, actor_id, autonomy_enabled=False, autonomy_mode="normal", wake_reason=None)
    conn.commit()


def test_single_character_runtime_has_configurable_default_actor(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        assert resolve_actor_id(conn) == "char_darian"
        stored = conn.execute(
            "SELECT value_json FROM runtime_state WHERE key=?", (DEFAULT_ACTOR_KEY,)
        ).fetchone()
        assert stored is not None
        assert json.loads(stored[0]) == "char_darian"

    runtime = status(db).runtime_state
    assert runtime["default_actor_id"] == "char_darian"


def test_multiple_characters_without_default_require_explicit_actor(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_character_stub(conn, "char_fixture", "Fixture Character")
        conn.execute("DELETE FROM runtime_state WHERE key=?", (DEFAULT_ACTOR_KEY,))
        conn.commit()

        with pytest.raises(ValueError, match="Multiple characters"):
            resolve_actor_id(conn)
        assert resolve_actor_id(conn, "char_fixture") == "char_fixture"


def test_unregistered_character_requires_character_seed_even_with_universal_policy(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_character_stub(conn, "char_fixture", "Fixture Character")
        with pytest.raises(KeyError, match="No character config registered"):
            ModelDecisionProvider(conn, character_id="char_fixture")


def test_policy_loader_is_universal_and_not_bound_to_character_identity():
    direct = load_character_autonomy_policy("char_darian")
    implicit = load_autonomy_policy()
    assert implicit == direct
    assert implicit["policy_revision"] == "universal-autonomy-v1-no-character-hardcoding"
    assert "entity_id" not in implicit


def test_universe_resume_wakes_every_enabled_idle_actor(tmp_path):
    db = tmp_path / "observer.sqlite3"
    initialize(db)
    with connect(db) as conn:
        _add_character_stub(conn, "char_fixture", "Fixture Character")
        set_actor_runtime(conn, "char_darian", autonomy_enabled=True, wake_reason=None)
        set_actor_runtime(conn, "char_fixture", autonomy_enabled=True, wake_reason=None)
        conn.commit()

        set_autonomy_paused(conn, True, actor_id="char_darian", now_wall=100.0)
        set_autonomy_paused(conn, False, actor_id="char_darian", now_wall=130.0)

        assert actor_runtime(conn, "char_darian")["wake_reason"] == "resume"
        assert actor_runtime(conn, "char_fixture")["wake_reason"] == "resume"
